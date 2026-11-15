"""
generate_site_index.py
Builds a machine-readable index of the published docs for the site agent
and for external AI agents.

Outputs (all under static/, all generated, none committed):
  static/agent/site-index.json   one entry per page: url, title, description,
                                 section, audience, tags, headings, word count
  static/agent/pages/<path>.md   the page as plain markdown, links made absolute
  static/llms.txt                llms.txt overview that links to the .md files

Run from the accessibility-resource folder, after generate_mermaids.py:
  python flatmap-tools/generate_site_index.py

Standard library only. Output is deterministic: the same docs give the same bytes.
"""
import json
import os
import re
import shutil
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(TOOLS_DIR)
DOCS_DIR = os.path.join(SITE_DIR, "docs")
STATIC_DIR = os.path.join(SITE_DIR, "static")
AGENT_DIR = os.path.join(STATIC_DIR, "agent")
PAGES_DIR = os.path.join(AGENT_DIR, "pages")
CONFIG_PATH = os.path.join(SITE_DIR, "docusaurus.config.js")

# Contributor scaffolding that is generated per page; not useful to site visitors.
EXCLUDED_TOP_FOLDERS = {"99-contribute"}
EXCERPT_CHARS = 280
LIST_FIELDS = ("audience", "disability_type", "tags", "topics")

ORDER_PREFIX = re.compile(r"^\d+[-_.]\s*")


# ---------------------------------------------------------------- config

def read_site_config():
    """Return (site_url, base_url) from docusaurus.config.js, without trailing slashes."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    url = re.search(r"^\s*url:\s*['\"]([^'\"]+)['\"]", text, re.MULTILINE)
    base = re.search(r"baseUrl:\s*['\"]([^'\"]*)['\"]", text)
    site_url = url.group(1).rstrip("/") if url else ""
    base_url = base.group(1).rstrip("/") if base else ""
    return site_url, base_url


# ----------------------------------------------------------- frontmatter

def _clean_scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    # Unquoted value: drop a trailing YAML comment.
    return re.sub(r"\s+#.*$", "", value).strip()


def split_frontmatter(text):
    """Return (frontmatter dict, body). Handles scalars, [inline, lists] and block lists."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    match = re.match(r"^---\n(.*?)\n---[ \t]*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    data = {}
    current_list_key = None
    for raw in match.group(1).split("\n"):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_list_key and raw[0] in " \t-":
            data[current_list_key].append(_clean_scalar(stripped[2:]))
            continue
        key_match = re.match(r"^([A-Za-z_][\w-]*):(.*)$", raw)
        if not key_match:
            continue
        key, value = key_match.group(1), key_match.group(2).strip()
        current_list_key = None
        if value == "":
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_clean_scalar(v) for v in inner.split(",")] if inner else []
        else:
            data[key] = _clean_scalar(value)
    return data, text[match.end():]


def as_list(value):
    if isinstance(value, list):
        return [v for v in value if v]
    if isinstance(value, str) and value:
        return [value]
    return []


def as_text(value):
    """Scalar frontmatter value as text; an empty block list means the key was blank."""
    return value if isinstance(value, str) else ""


# ------------------------------------------------------------------ urls

def doc_route(rel_path):
    """docs-relative file path -> route under /docs, the way Docusaurus builds it."""
    parts = rel_path.replace("\\", "/").split("/")
    parts[-1] = re.sub(r"\.mdx?$", "", parts[-1])
    parts = [ORDER_PREFIX.sub("", p) for p in parts]
    if parts[-1].lower() in ("index", "readme"):
        parts.pop()
    return "/".join(parts)


def route_to_url(base_url, route):
    return f"{base_url}/docs/{route}/" if route else f"{base_url}/docs/"


# ------------------------------------------------------------------ body

FENCE = re.compile(r"^(```|~~~)")


# Lines the flatmap generator adds to every section page; noise for a reader with no graph.
BOILERPLATE = (
    "Click any block below to navigate directly to that section.",
)
TEXT_NAV_SUMMARY = "Text navigation (no-JS / screen reader alternative)"


def split_fences(body):
    """Split a body into (is_code, text) segments. Mermaid fences are dropped."""
    segments, buffer, fence_lines = [], [], None
    for line in body.split("\n"):
        stripped = line.strip()
        if fence_lines is None:
            if FENCE.match(stripped):
                segments.append((False, "\n".join(buffer)))
                buffer, fence_lines = [], [line]
            else:
                buffer.append(line)
        else:
            fence_lines.append(line)
            if FENCE.match(stripped):
                if not fence_lines[0].strip()[3:].strip().lower().startswith("mermaid"):
                    segments.append((True, "\n".join(fence_lines)))
                fence_lines = None
    if fence_lines is not None:
        segments.append((True, "\n".join(fence_lines)))
    segments.append((False, "\n".join(buffer)))
    return segments


def clean_prose(text, fix_link):
    """Strip markup from text outside code fences. Inline code spans are left untouched."""
    spans = []

    def stash(match):
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`[^`\n]+`", stash, text)

    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"<svg\b.*?</svg>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style\b.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"^(import|export)\s.*$", "", text, flags=re.MULTILINE)

    # HTML links and list items become markdown so the link targets survive.
    text = re.sub(r"<a\b[^>]*?href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", r"[\2](\1)", text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"^[ \t]*<li[^>]*>", "- ", text, flags=re.MULTILINE | re.IGNORECASE)
    # <summary> is the only label a <details> block has; keep it as its own line.
    text = re.sub(r"<summary[^>]*>(.*?)</summary>", r"\n\1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    # Every other tag (HTML or JSX component) is dropped; its text stays.
    text = re.sub(r"</?[A-Za-z][^>\n]*>", "", text)

    for phrase in BOILERPLATE:
        text = text.replace(phrase, "")
    text = text.replace(TEXT_NAV_SUMMARY, "Pages in this section:")

    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", fix_link, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def clean_body(body, rel_path, routes_by_file, site_url, base_url):
    """Markdown/MDX body -> plain markdown an LLM can read. Drops diagrams and markup."""

    def fix_link(match):
        label, target = match.group(1), match.group(2).strip()
        return f"[{label}]({resolve_link(target, rel_path, routes_by_file, site_url, base_url)})"

    parts = [text if is_code else clean_prose(text, fix_link)
             for is_code, text in split_fences(body)]
    text = "\n".join(parts)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def resolve_link(target, rel_path, routes_by_file, site_url, base_url):
    """Turn relative .md links and site-absolute links into full URLs. Leave the rest."""
    if re.match(r"^(https?:|mailto:|tel:|#)", target):
        return target
    path, _, anchor = target.partition("#")
    anchor = f"#{anchor}" if anchor else ""
    if path.startswith("/"):
        if base_url and not path.startswith(base_url + "/") and path != base_url:
            path = base_url + path
        # Doc routes end in a slash on the live site; add it so links match the index.
        if "/docs" in path and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
            path += "/"
        return f"{site_url}{path}{anchor}"
    if re.search(r"\.mdx?$", path):
        base_dir = os.path.dirname(rel_path.replace("\\", "/"))
        joined = os.path.normpath(os.path.join(base_dir, path)).replace("\\", "/")
        route = routes_by_file.get(joined)
        if route is not None:
            return f"{site_url}{route_to_url(base_url, route)}{anchor}"
    return target


def first_h1(text):
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def headings(text):
    """H2 and H3 headings outside code fences, markdown formatting removed."""
    found, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{2,3})\s+(.+?)\s*#*$", line)
        if match:
            found.append(plain(match.group(2)))
    return found


def plain(text):
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def excerpt(text):
    """First real paragraph of prose, for pages with no frontmatter description."""
    in_fence = False
    paragraph = []
    for line in text.split("\n"):
        stripped = line.strip()
        if FENCE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        is_prose = (stripped and stripped != "Pages in this section:"
                    and not re.match(r"^(#|\||[-*+]\s|\d+\.\s|>|:::|---)", stripped))
        if is_prose:
            paragraph.append(stripped)
        elif paragraph:
            break
    result = plain(" ".join(paragraph))
    if len(result) > EXCERPT_CHARS:
        result = result[:EXCERPT_CHARS].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    return result


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9][\w'-]*", text))


# ------------------------------------------------------------------ main

def collect_files():
    files = []
    for root, dirs, names in os.walk(DOCS_DIR):
        dirs.sort()
        rel_root = os.path.relpath(root, DOCS_DIR).replace("\\", "/")
        top = rel_root.split("/")[0]
        if top in EXCLUDED_TOP_FOLDERS:
            dirs[:] = []
            continue
        for name in sorted(names):
            # Docusaurus ignores files that start with _ ; dot files are templates.
            if name.startswith(("_", ".")) or not re.search(r"\.mdx?$", name):
                continue
            rel = name if rel_root == "." else f"{rel_root}/{name}"
            files.append(rel)
    return files


def section_titles(rel_path, titles_by_route):
    """Titles of the parent sections, outermost first."""
    parts = doc_route(rel_path).split("/")[:-1] if doc_route(rel_path) else []
    names = []
    for depth in range(1, len(parts) + 1):
        route = "/".join(parts[:depth])
        names.append(titles_by_route.get(route) or parts[depth - 1].replace("-", " ").title())
    return names


def main():
    site_url, base_url = read_site_config()
    files = collect_files()

    parsed = {}
    for rel in files:
        with open(os.path.join(DOCS_DIR, rel), "r", encoding="utf-8") as f:
            front, body = split_frontmatter(f.read())
        if str(front.get("draft", "")).lower() == "true" or str(front.get("unlisted", "")).lower() == "true":
            continue
        parsed[rel] = (front, body)

    routes_by_file = {rel: doc_route(rel) for rel in parsed}
    titles_by_route = {}
    for rel, (front, body) in parsed.items():
        title = as_text(front.get("title")) or first_h1(body) or os.path.basename(rel)
        titles_by_route[routes_by_file[rel]] = plain(title)

    if os.path.isdir(AGENT_DIR):
        shutil.rmtree(AGENT_DIR)
    os.makedirs(PAGES_DIR)

    pages, missing_description = [], []
    for rel in sorted(parsed, key=lambda r: routes_by_file[r]):
        front, body = parsed[rel]
        route = routes_by_file[rel]
        title = titles_by_route[route]
        text = clean_body(body, rel, routes_by_file, site_url, base_url)
        description = plain(as_text(front.get("description")))
        description_source = "frontmatter"
        if not description:
            description = excerpt(re.sub(r"^#\s+.+$", "", text, count=1, flags=re.MULTILINE))
            description_source = "excerpt" if description else "none"
            missing_description.append(rel)

        page_file = f"{route or 'index'}.md"
        page_path = os.path.join(PAGES_DIR, *page_file.split("/"))
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        url = f"{site_url}{route_to_url(base_url, route)}"
        page_text = text if first_h1(text) else f"# {title}\n\n{text}"
        with open(page_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{page_text.strip()}\n\nSource: {url}\n")

        entry = {
            "url": url,
            "path": route_to_url(base_url, route),
            "text": f"{base_url}/agent/pages/{page_file}",
            "title": title,
            "section": section_titles(rel, titles_by_route),
            "description": description,
            "description_source": description_source,
            "level": as_text(front.get("level")),
            "type": as_text(front.get("type")),
            "status": as_text(front.get("status")),
            "content_status": as_text(front.get("content_status")),
            "headings": headings(text),
            "words": word_count(text),
        }
        for field in LIST_FIELDS:
            entry[field] = as_list(front.get(field))
        pages.append(entry)

    index = {"site": site_url + base_url + "/", "page_count": len(pages), "pages": pages}
    with open(os.path.join(AGENT_DIR, "site-index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
        f.write("\n")

    write_llms_txt(pages, site_url, base_url)

    print(f"Site index: {len(pages)} pages -> static/agent/site-index.json")
    print(f"Pages without a frontmatter description: {len(missing_description)}")
    if "--list-missing" in sys.argv:
        for rel in missing_description:
            print(f"  {rel}")


def write_llms_txt(pages, site_url, base_url):
    lines = [
        "# A11YHub",
        "",
        "> Open-source accessibility knowledge base: tools and practices for people with "
        "disabilities, and guidance for the developers who build inclusive technology.",
        "",
        f"Full machine-readable index: {site_url}{base_url}/agent/site-index.json",
        "",
    ]
    groups = {}
    for page in pages:
        group = page["section"][0] if page["section"] else "Start here"
        groups.setdefault(group, []).append(page)
    for group in sorted(groups, key=lambda g: (g != "Start here", g)):
        lines.append(f"## {group}")
        lines.append("")
        for page in groups[group]:
            note = f": {page['description']}" if page["description"] else ""
            lines.append(f"- [{page['title']}]({site_url}{page['text']}){note}")
        lines.append("")
    with open(os.path.join(STATIC_DIR, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    main()
