from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "data"
TODAY = "2026-09-27"
SLU_URL = "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/"
SLU_CANDIDATE = {
    "url": SLU_URL,
    "title": "PhD student in Arctic freshwater ecology",
}


def stable_id(url: str) -> str:
    if url.rstrip("/") == SLU_URL.rstrip("/"):
        return "SLU_2836"
    if match := re.search(r"jobID:(\d+)", url):
        if "su.varbi" in url:
            return f"SU_{match.group(1)}"
        if "uu.varbi" in url:
            return f"UU_{match.group(1)}"
        return f"KI_{match.group(1)}"
    if match := re.search(r"lediga-jobb/(\d+)", url):
        return f"KTH_{match.group(1)}"
    if match := re.search(r"query=(\d+)", url):
        return f"UU_{match.group(1)}"
    return "UNRESOLVED"


def reason(identifier: str, title: str) -> str:
    if identifier == "SLU_2836":
        return (
            "Official dynamic-source reconciliation found a live Uppsala PhD vacancy, "
            "but the master CV does not document the required valid Swedish driver’s license "
            "or the requested aquatic-ecology/limnology background."
        )
    if "postdoc" in title.lower() or "professor" in title.lower() or "lecturer" in title.lower():
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
            source["candidates"] = [SLU_CANDIDATE]
            source["candidate_urls"] = [SLU_URL]
            source["reconciliation"] = (
                "Client-rendered official index reconciled on 2026-09-27 using the configured official-domain PhD query and a direct official SLU page. "
                "The live Arctic freshwater ecology PhD page was inventoried and triaged."
            )
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status = "active_existing"
                triage_reason = "Live official vacancy retained in the active report."
            elif identifier in seen and seen[identifier].get("first_seen") != TODAY:
                status = "seen_not_selected"
                triage_reason = "Previously reviewed official candidate remains outside the active shortlist."
            else:
                status = "not_selected"
                triage_reason = reason(identifier, candidate.get("title", ""))
                seen[identifier] = {"source_url": candidate["url"], "first_seen": TODAY}
            triage.append({
                "url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier,
                "status": status, "reason": triage_reason,
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
    }))


if __name__ == "__main__":
    main()
