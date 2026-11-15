"""Loads a site content index and searches it.

The index format is the contract between a site and the agent:
  site-index.json   {"site": ..., "pages": [{"url", "path", "text", "title", ...}]}
  pages/<route>.md  the readable text of each page
"""
from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

STOPWORDS = frozenset(
    # English
    "a an and are as at be but by can do does for from get give has have how i if in is it me "
    "my of on or so some tell that the their there this to was what when where which who why "
    "will with you your about should "
    # Spanish
    "al como con cual de del donde el en es esta hay la las lo los mi para por puedo que se "
    "son su un una y".split()
)

# How much a query word counts when it appears in each part of a page entry.
FIELD_WEIGHTS = {"title": 5, "headings": 3, "tags": 3, "description": 2, "section": 1, "path": 1}
STUB_WORDS = 60


def normalize(text: str) -> str:
    """Lowercase and strip accents, so "accesibilidad" and "Accesibilidad" match."""
    decomposed = unicodedata.normalize("NFD", str(text or "").lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _stem(token: str) -> str:
    # Enough to match "readers" with "reader"; not a real stemmer.
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", normalize(text))
    return [_stem(w) for w in words if len(w) > 1 and w not in STOPWORDS]


def _normalize_path(value: str) -> str:
    path = str(value or "").strip()
    if re.match(r"^https?://", path):
        path = urlparse(path).path
    path = path.split("#")[0].split("?")[0]
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path.lower()


class SiteIndex:
    def __init__(self, data: dict, read_text: Callable[[dict], str]):
        self.site: str = data.get("site", "")
        self.pages: list[dict] = data.get("pages", [])
        self._read_text = read_text
        self._by_path = {_normalize_path(p["path"]): p for p in self.pages}

        self._fields = []
        for page in self.pages:
            labels = [*page.get("tags", []), *page.get("topics", []),
                      *page.get("disability_type", []), *page.get("audience", [])]
            self._fields.append({
                "title": set(tokenize(page.get("title", ""))),
                "headings": set(tokenize(" ".join(page.get("headings", [])))),
                "tags": set(tokenize(" ".join(labels))),
                "description": set(tokenize(page.get("description", ""))),
                "section": set(tokenize(" ".join(page.get("section", [])))),
                "path": set(tokenize(page.get("path", ""))),
            })

        # In how many pages each word appears; rare words count for more.
        self._document_frequency: dict[str, int] = {}
        for fields in self._fields:
            for token in set().union(*fields.values()):
                self._document_frequency[token] = self._document_frequency.get(token, 0) + 1

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Rank pages for a query. Best matches first."""
        tokens = set(tokenize(query))
        total = len(self.pages)
        scored = []
        for page, fields in zip(self.pages, self._fields):
            score = 0.0
            for token in tokens:
                frequency = self._document_frequency.get(token)
                if not frequency:
                    continue
                rarity = math.log(1 + total / frequency)
                best = max((w for name, w in FIELD_WEIGHTS.items() if token in fields[name]), default=0)
                score += rarity * best
            if score == 0:
                continue
            # A page with almost no content should not outrank a real one on its title alone.
            if page.get("words", 0) < STUB_WORDS:
                score *= 0.6
            scored.append((score, page))

        scored.sort(key=lambda item: (-item[0], item[1]["path"]))
        return [
            {
                "title": page["title"],
                "url": page["url"],
                "path": page["path"],
                "section": page.get("section", []),
                "description": page.get("description", ""),
                "status": page.get("status", ""),
                "words": page.get("words", 0),
                "score": round(score, 2),
            }
            for score, page in scored[:limit]
        ]

    def find_page(self, path_or_url: str) -> dict | None:
        """Find a page by full URL, site path, or the unambiguous tail of a path."""
        wanted = _normalize_path(path_or_url)
        if wanted in self._by_path:
            return self._by_path[wanted]
        matches = [p for key, p in self._by_path.items() if key.endswith(wanted)]
        return matches[0] if len(matches) == 1 else None

    def get_page(self, path_or_url: str) -> tuple[dict, str] | None:
        page = self.find_page(path_or_url)
        if page is None:
            return None
        return page, self._read_text(page)

    def sections(self) -> list[dict]:
        """Top-level pages, for the system prompt."""
        return [p for p in self.pages if not p.get("section")]

    def has_url(self, url: str) -> bool:
        return _normalize_path(url) in self._by_path


def load_from_directory(directory: str | Path) -> SiteIndex:
    """Load an index from a folder that holds site-index.json and pages/."""
    root = Path(directory)
    data = json.loads((root / "site-index.json").read_text(encoding="utf-8"))
    marker = "/agent/pages/"

    def read_text(page: dict) -> str:
        text_path = page.get("text", "")
        if marker not in text_path:
            raise FileNotFoundError(f"Page has no text file: {page.get('path')}")
        relative = text_path.split(marker, 1)[1]
        return (root / "pages").joinpath(*relative.split("/")).read_text(encoding="utf-8")

    return SiteIndex(data, read_text)
