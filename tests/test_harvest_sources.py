import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "harvest_sources.py"


def load_module():
    spec = importlib.util.spec_from_file_location("harvest_sources", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_extracts_only_listing_links_and_deduplicates_absolute_urls():
    module = load_module()
    html = """
    <a href="/en/about-uu/join-us/jobs-and-vacancies/job-details?query=959399">PhD position</a>
    <a href="/en/about-uu/join-us/jobs-and-vacancies/job-details?query=959399">Duplicate</a>
    <a href="https://uu.varbi.com/en/what:job/jobID:960212">Varbi listing</a>
    <a href="/en/study/phd-studies">Not a listing</a>
    """
    source = {
        "name": "Uppsala University",
        "url": "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies?varbiCategory=PhD+positions",
        "listing_url_patterns": ["job-details?query=", "varbi.com/en/what:job/jobID:"],
    }

    assert module.extract_listing_urls(html, source) == [
        "https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies/job-details?query=959399",
        "https://uu.varbi.com/en/what:job/jobID:960212",
    ]


def test_extracts_listing_titles_for_fast_deterministic_triage():
    module = load_module()
    html = """
    <a href="/jobs/42"><span>PhD student</span> in computational biology</a>
    <a href="/about">About us</a>
    """
    source = {
        "name": "Example",
        "url": "https://example.org/jobs",
        "listing_url_patterns": ["/jobs/"],
    }

    assert module.extract_listing_candidates(html, source) == [
        {
            "url": "https://example.org/jobs/42",
            "title": "PhD student in computational biology",
        }
    ]


def test_manifest_marks_failed_source_without_losing_successful_candidates(monkeypatch):
    module = load_module()
    sources = [
        {
            "name": "Healthy",
            "url": "https://healthy.example/jobs",
            "listing_url_patterns": ["/jobs/"],
        },
        {
            "name": "Unavailable",
            "url": "https://down.example/jobs",
            "listing_url_patterns": ["/jobs/"],
        },
    ]

    def fake_fetch(url, timeout):
        if "down" in url:
            raise OSError("network unavailable")
        return '<a href="/jobs/42">Role</a>'

    monkeypatch.setattr(module, "fetch", fake_fetch)
    manifest = module.harvest(sources, timeout=2)

    assert manifest["summary"] == {
        "sources_total": 2,
        "sources_ok": 1,
        "sources_failed": 1,
        "sources_empty": 0,
        "candidate_urls": 1,
    }
    assert manifest["sources"][0]["candidate_urls"] == ["https://healthy.example/jobs/42"]
    assert manifest["sources"][1]["status"] == "failed"
    assert manifest["sources"][1]["error"] == "network unavailable"


def test_manifest_marks_required_source_empty_when_index_has_no_listing_urls(monkeypatch):
    module = load_module()
    source = {
        "name": "Empty source",
        "url": "https://empty.example/jobs",
        "listing_url_patterns": ["/jobs/"],
        "required": True,
    }

    monkeypatch.setattr(module, "fetch", lambda url, timeout: "<a href='/about'>About</a>")
    manifest = module.harvest([source], timeout=2)

    assert manifest["sources"][0]["status"] == "empty"
    assert manifest["summary"]["sources_empty"] == 1
