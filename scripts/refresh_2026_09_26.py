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
TODAY = "2026-09-26"

NEW_POSITIONS = [
    {
        "id": "KI_967444",
        "kind": "phd",
        "title": "Doctoral (PhD) student position in Neuropsychoimmunology",
        "short_title": "neuropsychoimmunology",
        "organization": "Karolinska Institutet",
        "city": "Stockholm",
        "location_detail": "Neuropsychoimmunology Unit, Karolinska Institutet",
        "found_date": TODAY,
        "new_date": TODAY,
        "published": "2026-09-09",
        "deadline": "2026-09-30",
        "employment": "Full-time doctoral studentship, maximum 4 years",
        "fit_score": 87,
        "fit_label": "Strong match with neuroscience-method gaps",
        "description": "Investigate molecular and cellular mechanisms relevant to brain function and psychiatric disorders using cell culture, molecular biology, immunohistochemistry, imaging and biochemical analyses.",
        "match_reasons": [
            "Documented cell culture, molecular-biology workflows, immunostaining and microscopy align with the advertised laboratory methods",
            "Biomedical and biotechnology training plus an established research-publication record provide a relevant foundation for doctoral research",
            "R/Python-based reproducible analysis and experience working across experimental and computational colleagues support data analysis and collaboration",
            "The advert lists cell culture, molecular biology, immunohistochemistry and microscopy as advantageous experience, all represented in the master CV",
        ],
        "gaps": [
            "Neuropsychoimmunology, psychiatric-disorder and neuronal-function specialisation are not explicitly documented in the master CV",
            "Electrophysiology, in-vivo approaches and mass-spectrometry experience are not explicitly documented",
            "The application should accurately connect existing molecular and cell-biology experience to the project without claiming neuroscience-specific methods",
        ],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:967444/type:job/where:4/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:967444/type:job/where:4/apply:1/",
        "contact": "Funda Orhan — funda.orhan@ki.se",
        "headline": "Biomedical Researcher | Molecular Biology, Cell Culture & Reproducible Analysis",
        "statement": "Biomedical researcher with an established biology research and publication background, combining cell culture, molecular-biology methods, immunostaining and microscopy with growing bioinformatics skills. I use R, Python and reproducible workflows to support scientific analysis, and I work comfortably between experimental and computational colleagues. I would bring this foundation to neuropsychoimmunology while developing specialised expertise in neuroscience, electrophysiology and psychiatric research.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "UU_972267",
        "kind": "phd",
        "title": "PhD student in Machine Learning with a focus on mathematical and statistical methods for uncertainty quantification",
        "short_title": "ml_uncertainty_quantification",
        "organization": "Uppsala University",
        "city": "Uppsala",
        "location_detail": "Department of Information Technology, Division of Systems and Control",
        "found_date": TODAY,
        "new_date": TODAY,
        "published": "2026-09-23",
        "deadline": "2026-10-16",
        "employment": "Full-time doctoral employment",
        "fit_score": 62,
        "fit_label": "Exploratory stretch match",
        "description": "Develop mathematical and statistical uncertainty-quantification methods and apply them to large-scale clinical cancer data within the DDLS precision-medicine programme.",
        "match_reasons": [
            "Current bioinformatics study, Python/R analysis and reproducible workflows provide relevant computational foundations",
            "Cancer-biology and biomedical research experience gives useful context for the clinical-cancer-data application",
            "Research publications and interdisciplinary work support scientific communication and collaborative doctoral research",
            "The DDLS precision-medicine context aligns with the candidate's aim to bridge experimental biology and computational analysis",
        ],
        "gaps": [
            "The advertised degree background emphasises applied mathematics, statistics, engineering physics, physics or machine learning; equivalence is not established by the master CV",
            "Strong foundations in linear algebra, probability theory, calculus, Bayesian statistics and mathematical modelling are not explicitly documented",
            "The application should present this as a transition into mathematical-method development and substantiate any quantitative coursework or projects with evidence",
        ],
        "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=972267",
        "apply_url": "https://uu.varbi.com/en/what:login/type:job/jobID:972267",
        "contact": "Sara Hamis — sara.hamis@it.uu.se",
        "headline": "Biomedical Researcher | Bioinformatics, Cancer Biology & Reproducible Analysis",
        "statement": "Biomedical researcher with an established biology research and publication background and growing bioinformatics skills. I use R, Python and reproducible workflows for scientific data analysis, and I am comfortable working between experimental and computational colleagues. I would bring this life-science perspective to uncertainty quantification for clinical cancer data while building deeper foundations in probability, statistics and mathematical modelling.",
        "section_order": ["Personal Statement", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Research Experience", "Wet Lab & Experimental Expertise", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
]

SLU_BIOGAS = {
    "url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/2-doktorander-i-biogasprocessen/",
    "title": "Two PhD Positions in Biogas Process Development and Microbiology",
}


def stable_id(url: str) -> str:
    match = re.search(r"jobID:(\d+)", url)
    if match:
        if "su.varbi" in url:
            return "SU_" + match.group(1)
        if "uu.varbi" in url:
            return "UU_" + match.group(1)
        return "KI_" + match.group(1)
    match = re.search(r"lediga-jobb/(\d+)", url)
    if match:
        return "KTH_" + match.group(1)
    match = re.search(r"query=(\d+)", url)
    if match:
        return "UU_" + match.group(1)
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    return "SLU_" + re.sub(r"[^A-Z0-9]+", "_", slug.upper()).strip("_")


def not_selected_reason(identifier: str, title: str) -> str:
    if identifier == "SLU_2_DOKTORANDER_I_BIOGASPROCESSEN":
        return "Official SLU page was opened through dynamic-source reconciliation; the page's reported 31 August 2026 deadline has passed."
    if "POSTDOC" in title.upper() or "PROFESSOR" in title.upper() or "LECTURER" in title.upper():
        return "Official candidate reviewed; senior or postdoctoral eligibility is not documented in the immutable master CV."
    return "Official candidate reviewed; it is outside target scope, does not clear the realistic-fit gate, or requires qualifications not documented in the immutable master CV."


def add_candidate(source: dict, candidate: dict) -> None:
    candidates = source.setdefault("candidates", [])
    if not any(item["url"].rstrip("/") == candidate["url"].rstrip("/") for item in candidates):
        candidates.append(candidate)
    source["candidate_urls"] = [item["url"] for item in candidates]


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_by_name = {item["name"]: item for item in manifest["sources"]}
    add_candidate(source_by_name["Uppsala University PhD vacancies"], {"url": NEW_POSITIONS[1]["source_url"], "title": NEW_POSITIONS[1]["title"]})
    slu = source_by_name["SLU vacancies"]
    add_candidate(slu, SLU_BIOGAS)
    slu["reconciliation"] = "Client-rendered official index reconciled on 2026-09-26 using the configured official-domain PhD query and direct official pages. The Uppsala biogas-process and microbiology page was inventoried but its reported 31 August 2026 deadline has passed."

    positions_path = DATA / "positions.json"
    positions = [item for item in json.loads(positions_path.read_text(encoding="utf-8")) if item["deadline"] >= TODAY]
    ids = {item["id"] for item in positions}
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    with (DATA / "master_profile" / "master_cv.yml").open(encoding="utf-8") as handle:
        master = yaml_engine.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in ids:
            render_position(yaml_engine, master, position)
            positions.append(position)
            ids.add(position["id"])

    seen_path = DATA / "seen_positions.json"
    seen = json.loads(seen_path.read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in ids:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen:
                status, reason = "seen_not_selected", "Previously reviewed official candidate remains outside the active shortlist."
            else:
                status, reason = "not_selected", not_selected_reason(identifier, candidate.get("title", ""))
                seen[identifier] = {"source_url": candidate["url"], "first_seen": TODAY}
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    for position in NEW_POSITIONS:
        seen.setdefault(position["id"], {"source_url": position["source_url"], "first_seen": TODAY})
    positions.sort(key=lambda item: (item["kind"] != "phd", item["deadline"], -item["fit_score"], item["id"]))
    positions_path.write_text(json.dumps(positions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["refresh_date"] = TODAY
    manifest["summary"] = {
        "sources_total": len(manifest["sources"]),
        "sources_ok": sum(item["status"] == "ok" for item in manifest["sources"]),
        "sources_failed": sum(item["status"] == "failed" for item in manifest["sources"]),
        "sources_empty": sum(item["status"] == "empty" for item in manifest["sources"]),
        "sources_dynamic": sum(item["status"] == "dynamic" for item in manifest["sources"]),
        "candidate_urls": len({item["url"].rstrip("/") for source in manifest["sources"] for item in source.get("candidates", [])}),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "index.html").write_text(build_report(positions, TODAY), encoding="utf-8")
    print(json.dumps({"new": [position["id"] for position in NEW_POSITIONS], "active": len(positions), "summary": manifest["summary"], "triage": {item["name"]: len(item.get("triage", [])) for item in manifest["sources"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
