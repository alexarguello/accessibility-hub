## 🛠️ Metadata for Resources (Frontmatter)
Every file must include a `frontmatter` section (YAML metadata) to classify and describe the resource. This helps us organize the hub and ensures your contribution integrates seamlessly into our systems.
You can find a full **frontmatter guide** [here](FRONTMATTER_GUIDE.md), but below are **standard fields** for accessibility-related content:
### **Required Metadata Fields**
- `title`: concise resource name (e.g., "Introduction to ARIA").
- `type`: type of content (e.g., `overview`, `guide`, `tutorial`, `reference`).
- `level`: target expertise level (`beginner`, `intermediate`, `advanced`).
- `status`: resource status (`draft`, `wip`, `published`).
- `topics`: tags summarizing content. Split into **general categories** and **specific prefixes** like:
  - Accessibility basics: `accessibility`, `assistive-technology`.
  - Tools: `tool:JAWS`, `tool:NVDA`, `tool:VoiceOver`, etc.
  - Providers: `provider:freedom-scientific`, `provider:apple`.

### **Optional Metadata Fields**
- `author`: your name or team (GitHub links welcome!).
- `visibility`: public or internal (default: `public`).
- `features`: optional fields like `priority` or `responsibility`.
- 
# 📖 Guide to Writing Frontmatter for Resources
The `frontmatter` is a YAML block at the top of each Markdown file used to classify, tag, and describe your resource. It ensures the resource is easy to find, well-structured, and properly rendered on the platform.
## **General Rules**
1. **Required Fields**: These are mandatory for all resources (`title`, `type`, etc.). Always include them.
2. **Optional Fields**: These fields provide more context for maintainers or downstream consumers but can be skipped unless necessary.
3. **Syntax**:
  - Use consistent indentation (two spaces).
  - Use lowercase for predefined values (e.g., `status: draft`, not `Draft`).

## **Frontmatter Template Example**
``` yaml
---
title: My Resource Title
sidebar_position: 1
hide_title: true
level: beginner
type: overview
status: published
visibility: public
topics:
  - topic-example1
  - topic-example2
author: ["Your Name (https://github.com/your-profile)"]
eta: 2024-01-15
feature-priority: low
feature-responsible: Team Name / Contact
---
```
## **Field-by-Field Guide**
### 1. **`title`** (Required)
- **Description**: The resource's display title. Should be concise and descriptive.
- **Example**: `"Introduction to Accessibility Tools"`

### 2. **`sidebar_position`** (Optional)
- **Description**: Position of the resource in the sidebar navigation.
- **Value**: An integer defining the position (e.g., `1`, `2`). Lower numbers appear first.

### 3. **`hide_title`** (Optional)
- **Description**: Determines if the title should be hidden on the rendered page.
- **Values**:
  - `true`: Hide the title.
  - `false`: Show the title.

### 4. **`level`** (Required)
- **Description**: Difficulty level or intended audience expertise.
- **Allowed Values**:
  - `beginner`
  - `intermediate`
  - `advanced`

### 5. **`type`** (Required)
- **Description**: The type or purpose of the resource.
- **Allowed Values**:
  - `overview`
  - `tutorial`
  - `reference`
  - `guide`
  - `documentation`

### 6. **`status`** (Required)
- **Description**: Current state of the resource in the development process.
- **Allowed Values**:
  - `draft`: A work-in-progress; not ready for publication.
  - `planned`: Planned work that isn’t started yet. Must include `eta`.
  - `wip`: "Work in progress"; partially complete.
  - `published`: Fully complete and published.

### 7. **`visibility`** (Required)
- **Description**: Defines who can see the resource.
- **Allowed Values**:
  - `public`: Visible to everyone.
  - `internal`: Only visible to project team members.

### 8. **`topics`** (Required)
- **Description**: List of tags or keywords that contextualize the resource.
- **Best Practices**:
  - Use existing topics if possible for consistency.
  - Topics can include categories (e.g., `accessibility`), tools (e.g., `tool:JAWS`), and providers (e.g., `provider:microsoft`).

**Examples**:
- `accessibility`
- `assistive-technology`
- `tool:JAWS`
- `tool:NVDA`
- `provider:microsoft`

### 9. **`author`** (Optional)
- **Description**: Name(s) and GitHub profile(s) of the author(s).
- **Value**: A list with names and optional profiles.
- **Example**:
``` yaml
  author: ["Alexandra Arguello Saenz (https://github.com/alexarguello)"]
```
### 10. **`eta`** (Optional but Required for `planned` or `wip` statuses)
- **Description**: Estimated time of arrival (completion date) for incomplete resources.
- **Value**: A date in `YYYY-MM-DD` format.
- **Example**: `eta: 2024-03-01`

### 11. **`feature-priority`** (Optional)
- **Description**: Indicates the priority level of this resource for the project.
- **Allowed Values**:
  - `low`
  - `medium`
  - `high`

### 12. **`feature-responsible`** (Optional)
- **Description**: Name or group responsible for maintaining or completing the resource.
- **Value**: A person or team name.
- **Example**:
``` yaml
  feature-responsible: Accessibility Team
```
## **Allowed Values for Topics**
Here is a list of example topics you can use. Note that these are not exhaustive, and you can add new ones, but using existing ones ensures consistency:
### General Categories
- `accessibility`
- `visual-impairment`
- `assistive-technology`
- `screen-readers`
- `usability`

### Tools (Prefix: `tool:`)
- `tool:JAWS`
- `tool:NVDA`
- `tool:VoiceOver`
- `tool:Narrator`
- `tool:Orca`

### Providers (Prefix: `provider:`)
- `provider:freedom-scientific`
- `provider:nv-access`
- `provider:apple`
- `provider:microsoft`

## **Best Practices for Creating Frontmatter**
1. **Organize your topics**: Use categories and prefixes (e.g., `tool:`, `provider:`) to keep tags structured.
2. **Keep values accurate**: Ensure the correct `status` is set (`draft`, `wip`, etc.) and update `eta` for incomplete resources.
3. **Reusability**: Try to use existing topics and values whenever possible.
4. **Clarity**: Use clear titles to align with the resource purpose.

With this guide, you'll ensure all resources include consistent, high-quality frontmatter, making them easier to search, classify, and maintain. If followed correctly, this approach will also streamline triage and visualization of your content!
