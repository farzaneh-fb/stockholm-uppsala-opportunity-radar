from __future__ import annotations

import html
import json
import shutil
import subprocess
from copy import deepcopy
from datetime import date
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "data" / "master_profile" / "master_cv.yml"
TAILORED = ROOT / "data" / "tailored"
RENDER_WORK = ROOT / "data" / ".render_work"
POSITIONS_FILE = ROOT / "data" / "positions.json"
REPORT_FILE = ROOT / "index.html"
FOUND_DATE = "2026-08-23"


def rendercv_executable() -> Path:
    executable = ROOT / ".rendercv-venv" / "Scripts" / "rendercv.exe"
    if not executable.exists():
        raise FileNotFoundError(
            "RenderCV 2.8 environment is missing. Run: uv venv --python 3.12 .rendercv-venv "
            "&& uv pip install --python .rendercv-venv/Scripts/python.exe 'rendercv[full]==2.8'"
        )
    return executable


POSITIONS = [
    {
        "id": "KI_960758",
        "kind": "phd",
        "title": "Doctoral (PhD) student position in developmental neuroscience",
        "short_title": "developmental_neuroscience",
        "organization": "Karolinska Institutet",
        "city": "Stockholm",
        "location_detail": "Center for Molecular Medicine, Solna",
        "found_date": FOUND_DATE,
        "published": "2026-08-19",
        "deadline": "2026-09-09",
        "employment": "Full-time doctoral studentship, up to 4 years",
        "fit_score": 94,
        "fit_label": "Excellent match",
        "description": "Eric Herlenius' group studies how brainstem neural networks, inflammation and developmental transitions shape cardiorespiratory control in newborns and children. The project combines rodent models with single-cell RNA sequencing and spatial transcriptomics, with a central focus on computational integration of complex multimodal datasets and gene-regulatory programs.",
        "match_reasons": [
            "Direct overlap with single-cell RNA-seq and spatial transcriptomics",
            "Strong R/Python, Linux, sequencing and bioinformatics workflow fit",
            "Relevant wet-lab background in cell culture, molecular biology and imaging",
            "Current KI/SciLifeLab research experience and scientific publication record",
        ],
        "gaps": ["Deep-learning experience is foundational rather than extensive", "No stated prior neuroscience specialization"],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:960758/type:job/where:51/apply:1",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:960758/type:job/where:51/apply:1/",
        "contact": "Eric Herlenius — eric.herlenius@ki.se",
        "headline": "Bioinformatics & Molecular Biology Researcher | Single-Cell and Spatial Transcriptomics",
        "statement": "Interdisciplinary researcher combining bioinformatics, genomics and molecular biology, with hands-on experience in sequencing workflows, cell culture and translational research. I use R, Python, Linux and reproducible pipelines to analyze high-dimensional biological data, including single-cell RNA-seq and spatial transcriptomics, and I am motivated to investigate how gene-regulatory programs and tissue context shape developmental disease mechanisms.",
        "section_order": ["Personal Statement", "Education", "Bioinformatics & Computational Biology Projects", "Research Experience", "Computational Biology & Bioinformatics Skills", "Wet Lab & Experimental Expertise", "Peer-Reviewed Publications", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KI_957925",
        "kind": "phd",
        "title": "Doctoral student in computational pathology and medical artificial intelligence",
        "short_title": "computational_pathology_ai",
        "organization": "Karolinska Institutet",
        "city": "Stockholm",
        "location_detail": "Department of Medical Epidemiology and Biostatistics, Solna",
        "found_date": FOUND_DATE,
        "published": "2026-08-06",
        "deadline": "2026-08-31",
        "employment": "Full-time doctoral studentship, up to 4 years",
        "fit_score": 78,
        "fit_label": "Good stretch match",
        "description": "Kimmo Kartasalo's DDLS/SciLifeLab-affiliated group develops large-scale image-analysis and deep-learning methods for precision cancer medicine. The doctoral project evaluates and develops foundation models and agentic AI for prostate-cancer diagnosis, grading and prognosis across patient populations and pathology platforms, including multimodal integration of tissue images, molecular data and clinical variables.",
        "match_reasons": [
            "Eligible biotechnology/bioinformatics academic background",
            "Strong Python, scientific programming, version control and reproducibility",
            "Cancer biology, microscopy and multimodal omics experience are relevant",
            "Demonstrated scientific writing through publications and theses",
        ],
        "gaps": ["No documented digital pathology or whole-slide-image work", "PyTorch/deep-learning experience is not yet demonstrated at production or research depth"],
        "source_url": "https://kidoktorand.varbi.com/en/what:job/jobID:957925",
        "apply_url": "https://kidoktorand.varbi.com/en/what:login/jobID:957925/type:job/apply:1/",
        "contact": "Nita Mulliqi — nita.mulliqi@ki.se",
        "headline": "Computational Biology Researcher | Cancer Biology, Genomics and Reproducible Analysis",
        "statement": "Interdisciplinary researcher with a foundation in bioinformatics, cancer biology and molecular biotechnology, combining Python/R analysis with experimental work and scientific communication. My experience includes tumor models, microscopy, sequencing data, reproducible workflows and multimodal transcriptomics; I am motivated to deepen my expertise in machine learning and medical image analysis for clinically useful precision-oncology tools.",
        "section_order": ["Personal Statement", "Education", "Bioinformatics & Computational Biology Projects", "Computational Biology & Bioinformatics Skills", "Research Experience", "Peer-Reviewed Publications", "Wet Lab & Experimental Expertise", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KI_960143",
        "kind": "job",
        "title": "Project Coordinator for Large Research Study on Human intestinal diseases",
        "short_title": "intestinal_disease_project_coordinator",
        "organization": "Karolinska Institutet",
        "city": "Stockholm",
        "location_detail": "Department of Medicine, Solna / SciLifeLab",
        "found_date": FOUND_DATE,
        "published": "2026-08-17",
        "deadline": "2026-09-13",
        "employment": "Full-time special fixed-term employment",
        "fit_score": 89,
        "fit_label": "Strong match",
        "description": "Eduardo Villablanca's mucosal-immunology team is coordinating a three-lab translational study of inflammatory bowel disease and mucosal healing. The role combines project coordination, ethical and regulatory documentation, human-sample biobanking, single-cell suspension and organoid work, meeting facilitation, and communication of results across KI and SciLifeLab laboratories.",
        "match_reasons": [
            "Direct hands-on organoid, cell-culture and molecular-biology experience",
            "Strong single-cell/spatial biology awareness and SciLifeLab familiarity",
            "Track record of independent multidisciplinary research and presentations",
            "Well matched to coordination across wet-lab and computational teams",
        ],
        "gaps": ["Swedish biobank administration is not documented", "Formal multi-lab project-management responsibility is not explicit in the master CV"],
        "source_url": "https://ki.varbi.com/en/what:job/jobID:960143",
        "apply_url": "https://ki.varbi.com/en/what:login/jobID:960143/type:job/apply:1/",
        "contact": "Eduardo Villablanca — eduardo.villablanca@ki.se",
        "headline": "Biomedical Researcher | Organoid Models, Single-Cell Biology and Project Coordination",
        "statement": "Biomedical researcher experienced in organoid and 2D/3D cell culture, molecular-biology workflows, translational cancer models and cross-disciplinary work at KTH, Karolinska Institutet and SciLifeLab. I combine meticulous experimental practice with bioinformatics literacy, scientific reporting and an independent, structured working style suited to coordinating samples, documentation, timelines and communication across collaborative research teams.",
        "section_order": ["Personal Statement", "Research Experience", "Wet Lab & Experimental Expertise", "Professional & Personal Skills", "Education", "Bioinformatics & Computational Biology Projects", "Peer-Reviewed Publications", "Conference Presentations", "Computational Biology & Bioinformatics Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
    {
        "id": "KI_957295",
        "kind": "job",
        "title": "Biomedical systems developer to CLINTEC",
        "short_title": "biomedical_systems_developer",
        "organization": "Karolinska Institutet",
        "city": "Solna",
        "location_detail": "CLINTEC, Division of Ear, Nose and Throat Diseases",
        "found_date": FOUND_DATE,
        "published": "2026-08-05",
        "deadline": "2026-08-26",
        "employment": "Full-time permanent position; six-month trial period",
        "fit_score": 85,
        "fit_label": "Strong but competitive",
        "description": "Mikael Benson's medical-digital-twins group develops computational methods to identify cancer disease mechanisms, biomarkers and drug targets. The role applies machine learning and statistical methods to single-cell and spatial data, evaluates candidate targets, supports publications and presentations, and collaborates across Swedish and international EU projects.",
        "match_reasons": [
            "Computational-science Master's-level profile with bioinformatics specialization",
            "Relevant single-cell and spatial transcriptomics project experience",
            "Cancer, biomarker and translational-research background",
            "Strong scientific writing and interdisciplinary collaboration record",
        ],
        "gaps": ["Advert asks for experience with single-cell analyses including spatial; the CV shows project work but depth should be evidenced in application answers", "Deep-learning experience is currently foundational"],
        "source_url": "https://ki.varbi.com/en/what:job/jobID:957295/type:job/where:4/apply:1",
        "apply_url": "https://ki.varbi.com/en/what:login/jobID:957295/type:job/where:4/apply:1/",
        "contact": "Mikael Benson — mikael.benson@ki.se",
        "headline": "Biomedical Systems & Bioinformatics Researcher | Single-Cell, Spatial and Cancer Biology",
        "statement": "Interdisciplinary biomedical researcher combining bioinformatics, genomics and cancer biology with hands-on wet-lab experience. I develop reproducible R/Python workflows for sequencing and transcriptomic data, including single-cell and spatial analyses, and connect computational results to disease mechanisms, biomarkers and translational questions through experience at Karolinska Institutet, KTH and SciLifeLab.",
        "section_order": ["Personal Statement", "Bioinformatics & Computational Biology Projects", "Computational Biology & Bioinformatics Skills", "Research Experience", "Education", "Peer-Reviewed Publications", "Wet Lab & Experimental Expertise", "Conference Presentations", "Professional & Personal Skills", "Teaching & Mentorship", "Awards & Honors", "References"],
    },
]


def compatible_tailored_cv(master: dict, position: dict) -> dict:
    cv_doc = deepcopy(master)
    cv_doc["cv"]["headline"] = position["headline"]
    sections = cv_doc["cv"]["sections"]
    sections["Personal Statement"][0] = position["statement"]
    original = dict(sections)
    sections.clear()
    for section_name in position["section_order"]:
        if section_name in original:
            sections[section_name] = original[section_name]
    for section_name, entries in original.items():
        if section_name not in sections:
            sections[section_name] = entries
    return cv_doc


def render_position(yaml_engine: YAML, master: dict, position: dict) -> None:
    stem = f"{position['id']}_{position['short_title']}"
    yml_path = TAILORED / f"{stem}.yml"
    pdf_path = TAILORED / f"{stem}.pdf"
    tailored = compatible_tailored_cv(master, position)
    with yml_path.open("w", encoding="utf-8") as handle:
        yaml_engine.dump(tailored, handle)

    out_dir = RENDER_WORK / position["id"]
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    result = subprocess.run(
        [str(rendercv_executable()), "render", str(yml_path), "--output-folder", str(out_dir)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(f"RenderCV failed for {position['id']}:\n{result.stdout}\n{result.stderr}")
    rendered = out_dir / "Farzaneh_Fayazbakhsh_CV.pdf"
    if not rendered.exists():
        candidates = list(out_dir.glob("*.pdf"))
        if len(candidates) != 1:
            raise RuntimeError(f"Could not identify rendered PDF in {out_dir}")
        rendered = candidates[0]
    shutil.copy2(rendered, pdf_path)
    position["cv_yml"] = f"data/tailored/{yml_path.name}"
    position["cv_pdf"] = f"data/tailored/{pdf_path.name}"
    position["download_name"] = pdf_path.name


def build_report(positions: list[dict], report_date: str = FOUND_DATE) -> str:
    data_json = json.dumps(positions, ensure_ascii=False).replace("</", "<\\/")
    generated_date = date.fromisoformat(report_date)
    generated = f"{generated_date.day} {generated_date:%B %Y}"
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark light">
<title>Farzaneh's Opportunity Radar</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{ --bg:#08090a; --panel:#0f1011; --surface:#17181a; --surface2:#202124; --text:#f7f8f8; --secondary:#d0d6e0; --muted:#8a8f98; --faint:#62666d; --border:rgba(255,255,255,.09); --subtle:rgba(255,255,255,.04); --accent:#7170ff; --accent2:#5e6ad2; --green:#10b981; --amber:#f59e0b; --red:#ef4444; --shadow:rgba(0,0,0,.35); }}
html[data-theme="light"] {{ --bg:#f7f8fa; --panel:#fff; --surface:#fff; --surface2:#f0f1f3; --text:#15161a; --secondary:#343741; --muted:#676b75; --faint:#858a94; --border:rgba(17,24,39,.12); --subtle:rgba(17,24,39,.035); --accent:#5552d9; --accent2:#5e6ad2; --green:#07875f; --amber:#b76b00; --red:#c93636; --shadow:rgba(25,28,35,.10); }}
* {{ box-sizing:border-box; }} html {{ scroll-behavior:smooth; }} body {{ margin:0; min-width:320px; background:var(--bg); color:var(--text); font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif; font-feature-settings:"cv01","ss03"; -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; }} button,input {{ font:inherit; }} button {{ color:inherit; }}
.shell {{ width:min(1180px,100%); margin:auto; padding:0 24px 80px; }}
.topbar {{ position:sticky; top:0; z-index:20; border-bottom:1px solid var(--border); background:color-mix(in srgb,var(--bg) 88%,transparent); backdrop-filter:blur(18px); }}
.topbar-inner {{ width:min(1180px,100%); margin:auto; min-height:64px; padding:0 24px; display:flex; align-items:center; gap:16px; }}
.brand {{ display:flex; align-items:center; gap:10px; font-weight:560; letter-spacing:-.2px; }} .brand-mark {{ width:22px; height:22px; border-radius:6px; background:linear-gradient(135deg,#8a89ff,#4b49c8); box-shadow:0 0 28px rgba(113,112,255,.35); }}
.top-actions {{ margin-left:auto; display:flex; gap:8px; }} .icon-btn,.btn {{ border:1px solid var(--border); background:var(--subtle); border-radius:7px; cursor:pointer; min-height:40px; padding:0 13px; display:inline-flex; align-items:center; justify-content:center; gap:8px; text-decoration:none; transition:.16s ease; }} .icon-btn:hover,.btn:hover {{ border-color:color-mix(in srgb,var(--accent) 45%,var(--border)); background:color-mix(in srgb,var(--accent) 10%,var(--subtle)); transform:translateY(-1px); }} .icon-btn {{ width:40px; padding:0; font-size:17px; }}
.hero {{ padding:72px 0 38px; }} .eyebrow {{ color:var(--accent); font:500 12px/1.4 "JetBrains Mono",monospace; letter-spacing:.07em; text-transform:uppercase; }} h1 {{ max-width:780px; margin:14px 0 16px; font-size:clamp(36px,7vw,64px); font-weight:510; line-height:1.02; letter-spacing:-1.4px; }} .intro {{ max-width:720px; color:var(--muted); font-size:17px; line-height:1.65; }}
.stats {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:34px 0 30px; }} .stat {{ border:1px solid var(--border); border-radius:10px; padding:16px; background:var(--subtle); }} .stat strong {{ display:block; font-size:24px; font-weight:510; letter-spacing:-.5px; }} .stat span {{ color:var(--muted); font-size:12px; }}
.controls {{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin:12px 0 26px; }} .tabs {{ display:flex; width:max-content; padding:4px; border:1px solid var(--border); border-radius:9px; background:var(--panel); overflow:auto; max-width:100%; }} .tab {{ border:0; background:transparent; color:var(--muted); padding:9px 16px; border-radius:6px; cursor:pointer; white-space:nowrap; }} .tab.active {{ background:var(--surface2); color:var(--text); box-shadow:0 1px 2px var(--shadow); }} .filters {{ margin-left:auto; display:flex; gap:8px; align-items:center; }} .select {{ min-height:40px; padding:0 34px 0 12px; border:1px solid var(--border); border-radius:7px; background:var(--panel); color:var(--secondary); }}
.day-header {{ display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:12px; margin:34px 0 12px; }} .day-header h2 {{ font-size:14px; font-weight:510; margin:0; white-space:nowrap; }} .day-line {{ height:1px; background:var(--border); }} .day-count {{ color:var(--faint); font:12px "JetBrains Mono",monospace; }}
.cards {{ display:grid; gap:12px; }} .card {{ position:relative; border:1px solid var(--border); border-radius:12px; background:var(--surface); overflow:hidden; box-shadow:0 1px 2px var(--shadow); transition:.18s ease; }} .card:hover {{ border-color:color-mix(in srgb,var(--accent) 35%,var(--border)); transform:translateY(-1px); }} .card.applied {{ border-color:color-mix(in srgb,var(--green) 38%,var(--border)); box-shadow:inset 3px 0 0 color-mix(in srgb,var(--green) 72%,transparent),0 1px 2px var(--shadow); }} .card-main {{ display:grid; grid-template-columns:72px minmax(0,1fr) auto; gap:18px; padding:22px; }}
.score {{ width:64px; height:64px; border-radius:50%; display:grid; place-content:center; border:1px solid color-mix(in srgb,var(--score-color) 45%,var(--border)); background:color-mix(in srgb,var(--score-color) 11%,transparent); }} .score strong {{ display:block; text-align:center; font-size:20px; font-weight:560; }} .score small {{ color:var(--muted); font:9px "JetBrains Mono",monospace; text-transform:uppercase; }}
.card-title {{ display:flex; align-items:flex-start; gap:10px; flex-wrap:wrap; }} .card h3 {{ margin:0; font-size:19px; line-height:1.35; font-weight:560; letter-spacing:-.25px; }} .kind {{ padding:4px 7px; border:1px solid var(--border); border-radius:999px; color:var(--muted); font:10px "JetBrains Mono",monospace; text-transform:uppercase; }} .meta {{ color:var(--muted); font-size:13px; margin:7px 0 14px; display:flex; gap:8px 16px; flex-wrap:wrap; }} .description {{ margin:0; color:var(--secondary); font-size:14px; line-height:1.65; }} .deadline {{ min-width:145px; text-align:right; }} .deadline .date {{ display:block; font:500 13px "JetBrains Mono",monospace; margin-top:5px; }} .deadline .label {{ color:var(--faint); font-size:11px; }}
.card-extra {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; padding:18px 22px; border-top:1px solid var(--border); background:var(--subtle); }} .card-extra h4 {{ margin:0 0 9px; font-size:12px; font-weight:560; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }} ul {{ margin:0; padding-left:18px; }} li {{ margin:5px 0; color:var(--secondary); font-size:13px; line-height:1.45; }} .gaps li::marker {{ color:var(--amber); }} .matches li::marker {{ color:var(--green); }}
.card-actions {{ display:flex; align-items:center; flex-wrap:wrap; gap:8px; padding:14px 22px; border-top:1px solid var(--border); }} .btn.primary {{ color:white; background:var(--accent2); border-color:transparent; }} .apply-check {{ margin-left:auto; display:flex; gap:9px; align-items:center; color:var(--secondary); font-size:13px; cursor:pointer; min-height:40px; }} .apply-check input {{ width:18px; height:18px; accent-color:var(--accent); }}
.empty {{ border:1px dashed var(--border); border-radius:12px; padding:42px; text-align:center; color:var(--muted); }} .notice {{ margin-top:28px; padding:16px 18px; border:1px solid var(--border); border-radius:9px; color:var(--muted); font-size:13px; line-height:1.55; background:var(--subtle); }} .notice strong {{ color:var(--secondary); }}
.footer {{ margin-top:56px; padding-top:18px; border-top:1px solid var(--border); color:var(--faint); font-size:12px; display:flex; justify-content:space-between; gap:15px; flex-wrap:wrap; }}
@media (max-width:820px) {{ .stats {{ grid-template-columns:repeat(2,1fr); }} .card-main {{ grid-template-columns:64px minmax(0,1fr); }} .deadline {{ grid-column:2; text-align:left; display:flex; gap:8px; align-items:baseline; }} .card-extra {{ grid-template-columns:1fr; }} }}
@media (max-width:600px) {{ .shell,.topbar-inner {{ padding-left:16px; padding-right:16px; }} .hero {{ padding-top:48px; }} .brand span {{ display:none; }} .controls {{ align-items:stretch; }} .tabs {{ width:100%; }} .tab {{ flex:1; }} .filters {{ margin-left:0; width:100%; overflow-x:auto; padding-bottom:2px; }} .card-main {{ grid-template-columns:1fr; padding:18px; }} .score {{ width:auto; height:auto; border-radius:7px; display:flex; place-content:initial; align-items:center; gap:5px; padding:7px 10px; justify-self:start; }} .score strong {{ font-size:14px; }} .score small {{ font-size:9px; }} .deadline {{ grid-column:1; }} .card-extra,.card-actions {{ padding-left:18px; padding-right:18px; }} .apply-check {{ width:100%; margin-left:0; }} .btn {{ flex:1; }} }}
@media (prefers-reduced-motion:reduce) {{ * {{ scroll-behavior:auto!important; transition:none!important; }} }}
</style>
</head>
<body>
<header class="topbar"><div class="topbar-inner"><div class="brand"><i class="brand-mark"></i><span>Opportunity Radar</span></div><div class="top-actions"><button class="icon-btn" id="exportBtn" aria-label="Export application status" title="Export application status">⇩</button><label class="icon-btn" aria-label="Import application status" title="Import application status">⇧<input id="importInput" type="file" accept="application/json" hidden></label><button class="icon-btn" id="themeBtn" aria-label="Toggle color theme" title="Toggle theme">◐</button></div></div></header>
<main class="shell">
<section class="hero"><div class="eyebrow">Stockholm + Uppsala · Daily shortlist</div><h1>High-signal opportunities, tailored to your profile.</h1><p class="intro">Verified PhD and job openings ranked by realistic fit. Each listing includes a position-specific RenderCV résumé, transparent match reasoning, gaps to address, and source links.</p><div class="stats"><div class="stat"><strong id="newCount">0</strong><span>new today</span></div><div class="stat"><strong id="phdCount">0</strong><span>PhD positions</span></div><div class="stat"><strong id="jobCount">0</strong><span>job positions</span></div><div class="stat"><strong id="urgentCount">0</strong><span>closing within 7 days</span></div></div></section>
<section class="controls"><div class="tabs" role="tablist"><button class="tab active" data-kind="phd" role="tab">PhD positions</button><button class="tab" data-kind="job" role="tab">Job positions</button></div><div class="filters"><select class="select" id="statusFilter" aria-label="Filter by application status"><option value="unapplied">Not applied</option><option value="all">All positions</option><option value="applied">Applied</option></select><select class="select" id="cityFilter" aria-label="Filter by city"><option value="all">All cities</option></select></div></section>
<div id="results" aria-live="polite"></div>
<div class="notice"><strong>How tracking works:</strong> application checkboxes are saved privately in this browser using local storage. Use ⇩ / ⇧ in the header to export or import the status file when switching devices. Expired listings will be removed from the active report by the daily process, while previously seen source IDs remain in the deduplication ledger.</div>
<footer class="footer"><span>Generated {generated} · Europe/Stockholm</span><span>Fit scores are evidence-based estimates, not guarantees.</span></footer>
</main>
<script>
const positions={data_json};
const foundToday="{report_date}";
const stateKey="farzaneh-opportunity-applications-v1";
let activeKind="phd";
const today=new Date("{report_date}T12:00:00+02:00");
const esc=s=>String(s).replace(/[&<>'"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#039;','"':'&quot;'}}[c]));
const loadState=()=>{{try{{return JSON.parse(localStorage.getItem(stateKey)||"{{}}")}}catch{{return {{}}}}}};
const saveState=s=>localStorage.setItem(stateKey,JSON.stringify(s));
const fmt=d=>new Intl.DateTimeFormat("en-SE",{{day:"numeric",month:"short",year:"numeric"}}).format(new Date(d+"T12:00:00"));
const daysLeft=d=>Math.ceil((new Date(d+"T23:59:59+02:00")-today)/86400000);
function color(score){{return score>=90?'var(--green)':score>=80?'var(--accent)':score>=70?'var(--amber)':'var(--red)'}}
function populate(){{
 document.getElementById('newCount').textContent=positions.filter(p=>p.new_date===foundToday).length;
 document.getElementById('phdCount').textContent=positions.filter(p=>p.kind==='phd').length;
 document.getElementById('jobCount').textContent=positions.filter(p=>p.kind==='job').length;
 document.getElementById('urgentCount').textContent=positions.filter(p=>daysLeft(p.deadline)>=0&&daysLeft(p.deadline)<=7).length;
 const cities=[...new Set(positions.map(p=>p.city))].sort(); document.getElementById('cityFilter').insertAdjacentHTML('beforeend',cities.map(c=>`<option value="${{esc(c)}}">${{esc(c)}}</option>`).join(''));
}}
function render(){{
 const state=loadState(), status=document.getElementById('statusFilter').value, city=document.getElementById('cityFilter').value;
 let items=positions.filter(p=>p.kind===activeKind&&p.deadline>=foundToday&&(?: all entries )true);
 items=items.filter(p=>city==='all'||p.city===city).filter(p=>status==='all'||(status==='applied'?!!state[p.id]:!state[p.id]));
 items.sort((a,b)=>b.found_date.localeCompare(a.found_date)||b.fit_score-a.fit_score);
 const groups=Object.groupBy?Object.groupBy(items,p=>p.found_date):items.reduce((g,p)=>((g[p.found_date]??=[]).push(p),g),{{}});
 const root=document.getElementById('results');
 if(!items.length){{root.innerHTML='<div class="empty">No positions match this view. Try “All positions” or another tab.</div>';return}}
 root.innerHTML=Object.keys(groups).sort().reverse().map(day=>`<section><div class="day-header"><h2>${{day===foundToday?'Today · ':''}}${{fmt(day)}}</h2><div class="day-line"></div><span class="day-count">${{groups[day].length}} position${{groups[day].length===1?'':'s'}}</span></div><div class="cards">${{groups[day].map(p=>card(p,state)).join('')}}</div></section>`).join('');
 root.querySelectorAll('[data-applied]').forEach(el=>el.addEventListener('change',e=>{{const s=loadState();s[e.target.dataset.applied]=e.target.checked;saveState(s);render()}}));
}}
function card(p,state){{const left=daysLeft(p.deadline);return `<article class="card ${{state[p.id]?'applied':''}}"><div class="card-main"><div class="score" style="--score-color:${{color(p.fit_score)}}"><strong>${{p.fit_score}}</strong><small>fit / 100</small></div><div><div class="card-title"><h3>${{esc(p.title)}}</h3><span class="kind">${{p.kind}}</span></div><div class="meta"><span>${{esc(p.organization)}}</span><span>⌖ ${{esc(p.city)}}</span><span>ID ${{esc(p.id)}}</span><span>${{esc(p.employment)}}</span></div><p class="description">${{esc(p.description)}}</p></div><div class="deadline"><span class="label">Application deadline</span><span class="date">${{fmt(p.deadline)}}</span><span class="label">${{left<0?'closed':left===0?'closes today':left+' days left'}}</span></div></div><div class="card-extra"><div><h4>Why it matches</h4><ul class="matches">${{p.match_reasons.map(x=>`<li>${{esc(x)}}</li>`).join('')}}</ul></div><div><h4>Gaps to address honestly</h4><ul class="gaps">${{p.gaps.map(x=>`<li>${{esc(x)}}</li>`).join('')}}</ul></div></div><div class="card-actions"><a class="btn primary" href="${{esc(p.cv_pdf)}}" download="${{esc(p.download_name)}}">Download tailored CV</a><a class="btn" href="${{esc(p.cv_yml)}}" download>YAML</a><a class="btn" href="${{esc(p.source_url)}}" target="_blank" rel="noopener">Source</a><a class="btn" href="${{esc(p.apply_url)}}" target="_blank" rel="noopener">Apply ↗</a><label class="apply-check"><input type="checkbox" data-applied="${{esc(p.id)}}" ${{state[p.id]?'checked':''}}> I have applied</label></div></article>`}}
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{{document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));t.classList.add('active');activeKind=t.dataset.kind;render()}}));
document.getElementById('statusFilter').addEventListener('change',render); document.getElementById('cityFilter').addEventListener('change',render);
const setTheme=t=>{{document.documentElement.dataset.theme=t;localStorage.setItem('opportunity-theme',t)}};setTheme(localStorage.getItem('opportunity-theme')||((matchMedia('(prefers-color-scheme:light)').matches)?'light':'dark'));document.getElementById('themeBtn').onclick=()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
document.getElementById('exportBtn').onclick=()=>{{const blob=new Blob([JSON.stringify(loadState(),null,2)],{{type:'application/json'}}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='application_status.json';a.click();URL.revokeObjectURL(a.href)}};
document.getElementById('importInput').onchange=e=>{{const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=()=>{{try{{saveState(JSON.parse(r.result));render()}}catch{{alert('That file is not valid application status JSON.')}}}};r.readAsText(f)}};
populate();render();
</script>
</body></html>'''.replace("&&(?: all entries )true", "")


def main() -> None:
    TAILORED.mkdir(parents=True, exist_ok=True)
    RENDER_WORK.mkdir(parents=True, exist_ok=True)
    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    with MASTER.open(encoding="utf-8") as handle:
        master = yaml_engine.load(handle)
    for position in POSITIONS:
        render_position(yaml_engine, master, position)
    POSITIONS_FILE.write_text(json.dumps(POSITIONS, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_FILE.write_text(build_report(POSITIONS, FOUND_DATE), encoding="utf-8")
    print(json.dumps({"positions": len(POSITIONS), "phd": sum(p["kind"] == "phd" for p in POSITIONS), "jobs": sum(p["kind"] == "job" for p in POSITIONS), "report": str(REPORT_FILE), "tailored_dir": str(TAILORED)}, indent=2))


if __name__ == "__main__":
    main()
