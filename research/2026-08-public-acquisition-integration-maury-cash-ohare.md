# Public-only acquisition integration — Maury Island, Cash-Landrum, and O’Hare

Date: 2026-08-05

## Scope and boundary

This tranche followed a public-only recovery rule: public viewers, direct downloads, official pages, and clearly labeled public mirrors only. No outreach, requests, forms, accounts, payments, orders, or access-control bypasses were used.

The tranche changed three existing cases only:

- `BF-1947-MI-01` — Maury Island
- `BF-1980-CLD-01` — Cash-Landrum
- `BF-2006-OH-01` — O’Hare

No case, navigation, Blackfile question, or product feature was added.

## Acquisition outcomes

### Maury Island — recovered-new adjacent military record

Recovered a four-page Air Rescue Service Detachment 8 (62d AAF BU) **Final Mission Report**, dated 4 August 1947, from Internet Archive captures of a public personal-site mirror.

The scans document:

- B-25 `#1316` and the crash/recovery chronology;
- the report’s contemporaneous determination of a fire in the left engine;
- survivor/interrogation details and preliminary wreckage observations;
- classified material in the navigator’s kit; and
- transfer of recovered-document responsibility to a CIC agent.

The scan set is hash-manifested under `source-files/archives/MAURY-1947-ARS-FINAL-MISSION-REPORT/`.

Boundary: this is an Air Rescue Service mission report, **not** the complete formal accident-investigation board file. It does not identify the classified material as Maury fragments, does not connect alleged samples to the crash, and does not include the missing Seattle FBI report or slag laboratory/custody record.

Unresolved targets remain:

1. Complete Seattle FBI field report referenced in the 14 August 1947 teletype.
2. Complete formal AAF accident-investigation board record.
3. Laboratory report and sample custody record for the reported Tacoma slag.

### Cash-Landrum — recovered-new partial legal-file compilation

Recovered the 83-page AFU public mirror of **Quest Publications 101 — The Cash-Landrum File, Civil Action No. H-84-348**.

Verified payload:

- PDF 1.4, 83 pages, 28,429,852 bytes
- SHA-256 `c871d8f6eb68496a3fc92a8d1475a681fcabe6c9b67898f5f2ece3f21459a346`

The packet reproduces:

- the federal docket identity;
- the filed 21 August 1986 Order of Dismissal;
- government motion and memorandum;
- plaintiffs’ response; and
- NASA, Air Force, Navy, and Army declarations.

The packet is preserved under `source-files/archives/CASH-LANDRUM-1980-AFU-QUEST-H84-348/`.

Boundary: this is a third-party public mirror of a partial legal compilation, not a complete court-origin docket or authenticated medical/military operations packet. Pleadings and declarations are party positions and agency assertions. The short dismissal order does not adjudicate the reported event, object identity, medical causation, or helicopter origin.

Unresolved targets remain:

1. Complete court-origin federal file and authenticated medical/legal exhibits.
2. The defense’s underlying investigation.
3. Army/DoD/FAA/Fort Hood/III Corps/unit operations and CH-47 flight records.

### O’Hare — no recovered native payload; held-source factual repair

No new native FAA or United Airlines packet was recovered. Public results were duplicates, mirrors, or derivatives of material already represented through NARCAP and the FAA FOIA-log trail.

The held NARCAP report was re-read in full. It states that FAA supplied **13 one-minute NTAP primary/secondary radar data files** and publishes independent analyses that found no return corresponding to the reported stationary object near Gate C17 or its reported rapid departure.

The prior Atlas statement that “no radar analysis was published” was therefore false and was removed.

Boundary: the native 13 NTAP files, native tower audio, complete employee statements, full FAA production, United records, and airport-operations material remain outside mapped Atlas custody. A lack of a correlated radar return does not disprove the visual reports or establish object identity.

## Canonical repairs

- Added Maury ARS mission-report provenance and cause/custody boundaries.
- Added Cash-Landrum AFU/Quest legal-file provenance and corrected court-result language.
- Corrected Cash-Landrum witness roles and sensors from unrelated military/infrared metadata to three civilian unaided-visual witnesses.
- Corrected the Cash-Landrum timeline so dismissal is not presented as validation of the event.
- Corrected O’Hare radar-analysis language and added the published NTAP analysis boundary.
- Preserved all three cases as structured `acquisition_target` records because material primary classes remain missing.

## Regression contract

`scripts/test-public-acquisition-integration.py` protects:

- recovered-source identity and custody limitations;
- Maury crash-report versus sample-causation separation;
- Cash-Landrum civilian observation metadata and court/party-position separation;
- O’Hare published radar analysis versus missing-native-data separation; and
- continued acquisition-target ownership for all three cases.
