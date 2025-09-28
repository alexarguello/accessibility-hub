---
title: Accessible API Design for Developers
sidebar_position: 1
hide_title: true
level: intermediate
type: api-doc
status: draft
visibility: public
topics:
  - developer
  - api
  - accessibility  
  - tool:NVDA
  - tool:JAWS
  - tool:VoiceOver
author: ["Alexandra Arguello Saenz (https://github.com/alexarguello)"]
eta: 2025-12-31
---

# Accessible API Design for Developers

Accessibility in software is often associated with user interfaces, but it is equally important in API and schema design. Accessible APIs improve usability for developers using assistive technologies, enhance code readability, and support better tooling integration. This guide outlines key strategies Java developers can adopt to make their APIs more inclusive.

---

## Quick Start

If you only have 10 minutes, do this:
- Use clear, pronounceable identifiers. See: [1. Use Clear Word Separators](#1-use-clear-word-separators)
- Avoid abbreviations that confuse AT. See: [2. Avoid Abbreviations](#2-avoid-abbreviations)
- Prefer structured content over HTML blobs. See: [8. Deliver Structured Content, Not HTML Blobs](#8-deliver-structured-content-not-html-blobs)
- Include media accessibility metadata. See: [10. Provide Metadata for Media](#10-provide-metadata-for-media)
- Make docs accessible and include examples. See: [11. Make API Documentation Accessible](#11-make-api-documentation-accessible)
- Add CI checks for required accessibility fields. See: [13. Integrate Accessibility Testing into CI/CD](#13-integrate-accessibility-testing-into-cicd)

---

## Quick Links

- Design principles
  - [1. Use Clear Word Separators](#1-use-clear-word-separators)
  - [2. Avoid Abbreviations](#2-avoid-abbreviations)
  - [3. Design for Readability in Identifiers](#3-design-for-readability-in-identifiers)
  - [4. Document Clearly and Consistently](#4-document-clearly-and-consistently)
  - [5. Consider Tooling Compatibility](#5-consider-tooling-compatibility)
  - [6. Test with Assistive Technologies](#6-test-with-assistive-technologies)
- Implementation patterns
  - [7. Embed Accessibility at the Source](#7-embed-accessibility-at-the-source)
  - [8. Deliver Structured Content, Not HTML Blobs](#8-deliver-structured-content-not-html-blobs)
  - [9. Provide Structural Metadata to Support ARIA in UIs](#9-provide-structural-metadata-to-support-aria-in-uis)
  - [10. Provide Metadata for Media](#10-provide-metadata-for-media)
- Docs, errors, and communication
  - [11. Make API Documentation Accessible](#11-make-api-documentation-accessible)
  - [12. Improve Error Handling for Accessibility](#12-improve-error-handling-for-accessibility)
- Automation and contracts
  - [13. Integrate Accessibility Testing into CI/CD](#13-integrate-accessibility-testing-into-cicd)
  - [14. Use Contract Testing for Accessibility](#14-use-contract-testing-for-accessibility)
- Quality and fallbacks
  - [15. Perform Manual Quality Checks](#15-perform-manual-quality-checks)
  - [16. Plan for Graceful Degradation](#16-plan-for-graceful-degradation)
- Collaboration
  - [17. Foster Cross-Team Collaboration](#17-foster-cross-team-collaboration)
- Reference
  - [Further Reading](#further-reading)

---

## 1. Use Clear Word Separators

Screen readers rely on word boundaries to interpret identifiers. Without separators, compound words become opaque and hard to parse. Clear separators also improve parsing by code generators and linters.

Why this matters (refs): RFC 3986 recommends readable, hierarchical URIs; clear tokens aid comprehension and tooling. UUID format is defined in RFC 4122.
- RFC 3986 (URIs): https://www.rfc-editor.org/rfc/rfc3986
- RFC 4122 (UUIDs): https://www.rfc-editor.org/rfc/rfc4122

### Recommended Naming Conventions:
- `data_base64`
- `dataContentType`
- `data-content-type`
- `com.example.api`
- `/api/v1/resource`
- `123e4567-e89b-12d3-a456-426614174000`

### Avoid:
- `datacontenttype`

## 2. Avoid Abbreviations

Abbreviations can confuse screen readers and increase cognitive load for users. Prefer full words or expand on first use. When abbreviations are necessary, provide an expansion in documentation.

Why this matters (ref): WCAG 2.2 Success Criterion 3.1.4 (Abbreviations) recommends providing expansions or definitions for abbreviations.
- WCAG 2.2 Quick Ref: https://www.w3.org/WAI/WCAG22/quickref/#abbreviations

### Use Full Words:
- `privateKey`
- `accessToken`
- `userProfile`

### Avoid:
- `pvtKey`
- `accTkn`
- `usrProf`

## 3. Design for Readability in Identifiers

Some characters are visually ambiguous and can be misinterpreted by humans and machines alike.

### Watch out for:
- `O` vs `0`
- `1` vs `l` vs `I`

Avoid using these characters in isolation or in critical identifiers like URIs, keys, or codes.

## 4. Document Clearly and Consistently

Accessible APIs are well-documented. Ensure:
- Descriptions are complete and avoid jargon.
- Examples use accessible naming.
- Error messages are descriptive and avoid cryptic codes.

Use tools like Swagger/OpenAPI with annotations that support accessibility, such as `@Schema(description = "...")` in Springdoc.

## 5. Consider Tooling Compatibility

Accessible naming conventions improve compatibility with:
- Code generators
- Static analysis tools
- Documentation generators
- Assistive technologies

For example, using `dataContentType` allows Java tools to generate `getDataContentType()` methods, which are easier to read and use.

## 6. Test with Assistive Technologies

Use screen readers like NVDA, JAWS, or VoiceOver to test how your API documentation and schema are interpreted. This helps identify issues that may not be obvious during development.

Official resources:
- NVDA: https://www.nvaccess.org/
- JAWS (Freedom Scientific): https://www.freedomscientific.com/products/software/jaws/
- VoiceOver (Apple): https://support.apple.com/guide/voiceover/welcome/mac

---

## 7. Embed Accessibility at the Source

Accessibility should be part of the data model, not just the front-end. Provide text alternatives and descriptive fields where media or complex UI will be rendered.

Why this matters (ref): WCAG 2.2 Success Criterion 1.1.1 (Non-text Content) requires text alternatives for non-text content (e.g., images).
- WCAG 2.2 Quick Ref — 1.1.1: https://www.w3.org/WAI/WCAG22/quickref/#non-text-content

### Example:
```json
{
  "imageUrl": "https://example.com/image.jpg",
  "altText": "A person using a wheelchair entering a building"
}
```
---

## 8. Deliver Structured Content, Not HTML Blobs

Avoid sending pre-formatted HTML in API responses. Use structured JSON to describe content hierarchy. This preserves information and relationships so UIs can render them accessibly.

Why this matters (refs):
- WCAG 2.2 — 1.3.1 Info and Relationships: https://www.w3.org/WAI/WCAG22/quickref/#info-and-relationships
- JSON Schema (describe structure/constraints): https://json-schema.org/
- OpenAPI Specification (document your API): https://spec.openapis.org/oas/latest.html

### Example:
```json
{
  "content": [
    { "type": "heading", "level": 2, "text": "Our Mission" },
    { "type": "paragraph", "text": "We aim to do great things." }
  ]
}
```

---

## 9. Provide Structural Metadata to Support ARIA in UIs

For interactive components like tabs or accordions, provide structural metadata that allows UI layers to apply appropriate ARIA roles and attributes.

Why this matters (refs):
- WAI-ARIA 1.2 (roles, states, properties): https://www.w3.org/TR/wai-aria-1.2/
- ARIA Authoring Practices Guide (APG) patterns: https://www.w3.org/WAI/ARIA/apg/

### Example:
```json
{
  "tabs": [
    {
      "id": "tab1",
      "label": "Overview",
      "panelId": "panel1",
      "isSelected": true
    }
  ]
}
```

---

## 10. Provide Metadata for Media

Ensure media resources include accessibility metadata such as captions, transcripts, audio descriptions, and descriptions for images.

Why this matters (refs):
- WCAG 2.2 — 1.2.2 Captions (Prerecorded): https://www.w3.org/WAI/WCAG22/quickref/#captions-prerecorded
- WCAG 2.2 — 1.2.3 Audio Description or Media Alternative: https://www.w3.org/WAI/WCAG22/quickref/#audio-description-or-media-alternative-prerecorded
- WebVTT (W3C): https://www.w3.org/TR/webvtt/

### Example:
```json
{
  "featuredVideo": {
    "videoUrl": "https://example.com/video.mp4",
    "captionFileUrl": "https://example.com/captions.vtt",
    "transcriptUrl": "https://example.com/transcript.txt",
    "description": "Demo of our product features."
  }
}
```

---

## 11. Make API Documentation Accessible

### Best Practices:
- Use semantic HTML with proper heading structure.
- Ensure keyboard navigation and color contrast.
- Include accessible examples and explain accessibility-specific fields.
- Create a dedicated Accessibility section in your API docs.

References:
- WCAG 2.2 Overview/Quick Ref: https://www.w3.org/WAI/WCAG22/quickref/
- WAI: Planning and Managing Accessibility: https://www.w3.org/WAI/planning-and-managing/

---

## 12. Improve Error Handling for Accessibility

Error messages should be structured, human-readable, and helpful. Prefer standardized formats like Problem Details for HTTP APIs (RFC 7807) so tools and assistive technologies can present consistent information.

Reference:
- RFC 7807 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc7807

### Example:
```json
{
  "type": "https://example.com/problems/user-already-exists",
  "title": "User already exists",
  "status": 409,
  "detail": "This email address is already registered. Please try logging in or use a different email address.",
  "instance": "/signup/requests/12345",
  "errors": [
    { "field": "emailAddress", "message": "Email is already registered" }
  ]
}
```

---

## 13. Integrate Accessibility Testing into CI/CD

Automate checks for accessibility-related fields and formats using API and schema testing tools.

Ideas and tools:
- Spectral (OpenAPI linting): https://meta.stoplight.io/docs/spectral/
- Schemathesis (property-based testing for APIs): https://schemathesis.readthedocs.io/
- OpenAPI Validator (OpenAPI Initiative): https://www.openapis.org/resources/tools

### Checklist:
- Validate presence of `altText`, `captionFileUrl`, `transcriptUrl`
- Ensure structured content format (e.g., JSON Schema validation)
- Confirm clarity of error messages (e.g., RFC 7807 Problem Details)

---

## 14. Use Contract Testing for Accessibility

Contract testing ensures that the interaction between a consumer (e.g., a frontend app) and a provider (e.g., an API) adheres to a shared agreement, or contract. This is especially useful in microservices architectures and can be extended to include accessibility metadata in API responses.

By defining accessibility-related fields (like altText, captionFileUrl, transcriptUrl, etc.) in your contract, you ensure that both the backend and frontend teams are aligned on what accessibility data must be present and how it should be structured

Use tools like Pact or Spring Cloud Contract to validate presence and format of accessibility metadata.
###  Spring Cloud Contract
   Spring Cloud Contract is a powerful tool for JVM-based applications that supports Consumer-Driven Contracts (CDC). It allows you to define contracts in Groovy or YAML and automatically generates tests for both producers and consumers.

- Spring Cloud Contract Overview - https://spring.io/projects/spring-cloud-contract
- Baeldung Tutorial on Spring Cloud Contract - https://www.baeldung.com/spring-cloud-contract
- Official Documentation - https://docs.spring.io/spring-cloud-contract/docs/current/reference/html/using.html
###  Pact
   Pact is a language-agnostic contract testing tool that supports HTTP and message-based interactions. It’s widely used in microservices environments and supports multiple languages including Java, JavaScript, and Python.

- Pact Documentation - https://docs.pact.io/
- Baeldung Guide to Pact2 - https://www.baeldung.com/pact-junit-consumer-driven-contracts

#### Example: Pact (Java, HTTP)
A consumer test can assert that accessibility fields are present and correctly typed.

```java
@Pact(consumer = "webapp")
public RequestResponsePact getImage(PactDslWithProvider builder) {
  return builder
    .given("image exists with accessibility metadata")
    .uponReceiving("get image metadata")
      .path("/api/images/42")
      .method("GET")
    .willRespondWith()
      .status(200)
      .headers(Map.of("Content-Type", "application/json"))
      .body(newJsonBody(o -> {
        o.stringType("imageUrl", "https://example.com/image.jpg");
        o.stringMatcher("altText", ".+", "A person using a wheelchair entering a building");
        o.stringType("captionFileUrl", "https://example.com/captions.vtt");
        o.stringType("transcriptUrl", "https://example.com/transcript.txt");
      }).build())
    .toPact();
}
```

#### Example: Spring Cloud Contract (Groovy DSL)
Producer-side contract requiring accessibility fields in the response.

```groovy
org.springframework.cloud.contract.spec.Contract.make {
  description "Get video with captions and transcript"
  request {
    method GET()
    url "/api/videos/123"
  }
  response {
    status OK()
    headers { contentType(applicationJson()) }
    body(
      featuredVideo: [
        videoUrl: 'https://example.com/video.mp4',
        captionFileUrl: 'https://example.com/captions.vtt',
        transcriptUrl: 'https://example.com/transcript.txt',
        description: 'Demo of our product features.'
      ]
    )
    bodyMatchers {
      jsonPath('$.featuredVideo.captionFileUrl', byRegex('.+\\.vtt'))
      jsonPath('$.featuredVideo.transcriptUrl', byRegex('.+'))
      jsonPath('$.featuredVideo.description', byRegex('.+'))
    }
  }
}
```

---

## 15. Perform Manual Quality Checks

Automated checks confirm presence, not quality. Establish a lightweight review process so humans validate that accessibility data is accurate, complete, and useful.

### What to review
- Alt text (images/icons): Is it accurate, concise, and non-redundant? Avoid “image of…”. Don’t describe purely decorative images; use empty alt instead.
- Captions and transcripts (audio/video): Are captions synchronized and accurate? Do transcripts include speaker changes and important non-speech info? Provide audio description or a media alternative when needed.
- Labels, help text, and headings: Are field/parameter names and descriptions clear, unambiguous, and consistent? Do headings communicate structure?
- Error copy: Is guidance actionable and free of jargon? Does it identify the field and the fix?

### Quick checklist
- Images have meaningful `altText` or are explicitly marked decorative. (WCAG 2.2 — 1.1.1)
- Time-based media include captions and a transcript; audio description or equivalent is available where required. (WCAG 2.2 — 1.2.x)
- Headings/sections in docs follow a logical outline. (WCAG 2.2 — 2.4.6)
- Form fields and parameters have clear labels or instructions. (WCAG 2.2 — 3.3.2)

### Helpful references (authoritative)
- WCAG 2.2 — 1.1.1 Non-text Content: https://www.w3.org/WAI/WCAG22/quickref/#non-text-content
- WAI Images Tutorial: https://www.w3.org/WAI/tutorials/images/
- WAI Alt Text Decision Tree: https://www.w3.org/WAI/tutorials/images/decision-tree/
- WCAG 2.2 — 1.2.2 Captions (Prerecorded): https://www.w3.org/WAI/WCAG22/quickref/#captions-prerecorded
- WCAG 2.2 — 1.2.3 Audio Description or Media Alternative: https://www.w3.org/WAI/WCAG22/quickref/#audio-description-or-media-alternative-prerecorded
- WCAG 2.2 — 2.4.6 Headings and Labels: https://www.w3.org/WAI/WCAG22/quickref/#headings-and-labels
- WCAG 2.2 — 3.3.2 Labels or Instructions: https://www.w3.org/WAI/WCAG22/quickref/#labels-or-instructions
- Plain language guidance (US): https://www.plainlanguage.gov/guidelines/

---

## 16. Plan for Graceful Degradation

If required accessibility data is missing or a consumer cannot support a rich experience, degrade gracefully so users aren’t blocked.

### API strategies
- Provide explicit nullability and semantics: Distinguish missing vs. decorative (e.g., `altText: null` vs `altText: ""` with `isDecorative: true`). Document expectations in OpenAPI.
- Prefer omission over broken experiences: If a video lacks captions/transcript, supply a transcript placeholder and set a flag `isAccessible:false`, or omit the video and return a clear Problem Details error explaining the deficiency (RFC 7807).
- Content negotiation: Offer text-only or simplified variants (e.g., `Accept: application/vnd.example.article+json; profile=text-only`).
- Defaults for structure: When structural metadata is absent, return plain, semantic content instead of ARIA-dependent structures.
- Log and monitor: Emit structured logs/metrics when accessibility contracts are not met to prompt remediation.

### Consumer (frontend) strategies
- Images: Use `alt=""` for decorative images; don’t invent misleading alt text. If a critical image has no alt, replace with an equivalent text message or link to description instead of showing an inaccessible element.
- Media: If captions/transcript are missing, do not autoplay; provide transcript link or disable playback behind an explanation.
- Widgets: If required roles/relationships are missing, render a native, semantic fallback rather than a broken custom control. Remember: “No ARIA is better than bad ARIA.”

### References (authoritative)
- WCAG 2.2 — 1.1.1 Non-text Content: https://www.w3.org/WAI/WCAG22/quickref/#non-text-content
- WCAG 2.2 — 1.2.x Time-based Media: https://www.w3.org/WAI/WCAG22/quickref/#time-based-media
- HTML Standard — img alt attribute: https://html.spec.whatwg.org/multipage/images.html#alt
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WAI — “No ARIA is better than bad ARIA”: https://www.w3.org/TR/using-aria/#no_aria_better_bad_aria
- RFC 7807 — Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc7807

---

## 17. Foster Cross-Team Collaboration

Accessibility succeeds when product, design, engineering, QA, and docs share a contract and workflow.

### Practical actions
- Define responsibilities: Use W3C’s Accessibility Roles and Responsibilities Mapping (ARRM) to assign who writes alt text, who validates captions, who owns schema fields, etc.
- Definition of Done: Add concrete a11y acceptance criteria (e.g., caption files present for all new videos; alt text reviewed; error messages follow RFC 7807) to stories and PR templates.
- Shared artifacts: Keep an “Accessibility” section in the API spec (OpenAPI) and in product docs describing required fields, examples, and contracts.
- Joint rituals: Run design reviews and contract testing sessions with both frontend and backend to verify accessibility metadata.
- Training/enablement: Provide periodic training on WCAG and AT usage for engineers, PMs, and tech writers.

### References (authoritative)
- W3C — Accessibility Roles and Responsibilities Mapping (ARRM): https://www.w3.org/WAI/roles/
- WAI — Planning and Managing Accessibility: https://www.w3.org/WAI/planning-and-managing/
- WAI — Curricula on Web Accessibility: https://www.w3.org/WAI/curricula/
- W3C — ACT Rules (testing methodology): https://www.w3.org/WAI/standards-guidelines/act/
- WCAG 2.2 Quick Ref: https://www.w3.org/WAI/WCAG22/quickref/
- The A11Y Project Checklist: https://www.a11yproject.com/checklist/

---

## Further Reading
- See External Resources for Developers: [external-resources](./external-resources.md)

