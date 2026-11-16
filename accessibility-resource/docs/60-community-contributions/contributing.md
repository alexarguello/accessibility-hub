---
title: Contributing to the Accessibility Hub
description: "How to contribute to the Accessibility Hub: find current needs, add or improve a page, write the frontmatter, and submit a pull request."
sidebar_position: 1
hide_title: true
level: intermediate
type: guide
status: draft
content_status: needs-update
audience:
  - developer
  - educator
  - researcher
  - designer
disability_type:
  - general

tags:
  - contribution
  - wcag
  - aria
  - open-source
topics:
  - contribution
  - accessibility
  - wcag
  - aria
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
eta: 2025-12-31
---

# Contributing to the Accessibility Hub
Thank you for your interest in contributing to our **Accessibility Hub**!
Our mission is to create the **most reliable, well-organized, and user-friendly resource** for anyone involved in making the world more accessible. This includes tools, guidelines, and resources for improving digital accessibility in areas such as screen readers, assistive technologies, visual impairments, and more.
By contributing, you help developers, individuals with disabilities, accessibility testers, educators, and advocates find the resources they need to support accessible technology.

## Goals of the Accessibility Hub
1. **Promote Awareness**: Provide actionable and relatable accessibility information.
2. **Serve All Skill Levels**: Create resources for **beginners, experienced professionals, educators**, and **end users**.
3. **Cover Diverse Topics**: Include tools, best practices, regulations, user experience insights, and accessibility technologies.
4. **Improve Accessibility Culture**: Reduce barriers and make digital spaces inclusive.

## Accessible Emoji Policy (Docs and Readme)
- Headings (H1–H6), nav labels, and primary link labels must be plain text; do not include emoji characters.
- Decorative emojis may be used in body text sparingly and must not be the sole carrier of meaning. Always provide clear text.
- Generated artifacts (e.g., Mermaid maps, legends): emojis are stripped from node labels; legends provide textual explanations.
- Authoring rules:
  - Replace heading emojis with text-only headings.
  - If you keep emojis in body text, prefer `<span aria-hidden="true">🙂</span>` with adjacent visible text. In MDX, wrap directly; in MD, rely on our build tooling.
- UI components:
  - Homepage cards render as: title + `<span aria-hidden="true">{emoji}</span>`; the span is only rendered when an emoji is present.
- Tooling and CI:
  - Our Docusaurus build uses a remark plugin that strips emojis from headings.
  - Remark lint runs in CI and will fail PRs that include emojis in headings.

## How to Contribute
Not sure where to start? Here’s how you can pitch in:
### 1. Browse Current Needs
Check the last section in the sidebar called `Contribute`. Here you'll find examples of **resources we need**, as well as requests for improvements to existing materials.
### 2. Add or Improve Resources
Have your own idea? Follow these steps:
- Browse `/docs/` to find the right folder for your topic.
- Copy the [`/docs/.template.md`](https://github.com/alexarguello/accessibility-hub/blob/main/accessibility-resource/docs/.template.md) file as a starting point for your new resource.
- Rename your file (e.g., `screen-readers.md`, `dos-and-donts.md`).

⚠️ Do not name files `_intro.md` or `index.md` — these are reserved for folder landing pages.

### 3. Write and Format the Frontmatter
At the top of every Markdown file, include your **frontmatter** to classify, tag, and describe the resource. 
Frontmatter is essential YAML metadata included in every resource file to ensure classification, seamless system integration, and proper organization. Here are the key highlights:

1. **Purpose**: Frontmatter provides structure by categorizing and describing resources, making them easier to manage and access.
2. **Required Fields**:
  - `title`: A concise, descriptive name for the resource (e.g., "Introduction to ARIA").
  - `type`: The content type (e.g., `overview`, `guide`, `tutorial`, `reference`).
  - `level`: The intended audience expertise level (`beginner`, `intermediate`, or `advanced`).
  - `status`: The development stage of the resource (`draft`, `wip`, `published`).
  - `topics`: Tags summarizing the content, with a focus on:
    - Broad categories like `accessibility`.
    - Specific prefixes such as `assistive-technology`.
    - More about topics [here the Topics guide](/docs/community-contributions/TOPICS_GUIDE)

For the full guide, refer to [FRONTMATTER_GUIDE](/docs/community-contributions/FRONTMATTER_GUIDE).

The required fields are `title`, `description`, `level`, `type`, `status`, `content_status`, `audience` and `disability_type`. The guide lists the allowed values for each.

### 4. Check Your Page Locally
Run these from the `accessibility-resource` folder before you open a pull request:

```bash
npm ci
python flatmap-tools/generate_mermaids.py
npx remark docs/your-folder/your-page.md --frail --quiet --use ./remark/no-heading-emojis.mjs
npx markdown-link-check --config .mlc-config.json --quiet docs/your-folder/your-page.md
npm run build
npm run serve
```

- The generator adds your page to the section maps. Run it again after you add or rename a page.
- The link check reports dead links. Fix them before you submit.
- `npm run serve` shows the built site at `http://localhost:3000/accessibility-hub/`. Open your page and read it once.

### Diagrams
You can add a Mermaid diagram in a fenced `mermaid` code block. A diagram must never be the only place the information lives:

- Write the same content as a numbered list or a table **before** the diagram, and say that the diagram repeats it.
- Give the diagram an `accTitle:` and an `accDescr:` line so screen readers announce what it is.
- Do not use emojis in node labels.

### 5. Submit a Pull Request
Create a Pull Request (PR) in our GitHub repository. Include a summary of your changes, why they're important, and mention any related GitHub issues.

- Start a new branch from `main` for each change, and open the pull request against `main`.
- Keep one change per pull request. Small pull requests are reviewed faster and are easier to trace later.
- The automated checks run on every pull request to `main`. The site is published when the pull request is merged.

## About `_intro.md` Pages
Each directory in `/docs/` can have an `_intro.md` as a **topic landing page**.
### Guidelines for `_intro.md` Files
- Keep it **short and clear** (max 2–3 paragraphs).
- Define the purpose of the section and direct users to subtopics.
- Mention the expected audience, whether beginners, experienced developers, end-users, or educators.
- Ensure the section remains partially visible above **visual diagrams** or **flatmaps** on the site.

## Pull Request Guidelines
When submitting a PR, ensure:
- All **required frontmatter fields** are present.
- **Optional fields** are only added if relevant (e.g., `eta` for planned work).
- Files are placed in the correct folder within `/docs/`.
- Your content aligns with our **accessibility-first values**.

Automated checks run on pull requests to `main`: a link check, a site build, the end-to-end tests and an accessibility scan. The build and the end-to-end tests must pass.

Frontmatter is not validated automatically yet. Check it against the [FRONTMATTER_GUIDE](/docs/community-contributions/FRONTMATTER_GUIDE) yourself:
- Required fields are present and use the allowed values.
- **For planned or in-progress resources**: an `eta` field (completion date) is included.

⚠️ **Tip**: If there’s an issue or discussion related to your PR, reference it in the description!

## Available Topics and Prefixes
To maintain consistency, use the following **topics** when tagging your content:
### General Categories
- `accessibility`
- `assistive-technology`
- `visual-impairment`
- `design-principles`
- `standards` (WCAG, ARIA, etc.)

### Tools (Prefix: `tool:`)
- `tool:JAWS`
- `tool:NVDA`
- `tool:VoiceOver`
- `tool:Narrator`
- `tool:Orca`

### Providers (Prefix: `provider:`)
- `provider:freedom-scientific`
- `provider:microsoft`
- `provider:apple`
- `provider:nv-access`

Include your tags as **specific and accurate as possible** — these improve searchability and structure for other contributors.
For more details, check out the [Topics by Category](/docs/community-contributions/TOPICS_GUIDE).

## Formatting and Writing Guidelines
1. **Focus on Accessibility**: Write with an accessibility-first mindset, including inclusive examples (e.g., using headings, lists, and descriptive text).
2. **Use Clear Language**: Avoid technical jargon whenever possible. Cater to all skill levels.
3. **Cite Reliable Sources**: Reference official accessibility standards (e.g., WCAG, ARIA specifications).
4. **Test Recommendations**: Ensure tools or techniques described in your resource are tested and validated.

## Contributor Responsibilities
Contributors help ensure this hub is **valuable and up-to-date** by:
- Responding to resource requests.
- Keeping planned content on schedule (`eta` informed).
- Updating `draft` or `wip` resources once complete.

## “Planned” or “Work in Progress” Resources
If your resource is still being developed, set its `status` to `planned` or `wip` and include an **estimated completion date** (`eta`).
**Why?**:
- It prevents duplication.
- Maintainers and other contributors can monitor progress or assist.

Thank you for helping make the Accessibility Hub a trusted, inclusive, and insightful resource!

