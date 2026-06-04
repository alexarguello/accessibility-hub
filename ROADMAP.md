# A11YHub Feature Roadmap — May 2026
Site: alexarguello.github.io/accessibility-hub

---

## WEEK 1 — Critical Fixes (~5 hrs)
- Fix `/accessibility-resource/` → `/accessibility-hub/` paths (H-3)
- Remove `<a href="#">Coming soon</a>` links (H-4)
- Fix duplicate logo alt text (H-1)
- Fix `editUrl` in `docusaurus.config.js` (M-2)
- Add CI markdown link checker
- **Done when:** Zero 404s, CI link-check passes

---

## WEEK 2 — Search Layer 1: Local Full-Text (~10 hrs)
- Install `@easyops-cn/docusaurus-search-local` (free, browser-only, no API key)
- Configure: `hashed:true`, `language:["en"]`, `highlightSearchTermsOnTargetPage:true`
- Add `aria-label`, `aria-pressed`, `aria-live` to filter buttons (H-2, M-3)
- Add flatmap non-JS fallback list (H-5)
- **Done when:** Search returns results; axe passes on `/hot-topics/`
- **Later:** Migrate to Algolia DocSearch (free OSS, better ranking/analytics, ~1 week approval)

---

## WEEK 3 — Chatbot /guide-me Page (~14 hrs)
**Flow:** Step 0 free input → Step 1 persona confirm → Step 2 (2-3 Qs) → Step 3 guide → Step 4 free chat

**4 Persona Tracks:**
| Persona | Trigger keywords | Questions |
|---|---|---|
| Disabled user/Caregiver | disability, assistive tech, daily life | disability type / goal / tools or community? |
| Developer/Designer | code, audit, WCAG, build, test | what building / goal / skill level |
| Educator/Researcher | teaching, research, curriculum | context / audience / format |
| Product/Business | compliance, legal, procurement | driver / need / timeline |

**AI Output (JSON):**
```json
{
  "guide_title": "string",
  "persona": "string",
  "summary": "string",
  "resources": [{ "title": "string", "url": "string", "why": "<20 words" }],
  "next_steps": "string",
  "content_gap": "optional — missing content for maintainers"
}
```

**Build-time:** Script walks `/docs`, reads frontmatter + first 200 chars → writes `/static/search-index.json`. Runs in GitHub Actions before Docusaurus build.

**API key strategy (static site — can't expose key client-side). Pick one before Week 3:**
- ✅ **Netlify Functions** (recommended — lowest friction, free tier, add `netlify.toml`)
- Vercel serverless (similar free tier)
- User pastes own Anthropic key → stored in `sessionStorage`

**System prompt:**
```
You are the A11YHub guide assistant.
Site index: ${JSON.stringify(siteIndex)}
Rules: return valid JSON only | link only to pages in index | "why" <20 words | max 8 resources | add content_gap if need not covered
```

**Export options:**
- Copy as text: Clipboard API, ~10 lines JS
- PDF: `window.print()` with print stylesheet, no server needed
- Stretch: GitHub Gist / URL-encoded share link

**Done when:** Full conversation completes; guide renders; exports work (~$0.02/session)

---

## WEEK 4 — Floating Widget + AI Search Fallback (~10 hrs)
- Floating button bottom-right: "Find your path →" (`aria-label="Find your accessibility path"`)
- Opens slide-in panel with first question; full experience → opens `/guide-me`
- Wire AI fallback to search: on zero results → Claude API call with `search-index.json` + query → returns 3 suggestions labeled "AI suggested — not a direct match"
- Focus management: open → focus first element; close → return to trigger; `Escape` dismisses
- `aria-live="polite"` on chat container; spinner `role="status"`
- **Done when:** Widget passes NVDA + keyboard test; AI fallback triggers correctly

**AI search call:**
```js
// Zero results → fetch /search-index.json → POST to Claude API
// Returns: { "results": [{ "title", "url", "reason" }] }  max 3 items, max_tokens: 600
```

---

## WEEK 5 — Content + Polish (~12 hrs)
- Fill stub pages: Color Contrast, ARIA Roles, Dyslexia Support, Inclusive Design (M-1)
- Add For Users / For Developers / Hot Topics to navbar (M-4)
- Enable `showLastUpdateTime` and difficulty level badges (L-1, L-4)
- Review content gaps auto-logged by chatbot as GitHub Issues
- **Done when:** Zero pages under 200 words; navbar covers all sections

---

## ONGOING — CI/CD (~6 hrs setup)
- Add `pa11y-ci` or `@axe-core/playwright` to GitHub Actions
- Block PRs introducing new WCAG AA violations
- Budget alert: $5/month on Claude API costs

---

## A11Y Requirements (apply to all new components)
- Search: `role="search"` on container, visible label, `aria-live="polite"` on results, document `⌘K` shortcut
- Widget: all interactive elements are `<button>`, not divs
- Export buttons: descriptive labels ("Copy guide as plain text", "Export guide as PDF")
- Zero-results: explicit text message, not empty container
- AI results: clearly labeled as AI suggestions

---

## Effort Summary
| Feature | Effort | Cost |
|---|---|---|
| Local search | ~3 hrs | Free |
| AI search fallback | ~8 hrs | ~$0.01/query |
| Search index generator | ~2 hrs | Free |
| /guide-me page | ~12 hrs | ~$0.02/session |
| Floating widget | ~6 hrs | Same API |
| Export (copy + PDF) | ~3 hrs | Free |
| Content gap logging | ~2 hrs | Free |
| CI/CD | ~6 hrs | Free |
