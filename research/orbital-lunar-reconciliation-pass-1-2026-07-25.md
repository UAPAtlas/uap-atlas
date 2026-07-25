# Orbital/Lunar Reconciliation Pass 1 — Apollo/Gemini/STS Primary Records

**Date:** 2026-07-25  
**Scope:** Dedicated Orbital/Lunar evidence-layer reconciliation. No new cases, no outreach, no private acquisition.

## Cases reconciled

- `BF-NASA-D001` — Apollo 12 Transcript
- `BF-NASA-D022` — Gemini 9 Debriefing
- `BF-NASA-D026` — Apollo 14 Debriefing Video Record
- `BF-NASA-D030` — STS-80 Unidentified Object Image 1
- `BF-NASA-D031` — STS-80 Unidentified Object Image 2
- `BF-NASA-D032` — STS-80 Unidentified Object Image 3

Each case now has enriched main source-record boundaries: 3 supports + 3 limitations.

## Boundary pattern

### Transcript/debriefing records

**Supports:** official NASA/War.gov mission transcript or debriefing custody, local page/ROI imagery, primary mission-document anchoring.

**Limitations:** released record preserves context but does not establish object origin; no complete sensor/trajectory/final-resolution packet mapped; belongs in Orbital/Lunar layer rather than default main-stack proof.

### STS-80 released-image records

**Supports:** official released image/frame artifact, local full-frame and ROI assets, primary visual custody.

**Limitations:** image alone does not establish identity/distance/scale/trajectory/origin; no full native mission sequence/calibration/trajectory analysis mapped; unresolved visual artifact, not standalone proof.

## Source-index hardening

Fixed `NASA-UAP-D030` source-token mapping and added alias support for the filename-style source token used by STS-80 image 1.

```text
NASA-UAP-D030 mapped paths: 6
```

## Local verification

```text
caseCount: 146
sourceRecordCount: 234
sourceDepthWeakCaseCount: 70
casesWithMappedLinks: 146
casesWithPublicSourceUrls: 146
missingLocalAssets: []
static invalid refs: 0
/Users paths: 0
file:// strings: 0
bad Commons file-page refs: 0
patched cases: 6/6
```
