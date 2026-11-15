"""Unit tests. They use a tiny made-up index and a scripted fake model, so no key is needed.

  python -m unittest
"""
import json
import unittest

from site_agent.agent import Agent
from site_agent.grounding import check_links
from site_agent.model_client import ChatClient, ModelError
from site_agent.prompt import build_system_prompt
from site_agent.site_index import SiteIndex, tokenize
from site_agent.tools import Tools

SITE = "https://example.org/hub"
CONFIG = {"name": "Example Hub", "description": "A test site.", "siteUrl": SITE + "/",
          "extraPages": ["", "hot-topics/"], "languages": ["English", "Spanish"],
          "feedbackUrl": "https://example.org/issues"}


def make_index() -> SiteIndex:
    def page(route, title, description="", words=300, section=(), **extra):
        return {"url": f"{SITE}/docs/{route}", "path": f"/hub/docs/{route}",
                "text": f"/hub/agent/pages/{route.rstrip('/') or 'index'}.md", "title": title,
                "description": description, "words": words, "section": list(section),
                "headings": [], "tags": [], "topics": [], "audience": [], "disability_type": [],
                "status": "published", **extra}

    pages = [
        page("vision/", "Vision"),
        page("vision/screen-readers/", "Screen Readers", "Software that reads the screen aloud.",
             section=["Vision"], tags=["screen-readers"], headings=["NVDA", "VoiceOver"]),
        page("vision/e-readers/", "Accessible E-Readers", "Devices for reading books.", section=["Vision"]),
        page("hot-topics/color-contrast/", "Color Contrast", words=20, section=["Hot Topics"]),
        page("developers/checklist/", "Accessible Web Development Checklist",
             "Contrast, keyboard and screen reader checks.", section=["Developers"]),
    ]
    texts = {p["path"]: f"# {p['title']}\n\nBody of {p['title']}." for p in pages}
    return SiteIndex({"site": SITE + "/", "pages": pages}, lambda p: texts[p["path"]])


class FakeClient:
    """Returns scripted model messages in order and records what it was sent."""

    def __init__(self, *messages):
        self._messages = list(messages)
        self.requests = []

    def complete(self, messages, tools=None):
        self.requests.append({"messages": [dict(m) for m in messages], "tools": tools})
        return {"message": self._messages.pop(0), "usage": {"prompt_tokens": 10, "completion_tokens": 5}}


def tool_call(name, arguments, call_id="call_1"):
    payload = arguments if isinstance(arguments, str) else json.dumps(arguments)
    return {"role": "assistant", "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name, "arguments": payload}}]}


def text(content):
    return {"role": "assistant", "content": content}


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.index = make_index()

    def test_tokenize_strips_accents_stopwords_and_plurals(self):
        self.assertEqual(tokenize("¿Qué es un lector de Pantallas?"), ["lector", "pantalla"])
        self.assertEqual(tokenize("the screen readers"), ["screen", "reader"])

    def test_title_match_ranks_first(self):
        results = self.index.search("which screen reader can I try")
        self.assertEqual(results[0]["title"], "Screen Readers")

    def test_stub_page_scores_lower_than_the_same_page_with_content(self):
        stub_score = self.index.search("color contrast")[0]["score"]
        full = make_index()
        next(p for p in full.pages if p["title"] == "Color Contrast")["words"] = 300
        full_score = SiteIndex({"pages": full.pages}, lambda p: "").search("color contrast")[0]["score"]
        self.assertAlmostEqual(stub_score, full_score * 0.6, places=1)
        # A search for the topic still returns the real page that covers it.
        self.assertIn("Accessible Web Development Checklist",
                      [r["title"] for r in self.index.search("contrast")])

    def test_no_match_returns_empty(self):
        self.assertEqual(self.index.search("weather in Bogota"), [])

    def test_find_page_accepts_url_path_and_tail(self):
        for value in (f"{SITE}/docs/vision/screen-readers/", "/hub/docs/vision/screen-readers",
                      "vision/screen-readers/", f"{SITE}/docs/vision/screen-readers/#nvda"):
            self.assertEqual(self.index.find_page(value)["title"], "Screen Readers", value)

    def test_find_page_rejects_ambiguous_or_unknown(self):
        self.assertIsNone(self.index.find_page("nothing/here/"))
        self.assertEqual(self.index.find_page("docs/vision/")["title"], "Vision")


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tools = Tools(make_index(), max_page_chars=20)

    def test_search_site_returns_results(self):
        output = self.tools.execute("search_site", '{"query": "screen reader"}')
        self.assertEqual(output["results"][0]["title"], "Screen Readers")
        self.assertEqual(output["results"][0]["section"], "Vision")

    def test_get_page_returns_text_and_cuts_long_pages(self):
        output = self.tools.execute("get_page", {"path": "vision/screen-readers/"})
        self.assertEqual(output["url"], f"{SITE}/docs/vision/screen-readers/")
        self.assertIn("[Page cut here", output["text"])

    def test_bad_calls_return_errors_instead_of_raising(self):
        self.assertIn("error", self.tools.execute("delete_site", "{}"))
        self.assertIn("error", self.tools.execute("search_site", "{not json"))
        self.assertIn("error", self.tools.execute("search_site", '{"query": ""}'))
        self.assertIn("error", self.tools.execute("search_site", "[1, 2]"))
        self.assertIn("error", self.tools.execute("get_page", '{"path": "missing/page/"}'))


class AgentTests(unittest.TestCase):
    def make_agent(self, client, **options):
        return Agent(client, Tools(make_index()), "SYSTEM", **options)

    def test_answers_directly_when_model_calls_no_tool(self):
        result = self.make_agent(FakeClient(text("Hello."))).run("Hi")
        self.assertEqual((result.answer, result.steps, result.tool_calls), ("Hello.", 1, []))

    def test_runs_tools_and_feeds_results_back(self):
        client = FakeClient(
            tool_call("search_site", {"query": "screen reader"}, "call_a"),
            tool_call("get_page", {"path": "vision/screen-readers/"}, "call_b"),
            text("See Screen Readers."),
        )
        events = []
        result = self.make_agent(client, on_event=events.append).run("What is a screen reader?")

        self.assertEqual(result.answer, "See Screen Readers.")
        self.assertEqual([c["name"] for c in result.tool_calls], ["search_site", "get_page"])
        self.assertEqual(result.tool_calls[1]["url"], f"{SITE}/docs/vision/screen-readers/")
        self.assertEqual(len(events), 2)
        self.assertEqual(result.usage, {"prompt_tokens": 30, "completion_tokens": 15})

        # The third request must carry the full exchange so far, in order.
        roles = [m["role"] for m in client.requests[2]["messages"]]
        self.assertEqual(roles, ["system", "user", "assistant", "tool", "assistant", "tool"])
        tool_message = client.requests[2]["messages"][3]
        self.assertEqual(tool_message["tool_call_id"], "call_a")
        self.assertIn("Screen Readers", tool_message["content"])

    def test_tool_error_goes_back_to_the_model(self):
        client = FakeClient(tool_call("get_page", "{broken"), text("Sorry."))
        result = self.make_agent(client).run("x")
        self.assertFalse(result.tool_calls[0]["ok"])
        self.assertIn("not valid JSON", client.requests[1]["messages"][-1]["content"])

    def test_last_turn_gets_no_tools_and_must_answer(self):
        client = FakeClient(
            tool_call("search_site", {"query": "a"}),
            tool_call("search_site", {"query": "b"}),
            text("Best answer I have."),
        )
        result = self.make_agent(client, max_steps=3).run("x")
        self.assertEqual(result.answer, "Best answer I have.")
        self.assertIsNotNone(client.requests[1]["tools"])
        self.assertIsNone(client.requests[2]["tools"])

    def test_history_carries_into_the_next_question(self):
        client = FakeClient(text("First."), text("Second."))
        agent = self.make_agent(client)
        first = agent.run("One")
        agent.run("Two", first.history)
        contents = [m["content"] for m in client.requests[1]["messages"]]
        self.assertEqual(contents, ["SYSTEM", "One", "First.", "Two"])


class GroundingTests(unittest.TestCase):
    def test_sorts_links(self):
        answer = (f"Read [Screen Readers]({SITE}/docs/vision/screen-readers/). "
                  f"Also {SITE}/docs/vision/braille/ and {SITE}/hot-topics/ and https://www.w3.org/WAI/.")
        links = check_links(answer, make_index(), CONFIG)
        self.assertEqual(links["site_links"], [f"{SITE}/docs/vision/screen-readers/", f"{SITE}/hot-topics/"])
        self.assertEqual(links["unknown_links"], [f"{SITE}/docs/vision/braille/"])
        self.assertEqual(links["external_links"], ["https://www.w3.org/WAI/"])

    def test_extra_prefixes_cover_site_areas_left_out_of_the_index(self):
        config = {**CONFIG, "extraPrefixes": ["docs/contribute"]}
        answer = f"See {SITE}/docs/contribute and {SITE}/docs/contribute/page-a/ but not {SITE}/docs/contributeX/."
        links = check_links(answer, make_index(), config)
        self.assertEqual(links["site_links"], [f"{SITE}/docs/contribute", f"{SITE}/docs/contribute/page-a/"])
        self.assertEqual(links["unknown_links"], [f"{SITE}/docs/contributeX/"])


class PromptTests(unittest.TestCase):
    def test_prompt_uses_config_and_lists_top_level_pages(self):
        prompt = build_system_prompt(CONFIG, make_index())
        self.assertIn("Example Hub", prompt)
        self.assertIn(f"- Vision: {SITE}/docs/vision/", prompt)
        self.assertNotIn("Screen Readers", prompt)


class ChatClientTests(unittest.TestCase):
    def make_client(self, responses, **options):
        self.sent, self.slept = [], []
        queue = list(responses)

        def transport(url, headers, body, timeout):
            self.sent.append({"url": url, "headers": headers, "body": json.loads(body)})
            return queue.pop(0)

        return ChatClient("test-key", "some/model", transport=transport, sleep=self.slept.append, **options)

    @staticmethod
    def ok(content="Hi"):
        return 200, {}, json.dumps({"choices": [{"message": {"role": "assistant", "content": content}}],
                                    "usage": {"prompt_tokens": 3, "completion_tokens": 1}})

    def test_sends_openai_shaped_request(self):
        client = self.make_client([self.ok()])
        result = client.complete([{"role": "user", "content": "x"}], tools=[{"type": "function"}])
        sent = self.sent[0]
        self.assertEqual(sent["url"], "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(sent["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(sent["body"]["tool_choice"], "auto")
        self.assertEqual(result["message"]["content"], "Hi")

    def test_omits_tools_when_none_given(self):
        self.make_client([self.ok()]).complete([{"role": "user", "content": "x"}])
        self.assertNotIn("tools", self.sent[0]["body"])

    def test_retries_rate_limit_then_succeeds(self):
        limited = 429, {"Retry-After": "7"}, json.dumps({"error": {"message": "slow down", "code": 429}})
        result = self.make_client([limited, self.ok("Done")]).complete([])
        self.assertEqual(result["message"]["content"], "Done")
        self.assertEqual(self.slept, [7.0])

    def test_does_not_retry_bad_request(self):
        bad = 400, {}, json.dumps({"error": {"message": "bad model", "code": 400}})
        with self.assertRaises(ModelError) as caught:
            self.make_client([bad]).complete([])
        self.assertEqual(caught.exception.status, 400)
        self.assertEqual(len(self.sent), 1)

    def test_error_inside_200_response_is_raised(self):
        wrapped = 200, {}, json.dumps({"error": {"message": "provider down", "code": 503}})
        with self.assertRaises(ModelError) as caught:
            self.make_client([wrapped], max_retries=0).complete([])
        self.assertEqual(caught.exception.status, 503)

    def test_missing_key_is_reported(self):
        with self.assertRaises(ModelError):
            ChatClient("", "some/model")


if __name__ == "__main__":
    unittest.main()
