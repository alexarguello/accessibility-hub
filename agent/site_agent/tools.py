"""The tools the model can call. Each one reads the site index; none changes anything."""
from __future__ import annotations

import json

from .site_index import SiteIndex

# Tool descriptions are prompts too: the model decides when and how to call a tool from these.
DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_site",
            "description": (
                "Search the site for pages about a topic. The site content is in English: always "
                "search with English keywords, even when the person writes in another language. "
                "Returns page titles, URLs and short descriptions. Search again with different "
                "words if the first results do not fit."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": 'A few English keywords, for example "screen reader phone".',
                    },
                    "limit": {
                        "type": "integer",
                        "description": "How many results to return (1 to 8). Default 5.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_page",
            "description": (
                "Read the full text of one page of the site. Use a path or URL returned by "
                "search_site. Read a page before you state what it says."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The page path or URL from a search result.",
                    },
                },
                "required": ["path"],
            },
        },
    },
]


class Tools:
    def __init__(self, site_index: SiteIndex, max_page_chars: int = 12000):
        self.definitions = DEFINITIONS
        self._index = site_index
        self._max_page_chars = max_page_chars
        self._handlers = {"search_site": self._search_site, "get_page": self._get_page}

    def execute(self, name: str, raw_arguments) -> dict:
        """Run one tool call. Never raises: a failure comes back as {"error": ...}.

        The model sees that error as the tool result and can correct itself.
        """
        handler = self._handlers.get(name)
        if handler is None:
            return {"error": f'Unknown tool "{name}".'}
        arguments = raw_arguments
        if isinstance(raw_arguments, str):
            try:
                arguments = json.loads(raw_arguments) if raw_arguments.strip() else {}
            except json.JSONDecodeError:
                return {"error": "Arguments were not valid JSON."}
        if not isinstance(arguments, dict):
            return {"error": "Arguments must be an object."}
        try:
            return handler(arguments)
        except Exception as error:  # a tool bug must not end the conversation
            return {"error": f"Tool failed: {error}"}

    def _search_site(self, arguments: dict) -> dict:
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            return {"error": "query must be a non-empty string."}
        limit = arguments.get("limit")
        size = min(8, max(1, limit)) if isinstance(limit, int) else 5
        results = [
            {
                "title": r["title"],
                "url": r["url"],
                "section": " > ".join(r["section"]),
                "description": r["description"],
                "status": r["status"],
                "words": r["words"],
            }
            for r in self._index.search(query, limit=size)
        ]
        if not results:
            return {
                "results": [],
                "note": "No page matched. Try other English keywords, or tell the person "
                        "the site does not cover this.",
            }
        return {"results": results}

    def _get_page(self, arguments: dict) -> dict:
        path = arguments.get("path")
        if not isinstance(path, str) or not path.strip():
            return {"error": "path must be a non-empty string."}
        found = self._index.get_page(path)
        if found is None:
            return {"error": f'No page at "{path}". Use search_site to find the right path.'}
        page, text = found
        if len(text) > self._max_page_chars:
            text = text[: self._max_page_chars] + "\n[Page cut here; the rest is not shown.]"
        return {
            "title": page["title"],
            "url": page["url"],
            "status": page.get("status", ""),
            "words": page.get("words", 0),
            "text": text,
        }
