---
title: Accessible Web Development Checklist
sidebar_position: 5
hide_title: true
description: "A practical WCAG 2.2 Level AA checklist for developers. Every item links to the WCAG rule behind it and says how to check it in a few minutes."
level: beginner
type: checklist
status: published
content_status: current
audience:
  - developer
  - designer
disability_type:
  - general

tags:
  - wcag
  - aria
  - color-contrast
  - keyboard-accessibility
topics:
  - wcag
  - semantic-html
  - aria
  - color-contrast
  - keyboard-accessibility
  - tool:axe
  - tool:Lighthouse
  - tool:WAVE
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# Accessible Web Development Checklist

A practical checklist based on **WCAG 2.2 Level AA**, the level most laws and contracts ask for.
Each item shows the WCAG rule (success criterion) behind it, linked to the W3C page that explains
it, and a quick way to **check** it.

**How to use it:** run it on one user flow at a time, such as login or checkout, not the whole site
at once. Items marked *scanner* are usually caught by axe, WAVE or Lighthouse. Everything else needs
a person. [Test What Scanners Miss](./test-what-scanners-miss.md) explains why.

---

## Structure & Semantics

The accessibility tree is built from your HTML. Correct elements give screen readers and AI agents
the right roles for free.

- **Use semantic elements** (`<header>`, `<nav>`, `<main>`, `<footer>`, `<button>`, `<a href>`) instead of styled `<div>`s.
  WCAG [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).
  *Check:* open the browser's accessibility tree. Controls should show as `button`, `link` or `textbox`, not `generic`.
- **One `<h1>`, then headings in order** without skipping levels for styling.
  WCAG [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [2.4.6](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html).
  *Check:* list the headings with a browser extension or NVDA's Elements List (Insert+F7). They should read like a table of contents. *Scanner: partly.*
- **Use lists** (`<ul>`, `<ol>`, `<dl>`) for groups of items, such as navigation links.
  WCAG [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html).
  *Check:* a screen reader should say "list, 5 items".
- **Mark up page regions with landmarks**, with exactly one `<main>`.
  WCAG [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [2.4.1](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html).
  *Check:* press D in NVDA to jump between landmarks. *Scanner: yes.*
- **Give every page a unique, descriptive `<title>`.**
  WCAG [2.4.2](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html).
  *Check:* read the browser tab. It should say what the page is, for example "Register — Workshop 123".
- **Set the page language** with `<html lang="en">`.
  WCAG [3.1.1](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html).
  *Check:* view source. Without it, screen readers may read the page in the wrong accent. *Scanner: yes.*

## Keyboard Accessibility

Many people never use a mouse: screen reader users, people with motor disabilities, power users and
many AI agents.

- **Every interactive element works with the keyboard alone.**
  WCAG [2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html).
  *Check:* put the mouse away and complete the flow with Tab, Enter, Space, arrows and Esc.
- **Focus order follows the reading order.**
  WCAG [2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).
  *Check:* Tab through the page. Avoid positive `tabindex` values, which break the natural order.
- **Focus is always visible.** Don't remove `outline` without replacing it.
  WCAG [2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html).
  *Check:* at every Tab stop you should see where you are.
- **Focus is never hidden** behind sticky headers, cookie banners or chat widgets.
  WCAG [2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) (new in 2.2).
  *Check:* Tab through a long page with the sticky header visible.
- **No keyboard traps.** You can always Tab or Esc out of any component.
  WCAG [2.1.2](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html).
  *Check:* Tab into embedded players, editors and date pickers, then try to leave.
- **A "Skip to main content" link** is the first thing in the Tab order on pages with long navigation.
  WCAG [2.4.1](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html).
  *Check:* load the page and press Tab once.

## Screen Reader Support

Every control needs a role, a name and a state. Native HTML provides them. ARIA is for when native
HTML can't. See [ARIA Roles](../hot-topics/aria-roles.md).

- **Every control has an accessible name** that matches its visible label.
  WCAG [4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html), [2.5.3](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html).
  *Check:* icon-only buttons need `aria-label`; a button showing "Send" should not be named "Submit form". *Scanner: partly.*
- **Use ARIA only when no native element exists**, and never contradict the native role (for example `<button role="link">`).
  WCAG [4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).
  *Check:* search the code for `role=`. Each one should have a reason. *Scanner: catches invalid ARIA, not unnecessary ARIA.*
- **States are exposed and kept in sync**: `aria-expanded` on toggles, `aria-pressed` on toggle buttons, `aria-current="page"` on the current nav link.
  WCAG [4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).
  *Check:* open and close a menu while watching the accessibility tree. The state should change.
- **Status messages are announced** without moving focus: "Saved", "3 results", "Item added to cart".
  WCAG [4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
  *Check:* use `role="status"` (polite) or `role="alert"` (urgent), and listen with a screen reader.
- **Link text makes sense on its own**, or with its surrounding sentence. Avoid "click here" and "read more".
  WCAG [2.4.4](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html).
  *Check:* open NVDA's Elements List, Links tab. Each link should be clear out of context.

## Visual Design & Contrast

- **Text contrast is at least 4.5:1** against its background.
  WCAG [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
  *Check:* the color picker in Chrome or Firefox DevTools shows the ratio. *Scanner: yes, except text on images.*
- **Large text has contrast of at least 3:1.** Large means 24px, or 18.66px bold.
  WCAG [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- **Controls, focus outlines and meaningful icons have contrast of at least 3:1.**
  WCAG [1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
  *Check:* input borders and focus rings are the most common failures. Scanners don't check these.
- **Color is never the only signal.** Add text, an icon or a pattern.
  WCAG [1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).
  *Check:* view the page in grayscale (DevTools → Rendering → Emulate vision deficiencies). Errors, required fields and chart lines should still be clear.
- **Text can be resized to 200%** without content being cut off.
  WCAG [1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).
  *Check:* zoom the browser to 200%.
- **Text spacing can be increased** without breaking the layout.
  WCAG [1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html).
  *Check:* fixed-height containers with text are the usual cause. Use `min-height` instead.

## Images & Media

- **Informative images have `alt` text** that says what the image means, not what it looks like.
  WCAG [1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).
  *Check:* a scanner finds missing `alt`; only a person can judge whether it's useful. *Scanner: partly.*
- **Decorative images use `alt=""`** so screen readers skip them.
  WCAG [1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).
- **Charts and diagrams have a text alternative**: a summary, or the data as a table.
  WCAG [1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html).
- **Videos have captions.**
  WCAG [1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html).
  *Check:* review auto-generated captions; they often get names and technical terms wrong.
- **Videos have audio description** when important information is only shown visually.
  WCAG [1.2.5](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html).
- **Audio-only content has a transcript.**
  WCAG [1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html).
- **No auto-playing sound**, and moving content (carousels, animations) can be paused.
  WCAG [1.4.2](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html), [2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).

## Forms & Inputs

Forms are where most user flows fail, for people and for agents.

- **Every field has a visible `<label>`** connected with `for` and `id`. A placeholder is not a label: it disappears when you type.
  WCAG [3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html), [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html).
  *Check:* click the label text. The field should get focus. *Scanner: yes.*
- **Required fields are shown in text**, not only with a red asterisk, and marked with `required` or `aria-required="true"`.
  WCAG [3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html).
- **Errors are described in text and announced.** Say which field is wrong and how to fix it.
  WCAG [3.3.1](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html), [3.3.3](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html), [4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
  *Check:* submit with a mistake while a screen reader is on. Connect the message to the field with `aria-describedby` and set `aria-invalid="true"`.
- **Related controls are grouped** with `<fieldset>` and `<legend>`, for example radio buttons.
  WCAG [1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html).
- **Personal fields use `autocomplete`** (`name`, `email`, `tel`, `street-address`).
  WCAG [1.3.5](https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html).
  *Check:* the browser should offer to fill them. This also helps AI agents fill forms correctly.
- **Don't ask for the same information twice** in one process. Pre-fill it or let users select it.
  WCAG [3.3.7](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) (new in 2.2).
- **Login doesn't depend on memory or puzzles.** Allow paste and password managers. Offer an alternative to cognitive CAPTCHAs.
  WCAG [3.3.8](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) (new in 2.2).
- **Changing a field doesn't cause a surprise**, such as submitting the form or jumping to another page.
  WCAG [3.2.2](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html).

## Responsive & Mobile

- **Content reflows at 320 CSS pixels wide** with no horizontal scrolling (except for content like maps and data tables).
  WCAG [1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
  *Check:* zoom the browser to 400% on a 1280px-wide window.
- **Touch targets are at least 24×24 CSS pixels**, or have enough space around them.
  WCAG [2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) (new in 2.2).
  *Check:* small icon buttons and close (×) buttons are the usual failures.
- **Works in both portrait and landscape.**
  WCAG [1.3.4](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html).
- **Anything done by dragging can also be done with a single click or tap**, such as sliders and reordering lists.
  WCAG [2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) (new in 2.2).

## JavaScript & Dynamic Content

- **Custom components work with the keyboard** and expose the right role and state. Follow the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/patterns/) pattern for that widget.
  WCAG [2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).
  *Check:* better still, use the native element (`<select>`, `<dialog>`, `<details>`) and avoid the work.
- **Focus is managed**: it moves into a dialog when it opens, stays there, and goes back to the button that opened it.
  WCAG [2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).
  *Check:* the native `<dialog>` element with `showModal()` does most of this for you.
- **Content changes are announced** with live regions (`role="status"`, `role="alert"`). The live region must exist in the page before its content changes.
  WCAG [4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
- **In single-page apps, route changes are announced**: update the `<title>` and move focus to the new `<h1>` or announce the new page.
  WCAG [2.4.2](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html), [2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).

## Testing & Validation

- **Run an automated scanner in CI** (axe-core, pa11y, WAVE, Lighthouse). Treat it as a minimum: it misses most problems that block a whole task.
- **Write end-to-end tests with role-based locators** (`getByRole`), so every test also checks the accessibility tree.
- **Do a keyboard-only check** on each changed user flow.
- **Do a screen reader check** before each release (NVDA + Firefox, or VoiceOver + Safari).
- **Include people with disabilities** in usability testing.

Recipes and step-by-step scripts for all of these: [Test What Scanners Miss](./test-what-scanners-miss.md).

---

**Sources:** [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) · [WebAIM WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist) · [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
