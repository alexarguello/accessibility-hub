---
title: External Resources for Developers
sidebar_label: External Resources
sidebar_position: 9
hide_title: true
description: "A curated list of the standards, guides, testing tools and learning resources developers actually need for accessibility work, grouped by what you're trying to do."
level: beginner
type: resource-list
status: published
content_status: current
audience:
  - developer
disability_type:
  - general

tags:
  - api-design
  - accessibility
  - developer-tools
  - wcag
  - accessibility-testing
topics:
  - api
  - accessibility
  - wcag
  - accessibility-testing
  - tool:axe
  - tool:NVDA
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# External Resources for Developers

The resources below are grouped by what you're trying to do. Each one is free unless noted. If
you're new, start with the first item in each group.

## Understand the rules

| Resource | Use it for |
|---|---|
| [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) | Every success criterion with techniques and failures. Filter by level and technology. |
| [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/) | The intent behind each rule, who it helps, and examples. Read it when a rule is unclear. |
| [WCAG 2.2 (the standard)](https://www.w3.org/TR/WCAG22/) | The normative text, when you need the exact wording. |
| [WebAIM WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist) | A plain-language version of the rules. |

## Understand the accessibility tree

| Resource | Use it for |
|---|---|
| [MDN: Accessibility tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree) | A short definition, with links to go deeper. |
| [HTML Accessibility API Mappings (HTML-AAM)](https://www.w3.org/TR/html-aam-1.0/) | Exactly which role and properties the browser gives each HTML element. |
| [Accessible Name and Description Computation](https://www.w3.org/TR/accname-1.2/) | How the browser decides a control's name: `aria-labelledby`, `aria-label`, `<label>`, content, `title`, placeholder. |
| [Chrome DevTools: Accessibility features](https://developer.chrome.com/docs/devtools/accessibility/reference) | How to inspect the tree, names and contrast in Chrome and Edge. |

## Build components the right way

| Resource | Use it for |
|---|---|
| [ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/) | Roles, states and keyboard behavior for tabs, dialogs, menus, comboboxes and more, with working examples. |
| [Using ARIA](https://www.w3.org/TR/using-aria/) | The five rules of ARIA. Rule one: use native HTML first. |
| [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility) | Reference for every ARIA role and attribute, plus guides. |
| [Inclusive Components](https://inclusive-components.design/) | Long-form explanations of how to build common components accessibly, and why. |
| [W3C WAI Tutorials](https://www.w3.org/WAI/tutorials/) | Step-by-step guides for forms, tables, images, menus and carousels. |

On this site: [ARIA Roles](../hot-topics/aria-roles.md) and the [Accessible Web Development Checklist](./accessible-web-dev-checklist.md).

## Test your work

| Resource | Use it for |
|---|---|
| [axe-core](https://github.com/dequelabs/axe-core) | The rules engine behind most scanners. Run it in your test suite. |
| [axe-core for Java (Maven)](https://github.com/dequelabs/axe-core-maven-html) | Bindings for Playwright, Selenium and HtmlUnit. |
| [Playwright: Accessibility testing](https://playwright.dev/java/docs/accessibility-testing) | Using axe with Playwright, plus [aria snapshots](https://playwright.dev/java/docs/aria-snapshots). |
| [Testing Library: ByRole](https://testing-library.com/docs/queries/byrole/) | Role-based queries for JavaScript component tests. |
| [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/) | Free browser extension from Microsoft. FastPass for quick checks, Assessment for a guided WCAG review. |
| [WAVE](https://wave.webaim.org/) | Browser extension that shows issues directly on the page. |
| [pa11y](https://pa11y.org/) | Command-line scanner, easy to add to CI. |
| [IBM Equal Access Toolkit](https://www.ibm.com/able/toolkit/tools/) | IBM's accessibility checker, as a browser extension and for automation. |
| [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) | Check any two colors against WCAG contrast rules. |
| [W3C list of evaluation tools](https://www.w3.org/WAI/test-evaluate/tools/list/) | A searchable list of over 100 tools. |

On this site: [Test What Scanners Miss](./test-what-scanners-miss.md) explains what each kind of test catches.

## Use a screen reader

| Resource | Use it for |
|---|---|
| [NVDA](https://www.nvaccess.org/download/) | Free screen reader for Windows. Use it with Firefox. |
| [WebAIM: Using NVDA to Evaluate Web Accessibility](https://webaim.org/articles/nvda/) | The keys you need, and how to test with it. |
| [VoiceOver User Guide (Mac)](https://support.apple.com/guide/voiceover/welcome/mac) | Built into macOS; turn it on with Cmd+F5. |
| [WebAIM: Using VoiceOver to Evaluate Web Accessibility](https://webaim.org/articles/voiceover/) | The Mac equivalent of the NVDA guide. |
| [JAWS](https://www.freedomscientific.com/products/software/jaws/) | Widely used commercial screen reader for Windows (paid; has a demo mode). |

## Keep learning

| Resource | Use it for |
|---|---|
| [web.dev: Learn Accessibility](https://web.dev/learn/accessibility) | A free, structured course from the Chrome team. |
| [W3C WAI: Digital Accessibility Foundations](https://www.w3.org/WAI/courses/foundations-course/) | Free online course from the W3C. |
| [The A11Y Project](https://www.a11yproject.com/) | Community-driven checklist, articles and resources. |
| [WebAIM articles](https://webaim.org/articles/) | In-depth articles on almost every accessibility topic. |
| [Deque University](https://dequeuniversity.com/) | Courses and references (some free, most paid). |

On this site: [Communities & Groups](../40-resources/communities-groups.md) and [Conferences & Events](../40-resources/conferences-events.md).

## Design accessible APIs and developer tools

| Resource | Use it for |
|---|---|
| [How to design APIs for accessibility (endjin)](https://endjin.com/blog/2023/01/design-apis-for-accessibility) | Naming and documentation choices that help developers who use screen readers. |
| [How to Design More Inclusive APIs (Nordic APIs)](https://nordicapis.com/how-to-design-more-inclusive-apis/) | Inclusive naming and documentation practices. |
| [API Accessibility: Designing Inclusive Data Interfaces](https://accessibility-test.org/blog/apis/api-accessibility-designing-inclusive-data-interfaces/) | Making API responses easier to use in accessible apps. |
| [Accessibility APIs and their modern use case for UX (LogRocket)](https://blog.logrocket.com/ux-design/accessibility-apis-use-case-ux/) | How operating system accessibility APIs connect apps to assistive technology. |
| [The accessibility-first approach (dev.to series)](https://dev.to/yuridevat/series/18719) | A series of practical articles for front-end developers. |

On this site: [Accessible API Design for Developers](./accessible-api-design-guide.md).

---

Know a resource that should be here? [Suggest it on GitHub](https://github.com/alexarguello/accessibility-hub/issues).
