# UAP Atlas Systems Leap — Operational Backlog Recalibration

**Date:** 2026-07-25

**Scope:** Phase A / Leap 3. Audit and backlog systems only. No cases added, no source requests sent, and no UI changes.

## Problem corrected

The legacy weakness score combined three different conditions:

1. structural defects;
2. internal metadata or quote-verification upgrades;
3. evidence that can only improve through external source acquisition.

It also treated conservative `thin-summary` and unresolved-context language as active weakness after records had already been operationally completed. This left completed Orbital/Lunar records in the active queue.

## New operational triage

`scripts/audit-atlas-data.py` now assigns every case to one mutually exclusive category, in this priority order:

1. `true_gap` — missing main source record, empty supports/limitations, missing source-token mapping, or missing local mapped asset;
2. `acquisition_target` — the next material improvement requires an unrecovered official packet, first-party custody, authenticated original, native agency media, or unmapped primary pages;
3. `quality_upgrade` — internally actionable quote/source-confidence, generic provenance, secondary-only, or thin index improvements;
4. `complete` — no current structural, acquisition, or internal-upgrade trigger.

The old weakness outputs remain available for compatibility, but they no longer control the authorized internal queue.

## Generated artifacts

- `qa/atlas_operational_triage.json`
- `qa/atlas_true_gaps.json`
- `qa/atlas_quality_upgrades.json`
- `qa/atlas_acquisition_targets.json`
- `qa/enrichment-backlog.json` schema v2

The sole enrichment backlog now contains only `true_gap` and `quality_upgrade` records. Acquisition targets are tracked separately, and FOIA/archive requests and outreach remain unauthorized.

## Current state

```text
true gaps: 0
quality upgrades: 44
acquisition targets: 14
operationally complete: 88
case total: 146
Orbital/NASA complete: 26/26
active internal backlog: 44
```

## Regression protection

Added:

- `scripts/test-audit-operational-triage.py`
- `scripts/state-of-atlas.py`

The test verifies:

- exactly one category per case;
- 146 unique cases represented;
- category counts reconcile;
- category artifacts match the unified triage;
- the active backlog excludes acquisition and complete cases;
- all 26 Orbital/NASA records remain operationally complete.

The State of the Atlas runner executes both audit and regression test, then prints a concise weekly summary with top structural, acquisition, and internal-upgrade priorities. It performs no outreach, deployment, or case addition.
