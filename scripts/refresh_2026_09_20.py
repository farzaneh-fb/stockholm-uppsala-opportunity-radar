"""Apply the 2026-09-20 audited opportunity refresh.

This script never writes the immutable master CV. It records candidate triage, removes
expired active listings, and adds the one newly accepted official vacancy.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TODAY = "2026-09-20"

NEW_POSITION = {
    "id": "UU_967249",
    "kind": "phd",
    "title": "PhD-student in Evolutionary and Ecological Genetics",
    "short_title": "evolutionary_ecological_genetics",
    "organization": "Uppsala University",
    "city": "Uppsala",
    "location_detail": "Department of Ecology and Genetics, Evolutionary Biology Center",
    "found_date": TODAY,
    "new_date": TODAY,
    "published": None,
    "deadline": "2026-11-01",
    "employment": "Full-time doctoral employment, 4 years",
    "fit_score": 78,
    "fit_label": "Good stretch match",
    "description": "Experimental and computational evolutionary-genetics research using RNA-seq, DNA pool-seq, comparative genomics and phenotypic data from an evolve-and-resequence seed-beetle system.",
    "match_reasons": [
        "Documented bioinformatics study, R/Python analysis and reproducible workflows are relevant to the project's genomics and scripting focus",
        "Molecular-biology, sequencing-data and experimental research experience provides a useful bridge between wet-lab and computational work",
        "Research publications, independent project work and collaboration at KI, KTH and SciLifeLab support doctoral research readiness",
        "The advert explicitly welcomes applicants from bioinformatics or related fields and values server/cluster pipeline experience"
    ],
    "gaps": [
        "Ecology, evolutionary biology and population-genetics concepts are not explicitly documented in the master CV",
        "No documented experimental-evolution, insect-model or genetic-strain work",
        "Experience applying statistical methods to quantitative-genetic or population-genomic data should be demonstrated only where substantiated"
    ],
    "source_url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=967249",
    "apply_url": "https://uu.varbi.com/en/what:login/type:job/jobID:967249",
    "contact": "David Berger — david.berger@ebc.uu.se",
    "headline": "Bioinformatics & Molecular Biology Researcher | Genomics, Reproducible Analysis & Experimental Research",
    "statement": "Interdisciplinary researcher with a biology research and publication background, now building bioinformatics skills alongside molecular and cellular laboratory experience. I use R, Python, Linux and reproducible workflows to work with sequencing and transcriptomic data, and I am comfortable connecting experimental questions with computational analysis. I would bring this bridge between wet-lab and computational colleagues to evolutionary-genetics research while developing deeper expertise in ecology, population genomics and quantitative genetics.",
    "section_order": [
        "Personal Statement",
        "Education",
        "Bioinformatics & Computational Biology Projects",
        "Computational Biology & Bioinformatics Skills",
        "Research Experience",
        "Wet Lab & Experimental Expertise",
        "Peer-Reviewed Publications",
        "Conference Presentations",
        "Professional & Personal Skills",
        "Teaching & Mentorship",
        "Awards & Honors",
        "References"
    ]
}


def stable_id(url: str, organization: str) -> str:
    if "jobID:" in url:
        value = url.split("jobID:", 1)[1].split("/", 1)[0]
        return ("KI" if "ki" in url else "SU") + "_" + value
    if "kth.se" in url:
        value = urlparse(url).path.rstrip("/").split("/")[-1]
        return f"KTH_{value}"
    if "uu.se" in url:
        value = parse_qs(urlparse(url).query).get("query", [""])[0]
        return f"UU_{value}" if value else "UU_UNKNOWN"
    if "slu.se" in url:
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        return "SLU_" + slug.upper().replace("-", "_")
    return organization.upper().replace(" ", "_") + "_UNKNOWN"


def triage_item(candidate: dict, organization: str, active_ids: set[str]) -> dict:
    url = candidate["url"]
    item_id = stable_id(url, organization)
    item = {"url": url, "title": candidate.get("title", ""), "stable_id": item_id}
    if item_id == NEW_POSITION["id"]:
        item.update({"status": "accepted_new", "reason": "Live official PhD vacancy verified and accepted after realistic-fit review."})
    elif item_id in active_ids:
        item.update({"status": "active_existing", "reason": "Live official vacancy retained in the active report."})
    elif item_id == "UU_961661":
        item.update({"status": "not_selected", "reason": "Live official PhD vacancy reviewed; the advert requires Swedish fluency and specific biomedical-laboratory-science preparation and clinical sample-handling experience not documented in the master CV."})
    elif item_id == "KI_965275":
        item.update({"status": "not_selected", "reason": "Live official PhD vacancy reviewed; it requires a Swedish medical degree and very good Swedish, neither documented in the master CV."})
    elif item_id == "KTH_960673":
        item.update({"status": "not_selected", "reason": "Official candidate reviewed; required Machine Learning/AI/Signal Processing/Computer Vision degree and documented deep-neural-network and computer-vision experience are not established in the master CV."})
    else:
        item.update({"status": "not_selected", "reason": "Official candidate reviewed; it is outside target scope, expired/unverified, duplicate discovery signal, or did not clear the realistic-fit gate."})
    return item


def main() -> None:
    manifest_path = DATA / "discovery_manifest.json"
    positions_path = DATA / "positions.json"
    seen_path = DATA / "seen_positions.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    positions = json.loads(positions_path.read_text(encoding="utf-8"))
    seen = json.loads(seen_path.read_text(encoding="utf-8"))

    # Keep only currently active records and the newly accepted vacancy.
    positions = [position for position in positions if position["deadline"] >= TODAY and position["id"] != NEW_POSITION["id"]]
    positions.append(NEW_POSITION)
    positions.sort(key=lambda position: (position["kind"], position["deadline"], position["id"]))
    active_ids = {position["id"] for position in positions}

    # Reconcile the dynamic official SLU page. Its directly observed PhD listing is
    # in Umeå and therefore belongs in audit accounting, not the regional report.
    slu_url = "https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies/doktorand-i-biologi/"
    for source in manifest["sources"]:
        if source["name"] == "SLU vacancies":
            source["candidate_urls"] = [slu_url]
            source["candidates"] = [{
                "url": slu_url,
                "title": "PhD Student position in Biology, specialisation in Environmental Science"
            }]
            source["reconciliation"] = "Official-domain search and direct official index check completed; the observed PhD listing is in Umeå, outside the Stockholm/Solna/Uppsala/Ultuna scope."
        source["triage"] = [triage_item(candidate, source["organization"], active_ids) for candidate in source.get("candidates", [])]
        if source["name"] == "SLU vacancies":
            source["triage"][0]["status"] = "not_selected"
            source["triage"][0]["reason"] = "Official SLU listing reviewed during dynamic-source reconciliation; Umeå is outside the geographic scope."

    all_urls = {url for source in manifest["sources"] for url in source.get("candidate_urls", [])}
    manifest["generated_at"] = "2026-09-20T20:07:18.647528+00:00"
    manifest["summary"]["candidate_urls"] = len(all_urls)

    seen.setdefault(NEW_POSITION["id"], {"source_url": NEW_POSITION["source_url"], "first_seen": TODAY})
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    positions_path.write_text(json.dumps(positions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    seen_path.write_text(json.dumps(seen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"active": len(positions), "new": NEW_POSITION["id"], "candidate_urls": len(all_urls)}))


if __name__ == "__main__":
    main()
