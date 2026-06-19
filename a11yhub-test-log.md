# A11YHub — Accessibility Test Log

Manual tests run after each change. Flagged for future automation where possible.
Automated tests live in `accessibility-resource/e2e/`.

---

## HOT-001 — Hot Topics filter buttons
**Change:** aria-live count, aria-atomic, removed redundant sr-only span, simplified aria-label on topic links, removed auto-focus useEffect  
**Files:** `accessibility-resource/src/pages/hot-topics.js`  
**Date:** June 2026  
**Status:** ✅ Done — all tests pass. SR-NEW-2 browse mode behavior confirmed expected (not a code bug).

### Keyboard tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| K1 | Tab to the first filter button | Focus lands on the button, visible focus ring appears | ✅ Pass |
| K2 | Press Space or Enter on a filter button | Button activates, topic list updates | ✅ Pass |
| K3 | Tab through all four filter buttons | Each button is reachable in order, no traps | ✅ Pass |
| K4 | Activate two filters, then deactivate one | Button unpresses, list updates accordingly | ✅ Pass |

### Screen reader tests (NVDA + Firefox recommended)
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| SR1 | Focus a filter button, listen to announcement | Reads label ("Filter by category: Tool"), role ("toggle button"), and state ("pressed" or "not pressed") — category name announced once only | ✅ Pass |
| SR2 | Activate a filter button | Live region announces e.g. "Showing 3 of 18 topics. Filtered by: Protocol" | ✅ Pass |
| SR3 | Activate a second filter | Live region announces full updated message (both filters + new count) | ✅ Pass |
| SR4 | Deactivate all filters | Live region announces "Showing all 18 topics" | ✅ Pass |
| SR5 | Tab to the topics list after filtering | Focus moves into the list; no unexpected announcements | ✅ Pass |
| SR-NEW-1 | Activate filter, listen after | Focus stays on button; NVDA announces count via live region | ✅ Pass — NVDA reads count + filtered categories via live region |
| SR-NEW-2 | Press arrow keys after filtering | Right arrow triggers NVDA browse mode (virtual cursor) — reads forward through DOM: remaining filter button labels → live region → topic grid (filtered items only). TAB moves focus element-to-element correctly. Arrow key behavior is expected; no code bug. | ✅ Pass (expected browse mode behavior — original expectation was wrong) |
| SR-NEW-3 | Activate filter, then Tab | Focus moves to first topic link in filtered list | ✅ Pass |

### Visual / functional tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| V1 | Activate a filter button | Button shows pressed state visually (underline + checkmark) | ✅ Pass |
| V2 | Check srOnly is visually hidden but AT-accessible | sr-only text not visible; live region still announced by screen reader | ✅ Pass — filter status is intentionally visible (removed srOnly, added filterStatus class) |
| V3 | Console: `document.querySelector('[aria-label="Filter by category: Protocol"]').getAttribute('aria-pressed')` | Returns "true" when active, "false" when not | ✅ Pass |
| V4 | Filter by "Tool", then "Concept" | Only Tool + Concept topics appear in the list | ✅ Pass |

### Open issues
_None._

### CSS fixes applied (HotTopics.module.css)
- **HOT-001-CSS-A** (WCAG 2.4.7) `.topic-tag:focus` / `.topic-tag:hover` → `.topicTag:focus` / `.topicTag:hover` — dead selectors; topic links had no focus ring.
- **HOT-001-CSS-B** `.filterStatus` class added — was used in JS line 100 but missing from CSS; live region rendered without layout stability (`min-height: 1.4em` prevents shift on filter change).
- **HOT-001-CSS-C** `.inactive { opacity: 0.5 }` → `color: #767676; border-color: #ccc` — opacity halved contrast on colored text; replaced with explicit neutral grey.
- **HOT-001-CSS-D** Duplicate rules removed: `.filterButton`, `.legendSection`, `.legendGrid`, `.legendItem` each appeared twice; merged into single declarations.
- **HOT-001-CSS-E** `.srOnly` already camelCase — no rename needed (original open issue was already resolved).

### Resolved issues
- **HOT-001-NVDA** ✅ Root cause: NVDA + Brave browser incompatibility. Brave's sandboxing breaks accessibility APIs — NVDA only reads "Chrome legacy window". **Always test NVDA with Firefox.** Not a code bug.

### ⚠️ Standing rule: NVDA testing must use Firefox
NVDA has known issues with Brave and other Chromium-based browsers. Firefox is the reference browser for all screen reader tests in this project.

### Automation notes
- K1–K4: automatable with Playwright keyboard API
- SR1–SR5: use axe-core as proxy for ARIA state validation
- V3: automatable with `@axe-core/playwright`
- V4: automatable with Playwright — assert visible list items match expected types

---

## HOT-002 — Hot Topics page integrity (automated)
**Change:** Added Playwright e2e test suite to guard against the filter page being silently replaced by the mermaid flatmap.  
**Files:** `accessibility-resource/e2e/hot-topics.spec.js`, `accessibility-resource/playwright.config.js`  
**CI job:** `e2e` in `.github/workflows/ci-checks.yml` (runs after `build`, blocks on failure)  
**Date:** June 2026  
**Status:** ✅ Tests written — run `npm run test:e2e` from `accessibility-resource/` after first install (see Setup below)

**Background:** The navbar "Hot Topics" item was accidentally pointed at `/docs/hot-topics` (the auto-generated mermaid flatmap index) instead of `/hot-topics` (the React filter page at `src/pages/hot-topics.js`). The filter UI was silently unreachable with no build error. Fixed 2026-06-18; this suite prevents recurrence.

### Setup (first time only)
```bash
cd accessibility-resource
npm install          # installs @playwright/test
npx playwright install --with-deps chromium firefox
npm run build        # required — tests run against the built site
npm run test:e2e
```

### Tests

| # | Test | What it catches | Automated |
|---|------|-----------------|-----------|
| N1 | Navbar "Hot Topics" link resolves to `/hot-topics` | Navbar repointed to wrong path | ✅ |
| N2 | Page is NOT the mermaid flatmap (no `.mermaid` element) | React page replaced by generated index | ✅ |
| F1 | Filter group `[role=group]` is visible | Filter UI removed or hidden | ✅ |
| F2 | 4 filter buttons present with `aria-pressed="false"` on load | Button count changed; ARIA missing | ✅ |
| F3 | Topic cards visible on load | List not rendering | ✅ |
| F4 | Activating a filter sets `aria-pressed="true"` and updates live region | Filter state broken | ✅ |
| F5 | Deactivating all filters restores "all topics" in live region | Filter reset broken | ✅ |
| K1 | Filter button is keyboard-focusable and activatable with Space | Keyboard regression | ✅ |

### Open issues
_None._

### Automation notes
- All tests run in Chromium and Firefox (see `playwright.config.js`)
- Playwright report uploaded as a CI artifact on every run (pass or fail)
- To add more e2e tests: create `accessibility-resource/e2e/<name>.spec.js`

---

## LINK-001 — Broken internal path replacement
**Change:** `/accessibility-resource/docs/` → `/accessibility-hub/docs/` in overview.md and overview_upload.md  
**Files:** `accessibility-resource/docs/00-about/overview.md`, `accessibility-resource/overview_upload.md`  
**Date:** June 2026  
**Status:** ✅ Done — pending CI confirmation on push

### Tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| L1 | Run CI markdown-link-check | Zero broken link failures on overview files | ⬜ Re-run pending — history: (a) 2026-06-09 first run CRASHED on the space in the old filename (`find \| xargs` unquoted); fixed via rename + `find -print0 \| xargs -0`. (b) Second run: checker worked but reported two classes of FALSE positives, both fixed in `.mlc-config.json`: **403s** — sites that block bot requests but work in a browser; 403 added to `aliveStatusCodes`. **Fake 404s ending in `)%22%5D`** — not real links: the checker scans raw frontmatter and grabs `https://github.com/...)"]` from `author: ["Name (url)"]`. First fix (`["']` pattern) failed — the checker URL-encodes links BEFORE pattern matching, so the pattern must match `%22|%5D` too. Corrected to `[\"']\|%22\|%27\|%5B\|%5D`; verified locally with markdown-link-check: artifact link shows `[/]` (ignored), legit links incl. URLs ending in `)` still checked. Also added 405 to aliveStatusCodes (nia.nih.gov rejects HEAD) and raised timeout to 20s (fcc.gov status 0). HOW TO READ: `continue-on-error: true` means green proves nothing — read the step log for ERROR lines. Expect real broken links in contributing.md (backlog #11). |
| L2 | Open the live site Overview page, click each section link | Each link navigates to the correct page (no 404) | ✅ Pass (with caveat) — verified 2026-06-09 by fetching the live page and matching every listed path against the generated sitemap slugs; all resolve. CAVEAT: the section paths in overview.md are plain text like `For Users (/accessibility-hub/docs/for-users)`, NOT clickable links — nothing to click. Improvement filed: convert them to real markdown links. One stale path (`how_to-%20contribute`) found and fixed (see GEN-001/G6). |
| L3 | Check contributing.md links still resolve | GitHub repo links with `/accessibility-resource/docs/` still work | ✅ Pass — verified in terminal |

### Automation notes
- L1: already automated via `.github/workflows/ci-checks.yml` (markdown-link-check step)
- L2: automatable with Playwright — `expect(page).not.toHaveURL(/404/)` after each link click
- L3: covered by CI link-check

---

## FLATMAP-001 — Non-JS text navigation fallback
**Change:** Added `build_text_nav()` to `generate_mermaids.py`; emits `<details class="flatmap-text-nav">` block after each mermaid code fence in all three generator functions.  
**Files:** `accessibility-resource/flatmap-tools/generate_mermaids.py` (run to regenerate all `index.md` files)  
**Date:** June 2026  
**Status:** ✅ Done — verified visually in `npm run serve`

### Keyboard tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| K1 | Tab to the "Text navigation" `<details>` summary on any flatmap page | Focus lands on summary, visible focus ring appears | ✅ Pass — but requires tabbing through every mermaid node first. See open issue K1-REACHABILITY. |
| K2 | Press Space or Enter on the summary | `<details>` expands, list of links becomes visible | ✅ Pass |
| K3 | Tab through the expanded link list | Each link is reachable in order, no traps | ✅ Pass |
| K4 | Press Enter on a link | Navigates to the correct section page | ✅ Pass |
| K5 | Press Space or Enter on expanded summary | `<details>` collapses | ✅ Pass |

### Screen reader tests (NVDA + Firefox)
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| SR1 | Navigate to Site Overview, enter browse mode | NVDA announces "Text navigation (no-JS / screen reader alternative), collapsed" for the `<details>` summary | ✅ Pass |
| SR2 | Activate the summary | NVDA announces "expanded"; link list items become readable | ✅ Pass |
| SR3 | Read through link list | Each item announced as a link with the section name; no orphan or duplicate entries | ✅ Pass |
| SR4 | Activate a link | NVDA announces new page title on navigation | ✅ Pass |
| SR5 | Repeat SR1–SR4 on For Developers index and Full Site Map pages | Same behavior on all generated flatmap pages | ✅ Pass |

### Visual / functional tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| V1 | Load Site Overview in browser with JS enabled | Mermaid graph renders above; `<details>` section visible below | ✅ Pass |
| V2 | Count links in `<details>` list vs nodes with click handlers in the mermaid block | Counts match | ✅ Pass |
| V3 | Disable JS (DevTools → Network conditions → JS blocked), reload | Mermaid doesn't render; `<details>` fallback still present and all links resolve | ✅ Pass |

### Open issues
- **K1-REACHABILITY** 🔴 The `<details>` text nav is placed AFTER the mermaid block. Every mermaid node is a tab stop, so keyboard users must tab through the entire graph before reaching it. Fix: move `build_text_nav()` output to BEFORE the mermaid block in the generator. (WCAG 2.4.1 — bypass blocks)

### Automation notes
- K1–K5: automatable with Playwright keyboard API (`page.keyboard.press('Tab')`, `press('Enter')`)
- SR1–SR4: use axe-core to verify `<details>` / `<summary>` role semantics; full SR flow requires manual NVDA test
- V2: automatable — parse generated `index.md`, assert link count in `<details>` equals `click` line count in mermaid block
- V3: automatable with Playwright — `page.setJavaScriptEnabled(false)`, assert `details` element visible and links resolve

---

## FLATMAP-002 — Legend mismatch fix
**Change:** Removed icon_tags row from `create_compact_legend()` in `generate_mermaids.py`. Icons were never visible in the graph because `create_node_label()` calls `_strip_emojis()` on every label before writing to mermaid.  
**Files:** `accessibility-resource/flatmap-tools/generate_mermaids.py`  
**Date:** June 2026  
**Status:** ✅ Done — verified visually in `npm run serve`

### Visual / functional tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| V1 | Load any flatmap page, inspect the Legend | Legend shows only border color dots and background color rows; no emoji icon entries | ✅ Pass |
| V2 | Compare mermaid node appearance to legend entries | Every entry in the legend corresponds to a visible visual property on at least one node | ✅ Pass — resolved by FLATMAP-003 legend redesign (Alex verified 2026-06-09) |
| V3 | Run generate_mermaids.py, grep generated index.md files for icon legend pattern | No `\*\*🚧\*\*` / `\*\*💻\*\*` style entries in any legend block | ✅ Pass |

### Open issues
- **LEG-001** 🔴 Depth-based background colors (5-color palette: blue, purple, pink, orange, green) are visible throughout the graph but not explained in the legend. They are applied via `classDef col{d}` (structural depth), not via tag config, so `create_compact_legend()` never sees them. Fix: add a "node color = depth in site hierarchy" note to the legend output, OR explicitly document the palette.
- **LEG-002** 🔴 `bg grey: status:review-needed, status:draft, status:missing` has no visual indicator — the text "bg grey" is not self-explanatory to a sighted user and provides no color sample. Fix: add inline HTML color swatch (small colored square via inline style) next to each bg/border label.
- **LEG-003** 🟡 Legend `<small>` block and `<details>` text nav are rendered with no visual separation. Fix: add `margin-top` / `border-top` CSS to `.flatmap-text-nav` in Docusaurus custom CSS, or add inline style in the generator.

### Automation notes
- V3: automatable — add a CI step that greps all generated `index.md` files for bold-emoji patterns in `<small>` legend blocks and fails if found

---

## FLATMAP-003 — Legend split: mini legend + dedicated legend page
**Change:** Replaced the large inline SVG legend with a compact 580×78 strip (`create_mini_legend()`) under every flatmap, linking to a new auto-generated full legend page at `/docs/about/legend` (`generate_legend_page()` writes `docs/00-about/legend.md` each run: full SVG + markdown text tables). Old function renamed `create_full_legend()`, now used only by the legend page.  
**Files:** `accessibility-resource/flatmap-tools/flatmap_styles.py`, `accessibility-resource/flatmap-tools/generate_mermaids.py`  
**Date:** June 2026  
**Status:** ✅ Done — all tests pass (V1–V5, K1–K2, SR1–SR3; Alex verified 2026-06-09). SR2 closed as test-technique (LEG-004).

### Visual / functional tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| V1 | Load each flatmap page (Site Overview, section indexes, Full Site Map) | Compact mini legend renders below the graph: one Status row (4 shapes), one Level row (4 border samples) | ✅ Pass |
| V2 | Click the "How to read this map — full legend" link under the mini legend | Navigates to `/docs/about/legend`; full legend page displays with large SVG + explanation | ✅ Pass |
| V3 | Check the About section flatmap and text nav | "Map Legend" appears as a clickable node and as a text-nav link | ✅ Pass |
| V4 | Run `generate_mermaids.py` twice | `legend.md` regenerates identically; no drift between mini legend and full page styles | ✅ Pass |
| V5 | Open `/docs/about/legend`, check "Folder colors" section | Depth swatch strip (5 colors, Depth 0–4+) + table render; intro lists three encoded signals | ✅ Pass |

### Keyboard tests
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| K1 | Tab to the full-legend link below the mini legend | Focus lands on the link, visible focus ring appears | ✅ Pass |
| K2 | Press Enter on the link | Navigates to the legend page | ✅ Pass |

### Screen reader tests (NVDA + Firefox)
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| SR1 | Browse to the mini legend SVG | NVDA announces the aria-label summary (status = shape, level = border pattern, all eight values named) | ✅ Pass |
| SR2 | On the legend page, navigate both markdown tables with browse-mode arrows / Ctrl+Alt+Arrows | Tables navigable cell-by-cell, headers announced; same info as the SVG | ✅ Pass — original "reads row by row" expectation was wrong (NVDA doesn't auto-read tables); see resolved LEG-004 |
| SR3 | Browse the full legend SVG on the legend page | Announced as image with aria-label "Flatmap legend: status shapes and level border patterns" | ✅ Pass |

### Open issues
_None._

### Resolved issues
- **LEG-004** ✅ (SR2) Resolved 2026-06-09 — test-technique, not a code bug (same pattern as SR-NEW-2 in HOT-001). NVDA does not auto-read tables; rows are reachable with browse-mode arrows / `Ctrl+Alt+Arrows` table navigation. SR2 expectation updated: "Tables are navigable cell-by-cell with Ctrl+Alt+Arrows, announcing headers."
- **LEG-001** ✅ Resolved — `create_depth_legend()` added to `flatmap_styles.py`; legend page now has a "Folder colors — depth in the hierarchy" section with an SVG swatch strip (aria-labelled) + text table, both generated from `DEPTH_PALETTE` so they can't drift. Verify visually via V5.
- **LEG-002** ✅ Resolved by redesign — text-only "bg grey" rows are gone; mini and full legends show real rendered samples (shape + fill + border) for every entry.
- **LEG-003** 🟡 Likely resolved — mini legend has its own bordered white background, giving visual separation from the text nav. Confirm visually alongside V3.

### Automation notes
- V4: automatable — run generator twice in CI, `git diff --exit-code` on generated files
- K1–K2: automatable with Playwright keyboard API
- SR1/SR3: use axe-core to assert `role="img"` + non-empty `aria-label` on legend SVGs
- V2: automatable with Playwright — click link, assert URL and `h2` text "Map Legend"

---

## GEN-001 — Title-parsing hardening + malformed slug fixes
**Change:** (1) Removed inline template comment from `title:` in `accessible-web-dev-checklist.md` — it leaked into generated text-nav links as "...Checklist # A concise, descriptive title...". (2) Renamed `how_to- contribute.md` → `how-to-contribute.md` and `accessible-ap-_design-guide.md` → `accessible-api-design-guide.md` (malformed slugs; space / stray chars in URL). (3) Hardened title extraction: `flatmap_nodes.extract_title()` strips inline YAML comments (quoted titles containing `#` preserved) and its H1 fallback skips frontmatter; `util.extract_title()` skips frontmatter when scanning for H1 (frontmatter comments like `# Resource Metadata:` could become breadcrumb titles).  
**Files:** `accessibility-resource/docs/20-for-developers/` (3 files), `accessibility-resource/flatmap-tools/flatmap_nodes.py`, `accessibility-resource/flatmap-tools/util.py`  
**Date:** June 2026  
**Status:** ✅ Done — all tests pass (G4/G5 verified by Alex 2026-06-09). Follow-up fix: two hand-written references to the old slug (`how_to-%20contribute`, URL-encoded space — evaded the original grep) found in `overview.md` + `overview_upload.md`; both updated to `/for-developers/how-to-contribute`.

### Unit tests (parser logic)
| # | Input | Expected | Pass/Fail |
|---|-------|----------|-----------|
| U1 | `title: My Page  # comment` | `My Page` | ✅ Pass |
| U2 | `title: "Quoted # not comment"` | `Quoted # not comment` | ✅ Pass |
| U3 | Frontmatter comment `# Resource Metadata:` + body `# Real H1` | `Real H1` (both parsers) | ✅ Pass |
| U4 | No frontmatter, `# Plain H1` | `Plain H1` | ✅ Pass |
| U5 | `title: C# Accessibility Guide` (no space before #) | unchanged | ✅ Pass |

### Generated output checks
| # | Steps | Expected | Pass/Fail |
|---|-------|----------|-----------|
| G1 | grep generated docs for `A concise` | No matches in generated index/sitemap files | ✅ Pass |
| G2 | grep generated docs for old slugs (`how_to- contribute`, `ap-_design`) | No matches | ✅ Pass |
| G3 | Text-nav links use new slugs with correct titles | `/for-developers/how-to-contribute`, `/for-developers/accessible-api-design-guide` | ✅ Pass |
| G4 | `npm run build` + `serve`, open For Developers flatmap | Clean titles, links resolve, no 404 | ✅ Pass |
| G5 | After deploy: old URL `/for-developers/accessible-ap-_design-guide` | Will 404 — confirm no external links rely on it (URL change accepted) | ✅ Pass |
| G6 | grep repo for URL-encoded old slugs (`%20contribute`, `ap-_design`) | Zero matches incl. hand-written prose refs | ✅ Pass — after fixing overview.md + overview_upload.md (2026-06-09). Lesson: when renaming files, grep the URL-encoded variant too. |

### Automation notes
- U1–U5: keep as a pytest file under `flatmap-tools/` (currently run ad hoc)
- G1–G2: add CI grep step over generated `index.md` files (same place as the emoji-legend grep idea in FLATMAP-002)

---

_Add a new section here after each change following the same format._
