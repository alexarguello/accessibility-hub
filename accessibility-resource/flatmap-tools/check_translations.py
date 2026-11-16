"""
check_translations.py
Lists translated pages that are older than the page they were translated from.

A translation is a copy: when the original changes, nothing updates the copy.
This compares the last commit of each translated page with the last commit of
its original and reports the ones that have fallen behind.

Run from the accessibility-resource folder:
  python flatmap-tools/check_translations.py          report only, always exits 0
  python flatmap-tools/check_translations.py --strict exit 1 if any page is behind

Standard library only. Needs git; a page that is not committed yet is reported
as "not committed" and is not counted as behind.
"""
import os
import subprocess
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.dirname(TOOLS_DIR)
DOCS_DIR = os.path.join(SITE_DIR, "docs")
I18N_DIR = os.path.join(SITE_DIR, "i18n")
DOCS_PLUGIN = os.path.join("docusaurus-plugin-content-docs", "current")


def last_commit(path):
    """Return (unix time, short hash, date) of the last commit touching a file, or None."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct %h %cs", "--", path],
        cwd=SITE_DIR, capture_output=True, text=True,
    )
    parts = result.stdout.split()
    return (int(parts[0]), parts[1], parts[2]) if len(parts) == 3 else None


def translated_pages():
    """Yield (locale, docs-relative path) for every translated doc."""
    if not os.path.isdir(I18N_DIR):
        return
    for locale in sorted(os.listdir(I18N_DIR)):
        root = os.path.join(I18N_DIR, locale, DOCS_PLUGIN)
        for folder, _dirs, files in os.walk(root):
            for name in sorted(files):
                if name.endswith((".md", ".mdx")):
                    yield locale, os.path.relpath(os.path.join(folder, name), root)


def main():
    behind, checked = [], 0
    for locale, rel in translated_pages():
        checked += 1
        label = f"{locale}: {rel.replace(os.sep, '/')}"
        original_path = os.path.join(DOCS_DIR, rel)
        if not os.path.isfile(original_path):
            print(f"NO ORIGINAL    {label}  (the original page was moved or removed)")
            behind.append(label)
            continue
        translation = last_commit(os.path.join(I18N_DIR, locale, DOCS_PLUGIN, rel))
        original = last_commit(original_path)
        if translation is None or original is None:
            print(f"NOT COMMITTED  {label}")
        elif original[0] > translation[0]:
            print(f"BEHIND         {label}  (original changed {original[2]} in {original[1]}, "
                  f"translation is from {translation[2]})")
            behind.append(label)
        else:
            print(f"UP TO DATE     {label}")

    print(f"\n{checked} translated pages checked, {len(behind)} need attention.")
    return 1 if behind and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
