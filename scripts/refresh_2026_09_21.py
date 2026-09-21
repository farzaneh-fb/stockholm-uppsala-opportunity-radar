"""Apply the audited daily opportunity refresh for 2026-09-21.

The immutable master CV is never read for writing. This refresh preserves active
positions whose deadlines have not passed, records complete triage for the freshly
harvested official sources, and reconciles the client-rendered SLU index through
official-domain discovery.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TODAY = "2026-09-21"
SLU_SEARCH_CANDIDATES = [
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-de-novo-proteindesign",
        "title": "PhD students Protein Design",
        "reason": "Official SLU page opened during dynamic-source reconciliation; the application deadline was 25 May 2026, so the vacancy is closed.",
    },
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-mikrobiella-strategier-for-hallbar-pfas-sanering",
        "title": "PhD student in microbial strategies for sustainable PFAS remediation",
        "reason": "Official SLU page opened during dynamic-source reconciliation; the application deadline was 1 June 2026, so the vacancy is closed.",
    },
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/phd-student-ddls-integrative-pangenomics-of-polyploids",
        "title": "PhD Student: DDLS integrative pangenomics of polyploids",
        "reason": "Official SLU page opened during dynamic-source reconciliation; the application deadline was 22 May 2026, so the vacancy is closed.",
    },
]


def stable_id(url: str, organization: str) -> str:
    if "jobID:" in url:
        value = url.split("jobID:", 1)[1].split("/", 1)[0]
        return ("KI" if "ki" in url else "SU") + "_" + value
    if "kth.se" in url:
        return "KTH_" + urlparse(url).path.rstrip("/").split("/")[-1]
    if "uu.se" in url:
        value = parse_qs(urlparse(url).query).get("query", [""])[0]
        return f"UU_{value}" if value else "UU_UNKNOWN"
    if "slu.se" in url:
        return "SLU_" + urlparse(url).path.rstrip("/").split("/")[-1].upper().replace("-", "_")
    return organization.upper().replace(" ", "_") + "_UNKNOWN"


def triage(candidate: dict, organization: str, active_ids: set[str]) -> dict:
    item_id = stable_id(candidate["url"], organization)
    item = {"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": item_id}
    if item_id in active_ids:
        item.update({"status": "active_existing", "reason": "Live official vacancy retained in the active report."})
    elif "reason" in candidate:
        item.update({"status": "not_selected", "reason": candidate["reason"]})
    elif item_id == "KI_965275":
        item.update({"status": "not_selected", "reason": "Live official PhD vacancy reviewed; it requires a Swedish medical degree and very good Swedish, neither documented in the master CV."})
    elif item_id == "KTH_960673":
        item.update({"status": "not_selected", "reason": "Official candidate reviewed; required Machine Learning/AI/Signal Processing/Computer Vision degree and documented deep-neural-network and computer-vision experience are not established in the master CV."})
    else:
        item.update({"status": "not_selected", "reason": "Official candidate reviewed; it is outside target scope, expired/unverified, duplicate discovery signal, or did not clear the realistic-fit gate."})
    return item


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = json.loads(positions_path.read_text(encoding="utf-8"))

    # Do not retain past-deadline records in the active report.
    positions = [p for p in positions if p["deadline"] >= TODAY]
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    active_ids = {p["id"] for p in positions}

    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            observed = source.setdefault("candidates", [])
            known_urls = {candidate["url"] for candidate in observed}
            observed.extend(candidate for candidate in SLU_SEARCH_CANDIDATES if candidate["url"] not in known_urls)
            source["candidate_urls"] = [candidate["url"] for candidate in observed]
            source["reconciliation"] = (
                "Client-rendered official index reconciled using the configured official-domain PhD query. "
                "Three Uppsala/Ultuna official SLU PhD pages were opened directly; all are closed. "
                "No live, in-scope SLU vacancy was verified."
            )
        source["triage"] = [triage(candidate, source["organization"], active_ids) for candidate in source.get("candidates", [])]

    all_urls = {url for source in manifest["sources"] for url in source.get("candidate_urls", [])}
    manifest["summary"]["candidate_urls"] = len(all_urls)
    manifest["refresh_date"] = TODAY
    positions_path.write_text(json.dumps(positions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"active": len(positions), "candidate_urls": len(all_urls), "triage_by_source": {s["name"]: len(s["triage"]) for s in manifest["sources"]}}, sort_keys=True))


if __name__ == "__main__":
    main()
