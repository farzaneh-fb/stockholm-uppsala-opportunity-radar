"""Audited daily refresh for 28 October 2026; never writes the master CV."""
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
TODAY = "2026-10-28"

# Official-domain reconciliation for the client-rendered SLU index. These pages
# were opened directly; all have past deadlines and are retained in the audit.
SLU_RECONCILIATION = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/phd-student-ddls-integrative-pangenomics-of-polyploids", "title": "PhD Student: DDLS integrative pangenomics of polyploids"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-de-novo-proteindesign", "title": "PhD students Protein Design"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand2", "title": "PhD student - Cyanobacteria and their Toxins in a Changing Climate"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-mikrobiella-strategier-for-hallbar-pfas-sanering", "title": "PhD student in microbial strategies for sustainable PFAS remediation"},
]

# Direct official-domain discovery from Stockholm University's Science Faculty.
# The two accepted listings were opened and verified individually.
SU_BACKFILL = [
    {"url": "https://su.varbi.com/what:job/jobID:971439/", "title": "PhD student in Bioinformatics — AI for Multimodal Biology and Microscopy"},
    {"url": "https://su.varbi.com/what:job/jobID:970261/", "title": "PhD student in Bioinformatics — AI-driven Multiscale Modelling of Membrane Protein Complexes"},
]

NEW_POSITIONS = [
    {
        "id": "UU_974072", "kind": "phd", "title": "PhD student position in Bioinformatics/Evolutionary Microbiology", "short_title": "bioinformatics_evolutionary_microbiology", "organization": "Uppsala University", "city": "Uppsala", "location_detail": "Department of Medical Biochemistry and Microbiology, Biomedical Centre", "found_date": TODAY, "new_date": TODAY, "published": "2026-09-30", "deadline": "2026-10-29", "employment": "Full-time doctoral employment, temporary", "fit_score": 82, "fit_label": "Strong interdisciplinary match",
        "description": "Reconstruct the evolutionary history, metabolic potential and host-adaptation genes of deep-branching intracellular Gammaproteobacteria using genomes, metagenomics and evolutionary analysis.",
        "match_reasons": ["Master's-level biotechnology/nanotechnology training and molecular-biology research align with the stated degree backgrounds", "Documented Python/R, Linux and reproducible scientific-data workflows support the required coding component", "Research publications, independent project work and experimental molecular-biology experience support the doctoral research setting"],
        "gaps": ["Metagenomics and molecular-evolution method development are not documented as established specialisms", "The application should describe microbial-evolution motivation honestly rather than imply prior Legionella research"],
        "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=974072", "apply_url": "https://uu.varbi.com/en/what:login/type:job/jobID:974072", "contact": "Associate Professor Lionel Guy — lionel.guy@imbim.uu.se", "headline": "Bioinformatics & Molecular Biology Researcher | Genomics, Reproducible Analysis and Experimental Science", "statement": "Interdisciplinary researcher with a background in molecular biology, biotechnology and current bioinformatics training. I combine experimental research and scientific publication experience with Python/R-based analysis, Linux and reproducible workflows. I am motivated to develop deeper expertise in comparative genomics, metagenomics and molecular evolution, while contributing careful data analysis and practical understanding of biological experiments to a collaborative microbiology research environment.",
        "section_order": ["Personal Statement", "Education", "Bioinformatics & Computational Biology Projects", "Computational Biology & Bioinformatics Skills", "Research Experience", "Wet Lab & Experimental Expertise", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "SU_970261", "kind": "phd", "title": "PhD student in Bioinformatics — AI-driven Multiscale Modelling of Membrane Protein Complexes", "short_title": "bioinformatics_membrane_protein_complexes", "organization": "Stockholm University", "city": "Stockholm", "location_detail": "Department of Biochemistry and Biophysics, SciLifeLab", "found_date": TODAY, "new_date": TODAY, "published": "2026-10-13", "deadline": "2026-11-03", "employment": "Full-time doctoral employment, temporary", "fit_score": 78, "fit_label": "Relevant stretch match",
        "description": "Develop deep-learning-based multiscale models of membrane protein complexes, integrating proteomics, glycoproteomics, structural mass spectrometry and lipidomics with experimental collaborators.",
        "match_reasons": ["Bioinformatics training, Python/R work and reproducible scientific workflows provide a credible computational foundation", "Molecular-biology, cancer-biology and omics experience offer relevant biological context for proteomic and membrane-biology collaboration", "Published research and cross-disciplinary work at KI, KTH and SciLifeLab support doctoral-level scientific communication"],
        "gaps": ["Deep-learning, AlphaFold-based structural modelling and membrane-protein modelling are not documented as established experience", "The application should frame these as skills to develop, not claim advanced machine-learning expertise"],
        "source_url": "https://su.varbi.com/what:job/jobID:970261/", "apply_url": "https://su.varbi.com/what:job/jobID:970261/", "contact": "Professor Arne Elofsson — arne.elofsson@dbb.su.se", "headline": "Bioinformatics & Molecular Biology Researcher | Omics, Reproducible Analysis and Interdisciplinary Science", "statement": "Interdisciplinary researcher bridging molecular biology and bioinformatics, with experience in scientific programming, reproducible analysis and experimental life science. My research and current bioinformatics training have developed my ability to work with biological data in Python and R and to communicate across experimental and computational teams. I am motivated to build specialised expertise in structural bioinformatics and machine learning while contributing a careful biological perspective to collaborative multi-omics research.",
        "section_order": ["Personal Statement", "Education", "Bioinformatics & Computational Biology Projects", "Computational Biology & Bioinformatics Skills", "Research Experience", "Wet Lab & Experimental Expertise", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
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


def triage_reason(identifier: str) -> str:
    if identifier == "SU_971439":
        return "Official vacancy reviewed but not accepted: it requires solid machine-learning including deep-learning experience, which is not documented in the immutable master CV."
    if identifier == "KI_977931":
        return "Official vacancy reviewed but not accepted: it requires clinical training and Swedish clinical-care experience not documented in the immutable master CV."
    if identifier.startswith("SLU_"):
        return "Official SLU listing opened during dynamic-index reconciliation; its published deadline has passed."
    return "Official candidate triaged; it is expired, outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."


def main() -> None:
    manifest_path, seen_path, positions_path = DATA / "discovery_manifest.json", DATA / "seen_positions.json", DATA / "positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    existing_ids = {p["id"] for p in positions}
    yaml_engine = YAML(); yaml_engine.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
        master = yaml_engine.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in existing_ids:
            render_position(yaml_engine, master, position)
            positions.append(position)
            existing_ids.add(position["id"])
        seen.setdefault(position["id"], {"source_url": position["source_url"], "first_seen": TODAY})

    for source in manifest["sources"]:
        extras = []
        if source["name"] == "SLU vacancies":
            extras = SLU_RECONCILIATION
            source["reconciliation"] = "Dynamic official index reconciled on 2026-10-28 through the registry official-domain query; four relevant official Uppsala/Ultuna listings were opened directly and all had passed deadlines."
        if source["name"] == "Stockholm University MBW vacancies":
            extras = SU_BACKFILL
            source["official_domain_backfill"] = "Official Stockholm University domain query identified two current bioinformatics vacancies; both official Varbi pages were opened directly."
        candidates = source.get("candidates", []) + [item for item in extras if item["url"] not in {x["url"] for x in source.get("candidates", [])}]
        if extras:
            source["reconciled_candidates"] = extras
        triage = []
        for candidate in candidates:
            identifier = stable_id(candidate["url"])
            status = "active_existing" if identifier in existing_ids else "not_selected"
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": "Live official vacancy re-verified and retained in the active report." if status == "active_existing" else triage_reason(identifier)})
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY})
        source["triage"] = triage

    manifest["refresh_date"] = TODAY
    all_urls = {c["url"].rstrip("/") for s in manifest["sources"] for c in (s.get("candidates", []) + s.get("reconciled_candidates", []))}
    manifest["summary"] = {"sources_total": len(manifest["sources"]), "sources_ok": sum(s["status"] == "ok" for s in manifest["sources"]), "sources_dynamic": sum(s["status"] == "dynamic" for s in manifest["sources"]), "sources_failed": sum(s["status"] == "failed" for s in manifest["sources"]), "sources_empty": sum(s["status"] == "empty" for s in manifest["sources"]), "candidate_urls": len(all_urls)}
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [p["id"] for p in NEW_POSITIONS], "phd": sum(p["kind"] == "phd" for p in positions), "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"], "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
