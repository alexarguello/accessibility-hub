---
title: "AI Agents Read Your Accessibility Tree, Not Your HTML"
sidebar_label: "AI agents and the a11y tree"
sidebar_position: 6
image: /img/ai-agents-a11y-tree-card.png
description: "Results from a Spring Boot app served in two variants with identical backend and CSS but different markup, and what that one difference did to a screen reader and two AI agents."
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

**The data:** [results dashboard](https://alexarguello.github.io/accessibility-hub/ai-readiness/) ·
[source repository](https://github.com/alexarguello/a11y-ai-readiness) ·
[raw run data](https://github.com/alexarguello/a11y-ai-readiness/tree/main/results) ·
[NVDA run sheet and transcripts](https://github.com/alexarguello/a11y-ai-readiness/blob/main/docs/nvda-run-sheet.md)

**Came here from the talk?** [What to do next](./what-to-do-next.md) has six steps you can start with tomorrow.

This page is the results record for the experiment. A Spring Boot app serves one flow — *register
for a workshop* — from two sets of templates, with the same controller, validation, stylesheet and
data. Only the markup differs, and the session list is asserted pixel-identical by a test.

Both assistive technology and software acting on a user's behalf read the
[accessibility tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree) the
browser builds from your markup — roles, names and states — rather than your HTML or CSS. So
the same markup difference decides whether either one can finish the task.

## Who tried it

Three independent consumers, same task, both variants. Runs made **20 September 2026**.

| Who tried it | `/accessible` | `/inaccessible` |
|---|---|---|
| NVDA (screen reader, keyboard only) | Completed | **Failed** |
| AI agent — Grok (`grok-4.6`) | Completed | **Failed** |
| AI agent — Claude (`claude-sonnet-5`) | Completed | **Failed** |

Two unrelated vendors' models, tested separately, so this isn't one model's quirk.

## Agent runs

Five runs per variant per provider. Medians, with the full range across the five runs.

| Provider | Variant | Success | Tool calls | Tokens | Cost/run |
|---|---|---|---|---|---|
| Grok `grok-4.6` | `/accessible` | 5/5 | 11 (11–12) | 36.2k (33.2–45.0k) | $0.071 |
| Grok `grok-4.6` | `/inaccessible` | **0/5** | 33 (23–34) | 127.3k (108.4–210.3k) | $0.247 |
| Claude `claude-sonnet-5` | `/accessible` | 5/5 | 11 (11–11) | 46.6k (46.5–47.6k) | $0.104 |
| Claude `claude-sonnet-5` | `/inaccessible` | **0/5** | 3 (3–6) | 10.6k (10.4–24.2k) | $0.027 |

The two failures have different shapes: Grok kept retrying and Claude stopped early. Neither
obtained a confirmation code on any run.

## Screen reader runs

NVDA on Firefox, captured with the Speech Viewer. Verbatim transcripts and the counts derived from
them are in the
[run sheet](https://github.com/alexarguello/a11y-ai-readiness/blob/main/docs/nvda-run-sheet.md).

| | `/accessible` | `/inaccessible`, keyboard | `/inaccessible`, mouse + NVDA |
|---|---|---|---|
| Task completed | Yes — code `JCON-C7ED97` | **No** | **No**, even with a mouse |
| Where it stopped | — | After the filter field; Tab leaves the page | Silent resubmission loop on meal preference |
| Validation error announced | Yes — `role="alert"`, immediately | Never reached the form | **No** |
| Characters typed | 40 | 6 | 54 |
| `alert` announcements | 2 | 0 | **0** |

One precision worth keeping: on `/inaccessible` the *email* error **was** announced, because the
browser's native `type="email"` validity leaks through. The *meal preference* failure, the one that
blocked the task, was announced never.

## Scanner results

axe-core, run against both pages of both variants in the test suite:

| Page | Violations | Rules |
|---|---|---|
| `/accessible` sessions & register | 0 | — |
| `/inaccessible` sessions | 4 (9 nodes) | `image-alt`, `landmark-one-main`, `page-has-heading-one`, `region` |
| `/inaccessible` register | 4 (9 nodes) | `label`, `landmark-one-main`, `page-has-heading-one`, `region` |

Audited as a Lighthouse accessibility run in Edge DevTools, the broken register form scores
**91/100**.

None of those findings names the fake dropdown, the role-less Register control or the colour-only
error — the three defects that stopped every consumer. For which kind of test does catch which
defect, see [Test What Scanners Miss](./test-what-scanners-miss.md).

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

## How it was measured

- **Variants.** One flow, two template sets, same controller, validation, stylesheet and data.
  `VisualParityTest` asserts the session list is pixel-identical. The register form shares the same
  stylesheet and is not separately screenshot-tested.
- **What the agent can see.** Accessibility-tree primitives only — Playwright's `ariaSnapshot()` to
  look, role and name lookups to act. Nothing in its toolset reads raw HTML, the DOM or CSS, and it
  cannot take a screenshot. This isolates the tree as the channel under test.
- **Run order.** Five runs per variant per provider, alternating A-B-B-A so neither variant benefits
  from going first or last.
- **Tool-call cap.** 40. The highest run in this data used 34, so no published run was cut off.
- **Excluded data.** An earlier pass capped tool calls at 15. All five of Grok's `/inaccessible`
  runs hit that cap, which makes their counts the cap rather than a measurement, so they are
  excluded as spoiled and kept in `results/` flagged `budgetExhausted` rather than deleted. Raising
  the cap to 40 gave the broken variant more room, not less.
- **Costs** are computed, not observed on an invoice, from the rates each vendor published as of
  **20 September 2026**, the day of the runs: $2.00 per million input tokens and $6.00 output for
  `grok-4.6`, $2.00 input and $10.00 output for `claude-sonnet-5`. They also depend on how long a
  model keeps trying before giving up. Treat them as an order of magnitude at that date.
- **Provenance.** Every figure on this page is derived from committed artefacts by a script: the
  screen-reader counts from the transcripts, the agent figures from one JSON file per run.

To run it yourself, or to regenerate the dashboard, see the
[repository README](https://github.com/alexarguello/a11y-ai-readiness#readme). It needs JDK 25 and
nothing else; the agent runs on your own API key.

## What other people measured

This experiment tests one small application, so it can show that the problem is real but not how
common it is. Published research has measured related questions at larger scale — including a study
in which one off-screen `<span>` took agent click-through on a visually identical advert from 0 of
10 tries to 9 or 10 of 10 across three models. Those papers, what each one found, and where they
disagree are summarised on the
[results dashboard](https://alexarguello.github.io/accessibility-hub/ai-readiness/).

## What to do next

You don't need a big project to start. [What to Do Next](./what-to-do-next.md) walks you through
six short steps on one flow of your own app: look at the accessibility tree, use only the keyboard,
listen with a screen reader, find controls by role in your tests, keep a scanner in CI, and learn
the WCAG rules behind each fix.

To see which kind of test catches which defect, read
[Test What Scanners Miss](./test-what-scanners-miss.md).

## Further reading

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — filter by the success criteria above
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — before you build a custom widget, check whether a native element already does it
- [NVDA](https://www.nvaccess.org/download/) — free; thirty minutes with it teaches more than any checklist
- [Playwright role-based locators](https://playwright.dev/java/docs/locators) · [Testing Library `ByRole`](https://testing-library.com/docs/queries/byrole/) — the same tree, used as test infrastructure
- [axe-core](https://github.com/dequelabs/axe-core) — put it in CI, and remember what it cannot see

*From the talk “Why AI Agents Struggle With Your Java Web App”, JCON at IBM TechXchange,
October 2026 by Alexandra Arguello Saenz*
