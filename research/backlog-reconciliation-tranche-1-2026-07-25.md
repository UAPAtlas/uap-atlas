# Backlog-Driven Reconciliation Tranche 1 — Main Stack Official/Public Cases

**Date:** 2026-07-25  
**Scope:** Existing matrix/backlog/source-index reconciliation only. No new cases, no FOIA/outreach, no private acquisition.

## Operating correction

This tranche used the existing Atlas enrichment system instead of creating another matrix:

- `qa/enrichment-backlog.json`
- `qa/source-depth-weak-case-priorities.json`
- `research/atlas-dossier-case-by-case-visual-matrix-2026-07-18.md`
- `research/atlas-nara-crosswalk-2026-07-22.json`
- `source-file-index.json`
- local evidence-depth notes and mapped assets

## Cases reconciled

### `BF-2023-WUS-03` — Western U.S. Federal LE Encounters

Patched the main official-release narrative record.

**Supports now states:**
- official release context for the Western U.S. federal law-enforcement narratives;
- five mapped released narrative/contact images in the source index;
- series-level support rather than isolated witness anecdote.

**Limitations now states:**
- no complete investigative packets/raw sensor/witness files;
- no exact NARA mapping or complete local PDF custody packet;
- unresolved/reporting status only, not object identity.

### `BF-SF-09` — AAWSAP / AATIP & Skinwalker

Patched the main program/contract trail record.

**Supports now states:**
- government-funded UAP-adjacent program/contract ecosystem;
- relationship between DIA study work, DIRD-style papers, and later AATIP/Skinwalker narratives;
- institutional significance of government money/private contractors/anomalous-topic research.

**Limitations now states:**
- program existence does not validate Skinwalker phenomena or recovered-tech claims;
- complete primary contract packet/workpapers/page-verified quote custody remain missing;
- interviews/documentaries are context, not substitute evidence.

### `BF-1978-KK-01` — Kaikoura Lights

Patched the main official-investigation/media trail record using the existing Archives New Zealand recovery note.

**Supports now states:**
- RNZAF/DSIR-style official investigation context;
- recovered Archives New Zealand page summarizing analysis and film-copy issues;
- filmed/radar public-record status with government analytical attention.

**Limitations now states:**
- no first-generation TV1/Fogarty film, Crockett copy, native radar logs, or complete analytical workpapers;
- recovered page does not establish what produced lights/radar returns;
- extraordinary interpretation limited by missing native custody/final disposition.

### `BF-1978-VL-01` — Valentich Disappearance

Patched the main NAA/ATSB/transcript trail record.

**Supports now states:**
- official disappearance file and accident-investigation context;
- final-communications/transcript trail anchoring the UFO-related narrative;
- primary-record aviation disappearance with unusual observations before loss of contact.

**Limitations now states:**
- transcript/file do not prove cause or object identity;
- no wreckage, recovered aircraft, complete radar/sensor chain, or definitive causal finding mapped;
- public retellings must be separated from official record.

### `BF-2019-OM-01` — USS Omaha Sphere & Swarm Events

Patched the main official/public media record.

**Supports now states:**
- public video-frame imagery and official/public media records;
- Omaha video frame, DVIDS official media link, and contextual imagery in source index;
- modern Navy sensor/media event with public confirmation context.

**Limitations now states:**
- no complete raw sensor/deck-log/radar/EW packet;
- released imagery does not establish object identity, underwater transition mechanics, or non-human origin;
- broader swarm chronology remains incomplete without full logs/metadata/workpapers.

## Incidental hardening

Removed an unrelated Nimitz Wikimedia Commons `wiki/File:` runtime source-page URL from `atlas-data.json` and `source-file-index.json`. The official DVIDS video link remains available; the Commons file page was not a deploy-safe runtime source.

## Local verification

```text
caseCount: 146
sourceRecordCount: 236
sourceDepthWeakCaseCount: 76
casesWithMappedLinks: 146
casesWithPublicSourceUrls: 146
missingLocalAssets: []
static invalid refs: 0
/Users paths: 0
file:// strings: 0
bad Commons file-page refs in live HTML artifact: 0
patched cases: 5/5 with enriched main supports + limitations
```
