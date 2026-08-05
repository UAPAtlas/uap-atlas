# Blackfile Boundary and Quality-Queue Calibration

Date: 2026-08-05
Scope: Existing 19-case `quality_upgrade` queue; focused factual repair for `BF-SF-12`, `BF-1947-MI-01`, and `BF-2023-WUS-03`
Policy: Existing Atlas triage and Blackfile/D10 boundaries only; no new framework, case, outreach, or UI work

## Result

| Operational category | Before | After | Change |
|---|---:|---:|---:|
| True gaps | 0 | 0 | — |
| Quality upgrades | 19 | 13 | −6 |
| Acquisition targets | 13 | 15 | +2 |
| Complete | 114 | 118 | +4 |

The shift is conservative rather than confidence inflation:

- Santilli and Maury move from `quality_upgrade` to `acquisition_target` because load-bearing primary records remain absent.
- Western U.S. Federal LE, 2015 Navy videos, Langley incursions, and Robins AFB become `complete` after repairing factual fields or false-positive audit logic.
- Missing raw sensor material remains an explicit limitation; a complete released record set is not treated as proof of reported object identity or performance.

## Focused case decisions

### BF-SF-12 — Santilli “Alien Autopsy” Film

**Decision:** `acquisition_target`

Current local custody is a contextual preview, generated manifest, and Atlas audit note. It does not contain the exact 1995 broadcast, exact 2006 interview, production documentation, or an original master/negative. The prior dossier treated a reported “restoration” phrase as a verified confession and labeled the case `resolved-fabrication`; current custody cannot carry that conclusion.

Structured targets now identify the exact interview, first-generation broadcast/production record, claimed original film material, and exact John Humphreys admission record. The dossier is retained as a provenance-control case, not as Roswell evidence or a settled confession record.

### BF-1947-MI-01 — Maury Island Affair

**Decision:** `acquisition_target`

Held primary custody: FBI file 62-83894, *UFO Part 1 of 16*, official 69-page FBI Vault PDF.

The 14 August 1947 Seattle teletype on PDF p. 46 states that the redacted subject **“did not admit … that his story was a hoax”** and instead said he would call it a hoax if questioned to avoid further trouble. The record supports official investigation, reported Tacoma-slag analysis, and strong publicity/profit suspicion; it does not support the confession previously attributed to Dahl.

The complete Seattle field report referenced by the teletype, the AAF B-25 accident investigation, and the laboratory/sample custody record are not mapped and are now structured acquisition targets. The mapped part-file does not establish crash causation or a causal link to alleged samples.

### BF-2023-WUS-03 — Western U.S. Federal LE Encounters

**Decision:** `complete`

Held primary custody: the complete released set of five first-hand Memoranda for Record, `DOW-UAP-D079` through `DOW-UAP-D083`, each dated 2 June 2026 and preserving reports by five federal law-enforcement special agents about events over two days in October 2023.

Repairs separate encounter date from memorandum date, enumerate five records and five witnesses, remove inherited military/intelligence-role metadata, distinguish illustrative renderings from event imagery, and use the exact Witness 2 wording: **“The objects initially appeared to mimic vehicles.”** Publication authenticates the released narratives, not the phenomena, identity, performance, or origin.

## Full 19-row calibration

| Case | Calibrated lane | Basis / next action |
|---|---|---|
| `BF-SF-08` COMETA | Durable limitation / wording repair | Strong report custody; confidence language should distinguish exact report text from non-governmental institutional interpretation. |
| `BF-SF-12` Santilli | Acquisition | Exact interview, broadcast, production, and original-film custody absent. |
| `BF-SF-13` Billy Meier | Acquisition | No neutral first-generation photographic custody or independent authentication packet. |
| `BF-1947-MI-01` Maury Island | Acquisition | Official part-file held; complete Seattle report, crash investigation, and sample custody absent. |
| `BF-1973-PG-01` Pascagoula | Acquisition | Complete sheriff/interview packet and original covert-recording custody absent. |
| `BF-1978-VL-01` Valentich | Acquisition | Official trail is described but exact originating records are not mapped. |
| `BF-1997-PH-01` Phoenix Lights | Acquisition | Retrospective material dominates; contemporaneous operational records remain the useful target. |
| `BF-1978-KK-01` Kaikoura | Acquisition | First-generation film and radar workpapers remain missing. |
| `BF-2024-AS-01` Arabian Peninsula | Durable limitation / wording repair | Exact official release is held; broader interpretation remains unsupported and should stay bounded. |
| `BF-2023-WUS-03` Western U.S. Federal LE | Complete after repair | Complete five-memorandum released set held; raw-sensor limitations retained. |
| `BF-1944-FF-01` Foo Fighters | Acquisition | Primary microfilm/archival record remains unsecured despite a useful secondary and USAF trail. |
| `BF-1946-GR-01` Ghost Rockets | Source-verification/acquisition | Derivative packet held; exact first-party archival scan/custody remains the key upgrade. |
| `BF-1977-CB-01` Colares | Provenance wording repair | Primary record exists; `sourceQuality` remains generic. |
| `BF-2025-YS-01` Yellow Sea | Provenance wording repair | Primary record exists; `sourceQuality` remains generic. |
| `BF-1989-BW-01` Belgian Wave | Provenance wording repair | Primary record exists; `sourceQuality` remains generic. |
| `BF-1957-RA-01` Robins AFB | Complete / audit false positive | Detailed primary provenance was incorrectly caught by a broad prefix test. |
| `BF-2015-NAV-01` Navy video series | Complete / audit false positive | Multiple mapped source aliases were masked by the first locator. |
| `BF-2023-LG-01` Langley incursions | Complete / audit false positive | Multiple mapped source aliases were masked by the first locator. |
| `BF-2024-CH-01` Chapel Hill | Focused quality repair | Exact selected quotation/page verification remains unresolved. |

## Audit correction

`audit-atlas-data.py` previously stopped source-index matching when the primary `sourceLocator` was found, masking sibling aliases contained in structured source records. It also treated every detailed `Primary source — …` provenance statement as generic. The corrected audit:

1. counts the primary locator **and** all exact sibling source aliases in the factual payload;
2. limits generic-provenance detection to genuinely generic values;
3. preserves conservative quote-confidence and acquisition triggers.

Regression contract: `scripts/test-blackfile-boundary-queue-calibration.py`.

## Blackfile boundary

Question 4 retains its conclusion: crash-retrieval claims and record gaps are documented; anomalous retrieval remains unproven. A new tension note records that Maury supplies suspicion without confession and Santilli lacks exact admission/originating-film custody. The interpretive conclusion is unchanged; only the evidentiary boundary is tightened.
