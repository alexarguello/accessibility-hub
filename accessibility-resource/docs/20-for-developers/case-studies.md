---
title: Developer Case Studies
sidebar_position: 3
hide_title: true
description: "Real accessibility experiments and fixes from developers: what was built, how it was tested, what broke, and what fixed it."
level: intermediate
type: reference
status: published
content_status: current
audience:
  - developer
disability_type:
  - general

tags:
  - inclusive-design
  - accessibility
  - accessibility-testing
  - ai-accessibility
topics:
  - case-studies
  - accessibility
  - accessibility-testing
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# Developer Case Studies

Short, honest write-ups of accessibility work: what was built, how it was tested, what broke, and
what fixed it. Each one should be useful to a developer facing the same problem tomorrow.

---

## Case study 1: Same app, two markups — screen readers and AI agents

**Author:** Alexandra Arguello Saenz · **Stack:** Java 25, Spring Boot, Thymeleaf, Spring AI, Playwright, axe-core ·
**Full write-up:** [AI Agents Read Your Accessibility Tree, Not Your HTML](./ai-agents-read-your-accessibility-tree.md)

### The question

Does inaccessible markup only hurt screen reader users, or does it also block AI agents that act for
users in a browser?

### What was built

One "register for a workshop" flow served from two sets of templates. Same controller, validation,
CSS and data. Only the markup differs. To a sighted mouse user, the two versions look and work the
same.

### How it was tested

- A screen reader user (NVDA, keyboard only) tried to register on both versions.
- Two AI agents from different vendors tried the same task, 5 runs per version each. The agents
  could only see the page through accessibility tree tools: Playwright's `ariaSnapshot()` to look,
  and role and name lookups to act.
- axe-core ran on both versions in the test suite, and Lighthouse ran in the browser.

### What happened

| | Accessible version | Inaccessible version |
|---|---|---|
| Screen reader (NVDA) | Completed | **Failed.** The task couldn't even start. |
| AI agent 1 | Completed in all runs | **Failed in all runs.** It used about 3× the tool calls and cost. |
| AI agent 2 | Completed in all runs | **Failed in all runs.** It gave up after 3 calls. |
| Lighthouse score | — | **91/100** |

### What broke it

Four markup defects: a `<span onclick>` instead of a link, placeholders instead of labels, a `<div>`
pretending to be a dropdown, and an error shown only by color. The scanners flagged mostly other
issues. The fake dropdown, the worst defect, was invisible to them.

### What fixed it

Native HTML: `<a href>`, `<label for>`, `<select>`, and a `role="alert"` error message. Each fix
maps to a WCAG rule, and each one unblocked the screen reader and the agents at the same time.

### Lessons for developers

1. AI agents and screen readers read the same thing: the accessibility tree. One fix helps both.
2. A high scanner score is not a tested page. See [Test What Scanners Miss](./test-what-scanners-miss.md).
3. A thin accessibility tree is also why end-to-end tests need brittle CSS selectors. Role-based
   locators fix both problems.
4. A failing agent doesn't always cost more. One agent spent 3× more and failed; the other gave up
   cheaply and failed. Either way, the transaction was lost.

---

## Add your case study

Have you fixed an accessibility problem, run an experiment, or tested a product with real users?
Your story helps the next developer. Small fixes are welcome; they don't need to be big projects.

Use this outline (about 300–800 words):

```markdown
## Case study: <short title>

**Author:** <name> · **Stack:** <languages, frameworks, tools> · **Link:** <repo or article, optional>

### The problem
What was wrong, and who it affected. Which users or assistive technologies?

### How you found it
User report, audit, scanner, manual test, screen reader test, usability session?

### What you changed
Before and after code, if you can share it. Which WCAG rule does it relate to?

### How you checked the fix
Which tests or users confirmed it works?

### Lessons for other developers
Two to four points someone could apply tomorrow.
```

Then [open a pull request](https://github.com/alexarguello/accessibility-hub/pulls) adding it to this
page, or [open an issue](https://github.com/alexarguello/accessibility-hub/issues) with your draft and
we'll help publish it. See [How to Contribute](./how-to-contribute.md) for details.

**Please don't include** personal details about users, or anything your employer hasn't cleared
for sharing.

## More case studies elsewhere

- [W3C WAI: The Business Case for Digital Accessibility](https://www.w3.org/WAI/business-case/) — examples from organizations, with sources
- [W3C WAI: Stories of Web Users](https://www.w3.org/WAI/people-use-web/user-stories/) — how people with different disabilities use the web
