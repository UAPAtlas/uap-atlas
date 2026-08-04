# Hill and Ariel source-enrichment release

**Date:** 2026-08-04
**Scope:** `BF-1961-BH-01`, `BF-1994-AR-01`
**Canonical case count:** 146

## Betty and Barney Hill — official federal file layer

Integrated three unchanged JPEG objects selected from the 57-object Project Blue Book file unit in NARA NAID `28994660`, RG 341, series NAID `597821`:

- object `1043` — Project 10073 Record Card;
- object `1044` — UFO Analysis Sheet;
- object `1046` — 1963 Foreign Technology Division status memorandum naming the Hill sighting and its official handling.

The selected files are mapped through `assets/evidence/HILL-1961/NARA-NAID-28994660-selected.provenance.json`. Their byte lengths and SHA-256 values were verified against both the public selected-page sidecar and the complete 57-object custody manifest retained in durable source intake.

### Boundary

The NARA packet authenticates the federal file, Blue Book handling, and official evaluation of the September 1961 sighting. It does **not** independently authenticate the later hypnosis-derived abduction narrative, recovered-memory claims, occupants, radar correlation, or an extraordinary origin.

The defined federal-file acquisition target is now complete. Other later-material gaps remain stated as limitations rather than being allowed to reopen the completed official-file target.

## Ariel School — contemporaneous derivative publication layer

Integrated four 180-DPI page renders from locally retained derivative PDF scans of Cynthia Hind's *UFO Afrinews*:

- No. 11, PDF pp. 12–13 — opening Ariel report, witness-count statement, and drawing context;
- No. 12, PDF pp. 6–7 — follow-up reporting, John Mack context, Figure 2 site map, and soil-sampling context.

The original PDFs, rendered assets, dimensions, byte lengths, and SHA-256 values are recorded in `assets/sources/ARIEL-1994/afrinews-selected.provenance.json`.

### Boundary

*UFO Afrinews* is a near-contemporaneous investigative publication, but the retained PDFs are later derivative scans. They are not the original Mack/Hind interview archive, unedited recordings, first-generation notes, original witness drawings, or raw laboratory/custody records.

The prior pseudo-quotation was replaced with the page-verified wording: “Out of the 250 children at the school, more than 60 were now witnesses to an extraordinary event.”

Ariel remains an `acquisition_target` for four explicitly structured targets:

1. complete unedited 1994 interview footage and original Mack/Hind field materials;
2. first-party *UFO Afrinews* publisher custody;
3. an official Zimbabwean, Ariel School, or police investigative packet;
4. soil-sampling raw laboratory data and chain-of-custody records.

## Operational outputs

Regenerated:

- source availability;
- operational triage and acquisition-target artifacts;
- source-depth weak-case and enrichment artifacts;
- Atlas-to-NARA JSON and Markdown crosswalks;
- generated map/runtime payloads;
- split runtime synchronization.

Resulting triage:

- true gaps: 0;
- quality upgrades: 35;
- acquisition targets: 13;
- complete: 98.

Hill is `complete`; Ariel is `acquisition_target`. The triage and Evidence Lens regression contracts enforce both transitions through the structured `acquisitionTargets` field.

## Release acceptance

Passed locally in the clean deployment clone:

- 146-case schema validation;
- source availability: 834 indexed paths, 698 actionable, 136 custody-only, 0 unavailable;
- operational-triage regression;
- runtime synchronization and payload contract;
- health, navigation, single-entry redirect, Evidence Lens, Cultural Legacy, and source-availability contracts;
- responsive build idempotence across two consecutive runs;
- focused Playwright QA for Hill and Ariel on desktop and 390px mobile: four states, four screenshots, all seven new images decoded, zero console/page/request failures;
- representative visual review with no clipping, overflow, broken media, or layout regression.

No archive outreach, researcher contact, paid order, FOIA request, or NARA request was made in this release.
