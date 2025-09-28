# Accessibility Plan: AI & Empowerment

This master plan drives our **community-driven hub** for AI & digital solutions in accessibility. We’ll split this file into per-topic resources under `docs/accessibility/`, complete with front-matter and flatmaps.

## Table of Contents
- [Overview](#accessibility-hub-overview) *(-> overview.md)*
- [About](#about) *(-> about.md)*
- [For Users](#for-users) *(-> for-users/)*
  - [By Disability Type](#by-disability-type)  *(-> for-users/types/)*
    - [Vision](#vision) *(-> for-users/types/vision.md)*
      - [Screen readers](#screen-readers) *(-> for-users/types/vision/screen-readers.md)*
      - [Accessible e-readers](#accessible-e-readers) *(-> for-users/types/vision/e-readers.md)*
      - [External Resources](#external-resources) *(-> for-users/types/vision/external-resources.md)*
    - [Hearing](#hearing) *(-> for-users/types/hearing.md)*
      - [External Resources](#external-resources-1) *(-> for-users/types/hearing/external-resources.md)*
    - [Cognitive](#cognitive) *(-> for-users/types/cognitive.md)*
      - [External Resources](#external-resources-2) *(-> for-users/types/cognitive/external-resources.md)*
    - [Mobility](#mobility) *(-> for-users/types/mobility.md)*
      - [External Resources](#external-resources-3) *(-> for-users/types/mobility/external-resources.md)*
    - [Speech & Language](#speech--language) *(-> for-users/types/speech-language.md)*
      - [External Resources](#external-resources-4) *(-> for-users/types/speech-language/external-resources.md)*
    - [Neurodiversity](#neurodiversity) *(-> for-users/types/neurodiversity.md)*
      - [External Resources](#external-resources-5) *(-> for-users/types/neurodiversity/external-resources.md)*
    - [Aging & Dexterity](#aging--dexterity) *(-> for-users/types/aging-dexterity.md)*
      - [External Resources](#external-resources-6) *(-> for-users/types/aging-dexterity/external-resources.md)*
- [For Developers](#for-developers) *(-> for-developers/)*
  - [Accessibility APIs & SDKs](#developer-resources) *(-> for-developers/apis-sdks.md)*
  - [Open Issues & Gaps](#engineering-gaps--design-patterns) *(-> for-developers/engineering-gaps.md)*
  - [Contribution Guidelines](#community-contributions) *(-> for-developers/contribution-guidelines.md)*
  - [Case Studies](#case-studies) *(-> for-developers/case-studies.md)*
- [Community](#community-hub) *(-> community/)*
  - [Forums or Discussions](#forums-or-discussions) *(-> community/forums.md)*
  - [Events & Hackathons](#events--hackathons) *(-> community/events.md)*
  - [Success Stories](#success-stories) *(-> community/success-stories.md)*
- [Resources](#resources) *(-> resources/)*
  - [Accessibility Standards](#legal--standards-overview) *(-> resources/legal-standards.md)*
  - [Tutorials & Courses](#tutorials--courses) *(-> resources/tutorials.md)*
  - [Research & Whitepapers](#research--whitepapers) *(-> resources/research.md)*
- [Applications](#applications) *(-> applications/)*
  - [For visual](#for-visual) *(-> applications/for-visual.md)*
  - [Open Source](#open-source) *(-> applications/open-source.md)*
- [Use Cases](#use-cases)  *(-> use-cases/)*
  - [Work-Related Use Cases](#work-related-use-cases) *(-> use-cases/work.md)*
  - [Home and Daily Life Scenarios](#home-and-daily-life-scenarios) *(-> use-cases/home.md)*
  - [Hypothetical/Future Scenarios](#hypotheticalfuture-scenarios) *(-> use-cases/future.md)*
- [Unmet Needs & Future Possibilities](#unmet-needs--future-possibilities)*(-> unmet-needs/)*
- [AI Solution Categories table](#ai-solution-categories-table) *(-> `ai-solution-categories.md)*
- [Tool Directory](#tool-directory) *(-> tool-directory.md`)*
- [Engineering Gaps & Design Patterns](#engineering-gaps--design-patterns) *(-> `engineering-gaps.md)*
- [User Personas](#user-personas) *(-> personas.md`)*
  - [Blind Developer](#blind-developer)
  - [Scientist - Educator (Low Vision)](#scientist---educator-low-vision)
- [Community Contributions](#community-contributions) *(-> community.md)*
  - [What’s Missing?](#whats-missing)
  - [Getting Started](#getting-started)
  - [Testimony Interview Template](#testimony-interview-template) 
- [Roadmap](#roadmap) *(-> roadmap.md)*
- [To-Do List](#to-do-list) *(-> to-do-list.md)*
- [Full Sitemap](#full-sitemap) *(-> sitemap.md)*

---
## Project File Structure
📂 Project Root
├── 1.01-overview.md
├── 2.01-about.md
├── 📂 3.01-for-users
│   ├── 📂 1.01-by-disability-type
│   │   ├── 1.01-vision.md
│   │   ├── 📂 1.01-vision
│   │   │   ├── 1.01-screen-readers.md
│   │   │   ├── 1.02-e-readers.md
│   │   │   ├── 1.03-external-resources.md
│   │   ├── 1.02-hearing.md
│   │   ├── 📂 1.02-hearing
│   │   │   └── 1.01-external-resources.md
│   │   ├── 1.03-cognitive.md
│   │   ├── 📂 1.03-cognitive
│   │   │   └── 1.01-external-resources.md
│   │   ├── 1.04-mobility.md
│   │   ├── 📂 1.04-mobility
│   │   │   └── 1.01-external-resources.md
│   │   ├── 1.05-speech-language.md
│   │   ├── 📂 1.05-speech-language
│   │   │   └── 1.01-external-resources.md
│   │   ├── 1.06-neurodiversity.md
│   │   ├── 📂 1.06-neurodiversity
│   │   │   └── 1.01-external-resources.md
│   │   ├── 1.07-aging-dexterity.md
│   │   ├── 📂 1.07-aging-dexterity
│   │   │   └── 1.01-external-resources.md
├── 📂 4.01-for-developers
│   ├── 1.01-apis-sdks.md
│   ├── 1.02-engineering-gaps.md
│   ├── 1.03-contribution-guidelines.md
│   ├── 1.04-case-studies.md
├── 📂 5.01-community
│   ├── 1.01-forums.md
│   ├── 1.02-events.md
│   ├── 1.03-success-stories.md
├── 📂 6.01-resources
│   ├── 1.01-legal-standards.md
│   ├── 1.02-tutorials.md
│   ├── 1.03-research.md
├── 📂 7.01-applications
│   ├── 1.01-for-visual.md
│   ├── 1.02-open-source.md
├── 📂 8.01-use-cases
│   ├── 1.01-work.md
│   ├── 1.02-home.md
│   ├── 1.03-future.md
├── 📂 9.01-unmet-needs
│   └── 1.01-unmet-needs.md
├── 10.01-ai-solution-categories.md
├── 11.01-tool-directory.md
├── 12.01-engineering-gaps.md
├── 13.01-personas
├── 📂 14.01-community-contributions
│   ├── 1.01-whats-missing.md
│   ├── 1.02-getting-started.md
│   ├── 1.03-testimony-template.md
├── 15.01-roadmap.md
├── 16.01-to-do-list.md
└── 17.01-sitemap.md

---
## ♿ Accessibility HUB Overview

An open-source, AI-powered platform designed to centralize accessibility tools, identify gaps, and foster collaboration between people with disabilities and developers building inclusive technology.

### 🌟 Purpose

Accessibility HUB serves two core audiences:

- **Visually impaired professionals and individuals with disabilities**  
  To discover tools that support independent reading, content creation, and daily task management.

- **Software developers and creators**  
  To explore accessibility gaps, find inspiration, and build inclusive, legally compliant applications.

### 🎯 Mission

To bridge the gap between accessibility needs and inclusive technology by mapping existing tools, identifying unmet needs, and fostering collaboration between users and developers.

### 🧩 Key Features

- **Interactive Site Map**  
  Auto-generated using Flatmap Docs Kit, providing a visual overview of tools, resources, and opportunities.

- **Tool Directory**  
  Categorized listings of accessibility tools, filterable by disability type, function, and platform.

- **Gap Identification**  
  Highlighting areas where tools are lacking, based on user feedback and research.

- **Developer Resources**  
  - Accessibility APIs, SDKs, and libraries  
  - Tutorials and best practices  
  - Legal standards (WCAG, EAA, etc.)  
  - Open issues and contribution opportunities

- **User Resources**  
  - Guides for using assistive tools  
  - Community reviews and ratings  
  - Success stories and testimonials

- **Community Hub**  
  A space for users and developers to connect, share ideas, and collaborate on accessibility-focused projects.

- **Future Vision**  
  Includes the development of a **smart reader for visually impaired scientists**, inspired by the founder’s sister.
---
## About *(-> about.md)*

A brief introduction to the Accessibility HUB, its history, and the founder’s motivation.  
**Mission:** To empower people with disabilities and developers to co-create accessible digital solutions.  
**Vision:** A world where technology is barrier-free for everyone.

---

## For Users *(-> for-users.md)*

Guides, reviews, and resources for people with disabilities to discover, use, and rate accessibility tools.  
- **How to Use This Hub:** Step-by-step instructions for navigating the site, filtering tools, and submitting feedback.  
- **Success Stories:** Real-world examples of users who have benefited from accessible technology.

---


## By Disability Type *(-> `types/`)*

### Vision *(-> `types/vision.md`)*

### Vision

#### Screen readers  
Access text content. JAWS is the most feature-rich but expensive; NVDA is free and highly capable; VoiceOver and Narrator are good built-in options. The future is in AI-driven context, smarter navigation, and making these tools more affordable and intuitive.

##### JAWS (Job Access With Speech)
- Overview: Commercial Windows screen reader by Freedom Scientific.
- Features:
  - Reads text aloud from applications, web pages, and documents.
  - Braille display support.
  - Powerful scripting for custom app accessibility.
  - OCR for reading images and scanned PDFs.
  - Advanced navigation for tables, forms, and complex web content.
- Price: ~$95/year (home license), or ~$1,000 for a perpetual license. Discounts for students/educators.
- How Users Use It: Keyboard shortcuts to navigate, read, and interact with all elements on screen. Used for work, study, and daily computing.
- Gaps/Future Needs:
  - High cost is a barrier.
  - Steep learning curve for beginners.
  - Needs better AI-driven context awareness (e.g., summarizing complex layouts, describing images in detail). cost barrier, steep learning curve, AI context awareness.

##### NVDA (NonVisual Desktop Access)
- Overview: Free, open-source screen reader for Windows, developed by NV Access.
- Key Features:
  - Reads text from most Windows apps and browsers.
  - Braile display support.
  - Regular updates and strong community support.
  - Extensible via add-ons.
- Price: Free (donation-supported).
- How Users Use It: Similar to JAWS—keyboard navigation, customizable settings, and add-ons for extra features.
- Gaps/Future Needs:
  - Slightly less robust with complex enterprise apps (e.g., some Office features).
  - Lacks some advanced scripting/customization found in JAWS.
  - Could benefit from more AI-powered features (e.g., image description, smart navigation).
##### Other Tools (VoiceOver, Narrator, Orca)
- VoiceOver (macOS/iOS) : Built-in on Apple devices.
  - Features: Touch and gesture navigation, Braille support, reads everything on screen.
  - Price: Free with Apple devices.
  - Gaps: Less customizable than JAWS/NVDA, but highly usable for most tasks.
- Narrator (Windows) Built-in on Windows 10/11.
  - Features: Basic screen reading, improved in recent versions, supports Braille.
  - Price: Free.
  - Gaps: Still less powerful than JAWS/NVDA for advanced users.
- Orca (Linux)  Open-source for Linux desktops.
  - Features: Reads text, supports Braille, works with many Linux apps.
  - Price: Free.
  - Gaps: Varies in quality depending on Linux distribution and app support.

#### Accessible e-readers  
Users want better format support, richer navigation, improved image accessibility, reliable Braille integration, and more affordable devices. Here are common user complaints about accessible e-readers:
  - Limited Book Formats: Not all e-books are available in accessible formats (e.g., some DRM-protected or image-based PDFs are not readable).
  - Inconsistent Accessibility: Some e-reader apps or devices have incomplete screen reader or Braille support, especially for navigation, bookmarks, or highlighting.
  - Complex Navigation: Moving between chapters, footnotes, or searching text can be cumbersome with screen readers.
  - Poor Image/Graph Accessibility: Figures, charts, and images often lack alt text or descriptions, making them inaccessible.
  - Sync Issues: Notes, highlights, or reading position may not sync well across devices, especially with Braille displays.
  - Limited Braille Support: Some devices or apps do not support all Braille displays or advanced Braille features.
  - Voice Quality: Text-to-speech voices may sound robotic or be hard to understand for long reading sessions.
  - Cost: Specialized Braille e-readers and hardware are expensive and not widely available.
  - Regional Restrictions: Some accessible libraries (like Bookshare or NLS BARD) are only available in certain countries.


#### External Resources  

- [American Foundation for the Blind](https://www.afb.org/)
- [Bookshare](https://www.bookshare.org/)
- [NLS BARD](https://nlsbard.loc.gov/)
- [Apple Accessibility](https://www.apple.com/accessibility/)
*(-> types/vision/external-resources.md)*

---
### Companies committed to accessibility  
- **Freedom Scientific:**
A leading company that develops assistive technology products for people who are blind or visually impaired, best known for the JAWS screen reader.

- **NV Access:**
The non-profit organization behind NVDA (NonVisual Desktop Access), a free and open-source screen reader for Windows.

- **Apple:**
The technology company known for its commitment to accessibility, especially through built-in features like VoiceOver on macOS and iOS devices.

- **Microsoft**
Accessibility training
Accessibility summit

*(-> `types/vision/companies.md`)*
---

### Hearing

Intro: Hearing assistive tech includes captioning, assistive listening devices, cochlear implants, and AI-powered transcription.  
**Emerging trends:** Real-time AI captioning, automatic sign language translation, and personalized sound amplification.

*(-> `types/vision/companies.md`)*

#### External Resources  
- [National Association of the Deaf (NAD)](https://www.nad.org/)
- [Hearing Loss Association of America (HLAA)](https://www.hearingloss.org/)
- [Described and Captioned Media Program (DCMP)](https://dcmp.org/)
- [World Health Organization: Deafness and hearing loss](https://www.who.int/news-room/fact-sheets/detail/deafness-and-hearing-loss)
- [European Federation of Hard of Hearing People (EFHOH)](https://www.efhoh.org/)
- [FCC Accessibility](https://www.fcc.gov/accessibility)
*(-> `types/hearing/external-resources.md`)*
---

## Cognitive *(-> `types/cognitive.md`)*

Intro: Cognitive-accessibility tools include simplified user interfaces, memory aids, focus support, and text-to-speech tools.  
**AI applications:** Reading comprehension, reminders, distraction reduction, and adaptive learning environments.


#### External Resources  
- [Cognitive Accessibility Task Force (W3C)](https://www.w3.org/WAI/cognitive/)
- [CAST: Universal Design for Learning](https://www.cast.org/)
- [National Center for Learning Disabilities](https://www.ncld.org/)
- [Mencap (UK)](https://www.mencap.org.uk/)
*(-> `types/cognitive/external-resources.md`)*

---

### Mobility *(-> `types/mobility.md`)*

Intro to mobility assistive tech: Switch control, voice interfaces, adaptive keyboards, and robotics enable users with limited mobility to interact with computers and environments. AI can enhance voice recognition and environmental control.
**AI enhancements:** Voice recognition, gesture control, and smart home/environmental automation.

#### External Resources  
- [United Spinal Association](https://unitedspinal.org/)
- [Christopher & Dana Reeve Foundation](https://www.christopherreeve.org/)
- [AbilityNet](https://abilitynet.org.uk/)
- [Microsoft Accessibility: Mobility](https://www.microsoft.com/en-us/accessibility/)
*(-> `types/mobility/external-resources.md`)*

---

### Speech & Language *(-> `types/speech-language.md`)*

Intro to speech & language solutions: Speech recognition, Augmentative and Alternative Communication (AAC) devices, and voice generation tools support users with speech impairments. AI-driven voice synthesis and recognition are rapidly improving.
**AI trends:** Personalized voice synthesis, improved speech-to-text, and multilingual support.

#### External Resources  
- [American Speech-Language-Hearing Association](https://www.asha.org/)
- [Communication Disabilities Access Canada](https://www.cdacanada.com/)
- [AAC Institute](https://aacinstitute.org/)
- [Speech Accessibility Project (University of Illinois)](https://speechaccessibilityproject.beckman.illinois.edu/)
*(-> `types/speech-language/external-resources.md`)*

---

### Neurodiversity *(-> `types/neurodiversity.md`)*

Intro to autism, ADHD, dyslexia accommodations: Read-aloud tools, distraction reduction apps, and customizable learning environments support neurodiverse users. AI can personalize content and reduce cognitive load.
**AI role:** Personalized content, adaptive interfaces, and cognitive load reduction.

#### External Resources  
- [Autistic Self Advocacy Network](https://autisticadvocacy.org/)
- [ADHD Foundation](https://www.adhdfoundation.org.uk/)
- [British Dyslexia Association](https://www.bdadyslexia.org.uk/)
- [Understood.org](https://www.understood.org/)
*(-> `types/neurodiversity/external-resources.md`)*

---

### Aging & Dexterity *(-> `types/aging-dexterity.md`)*

Intro to tools for low-vision senior users and fine-motor support: Large controls, haptic feedback, voice assistants, and simplified interfaces help older adults and those with dexterity challenges. AI can adapt interfaces to user needs.
**AI potential:** Interface adaptation, fall detection, and health monitoring.

#### External Resources  
- [AARP: Technology and Aging](https://www.aarp.org/home-family/personal-technology/)
- [National Institute on Aging](https://www.nia.nih.gov/)
- [Eldercare Locator](https://eldercare.acl.gov/)
- [AbilityNet: Older People](https://abilitynet.org.uk/at-home/older-people)
*(-> `types/aging-dexterity/external-resources.md`)*

---

## Applications 
### For visual

- **Be My Eyes**: AI-powered visual assistance.  
- **Seeing AI**: OCR, scene recognition, text reading. Microsoft app for reading text, recognizing people/objects/environments. 
- **Microsoft Copilot**: Automates content creation (e.g., presentations from Word docs). 
- **Markdown Editors**: Tools that allow you to write and format text using Markdown. Examples: Typora, Visual Studio Code, and Dillinger. Markdown is popular for creating accessible, structured content 

 ### **Open Source**
- **Bookshare:**
An accessible online library for people with print disabilities, offering books in formats compatible with screen readers and Braille devices.

- **NLS BARD:**
The Braille and Audio Reading Download service from the U.S. National Library Service, providing free access to Braille and audio books for eligible users.

- **AppleVis:**
A community-driven website offering resources, app reviews, and forums for blind and low-vision users of Apple products.

- **Medium:**
While not open source, Medium is included here as a widely used platform for sharing open content, including accessibility resources.


*(These will become `applications.md`)*

---

## Use Cases

### Work-Related Use Cases

#### Preparing Presentations Independently
- **Challenge**: Creating/formatting slides required days and visual help.
- **Solution**: Write script in Word, use Copilot in PowerPoint to generate slides.
- **Prompts**:  
  - “Create a presentation with 50 slides based on this document.”  
  - “Illustrate with graphs and use a cartoon style.”
- **Outcome**: Fully accessible, formatted slides with notes, tables, visuals—no external help needed.



### Home and Daily Life Scenarios

#### Image Recognition with AI
- **Example**: Take a picture of the kitchen, ask “What’s in this image?” or “What brand is the oven?” (AI: “It’s a SAMSUNG oven.”)
- **Tool**: Be My Eyes AI

#### Reading Labels and Receipts
- **Prompts**:  
  - “Can you read this prescription for me?”  
  - “Can you tell me the value on this receipt?”
- **Tool**: Be My Eyes

#### Reading Printed Text
- **Tool**: Seeing AI
- **Action**: Point phone at document, AI guides framing and reads aloud.

#### Indoor Navigation
- **Use case**: Navigate hotels, restaurants, elevators using phone camera and AI.
- **Prompts**:  
  - “Where is the restaurant from here?”  
  - “Which way to the elevator?”
- **Tool**: Be My Eyes + Hilton integration

#### Hypothetical/Future Scenarios
- **Cooking Guidance**:  
  - “What ingredients are on the table?”  
  - “I want to make pasta—what’s next?”  
  - Conversational, real-time guidance as a personal tutor.

- **Outfit Matching**:  
  - “Can I wear this T-shirt with these pants and these shoes?”  
  - AI gives fashion feedback or suggestions.

*(These will split into `use-cases/work.md`, `use-cases/home.md`, `use-cases/future.md`)*

---

## Unmet Needs & Future Possibilities

- **Advanced reading workflows** for scientists (skimming, referencing, jumping between sections). Currently, OCR and screen readers are limited to reading text in graphs. True accessibility for statistical graphs requires authors to include descriptive text and, ideally, provide underlying data in accessible formats. AI solutions for automatic graph interpretation are in early stages and not yet reliable for critical scientific content.
- **AI for daily tasks**: Cooking, matching outfits, organizing spaces.
- **Assistive GPS/navigation** for indoor environments (hotels, offices).
- **Better video content description**: AI describes visual cues (“click here”, “go there”).
- **Social support and peer connection** for people newly experiencing disability.
- **Creating Accessible Training Content** :
  - Co-developed materials for people with disabilities to learn:
    - Accessibility features in Windows, Word, Excel, etc.
    - Using Copilot tailored for different disabilities (visual, hearing, cognitive).
  - **Goal**: Empower users to increase productivity through adaptive AI.

*(-> `unmet-needs-future-possibilities.md`)*

---

## AI Solution Categories table

| Category                | Tool                | Function                                      |
|-------------------------|---------------------|-----------------------------------------------|
| Content Creation        | Microsoft Copilot   | Automate slide & doc creation                 |
| Accessibility Training  | Internal MS tools   | Teach Copilot & Office to users with disabilities |
| Academic Reading Support| ChatGPT / Copilot   | Assist comprehension & referencing            |
| Print Text Reader       | Seeing AI           | Read physical text & signs                    |
| Cooking Assistant (Fut.)| Vision AI           | Step-by-step kitchen guidance                 |
| Outfit Advisor (Fut.)   | Vision AI           | Clothing matching                             |
| Indoor Navigation       | Be My Eyes + GPS    | Wayfinding in buildings                       |
| Label Recognition       | Be My Eyes AI       | Read labels & identify items                  |

*(-> `ai-solution-categories.md`)*

---

## Tool Directory

| Tool              | Type             | Tags                         | Link                                        |
|-------------------|------------------|------------------------------|---------------------------------------------|
| NVDA              | Screen Reader    | vision, open-source          | https://www.nvaccess.org                    |
| Seeing AI         | AI App           | vision, mobile               | https://www.microsoft.com/seeing-ai         |
| Bookshare         | Library          | reading, braille             | https://www.bookshare.org                   |
| Be My Eyes        | Assistance App   | vision, real-time            | https://www.bemyeyes.com                    |
| Microsoft Copilot | Content Creation | productivity, ai             | https://aka.ms/microsoft365copilot          |

*(-> `tool-directory.md`)*

---

## Engineering Gaps & Design Patterns

| Challenge                               | Opportunity                            | Suggested Tech         |
|-----------------------------------------|----------------------------------------|------------------------|
| Blind navigation in complex layouts     | AI-powered layout summarization        | NLP + DOM parsing      |
| Inaccessible graphs in research papers  | Auto-generate alt text + data summary  | Vision API + LLMs      |
| Lack of indoor wayfinding               | AI + building maps + BLE beacons       | ARKit + Be My Eyes API |
| Format conversion (DRM/PDF→EPUB)        | Universal converter toolkit            | Open-source libs       |

*(-> `engineering-gaps.md`)*

---

## User Personas

### Blind Developer  
Needs efficient screen-reader workflows, accessible IDE; uses NVDA, Copilot, Seeing AI.

### Scientist - Educator (Low Vision)  
Needs large-print, voice-control; uses Word+Copilot, Bookshare.

*(-> `personas.md`)*

---

## Community Hub *(-> community.md)*

A space for users and developers to connect, share ideas, and collaborate on accessibility-focused projects.

### Forums or Discussions *(-> community/forums.md)*
Open forums for sharing experiences, troubleshooting, and networking.

### Events & Hackathons *(-> community/events.md)*
Calendar of upcoming accessibility events, hackathons, and webinars.

### Success Stories *(-> community/success-stories.md)*
Real-world examples of accessibility breakthroughs and user impact.

---

## Community Contributions *(-> community-contributions/)*

### What’s Missing? *(-> community-contributions/whats-missing.md)*
Help us grow! Reviews, benchmarks, tutorials, case studies, open-source tests.

### Getting Started *(-> community-contributions/getting-started.md)*
1. Fork & clone.
2. Copy `docs/.template.md` into your folder.
3. Rename & fill front-matter.
4. PR!


### Testimony Interview Template
To include real user stories, use this template when interviewing disabled people or collaborators:

**Accessibility Testimony Interview Template**
- Name (optional or pseudonym):
- Disability/Condition (optional):
- Country/Region:
- Tools/Technologies Used:
- Biggest Accessibility Challenge:
- Favorite Solution or Tool:
- What would you like to see improved?
- Any advice for others or for developers?
- (Optional) Would you like to be contacted for follow-up?

*(-> `community-contributions/interview-template.md`)*

---

## Legal & Standards Overview

Accessibility is governed by international and regional standards and laws. Key frameworks include:

- **WCAG (Web Content Accessibility Guidelines):** The global standard for web accessibility, developed by the W3C. [WCAG Overview](https://www.w3.org/WAI/standards-guidelines/wcag/)
- **ADA (Americans with Disabilities Act):** U.S. law prohibiting discrimination based on disability, including digital accessibility. [ADA Overview](https://www.ada.gov/)
- **Section 508 (U.S.):** Requires federal agencies to make electronic and information technology accessible. [Section 508](https://www.section508.gov/)
- **European Accessibility Act (EAA):** EU directive requiring products and services (including digital) to be accessible by 2025. [EAA Overview](https://ec.europa.eu/social/main.jsp?catId=1202)
- **EN 301 549:** European standard for ICT accessibility, referenced by the EAA. [EN 301 549](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/)

**How They Relate:**
- WCAG is the technical foundation for most laws and standards worldwide, including ADA, Section 508, and EN 301 549.
- ADA and Section 508 are U.S.-specific, while EAA and EN 301 549 apply in Europe.
- The EAA harmonizes accessibility requirements across EU member states, referencing EN 301 549 and WCAG.
- Compliance with these standards ensures digital products are accessible to people with disabilities and reduces legal risk.

**Localization & Multilingual Access:**  
Many standards require information to be accessible in multiple languages and formats. This hub aims to provide resources and guidance for global audiences.

**Further Reading:**  
- [W3C Accessibility Laws & Policies](https://www.w3.org/WAI/policies/)

*(-> `legal-standards.md`)*

---



## Roadmap

- [ ] Add tool reviews by disability.  
- [ ] Flatmaps per category.  
- [ ] Contributor dashboards.  
- [ ] Feedback integration.  
- [ ] Beginner tutorials.  

*(-> `roadmap.md`)*

---

## To-Do List

- [ ] Research AI accessibility tools.  
- [ ] user interviews.  
- [ ] Prototype smart-reader assistant.  
- [ ] Plan training content.  

*(-> `to-do-list.md`)*

---

## Full Sitemap *(-> sitemap.md)*

A machine-readable, auto-generated sitemap for the entire hub.
