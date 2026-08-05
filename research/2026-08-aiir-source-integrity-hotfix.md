# AIIR 1957 Source-Integrity Repair

**Date:** 2026-08-04
**NARA container:** NAID 311001910
**Scope:** Every canonical Atlas case linked to the 301-object *Air Intelligence Information Reports, 1957* digital unit

## Result

All six linked dossiers were reconciled against the raw NARA object sequence by OCR, visual page review, document continuity, and SHA-256 matching. The Atlas remains at exactly 146 canonical cases.

A follow-up independent audit found that the NARA unit contains duplicate scans of several reports. The initial repair had selected a later, disordered duplicate run for Hastings and an incomplete later duplicate subset for the Northern California radar report. It also exposed a deeper legacy problem in the Robins dossier: its title/location, summary, quotation, and images had been drawn from three different reports. This revision replaces those inherited mixtures with the earliest complete packet for each case.

## Canonical mappings

| Atlas case | Canonical NARA raw objects | Evidentiary role |
|---|---:|---|
| `BF-1956-DF-01` — DeFuniak Springs | `001–003` | Complete three-page report; quotation on `003` |
| `BF-1957-CG-01` — Cigar-Y / Sand Point | `015` | One-page report; Sand Point, Michigan location |
| `BF-1957-B47-01` — Eglin B-47 acceleration | `019–021` | Complete report; quotation on `020` |
| `BF-1957-HT-01` — Hastings | `048–054` | Official report `048–050`, transmittal `051`, complete witness statement `052–054`; quotation on `049` |
| `BF-1957-RA-01` — Robins AFB / Pine Grove railway sighting | `016–018` | Complete three-page Robins AFB report; official meteor-characteristics assessment on `018` |
| `BF-1957-NC-01` — Northern California radar skinpaint | `058–064` | AIIR `058`, routing `059–060`, control roster `061`, scope log `062`, operator statement `063`, route plot `064` |

## Duplicate-run reconciliation

- Hastings objects `243–251` are later duplicate scans of the `048–054` packet. They are less suitable as the canonical run because the witness statement is disordered and the sequence contains duplicate/reverse-side material.
- Northern California objects `258–264` duplicate portions of the `058–064` packet. The initial public selection (`258`, `260`) contained the report and one routing memorandum but omitted the scope log, operator statement, and route plot.
- The corrected Atlas uses the earliest complete occurrence in the 301-object NARA sequence and removes the superseded duplicate assets from the public manifest.

## Robins conflation correction

The inherited Robins dossier mixed three separate AIIR packets:

1. `005–007` — Shaw AFB air/ground fiery-ball report. The gravitational-trajectory assessment belongs to this report.
2. `016–018` — Pine Grove railway-observer report.
3. `055–057` — Warner Robins star-shaped-object report, one mile west of Robins AFB.

Following object-identity review, the canonical `BF-1957-RA-01` dossier maps only to the coherent Robins-origin packet at `016–018`: the Pine Grove railway-observer report. Its date, location, witness model, quotation, official assessment, taxonomy, phenomena fields, timeline language, source record, and visual treatment were rebuilt from those three pages. Objects `055–057` are a distinct later Warner Robins civilian report and are intentionally not assigned to this case; their unsupported narrative and images must not be restored here.

The corrected packet records three Southern Railway co-witnesses who described a green chord-with-handle or tadpole-shaped object with a yellow glowing trail for about one minute. Major John W. Porter recorded that the witnesses did not perceive a comet or meteor, while judging that the description indicated meteor characteristics.

## Provenance rules applied

- Public filenames identify the exact raw NARA object number.
- `source-file-index.json` points only to the corrected public assets and NARA catalog record.
- Source records distinguish what each packet supports from what it does not establish.
- Editorial reconstructions remain explicitly labeled and are not treated as event evidence.
- Superseded duplicate or unrelated images are removed rather than silently retained.

## Validation contract

The corrective release must pass:

1. `validate_atlas.py`
2. source-availability regeneration
3. operational-triage audit and regression test
4. NARA crosswalk regeneration
5. generated map/runtime synchronization
6. split-runtime payload contract
7. desktop/mobile navigation contract
8. browser QA for all six affected cases at desktop and mobile widths
9. post-deployment asset, payload, and browser verification

External archive outreach and new NARA/FOIA requests remain outside this repair.
