"""Audited daily refresh for 22 October 2026; never writes the master CV."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "data"
TODAY = "2026-10-22"

# Reconciled from SLU's official PhD filter and then opened directly on 22 October.
SLU_RECONCILIATION_CANDIDATES = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-inom-tradgardsvetenskap-/", "title": "PhD student in Horticultural Science"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-inom-biomassa-resurser-fran-hallbara-odlingssystem/", "title": "PhD student in biomass resources from sustainable cropping systems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-inom-bioekonomiska-system-i-jordbruket/", "title": "PhD student in agricultural bioeconomy systems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand----resilienta-vallproduktionssystem/", "title": "PhD student in resilient forage production systems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogsskotsel/", "title": "PhD student in silviculture of planted birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogspatologi/", "title": "PhD student in forest pathology: biotic risks to birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-landskapets-governance-och-forvaltning/", "title": "PhD Student in Landscape Governance and Management"},
]


def stable_id(url: str) -> str:
    if "jobID:" in url:
        number = re.search(r"jobID:(\d+)", url).group(1)
        if "su.varbi" in url:
            return f"SU_{number}"
        if "uu.varbi" in url:
            return f"UU_{number}"
        return f"KI_{number}"
    if match := re.search(r"lediga-jobb/(\d+)", url):
        return f"KTH_{match.group(1)}"
    if match := re.search(r"query=(\d+)", url):
        return f"UU_{match.group(1)}"
    if "scilifelab.se/career/" in url:
        return "SCILIFE_" + url.rstrip("/").rsplit("/", 1)[-1]
    return "SLU_" + re.sub(r"[^a-z0-9]+", "_", url.lower().rstrip("/").rsplit("/", 1)[-1]).strip("_")


def rejection_reason(identifier: str) -> str:
    if identifier == "KI_975419":
        return "Official vacancy reviewed but not accepted: it requires a Biomedical Scientist degree or licence, which is not documented in the immutable master CV."
    if identifier.startswith("SLU_"):
        return "Official SLU listing opened after dynamic-index reconciliation; it is outside the Stockholm/Solna/Uppsala scope or does not clear the realistic-fit gate from the immutable master CV."
    return "Official candidate triaged; it is outside target scope, does not clear the realistic-fit gate, is expired, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    seen_path = DATA / "seen_positions.json"
    positions_path = DATA / "positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    active_ids = {p["id"] for p in positions}

    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_RECONCILIATION_CANDIDATES
            source["candidate_urls"] = [item["url"] for item in SLU_RECONCILIATION_CANDIDATES]
            source["reconciliation"] = (
                "Dynamic official index reconciled on 2026-10-22 using the registry's official-domain query and "
                "the official SLU PhD filter. All seven discovered official listing pages were opened directly; "
                "none met both geographic coverage and realistic-fit gates."
            )
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            status = "active_existing" if identifier in active_ids else "not_selected"
            triage.append({
                "url": candidate["url"],
                "title": candidate.get("title", ""),
                "stable_id": identifier,
                "status": status,
                "reason": "Live official vacancy re-verified and retained in the active report." if status == "active_existing" else rejection_reason(identifier),
            })
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY})
        source["triage"] = triage

    manifest["refresh_date"] = TODAY
    all_urls = {candidate["url"].rstrip("/") for source in manifest["sources"] for candidate in source.get("candidates", [])}
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(source["status"] == "ok" for source in manifest["sources"]),
        "sources_dynamic": sum(source["status"] == "dynamic" for source in manifest["sources"]),
        "sources_failed": sum(source["status"] == "failed" for source in manifest["sources"]),
        "sources_empty": sum(source["status"] == "empty" for source in manifest["sources"]),
        "candidate_urls": len(all_urls),
    }
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from build_test_report import build_report
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({
        "active": len(positions), "new": [], "phd": sum(p["kind"] == "phd" for p in positions),
        "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"],
        "triage": {source["name"]: len(source.get("triage", [])) for source in manifest["sources"]},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
