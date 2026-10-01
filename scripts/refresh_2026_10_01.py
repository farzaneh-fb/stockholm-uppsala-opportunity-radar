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
TODAY = "2026-10-01"

NEW_POSITIONS = [
    {
        "id": "KI_970686", "kind": "phd", "title": "PhD student position in Extracellular Vesicles in Cardiovascular Disease", "short_title": "extracellular_vesicles_cardiovascular_disease", "organization": "Karolinska Institutet", "city": "Stockholm", "location_detail": "Department of Laboratory Medicine, Division of Clinical Chemistry", "found_date": TODAY, "new_date": TODAY, "published": "2026-09-23", "deadline": "2026-10-07", "employment": "Full-time doctoral studentship, maximum 4 years", "fit_score": 88, "fit_label": "Strong match with cardiovascular-method gaps",
        "description": "Experimental and translational cardiovascular research on extracellular vesicles, combining human plasma samples, flow cytometry, imaging, omics, primary-cell studies and bioinformatic analysis.",
        "match_reasons": ["Documented cell culture, molecular-biology workflows, flow cytometry, fluorescence microscopy and immunohistochemistry align with the experimental core of the project.", "Documented R/Python, Linux, sequencing analysis and reproducible workflows support the advertised quantitative and bioinformatic components.", "Established publications and interdisciplinary research experience support scientific writing, careful documentation and collaboration.", "The project’s translational molecular-biology setting is compatible with the documented biomedical research background."],
        "gaps": ["Cardiovascular disease, lipid and lipoprotein metabolism, extracellular-vesicle isolation and clinical cohort-data analysis are not explicitly documented in the master CV.", "Human plasma handling, ultracentrifugation, lipidomics, proteomics and primary-cell studies are not explicitly documented.", "The application should foreground documented cell and molecular methods without claiming specialised extracellular-vesicle or cardiovascular experience."],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:970686/type:job/where:4/apply:1", "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:970686/type:job/where:4/apply:1/", "contact": "Uwe Tietge — uwe.tietge@ki.se", "headline": "Biomedical Researcher | Cell Biology, Molecular Methods & Bioinformatics", "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture, molecular-biology methods, flow cytometry, immunohistochemistry and fluorescence microscopy with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to extracellular-vesicle research while developing specialised expertise in cardiovascular biology, plasma-based assays and omics integration.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KTH_970376", "kind": "phd", "title": "Doctoral student in next-generation targeted biotherapeutics", "short_title": "next_generation_targeted_biotherapeutics", "organization": "KTH Royal Institute of Technology", "city": "Stockholm", "location_detail": "School of Engineering Sciences in Chemistry, Biotechnology and Health", "found_date": TODAY, "new_date": TODAY, "published": "2026-10-01", "deadline": "2026-10-10", "employment": "Full-time doctoral employment, up to 4 years", "fit_score": 86, "fit_label": "Strong match with protein-engineering gaps",
        "description": "Develop protein-based drug candidates for diagnostics and therapy using directed evolution, protein libraries and cell-display methods, focused on neurodegenerative diseases.",
        "match_reasons": ["Documented biotechnology and molecular-biology training, cell culture and flow cytometry provide a relevant experimental foundation.", "Documented cancer-biology and translational-research experience supports work in a therapeutic and diagnostics-oriented setting.", "Research publications and collaborative work at KI, KTH and SciLifeLab support independent research and scientific communication.", "R/Python-based reproducible analysis provides a useful complementary quantitative skill set."],
        "gaps": ["Directed evolution, cell-display methods, recombinant protein production and purification, and affinity-protein characterisation are not explicitly documented in the master CV.", "Blood-brain-barrier and neurodegenerative-disease research are not explicitly documented.", "The application should accurately present general molecular and flow-cytometry experience while stating readiness to learn protein-engineering methods."],
        "source_url": "https://www.kth.se/lediga-jobb/970376?l=en", "apply_url": "https://kth.varbi.com/en/apply/positionquick/970376/?where=4", "contact": "John Löfblom — see official KTH advert", "headline": "Biomedical Researcher | Molecular Biology, Cell Methods & Bioinformatics", "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture, molecular-biology methods and flow cytometry with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to targeted biotherapeutics while developing specialised expertise in directed evolution, cell-display methods and protein engineering.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KTH_967413", "kind": "phd", "title": "Doctoral student in Biotechnology", "short_title": "biotechnology_protein_engineering", "organization": "KTH Royal Institute of Technology", "city": "Stockholm", "location_detail": "Department of Protein Technology", "found_date": TODAY, "new_date": TODAY, "published": "2026-10-01", "deadline": "2026-10-10", "employment": "Full-time doctoral employment, up to 4 years", "fit_score": 80, "fit_label": "Relevant match with protein-production gaps",
        "description": "Study calcium-regulated affinity binders through protein engineering, biophysical characterisation, structural biology, computational modelling and machine learning.",
        "match_reasons": ["Master’s-level biotechnology training and documented molecular-biology laboratory experience provide a relevant foundation.", "Growing bioinformatics skills, R/Python analysis and reproducible workflows support the computational-modelling and machine-learning environment.", "Established research publications and interdisciplinary collaboration support doctoral research readiness and scientific communication."],
        "gaps": ["Protein production, purification, protein engineering, biophysical characterisation and structural biology are not explicitly documented in the master CV.", "The specific calcium-regulated affinity-binder research area is not documented.", "The application should not claim protein-engineering experience and should explain motivation to build this expertise."],
        "source_url": "https://www.kth.se/lediga-jobb/967413?l=en", "apply_url": "https://kth.varbi.com/en/apply/positionquick/967413/?where=4", "contact": "Sophia Hober — see official KTH advert", "headline": "Biomedical Researcher | Biotechnology, Molecular Methods & Bioinformatics", "statement": "Biomedical researcher with an established biology research and publication background, combining molecular-biology and cell-culture experience with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I work comfortably between experimental and computational colleagues. I would bring this interdisciplinary foundation to biotechnology research while developing specialised expertise in protein production, engineering and biophysical characterisation.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
]


def stable_id(url: str) -> str:
    if "jobID:" in url:
        n = re.search(r"jobID:(\d+)", url).group(1)
        return "SU_" + n if "su.varbi" in url else "UU_" + n if "uu.varbi" in url else "KI_" + n
    if m := re.search(r"lediga-jobb/(\d+)", url): return "KTH_" + m.group(1)
    if m := re.search(r"query=(\d+)", url): return "UU_" + m.group(1)
    if "scilifelab.se/career/" in url: return "SCILIFE_" + url.rstrip("/").rsplit("/", 1)[-1]
    return "SLU_" + re.sub(r"[^a-z0-9]+", "_", url.lower().rstrip("/").rsplit("/", 1)[-1]).strip("_")


def reason(identifier: str, source: str) -> str:
    specific = {
        "UU_970239": "Live official PhD vacancy reviewed; its required battery-energy-storage knowledge and battery-electrochemistry experience are not established by the immutable master CV.",
        "UU_962817": "Live official PhD vacancy reviewed; demonstrated complement-system and innate-immunity research is a stated requirement and is not documented in the immutable master CV.",
    }
    return specific.get(identifier, "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV.")


def main() -> None:
    manifest_path, positions_path, seen_path = DATA / "discovery_manifest.json", DATA / "positions.json", DATA / "seen_positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    existing = {p["id"] for p in positions}
    yaml = YAML(); yaml.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as f: master = yaml.load(f)
    for p in NEW_POSITIONS:
        if p["id"] not in existing:
            render_position(yaml, master, p)
            positions.append(p)
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    seen = json.loads(seen_path.read_text(encoding="utf-8")); active = {p["id"] for p in positions}
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["reconciliation"] = "Client-rendered official index reconciled on 2026-10-01 with the configured official-domain PhD query and direct official SLU listings. No live Uppsala/Ultuna PhD listing meeting the target scope was verified."
        triage = []
        for c in source.get("candidates", []):
            identifier = stable_id(c["url"])
            if identifier in active: status, why = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen: status, why = "seen_not_selected", "Previously reviewed candidate remains outside the active shortlist."
            else: status, why = "not_selected", reason(identifier, source["name"])
            seen.setdefault(identifier, {"source_url": c["url"], "first_seen": TODAY})
            triage.append({"url": c["url"], "title": c.get("title", ""), "stable_id": identifier, "status": status, "reason": why})
        source["triage"] = triage
    manifest["refresh_date"] = TODAY
    manifest["summary"] = {"sources_total": len(manifest["sources"]), "sources_ok": sum(s["status"] == "ok" for s in manifest["sources"]), "sources_dynamic": sum(s["status"] == "dynamic" for s in manifest["sources"]), "sources_failed": sum(s["status"] == "failed" for s in manifest["sources"]), "sources_empty": sum(s["status"] == "empty" for s in manifest["sources"]), "candidate_urls": len({c["url"].rstrip("/") for s in manifest["sources"] for c in s.get("candidates", [])})}
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [p["id"] for p in NEW_POSITIONS], "phd": sum(p["kind"] == "phd" for p in positions), "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"], "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]}}, ensure_ascii=False))

if __name__ == "__main__": main()
