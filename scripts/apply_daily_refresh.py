from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_test_report import render_position  # noqa: E402
from ruamel.yaml import YAML  # noqa: E402
POSITIONS_FILE = ROOT / "data" / "positions.json"
SEEN_FILE = ROOT / "data" / "seen_positions.json"
MASTER = ROOT / "data" / "master_profile" / "master_cv.yml"
TODAY = date(2026, 9, 10)

NEW_POSITIONS = [
    {
        "id": "UU_960660", "kind": "phd", "title": "PhD student in Computational Materials Chemistry", "short_title": "computational_materials_chemistry", "organization": "Uppsala University", "city": "Uppsala", "location_detail": "Department of Chemistry – Ångström Laboratory", "found_date": TODAY.isoformat(), "new_date": TODAY.isoformat(), "published": "2026-09-03", "deadline": "2026-09-15", "employment": "Full-time doctoral employment", "fit_score": 72, "fit_label": "Relevant stretch match", "description": "Use multiscale modelling, data mining and machine learning to study ion transport in solid-state polymer electrolytes for Li-ion batteries.",
        "match_reasons": ["Master's-level medical nanotechnology training provides a relevant materials-science foundation", "Documented Python/R, HPC and reproducible scientific-data workflows align with the computational component", "Research experience and publication record support independent doctoral research and scientific communication"],
        "gaps": ["Materials modelling, solid-state electrolytes and battery research are not documented in the master CV", "The advert prefers physics or chemistry specialisation and computational materials-modelling experience, which should be addressed candidly"],
        "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=960660", "apply_url": "https://uu.varbi.com/en/what:login/type:job/jobID:960660", "contact": "Amber Mace — amber.mace@kemi.uu.se", "headline": "Interdisciplinary Researcher | Nanotechnology, Scientific Computing & Reproducible Analysis", "statement": "Interdisciplinary biomedical researcher with Master's-level training in medical nanotechnology and current bioinformatics study, combining experimental materials and molecular-biology research with Python/R-based scientific-data analysis and reproducible computational workflows. My work at KI, KTH and SciLifeLab has developed my independence, scientific communication and cross-disciplinary research practice. I am motivated to apply this foundation to computational materials chemistry while developing specialised expertise in multiscale modelling, battery materials and ion transport.",
        "section_order": ["Personal Statement", "Education", "Research Experience", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Wet Lab & Experimental Expertise", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
]


def main() -> None:
    positions = json.loads(POSITIONS_FILE.read_text(encoding="utf-8"))
    positions = [position for position in positions if date.fromisoformat(position["deadline"]) >= TODAY]
    existing_ids = {position["id"] for position in positions}
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    with MASTER.open(encoding="utf-8") as handle:
        master = yaml_engine.load(handle)
    for position in NEW_POSITIONS:
        if position["id"] not in existing_ids:
            render_position(yaml_engine, master, position)
            positions.append(position)
    positions.sort(key=lambda position: (position["kind"] != "phd", position["deadline"], -position["fit_score"]))
    POSITIONS_FILE.write_text(json.dumps(positions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    seen = json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    for position in NEW_POSITIONS:
        seen.setdefault(position["id"], {"source_url": position["source_url"], "first_seen": TODAY.isoformat()})
    SEEN_FILE.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": [position["id"] for position in NEW_POSITIONS]}))


if __name__ == "__main__":
    main()
