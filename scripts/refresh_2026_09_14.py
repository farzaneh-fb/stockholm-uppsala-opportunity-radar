from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import MASTER, render_position  # noqa: E402
from ruamel.yaml import YAML  # noqa: E402
POSITIONS_FILE = ROOT / "data" / "positions.json"
SEEN_FILE = ROOT / "data" / "seen_positions.json"
TODAY = date(2026, 9, 14)

NEW_POSITION = {
    "id": "KI_964505",
    "kind": "phd",
    "title": "Doctoral (PhD) student position in cellular and molecular immunology",
    "short_title": "cellular_molecular_immunology",
    "organization": "Karolinska Institutet",
    "city": "Solna",
    "location_detail": "Department of Medicine, Solna, Center for Molecular Medicine",
    "found_date": TODAY.isoformat(),
    "new_date": TODAY.isoformat(),
    "published": "2026-09-01",
    "deadline": "2026-09-22",
    "employment": "Full-time doctoral studentship, up to 4 years",
    "fit_score": 90,
    "fit_label": "Excellent match with domain gaps",
    "description": "Investigate lymphocyte development and function through in-vivo and in-vitro experiments in cellular and molecular immunology.",
    "match_reasons": [
        "Master's-level biotechnology and cellular and molecular biology training provide a directly relevant academic foundation",
        "Documented cell culture, molecular-biology workflows and flow-cytometry experience align with the project's experimental approaches",
        "Single-cell and spatial transcriptomics, Python/R analysis and reproducible bioinformatics workflows align with listed beneficial skills",
        "KI, KTH and SciLifeLab research experience plus publications support independent experimental work, collaboration and scientific communication",
    ],
    "gaps": [
        "Lymphocyte biology and immunology specialization are not explicitly documented in the master CV",
        "In-vivo experimental experience is not explicitly documented",
        "The application should certify doctoral eligibility and describe only concrete immunology-relevant experience",
    ],
    "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:964505/type:job/where:4/apply:1",
    "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:964505/type:job/where:4/apply:1/",
    "contact": "Taras Kreslavskiy — taras.kreslavskiy@ki.se",
    "headline": "Biomedical Researcher | Cell Biology, Molecular Methods & Bioinformatics",
    "statement": "Biomedical researcher with Master's-level training in biotechnology and hands-on experience in cell culture, molecular-biology workflows and flow cytometry. I combine careful experimental work with single-cell and spatial transcriptomics, Python/R-based data analysis and reproducible bioinformatics workflows developed through research at Karolinska Institutet, KTH and SciLifeLab. I am motivated to contribute to rigorous lymphocyte-biology research while developing specialised immunology and in-vivo methods.",
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


def main() -> None:
    positions = json.loads(POSITIONS_FILE.read_text(encoding="utf-8"))
    positions = [item for item in positions if date.fromisoformat(item["deadline"]) >= TODAY]
    if NEW_POSITION["id"] not in {item["id"] for item in positions}:
        yaml_engine = YAML()
        yaml_engine.preserve_quotes = True
        with MASTER.open(encoding="utf-8") as handle:
            master = yaml_engine.load(handle)
        render_position(yaml_engine, master, NEW_POSITION)
        positions.append(NEW_POSITION)
    positions.sort(key=lambda item: (item["kind"] != "phd", item["deadline"], -item["fit_score"]))
    POSITIONS_FILE.write_text(json.dumps(positions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    seen = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    seen.setdefault(NEW_POSITION["id"], {"source_url": NEW_POSITION["source_url"], "first_seen": TODAY.isoformat()})
    SEEN_FILE.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [NEW_POSITION["id"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
