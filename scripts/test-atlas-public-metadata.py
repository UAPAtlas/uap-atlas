#!/usr/bin/env python3
"""Regression tests for Atlas public metadata counts and latest audit freshness."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update-atlas-public-metadata.py"


def load_module():
    spec = importlib.util.spec_from_file_location("atlas_public_metadata", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def current_counts():
    atlas = json.loads((ROOT / "atlas-data.json").read_text())
    cases = atlas["cases"]
    timeline = atlas.get("timeline") or atlas.get("timelineEvents") or []
    return {
        "records": len(cases),
        "cases": sum(1 for case in cases if case.get("countInCaseTotals", True)),
        "timeline": len(timeline),
        "sourceRecords": sum(len(case.get("sourceRecords") or []) for case in cases),
    }


def test_public_metadata_updater_preserves_copy_except_count():
    module = load_module()
    counts = module.load_counts(ROOT / "atlas-data.json")
    assert_equal(counts, current_counts(), "derived counts")

    with tempfile.TemporaryDirectory() as temp:
        html = Path(temp) / "index.html"
        shutil.copyfile(ROOT / "index.html", html)
        # Artificially stale the copy so the updater has work to do.
        stale_text = html.read_text().replace(
            f"{counts['records']} documented UAP cases", "150 documented UAP cases"
        )
        html.write_text(stale_text)
        before = html.read_text()
        changed = module.update_html(html, counts, noun="cases")
        after = html.read_text()

    assert changed, "stale fixture should require metadata count update"
    assert f"{counts['records']} documented UAP cases" in after
    assert "150 documented UAP cases" not in after
    normalized_before = before.replace("150 documented UAP cases", "COUNT documented UAP cases")
    normalized_after = after.replace(f"{counts['records']} documented UAP cases", "COUNT documented UAP cases")
    assert_equal(normalized_after, normalized_before, "only stale metadata counts changed")


def test_check_mode_detects_stale_copy_and_accepts_updated_copy():
    with tempfile.TemporaryDirectory() as temp:
        html = Path(temp) / "index.html"
        shutil.copyfile(ROOT / "index.html", html)
        # Artificially stale the copy so --check detects drift.
        counts = current_counts()
        stale_text = html.read_text().replace(
            f"{counts['records']} documented UAP cases", "150 documented UAP cases"
        )
        html.write_text(stale_text)
        stale = subprocess.run(
            [sys.executable, str(SCRIPT), "--atlas-data", str(ROOT / "atlas-data.json"), "--html", str(html), "--check"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert_equal(stale.returncode, 1, "stale check return code")

        subprocess.run(
            [sys.executable, str(SCRIPT), "--atlas-data", str(ROOT / "atlas-data.json"), "--html", str(html)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        fresh = subprocess.run(
            [sys.executable, str(SCRIPT), "--atlas-data", str(ROOT / "atlas-data.json"), "--html", str(html), "--check"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert_equal(fresh.returncode, 0, "fresh check return code")


def test_latest_audit_summary_matches_authoritative_current_outputs():
    latest = json.loads((ROOT / "qa" / "latest-audit-summary.json").read_text())
    audit = json.loads((ROOT / "qa" / "atlas-data-code-audit.json").read_text())
    triage = json.loads((ROOT / "qa" / "atlas_operational_triage.json").read_text())
    counts = current_counts()

    expected_fields = {
        "caseCount": counts["records"],
        "countedCaseCount": counts["cases"],
        "timelineEventCount": counts["timeline"],
        "sourceRecordCount": counts["sourceRecords"],
        "operationalTriageCounts": triage["counts"],
        "sourceDepthWeakCaseCount": audit["sourceDepthWeakCaseCount"],
        "sourceDepthEnrichmentCandidateCount": audit["sourceDepthEnrichmentCandidateCount"],
        "sourceDepthWeakThreshold": audit["sourceDepthWeakThreshold"],
    }
    for field, expected in expected_fields.items():
        assert_equal(latest.get(field), expected, f"latest {field}")

    assert "/Users/" not in json.dumps(latest)
    assert "/private/tmp" not in json.dumps(latest)


def main():
    tests = [
        test_public_metadata_updater_preserves_copy_except_count,
        test_check_mode_detects_stale_copy_and_accepts_updated_copy,
        test_latest_audit_summary_matches_authoritative_current_outputs,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
