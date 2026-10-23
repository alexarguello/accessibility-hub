---
title: "AI Agents Read Your Accessibility Tree, Not Your HTML"
sidebar_label: "AI agents and the a11y tree"
sidebar_position: 6
description: "A Spring Boot app served in two variants with identical backend and CSS but different markup, and what that one difference does to screen readers and AI agents."
level: intermediate
type: reference
status: published
content_status: current
audience:
  - developer
disability_type:
  - general
tags:
  - ai-accessibility
  - screen-readers
  - accessibility-testing
  - wcag
topics:
  - ai
  - accessibility-testing
  - tool:NVDA
  - wcag
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# AI Agents Read Your Accessibility Tree, Not Your HTML

**Repo:** [a11y-ai-readiness](https://github.com/alexarguello/a11y-ai-readiness) ·
**Live results dashboard:** [view the live results](https://alexarguello.github.io/accessibility-hub/ai-readiness/)

**Came here from the talk?** [What to do next](./what-to-do-next.md) has six steps you can start with tomorrow.

A Spring Boot web app that serves one flow — *register for a workshop* — from two sets of
templates. Same controller, same validation, same stylesheet, same data. Only the markup
differs. The session list is asserted pixel-identical by a test; the registration form, where
the testing happened, looks and behaves the same to a sighted mouse user.

That one difference decides whether a screen reader user or an AI agent can complete the task
at all.

## Why a developer should care

Your UI has two consumers you probably don't test: assistive technology, and software acting on
a user's behalf. Neither reads your HTML or your CSS. Both read the
[accessibility tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree) the
browser builds from your markup — roles, names, states.

An agent driving a browser asks that tree "what's on this page, and what can I do to it?" A
screen reader asks the identical question. So a `<div onclick>` that looks like a button isn't a
styling choice — it's a control that neither one can find.

There is no separate "make it AI-ready" project. It's the same work, and it's already in your
backlog as an accessibility ticket.

## What was measured

Three independent consumers, same task, both variants:

| Who tried it | `/accessible` | `/inaccessible` |
|---|---|---|
| NVDA (screen reader, keyboard only) | Completed | **Failed** |
| AI agent — Grok (`grok-4.6`) | Completed | **Failed** |
| AI agent — Claude (`claude-sonnet-5`) | Completed | **Failed** |

Two unrelated vendors' models, tested separately, so this isn't one model's quirk.

**Agent runs — 5 runs per variant per provider, medians:**

| Provider | Variant | Success | Tool calls | Tokens | Cost/run |
|---|---|---|---|---|---|
| Grok `grok-4.6` | `/accessible` | 100% | 11 | 36k | $0.071 |
| Grok `grok-4.6` | `/inaccessible` | **0%** | 33 | 127k | $0.247 |
| Claude `claude-sonnet-5` | `/accessible` | 100% | 11 | 47k | $0.104 |
| Claude `claude-sonnet-5` | `/inaccessible` | **0%** | 3 | 11k | $0.027 |

Note the two shapes of failure. Grok kept hunting — 3× the calls, 3.5× the tokens, 3.5× the cost,
and still no confirmation code. Claude recognised there was no reachable control and gave up after
three calls. **Cheap is not good news here: the transaction is lost either way.** If that flow were
a checkout, a booking, or a claim submission, an inaccessible UI is one your customer's agent
cannot buy from.

The agent perceives the page *only* through accessibility-tree primitives — Playwright's
`ariaSnapshot()` to look, role/name lookups to act. Nothing in its toolset reads raw HTML or CSS,
which is what makes the comparison meaningful.

**Screen reader (NVDA, keyboard only):** on `/accessible`, 61 keystrokes to a confirmation code,
with the validation error announced immediately. On `/inaccessible` the task couldn't be *started*:
after the filter box, Tab leaves the page entirely — the filter box is the only reachable control.
With a mouse, the meal-preference dropdown still could not be operated, and nothing was ever
announced to explain why submission kept failing.

## Automated scans only catch part of it

axe-core runs against both pages in the test suite:

| Page | Violations | Rules |
|---|---|---|
| `/accessible` sessions & register | 0 | — |
| `/inaccessible` sessions | 4 (9 nodes) | `image-alt`, `landmark-one-main`, `page-has-heading-one`, `region` |
| `/inaccessible` register | 4 (9 nodes) | `label`, `landmark-one-main`, `page-has-heading-one`, `region` |

Run as a Lighthouse audit in Edge DevTools, the broken register form still scores **91/100** for
accessibility. Those four findings are largely *not* the four defects that actually broke every
consumer. A scanner can only flag code that at least tries to be a button, field, or link; code
that never tries — the fake `<div>` dropdown — is invisible to it.

**A high score is not a tested page.** Keep the scanner in CI, but it is a floor, not a verdict.

## The four defects, and the fixes

Each fix is a WCAG requirement, and each one unblocks the screen reader and the agent at the same
time.

| Problem | Before | After | WCAG |
|---|---|---|---|
| "Register" isn't a real link | `<span onclick="…">Register</span>` | `<a href="/register/123">Register</a>` | 2.1.1 Keyboard, 4.1.2 Name, Role, Value |
| Fields have placeholders, not labels | `<input placeholder="Full name">` | `<label for="name">Full name</label><input id="name">` | 3.3.2 Labels or Instructions, 1.3.1 Info and Relationships |
| Fake dropdown | `<div class="dropdown">Meal preference…</div>` | `<select><option>Vegetarian</option></select>` | 4.1.2 Name, Role, Value |
| Error shown by colour alone | `<input class="has-error">` | `<div role="alert">Enter a valid email address.</div>` | 3.3.1 Error Identification, 4.1.3 Status Messages |

Plus two on the session list: an `<img>` with no `alt`, and a page title and main region that are
styled `<div>`s instead of `<h1>` and `<main>` (1.1.1, 1.3.1).

**A side effect worth the ticket on its own:** missing roles and names are exactly what forces
`div:nth-child(4) > span` selectors in your E2E tests instead of
[`getByRole`](https://playwright.dev/java/docs/locators). Brittle Playwright or Testing Library
locators are a symptom of a thin accessibility tree, not bad luck.

## What to do next

You don't need a big project to start. [What to Do Next](./what-to-do-next.md) walks you through
six short steps on one flow of your own app: look at the accessibility tree, use only the keyboard,
listen with a screen reader, find controls by role in your tests, keep a scanner in CI, and learn
the WCAG rules behind each fix.

To see which kind of test catches which defect, read
[Test What Scanners Miss](./test-what-scanners-miss.md).

## Running it yourself

Needs **JDK 25** — nothing else. The Maven wrapper fetches its own Maven, and there is no
Node/npm step.

```bash
./mvnw spring-boot:run
```

Then open [http://localhost:8080/](http://localhost:8080/), which links to both variants. Open DevTools' accessibility
tree on each and compare — that is the whole demo in thirty seconds.

The agent never runs during `spring-boot:run` or `mvn test`. To run it (needs `xai.api.key` /
`XAI_API_KEY` or `anthropic.api.key` / `ANTHROPIC_API_KEY`, see `secrets.properties.example`):

```bash
./mvnw spring-boot:run -Dspring-boot.run.arguments="--agent.run=true --variant=accessible --provider=xai"
```

Add `--runs=5` to run both variants N times each in alternating A-B-B-A order and write a summary
with medians and ranges. Each run writes a `results/*.json` with tool calls, tokens, estimated
cost, and the action log. `DashboardGeneratorTest` regenerates `results/dashboard.html` from
whatever is in `results/` — no server or browser needed to view it.

## Stack

| Piece | Choice |
|---|---|
| Language / JDK | Java 25 |
| Framework | Spring Boot 4.1.1, Spring MVC |
| Templates | Thymeleaf, server-rendered — no frontend build |
| Validation | Jakarta Bean Validation |
| JS | ~30 lines of vanilla JS (live-region errors; the broken variant's mouse-only widgets) |
| AI agent | [Spring AI](https://docs.spring.io/spring-ai/reference/) 2.0.1 — xAI via the OpenAI-compatible client, Anthropic via its own; tools backed by Playwright 1.62 |
| Scanner | [axe-core](https://github.com/dequelabs/axe-core) in the test suite |
| Data | In-memory repository, no database |

## Further reading

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — filter by the success criteria above
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — before you build a custom widget, check whether a native element already does it
- [NVDA](https://www.nvaccess.org/download/) — free; thirty minutes with it teaches more than any checklist
- [Playwright role-based locators](https://playwright.dev/java/docs/locators) · [Testing Library `ByRole`](https://testing-library.com/docs/queries/byrole/) — the same tree, used as test infrastructure
- [axe-core](https://github.com/dequelabs/axe-core) — put it in CI, and remember what it cannot see

*From the talk “Why AI Agents Struggle With Your Java Web App”, JCON at IBM TechXchange,
October 2026 by Alexandra Arguello Saenz*
