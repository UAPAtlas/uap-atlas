# AIIR 1957 Source-Integrity Hotfix

**Date:** 2026-08-04
**Archive container:** NARA NAID 311001910, *Air Intelligence Information Reports: 1957* (301 digital objects)

## Scope

Audited every Atlas case tied to the AIIR 1957 compilation using:

1. SHA-256 matching between published assets and all 301 raw objects;
2. targeted OCR of candidate report ranges;
3. visual review of report headers, page numbers, continuation boundaries, transmittals, and witness attachments;
4. quote-location verification;
5. runtime source-token/index reconciliation.

Government archival custody establishes the record and its routing. It does not establish the reported object’s identity or the accuracy of witness estimates.

## Repaired mappings

### BF-1956-DF-01 — DeFuniak Springs

- Previous gallery: unrelated raw objects 017, 019, and 020.
- Correct packet: raw objects **001–003**.
- Complete three-page TR-1-57 report.
- Key high-velocity assessment: object **003**.

### BF-1957-B47-01 — B-47 acceleration

- Previous gallery: unrelated raw objects 011–013.
- Correct packet: raw objects **019–021**.
- Complete three-page IR-2-57 report.
- Mach 2/3 language: object **020**.
- Recovered metadata: sighting **15 April 1957**, Eglin AFB, Florida.
- Corrected map placement from a generalized U.S. centroid to Eglin AFB.

### BF-1957-HT-01 — Hastings

- Previous gallery: raw object 015, which belongs to the separate cigar-Y report.
- Correct archival range: raw objects **243–251**.
- Public gallery now maps:
  - official report: 243–245;
  - transmittal: 246;
  - witness statement in logical reading order: 250, 249, 251.
- Omitted from the gallery: duplicate transmittal 247 and reverse scan 248.
- Separating/rejoining and arrowhead language: official report object **244**, repeated in witness statement object **249**.

### BF-1957-NC-01 — Northern California radar skinpaint

- Previous gallery: unrelated raw objects 100–102.
- Correct case report: raw object **258**.
- Routing memorandum: object **260**.
- Duplicate routing scan omitted.
- Recovered exact report location: **35°30′N, 124°30′W**.

## Verified mappings retained

### BF-1957-CG-01 — Cigar-Y

- Raw object **015** was already correct.
- Recovered location: St. Martins Bay, off Sand Point, Michigan.
- Sighting date: 9 August 1957.

### BF-1957-RA-01 — Robins AFB

- Raw objects **016–018** were already correct.
- Key assessment: object **018**.
- Recovered sighting date: 10 March 1957.

## Runtime/index correction

All six case source labels now exactly contain their `source-file-index.json` keys. This repairs Evidence Lens source-token resolution in addition to correcting the visible galleries.

## Verification

- `validate_atlas.py`: PASS — 146 cases.
- Atlas data audit: PASS — 146/146 cases with evidence assets, indexed source links, structured source records, and public source URLs.
- Operational triage test: PASS.
- Source availability: 818 indexed paths; 0 unavailable.
- Replacement assets: byte-for-byte SHA-256 matches against their stated raw NARA objects.

## Remaining gaps

- DeFuniak: no additional witness/follow-up packet located.
- B-47: aircraft/unit identity and follow-up investigation remain absent.
- Hastings: no radar confirmation or photographic evidence.
- Northern California: mission logs, full aircraft/crew identity, and referenced explanatory enclosure remain absent.
- Cigar-Y: witness identity remains redacted; no follow-up located.
- Robins: specific witness identities and follow-up investigation remain absent.
