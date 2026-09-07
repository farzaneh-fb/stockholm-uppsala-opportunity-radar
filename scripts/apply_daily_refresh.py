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
TODAY = date(2026, 9, 8)

NEW_POSITIONS = [
    {
        "id": "KI_962127",
        "kind": "job",
        "title": "Research assistant",
        "short_title": "childhood_cancer_research_assistant",
        "organization": "Karolinska Institutet",
        "city": "Solna",
        "location_detail": "Nikolas Herold research group",
        "found_date": TODAY.isoformat(),
        "new_date": TODAY.isoformat(),
        "published": "2026-08-24",
        "deadline": "2026-09-13",
        "employment": "Full-time fixed-term employment",
        "fit_score": 82,
        "fit_label": "Strong match with method gaps",
        "description": "Support translational childhood-cancer research on cancer-cell responses to cytotoxic drugs, centred on primary cell culture and molecular analyses.",
        "match_reasons": [
            "Master's-level biotechnology training and documented cellular and molecular-biology research meet the core academic and laboratory profile",
            "Documented neuroblastoma cell culture, drug treatment, DNA extraction and long-range PCR are directly relevant to the group’s cancer-cell workflows",
            "Current KI/SciLifeLab research experience and publications support independent experimental work, collaboration and scientific presentation",
            "Python/R-based bioinformatics experience is relevant to the posting’s data-analysis component",
        ],
        "gaps": [
            "Primary human fibroblast, stem-cell and feeder-based culture are not documented in the master CV",
            "dNTP-pool measurement, mitochondrial-DNA/telomere assays, viability assays, CRISPR and plasmid cloning are not documented",
            "Fiji/ImageJ, ModFit and GraphPad Prism are not explicitly documented",
        ],
        "source_url": "https://ki.varbi.com/en/what:job/jobID:962127/type:job/where:4/apply:1",
        "apply_url": "https://ki.varbi.com/en/what:login/jobID:962127/type:job/apply:1/",
        "contact": "Nikolas Herold — nikolas.herold@ki.se",
        "headline": "Biomedical Researcher | Cancer Cell Biology, Molecular Methods & Genomics",
        "statement": "Biomedical researcher with Master's-level biotechnology training and hands-on experience in neuroblastoma cell culture, drug treatments, DNA extraction and long-range PCR. I combine careful molecular-biology experimentation with Python/R-based bioinformatics and reproducible data analysis through research at Karolinska Institutet, KTH and SciLifeLab. I am motivated to contribute rigorous cancer-cell research while developing the group’s specialised nucleotide-metabolism and primary-cell methods.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KTH_964164",
        "kind": "phd",
        "title": "Doctoral student in Biomedical microsystems",
        "short_title": "biomedical_microsystems",
        "organization": "KTH Royal Institute of Technology",
        "city": "Stockholm",
        "location_detail": "Micro and Nanosystems Lab, KTH / KI / SciLifeLab",
        "found_date": TODAY.isoformat(),
        "new_date": TODAY.isoformat(),
        "published": "2026-09-03",
        "deadline": "2026-09-30",
        "employment": "Full-time doctoral employment, up to 4 years",
        "fit_score": 74,
        "fit_label": "Relevant stretch match",
        "description": "Develop minimally invasive biomedical-MEMS sampling technologies for neurological biomarkers, including platform development and in-vitro/in-vivo model evaluation.",
        "match_reasons": [
            "Master's-level medical nanotechnology training and documented microfluidic-device development provide relevant microsystems context",
            "Tumor-on-a-Chip, Brain-on-a-Chip and endothelial-on-a-chip research align with in-vitro biomedical-platform development",
            "Experimental cell-culture, molecular-biology and translational research experience support interdisciplinary work with KI and SciLifeLab",
            "Documented publications and independent research experience support the required scientific communication and project work",
        ],
        "gaps": [
            "The advert specifically requests a mechanical-engineering degree or similar; the master CV documents medical nanotechnology and biotechnology instead",
            "Biomedical MEMS, microfabrication, biomechanics, fine mechanics and in-vivo model work are not explicitly documented",
            "The applicant should substantiate degree equivalence and experimental-platform contributions in the application letter",
        ],
        "source_url": "https://www.kth.se/lediga-jobb/964164?l=en",
        "apply_url": "https://kth.varbi.com/en/apply/positionquick/964164/?where=4",
        "contact": "Prof. Niclas Roxhed — see official KTH advert",
        "headline": "Biomedical Researcher | Medical Nanotechnology, Microfluidics & Organ-on-Chip",
        "statement": "Interdisciplinary biomedical researcher with Master's-level training in medical nanotechnology and biotechnology, bringing hands-on experience developing microfluidic devices and organ-on-chip platforms for endothelial, tumor and brain research. I combine careful experimental work in cell culture and molecular biology with scientific communication and reproducible data analysis. I am motivated to apply this platform-development foundation to biomedical microsystems while building formal expertise in MEMS, microfabrication and biomechanics.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Education", "Peer-Reviewed Publications", "Conference Presentations", "Bioinformatics & Computational Biology Projects", "Computational Biology & Bioinformatics Skills", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "SLU_2585",
        "kind": "job",
        "title": "Research technician – Molecular Biology and Genomics",
        "short_title": "molecular_biology_genomics_technician",
        "organization": "Swedish University of Agricultural Sciences",
        "city": "Uppsala",
        "location_detail": "Department of Plant Biology, Biocentrum, Ultuna",
        "found_date": TODAY.isoformat(),
        "new_date": TODAY.isoformat(),
        "published": "2026-09-03",
        "deadline": "2026-09-17",
        "employment": "Full-time fixed-term employment, 2 months with possible extension",
        "fit_score": 84,
        "fit_label": "Strong match with domain gaps",
        "description": "Support molecular-biology and genomics experiments processing cereal samples for DNA/RNA extraction, sequencing-library preparation, quality control and sample tracking.",
        "match_reasons": [
            "Master's-level biotechnology and documented molecular-biology research satisfy the stated academic background",
            "DNA extraction, long-range PCR, sequencing-data workflows and quality-control pipeline development are directly relevant to nucleic-acid and genomics work",
            "Documented reproducible workflow, HPC and scientific-data experience supports accurate sample documentation and sequencing-data handling",
            "Hands-on laboratory research and collaborative KI/KTH/SciLifeLab experience support careful independent work in a research team",
        ],
        "gaps": [
            "Plant-material handling and cereal-sample processing are not documented in the master CV",
            "Genotyping-by-Sequencing, RAD-seq and wet-lab NGS library preparation are not explicitly documented",
            "High-throughput sample processing and external sequencing-submission experience are not explicitly documented",
        ],
        "source_url": "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/forsokstekniker-inom-molekylar-biologi-och-genomik/",
        "apply_url": "https://web103.reachmee.com/ext/I017/1114/profile?site=7&validator=87e4b706891e51f731ed44be28da8352&lang=UK&job_id=15849",
        "contact": "See official SLU advert",
        "headline": "Molecular Biology & Genomics Researcher | Sequencing Workflows, PCR & QC",
        "statement": "Biomedical researcher with Master's-level biotechnology training and hands-on molecular-biology experience, including DNA extraction, long-range PCR and sequencing-data workflows. I have developed reproducible quality-control pipelines for sequencing data and bring careful laboratory practice, documentation and collaborative research experience from KI, KTH and SciLifeLab. I am motivated to apply this foundation to high-quality nucleic-acid processing and genomics support while developing plant-specific and GBS library-preparation methods.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Computational Biology & Bioinformatics Skills", "Bioinformatics & Computational Biology Projects", "Education", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
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
