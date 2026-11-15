# Site agent

A text-first agent that answers questions from a site's own content. It finds pages with a search tool, reads them, and answers with links to what it read. It is built for A11YHub but the code in `site_agent/` does not know which site it serves.

Python 3.10 or later. No packages to install: it uses the standard library only.

## How it works

1. The site publishes a content index: `site-index.json` plus one text file per page. For A11YHub, `accessibility-resource/flatmap-tools/generate_site_index.py` builds it.
2. The agent sends the question to a language model along with two tools it may call: `search_site` and `get_page`.
3. The model asks for a tool, the agent runs it and sends the result back, and this repeats until the model answers in text.

| File | What it does |
|---|---|
| `site_agent/site_index.py` | Loads the index and ranks pages for a query |
| `site_agent/tools.py` | The two tools and their descriptions |
| `site_agent/model_client.py` | The HTTP call to the model, with retry on rate limits |
| `site_agent/agent.py` | The loop |
| `site_agent/prompt.py` | Builds the system prompt from the config |
| `site_agent/grounding.py` | Checks that links in an answer are real pages |
| `site.config.json` | Everything specific to the site |

## Set up

Build the index (from `accessibility-resource/`):

```
python flatmap-tools/generate_mermaids.py
python flatmap-tools/generate_site_index.py
```

Then, in this folder, copy `.env.example` to `.env.local` and add an OpenRouter key. `.env.local` is never committed.

## Use

Run these from this folder.

| Command | What it does |
|---|---|
| `python -m site_agent.cli` | Chat in the terminal |
| `python -m site_agent.cli "question" --verbose` | One question, showing each tool call |
| `python -m site_agent.list_models` | List free models that support tool calling |
| `python -m unittest` | Unit tests (no key needed) |
| `python -m evals.run --search` | Search-only eval (no key needed) |
| `python -m evals.run` | Full eval against the model |
| `python -m evals.run --pending` | Only the questions that have no result yet |
| `python -m evals.run --summary` | Latest result per question across all runs (no key needed) |

The full eval also accepts `--only en-05,es-01`, `--lang es`, `--limit 5`, `--model <id>` and `--delay <seconds>`. Answers are saved under `evals/results/`. A run stops by itself when the provider's daily free limit is reached; continue later with `--pending`.

## Reading eval results

- **PASS**: the answer links a page listed in `expect` and contains no made-up site link.
- **FAIL**: the expected page was not linked, or the answer contains a site link that does not exist.
- **REVIEW**: a question the agent should decline (medical, legal, off topic). A person has to read the answer.

The checks are deliberately simple. They show whether the agent found and cited the right page, not whether the wording is good.

## Using it for another site

Produce the same index format for that site and point `site.config.json` at it. Nothing in `site_agent/` needs to change.
