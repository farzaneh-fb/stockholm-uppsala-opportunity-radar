from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ruamel.yaml import YAML
from build_test_report import build_report, render_position
DATA = ROOT / "data"
TODAY = "2026-09-22"

NEW_POSITIONS = [
    {
        "id": "KI_966651",
        "kind": "phd",
        "title": "Doctoral (PhD) student position in colorectal tumor immunology",
        "short_title": "colorectal_tumor_immunology",
        "organization": "Karolinska Institutet",
        "city": "Solna",
        "location_detail": "Department of Medicine, Solna",
        "found_date": TODAY,
        "new_date": TODAY,
        "published": "2026-09-05",
        "deadline": "2026-09-25",
        "employment": "Full-time doctoral studentship, up to 4 years",
        "fit_score": 91,
        "fit_label": "Excellent match with domain gaps",
        "description": "Translational colorectal-cancer immunology using human tissue, single-cell RNA sequencing, multicolour flow cytometry, tissue sectioning and spatial analyses.",
        "match_reasons": [
            "Documented cancer-cell culture, molecular-biology workflows and flow-cytometry experience align with the experimental setting",
            "Single-cell and spatial transcriptomics, Python/R analysis and reproducible workflows align with the project's data-generation and data-organisation needs",
            "Research publications and collaboration at KI, KTH and SciLifeLab support communication and multidisciplinary team work",
            "The project connects experimental tumour biology with computational analysis, matching the candidate's wet-lab-to-bioinformatics bridge"
        ],
        "gaps": [
            "Mucosal immunology, innate lymphoid-cell and T-cell specialisation are not explicitly documented in the master CV",
            "Human intestinal-tissue dissection and MACSima-platform experience are not explicitly documented",
            "Any claimed experience with colorectal cancer or lymphocyte assays must be supported by concrete evidence in the application"
        ],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:966651/type:job/where:4/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:966651/type:job/where:4/apply:1/",
        "contact": "Jenny Mjösberg — jenny.mjosberg@ki.se",
        "headline": "Biomedical Researcher | Cancer Biology, Single-Cell Analysis & Molecular Methods",
        "statement": "Biomedical researcher with a biology research and publication background, combining cancer-cell culture, molecular-biology methods and flow cytometry with growing bioinformatics skills. I use R, Python and reproducible workflows for single-cell and spatial transcriptomic data, and I am comfortable working between experimental and computational colleagues. I would bring this foundation to colorectal tumour immunology while developing deeper expertise in mucosal immunology, lymphocyte biology and human-tissue analysis.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"]
    },
    {
        "id": "KI_962593",
        "kind": "phd",
        "title": "Doctoral position in translational research on leukemia niche",
        "short_title": "translational_leukemia_niche",
        "organization": "Karolinska Institutet",
        "city": "Huddinge",
        "location_detail": "Department of Medicine, Huddinge, Center for Hematology and Regenerative Medicine",
        "found_date": TODAY,
        "new_date": TODAY,
        "published": "2026-08-25",
        "deadline": "2026-09-25",
        "employment": "Full-time doctoral studentship, up to 4 years",
        "fit_score": 84,
        "fit_label": "Strong match with method gaps",
        "description": "Translational acute-myeloid-leukaemia research on the bone-marrow niche and drug response using patient samples and mouse models, flow cytometry, confocal imaging, RNA sequencing and molecular assays.",
        "match_reasons": [
            "Master's-level biotechnology and medical-nanotechnology training provide a relevant biomedical foundation",
            "Documented cell culture, molecular-biology workflows, flow cytometry, imaging and cancer research are relevant to the project's experimental methods",
            "Sequencing-data analysis and reproducible bioinformatics workflows support the RNA-sequencing component",
            "Publications and cross-disciplinary research experience support scientific communication and collaborative work"
        ],
        "gaps": [
            "Haematology, acute myeloid leukaemia and bone-marrow-niche specialisation are not explicitly documented in the master CV",
            "Mouse-model, transplantation, lineage-tracing, CRISPR/Cas9 and droplet-digital-PCR experience are not explicitly documented",
            "The application must describe only substantiated cancer, cell-culture, imaging and molecular-method experience"
        ],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:962593/type:job/where:4/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:962593/type:job/where:4/apply:1/",
        "contact": "Hong Qian — hong.qian@ki.se",
        "headline": "Biomedical Researcher | Cancer Biology, Molecular Methods & Bioinformatics",
        "statement": "Biomedical researcher with a biology research and publication background, combining cancer-cell culture, molecular-biology methods, flow cytometry and imaging with current bioinformatics study. I use R and Python for reproducible sequencing-data analysis and work comfortably across experimental and computational research. I would bring this foundation to translational leukaemia research while developing specialised expertise in haematology, in-vivo models and functional stem-cell assays.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"]
    }
]


def stable_id(url: str) -> str:
    if "jobID:" in url:
        return "KI_" + url.split("jobID:", 1)[1].split("/", 1)[0]
    if "doktorand/" in url:
        return "SLU_2836"
    return "SLU_" + url.rstrip("/").split("/")[-1].upper().replace("-", "_")


def main() -> None:
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    manifest_path = DATA / "discovery_manifest.json"
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    existing = {p["id"] for p in positions}
    y = YAML()
    y.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
        master = y.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in existing:
            render_position(y, master, position)
            positions.append(position)
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    for p in NEW_POSITIONS:
        seen.setdefault(p["id"], {"source_url": p["source_url"], "first_seen": TODAY})
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    active = {p["id"] for p in positions}
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            candidate = {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/", "title": "PhD student in Arctic freshwater ecology"}
            urls = {x["url"].rstrip("/") for x in source.get("candidates", [])}
            if candidate["url"].rstrip("/") not in urls:
                source.setdefault("candidates", []).append(candidate)
                source.setdefault("candidate_urls", []).append(candidate["url"])
            source["reconciliation"] = "Client-rendered official index reconciled using the configured official-domain PhD query and direct official SLU pages. The live Uppsala PhD student in Arctic freshwater ecology (SLU.ua.2026.2.5.1-2836; deadline 12 October 2026) was triaged but not selected because the master CV does not document the required aquatic ecology, limnology or ecology degree."
        triage = []
        for c in source.get("candidates", []):
            ident = stable_id(c["url"]) if source["name"] in {"SLU vacancies", "Karolinska Institutet vacancies"} else None
            if ident in active:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif ident == "SLU_2836":
                status, reason = "not_selected", "Live official PhD vacancy reviewed; it requires an aquatic ecology, limnology, ecology or equivalent degree, which is not documented in the master CV."
            elif ident is None:
                # Preserve the correctly generated stable IDs for non-SLU/KI sources.
                previous = next((t for t in source.get("triage", []) if t["url"] == c["url"]), None)
                ident = previous["stable_id"] if previous else "UNRESOLVED"
                status, reason = (previous["status"], previous["reason"]) if previous else ("not_selected", "Official candidate reviewed; it did not clear the realistic-fit gate.")
            else:
                status, reason = "not_selected", "Official candidate reviewed; it is outside target scope, expired/unverified, duplicate discovery signal, or did not clear the realistic-fit gate."
            triage.append({"url": c["url"], "title": c.get("title", ""), "stable_id": ident, "status": status, "reason": reason})
        source["triage"] = triage
    manifest["refresh_date"] = TODAY
    manifest["summary"]["candidate_urls"] = len({u.rstrip("/") for s in manifest["sources"] for u in s.get("candidate_urls", [])})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [p["id"] for p in NEW_POSITIONS], "candidate_urls": manifest["summary"]["candidate_urls"]}))


if __name__ == "__main__":
    main()
