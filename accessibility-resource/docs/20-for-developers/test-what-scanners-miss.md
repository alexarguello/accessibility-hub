---
title: "Test What Scanners Miss"
sidebar_label: "Test what scanners miss"
sidebar_position: 8
description: "Why a high Lighthouse score is not a tested page, and the layers of testing that do catch the defects that block screen reader users and AI agents — with Java recipes for axe-core, role-based locators, aria snapshots and keyboard tests."
level: intermediate
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
  - screen-readers
  - keyboard-accessibility
  - wcag
  - ai-accessibility
topics:
  - accessibility-testing
  - wcag
  - tool:axe
  - tool:Lighthouse
  - tool:NVDA
  - tool:Playwright
author:
  - Alexandra Arguello Saenz (https://github.com/alexarguello)
---

# Test What Scanners Miss

In the [accessibility tree experiment](./ai-agents-read-your-accessibility-tree.md), a
registration form that **no screen reader user and no AI agent could complete** still scored
**91/100** in a Lighthouse accessibility audit. This page explains why, and which tests do catch
those defects.

## Why a high score is not a tested page

Automated scanners such as Lighthouse, axe and WAVE read your markup and check it against rules.
They are fast and reliable at what they check. But they can only judge code that **tries** to be a
control: an `<img>`, an `<input>`, a `<button>`. They cannot see:

- **A control that never tries.** A `<div>` styled as a dropdown, or a `<span>` with a click
  handler, has no role. To the scanner it is just text. There is nothing to fail.
- **Whether a task can be finished.** A scanner checks one page at a time. It doesn't try to
  register, check out or log in.
- **Meaning.** It can tell that an image has `alt` text, not whether the text is right. It can
  tell that an error message exists, not whether anyone is told about it.

Lighthouse also gives a **weighted score**. It runs a subset of the axe-core rules, and a page
with a few failures on a large page can still score in the 90s. Treat the score as a trend line,
not a pass mark.

Keep the scanner. It catches real defects cheaply on every build. Just add the layers below.

## The layers of testing

| Layer | Tools | What it catches | Effort |
|---|---|---|---|
| **1. Scanner in CI** | [axe-core](https://github.com/dequelabs/axe-core) (Java bindings for Playwright and Selenium), [pa11y](https://pa11y.org/), [IBM Equal Access Checker](https://www.ibm.com/able/toolkit/tools/) | Missing labels, missing `alt` text, low contrast, missing landmarks, invalid ARIA | Low. Runs on every build. |
| **2. Accessibility tree tests** | Playwright `getByRole` and aria snapshots, [Testing Library `ByRole`](https://testing-library.com/docs/queries/byrole/) | Controls with no role or no name, fake buttons, fake dropdowns, missing headings | Low. Uses tests you already write. |
| **3. Keyboard tests** | Manual script below, or a scripted Tab path in Playwright | Unreachable controls, focus traps, invisible focus, wrong focus order | 5 minutes per flow by hand |
| **4. Guided manual check** | [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/) (FastPass, Tab stops, Assessment) | Issues that need a human: color-only meaning, reading order, meaningful text alternatives | 30–60 minutes per page |
| **5. Screen reader check** | [NVDA](https://www.nvaccess.org/download/) + Firefox, VoiceOver + Safari | Missing or wrong announcements, silent errors, confusing reading order | 10 minutes per flow |
| **6. Agent test** (optional) | An agent limited to accessibility tree tools, like the [experiment](./ai-agents-read-your-accessibility-tree.md) | Whether software acting for a user can finish the task | Medium |
| **7. Testing with disabled users** | Usability sessions with people who use assistive technology every day | Real problems that no tool predicts | Highest value |

Layers 1 and 2 belong in CI. Layers 3 and 5 belong in your definition of done for any change to a
user flow. Layer 4 fits a release or a quarterly review. Layer 7 is how you find out whether any of
it actually works for people.

## Which test catches which defect

These are the four defects that broke the registration form in the experiment, plus the general
behavior of each kind of test:

| Defect | Scanner (axe / Lighthouse) | Tree test (`getByRole`) | Keyboard test | Screen reader |
|---|---|---|---|---|
| `<span onclick>` instead of a link | **Missed.** A span with a click handler has no role to check. | **Caught.** There is no `link` named "Register". | **Caught.** The span can't get focus. | **Caught.** It's read as plain text, if at all. |
| Placeholder instead of a label | **Caught** (`label` rule). | **Not reliable.** A placeholder can still be used as the field's name. | **Missed.** The field works with the keyboard. | **Partly.** Some screen readers read the placeholder; it disappears once you type. |
| `<div>` pretending to be a dropdown | **Missed.** The div has no role. | **Caught.** There is no `combobox`. | **Caught.** It can't be reached or opened. | **Caught.** It isn't announced as a control. |
| Error shown by color only | **Missed.** Color has no rule to fail. | **Caught**, if you assert a `role="alert"` message. | **Missed.** | **Caught.** Nothing is read out. |

The tree test catches three of the four, and it is code you already write. The scanner caught one.
That is the difference between "the page passes" and "the task works".

> **If your test can find the control by role and name, so can an agent and a screen reader.**

## Recipes for Java

These use [Playwright for Java](https://playwright.dev/java/) with JUnit 5. Each one fits in an
existing end-to-end test. The control names come from a registration form like the one in the
experiment; change them to match your own page.

### Layer 1: axe-core in a test

Add the axe-core Playwright bindings (check Maven Central for the latest version):

```xml
<dependency>
  <groupId>com.deque.html.axe-core</groupId>
  <artifactId>playwright</artifactId>
  <version><!-- latest --></version>
  <scope>test</scope>
</dependency>
```

```java
import com.deque.html.axecore.playwright.AxeBuilder;
import com.deque.html.axecore.utilities.axeresults.AxeResults;

@Test
void registerPageHasNoAxeViolations() {
    page.navigate(baseUrl + "/register/123");

    AxeResults results = new AxeBuilder(page)
            .withTags(List.of("wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"))
            .analyze();

    assertTrue(results.getViolations().isEmpty(),
            () -> results.getViolations().stream()
                    .map(v -> v.getId() + ": " + v.getHelp())
                    .collect(Collectors.joining("\n")));
}
```

Selenium users can use the `com.deque.html.axe-core:selenium` artifact, which works the same way
with a `WebDriver`.

### Layer 2: find controls by role and name

```java
@Test
void userCanRegisterUsingOnlyRolesAndNames() {
    page.navigate(baseUrl + "/sessions");

    page.getByRole(AriaRole.LINK, new Page.GetByRoleOptions().setName("Register")).first().click();
    page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Full name")).fill("Ada Lovelace");
    page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Email")).fill("ada@example.com");
    page.getByRole(AriaRole.COMBOBOX, new Page.GetByRoleOptions().setName("Meal preference")).selectOption("Vegetarian");
    page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Register")).click();

    assertThat(page.getByRole(AriaRole.MAIN)).containsText("confirmation code");
}
```

Every step fails if the control has no role or no name. On the broken variant, this test fails on
the first line.

### Layer 2: check that errors are announced

```java
@Test
void invalidEmailErrorIsAnnounced() {
    page.navigate(baseUrl + "/register/123");
    page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Email")).fill("not-an-email");
    page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Register")).click();

    // role="alert" is read out by screen readers as soon as it appears
    assertThat(page.getByRole(AriaRole.ALERT)).containsText("valid email");
}
```

This is the test that catches "error shown by color only". A red border has no role.

### Layer 2: snapshot the accessibility tree

An aria snapshot records the part of the tree you care about, as text. If someone replaces a
`<select>` with a styled `<div>`, the snapshot no longer matches.

```java
@Test
void registrationFormTreeIsStable() {
    page.navigate(baseUrl + "/register/123");

    assertThat(page.getByRole(AriaRole.MAIN)).matchesAriaSnapshot("""
        - heading "Register" [level=1]
        - textbox "Full name"
        - textbox "Email"
        - combobox "Meal preference"
        - button "Register"
        """);
}
```

To see what your page looks like today, print it once with
`System.out.println(page.getByRole(AriaRole.MAIN).ariaSnapshot());`. This is the same view the
agent in the experiment used to understand the page.

### Layer 3: script the Tab order

```java
@Test
void keyboardUserReachesEveryFieldInOrder() {
    page.navigate(baseUrl + "/register/123");

    List<Locator> expectedOrder = List.of(
            page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Full name")),
            page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("Email")),
            page.getByRole(AriaRole.COMBOBOX, new Page.GetByRoleOptions().setName("Meal preference")),
            page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Register")));

    expectedOrder.get(0).focus();
    for (int i = 1; i < expectedOrder.size(); i++) {
        page.keyboard().press("Tab");
        assertThat(expectedOrder.get(i)).isFocused();
    }
}
```

This catches controls that can't get focus and focus that jumps somewhere unexpected. It doesn't
check that the focus is **visible**. That still needs a human, or a visual comparison test.

### The same tools in JavaScript

| Java | JavaScript / TypeScript |
|---|---|
| `com.deque.html.axe-core:playwright` | [`@axe-core/playwright`](https://www.npmjs.com/package/@axe-core/playwright) |
| `page.getByRole(AriaRole.BUTTON, ...)` | `page.getByRole('button', { name: 'Register' })` |
| `assertThat(locator).matchesAriaSnapshot(...)` | `await expect(locator).toMatchAriaSnapshot(...)` |
| — | Testing Library: `screen.getByRole('button', { name: 'Register' })` |

## A 5-minute keyboard check

Do this by hand for any change to a user flow.

1. Click in the browser's address bar, then press **Tab**. Focus should land on the first control
   on the page, or on a "Skip to main content" link.
2. Keep pressing **Tab** through the whole flow. Write down any control you can't reach.
3. At each stop, check that you can **see** the focus. A missing outline counts as a failure.
4. Check that the order makes sense: top to bottom, left to right, as the page reads.
5. Use each control: **Enter** on links and buttons, **Space** on checkboxes, **arrow keys** in
   dropdowns and radio groups, **Esc** in dialogs.
6. Open any dialog or menu. Check that focus moves into it, stays inside while it's open, and
   returns to where you were when it closes.
7. Finish the task. If you can't, that's the result of the test.

## A 10-minute screen reader check

This uses NVDA on Windows. NVDA works best with Firefox; with some Chromium browsers it may only
announce "Chrome legacy window".

1. Install [NVDA](https://www.nvaccess.org/download/) and start it. **Insert** is the NVDA key.
   **Ctrl** stops speech at any time.
2. Open your page in Firefox. Press **Insert+F7** to open the Elements List. Check the
   **Links**, **Headings**, **Form fields** and **Buttons** tabs. Every item should have a clear
   name. "Click here", "button" and blank entries are failures.
3. Press **H** to jump between headings. The headings should tell you what's on the page without
   reading it all.
4. Press **D** to jump between landmarks. You should find at least a main region.
5. Press **Tab** through the form. Each field should be read with its label, its type and whether
   it's required.
6. Submit the form with a mistake in it. The error should be read out without you having to look
   for it.
7. Finish the task with the screen on, then try again with the screen off.

On a Mac, VoiceOver (**Cmd+F5**) with Safari works the same way. Use the Rotor (**VO+U**) instead
of the Elements List.

## If you only do two things

1. **Write your end-to-end tests with `getByRole`.** It costs nothing extra, and it turns every test
   into an accessibility tree check.
2. **Do the 5-minute keyboard check** before you merge any change to a user flow.

Then add the scanner to CI, and the screen reader check before each release.

## Further reading

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — every rule, with how to meet it
- [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/) — free guided assessment from Microsoft
- [Playwright: aria snapshots](https://playwright.dev/java/docs/aria-snapshots) and [locators](https://playwright.dev/java/docs/locators)
- [axe-core rule descriptions](https://dequeuniversity.com/rules/axe/) — what each rule checks
- [WebAIM: Using NVDA to evaluate web accessibility](https://webaim.org/articles/nvda/)
- [What to Do Next](./what-to-do-next.md) — six steps to start on your own app
- [Accessible Web Development Checklist](./accessible-web-dev-checklist.md)
