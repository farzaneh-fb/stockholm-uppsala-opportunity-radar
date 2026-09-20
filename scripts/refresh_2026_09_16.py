from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import MASTER, build_report, render_position  # noqa: E402

TODAY = date(2026, 9, 16)
POSITIONS_PATH = ROOT / "data" / "positions.json"
SEEN_PATH = ROOT / "data" / "seen_positions.json"
MANIFEST_PATH = ROOT / "data" / "discovery_manifest.json"

NEW_POSITION = {
    "id": "KI_965327",
    "kind": "phd",
    "title": "Doctoral (PhD) student position in leukotrienes and extracellular vesicles in cancer",
    "short_title": "leukotrienes_extracellular_vesicles_cancer",
    "organization": "Karolinska Institutet",
    "city": "Solna",
    "location_detail": "Department of Medicine, Division of Immunology and Respiratory Medicine",
    "found_date": TODAY.isoformat(),
    "new_date": TODAY.isoformat(),
    "published": "2026-09-02",
    "deadline": "2026-09-23",
    "employment": "Full-time doctoral studentship, up to 4 years",
    "fit_score": 88,
    "fit_label": "Strong match with method gaps",
    "description": "Study extracellular vesicles in cancer patients and their immunological roles, using clinical material, cell lines, primary cells, biochemical and cellular/molecular immunology methods in vitro and in vivo.",
    "match_reasons": [
        "Master's-level medical nanotechnology and cellular/molecular biotechnology training provide a relevant interdisciplinary biomedical foundation",
        "Documented cancer-cell culture, 2D/3D models, molecular-biology workflows and flow cytometry align with desired experimental skills",
        "Current KI/SciLifeLab research plus publications demonstrate research independence, collaboration and scientific communication",
        "Current bioinformatics study and sequencing-data workflows support quantitative analysis and cross-disciplinary work",
    ],
    "gaps": [
        "Immunology and extracellular-vesicle analysis are not explicitly documented in the master CV",
        "Animal-model experience is not explicitly documented",
        "The advert prefers a Master's degree in immunology or medical degree; degree relevance and doctoral eligibility must be documented accurately",
    ],
    "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:965327/type:job/where:4/apply:1",
    "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:965327/type:job/where:4/apply:1/",
    "contact": "Susanne Gabrielsson — susanne.gabrielsson@ki.se",
    "headline": "Biomedical Researcher | Cancer Biology, Cell Culture & Bioinformatics",
    "statement": "Biomedical researcher with Master's-level training in medical nanotechnology and cellular and molecular biotechnology, combining cancer-cell culture, 2D/3D models and molecular-biology workflows with Python/R-based bioinformatics. My work at Karolinska Institutet, KTH and SciLifeLab includes neuroblastoma cell culture, long-read sequencing analysis, organ-on-chip research and reproducible computational workflows. I am motivated to contribute careful experimental and analytical work to cancer and extracellular-vesicle research while developing specialised immunology, EV-analysis and in-vivo methods.",
    "section_order": [
        "Personal Statement",
        "Research Experience",
        "Wet Lab & Experimental Expertise",
        "Education",
        "Computational Biology & Bioinformatics Skills",
        "Bioinformatics & Computational Biology Projects",
        "Peer-Reviewed Publications",
        "Conference Presentations",
        "Professional & Personal Skills",
        "Teaching & Mentorship",
        "Awards & Honors",
        "References",
    ],
}

SLU_CANDIDATES = [
    {"url": "https://slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-de-novo-proteindesign", "title": "PhD students Protein Design"},
    {"url": "https://slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-mikrobiella-strategier-for-hallbar-pfas-sanering", "title": "PhD student in microbial strategies for sustainable PFAS remediation"},
    {"url": "https://slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand6", "title": "PhD student in AI-driven digital phenotyping and genomics"},
    {"url": "https://slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/phd-student-ddls-integrative-pangenomics-of-polyploids", "title": "PhD Student: DDLS integrative pangenomics of polyploids"},
]


def stable_id(url: str) -> str:
    match = re.search(r"jobID:(\d+)", url)
    if match:
        return ("KI_" if "ki.varbi" in url or "kidoktorand" in url else "SU_") + match.group(1)
    match = re.search(r"lediga-jobb/(\d+)", url)
    if match:
        return "KTH_" + match.group(1)
    match = re.search(r"query=(\d+)", url)
    if match:
        return "UU_" + match.group(1)
    return "URL_" + re.sub(r"[^a-z0-9]+", "_", url.lower()).strip("_")[:60]


def reconcile_manifest(active_ids: set[str], seen_ids: set[str]) -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        triage = []
        for candidate in source.get("candidates", []):
            identifier = stable_id(candidate["url"])
            if identifier in active_ids:
                status, reason = "active_existing", "Live official vacancy retained in the active report."
            elif identifier in seen_ids:
                status, reason = "seen_not_selected", "Previously reviewed official candidate is not selected for the active report."
            else:
                status, reason = "not_selected", "Official candidate reviewed; it is outside target scope, expired/unverified, duplicate discovery signal, or did not clear the realistic-fit gate."
            triage.append({"url": candidate["url"], "title": candidate.get("title", ""), "stable_id": identifier, "status": status, "reason": reason})
        source["triage"] = triage

    slu = next(source for source in manifest["sources"] if source["name"] == "SLU vacancies")
    slu["candidates"] = SLU_CANDIDATES
    slu["candidate_urls"] = [candidate["url"] for candidate in SLU_CANDIDATES]
    slu["reconciliation"] = "Official-domain search performed for the client-rendered index. Direct vacancy-page retrieval resolved to a generic SLU page, so candidates remain unverified and are not accepted."
    slu["triage"] = [
        {
            "url": candidate["url"],
            "title": candidate["title"],
            "stable_id": stable_id(candidate["url"]),
            "status": "unverified_dynamic",
            "reason": "Official-domain search discovery candidate; direct official vacancy page did not expose a live advert for verification.",
        }
        for candidate in SLU_CANDIDATES
    ]
    manifest["summary"]["candidate_urls"] = len({candidate["url"] for source in manifest["sources"] for candidate in source.get("candidates", [])})
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    positions = json.loads(POSITIONS_PATH.read_text(encoding="utf-8"))
    positions = [position for position in positions if date.fromisoformat(position["deadline"]) >= TODAY]
    if NEW_POSITION["id"] not in {position["id"] for position in positions}:
        yaml_engine = YAML()
        yaml_engine.preserve_quotes = True
        with MASTER.open(encoding="utf-8") as handle:
            master = yaml_engine.load(handle)
        render_position(yaml_engine, master, NEW_POSITION)
        positions.append(NEW_POSITION)
    positions.sort(key=lambda position: (position["kind"] != "phd", position["deadline"], -position["fit_score"]))
    POSITIONS_PATH.write_text(json.dumps(positions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    seen = json.loads(SEEN_PATH.read_text(encoding="utf-8"))
    seen.setdefault(NEW_POSITION["id"], {"source_url": NEW_POSITION["source_url"], "first_seen": TODAY.isoformat()})
    SEEN_PATH.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest = reconcile_manifest({position["id"] for position in positions}, set(seen))
    (ROOT / "index.html").write_text(build_report(positions, TODAY.isoformat()), encoding="utf-8")
    print(json.dumps({
        "new": [NEW_POSITION["id"]],
        "active": len(positions),
        "phd": sum(position["kind"] == "phd" for position in positions),
        "job": sum(position["kind"] == "job" for position in positions),
        "candidate_urls": manifest["summary"]["candidate_urls"],
        "triage_by_source": {source["name"]: len(source["triage"]) for source in manifest["sources"]},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
