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
    site_links, unknown_links, external_links = [], [], []

    for raw in dict.fromkeys(URL_PATTERN.findall(answer)):
        url = raw.rstrip(".,;:!?*")
        if not url.startswith(base):
            external_links.append(url)
            continue
        clean = url.split("#")[0].split("?")[0].rstrip("/")
        if site_index.has_url(clean) or clean in extra:
            site_links.append(url)
        else:
            unknown_links.append(url)
    return {"site_links": site_links, "unknown_links": unknown_links, "external_links": external_links}
