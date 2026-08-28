from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data" / "source_registry.json"
DEFAULT_OUTPUT = ROOT / "data" / "discovery_manifest.json"
USER_AGENT = "OpportunityRadar/1.0 (+https://github.com/farzaneh-fb/stockholm-uppsala-opportunity-radar)"


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._active_href: str | None = None
        self._active_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)
            self._active_href = href
            self._active_text = []

    def handle_data(self, data: str) -> None:
        if self._active_href is not None:
            self._active_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._active_href is not None:
            self.links.append((self._active_href, " ".join("".join(self._active_text).split())))
            self._active_href = None
            self._active_text = []


def fetch(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")


def extract_listing_urls(html: str, source: dict[str, Any]) -> list[str]:
    return [candidate["url"] for candidate in extract_listing_candidates(html, source)]


def extract_listing_candidates(html: str, source: dict[str, Any]) -> list[dict[str, str]]:
    collector = LinkCollector()
    collector.feed(html)
    base_url = source["url"]
    patterns = source["listing_url_patterns"]
    candidates: list[dict[str, str]] = []
    seen: set[str] = set()
    for href, title in collector.links:
        absolute = urljoin(base_url, href).split("#", 1)[0]
        if not any(pattern in absolute for pattern in patterns) or absolute in seen:
            continue
        seen.add(absolute)
        candidates.append({"url": absolute, "title": title})
    return candidates


def harvest(sources: list[dict[str, Any]], timeout: int) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    all_urls: set[str] = set()
    for source in sources:
        item = {"name": source["name"], "url": source["url"]}
        try:
            candidates = extract_listing_candidates(fetch(source["url"], timeout), source)
            candidate_urls = [candidate["url"] for candidate in candidates]
            status = "ok" if candidate_urls or not source.get("required", True) else "empty"
            item.update({"status": status, "candidate_urls": candidate_urls, "candidates": candidates})
            all_urls.update(candidate_urls)
        except Exception as exc:  # noqa: BLE001 - one source must not abort a run
            item.update({"status": "failed", "candidate_urls": [], "error": str(exc)})
        results.append(item)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": results,
        "summary": {
            "sources_total": len(results),
            "sources_ok": sum(item["status"] == "ok" for item in results),
            "sources_failed": sum(item["status"] == "failed" for item in results),
            "sources_empty": sum(item["status"] == "empty" for item in results),
            "candidate_urls": len(all_urls),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest official opportunity source indexes into an auditable manifest.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    manifest = harvest(registry["sources"], args.timeout)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
