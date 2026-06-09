"""
flatmap_styles.py
Visual styling for the A11YHub flatmap generator.

Design (WCAG 1.4.1):
  - Shape  = primary non-color signal for status
  - Color  = redundant reinforcement (fill + border + text are coordinated per status)
  - Depth palette = structural signal for section/folder nodes only

Status → shape + border mapping (all labels quoted to safely handle parentheses):
  published  →  ["label"]     rectangle      solid border       green palette
  draft      →  [["label"]]   double-border  dotted border      amber palette
  wip        →  >"label"]     flag           dashed border      orange palette
  planned    →  ("label")     rounded        long-dashed border slate palette

Level → border dash + color (overrides status border when level tag is present):
  beginner     → dots      stroke-dasharray: 1 5   #b4dfc5
  intermediate → dash-dot  stroke-dasharray: 6 3 1 3  #b6c8f3
  advanced     → long-dash stroke-dasharray: 8 4   #dabef3
  expert       → solid     stroke-dasharray: 0     #f6c8a5
"""
from flatmap_frontmatter import evaluate_tag_condition

# ---------------------------------------------------------------------------
# STATUS_STYLES: unified shape + color per status.
# Matches the proposal chip colors so the visual language is consistent
# between mermaid nodes and Docusaurus tag chips on individual pages.
# (fill, border, text, dash, shape-template)
# ---------------------------------------------------------------------------
STATUS_STYLES = {
    #            fill       border     text       dash         shape-template
    'published': ('#e6f4ea', '#b4dfc5', '#205d3b', 'solid',     '["{label}"]'),
    'draft':     ('#FAEEDA', '#FAC775', '#78350f', 'dotted',    '[["{label}"]]'),
    'wip':       ('#fff0e6', '#f6c8a5', '#7c2d12', 'dashed',    '>"{label}"]'),
    'planned':   ('#f1f5f9', '#cbd5e1', '#1e293b', 'long-dash', '("{label}")'),
}

# Depth palette: (fill, text_color, border_color) for folder/section nodes.
# Uses the same pastel card palette as the landing page for visual consistency.
DEPTH_PALETTE = [
    ('#e6f4ea', '#205d3b', '#b4dfc5'),   # depth 0 — green  (brand primary)
    ('#e7f0fd', '#1e40af', '#b6c8f3'),   # depth 1 — blue
    ('#f3e8fd', '#5b21b6', '#dabef3'),   # depth 2 — purple
    ('#e6fffa', '#0f766e', '#99f6e4'),   # depth 3 — teal
    ('#f1f5f9', '#334155', '#cbd5e1'),   # depth 4+ — slate
]


def get_node_line(node_id, label, status):
    """Return a Mermaid node definition with shape encoding for status."""
    st = STATUS_STYLES.get(status)
    template = st[4] if st else '["{label}"]'
    return '{}{}'.format(node_id, template.format(label=label))


def inject_status_styles(styles, status):
    """
    Apply status-based fill, text-color, border-color, and border-dash to styles.
    Rule: status provides the defaults; tag config (level/type border colors) wins
    over status border color, but never over dash style (dash is the shape signal).
    """
    st = STATUS_STYLES.get(status)
    if not st:
        return styles
    fill, border, text, dash, _ = st
    styles = dict(styles)
    # Dash: status provides fallback; tag config (level) wins if already set
    if not styles.get('border_styles'):
        styles['border_styles'] = [dash]
    styles['border_widths'] = styles.get('border_widths') or ['2.5px']
    # Border color: tag config wins (level/type may override)
    if not styles.get('border_colors'):
        styles['border_colors'] = [border]
    # Fill: tag config background_color wins
    if not styles.get('background_colors'):
        styles['background_colors'] = [fill]
    # Text: tag config text_color wins
    if not styles.get('text_colors'):
        styles['text_colors'] = [text]
    return styles


def _empty_styles():
    return {
        'left_icons': [], 'right_icons': [],
        'border_colors': [], 'background_colors': [],
        'text_colors': [], 'border_styles': [], 'border_widths': [],
        'clickable': True, 'exclude': False,
    }


def apply_styling_to_node(tags, style_config, frontmatter=None):
    """Apply visual styling from the tag config to a node."""
    styles = _empty_styles()
    for config_tag, tag_properties in style_config.get('tags', {}).items():
        matched = (
            config_tag in tags
            or (' AND ' in config_tag and frontmatter
                and evaluate_tag_condition(config_tag, frontmatter))
        )
        if not matched:
            continue
        # Support both list-of-tuples [("key","val"), ...] and dict {"key":"val"} formats
        props = tag_properties if isinstance(tag_properties, list) else list(tag_properties.items())
        for prop_key, prop_value in props:
            if prop_key == 'icon':
                side = next((v for k, v in tag_properties if k == 'icon_side'), 'left')
                styles['right_icons' if side == 'right' else 'left_icons'].append(prop_value)
            elif prop_key == 'border_color':
                styles['border_colors'].append(prop_value)
            elif prop_key == 'background_color':
                styles['background_colors'].append(prop_value)
            elif prop_key == 'text_color':
                styles['text_colors'].append(prop_value)
            elif prop_key == 'border_style':
                styles['border_styles'].append(prop_value)
            elif prop_key == 'border_width':
                styles['border_widths'].append(prop_value)
            elif prop_key == 'exclude':
                styles['exclude'] = prop_value
    return styles


def create_mermaid_node_style(styles, default_fill=None, default_text_color=None, default_border_color=None):
    """Return a Mermaid classDef style string for a node."""
    parts = []
    fill = (styles.get('background_colors') or [None])[-1] or default_fill
    if fill:
        parts.append('fill:{}'.format(fill))
    border_colors = styles.get('border_colors', [])
    effective_border = border_colors[-1] if border_colors else default_border_color
    if effective_border:
        dash = {
            'dotted':    '1 4',
            'dots':      '1 5',
            'dashed':    '5 4',
            'dash-dot':  '6 3 1 3',
            'long-dash': '8 4',
        }.get((styles.get('border_styles') or ['solid'])[-1], '0')
        parts.append('stroke:{}'.format(effective_border))
        parts.append('stroke-width:{}'.format((styles.get('border_widths') or ['1.5px'])[-1]))
        parts.append('stroke-dasharray:{}'.format(dash))
    text = (styles.get('text_colors') or [None])[-1] or default_text_color
    if text:
        parts.append('color:{}'.format(text))
    return ','.join(parts) if parts else None


def create_mini_legend(legend_url=None):
    """
    Compact one-strip legend shown under every flatmap graph.
    Two rows: status (shape) and level (border pattern), four samples each.
    SVG presentation attributes only — no style= attributes (MDX/React SSR).
    Appends a link to the full legend page when legend_url is given.
    """
    W, H = 580, 78
    ROW1, ROW2 = 25, 57   # vertical centers of the two rows
    X0, STEP = 78, 127    # first item x, distance between items
    SW = 30               # swatch width

    status_items = [
        # (kind, fill, stroke, dasharray, label)
        ('rect',    '#e6f4ea', '#b4dfc5', '',    'Published'),
        ('double',  '#FAEEDA', '#FAC775', '1 4', 'Draft'),
        ('flag',    '#fff0e6', '#f6c8a5', '5 4', 'WIP'),
        ('rounded', '#f1f5f9', '#cbd5e1', '8 4', 'Planned'),
    ]
    level_items = [
        # (stroke, dasharray, label)
        ('#b4dfc5', '1 5',     'Beginner'),
        ('#b6c8f3', '6 3 1 3', 'Intermediate'),
        ('#dabef3', '8 4',     'Advanced'),
        ('#f6c8a5', '',        'Expert'),
    ]

    def _da(da):
        return ' stroke-dasharray="' + da + '"' if da else ''

    def _mini_shape(x, kind, fill, stroke, da):
        y, h = ROW1 - 8, 16
        d = _da(da)
        common = ' fill="' + fill + '" stroke="' + stroke + '" stroke-width="2"' + d + '/>'
        if kind == 'double':
            return (
                '<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(SW) + '" height="' + str(h) + '" rx="2"' + common
                + '<rect x="' + str(x + 3) + '" y="' + str(y + 3) + '" width="' + str(SW - 6) + '" height="' + str(h - 6) + '" rx="1" fill="none" stroke="' + stroke + '" stroke-width="1"' + d + '/>'
            )
        if kind == 'flag':
            pts = '{0},{1} {2},{1} {3},{4} {2},{5} {0},{5}'.format(
                x, y, x + SW - 6, x + SW, ROW1, y + h)
            return '<polygon points="' + pts + '"' + common
        rx = '8' if kind == 'rounded' else '2'
        return '<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(SW) + '" height="' + str(h) + '" rx="' + rx + '"' + common

    parts = [
        '<svg viewBox="0 0 ' + str(W) + ' ' + str(H) + '" xmlns="http://www.w3.org/2000/svg"'
        ' role="img" aria-label="Legend summary. Status is shown by node shape:'
        ' published is a rectangle, draft is a double border, work in progress is a flag,'
        ' planned is rounded. Level is shown by border pattern: beginner is dotted,'
        ' intermediate is dash-dot, advanced is long-dash, expert is solid.">',
        '<rect width="' + str(W) + '" height="' + str(H) + '" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>',
        '<text x="14" y="' + str(ROW1) + '" dominant-baseline="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="#0f172a">Status</text>',
        '<text x="14" y="' + str(ROW2) + '" dominant-baseline="middle" font-size="11" font-weight="bold" font-family="sans-serif" fill="#0f172a">Level</text>',
    ]
    for i, (kind, fill, stroke, da, label) in enumerate(status_items):
        x = X0 + i * STEP
        parts.append(_mini_shape(x, kind, fill, stroke, da))
        parts.append('<text x="' + str(x + SW + 8) + '" y="' + str(ROW1) + '" dominant-baseline="middle" font-size="11" font-family="sans-serif" fill="#334155">' + label + '</text>')
    for i, (stroke, da, label) in enumerate(level_items):
        x = X0 + i * STEP
        parts.append('<line x1="' + str(x) + '" y1="' + str(ROW2) + '" x2="' + str(x + SW) + '" y2="' + str(ROW2) + '" stroke="' + stroke + '" stroke-width="3"' + _da(da) + '/>')
        parts.append('<text x="' + str(x + SW + 8) + '" y="' + str(ROW2) + '" dominant-baseline="middle" font-size="11" font-family="sans-serif" fill="#334155">' + label + '</text>')
    parts.append('</svg>')

    out = ['', '\n'.join(parts)]
    if legend_url:
        out += ['', '<p class="flatmap-legend-link"><small><a href="' + legend_url + '">How to read this map — full legend</a></small></p>']
    return out


DEPTH_NAMES = ['Green', 'Blue', 'Purple', 'Teal', 'Slate']


def create_depth_legend():
    """
    SVG swatch strip + text table for the folder depth palette.
    Folder/section nodes use DEPTH_PALETTE colors to show hierarchy depth —
    this is separate from status (shape) and level (border pattern).
    Used only on the legend page. SVG presentation attributes only.
    """
    W, H = 580, 64
    X0, STEP, SW, SH = 16, 112, 96, 30
    Y = (H - SH) // 2

    aria = ('Folder color samples by depth: '
            + ', '.join('depth {} {}'.format(i if i < 4 else '4 and deeper', n.lower())
                        for i, n in enumerate(DEPTH_NAMES)) + '.')
    parts = [
        '<svg viewBox="0 0 ' + str(W) + ' ' + str(H) + '" xmlns="http://www.w3.org/2000/svg"'
        ' role="img" aria-label="' + aria + '">',
        '<rect width="' + str(W) + '" height="' + str(H) + '" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>',
    ]
    for i, (fill, text, border) in enumerate(DEPTH_PALETTE):
        x = X0 + i * STEP
        label = 'Depth {}'.format(i) if i < 4 else 'Depth 4+'
        parts.append('<rect x="' + str(x) + '" y="' + str(Y) + '" width="' + str(SW) + '" height="' + str(SH) + '" rx="3" fill="' + fill + '" stroke="' + border + '" stroke-width="1.5"/>')
        parts.append('<text x="' + str(x + SW // 2) + '" y="' + str(Y + SH // 2) + '" text-anchor="middle" dominant-baseline="middle" font-size="11" font-family="sans-serif" fill="' + text + '">' + label + '</text>')
    parts.append('</svg>')

    table = ['', '| Depth | Color | Background |', '|---|---|---|']
    for i, ((fill, _t, _b), name) in enumerate(zip(DEPTH_PALETTE, DEPTH_NAMES)):
        depth = '0 (home)' if i == 0 else ('4+' if i == 4 else str(i))
        table.append('| {} | {} | `{}` |'.format(depth, name, fill))
    return ['', '\n'.join(parts)] + table


def create_full_legend():
    """
    Full visual legend rendered as a single inline SVG.
    Used only on the dedicated legend page (docs/00-about/legend.md).
    SVG presentation attributes (fill, stroke, stroke-width, etc.) are used
    throughout — no style= attributes — so MDX/React SSR does not reject it.
    """
    W      = 580
    ROW_H  = 48
    HDR_H  = 28
    GAP    = 16
    PAD    = 16
    SX     = 20   # shape column x
    LX     = 155  # label column x
    DX     = 345  # description column x

    y_sh = PAD
    y_sr = y_sh + HDR_H
    y_lh = y_sr + 4 * ROW_H + GAP
    y_lr = y_lh + HDR_H
    H    = y_lr + 4 * ROW_H + PAD

    def _da(da):
        return ' stroke-dasharray="' + da + '"' if da else ''

    def _shape_els(kind, fill, stroke, da):
        d = _da(da)
        if kind == 'rounded':
            return '<rect x="3" y="3" width="114" height="32" rx="19" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2.5"' + d + '/>'
        if kind == 'double':
            return (
                '<rect x="3" y="3" width="114" height="32" rx="2" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2"' + d + '/>'
                '<rect x="7" y="7" width="106" height="24" rx="1" fill="none" stroke="' + stroke + '" stroke-width="1.5"' + d + '/>'
            )
        if kind == 'flag':
            return '<polygon points="3,3 109,3 118,19 109,35 3,35" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2.5"' + d + '/>'
        # default: rect
        return '<rect x="3" y="3" width="114" height="32" rx="3" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2.5"' + d + '/>'

    def _row_els(y_top, kind, fill, stroke, da, ptext, tc, label, desc, sep):
        tx = 56 if kind == 'flag' else 60
        mid = y_top + ROW_H // 2
        out = [
            '<g transform="translate(' + str(SX) + ',' + str(y_top + 5) + ')">',
            _shape_els(kind, fill, stroke, da),
            '<text x="' + str(tx) + '" y="19" text-anchor="middle" dominant-baseline="middle" font-size="11" font-family="sans-serif" fill="' + tc + '">' + ptext + '</text>',
            '</g>',
            '<text x="' + str(LX) + '" y="' + str(mid) + '" dominant-baseline="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="#1e293b">' + label + '</text>',
            '<text x="' + str(DX) + '" y="' + str(mid) + '" dominant-baseline="middle" font-size="12" font-family="sans-serif" fill="#64748b">' + desc + '</text>',
        ]
        if sep:
            out.append('<line x1="' + str(SX) + '" y1="' + str(y_top + ROW_H) + '" x2="' + str(W - SX) + '" y2="' + str(y_top + ROW_H) + '" stroke="#f1f5f9" stroke-width="1"/>')
        return '\n'.join(out)

    status_data = [
        ('rounded', '#f1f5f9', '#cbd5e1', '8 4',  'title', '#1e293b', 'Planned',          'rounded · long-dash'),
        ('flag',    '#fff0e6', '#f6c8a5', '5 4',  'title', '#7c2d12', 'Work in progress', 'flag · dashed'),
        ('double',  '#FAEEDA', '#FAC775', '1 4',  'title', '#78350f', 'Draft',            'double-border · dotted'),
        ('rect',    '#e6f4ea', '#b4dfc5', '',     'title', '#205d3b', 'Published',        'rectangle · solid'),
    ]
    level_data = [
        ('rect', '#f8fafc', '#b4dfc5', '1 5',     'dots',     '#334155', 'Beginner',     'dotted (1,5)'),
        ('rect', '#f8fafc', '#b6c8f3', '6 3 1 3', 'dash-dot', '#334155', 'Intermediate', 'dash-dot (6,3,1,3)'),
        ('rect', '#f8fafc', '#dabef3', '8 4',     'dash',     '#334155', 'Advanced',     'long-dash (8,4)'),
        ('rect', '#f8fafc', '#f6c8a5', '',        'solid',    '#334155', 'Expert',       'solid'),
    ]

    parts = [
        '<svg viewBox="0 0 ' + str(W) + ' ' + str(H) + '" xmlns="http://www.w3.org/2000/svg"'
        ' role="img" aria-label="Flatmap legend: status shapes and level border patterns">',
        '<rect width="' + str(W) + '" height="' + str(H) + '" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>',
        '<text x="' + str(SX) + '" y="' + str(y_sh + HDR_H // 2) + '" dominant-baseline="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="#0f172a">Status — read the shape</text>',
    ]
    for i, row in enumerate(status_data):
        kind, fill, stroke, da, ptext, tc, label, desc = row
        parts.append(_row_els(y_sr + i * ROW_H, kind, fill, stroke, da, ptext, tc, label, desc, sep=(i < 3)))

    parts.append('<text x="' + str(SX) + '" y="' + str(y_lh + HDR_H // 2) + '" dominant-baseline="middle" font-size="13" font-weight="bold" font-family="sans-serif" fill="#0f172a">Level — read the border pattern</text>')
    for i, row in enumerate(level_data):
        kind, fill, stroke, da, ptext, tc, label, desc = row
        parts.append(_row_els(y_lr + i * ROW_H, kind, fill, stroke, da, ptext, tc, label, desc, sep=(i < 3)))

    parts.append('</svg>')
    return ['', '\n'.join(parts)]
