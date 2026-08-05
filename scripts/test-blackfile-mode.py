#!/usr/bin/env python3
"""Contract for the integrated Blackfile analytical mode."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--html", default="index.html")
args = parser.parse_args()

html = (ROOT / args.html).read_text()
atlas = json.loads((ROOT / "atlas-data.json").read_text())
analysis = json.loads((ROOT / "blackfile-analysis.json").read_text())
runtime = (ROOT / "blackfile-analysis.js").read_text()
mode_js = (ROOT / "blackfile-mode.js").read_text()
mode_css = (ROOT / "blackfile-mode.css").read_text()
errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


require(analysis.get("schemaVersion") == 1, "Blackfile schemaVersion must be 1")
questions = analysis.get("questions", [])
require(len(questions) == 7, f"expected seven questions, found {len(questions)}")
require([q.get("id") for q in questions] == [f"q{i}" for i in range(1, 8)], "question IDs/order must be q1–q7")
require(analysis.get("analysisSource") == "Blackfile Seven Questions — State of Evidence (2026-08-05)", "controlling Seven Questions source missing")
require(analysis.get("boundarySource") == "D10 Contradiction & Interpretive-Boundary Ledger", "controlling D10 source missing")

case_ids = {case["id"] for case in atlas.get("cases", [])}
for q in questions:
    qid = q.get("id", "?")
    for field in ("title", "shortTitle", "status", "tone", "confidence", "answer"):
        require(bool(q.get(field)), f"{qid}: missing {field}")
    for field, minimum in (("findings", 3), ("counterEvidence", 2), ("missingEvidence", 3), ("tensions", 1), ("caseIds", 1)):
        value = q.get(field, [])
        require(isinstance(value, list) and len(value) >= minimum, f"{qid}: {field} must contain at least {minimum} entries")
    for case_id in q.get("caseIds", []):
        require(case_id in case_ids, f"{qid}: unknown Atlas case {case_id}")
    for tension in q.get("tensions", []):
        require(tension.get("label") and tension.get("summary"), f"{qid}: incomplete D10 tension")
        for case_id in tension.get("caseIds", []):
            require(case_id in case_ids, f"{qid}: D10 tension references unknown case {case_id}")

# Guard the reconciled proposition boundaries most likely to regress.
q = {item["id"]: item for item in questions}
require("does not establish that every case belongs to one phenomenon" in q["q1"]["answer"], "Q1 unified-phenomenon boundary regressed")
require("None supplies direct proof of non-human origin" in q["q2"]["answer"], "Q2 non-human-origin boundary regressed")
require("Deliberate nuclear interference is not established" in q["q3"]["answer"], "Q3 nuclear-causation boundary regressed")
require("does not prove recovery of anomalous craft or biological material" in q["q4"]["answer"], "Q4 retrieval boundary regressed")
require("Reverse engineering of non-human craft is not established" in q["q5"]["answer"], "Q5 reverse-engineering boundary regressed")
require("this does not make every denial false" in q["q6"]["answer"], "Q6 disinformation calibration regressed")
require("not proof of one continuous hidden crash-retrieval or reverse-engineering program" in q["q7"]["answer"], "Q7 continuity boundary regressed")
for token in ("Malmstrom", "Rendlesham", "Lazar", "Brown", "Bennewitz", "MJ-12"):
    require(token in json.dumps(analysis), f"D10 reconciliation missing {token}")

match = re.fullmatch(r"const blackfileAnalysis = (.*);\n", runtime, re.S)
require(bool(match), "blackfile-analysis.js must contain one generated constant")
if match:
    require(json.loads(match.group(1)) == analysis, "blackfile-analysis.js is not synchronized with canonical JSON")

required_html = (
    'id="blackfileModeToggle"',
    'aria-pressed="false"',
    'id="blackfileShell"',
    'id="blackfileSignal"',
    'id="blackfileConstellation"',
    'id="blackfileBrief"',
    'id="blackfileEvidence"',
    'data-blackfile="Questions"',
    'data-blackfile="Evidence"',
    'data-blackfile="Brief"',
    'href="blackfile-mode.css"',
    'src="blackfile-analysis.js"',
    'src="blackfile-mode.js"',
    'window.__blackfileInitialHash=location.hash;',
)
for needle in required_html:
    require(needle in html, f"HTML missing Blackfile contract: {needle}")
require("145 documented UAP cases" not in html, "stale 145-case metadata remains")
require("146 documented UAP cases" in html, "146-case metadata missing")
require("hidden>" in html[html.find('id="blackfileShell"') : html.find('id="blackfileShell"') + 160], "Blackfile shell must be hidden before JS initializes")

for needle in (
    "state.appMode = 'atlas'",
    "state.selectedQuestionId",
    "body.dataset.atlasMode",
    "params.set('mode', 'blackfile')",
    "window.blackfileMode",
    "event.stopImmediatePropagation()",
    "setAtlasMode('atlas', {write:false})",
    "window.__blackfileInitialHash",
    "if (modeIsBlackfile()) updateUrl();",
):
    require(needle in mode_js, f"mode controller missing: {needle}")
for needle in (
    'body[data-atlas-mode="blackfile"] .main',
    '.bf-question-node[data-question="q7"]',
    'body[data-atlas-mode="blackfile"][data-mobile-page="dossier"] .bf-brief-panel',
    '@media(max-width:1080px)',
    '@media(prefers-reduced-motion:reduce)',
):
    require(needle in mode_css, f"mode stylesheet missing: {needle}")

shell_start = html.find('<section class="blackfile-shell"')
shell_end = html.find('</section>\n <div class="console-footer">', shell_start)
blackfile_shell = html[shell_start:shell_end] if shell_start >= 0 and shell_end >= 0 else ""
public_text = "\n".join((json.dumps(analysis), runtime, mode_js, mode_css, blackfile_shell))
for forbidden in ("/Users/", "/Volumes/", "/private/tmp/", "Cortana Vault", "[REDACTED]"):
    require(forbidden not in public_text, f"public Blackfile artifacts expose forbidden string: {forbidden}")

if errors:
    print("BLACKFILE MODE CONTRACT FAILED")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)
print(f"BLACKFILE MODE CONTRACT OK: {len(questions)} questions · {len({cid for item in questions for cid in item['caseIds']})} linked cases")
