from pathlib import Path

from ruamel.yaml import YAML

from build_test_report import POSITIONS, compatible_tailored_cv, rendercv_executable

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "master_profile" / "master_cv.yml"


def load_master():
    with MASTER.open(encoding="utf-8") as handle:
        return YAML().load(handle)


def test_project_uses_rendercv_28_environment():
    executable = rendercv_executable()

    assert executable.name == "rendercv.exe"
    assert executable.parent.parent.name == ".rendercv-venv"
    assert executable.exists()


def test_tailored_cv_preserves_rendering_guide_design_and_locale():
    master = load_master()
    tailored = compatible_tailored_cv(master, POSITIONS[0])

    assert tailored["design"] == master["design"]
    assert tailored["locale"] == {"language": "english"}


def test_rendering_guide_values_are_present():
    master = load_master()
    design = master["design"]

    assert design["theme"] == "classic"
    assert design["page"] == {
        "top_margin": "0.55in",
        "bottom_margin": "0.55in",
        "left_margin": "0.55in",
        "right_margin": "0.55in",
    }
    assert design["typography"]["alignment"] == "left"
    assert design["typography"]["font_size"] == {
        "body": "9.5pt",
        "name": "28pt",
        "headline": "9.5pt",
        "connections": "9.5pt",
        "section_titles": "1.35em",
    }
    assert design["entries"]["date_and_location_width"] == "2.4cm"
    assert design["templates"]["education_entry"]["date_and_location_column"] == "DATE"
    assert design["templates"]["experience_entry"]["date_and_location_column"] == "DATE"
    assert design["templates"]["normal_entry"]["date_and_location_column"] == "DATE"
