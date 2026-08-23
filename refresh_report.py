from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from build_test_report import build_report

ROOT = Path(__file__).resolve().parent
POSITIONS = ROOT / "data" / "positions.json"
REPORT = ROOT / "index.html"

report_date = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
date.fromisoformat(report_date)
positions = json.loads(POSITIONS.read_text(encoding="utf-8"))
REPORT.write_text(build_report(positions, report_date), encoding="utf-8")
print(json.dumps({"report_date": report_date, "positions": len(positions), "report": str(REPORT)}))
