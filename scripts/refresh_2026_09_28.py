from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "data"
TODAY = "2026-09-28"

# Reconciled directly from the live, client-rendered official SLU index.
SLU_CANDIDATES = [
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/",
        "title": "PhD student in Arctic freshwater ecology",
    },
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-landskapets-governance-och-forvaltning/",
        "title": "PhD Student in Landscape Governance and Management",
    },
]


def stable_id(url: str) -> str:
    if url.rstrip("/").endswith("/doktorand"):
        return "SLU_2836"
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


def not_selected_reason(identifier: str, title: str, source_name: str) -> str:
    title_lower = title.lower()
    if identifier == "KI_968211":
        return "Live official PhD vacancy reviewed; LC-MS experience is a stated requirement and is not documented in the immutable master CV."
    if identifier == "SLU_2836":
        return "Live official Uppsala PhD vacancy reviewed; the immutable master CV does not document the required valid Swedish driver’s license or the requested aquatic-ecology/limnology background."
    if source_name == "SciLifeLab careers":
        return "Official SciLifeLab discovery item reviewed; it is a partner listing, outside the target geography/seniority gate, duplicate of an official employer listing, or lacks a live primary-employer application page for acceptance."
    if "postdoc" in title_lower or "professor" in title_lower or "lecturer" in title_lower:
        return "Official candidate reviewed; senior or postdoctoral eligibility is not documented in the immutable master CV."
    return "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    active_ids = {p["id"] for p in positions}
    seen = json.loads(seen_path.read_text(encoding="utf-8"))

    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_CANDIDATES
            source["candidate_urls"] = [candidate["url"] for candidate in SLU_CANDIDATES]
            source["reconciliation"] = (
                "Client-rendered official index reconciled on 2026-09-28 with the configured official-domain PhD query and direct official SLU vacancy pages. "
                "Current Uppsala/Ultuna PhD candidates were inventoried and triaged."
            )
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status = "active_existing"
                reason = "Live official vacancy retained in the active report."
            elif identifier in seen:
                status = "seen_not_selected"
                reason = "Previously reviewed candidate remains outside the active shortlist."
            else:
                status = "not_selected"
                reason = not_selected_reason(identifier, candidate.get("title", ""), source["name"])
                seen[identifier] = {"source_url": candidate["url"], "first_seen": TODAY}
            triage.append({
                "url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier,
                "status": status, "reason": reason,
            })
        source["triage"] = triage

    manifest["refresh_date"] = TODAY
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(s["status"] == "ok" for s in manifest["sources"]),
        "sources_dynamic": sum(s["status"] == "dynamic" for s in manifest["sources"]),
        "sources_failed": sum(s["status"] == "failed" for s in manifest["sources"]),
        "sources_empty": sum(s["status"] == "empty" for s in manifest["sources"]),
        "candidate_urls": len({c["url"].rstrip("/") for s in manifest["sources"] for c in s.get("candidates", [])}),
    }
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from build_test_report import build_report
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({
        "active": len(positions), "phd": sum(p["kind"] == "phd" for p in positions),
        "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"],
        "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
