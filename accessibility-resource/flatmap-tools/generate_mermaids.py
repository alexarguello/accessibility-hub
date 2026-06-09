"""
generate_mermaids.py
Entry point for the A11YHub flatmap generator.
Walks the docs tree and writes auto-generated index.md files for each section.

Run from accessibility-resource/flatmap-tools/:
    python generate_mermaids.py
"""
import os

from util import get_docs_root_dir, load_style_config, get_docs_url
from flatmap_frontmatter import parse_frontmatter, extract_tags_from_frontmatter
from flatmap_styles import (
    DEPTH_PALETTE,
    STATUS_STYLES,
    apply_styling_to_node,
    create_mermaid_node_style,
    create_compact_legend,
    get_node_line,
    inject_status_styles,
)
from flatmap_nodes import (
    strip_order_prefix,
    normalize_id,
    extract_title,
    create_node_label,
    get_folder_sidebar_position,
    is_external_doc,
    build_text_nav,
)

ROOT_DIR = get_docs_root_dir()
DO_NOT_EDIT = "<!-- AUTO-GENERATED FILE — DO NOT EDIT. Regenerated on merge -->"


def get_max_depth():
    return load_style_config().get("flatmap_depth", 4)


def _build_class_lines(classes, style_classes, max_depth):
    """Generate Mermaid classDef + class assignment lines."""
    out = []
    for d in range(max_depth + 1):
        fill, text, border = DEPTH_PALETTE[d % len(DEPTH_PALETTE)]
        out.append("classDef col{} fill:{},stroke:{},stroke-width:1.5px,color:{};".format(d, fill, border, text))
    for nid, col in classes.items():
        if nid not in style_classes:
            out.append("class {} col{};".format(nid, col))
    for i, (nid, style) in enumerate(style_classes.items()):
        out.append("classDef custom{} {};".format(i, style))
        out.append("class {} custom{};".format(nid, i))
    return out


def _mermaid_block(lines, clicks, class_lines):
    return (
            ["```mermaid", "graph LR"]
            + lines + clicks + class_lines
            + ["linkStyle default interpolate basis", "```"]
    )


def build_mermaid(folder_path, rel_path, depth, parent_id=None,
                  max_depth_override=None, style_config=None):
    if style_config is None:
        style_config = load_style_config()

    lines, clicks, classes, style_classes = [], [], {}, {}
    current_id = normalize_id(rel_path or "root")
    label = strip_order_prefix(os.path.basename(folder_path)).replace("-", " ").title() or "Home"

    # --- Folder node (structural — always uses depth palette, never status colors) ---
    index_md = os.path.join(folder_path, "index.md")
    intro_md = os.path.join(folder_path, "_intro.md")
    folder_fm = {}
    folder_styles = {
        'left_icons': [], 'right_icons': [], 'border_colors': [],
        'background_colors': [], 'text_colors': [], 'border_styles': [],
        'border_widths': [], 'clickable': True, 'exclude': False,
    }
    for candidate in (index_md, intro_md):
        if os.path.isfile(candidate):
            folder_fm = parse_frontmatter(candidate)
            folder_styles = apply_styling_to_node(
                extract_tags_from_frontmatter(folder_fm), style_config, folder_fm
            )
            break

    if folder_styles['exclude']:
        return lines, clicks, classes, style_classes

    node_label = create_node_label(label, folder_styles)
    # Folder nodes always use rectangle — they are navigation structure, not content
    lines.append('{}["{}"]'.format(current_id, node_label))

    if rel_path:
        clean = "/".join(strip_order_prefix(p) for p in rel_path.split(os.sep))
        clicks.append('click {} "{}"'.format(current_id, get_docs_url(clean)))
    if parent_id:
        lines.append("{} --> {}".format(parent_id, current_id))

    # Folder styling: depth palette only (tag config border may apply, but no status fill)
    d_fill, d_text, d_border = DEPTH_PALETTE[depth % len(DEPTH_PALETTE)]
    style = create_mermaid_node_style(folder_styles, default_fill=d_fill, default_text_color=d_text, default_border_color=d_border)
    if style:
        style_classes[current_id] = style

    # --- Children ---
    effective_max = max_depth_override if max_depth_override is not None else get_max_depth()
    if depth >= effective_max:
        classes[current_id] = depth
        return lines, clicks, classes, style_classes

    entries = [e for e in sorted(os.listdir(folder_path)) if e != '99-contribute']
    combined = []
    for e in entries:
        full = os.path.join(folder_path, e)
        if os.path.isdir(full):
            combined.append((e, True, get_folder_sidebar_position(full)))
        elif e.endswith('.md') and e not in ("index.md", "_intro.md") and not e.startswith('.'):
            fm = parse_frontmatter(full)
            try:
                pos = float(fm.get('sidebar_position', float('inf')))
            except (TypeError, ValueError):
                pos = float('inf')
            combined.append((e, False, pos))
    combined.sort(key=lambda x: (x[2], x[0]))

    for name, is_dir, _ in combined:
        full = os.path.join(folder_path, name)
        entry_rel = os.path.join(rel_path, name) if rel_path else name

        if is_dir:
            sl, sc, scl, ssc = build_mermaid(
                full, entry_rel, depth + 1, current_id, max_depth_override, style_config
            )
            lines.extend(sl); clicks.extend(sc)
            classes.update(scl); style_classes.update(ssc)
        else:
            title = extract_title(full)
            node_id = normalize_id(entry_rel)
            external, ext_url = is_external_doc(full)
            fm = parse_frontmatter(full)
            node_styles = apply_styling_to_node(
                extract_tags_from_frontmatter(fm), style_config, fm
            )
            if node_styles['exclude']:
                continue

            # Leaf nodes: shape + fill + text + border-dash from status
            status = fm.get('status', 'published')
            node_styles = inject_status_styles(node_styles, status)

            node_label = create_node_label(title, node_styles, external, ext_url)
            lines.append(get_node_line(node_id, node_label, status))

            if node_styles['clickable'] and not external:
                clean = get_docs_url("/".join(
                    strip_order_prefix(p)
                    for p in entry_rel.replace(".md", "").split(os.sep)
                ))
                clicks.append('click {} "{}"'.format(node_id, clean))
            lines.append("{} --> {}".format(current_id, node_id))

            # Leaf style: status fill/text/border are already in node_styles;
            # depth palette provides fallback fill/text if status was unrecognized
            lf, lt, lb = DEPTH_PALETTE[(depth + 1) % len(DEPTH_PALETTE)]
            style = create_mermaid_node_style(node_styles, default_fill=lf, default_text_color=lt)
            if style:
                style_classes[node_id] = style
            classes[node_id] = depth + 1

    classes[current_id] = depth
    return lines, clicks, classes, style_classes


def split_frontmatter_and_body(md_content):
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            return '---' + parts[1] + '---', parts[2].lstrip('\n')
    return '', md_content


def generate_index_md(folder_path, rel_path):
    folder_name  = os.path.basename(folder_path)
    human_title  = strip_order_prefix(folder_name).replace("-", " ").title() or "Home"
    frontmatter  = "---\ntitle: {}\nhide_title: true\n---".format(human_title)
    intro_path   = os.path.join(folder_path, "_intro.md")
    style_config = load_style_config()

    lines, clicks, classes, style_classes = build_mermaid(
        folder_path, rel_path, depth=0, style_config=style_config
    )
    class_lines = _build_class_lines(classes, style_classes, get_max_depth())
    custom_intro = [
        "### {}".format(human_title),
        '<p class="margin-top-negative"><em>Click any block below to navigate directly to that section.</em></p>',
        "",
    ]

    output = []
    if os.path.isfile(intro_path):
        with open(intro_path, "r", encoding="utf-8") as f:
            fm, body = split_frontmatter_and_body(f.read().strip())
        output += [fm, body, "## What's in this chapter?"] + custom_intro
    else:
        output += [frontmatter, DO_NOT_EDIT] + custom_intro

    text_nav = build_text_nav(lines, clicks)
    if text_nav:
        output.extend(text_nav)

    output += _mermaid_block(lines, clicks, class_lines)
    output += create_compact_legend(style_classes, style_config)

    with open(os.path.join(folder_path, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Wrote: {}".format(os.path.join(folder_path, "index.md")))


def generate_root_index_md():
    frontmatter = (
        "---\nsidebar_position: 1\ntitle: Site Overview\nhide_title: true\n---"
    )
    custom_intro = [
        "### Welcome",
        "<small>Here's an overview of the first layers of this resource. "
        "Simply click on the boxes to get directly to your article of choice, "
        "or use the sidebar to navigate.</small>",
        "",
    ]
    style_config = load_style_config()
    lines, clicks, classes, style_classes = build_mermaid(ROOT_DIR, '', depth=0)
    class_lines = _build_class_lines(classes, style_classes, get_max_depth())

    output = [frontmatter, DO_NOT_EDIT, ""]

    text_nav = build_text_nav(lines, clicks)
    if text_nav:
        output.extend(text_nav)

    output += custom_intro + _mermaid_block(lines, clicks, class_lines)
    output += create_compact_legend(style_classes, style_config)

    path = os.path.join(ROOT_DIR, "index.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Wrote root flatmap: {}".format(path))


def generate_full_sitemap():
    frontmatter = (
        "---\ntitle: Full Site Map\nsidebar_label: Full Site Map\n"
        "sidebar_position: 2\nhide_title: true\n---"
    )
    custom_intro = [
        "### Full Site Map",
        "<small>Complete overview of all content in this resource. "
        "This map shows everything at maximum depth - it's quite detailed!</small>",
        "",
    ]
    style_config = load_style_config()
    lines, clicks, classes, style_classes = build_mermaid(
        ROOT_DIR, '', depth=0, max_depth_override=10
    )
    class_lines = _build_class_lines(classes, style_classes, 10)

    output = [frontmatter, DO_NOT_EDIT, ""]

    text_nav = build_text_nav(lines, clicks)
    if text_nav:
        output.extend(text_nav)

    output += custom_intro + _mermaid_block(lines, clicks, class_lines)
    output += create_compact_legend(style_classes, style_config)

    path = os.path.join(ROOT_DIR, "full-sitemap.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print("Wrote full sitemap: {}".format(path))


def walk_folders():
    for root, dirs, files in os.walk(ROOT_DIR):
        if '99-contribute' in dirs:
            dirs.remove('99-contribute')
        if [f for f in files if f.endswith('.md')] or dirs:
            rel = os.path.relpath(root, ROOT_DIR)
            generate_index_md(root, "" if rel == "." else rel)
    generate_root_index_md()
    generate_full_sitemap()


walk_folders()