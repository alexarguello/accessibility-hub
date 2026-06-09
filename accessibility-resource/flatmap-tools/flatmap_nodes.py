"""
flatmap_nodes.py
Node ID, label, file utilities, and the accessible text-nav fallback
for the A11YHub flatmap generator.
"""
import os
import re
import unicodedata

from flatmap_frontmatter import parse_frontmatter


def _strip_emojis(text):
    """Remove emoji/pictographic symbols — accessibility: no emoji in node labels."""
    if not isinstance(text, str):
        return text
    pattern = re.compile(
        r'[\U0001F600-\U0001F64F'
        r'\U0001F300-\U0001F5FF'
        r'\U0001F680-\U0001F6FF'
        r'\U0001F700-\U0001FAFF'
        r'\U00002600-\U000027BF'
        r'\U0000FE00-\U0000FE0F'
        r'\U0001F1E6-\U0001F1FF'
        r'\U0000200D]+'
    )
    return pattern.sub('', text)


def strip_order_prefix(name):
    """Remove numeric ordering prefix, e.g. '01-' from '01-intro'."""
    return re.sub(r'^\d{2,}-', '', name)


def normalize_id(path):
    """Sanitize a path into a valid Mermaid node ID (a-z A-Z 0-9 _ only)."""
    raw = unicodedata.normalize('NFKD', path).encode('ascii', 'ignore').decode('ascii')
    raw = raw.replace('/', '_').replace('-', '_').replace('.', '_')
    raw = re.sub(r'[^a-zA-Z0-9_]', '_', raw)
    raw = re.sub(r'^[_\d]+', '', raw)
    return raw or 'node'


def extract_title(path):
    """Extract display title from frontmatter title:, first H1, or filename."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if m:
                for line in m.group(1).split('\n'):
                    if line.strip().startswith('title:'):
                        t = line.split(':', 1)[1].strip().strip('"').strip("'")
                        if t:
                            return t
        for line in content.splitlines():
            if line.strip().startswith('# '):
                return line.strip().lstrip('# ').strip()
    except Exception:
        pass
    return os.path.basename(path).replace('.md', '')


def create_node_label(title, styles, is_external=False, external_url=None):
    """
    Build the display label for a Mermaid node.
    Sanitizes quotes/brackets/newlines; strips emojis for accessibility.
    """
    parts = list(styles.get('left_icons', []))
    safe = title.replace('"', "'").replace('\n', ' ').replace('\r', ' ')
    safe = safe.replace('[', '(').replace(']', ')')
    if len(safe) > 80:
        safe = safe[:77] + '...'
    parts.append(safe)
    parts.extend(styles.get('right_icons', []))
    label = _strip_emojis(' '.join(parts)).strip()
    if is_external and external_url:
        return "<a href='{}' target='_blank' rel='noopener noreferrer'>{}</a>".format(
            external_url, label
        )
    return label


def get_folder_sidebar_position(folder_path):
    """Read sidebar_position from _intro.md, or return infinity."""
    intro = os.path.join(folder_path, '_intro.md')
    if os.path.isfile(intro):
        fm = parse_frontmatter(intro)
        try:
            return float(fm.get('sidebar_position', float('inf')))
        except (TypeError, ValueError):
            pass
    return float('inf')


def has_author_and_draft(frontmatter):
    """Return True if the doc has a non-empty author and status == 'draft'."""
    return (
        frontmatter.get('status') == 'draft'
        and isinstance(frontmatter.get('author', ''), str)
        and frontmatter['author'].strip()
    )


def is_external_doc(path):
    """Return (True, url) when a doc is marked type: external with a link: field."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not re.search(r'^type:\s*external\s*$', content, re.MULTILINE):
            return False, None
        m = re.search(r'^link:\s*(\S+)', content, re.MULTILINE)
        return True, (m.group(1) if m else None)
    except Exception:
        return False, None


def build_text_nav(lines, clicks):
    """Accessible <details> text-navigation fallback for the mermaid diagram.

    Parses node labels and click URLs produced by build_mermaid() and emits a
    <details> block that works without JavaScript and is fully keyboard/SR
    accessible. Satisfies WCAG 1.3.1 for mermaid-only navigation pages.

    Handles all current Mermaid shape syntaxes:
      node["label"]      rectangle  (published)
      node("label")      rounded    (draft)
      node[/"label"/]    parallelogram (wip)
      node{"label"}      rhombus    (planned)
    And external nodes whose label contains an <a href='url'>Title</a>.
    """
    node_labels = {}
    node_external_urls = {}

    for line in lines:
        line = line.strip()
        # Extract node ID (leading word chars)
        id_match = re.match(r'^(\w+)', line)
        if not id_match:
            continue
        nid = id_match.group(1)
        # Find label content between the first and last double-quote on this line
        first_q = line.find('"')
        last_q  = line.rfind('"')
        if first_q == -1 or last_q <= first_q:
            continue
        raw = line[first_q + 1:last_q]
        # Check for an external href embedded in the label
        ext = re.search(r"href='([^']+)'", raw)
        if ext:
            node_external_urls[nid] = ext.group(1)
        label = re.sub(r'<[^>]+>', '', raw).strip()
        if label:
            node_labels[nid] = label

    # Parse click URLs: click node_id "url"
    node_urls = {}
    for click in clicks:
        m = re.match(r'^click (\w+) "(.+)"$', click.strip())
        if m:
            node_urls[m.group(1)] = m.group(2)

    items = []
    for nid, label in node_labels.items():
        if nid in node_urls:
            items.append('  <li><a href="{}">{}</a></li>'.format(node_urls[nid], label))
        elif nid in node_external_urls:
            items.append(
                '  <li><a href="{}" target="_blank" rel="noopener noreferrer">{} &#8599;</a></li>'.format(
                    node_external_urls[nid], label
                )
            )

    if not items:
        return []

    return [
        '',
        '<details class="flatmap-text-nav">',
        '<summary>Text navigation (no-JS / screen reader alternative)</summary>',
        '<ul>',
    ] + items + [
        '</ul>',
        '</details>',
    ]
