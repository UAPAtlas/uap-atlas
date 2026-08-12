# PURSUE Release 05 — Source-Depth Completion

**Date:** 2026-08-10
**Scope:** Three existing Atlas dossiers plus two Blackfile question surfaces
**Case contract:** 155 cases / 153 timeline entries / 129 projected terrestrial / 26 Orbital-Lunar

## Completed upgrades

### `BF-SF-07` — Project SIGN / Estimate of the Situation

DOW-UAP-D100 is now represented through three distinct primary-record layers:

1. **USAF/AMC acknowledgment and assessment — PDF pp. 1–3 and 7–9**
   - Headquarters USAF described it as “inescapable” that some type of flying object had been observed while identity and origin remained undetermined.
   - AMC retained reports without a reasonable everyday explanation while reporting no physical evidence and no tangible support for an interplanetary conclusion.
2. **RAND study request — PDF pp. 31–34**
   - AMC asked RAND to study whether reports might involve experimental “spaceships” or test vehicles and how such vehicles might be distinguished technically.
   - This is explicitly presented as a study request, not a finding.
3. **Project SIGN assignment and analytical architecture — PDF pp. 232–244**
   - Formal assignment of collection, collation, evaluation, and intelligence production to Air Materiel Command.
   - Early analytical material preserves recurring reported characteristics, radar cases, foreign-technology alternatives, and continued-investigation recommendations.

**Boundary retained:** DOW-UAP-D100 is not the missing Estimate of the Situation. The original document and its control, routing, transfer, or destruction trail remain active acquisition targets.

### `BF-2021-GOM-01` — Gulf of Oman AC-130 EO/IR Event

The dossier now surfaces the IIR’s direct-source and missing-data architecture:

- source had direct access through official duties;
- two reported cold objects approximately 0–20 feet above water near a flare for about 15 seconds;
- reported departure immediately after trigger pull and before cannon recoil;
- approximately 25 observations, coordinated “dolphins” motion, and groups of three;
- TACTOOL-derived estimates of 250–1,300 mph;
- coordinates derived from AC-130 sensor GPS;
- broad military/intelligence dissemination;
- attachment list of one video plus a PowerPoint containing six embedded videos;
- corrupted full DVR and absent native telemetry/metadata.

**Boundary retained:** The report remains “not finally evaluated intelligence.” PR117–PR122 are secondary recordings of a display and do not independently validate size, range, speed, response to gunfire, identity, or origin.

### `BF-1946-GR-01` — Scandinavian Ghost Rockets

The January 1947 `SECRET Intelligence Review` cover from DOW-UAP-D099 is now the documentary hero. The former Swedish archival-context image remains immediately behind it.

**Boundary retained:** The cover is an official publication cover, not an image of a reported ghost rocket.

### Blackfile Q6 / Q7

Both surfaces now carry one bounded D100 tension:

> **Internal uncertainty versus public messaging** — Project SIGN internally retained unexplained reports, considered domestic, foreign, and interplanetary possibilities, and sought RAND analysis while recommending narrower public disclosure centered on balloons, astronomical objects, and continuing investigation. This documents information management, not proof of a hidden non-human program.

Blackfile confidence levels were not changed.

## Deterministic impact

- **Cases added:** 0
- **Timeline entries added:** 0
- **Existing cases changed:** `BF-1946-GR-01`, `BF-SF-07`, `BF-2021-GOM-01`
- **Blackfile questions changed:** `q6`, `q7`
- **Selected new page renders:** 7
- **Source-index paths:** 952 after generation; 0 unavailable
- **Admission decisions unchanged:** D033 remains deferred; D034–D036 remain unidentified; no lower-confidence case was added.

## Generator ownership

`scripts/apply-2026-08-release05-source-depth-completion.py` is the authoritative final layer for these upgrades. It is idempotent and runs after earlier Release 05 admission/closure mutators. The Batch 01 mutator now invokes this final layer after its historical mutations so it cannot recreate the older D099/D100 presentation.
