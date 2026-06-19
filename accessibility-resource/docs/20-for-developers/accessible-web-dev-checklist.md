---
title: Accessible Web Development Checklist
sidebar_position: 5
hide_title: true
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
  - Your Name (https://github.com/your-profile)
---

# Accessible Web Development Checklist

A comprehensive checklist based on WCAG 2.1 Level AA and best practices from W3C, WebAIM, and Section508.gov.

---

## Structure & Semantics
- [ ] Use semantic HTML (`<header>`, `<nav>`, `<main>`, `<footer>`, etc.)
- [ ] Use headings (`<h1>` to `<h6>`) in a logical, nested order
- [ ] Use lists (`<ul>`, `<ol>`, `<dl>`) for grouped content
- [ ] Use landmarks (`<main>`, `<aside>`, `<section>`) to define page regions

## Keyboard Accessibility
- [ ] All interactive elements are reachable and usable via keyboard
- [ ] Focus order is logical and intuitive
- [ ] Visible focus indicator is present and clearly visible
- [ ] No keyboard traps (user can tab in and out of all components)

## Screen Reader Support
- [ ] Use `aria-label`, `aria-labelledby`, or `aria-describedby` where needed
- [ ] Use `role` attributes appropriately (e.g., `role="dialog"`)
- [ ] Avoid redundant or conflicting ARIA roles
- [ ] Dynamic content updates are announced (e.g., using `aria-live`)

## Visual Design & Contrast
- [ ] Text has a contrast ratio of at least 4.5:1 against its background
- [ ] Large text (18pt or 14pt bold) has a contrast ratio of at least 3:1
- [ ] Color is not the only means of conveying information
- [ ] Users can resize text up to 200% without loss of content or functionality

## Images & Media
- [ ] All informative images have descriptive `alt` text
- [ ] Decorative images use `alt=""` or `role="presentation"`
- [ ] Videos have captions and transcripts
- [ ] Audio content has transcripts
- [ ] Avoid auto-playing media or provide a way to pause/stop it

## Forms & Inputs
- [ ] All form fields have associated `<label>` elements
- [ ] Required fields are clearly indicated
- [ ] Error messages are descriptive and programmatically associated
- [ ] Use `fieldset` and `legend` for grouped form controls

## Responsive & Mobile
- [ ] Layout adapts to various screen sizes and orientations
- [ ] Touch targets are large enough and spaced appropriately
- [ ] No horizontal scrolling required at 320px width

## JavaScript & Dynamic Content
- [ ] Custom components are accessible via keyboard
- [ ] Use ARIA roles and states for custom widgets
- [ ] Ensure focus is managed correctly (e.g., modals, menus)
- [ ] Announce dynamic updates using `aria-live` regions

## Testing & Validation
- [ ] Run automated tests (axe, WAVE, Lighthouse)
- [ ] Conduct manual keyboard and screen reader testing
- [ ] Validate HTML and CSS
- [ ] Include users with disabilities in usability testing
