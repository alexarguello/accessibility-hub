---
title: Frontmatter Guide
type: reference
level: beginner
status: published
content_status: current
audience:
  - developer
  - educator
  - researcher
disability_type:
  - general

tags:
  - contribution
  - documentation
  - accessibility
topics:
  - contribution
  - accessibility
author: ["Alexandra Arguello Saenz (https://github.com/alexarguello)"]
---

Every Markdown file in `/docs/` must include a YAML frontmatter block at the top. This classifies the document for filtering, search, and the flatmap renderer.

## Quick Template

```yaml
---
title: Your Resource Title
sidebar_position: 1
hide_title: true
level: beginner
type: guide
status: draft
content_status: placeholder
audience:
  - end-user
disability_type:
  - general
tags:
  - accessibility
topics:
  - tool:example
author: ["Your Name (https://github.com/your-profile)"]
eta: 2025-12-31
---
```

For the full template with all optional fields, copy `docs/.template.md`.

---

## Required Fields

### `title` · string

Concise display title shown in the sidebar, flatmap nodes, and search results.

```yaml
title: Introduction to Screen Readers
```

---

### `status` · enum

The publication state of the page.

| Value | Meaning |
|---|---|
| `draft` | Written but not yet reviewed |
| `wip` | Actively being written — partial content |
| `published` | Reviewed and complete |
| `planned` | Stub — content not started yet |

`planned` and `wip` require an `eta` date.

```yaml
status: draft
```

---

### `level` · enum

Expected expertise of the reader.

| Value | Reader |
|---|---|
| `beginner` | No prior accessibility knowledge needed |
| `intermediate` | Basic accessibility concepts assumed |
| `advanced` | Deep technical content (ARIA internals, API design) |
| `expert` | Specialist topics (standards authoring, AT development) |

```yaml
level: beginner
```

---

### `type` · enum

The format and purpose of the content.

| Value | Use for |
|---|---|
| `overview` | Section intro — sets context, links to subtopics |
| `guide` | Step-by-step instructional content |
| `tutorial` | Hands-on walkthrough with concrete exercises |
| `reference` | Lookup content — specs, comparisons, criteria |
| `api-doc` | API or SDK documentation with code examples |
| `checklist` | Structured list of actionable items to verify |
| `resource-list` | Curated list of external links with descriptions |

```yaml
type: guide
```

---

### `content_status` · enum

How complete the actual content is, independent of the publication `status`. Used to triage work.

| Value | Meaning |
|---|---|
| `placeholder` | Title + stub only — no real content yet |
| `shallow` | Has content but needs significant expansion |
| `current` | Complete and accurate |
| `needs-update` | Has content but outdated or references stale info |

```yaml
content_status: shallow
```

---

### `audience` · array of enum

Who this document is for. Used by the `/guide-me` chatbot for persona routing and by nav filters.

| Value | Who |
|---|---|
| `end-user` | People with disabilities using assistive technology |
| `caregiver` | Family members and support workers |
| `developer` | Engineers building accessible software |
| `designer` | UX/product designers |
| `educator` | Teachers and trainers |
| `researcher` | Academic or policy researchers |
| `business` | Product managers, executives, procurement |

Use multiple values when content genuinely serves multiple audiences.

```yaml
audience:
  - end-user
  - caregiver
```

---

### `disability_type` · array of enum

Which disability category the content primarily addresses. This is the primary filter axis in the For Users section.

| Value | Covers |
|---|---|
| `visual` | Blindness, low vision, color blindness |
| `hearing` | Deafness, hard of hearing, auditory processing |
| `cognitive` | Dyslexia, ADHD, intellectual disabilities, dementia |
| `mobility` | Limb differences, paralysis, motor impairments |
| `speech` | Aphasia, dysarthria, stuttering, AAC users |
| `neurological` | Autism, ADHD, epilepsy, neurodiversity broadly |
| `chronic-illness` | Fatigue, pain, conditions that fluctuate |
| `aging` | Age-related changes in dexterity, vision, hearing, cognition |
| `multiple` | Content addressing two or more disability types together |
| `general` | Not disability-specific (WCAG standards, tooling, contribution guides) |

```yaml
disability_type:
  - visual
  - hearing
```

---

## Optional Fields

### `tags` · array of string

Human-readable content keywords rendered by Docusaurus as clickable chips at the bottom of each page. All tags are browsable at [`/docs/tags/`](/docs/tags).

Use 2–4 tags per doc. Choose words a site visitor would search or browse by — not structural metadata (don't repeat `level` or `type` values here).

**Good tag examples:** `screen-readers`, `wcag`, `aria`, `color-contrast`, `captions`, `keyboard-accessibility`, `alt-text`, `aac`, `stroke`, `cognitive-accessibility`, `inclusive-design`, `api-design`, `mobile-accessibility`, `pdf-accessibility`, `dyslexia`, `braille`, `voice-control`, `ai-accessibility`

> **`tags` vs `topics`** — these serve different systems:
>
> | | `tags` | `topics` |
> |---|---|---|
> | **Rendered by** | Docusaurus — chip list on each page, `/docs/tags/` browsing | Internal — `/guide-me` chatbot + search index |
> | **Audience** | Site visitors | Code and tools |
> | **Format** | Short human-readable words | Prefixed conventions (`tool:NVDA`, `provider:apple`) |

```yaml
tags:
  - screen-readers
  - wcag
  - aria
```

---

### `topics` · array of string

Machine-readable keywords for specific tools, providers, standards, and subtopics. Used by the `/guide-me` chatbot and search indexing. Never rendered as Docusaurus tags. Keep `topics` focused — do not repeat values already expressed by `audience` or `disability_type`.

**Conventions:**

| Prefix | Example | Use for |
|---|---|---|
| `tool:` | `tool:NVDA` | Specific software tools |
| `provider:` | `provider:apple` | Organizations and vendors |
| `wcag:` | `wcag:1.4.3` | Specific WCAG success criteria |
| (none) | `aria`, `stroke`, `aac` | Specific subtopics |

```yaml
topics:
  - tool:NVDA
  - tool:JAWS
  - provider:nv-access
  - wcag:1.4.1
  - aria
```

---

### `author` · array of string

Contributor name(s) and optional GitHub profile links.

```yaml
author: ["Alexandra Arguello Saenz (https://github.com/alexarguello)"]
```

---

### `eta` · date (YYYY-MM-DD)

Estimated completion date. **Required when `status` is `draft`, `wip`, or `planned`.** Remove when the page reaches `published`.

```yaml
eta: 2025-09-01
```

---

### `sidebar_position` · integer

Controls sidebar 