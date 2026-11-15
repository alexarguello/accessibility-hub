"""Checks that every link in an answer that points at the site is a page that exists."""
from __future__ import annotations

import re

from .site_index import SiteIndex

URL_PATTERN = re.compile(r"https?://[^\s)\]>\"'`]+")


def check_links(answer: str, site_index: SiteIndex, config: dict) -> dict:
    """Sort the links in an answer into site pages, unknown site links, and external links.

    An unknown site link is one the model made up or altered.
    """
    base = config["siteUrl"].rstrip("/")
    extra = {f"{base}/{page}".rstrip("/") for page in config.get("extraPages", [])}
    # Real parts of the site that are left out of the index on purpose.
    prefixes = tuple(f"{base}/{prefix}".rstrip("/") for prefix in config.get("extraPrefixes", []))
    site_links, unknown_links, external_links = [], [], []

    for raw in dict.fromkeys(URL_PATTERN.findall(answer)):
        url = raw.rstrip(".,;:!?*")
        if not url.startswith(base):
            external_links.append(url)
            continue
        clean = url.split("#")[0].split("?")[0].rstrip("/")
        in_prefix = any(clean == p or clean.startswith(p + "/") for p in prefixes)
        if site_index.has_url(clean) or clean in extra or in_prefix:
            site_links.append(url)
        else:
            unknown_links.append(url)
    return {"site_links": site_links, "unknown_links": unknown_links, "external_links": external_links}
