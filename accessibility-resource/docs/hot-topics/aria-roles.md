---
title: ARIA Roles
sidebar_position: 1
hide_title: true
description: "What ARIA roles do in the accessibility tree, why native HTML comes first, which roles you actually need, and the most common ARIA mistakes."
level: beginner
type: reference
status: published
content_status: current
audience:
  - developer
disability_type:
  - general

tags:
  - aria
  - wcag
  - semantic-html
topics:
  - aria
  - wcag
  - semantic-html
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# ARIA Roles

**ARIA** (Accessible Rich Internet Applications) is a set of HTML attributes that change what the
browser puts in the **accessibility tree**. Screen readers, voice control software and AI agents
read that tree to understand the page. They don't read your CSS.

A **role** tells them what an element is: a button, a tab, a dialog, an alert. Together with a
**name** ("Save") and a **state** (pressed, expanded, checked), it's all they know about a control.
See [AI Agents Read Your Accessibility Tree](../20-for-developers/ai-agents-read-your-accessibility-tree.md)
for what happens when these are missing.

## The first rule: use native HTML

The [first rule of ARIA](https://www.w3.org/TR/using-aria/#rule1) is: if a native HTML element
already does what you need, use it instead of adding a role.

```html
<!-- Native: role, name, focus, Enter and Space all work, with zero JavaScript -->
<button type="button">Save</button>

<!-- ARIA: you now have to add all of that yourself -->
<div role="button" tabindex="0" onclick="save()" onkeydown="handleKeys(event)">Save</div>
```

**ARIA changes what the element is called, not what it does.** `role="button"` makes a screen
reader say "button". It does not make the element focusable, and it does not make Enter or Space
work. Every behavior the native element gives you, you have to write and test yourself.

That's why [WebAIM's yearly scan of the top million home pages](https://webaim.org/projects/million/)
keeps finding that pages using ARIA have *more* detected errors on average, not fewer. Use less of
it, but use it correctly.

## Roles you get for free

These native elements already have the right role in the accessibility tree:

| You write | Role in the tree | Free behavior |
|---|---|---|
| `<button>` | `button` | Focus, Enter, Space |
| `<a href="...">` | `link` | Focus, Enter, listed in "Links" by screen readers |
| `<input type="text">` | `textbox` | Focus, typing, label connection |
| `<input type="checkbox">` | `checkbox` | Focus, Space, checked state |
| `<select>` | `combobox` or `listbox` | Focus, arrow keys, selected state |
| `<h1>` … `<h6>` | `heading` (with level) | Heading navigation (H key in NVDA) |
| `<ul>`, `<ol>` | `list` | "List, 5 items" |
| `<table>` with `<th>` | `table`, `columnheader` | Table navigation, headers read with each cell |
| `<nav>`, `<main>`, `<header>`, `<footer>`, `<aside>` | `navigation`, `main`, `banner`, `contentinfo`, `complementary` | Landmark navigation (D key in NVDA) |
| `<dialog>` with `showModal()` | `dialog` | Focus moved inside, Esc to close, rest of page blocked |
| `<details>` / `<summary>` | `group` / disclosure control | Expand and collapse with Enter or Space, expanded state |

Adding the same role again (`<button role="button">`, `<nav role="navigation">`) does nothing.
It just adds noise to the code.

## When you do need ARIA

Use ARIA when HTML has no element for the pattern, or to expose a state HTML can't express:

| Need | ARIA | Notes |
|---|---|---|
| Tabs | `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected` | Arrow keys move between tabs. See the [APG Tabs pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). |
| Announce a change without moving focus | `role="status"` (polite) or `role="alert"` (urgent) | The element must be in the page *before* the text changes. |
| A toggle that opens something | `aria-expanded="true"` / `"false"` on the button, `aria-controls` | Update it every time the state changes. |
| A toggle button | `aria-pressed="true"` / `"false"` | For buttons like "Bold" or a filter. |
| The current page in navigation | `aria-current="page"` | Sighted users see it highlighted; this says it out loud. |
| An icon-only button | `aria-label="Close"` | Or visually hidden text inside the button. |
| A field with help or error text | `aria-describedby="id-of-text"`, `aria-invalid="true"` | The text is read after the label. |
| Hide decoration from screen readers | `aria-hidden="true"` | Never on something that can get focus. |

Before you build any custom widget, look it up in the
[ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/patterns/). It lists the
roles, states **and keyboard behavior** each pattern needs, with working examples.

## Common mistakes

| Mistake | Why it breaks | Fix |
|---|---|---|
| `<div role="button">` without `tabindex="0"` and key handlers | Announced as a button, but keyboard users can't reach or press it | Use `<button>` |
| `aria-label` on a `<div>` or `<span>` with no role | Many screen readers ignore names on elements with no role | Add a proper role, or use a real control |
| `aria-hidden="true"` on a focusable element | Keyboard focus lands on something the screen reader says doesn't exist | Remove it, or also make the element unfocusable (`inert`, or remove from the Tab order) |
| `aria-label` that differs from the visible text | Voice control users say "click Send", but the control is named "Submit form" | Make the name start with the visible text ([WCAG 2.5.3](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html)) |
| `role="presentation"` or `role="none"` on a focusable or interactive element | The browser ignores the change, or the control loses its meaning | Only use it on purely visual elements, such as layout tables |
| States that are never updated | The menu is open, but `aria-expanded` still says `false` | Update ARIA states in the same code that changes the UI |
| `role="menu"` for site navigation | Screen readers switch to application-menu keyboard mode, which users don't expect on a website | Use `<nav>` with a list of links |
| A live region added to the page at the same time as its message | Often nothing is announced | Render the empty `role="status"` element first, then put the text in |

## How to check your ARIA

- **Look at the accessibility tree** in DevTools (Chrome/Edge: Elements → Accessibility; Firefox:
  Accessibility tab). Each control should have the role, name and state you expect.
- **Run axe-core.** It catches invalid roles, missing required attributes and `aria-hidden` on
  focusable elements. It can't tell you whether a role is the *right* one.
- **Use the keyboard.** Every element with an interactive role must work without a mouse.
- **Use role-based locators in your tests**, so a missing role fails the build.
  See [Test What Scanners Miss](../20-for-developers/test-what-scanners-miss.md).

## Learn more

- [Using ARIA (W3C)](https://www.w3.org/TR/using-aria/) — the five rules of ARIA
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — patterns and keyboard behavior for every widget
- [WAI-ARIA 1.2 specification](https://www.w3.org/TR/wai-aria-1.2/) — the full list of roles, states and properties
- [MDN: ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) — reference for each role and attribute, with examples
- [WebAIM: Introduction to ARIA](https://webaim.org/techniques/aria/)
- [Accessible Web Development Checklist](../20-for-developers/accessible-web-dev-checklist.md)

Have an ARIA pattern or mistake to add? [Suggest it on GitHub](https://github.com/alexarguello/accessibility-hub/issues).
