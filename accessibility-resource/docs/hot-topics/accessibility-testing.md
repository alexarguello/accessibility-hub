---
title: Accessibility Testing
sidebar_position: 1
hide_title: true
description: "An overview of accessibility testing: what automated scanners catch, what they miss, and the manual and code-based tests that fill the gap."
level: beginner
type: guide
status: published
content_status: current
audience:
  - developer
  - designer
disability_type:
  - general

tags:
  - accessibility-testing
  - wcag
  - aria
topics:
  - accessibility-testing
  - wcag
  - tool:axe
  - tool:WAVE
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# Accessibility Testing

Accessibility testing checks whether people with disabilities, and the assistive technology they
use, can perceive and operate your product. In practice it asks one question: **can someone finish
the task** without a mouse, without sight, without hearing, or with an AI agent acting for them?

## Scanners are a minimum, not a result

Automated tools such as axe, WAVE and Lighthouse check your markup against rules. They are fast and
belong in every build. But they only judge code that tries to be a control. A `<div>` styled as a
dropdown has no role, so there is nothing for them to fail.

In the [accessibility tree experiment](../20-for-developers/ai-agents-read-your-accessibility-tree.md),
a form that no screen reader user and no AI agent could complete still scored **91/100** in
Lighthouse.

## What to test, and how

| Test | Catches | Time |
|---|---|---|
| Automated scanner (axe, WAVE, pa11y) | Missing labels, `alt` text, contrast, landmarks | Seconds, in CI |
| Role-based tests (`getByRole`) | Controls with no role or name | Part of your end-to-end tests |
| Keyboard only | Unreachable controls, traps, invisible focus | 5 minutes per flow |
| Screen reader (NVDA, VoiceOver) | Missing announcements, silent errors | 10 minutes per flow |
| Guided review (Accessibility Insights) | Color-only meaning, reading order, text alternatives | 30–60 minutes per page |
| People with disabilities | Real problems no tool predicts | Usability sessions |

## Go deeper

- [Test What Scanners Miss](../20-for-developers/test-what-scanners-miss.md) — which test catches which defect, Java recipes, and step-by-step keyboard and screen reader scripts
- [What to Do Next](../20-for-developers/what-to-do-next.md) — six steps to start on your own app today
- [Accessible Web Development Checklist](../20-for-developers/accessible-web-dev-checklist.md) — WCAG 2.2 AA, with how to check each item
- [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/) — free guided assessment tool
- [WebAIM: Evaluating Web Accessibility](https://webaim.org/articles/evaluationguide/)
