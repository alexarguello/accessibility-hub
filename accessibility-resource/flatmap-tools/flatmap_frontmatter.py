"""
flatmap_frontmatter.py
Frontmatter parsing and tag extraction for the A11YHub flatmap generator.
"""
import re


def parse_frontmatter(file_path):
    """Parse YAML frontmatter from a markdown file. Returns a dict of key->value."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            return {}
        m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not m:
            return {}
        tags = {}
        for line in m.group(1).split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if '#' in value:
                    value = value.split('#')[0].strip()
                if value.startswith('[') and value.endswith(']'):
                    inner = value[1:-1]
                    value = [i.strip() for i in inner.split(',')] if inner.strip() else []
                elif value.startswith('""') and value.endswith('""'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                tags[key] = value
    except Exception as e:
        print(f"Warning: Could not parse frontmatter from {file_path}: {e}")
        return {}
    return tags


def evaluate_tag_condition(condition, frontmatter):
    """Evaluate a compound condition like 'author:not_empty AND status:draft'."""
    if ' AND ' in condition:
        return all(evaluate_simple_condition(p.strip(), frontmatter)
                   for p in condition.split(' AND '))
    return evaluate_simple_condition(condition, frontmatter)


def evaluate_simple_condition(condition, frontmatter):
    """Evaluate 'field:value', 'field:not_empty', or 'field:is_empty'."""
    if ':' not in condition:
        return False
    field, value = condition.split(':', 1)
    fv = frontmatter.get(field, '')
    if value == 'not_empty':
        return isinstance(fv, str) and fv.strip() != ''
    if value == 'is_empty':
        return not isinstance(fv, str) or fv.strip() == ''
    return frontmatter.get(field) == value


def extract_tags_from_frontmatter(frontmatter):
    """Return a list of tag strings derived from frontmatter fields."""
    tags = []
    for field in ('type', 'status', 'level', 'visibility'):
        if field in frontmatter and isinstance(frontmatter[field], str):
            tags.append(f"{field}:{frontmatter[field]}")
    topics = frontmatter.get('topics', [])
    if isinstance(topics, list):
        for t in topics:
            if isinstance(t, str) and ':' in t:
                tags.append(t)
    author = frontmatter.get('author', '')
    tags.append('author:not_empty' if (isinstance(author, str) and author.strip())
                else 'author:is_empty')
    for field, value in frontmatter.items():
        if isinstance(value, str):
            tags.append(f"{field}:is_not_empty" if value.strip() else f"{field}:is_empty")
        elif value is None or value == "":
            tags.append(f"{field}:is_empty")
        else:
            tags.append(f"{field}:is_not_empty")
    return tags
