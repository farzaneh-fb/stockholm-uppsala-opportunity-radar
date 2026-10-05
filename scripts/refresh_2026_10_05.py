from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import build_report  # noqa: E402

DATA = ROOT / "data"
TODAY = "2026-10-05"

# Directly opened official pages from the required SLU official-domain reconciliation.
SLU_CANDIDATES = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogsskotsel/", "title": "PhD student in silviculture of planted birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand----resilienta-vallproduktionssystem/", "title": "PhD student in resilient forage production systems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogspatologi/", "title": "PhD student in forest pathology: biotic risks to birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/", "title": "PhD student in Arctic freshwater ecology"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-landskapets-governance-och-forvaltning/", "title": "PhD Student in Landscape Governance and Management"},
]

# Official KI index backfill, ordered by most distant deadline. Every one was opened
# directly before triage; they do not pass the documented realistic-fit gate.
KI_BACKFILL_CANDIDATES = [
    {"url": "https://kidoktorand.varbi.com/en/what:job/jobID:974313/type:job/where:4/apply:1", "title": "Doctoral student position in immunometabolism for alphavirus therapeutics"},
    {"url": "https://kidoktorand.varbi.com/en/what:job/jobID:974353/type:job/where:4/apply:1", "title": "Doctoral student in virus-host interactions and immunometabolism"},
    {"url": "https://kidoktorand.varbi.com/en/what:job/jobID:974417/type:job/where:4/apply:1", "title": "Doctoral student position in immunometabolism and functional HIV cure"},
    {"url": "https://kidoktorand.varbi.com/en/what:job/jobID:975419/type:job/where:4/apply:1", "title": "Doctoral (PhD) student position in clinical cell manufacturing"},
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


def not_selected_reason(identifier: str) -> str:
    reasons = {
        "KI_974313": "Live official vacancy reviewed; the MSCA mobility rule excludes applicants who have resided or carried out their main activity in Sweden for more than 12 of the preceding 36 months, which conflicts with the master CV's documented Stockholm-based study and work history.",
        "KI_974353": "Live official vacancy reviewed; the MSCA mobility rule excludes applicants who have resided or carried out their main activity in Sweden for more than 12 of the preceding 36 months, which conflicts with the master CV's documented Stockholm-based study and work history.",
        "KI_974417": "Live official vacancy reviewed; the MSCA mobility rule excludes applicants who have resided or carried out their main activity in Sweden for more than 12 of the preceding 36 months, which conflicts with the master CV's documented Stockholm-based study and work history.",
        "KI_975419": "Live official vacancy reviewed; it is restricted to applicants holding a Biomedical Scientist degree or licence, and that credential is not documented in the immutable master CV.",
        "SLU_doktorand_i_skogsskotsel": "Live official SLU PhD vacancy reviewed; it requires forest-science and fieldwork expertise not documented in the immutable master CV.",
        "SLU_doktorand_resilienta_vallproduktionssystem": "Live official SLU PhD vacancy reviewed; it is based in Alnarp and requires agricultural-crop-production expertise not documented in the immutable master CV.",
        "SLU_doktorand_i_skogspatologi": "Live official SLU PhD vacancy reviewed; it is based in Alnarp and requires forest-management eligibility and forest-pathology/fieldwork experience not documented in the immutable master CV.",
        "SLU_doktorand": "Live official SLU PhD vacancy reviewed; it is outside the Stockholm/Solna/Uppsala/Ultuna geography and requires freshwater-ecology expertise not documented in the immutable master CV.",
        "SLU_doktorand_i_landskapets_governance_och_forvaltning": "Live official SLU PhD vacancy reviewed; it requires landscape-governance and planning expertise not documented in the immutable master CV.",
        "UU_970239": "Live official PhD vacancy reviewed; its required battery-energy-storage knowledge and battery-electrochemistry experience are not established by the immutable master CV.",
        "UU_970707": "Live official PhD vacancy reviewed; its required lithium-ion battery formulation, assembly and testing experience is not established by the immutable master CV.",
        "UU_971356": "Live official PhD vacancy reviewed; it requires experimental nuclear-physics expertise not documented in the immutable master CV.",
        "UU_971449": "Live official PhD vacancy reviewed; the required rehabilitation/prosthetics or discrete-choice-experiment background is not documented in the immutable master CV.",
    }
    return reasons.get(identifier, "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, is expired, or requires qualifications not documented in the immutable master CV.")


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
            source["candidate_urls"] = [candidate["url"] for candidate in SLU_CANDIDATES]
            source["candidates"] = SLU_CANDIDATES
            source["reconciliation"] = "Client-rendered official index reconciled on 2026-10-05 using the configured official-domain PhD query and direct official SLU vacancy pages. All current official PhD listings returned by the Uppsala/Ultuna reconciliation were inventoried and triaged; no listing cleared geography and realistic-fit gates."
        if source["name"] == "Karolinska Institutet vacancies":
            existing_urls = {candidate["url"].rstrip("/") for candidate in source["candidates"]}
            for candidate in KI_BACKFILL_CANDIDATES:
                if candidate["url"].rstrip("/") not in existing_urls:
                    source["candidates"].append(candidate)
                    source["candidate_urls"].append(candidate["url"])
                    existing_urls.add(candidate["url"].rstrip("/"))
            source["backfill"] = "Official KI vacancy-index sorting by last application date was checked on 2026-10-05; all current official PhD listings discovered outside the harvested first page were added to candidate inventory and directly verified."

        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", not_selected_reason(identifier)
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY})
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    manifest["refresh_date"] = TODAY
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(source["status"] == "ok" for source in manifest["sources"]),
        "sources_dynamic": sum(source["status"] == "dynamic" for source in manifest["sources"]),
        "sources_failed": sum(source["status"] == "failed" for source in manifest["sources"]),
        "sources_empty": sum(source["status"] == "empty" for source in manifest["sources"]),
        "candidate_urls": len({candidate["url"].rstrip("/") for source in manifest["sources"] for candidate in source.get("candidates", [])}),
    }
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({
        "active": len(positions), "new": [],
        "phd": sum(p["kind"] == "phd" for p in positions),
        "jobs": sum(p["kind"] == "job" for p in positions),
        "summary": manifest["summary"],
        "triage": {source["name"]: len(source.get("triage", [])) for source in manifest["sources"]},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
