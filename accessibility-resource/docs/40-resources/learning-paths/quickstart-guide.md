---
title: Quickstart Guide with FOSS
sidebar_position: 2
level: beginner
type: guide
status: published
visibility: public
topics:
  - accessibility
  - assistive-technology
  - tool:WAVE
  - tool:Lighthouse
  - tool:NVDA
  - tool:VoiceOver
---

# Quickstart: A 7-Day Plan with Free Open Source Tools

This plan is designed to get you hands-on with core accessibility concepts in one week, using freely available, and wherever possible, open-source tools.

- **Day 1: Foundations & Tools**
    - **Read**: Start with the fundamentals by reading the [W3C WAI – Accessibility Fundamentals](https://www.w3.org/WAI/fundamentals/accessibility-intro/) to understand the scope of web accessibility. Follow this with the [Introduction to WCAG](https://www.w3.org/WAI/WCAG21/Understanding/intro) to learn about the guidelines that define accessibility.
    - **Skim**: Get a practical overview with [The A11Y Project Checklist](https://www.a11yproject.com/checklist/). This is a great reference for what to look for.
    - **Install Tools**: Install browser extensions to help you test. The [WAVE](https://wave.webaim.org/extension/) extension is a great tool for evaluating web accessibility. Google's [Lighthouse](https://developer.chrome.com/docs/lighthouse/accessibility/scoring) is another excellent, open-source tool built directly into Chrome and Edge DevTools.

- **Day 2: Keyboard-Only Navigation**
    - **Practice**: Unplug your mouse and navigate a complex website using only your keyboard. Use `Tab` to move forward, `Shift+Tab` to move backward, `Enter` to activate links and buttons, `Space` to check/uncheck boxes, and arrow keys for radio buttons and sliders.
    - **Learn**: Pay close attention to the visible focus indicator (the outline around interactive elements). Is it always visible? Does the order in which you `Tab` through elements make sense? 
      - Read about creating [Skip Navigation Links](https://www.geeksforgeeks.org/html/how-to-add-skip-navigation-links-for-better-web-accessibility-in-html/)
      - and about [The Navigation Section element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/nav/) to allow users to bypass repetitive navigation.

- **Day 3: Semantic HTML and Structure**
    - **Learn**: Dive into the importance of using correct HTML elements for their intended purpose. Use landmarks like `<header>`, `<nav>`, `<main>`, and `<footer>` to define regions of a page. Ensure headings (`<h1>` through `<h6>`) form a logical outline of the content.
    - **Read**: Get a quick introduction to ARIA (Accessible Rich Internet Applications) with [ARIA basics in 15 minutes](https://www.tpgi.com/aria-basics-in-15-minutes/). The first rule of ARIA is to not use ARIA; always prefer using native HTML elements when they are available.

- **Day 4: Images, Media, & Color Contrast**
    - **Practice**: Alternative text is crucial for non-text content. Use the [W3C's Alt Text Decision Tree](https://www.w3.org/WAI/tutorials/images/decision-tree/) to practice writing meaningful alt text for different types of images (e.g., decorative, functional, complex).
    - **Check**: Color contrast is vital for readability. Use a [Color Contrast Checker](https://webaim.org/resources/contrastchecker/) to test a site's color palette. Ensure that text and important UI elements meet at least WCAG AA contrast ratios.

- **Day 5: Inclusive Components**
  - **Learn**: Read about a component on [Inclusive Components](https://inclusive-components.design/). Choose one that interests you, for example, a "Content Filter" or a "Data Table".
  - **Practice**: Try to build the component yourself, following the principles from the article. Pay attention to the ARIA attributes and keyboard interactions.

- **Day 6: Automated and Manual Testing**
    - **Run Automated Checks**: Use the tools you installed on Day 1. Run Lighthouse (via the "Audits" or "Lighthouse" panel in your browser's DevTools) and the WAVE extension on a page. These tools can catch many common issues automatically.
    - **Practice a Basic Screen Reader Check**: Get a feel for how screen readers announce content. Use [NVDA on Windows](https://www.nvaccess.org/download/) (it's free and open-source) or [VoiceOver on macOS](https://www.apple.com/voiceover/info/guide/10.15/) (built-in) to navigate and read through a web page. Can you understand the content and operate all controls?

- **Day 7: Review, Fix, and Share**
    - **Fix**: Based on your testing, choose one accessibility issue you discovered this week and fix it in your own code or a demo project. This could be adding a missing label, improving color contrast, or fixing a keyboard navigation trap.
    - **Share**: Document what you found and how you fixed it. Share this with your team, in a blog post, or on social media. Raising awareness is a key part of building a more accessible web.

## URL Reference List
- W3C WAI – Accessibility Fundamentals: https://www.w3.org/WAI/fundamentals/accessibility-intro/
- Introduction to WCAG: https://www.w3.org/WAI/WCAG21/Understanding/intro
- The A11Y Project Checklist: https://www.a11yproject.com/checklist/
- WAVE Browser Extension: https://wave.webaim.org/extension/
- Lighthouse: https://developer.chrome.com/docs/lighthouse/accessibility/scoring
- Skip Navigation Links: https://www.geeksforgeeks.org/html/how-to-add-skip-navigation-links-for-better-web-accessibility-in-html/
- The Navigation Section element: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/nav/
- ARIA basics in 15 minutes: https://www.tpgi.com/aria-basics-in-15-minutes/
- W3C's Alt Text Decision Tree: https://www.w3.org/WAI/tutorials/images/decision-tree/
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/
- Inclusive Components: https://inclusive-components.design/
- NVDA Screen Reader: https://www.nvaccess.org/download/
- VoiceOver on macOS: https://www.apple.com/voiceover/info/guide/10.15/
