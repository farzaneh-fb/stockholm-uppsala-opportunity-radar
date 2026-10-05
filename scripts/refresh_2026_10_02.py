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
TODAY = "2026-10-02"
SLU_CANDIDATES = [
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand/", "title": "PhD student in Arctic freshwater ecology"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogspatologi/", "title": "PhD student in forest pathology: biotic risks to birch"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-teknologi/", "title": "PhD student in Technology - Accounting for Unexpected Events When Optimizing the Climate Effects of Broadleaf Tree Production"},
    {"url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-skogsskotsel/", "title": "PhD student in silviculture of planted birch"},
]

NEW_POSITION = {
    "id": "KI_971139", "kind": "phd", "title": "Doctoral (PhD) student position in proteomics and insulin resistance in metabolic disease", "short_title": "proteomics_insulin_resistance_metabolic_disease", "organization": "Karolinska Institutet", "city": "Solna", "location_detail": "Department of Microbiology, Tumor and Cell Biology", "found_date": TODAY, "new_date": TODAY, "published": "2026-09-18", "deadline": "2026-10-09", "employment": "Full-time doctoral studentship, maximum 4 years", "fit_score": 90, "fit_label": "Excellent match with proteomics/metabolism gaps",
    "description": "Use mass-spectrometry-based proteomics, metabolomics, quantitative analysis, bioinformatics and multi-omics integration to investigate adipocyte insulin resistance and its reversal after bariatric surgery.",
    "match_reasons": ["The advertised molecular-biology, mammalian-cell-culture and quantitative-biological-data-analysis foundation is supported by documented cell culture, molecular methods and R/Python-based reproducible analysis.", "Documented bioinformatics study, Linux, sequencing-data analysis and reproducible workflows provide a relevant bridge to large biological datasets and multi-omics integration.", "Established publications and interdisciplinary research experience support experiment planning, scientific communication, manuscript contribution and collaboration.", "The biomedical, molecular-biology and biotechnology background aligns with the position's stated subject areas."],
    "gaps": ["Mass-spectrometry-based proteomics, metabolomics and their sample preparation are not explicitly documented in the master CV.", "Metabolism, adipocyte biology, insulin signalling, obesity, type 2 diabetes, bariatric-surgery samples and plasma-proteomics experience are not explicitly documented.", "3D adipocyte spheroids, CRISPR/Cas9, gene silencing and functional metabolic assays are not explicitly documented; the application should frame these as methods to learn."],
    "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:971139/type:job/where:4/apply:1", "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:971139/type:job/where:4/apply:1/", "contact": "Amir Ata Saei — amir.saei@ki.se", "headline": "Biomedical Researcher | Molecular Biology, Cell Methods & Bioinformatics", "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture and molecular-biology methods with growing bioinformatics skills. I use R, Python, Linux and reproducible workflows to support scientific data analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to proteomics and metabolic-disease research while developing specialised expertise in mass-spectrometry-based omics, metabolomics and adipocyte biology.",
    "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
}


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
    slu_reasons = {
        "SLU_doktorand": "Live official SLU PhD vacancy reviewed; the role is outside the Stockholm/Solna/Uppsala/Ultuna geography and requires freshwater-ecology expertise not documented in the immutable master CV.",
        "SLU_doktorand_i_skogspatologi": "Live official SLU PhD vacancy reviewed; it is based in Alnarp and requires forest-management eligibility and forest-pathology/fieldwork experience not documented in the immutable master CV.",
        "SLU_doktorand_i_teknologi": "Live official SLU PhD vacancy reviewed; it is outside the target scope or requires forestry and technology expertise not documented in the immutable master CV.",
        "SLU_doktorand_i_skogsskotsel": "Live official SLU PhD vacancy reviewed; it is outside the target scope or requires forest-science and fieldwork expertise not documented in the immutable master CV.",
    }
    return slu_reasons.get(identifier, "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV.")


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = [p for p in json.loads(positions_path.read_text(encoding="utf-8")) if p["deadline"] >= TODAY]
    existing_ids = {p["id"] for p in positions}
    yaml = YAML(); yaml.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
        master = yaml.load(handle)
    if NEW_POSITION["id"] not in existing_ids:
        render_position(yaml, master, NEW_POSITION)
        positions.append(NEW_POSITION)
    positions.sort(key=lambda p: (p["kind"] != "phd", p["deadline"], -p["fit_score"], p["id"]))
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    active_ids = {p["id"] for p in positions}
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidates"] = SLU_CANDIDATES
            source["candidate_urls"] = [candidate["url"] for candidate in SLU_CANDIDATES]
            source["reconciliation"] = "Client-rendered official index was reconciled on 2026-10-02 using the configured official-domain PhD query and direct official SLU vacancy pages. The query exposed an incomplete index view; each discovered current official listing was inventoried and triaged."
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status, why = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, why = "seen_not_selected", "Previously reviewed candidate remains outside the active shortlist."
            else:
                status, why = "not_selected", not_selected_reason(identifier, source["name"])
            seen.setdefault(identifier, {"source_url": candidate["url"], "first_seen": TODAY})
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": why})
        source["triage"] = triage
    manifest["refresh_date"] = TODAY
    manifest["summary"] = {"sources_total": len(manifest["sources"]), "sources_ok": sum(s["status"] == "ok" for s in manifest["sources"]), "sources_dynamic": sum(s["status"] == "dynamic" for s in manifest["sources"]), "sources_failed": sum(s["status"] == "failed" for s in manifest["sources"]), "sources_empty": sum(s["status"] == "empty" for s in manifest["sources"]), "candidate_urls": len({c["url"].rstrip("/") for s in manifest["sources"] for c in s.get("candidates", [])})}
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [NEW_POSITION["id"]], "phd": sum(p["kind"] == "phd" for p in positions), "jobs": sum(p["kind"] == "job" for p in positions), "summary": manifest["summary"], "triage": {s["name"]: len(s.get("triage", [])) for s in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
