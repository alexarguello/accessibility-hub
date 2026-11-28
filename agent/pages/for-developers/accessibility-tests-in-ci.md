# Enforce Accessibility with Playwright Tests in CI

A check that someone has to remember to run gets skipped. A test that runs on every pull request
does not. This page shows how to put Playwright end-to-end tests into a CI pipeline so that a
change which breaks a control for screen reader users, keyboard users or AI agents cannot be
merged without someone noticing.

The examples are this site's own pipeline. The workflow, the tests and the failure described
below are real and linked at the end.

## Why run accessibility tests in CI

- **Regressions arrive quietly.** Nobody removes a button's name on purpose. It happens during a
  redesign, a refactor or a library upgrade, and a code reviewer cannot see an accessible name in
  a diff.
- **Role and name are an interface.** A screen reader announces them, voice control software
  matches spoken commands against them, and an AI agent uses them to find the control. WCAG
  requires them in [4.1.2 Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html).
  An interface that other software depends on deserves a test.
- **It costs almost nothing extra.** If your end-to-end tests find controls by role and name, every
  test you already write is also an accessibility check. Playwright recommends role locators
  first because they are the closest to how users and assistive technology perceive the page
  ([Playwright: locators](https://playwright.dev/docs/locators)).
- **A blocking check changes behavior.** A report people may read is advice. A failed required
  check is a decision someone has to make before merging.

It has limits. Playwright's own documentation says that many accessibility problems can only be
found through manual testing. CI tests are the floor, not the whole job. See
[Test What Scanners Miss](https://alexarguello.github.io/accessibility-hub/docs/for-developers/test-what-scanners-miss/) for the layers that sit on top.

## The example: this site

This site is a static site built with Docusaurus and deployed to GitHub Pages. Its end-to-end
setup is four files, all in the public repository:

| File | What it does |
|---|---|
| `accessibility-resource/e2e/hot-topics.spec.js` | The tests: eight checks on the Hot Topics filter page |
| `accessibility-resource/playwright.config.js` | Serves the built site, sets the browsers and the CI behavior |
| `accessibility-resource/package.json` | The `test:e2e` script, which runs `playwright test` |
| `.github/workflows/ci-checks.yml` | The pipeline: link check, build, end-to-end tests, accessibility scan |

To run the same tests on your machine, clone the repository and run these from the
`accessibility-resource` folder:

```bash
npm ci
npx playwright install chromium firefox
npm run build
npm run test:e2e
```

The tests run against the built site, so run the build again after you change a page.

## How the pipeline works

These are the steps on this site, in order. The diagram after the list shows the same steps and adds no
information.

1. A developer opens a pull request.
2. The **build** job builds the site and saves the result as an artifact.
3. The **end-to-end test** job downloads that artifact, serves it locally, and runs the Playwright
   tests in Chromium and Firefox.
4. In parallel, the **scanner** job runs an automated accessibility scan over every page in the
   sitemap.
5. If any end-to-end test fails, the job fails. The pull request shows a failed check, and the
   Playwright report is uploaded so the developer can see which control was not found.
6. The developer fixes the page, or updates the test if the change was intended, and pushes
   again. The pipeline runs again from step 2.
7. When the end-to-end tests pass, the pull request can be merged.
8. The merge triggers the deploy.

## What the tests check

Each row is one kind of assertion. The first four need no extra library.

| What you assert | In Playwright | What it enforces |
|---|---|---|
| The control exists, with a role and a name | `page.getByRole('button', { name: /^Filter by Tool/i })` | WCAG 4.1.2. A `<div>` with a click handler fails here. |
| Its state is exposed | `expect(button).toHaveAttribute('aria-pressed', 'true')` | WCAG 4.1.2. A toggle that only changes color fails. |
| It works from the keyboard | `button.focus()`, then `page.keyboard.press('Space')` | WCAG 2.1.1 Keyboard. |
| Changes are announced | `expect(page.locator('#filter-context')).not.toBeEmpty()` on a live region | WCAG 4.1.3 Status Messages. |
| The structure has not changed | `expect(page.getByRole('main')).toMatchAriaSnapshot(...)` | Catches a native control swapped for a styled `<div>`. |
| No rule-based failures | `new AxeBuilder({ page }).analyze()` from `@axe-core/playwright` | The WCAG failures a scanner can detect, such as missing labels and low contrast. |

Two tests from this site's suite. They check a group of four filter buttons:

```js
test('filter buttons are present and have correct ARIA', async ({ page }) => {
  const buttons = page.getByRole('button', { name: /^Filter by /i });
  await expect(buttons).toHaveCount(4);

  for (const btn of await buttons.all()) {
    await expect(btn).toHaveAttribute('aria-pressed', 'false');
  }
});

test('filter button is keyboard-activatable with Space', async ({ page }) => {
  const toolBtn = page.getByRole('button', { name: /^Filter by Tool/i });
  await toolBtn.focus();
  await page.keyboard.press('Space');
  await expect(toolBtn).toHaveAttribute('aria-pressed', 'true');
});
```

Neither test mentions accessibility. They describe what a user does. They pass only if the
buttons have a role, a name, an exposed state and keyboard support.

For the same checks in Java, see the
[recipes in Test What Scanners Miss](https://alexarguello.github.io/accessibility-hub/docs/for-developers/test-what-scanners-miss/#recipes-for-java).

## The workflow

This is the relevant part of this site's GitHub Actions workflow, shortened: the real file also
sets a working directory and caches npm. The build job produces the site once, and the test job
reuses it.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: site-build
          path: build

  e2e:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx playwright install --with-deps chromium firefox
      - uses: actions/download-artifact@v4
        with:
          name: site-build
          path: build
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

And the part of `playwright.config.js` that serves the built site and sets the CI behavior:

```js
export default defineConfig({
  testDir: './e2e',
  forbidOnly: !!process.env.CI,       // a stray test.only fails the run
  retries: process.env.CI ? 1 : 0,    // one retry in CI, to absorb a slow start
  use: { baseURL: 'http://localhost:3000', trace: 'on-first-retry' },
  webServer: {
    command: 'npm run serve -- --port 3000 --no-open',
    url: 'http://localhost:3000/',
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
  ],
});
```

What matters in it:

- **`needs: build`** makes the tests run against the same output that will be deployed, not a
  development server.
- **`if: always()`** uploads the report when tests fail, which is the only time you need it.
- **Two browsers.** Browsers build the accessibility tree differently in places. Firefox is also
  the reference browser for NVDA.
- **No `continue-on-error` on the test step.** That is what makes the job blocking.

To turn a failing job into a rule, mark it as a required status check in the repository's branch
protection settings
([GitHub: about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).
Without that, a red check is still only a warning.

### Blocking and non-blocking jobs

On this site the end-to-end tests block. The scanner job (pa11y over the sitemap) reports
without blocking, because it started with a backlog of existing findings. That split is a
reasonable way to begin:

- Make **behavior tests** blocking from day one. They only cover what you wrote them for, so they
  start green.
- Run the **scanner** as a report until its backlog is cleared, then make it blocking too.

## A real failure on this site

In June 2026 the filter buttons were redesigned. Their accessible name changed from
"Filter by category: Tool" to "Filter by Tool (rectangle · solid border)", so that the shape of
each button is also available as text.

Four tests looked for the old name. From that commit on they could not pass, in either browser.
The other four tests in the file, which did not depend on the name, kept passing.

What that shows:

1. **The tests did their job.** The accessible name is what a screen reader user hears and what
   an agent searches for. It changed, and the pipeline said so.
2. **A changed name is an interface change.** Here the change was intended, so the right fix was
   to update the tests in the same pull request as the redesign. That did not happen, and the
   project's notes even recorded that no test depended on the label.
3. **Match the stable part of a name.** The tests now use `/^Filter by Tool/i`. They still fail if
   the button loses its name or its role, but not if the description in brackets is reworded.
4. **A red check that stays red stops enforcing anything.** The value of a blocking test is that
   red means stop. Fix or update a failing test promptly, or people learn to ignore it.

## When to use it, and when not

Use end-to-end accessibility tests for:

- **User flows:** sign-up, checkout, search, filters, navigation, dialogs.
- **Shared components:** one broken date picker breaks every form that uses it.
- **Every accessibility bug you fix.** Add a test with the fix so it cannot come back.
- **Anything an AI agent is expected to operate.**

Use a scanner over the sitemap, not hand-written tests, for content pages with no interaction.

Do not expect CI to judge:

- whether focus is visible
- whether alternative text is meaningful
- whether the reading order makes sense
- whether color is the only way something is shown
- how the page behaves with a real screen reader
- whether people can use it

Those need the manual checks and user testing described in
[Test What Scanners Miss](https://alexarguello.github.io/accessibility-hub/docs/for-developers/test-what-scanners-miss/#the-layers-of-testing).

## How this helps AI agents

AI agents that operate a browser do not look at your page the way a sighted person does. They
read the accessibility tree: roles, names and states. This site measured that in
[AI Agents Read Your Accessibility Tree, Not Your HTML](https://alexarguello.github.io/accessibility-hub/docs/for-developers/ai-agents-read-your-accessibility-tree/).

That is the same information a role locator uses. So:

- **If a test can find a control by role and name, an agent can too.** A passing flow test is
  evidence that an agent has a path through the task.
- **An aria snapshot is the agent's view of the page**, written down. Keeping it in a test keeps
  that view stable.
- **CI keeps it true over time.** A page that agents could use last month stays usable after the
  next redesign, because the redesign cannot merge while the test is red.
- **Failures are precise.** A failing role locator names the exact control and name that went
  missing. A person or a coding agent can act on that without guessing.

## Start in an afternoon

1. Pick one user flow that matters.
2. Write one test for it that uses only `getByRole` to find controls.
3. Add one keyboard assertion: focus a control, press a key, check the result.
4. Add the workflow above and make the test job a required check.
5. Add `@axe-core/playwright` as a report first. Make it blocking once it is clean.

## Resources

On this site:

- [Test What Scanners Miss](https://alexarguello.github.io/accessibility-hub/docs/for-developers/test-what-scanners-miss/): the layers of testing, with Java recipes
- [AI Agents Read Your Accessibility Tree, Not Your HTML](https://alexarguello.github.io/accessibility-hub/docs/for-developers/ai-agents-read-your-accessibility-tree/): the experiment behind the agent claims
- [Accessible Web Development Checklist](https://alexarguello.github.io/accessibility-hub/docs/for-developers/accessible-web-dev-checklist/)
- [What to Do Next: Six Steps for Your Own App](https://alexarguello.github.io/accessibility-hub/docs/for-developers/what-to-do-next/)
- [Accessibility Testing](https://alexarguello.github.io/accessibility-hub/docs/hot-topics/accessibility-testing/)

This site's pipeline:

- [CI workflow](https://github.com/alexarguello/accessibility-hub/blob/main/.github/workflows/ci-checks.yml)
- [End-to-end tests](https://github.com/alexarguello/accessibility-hub/blob/main/accessibility-resource/e2e/hot-topics.spec.js)
- [Playwright configuration](https://github.com/alexarguello/accessibility-hub/blob/main/accessibility-resource/playwright.config.js)

External:

- [Playwright: setting up CI](https://playwright.dev/docs/ci-intro)
- [Playwright: accessibility testing](https://playwright.dev/docs/accessibility-testing)
- [Playwright: aria snapshots](https://playwright.dev/docs/aria-snapshots)
- [Playwright: locators](https://playwright.dev/docs/locators)
- [`@axe-core/playwright`](https://www.npmjs.com/package/@axe-core/playwright)
- [pa11y-ci](https://github.com/pa11y/pa11y-ci)
- [WCAG 2.2: Understanding 4.1.2 Name, Role, Value](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html)
- [WCAG 2.2: Understanding 2.1.1 Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)
- [WCAG 2.2: Understanding 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

Source: https://alexarguello.github.io/accessibility-hub/docs/for-developers/accessibility-tests-in-ci/
