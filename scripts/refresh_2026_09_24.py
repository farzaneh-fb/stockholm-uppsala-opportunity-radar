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
TODAY = "2026-09-24"
SLU_PREFIX = "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/"
SLU_CANDIDATES = [
    ("PhD student in Arctic freshwater ecology", "doktorand/"),
    ("Researcher in Food Control Literature Review", "forskare-for-litteratursammanstallning-inom-livsmedelskontroll-/"),
    ("Research Coordinator", "forskningskoordinator/"),
    ("PhD Student in Landscape Governance and Management", "doktorand-i-landskapets-governance-och-forvaltning/"),
    ("Small Animal Veterinarian – Department of Clinical Sciences and Small Animal Department, UDS", "klinikveterinar-smadjursavd/"),
    ("Senior lecturer in dairy cow management", "universitetslektor-i-skotsel-av-mjolkkor/"),
    ("Postdoc in Chromatin Dynamics During Extreme Desiccation Tolerance", "postdoc-i-kromatindynamik-vid-extrem-uttorkningstolerans/"),
    ("Senior Lecturer in horticultural genomics and breeding", "universitetslektor-i-hortikulturell-genomik-och-foradling/"),
    ("Senior Lecturer/Associate Professor in Small Animal Surgery", "universitetslektor-i-smadjurskirurgi/"),
    ("Senior Lecturer/Associate Professor in Animal Reproduction", "universitetslektor-i-husdjursreproduktion/"),
    ("PhD student in Technology - Accounting for Unexpected Events When Optimizing the Climate Effects of Broadleaf Tree Production", "doktorand-i-teknologi/"),
    ("Postdoctoral position in freshwater ecology and climate change", "postdoktor-sotvattensekologi-/"),
    ("PhD Student position in Biology, specialisation in Environmental Science", "doktorand-i-biologi/"),
    ("Postdoctoral Researcher: Psychology of Forest Management and Biodiversity", "postdoktor---tillampad-ekonomi/"),
    ("Senior Lecturer in Digitalisation of Agriculture", "universitetslektor-i-lantbrukets-digitalisering/"),
    ("Professor (full tenure) in animal ecology", "professor-i-zooekologi/"),
]
NEW_POSITION = {
    "id": "KI_966583",
    "kind": "phd",
    "title": "PhD candidate in molecular and circuit mechanisms of learning and memory",
    "short_title": "molecular_circuit_learning_memory",
    "organization": "Karolinska Institutet",
    "city": "Solna",
    "location_detail": "Department of Medical Biochemistry and Biophysics, Biomedicum",
    "found_date": TODAY,
    "new_date": TODAY,
    "published": "2026-09-04",
    "deadline": "2026-09-29",
    "employment": "Full-time doctoral studentship, up to 4 years",
    "fit_score": 78,
    "fit_label": "Good stretch match with method gaps",
    "description": "Use engineered proteins to study molecular signalling and neuronal circuits in the mouse brain, leading experimental design, experimentation, analysis and scientific presentation/publication.",
    "match_reasons": [
        "Master's-level biotechnology and medical-nanotechnology training provide a relevant biological and biomedical foundation",
        "Documented molecular-biology workflows, cell culture, imaging and experimental research support the laboratory component",
        "Research publications and collaborative work at KI, KTH and SciLifeLab support experimental planning, analysis and scientific communication",
        "Python/R-based reproducible analysis provides a useful quantitative complement in an interdisciplinary research environment",
    ],
    "gaps": [
        "Electrophysiology is desirable in the advert but is not explicitly documented in the master CV",
        "Mouse-brain, neuronal-circuit and protein-engineering experience are not explicitly documented",
        "The application should present only substantiated molecular and experimental skills while explaining motivation to learn the specialised methods",
    ],
    "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:966583/type:job/where:4/apply:1",
    "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:966583/type:job/where:4/apply:1/",
    "contact": "Onur Dagliyan — onur.dagliyan@ki.se",
    "headline": "Biomedical Researcher | Molecular Biology, Imaging & Reproducible Analysis",
    "statement": "Biomedical researcher with a biology research and publication background, combining molecular-biology methods, cell culture and imaging with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I am comfortable working between experimental and computational colleagues. I would bring this foundation to molecular neurobiology while developing specialised expertise in protein engineering, electrophysiology and neuronal-circuit research.",
    "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
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


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slu = next(item for item in manifest["sources"] if item["name"] == "SLU vacancies")
    slu["candidates"] = [{"title": title, "url": SLU_PREFIX + slug} for title, slug in SLU_CANDIDATES]
    slu["candidate_urls"] = [item["url"] for item in slu["candidates"]]
    slu["reconciliation"] = "The client-rendered official SLU index was reconciled on 2026-09-24 using the configured official-domain PhD query and direct official index retrieval. All 16 current official listings were inventoried; the four PhD listings were reviewed and the Uppsala Arctic freshwater ecology listing was opened directly."

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
            elif identifier == "SLU_DOKTORAND":
                status, reason = "not_selected", "Live Uppsala PhD vacancy reviewed; it requires aquatic ecology, limnology, ecology or equivalent, which is not documented in the master CV."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed official candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."
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
