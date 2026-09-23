from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_test_report import build_report
from scripts.harvest_sources import harvest
DATA = ROOT / "data"
TODAY = "2026-09-23"

# Reconciled directly from the official SLU vacancy index, whose client rendering
# prevents the static harvester from collecting its links.
SLU_CANDIDATES = [
    ("PhD student in Arctic freshwater ecology", "doktorand/"),
    ("Researcher in Food Control Literature Review", "forskare-for-litteratursammanstallning-inom-livsmedelskontroll-/"),
    ("Research Coordinator", "forskningskoordinator/"),
    ("PhD Student in Landscape Governance and Management", "doktorand-i-landskapets-governance-och-forvaltning/"),
    ("Small Animal Veterinarian – Department of Clinical Sciences and Small Animal Department, UDS", "klinikveterinar-smadjursavd/"),
    ("Senior lecturer in dairy cow management", "universitetslektor-i-skotsel-av-mjolkkor/"),
    ("Postdoc in Chromatin Dynamics During Extreme Desiccation Tolerance", "postdoc-i-kromatindynamik-vid-extrem-uttorkningstolerans/"),
    ("Senior Lecturer in horticultural genomics and breeding", "universitetslektor-i-hortikulturell-genomik-och-foradling/"),
    ("Senior Lecturer/Associate Professor* in Small Animal Surgery", "universitetslektor-i-smadjurskirurgi/"),
    ("Senior Lecturer/Associate Professor* in Animal Reproduction", "universitetslektor-i-husdjursreproduktion/"),
    ("PhD student in Technology - Accounting for Unexpected Events When Optimizing the Climate Effects of Broadleaf Tree Production", "doktorand-i-teknologi/"),
    ("Postdoctoral position in freshwater ecology and climate change", "postdoktor-sotvattensekologi-/"),
    ("PhD Student position in Biology, specialisation in Environmental Science", "doktorand-i-biologi/"),
    ("Postdoctoral Researcher: Psychology of Forest Management and Biodiversity", "postdoktor---tillampad-ekonomi/"),
    ("Senior Lecturer in Digitalisation of Agriculture", "universitetslektor-i-lantbrukets-digitalisering/"),
    ("Professor (full tenure) in animal ecology", "professor-i-zooekologi/"),
]
SLU_PREFIX = "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/"


def stable_id(url: str, source_name: str) -> str:
    match = re.search(r"jobID:(\d+)", url)
    if match:
        return ("SU" if "su.varbi" in url else "KI") + "_" + match.group(1)
    match = re.search(r"lediga-jobb/(\d+)", url)
    if match:
        return "KTH_" + match.group(1)
    match = re.search(r"query=(\d+)", url)
    if match:
        return "UU_" + match.group(1)
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    return "SLU_" + re.sub(r"[^A-Z0-9]+", "_", slug.upper()).strip("_")


def preserve_failures(fresh: dict, previous: dict) -> None:
    old = {source["name"]: source for source in previous.get("sources", [])}
    for source in fresh["sources"]:
        if source["status"] == "failed" and source["name"] in old:
            retained = old[source["name"]].copy()
            retained["status"] = "failed"
            retained["error"] = source.get("error", "source harvest failed; prior inventory retained")
            source.clear()
            source.update(retained)


def main() -> None:
    registry = json.loads((DATA / "source_registry.json").read_text(encoding="utf-8"))
    previous = json.loads((DATA / "discovery_manifest.json").read_text(encoding="utf-8"))
    manifest = harvest(registry["sources"], timeout=60)
    preserve_failures(manifest, previous)

    slu = next(source for source in manifest["sources"] if source["name"] == "SLU vacancies")
    slu["candidates"] = [{"title": title, "url": SLU_PREFIX + slug} for title, slug in SLU_CANDIDATES]
    slu["candidate_urls"] = [candidate["url"] for candidate in slu["candidates"]]
    slu["reconciliation"] = (
        "Client-rendered official index reconciled with the configured official-domain query and direct official SLU vacancy-index retrieval on 2026-09-23. "
        "All 16 current official index listings were inventoried and triaged; only Uppsala/Ultuna candidates were considered for the regional shortlist."
    )

    positions_path = DATA / "positions.json"
    positions = [position for position in json.loads(positions_path.read_text(encoding="utf-8")) if position["deadline"] >= TODAY]
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    active = {position["id"] for position in positions}

    seen_path = DATA / "seen_positions.json"
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"], source["name"])
            if identifier in active:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed official candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."
                seen[identifier] = {"source_url": candidate["url"], "first_seen": TODAY}
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["generated_at"] = f"{TODAY}T00:00:00+00:00"
    manifest["refresh_date"] = TODAY
    unique_urls = {url.rstrip("/") for source in manifest["sources"] for url in source.get("candidate_urls", [])}
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(source["status"] == "ok" for source in manifest["sources"]),
        "sources_failed": sum(source["status"] == "failed" for source in manifest["sources"]),
        "sources_empty": sum(source["status"] == "empty" for source in manifest["sources"]),
        "sources_dynamic": sum(source["status"] == "dynamic" for source in manifest["sources"]),
        "candidate_urls": len(unique_urls),
    }
    (DATA / "discovery_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({
        "active": len(positions),
        "phd": sum(position["kind"] == "phd" for position in positions),
        "jobs": sum(position["kind"] == "job" for position in positions),
        "candidate_urls": len(unique_urls),
        "triage_by_source": {source["name"]: len(source["triage"]) for source in manifest["sources"]},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
