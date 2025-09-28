---
# Resource Metadata: Fill in the fields below to ensure proper classification and organization.
title: Accessible Web Development Checklist  # A concise, descriptive title (e.g., "Introduction to ARIA")
sidebar_position: 5
hide_title: true

# REQUIRED METADATA — please complete all fields:
level: beginner             # Target audience expertise: beginner / intermediate / advanced
type: guide                 # Type of content: overview / guide / tutorial / reference
status: draft               # Current state: draft / wip (work in progress) / published
visibility: public          # Visibility: public (default) or internal
topics:
  - accessibility
  - web-standards
  - semantic-html
  - keyboard-accessibility
  - screen-reader-support
  - aria
  - color-contrast
  - visual-design
  - responsive-design
  - images-and-media
  - alt-text
  - forms-and-inputs
  - error-messages
  - mobile-accessibility
  - touch-accessibility
  - dynamic-content
  - testing
  - validation

# OPTIONAL METADATA — provide only if applicable:
author: ["Your Name (https://github.com/your-profile)"]  # Contributor(s)

eta: 2026-01-15             # Estimated completion date for draft or planned resources
feature-priority: high      # Priority level for feature-related resources: low / medium / high

# article-priority: high   # high / medium — omit if not important
# collaboration: open      # set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  # explain what help is welcome (appears on the dashboard & collab page)
# review-reason: "seems not to be on the right topic" # required when status: review-needed — will show on the article and in the dashboard
# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview        # missing / experimental / preview / stable / specified
# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>

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
