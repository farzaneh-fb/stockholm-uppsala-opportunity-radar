from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import build_report, render_position  # noqa: E402

DATA = ROOT / "data"
TODAY = date(2026, 10, 8)

SLU_CANDIDATES = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogsskotsel/", "title": "PhD student in silviculture of planted birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand----resilienta-vallproduktionssystem/", "title": "PhD student in resilient forage production systems"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogspatologi/", "title": "PhD student in forest pathology: biotic risks to birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/", "title": "PhD student in Arctic freshwater ecology"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-landskapets-governance-och-forvaltning/", "title": "PhD Student in Landscape Governance and Management"},
]

SECTION_ORDER = [
    "Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education",
    "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects",
    "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills",
    "Teaching & Mentorship", "Awards & Honors", "References",
]

NEW_POSITIONS = [
    {
        "id": "KI_972393", "kind": "phd", "title": "Doctoral (PhD) student position in Epigenetics, Bioinformatics and Neuroimmunology",
        "short_title": "epigenetics_bioinformatics_neuroimmunology", "organization": "Karolinska Institutet", "city": "Stockholm",
        "location_detail": "Department of Clinical Neuroscience", "found_date": TODAY.isoformat(), "new_date": TODAY.isoformat(),
        "published": "2026-09-24", "deadline": "2026-10-15", "employment": "Full-time doctoral studentship, maximum 4 years",
        "fit_score": 92, "fit_label": "Excellent match with neuroimmunology-method gaps",
        "description": "Study cell-free DNA in neurological conditions by generating high-throughput sequencing data and developing computational and statistical analyses integrated with molecular and clinical information.",
        "match_reasons": [
            "Documented molecular-biology and cell-culture research, together with R, Python, Linux and reproducible workflow experience, matches the project's experimental and computational components.",
            "Documented sequencing analysis, scientific-data workflows and bioinformatics study provide a relevant basis for high-throughput data processing, statistics and visualisation.",
            "Established publications and interdisciplinary research experience support scientific writing, presentations and collaboration across experimental, clinical and computational colleagues.",
        ],
        "gaps": [
            "DNA-methylation, cell-free-DNA and neuroimmunology experience are not explicitly documented in the master CV.",
            "Single-cell RNA-seq analysis, machine learning and cell-type deconvolution are listed as advantages in the advert but are not established as completed specialist experience in the master CV.",
            "The application should foreground documented molecular and bioinformatics foundations while presenting these specialised methods as areas to develop.",
        ],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:972393/type:job/where:4/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:972393/type:job/where:4/apply:1/",
        "contact": "Maria Needhamsen — maria.needhamsen@ki.se; Maja Jagodic — maja.jagodic@ki.se",
        "headline": "Biomedical Researcher | Molecular Biology, Bioinformatics & Reproducible Analysis",
        "statement": "Biomedical researcher with an established biology research and publication background, combining molecular and cell-biology research with growing bioinformatics skills. I use R, Python, Linux and reproducible workflows to support scientific data analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to epigenetics and neuroimmunology research while developing specialised experience in cell-free DNA, high-throughput sequencing and clinical data integration.",
        "section_order": SECTION_ORDER,
    },
    {
        "id": "UU_971888", "kind": "phd", "title": "Doktorand inom immunofysiologi", "short_title": "immunophysiology_regenerative_healing",
        "organization": "Uppsala University", "city": "Uppsala", "location_detail": "Department of Medical Cell Biology",
        "found_date": TODAY.isoformat(), "new_date": TODAY.isoformat(), "published": "2026-09-22", "deadline": "2026-10-16",
        "employment": "Full-time doctoral employment, 4 years", "fit_score": 84, "fit_label": "Strong match with in-vivo-method gaps",
        "description": "Investigate cellular and molecular mechanisms distinguishing regenerative healing from fibrotic tissue repair using myocardial-infarction and endometrial-fibrosis models, single-cell sequencing and tissue characterisation.",
        "match_reasons": [
            "Documented molecular biology, cell culture, flow cytometry, fluorescence microscopy and immunohistochemistry support the project's cell and tissue-biology foundation.",
            "Documented R/Python, Linux, sequencing analysis and reproducible workflows provide a relevant bridge to the single-cell sequencing component.",
            "Established biology research, publications and interdisciplinary collaboration support research independence, scientific communication and team-based work.",
        ],
        "gaps": [
            "Mouse handling, anaesthesia, dissection and intravital confocal microscopy are not documented in the master CV.",
            "Advanced flow cytometry, immunophysiology, regenerative healing and fibrosis research are not explicitly documented.",
            "The application should present documented cell, molecular and computational experience accurately and describe the in-vivo methods as skills to learn.",
        ],
        "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=971888",
        "apply_url": "https://uu.varbi.com/se/what:login/type:job/jobID:971888",
        "contact": "Mia Phillipson — mia.phillipson@mcb.uu.se",
        "headline": "Biomedical Researcher | Cell Biology, Molecular Methods & Bioinformatics",
        "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture, molecular-biology methods, flow cytometry, immunohistochemistry and fluorescence microscopy with growing bioinformatics skills. I use R, Python, Linux and reproducible workflows to support scientific data analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to immunophysiology and tissue-repair research while developing specialised in-vivo and advanced imaging methods.",
        "section_order": SECTION_ORDER,
    },
]


def stable_id(url: str) -> str:
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
    if "scilifelab.se/career/" in url:
        return "SCILIFE_" + url.rstrip("/").rsplit("/", 1)[-1]
    return "SLU_" + re.sub(r"[^a-z0-9]+", "_", url.lower().rstrip("/").rsplit("/", 1)[-1]).strip("_")


def rejection_reason(identifier: str) -> str:
    if identifier.startswith("SLU_"):
        return "Live official SLU vacancy reviewed through required official-domain reconciliation; it is outside the target geography or requires forest, crop, aquatic-ecology or landscape-governance qualifications not documented in the immutable master CV."
    if identifier == "KI_972121":
        return "Live official vacancy reviewed; the senior bioinformatician role requires a PhD/equivalent expertise and demonstrated excellence in computational biology and single-cell RNA transcriptomics beyond the documented master-CV record."
    if identifier == "KTH_976709":
        return "Live official vacancy reviewed; the postdoctoral role requires a doctoral degree and specialised sustainable-electrochemical-systems experience not documented in the immutable master CV."
    return "Official candidate reviewed; it is outside the target scope, does not clear the realistic-fit gate, is expired, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY.isoformat()]
    existing_ids = {p["id"] for p in positions}
    yaml = YAML()
    yaml.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
        master = yaml.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in existing_ids:
            render_position(yaml, master, position)
            positions.append(position)
            existing_ids.add(position["id"])

    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_CANDIDATES
            source["candidate_urls"] = [item["url"] for item in SLU_CANDIDATES]
            source["reconciliation"] = "Client-rendered official index reconciled on 2026-10-08 using the configured official-domain PhD query. Each current official doctoral listing returned for the Uppsala/Ultuna signal was opened directly, inventoried and triaged."
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in existing_ids:
                status, reason = "active_existing", "Live official vacancy verified and retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", rejection_reason(identifier)
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY.isoformat()})
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    manifest["refresh_date"] = TODAY.isoformat()
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(s["status"] == "ok" for s in manifest["sources"]),
        "sources_dynamic": sum(s["status"] == "dynamic" for s in manifest["sources"]),
        "sources_failed": sum(s["status"] == "failed" for s in manifest["sources"]),
        "sources_empty": sum(s["status"] == "empty" for s in manifest["sources"]),
        "candidate_urls": len({c["url"].rstrip("/") for s in manifest["sources"] for c in s.get("candidates", [])}),
    }
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY.isoformat()), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [p["id"] for p in NEW_POSITIONS], "phd": sum(p["kind"] == "phd" for p in positions), "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"], "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
