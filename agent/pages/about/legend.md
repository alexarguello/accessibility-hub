# Map Legend

## Map Legend

Every section page shows a clickable map of its content. Each node
encodes three pieces of information:

- **Status** — the *shape* of the node shows how finished the page is.
- **Level** — the *border pattern* shows the expected experience level.
- **Folder depth** — the *background color* of folder nodes shows how
  deep that section sits in the site hierarchy.

Color reinforces both signals but is never the only carrier (WCAG 1.4.1).
A text navigation alternative is provided above every map for screen
reader and no-JavaScript users.

### Status — read the shape

| Status | Shape | Border | Meaning |
|---|---|---|---|
| Published | Rectangle | Solid | Reviewed and complete |
| Draft | Double border | Dotted | Written, awaiting review |
| Work in progress | Flag | Dashed | Actively being written |
| Planned | Rounded | Long-dash | Stub — content to come |

### Level — read the border pattern

| Level | Border pattern | Border color | Meaning |
|---|---|---|---|
| Beginner | Dots (1 5) | Green `#b4dfc5` | No prior knowledge needed |
| Intermediate | Dash-dot (6 3 1 3) | Blue `#b6c8f3` | Basic accessibility knowledge assumed |
| Advanced | Long-dash (8 4) | Purple `#dabef3` | Deep technical content |
| Expert | Solid | Orange `#f6c8a5` | Specialist topics |

### Folder colors — depth in the hierarchy

Folder (section) nodes are always rectangles and use a separate
background palette that shows how deep the section sits in the site
structure. Folder color does not encode status or level.

| Depth | Color | Background |
|---|---|---|
| 0 (home) | Green | `#e6f4ea` |
| 1 | Blue | `#e7f0fd` |
| 2 | Purple | `#f3e8fd` |
| 3 | Teal | `#e6fffa` |
| 4+ | Slate | `#f1f5f9` |

### When a page has both

The level border pattern takes priority over the status border.
The shape still tells you the status, so both signals stay readable.

Source: https://alexarguello.github.io/accessibility-hub/docs/about/legend/
