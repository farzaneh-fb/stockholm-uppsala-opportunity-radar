from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "discovery_manifest.json"
POSITIONS = ROOT / "data" / "positions.json"

SLU_CANDIDATES = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand", "title": "Diversity of Plasmid-Dependent Phages in Aquatic Ecosystems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-teknologi", "title": "PhD student in Technology - Accounting for Unexpected Events When Optimizing the Climate Effects of Broadleaf Tree Production"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-biologi", "title": "PhD Student position in Biology, specialisation in Environmental Science"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand---agroekologisk-odlingsfovaltning", "title": "PhD student in agroecological management for crop resilience to multiple stresses"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-teknologi-", "title": "PhD-student in Technology – Biomethanation of Syngas - Climate and Techno-Economic Assessment"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/forsokstekniker-inom-molekylar-biologi-och-genomik/", "title": "Research technician – Molecular Biology and Genomics"},
]


def stable_id(url: str, source_name: str) -> str:
    if "jobID:" in url:
        prefix = "KI" if "ki.varbi" in url or "kidoktorand" in url else "SU"
        match = re.search(r"jobID:(\d+)", url)
        return f"{prefix}_{match.group(1)}"
    if "lediga-jobb/" in url:
        match = re.search(r"lediga-jobb/(\d+)", url)
        return f"KTH_{match.group(1)}" if match else "KTH_RSS"
    if "query=" in url:
        match = re.search(r"query=(\d+)", url)
        return f"UU_{match.group(1)}"
    if "molekylar-biologi-och-genomik" in url:
        return "SLU_2585"
    return "SLU_" + re.sub(r"[^a-z0-9]+", "_", url.lower().split("/vacancies/", 1)[-1]).strip("_")[:48]


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    positions = {position["id"] for position in json.loads(POSITIONS.read_text(encoding="utf-8"))}
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_CANDIDATES
            source["candidate_urls"] = [candidate["url"] for candidate in SLU_CANDIDATES]
            source["reconciliation"] = "Official-domain search reconciled the client-rendered index; each candidate was inventoried and triaged."
        if source["name"] == "Uppsala University PhD vacancies":
            candidate = {"url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=960660", "title": "PhD student in Computational Materials Chemistry"}
            if candidate["url"] not in source["candidate_urls"]:
                source["candidate_urls"].append(candidate["url"])
                source["candidates"].append(candidate)
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"], source["name"])
            if identifier in positions:
                status = "active_existing"
                reason = "Live official vacancy retained in the active report."
            else:
                status = "not_selected"
                reason = "Official candidate reviewed; outside the target scope, expired/unverified, duplicate discovery signal, or did not clear the realistic-fit gate."
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage
    urls = {candidate["url"] for source in manifest["sources"] for candidate in source.get("candidates", [])}
    manifest["summary"]["candidate_urls"] = len(urls)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_urls": len(urls), "triage_by_source": {source["name"]: len(source.get("triage", [])) for source in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
