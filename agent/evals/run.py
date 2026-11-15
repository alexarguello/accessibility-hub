"""Run the test questions.

  python -m evals.run --search        search only, no model and no key needed
  python -m evals.run                 full agent run (needs OPENROUTER_API_KEY)

  python -m evals.run --pending       only the questions that have no result yet
  python -m evals.run --summary       latest result per question across all runs; no model needed

Options for the full run:
  --only en-05,es-01    run only these ids
  --lang es             run only one language
  --limit 5             stop after this many questions
  --model <id>          override the model
  --delay 4             seconds to wait between questions (free models are rate limited)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from site_agent.config import build_agent, load_config, load_site_index
from site_agent.grounding import check_links
from site_agent.model_client import ModelError

EVALS_DIR = Path(__file__).resolve().parent


def load_questions(site_index) -> list[dict]:
    questions = json.loads((EVALS_DIR / "questions.json").read_text(encoding="utf-8"))["questions"]
    for question in questions:
        urls = []
        for path in question.get("expect", []):
            page = site_index.find_page(path)
            if page is None:
                raise SystemExit(f"{question['id']}: expected page not in the index: {path}")
            urls.append(page["url"])
        question["expect_urls"] = urls
    return questions


def latest_results() -> dict[str, dict]:
    """Latest finished result per question id, across every saved run. Errors do not count."""
    latest: dict[str, dict] = {}
    for path in sorted((EVALS_DIR / "results").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data.get("records", []):
            if record.get("verdict") in ("PASS", "FAIL", "REVIEW"):
                latest[record["id"]] = {**record, "model": data.get("model", ""), "run": path.name}
    return latest


def print_summary(questions: list[dict]) -> int:
    latest = latest_results()
    counts: dict[str, int] = {}
    for question in questions:
        record = latest.get(question["id"])
        verdict = record["verdict"] if record else "PENDING"
        counts[verdict] = counts.get(verdict, 0) + 1
        model = f"  [{record['model']}]" if record else ""
        print(f"{verdict:<8}{question['id']:<12}{question['question'][:70]}{model}")
    summary = ", ".join(f"{count} {verdict}" for verdict, count in sorted(counts.items()))
    print(f"\n{len(questions)} questions: {summary}.")
    return 0


def run_search_eval(site_index, questions: list[dict]) -> int:
    """Does search alone put an expected page in the top results for the raw question?"""
    scored = [q for q in questions if q.get("expect_urls") and q["lang"] == "en"]
    hits = {1: 0, 3: 0, 5: 0}
    misses = []
    for question in scored:
        ranked = [r["url"] for r in site_index.search(question["question"], limit=5)]
        rank = next((i + 1 for i, url in enumerate(ranked) if url in question["expect_urls"]), None)
        for cutoff in hits:
            if rank and rank <= cutoff:
                hits[cutoff] += 1
        if rank is None:
            misses.append((question, ranked))

    total = len(scored)
    print(f"Search eval: {total} English questions with an expected page")
    for cutoff, count in hits.items():
        print(f"  expected page in top {cutoff}: {count}/{total}")
    for question, ranked in misses:
        print(f"\n  MISS {question['id']}: {question['question']}")
        for url in ranked[:3]:
            print(f"       got {url}")
    return 0


def judge(question: dict, result, links: dict) -> dict:
    fetched = {call["url"] for call in result.tool_calls if call["name"] == "get_page" and call["ok"]}
    cited = any(url in result.answer for url in question["expect_urls"])
    retrieved = any(url in fetched for url in question["expect_urls"])
    grounded = not links["unknown_links"]
    if question.get("decline"):
        verdict = "REVIEW" if grounded else "FAIL"
    else:
        verdict = "PASS" if cited and grounded else "FAIL"
    return {"verdict": verdict, "cited": cited, "retrieved": retrieved, "grounded": grounded}


def run_agent_eval(config: dict, site_index, questions: list[dict], args) -> int:
    try:
        agent = build_agent(config, site_index, model=args.model)
    except ModelError as error:
        print(f"Cannot start: {error}", file=sys.stderr)
        return 1

    records = []
    for number, question in enumerate(questions):
        if number:
            time.sleep(args.delay)
        try:
            result = agent.run(question["question"])
        except ModelError as error:
            if "per-day" in str(error):
                # The daily allowance is used up; every further question would fail the same way.
                left = len(questions) - number
                print(f"\nStopped: daily free-model limit reached. {left} questions not run.")
                print("Run again with --pending after the limit resets (00:00 UTC).")
                break
            print(f"ERROR  {question['id']}: {error}")
            records.append({"id": question["id"], "verdict": "ERROR", "error": str(error)})
            continue
        links = check_links(result.answer, site_index, config)
        outcome = judge(question, result, links)
        print(f"{outcome['verdict']:<6} {question['id']}: {question['question']}")
        if outcome["verdict"] == "FAIL":
            reason = "made-up link" if not outcome["grounded"] else (
                "read the page but did not link it" if outcome["retrieved"] else "expected page not used")
            print(f"       {reason}")
        if outcome["verdict"] == "REVIEW":
            print(f"       {result.answer[:300]!r}")
        records.append({
            "id": question["id"], "question": question["question"], **outcome,
            "answer": result.answer, "tool_calls": result.tool_calls, "links": links,
            "steps": result.steps, "usage": result.usage,
        })

    counts = {}
    for record in records:
        counts[record["verdict"]] = counts.get(record["verdict"], 0) + 1
    summary = ", ".join(f"{count} {verdict}" for verdict, count in sorted(counts.items()))
    if not records:
        return 1
    print(f"\n{len(records)} questions: {summary}. REVIEW answers need a person to read them.")

    results_dir = EVALS_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    out = results_dir / f"{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps({"model": agent._client.model, "counts": counts, "records": records},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Full answers saved to {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the site agent test questions.")
    parser.add_argument("--search", action="store_true", help="Search-only eval; no model needed.")
    parser.add_argument("--pending", action="store_true", help="Only questions with no result yet.")
    parser.add_argument("--summary", action="store_true", help="Show the latest result per question.")
    parser.add_argument("--only", help="Comma-separated question ids, for example en-09,en-10.")
    parser.add_argument("--lang", help="Only questions in this language (en or es).")
    parser.add_argument("--limit", type=int, help="Run at most this many questions.")
    parser.add_argument("--model", help="Model id to use.")
    parser.add_argument("--delay", type=float, default=4, help="Seconds between questions.")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")

    config = load_config()
    site_index = load_site_index(config)
    questions = load_questions(site_index)
    if args.search:
        return run_search_eval(site_index, questions)
    if args.summary:
        return print_summary(questions)

    if args.pending:
        done = latest_results()
        questions = [q for q in questions if q["id"] not in done]
        if not questions:
            print("Every question has a result. Use --summary to see them.")
            return 0
        print(f"{len(questions)} questions pending: {', '.join(q['id'] for q in questions)}\n")
    if args.only:
        wanted = set(args.only.split(","))
        questions = [q for q in questions if q["id"] in wanted]
    if args.lang:
        questions = [q for q in questions if q["lang"] == args.lang]
    if args.limit:
        questions = questions[: args.limit]
    return run_agent_eval(config, site_index, questions, args)


if __name__ == "__main__":
    sys.exit(main())
