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
TODAY = "2026-09-30"

SLU_CANDIDATES = [
    {
        "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand",
        "title": "PhD student in Arctic freshwater ecology",
    }
]

NEW_POSITIONS = [
    {
        "id": "KI_969035",
        "kind": "phd",
        "title": "Doctoral (PhD) student position in T-cell biology in rheumatic diseases",
        "short_title": "t_cell_biology_rheumatic_diseases",
        "organization": "Karolinska Institutet",
        "city": "Solna",
        "location_detail": "Department of Medicine, Solna",
        "found_date": TODAY,
        "new_date": TODAY,
        "published": "2026-09-14",
        "deadline": "2026-10-05",
        "employment": "Full-time doctoral studentship, maximum 4 years",
        "fit_score": 91,
        "fit_label": "Excellent match with disease-area gaps",
        "description": "Investigate regulatory and tissue-resident memory T-cell biology in rheumatic diseases, cancer and immune-checkpoint-inhibitor-induced myositis using human samples, flow cytometry, single-cell sorting, immunofluorescence, in-vitro culture, molecular biology and bioinformatic analyses.",
        "match_reasons": [
            "The required cell-biology laboratory background is directly supported by documented cell culture, molecular-biology workflows, flow cytometry, fluorescence microscopy and immunohistochemistry.",
            "Documented R/Python, Linux, sequencing-analysis and reproducible workflow experience supports the advertised basic-bioinformatics requirement.",
            "Established publications, research presentations and collaborative work at KI, KTH and SciLifeLab support rigorous experimental practice, communication and interdisciplinary teamwork.",
            "Cancer-biology and translational research experience provide relevant context for a project spanning inflammation, cancer and human samples."
        ],
        "gaps": [
            "T-cell immunology, rheumatology and regulatory T-cell biology are not explicitly documented in the master CV.",
            "Primary human-cell work, single-cell sorting and full-spectrum or multi-parameter flow cytometry are not explicitly documented.",
            "The application should accurately foreground documented general flow-cytometry and cell-biology experience while explaining readiness to learn the specialised immune methods."
        ],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:969035/type:job/where:4/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:969035/type:job/where:4/apply:1/",
        "contact": "Karine Chemin — karine.chemin@ki.se",
        "headline": "Biomedical Researcher | Cell Biology, Molecular Methods & Bioinformatics",
        "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture, molecular-biology methods, flow cytometry, immunohistochemistry and fluorescence microscopy with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to T-cell biology while developing specialised expertise in immunology, rheumatology and primary human-cell research.",
        "section_order": [
            "Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education",
            "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects",
            "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills",
            "Teaching & Mentorship", "Awards & Honors", "References"
        ],
    }
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


def not_selected_reason(identifier: str, source_name: str) -> str:
    if identifier == "KI_969224":
        return "Live official PhD vacancy reviewed; required documented epidemiology, biostatistics and epidemiological-data experience are not established by the immutable master CV."
    if identifier == "KI_968887":
        return "Live official PhD vacancy reviewed; the position centres advanced epidemiology, longitudinal cohort analysis and causal inference, which are not documented in the immutable master CV."
    if identifier == "SLU_doktorand":
        return "Live official Uppsala PhD vacancy reviewed; the role requires aquatic-ecology background, field sampling and specialised food-web, chromatography and Bayesian-mixing-model methods not documented in the immutable master CV."
    if source_name == "SciLifeLab careers":
        return "Official SciLifeLab discovery item reviewed; it is a partner listing, duplicate of an official employer listing, outside the target geography/seniority gate, or lacks a live primary-employer application page."
    return "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    master_path = DATA / "master_profile" / "master_cv.yml"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    existing_ids = {p["id"] for p in positions}
    yaml = YAML()
    yaml.preserve_quotes = True
    with master_path.open(encoding="utf-8") as handle:
        master = yaml.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in existing_ids:
            render_position(yaml, master, position)
            positions.append(position)
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))

    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    active_ids = {p["id"] for p in positions}
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_CANDIDATES
            source["candidate_urls"] = [c["url"] for c in SLU_CANDIDATES]
            source["reconciliation"] = "Client-rendered official index reconciled on 2026-09-30 with the configured official-domain PhD query and direct official SLU vacancy page. Current Uppsala/Ultuna PhD candidates were inventoried and triaged."
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", not_selected_reason(identifier, source["name"])
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY})
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
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
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [p["id"] for p in NEW_POSITIONS], "phd": sum(p["kind"] == "phd" for p in positions), "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"], "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
