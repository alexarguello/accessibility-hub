---
title: "What to Do Next: Six Steps for Your Own App"
sidebar_label: "What to do next"
sidebar_position: 7
description: "Six short steps to check your own app the way screen readers and AI agents see it — the accessibility tree, the keyboard, a screen reader, role-based tests, a scanner, and the WCAG rules behind the fixes."
level: beginner
type: guide
status: published
content_status: current
audience:
  - developer
disability_type:
  - general
tags:
  - accessibility-testing
  - screen-readers
  - keyboard-accessibility
  - wcag
topics:
  - accessibility-testing
  - wcag
  - tool:NVDA
  - tool:axe
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# What to Do Next: Six Steps for Your Own App

This page follows [AI Agents Read Your Accessibility Tree, Not Your HTML](./ai-agents-read-your-accessibility-tree.md).
That page showed one flow that worked for nobody but a sighted mouse user. This page shows how
to find the same problems in your own app.

You don't need a big project to start. Pick **one key flow**, such as login, checkout or a
sign-up form, and do these six steps on it. Steps 1 to 3 take about 20 minutes and need no setup.

## 1. Look at your own accessibility tree (5 minutes)

Open the flow in your browser and inspect it the way an agent or a screen reader does.

- **Chrome or Edge:** DevTools → Elements → **Accessibility** pane. Turn on
  *Enable full-page accessibility tree* to see the whole page as a tree.
- **Firefox:** DevTools → **Accessibility** tab.
- **Safari:** Web Inspector → Elements → Node sidebar → **Accessibility**.

For every button, link and field, check three things:

| Property | What it is | Example |
|---|---|---|
| **Role** | What kind of control it is | `button`, `link`, `textbox`, `combobox` |
| **Name** | The text a screen reader reads out, and the text an agent searches for | "Register", "Email address" |
| **State** | The current condition, if it has one | checked, expanded, disabled, invalid |

A control shown as `generic`, or with an empty name, is a control that people and agents
can't use. If something looks like a button on screen but isn't a `button` in the tree, it is
not a button.

## 2. Put the mouse away (5 minutes)

Do the same flow with the keyboard only:

| Key | What it should do |
|---|---|
| **Tab** / **Shift+Tab** | Move to the next / previous control |
| **Enter** | Follow a link, press a button, submit a form |
| **Space** | Press a button, tick a checkbox |
| **Arrow keys** | Move inside dropdowns, radio groups, tabs and menus |
| **Esc** | Close a dialog or a menu |

Check four things:

- You can reach every control.
- You can always see where the focus is.
- The focus moves in a sensible order.
- You never get stuck inside a component.

If you can't finish the task, neither can a keyboard user, and neither can many agents.

## 3. Listen to it with a screen reader (10 minutes)

- **Windows:** [NVDA](https://www.nvaccess.org/download/) (free), with Firefox.
- **Mac:** VoiceOver (Cmd+F5), with Safari.

Turn off the screen or close your eyes, and try the flow again. Listen for:

- controls with no name, or a name like "button" or "clickable"
- form fields read without their label
- errors that appear on screen but are never read out
- content read in a confusing order

The [testing guide](./test-what-scanners-miss.md#a-10-minute-screen-reader-check) has a
step-by-step NVDA script.

## 4. Find one control by role in your tests

Take one end-to-end test and replace a CSS selector with a role-based locator:

```java
// Before: breaks when the markup changes, and proves nothing about accessibility
page.locator("div.actions > span:nth-child(2)").click();

// After: fails if the control has no link role or no "Register" name
page.getByRole(AriaRole.LINK, new Page.GetByRoleOptions().setName("Register")).click();
```

If your test can't find the control by role and name, an agent can't either. This one change
makes your normal tests check the accessibility tree too. It also makes them less brittle,
because they no longer depend on the page layout.

The same idea works in JavaScript tests with Playwright's `page.getByRole()` and
[Testing Library](https://testing-library.com/docs/queries/byrole/)'s `getByRole`.

## 5. Keep a scanner in CI, as a minimum

Add [axe-core](https://github.com/dequelabs/axe-core) to your test suite. On every build it
catches missing labels, missing `alt` text, low contrast and missing landmarks.

Remember what the experiment showed: the broken form still scored **91/100** in Lighthouse.
A scanner can only judge code that tries to be a control. A `<div>` that pretends to be a
dropdown is invisible to it. A passing scan is a minimum, not a result.

[Test What Scanners Miss](./test-what-scanners-miss.md) explains what each kind of test catches,
with copy-paste Java recipes.

## 6. Learn the rules behind the fixes

- Use the [Accessible Web Development Checklist](./accessible-web-dev-checklist.md). Each item
  links to its WCAG rule and says how to check it.
- Look up any rule in the [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/).
  You can filter it by level (A, AA) and by technology.
- Before you build a custom widget, read [ARIA Roles](../hot-topics/aria-roles.md) and check the
  [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/). Most of the time a native
  HTML element already does the job, with keyboard support included.

## Keep going

- Share what you find, or suggest a page: see [How to Contribute](./how-to-contribute.md).
- Explore the rest of the [For Developers](./index.md) section.
