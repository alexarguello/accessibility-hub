---
title: Contributing to Accessibility Hub
sidebar_position: 1
hide_title: true
level: beginner
type: tutorial
status: draft
visibility: public
topics:
  - community-contributions
  - accessibility
  - onboarding
author: ["Alexandra Arguello Saenz (https://github.com/alexarguello)"]
---

# Contributing to Accessibility Hub

Thank you for your interest in contributing to the Accessibility Hub! This project thrives on community input to grow a rich, inclusive, and practical resource for accessible technology.

> If you're new here, start with **`docs/00-about/overview.md`** and **`README.md`** to understand the mission and information architecture.

---

## 🔎 What You Can Contribute

We welcome contributions such as:

- **Guides** – Step-by-step tutorials on accessibility topics
- **Tools** – Assistive technologies, testing utilities, or developer aids
- **Case Studies** – Real-world examples of accessibility in practice
- **External Resources** – Curated links to valuable articles, videos, or tools

See also:
- `docs/60-community-contributions/whats-missing.md` – open needs & ideas
- `docs/60-community-contributions/to-do-list.md` – tasks and backlog
- `docs/60-community-contributions/getting-started.md` – onboarding tips

---

##  Where to Place Your File

Choose the folder that best matches your contribution:

- `docs/40-resources/` – General resources, catalogs, patterns
- `docs/50-use-cases/` – Scenario-based content and examples
- `docs/60-community-contributions/` – Community-led content (templates, calls-for-help, dashboards)

> Use existing files as references, and the general content template at **`docs/.template.md`**.

---

##  Required Frontmatter (Metadata)

Add YAML frontmatter at the top of your Markdown file. This powers navigation, tagging, and dashboards.

```yaml
---
# Required
title: "Descriptive, concise title"
type: guide # one of: guide | tool | case-study | external
status: draft # one of: draft | review-needed | published

# Recommended
summary: "1–3 sentence summary for previews and SEO"
author: "Your Name (@github-handle)"
audience: [users, developers, educators]
focus: [vision, hearing, cognitive, mobility, universal]
tags: [tag-one, tag-two]
links:
  - label: "Official site"
    url: "https://example.com"
  - label: "Source / repo"
    url: "https://github.com/…"
---
````

Refer to **`FRONTMATTER_GUIDE.md`** and **`TOPICS_GUIDE.md`** at the repository root for detailed definitions and best practices.

***

## Accessibility Best Practices for Contributions

Please align with our accessibility principles:

*   **Headings**: Use meaningful, nested headings (`#`, `##`, `###`). Avoid emojis in headings and primary link labels (see Accessible Emoji Policy in `README.md`).
*   **Alt text**: Provide descriptive `alt` text for all images. If decorative, use empty alt (e.g., `alt=""`).
*   **Color & contrast**: Ensure examples, screenshots, and diagrams meet WCAG contrast guidance.
*   **Links**: Use descriptive link text (avoid "click here").
*   **Code blocks**: Add language hints for syntax highlighting and accessibility (e.g., `js, `html).
*   **Tables**: Include headers; keep simple and scannable.
*   **Plain language**: Prefer short sentences and clear vocabulary.

> Tip: When in doubt, check similar pages under `docs/40-resources/` for examples of tone, structure, and tags.

***

##  Pre-Submission Checklist

Before opening a PR:

*   [ ] File placed in the correct directory (see **Where to Place Your File**)
*   [ ] Frontmatter includes `title`, `type`, and `status`
*   [ ] Tags and focus areas reflect the content
*   [ ] Images include appropriate `alt` text
*   [ ] Links are valid and use descriptive labels
*   [ ] Markdown passes a quick lint (headings, lists, code blocks render properly)

***

##  How to Submit a Pull Request

1.  **Fork** this repository and **create a feature branch**:
    ```bash
    git checkout -b feat/add-{short-topic-name}
    ```
2.  **Add your content** under the appropriate folder.
3.  **Commit** with a clear message:
    ```bash
    git add path/to/file.md
    git commit -m "docs: add {title} ({type})"
    git push origin feat/add-{short-topic-name}
    ```
4.  **Open a Pull Request** against `main`:
    *   Use a concise title (e.g., `docs: add Accessible Forms guide`)
    *   In the PR description, include:
        *   Purpose and summary
        *   Any open questions
        *   Screenshots (if UI-related)
        *   Checklist confirmation

> If your contribution replaces or deprecates content, reference the file(s) and explain the change.

***

##  Reviews & Status

*   New content typically starts as `status: draft`.
*   Maintainers (and community reviewers) may propose edits via suggestions.
*   Once approved, the page is moved to `status: published`.
*   Larger changes might be routed through Discussions before merging.

***

##  Helpful Templates & References

*   Content template: `docs/.template.md`
*   Interview template: `docs/60-community-contributions/interview-template.md`
*   What’s missing: `docs/60-community-contributions/whats-missing.md`
*   To-do list: `docs/60-community-contributions/to-do-list.md`
*   Project setup: `PROJECTSETUP.md`

***

##  Questions or Support

*   Open a **Discussion** in the repo if enabled
*   Or create a **draft PR** to get early feedback

Thank you for helping build a more accessible digital world! 🌍

````

