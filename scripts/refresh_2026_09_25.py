from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import build_report, render_position  # noqa: E402

DATA = ROOT / "data"
TODAY = "2026-09-25"
SLU_PREFIX = "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/"
SLU_CANDIDATES = [
    ("PhD student in resilient forage production systems", "doktorand----resilienta-vallproduktionssystem/"),
    ("PhD student in silviculture of planted birch", "doktorand-i-skogsskotsel/"),
    ("PhD student in forest pathology: biotic risks to birch", "doktorand-i-skogspatologi/"),
    ("Small Animal Veterinarian with Focus on Anaesthesiology, University Animal Hospital, Department of Clinical Sciences, SLU", "klinikveterinar-anestesi-smadjur/"),
    ("PhD student in Arctic freshwater ecology", "doktorand/"),
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
NEW_POSITION = {
    "id": "UU_968823",
    "kind": "phd",
    "title": "PhD student with specialization in chemistry in polymer-based solid-state batteries",
    "short_title": "polymer_solid_state_batteries",
    "organization": "Uppsala University",
    "city": "Uppsala",
    "location_detail": "Department of Chemistry – Ångström Laboratory",
    "found_date": TODAY,
    "new_date": TODAY,
    "published": "2026-09-16",
    "deadline": "2026-10-07",
    "employment": "Full-time doctoral employment",
    "fit_score": 72,
    "fit_label": "Relevant stretch match",
    "description": "Develop and investigate anode-free sodium batteries based on polymer electrolytes through experimental polymer science, materials chemistry, electrochemistry and spectroscopy.",
    "match_reasons": [
        "Master's-level medical nanotechnology training provides a relevant interdisciplinary materials-science foundation",
        "Documented experimental research, analytical work and scientific communication support laboratory-based doctoral research",
        "Python/R-based scientific-data analysis and reproducible workflows provide a useful complement for experimental data handling",
        "Collaborative research experience at KI, KTH and SciLifeLab supports work across experimental and quantitative colleagues",
    ],
    "gaps": [
        "Battery fabrication, electrochemical characterization and polymer-electrolyte experience are not documented in the master CV",
        "Advanced materials analysis, especially X-ray photoelectron spectroscopy, is not explicitly documented",
        "The application should present the nanotechnology foundation accurately while explaining motivation to develop battery-specific methods",
    ],
    "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=968823",
    "apply_url": "https://uu.varbi.com/en/what:login/type:job/jobID:968823",
    "contact": "Maria Hahlin — Maria.Hahlin@kemi.uu.se; Jonas Mindemark — Jonas.Mindemark@kemi.uu.se",
    "headline": "Interdisciplinary Researcher | Nanotechnology, Experimental Science & Reproducible Analysis",
    "statement": "Interdisciplinary biomedical researcher with Master's-level training in medical nanotechnology, an established biology research and publication background, and growing bioinformatics skills. I combine experimental research with Python/R-based scientific-data analysis and reproducible workflows, and work comfortably between experimental and computational colleagues. I would bring this foundation to experimental battery research while developing specialised expertise in polymer electrolytes, electrochemistry and materials analysis.",
    "section_order": ["Personal Statement", "Education", "Research Experience", "Wet Lab & Experimental Expertise", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
}


def stable_id(url: str) -> str:
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


def reason_for_new(identifier: str, title: str) -> str:
    if identifier == "KI_929898":
        return "Official role reviewed. The master CV supports laboratory research but does not document the prioritized systems-neuroscience, electrophysiology, in-vivo animal-behaviour or circuit-imaging experience; it does not clear the stricter non-PhD fit gate."
    if identifier == "UU_968823":
        return "Live official vacancy accepted after fit review and included in the active report."
    if "POSTDOC" in title.upper() or "PROFESSOR" in title.upper() or "LECTURER" in title.upper():
        return "Official candidate reviewed; senior or postdoctoral eligibility is not documented in the immutable master CV."
    return "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slu = next(item for item in manifest["sources"] if item["name"] == "SLU vacancies")
    slu["candidates"] = [{"title": title, "url": SLU_PREFIX + slug} for title, slug in SLU_CANDIDATES]
    slu["candidate_urls"] = [item["url"] for item in slu["candidates"]]
    slu["reconciliation"] = "The client-rendered official SLU index was reconciled on 2026-09-25 using the configured official-domain PhD query and direct official index retrieval. All 19 current official listings were inventoried; Uppsala/Ultuna-targeted PhD listings were triaged against the immutable master CV."

    positions_path = DATA / "positions.json"
    positions = [item for item in json.loads(positions_path.read_text(encoding="utf-8")) if item["deadline"] >= TODAY]
    active_ids = {item["id"] for item in positions}
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    if NEW_POSITION["id"] not in active_ids:
        with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
            master = yaml_engine.load(handle)
        render_position(yaml_engine, master, NEW_POSITION)
        positions.append(NEW_POSITION)
        active_ids.add(NEW_POSITION["id"])

    seen_path = DATA / "seen_positions.json"
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    seen.setdefault(NEW_POSITION["id"], {"source_url": NEW_POSITION["source_url"], "first_seen": TODAY})
    for source in manifest["sources"]:
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed official candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", reason_for_new(identifier, candidate.get("title", ""))
                seen[identifier] = {"source_url": candidate["url"], "first_seen": TODAY}
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    positions.sort(key=lambda item: (item["kind"] != "phd", item["deadline"], -item["fit_score"], item["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["generated_at"] = f"{TODAY}T00:00:00+00:00"
    manifest["refresh_date"] = TODAY
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(item["status"] == "ok" for item in manifest["sources"]),
        "sources_failed": sum(item["status"] == "failed" for item in manifest["sources"]),
        "sources_empty": sum(item["status"] == "empty" for item in manifest["sources"]),
        "sources_dynamic": sum(item["status"] == "dynamic" for item in manifest["sources"]),
        "candidate_urls": len({url.rstrip("/") for item in manifest["sources"] for url in item.get("candidate_urls", [])}),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"new": NEW_POSITION["id"], "active": len(positions), "summary": manifest["summary"], "triage": {item["name"]: len(item["triage"]) for item in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
