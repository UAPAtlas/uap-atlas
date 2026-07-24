# UAP Atlas — Priorities 1–5 Completion Report

**Date:** July 24, 2026
**Scope:** Existing cases and public/existing records only; no new cases, FOIA, outreach, or archival requests.

## 1. Integrity repair

- Fort Monmouth lead image now equals `image` and `images[0]`.
- Added one Fort Monmouth timeline event for 10–11 September 1951.
- Validator now rejects carousel/hero mismatches, counted cases without timeline coverage, missing lead assets, duplicate image arrays, and timeline references to unknown cases.

## 2. Washington D.C. 1952

- Expanded from one structured record to five evidence-separated records:
  - recovered NARA Blue Book page set;
  - Andrews/OSI spot report;
  - Ruppelt Staff Study;
  - CAA Technical Development Report No. 180;
  - OIN telephoned-report set.
- Added explicit supports and limitations for radar, visual, interceptor, investigation-capacity, and anomalous-propagation claims.
- Promoted the contemporaneous Andrews spot report to slide one.
- Added the Ruppelt Staff Study page as a locally deployed evidence asset.

## 3. Socorro and Killeen

### Socorro

- Split the FBI/Blue Book material into four structured records.
- Added page-located Zamora interview, field-trace description, and Air Force/FBI assessment images.
- Separated observed traces from what the record can establish about object identity.

### Killeen

- Split the 155-object AISS packet into packet, witness, balloon-test, and investigator-assessment records.
- Added the balloon-analysis and Captain Magee conclusion pages.
- Preserved the key boundary: the field investigation rejected the tested balloon candidate and endorsed witness reliability, but the packet still lacks a final ATIC/Blue Book disposition.

## 4. Public-record recovery queue

- Ghost Rockets: official Riksarkivet topic recovered; 1,779-PDF Internet Archive corpus preserved as an unverified lead, not promoted to custody.
- Foo Fighters: exact AFHRA reel/frame identifiers preserved; no original reel scans recovered.
- Westall: institutional context retained; tested A9755/22 PDF produced no Westall match and is recorded as a negative finding.
- Kecksburg: recovered *Kean v. NASA*, 480 F. Supp. 2d 150 (D.D.C. 2007), as the primary legal record for the FOIA dispute.
- Aztec: recovered Cahn’s 1952 and 1956 *True* articles and the FBI Vault Silas Newton collection; the Cahn opening pages were visually verified and added to the dossier.

Control files:

- `research/public-record-recovery-queue-2026-07-24.json`
- `research/public-record-recovery-queue-2026-07-24.md`

## 5. Evidence-depth reranking

The previous scorer treated almost every one-record dossier as weak. The new model classifies source shape before scoring:

- complete primary packet;
- multi-source independent;
- single primary record;
- thin summary;
- secondary only;
- mixed provenance.

Current result:

- 146 total cases;
- 18 complete-primary-packet cases;
- 11 multi-source-independent cases;
- 77 single-primary-record cases;
- 20 thin-summary cases;
- 18 secondary-only cases;
- 2 mixed-provenance cases;
- 84 cases in the actual weak queue at score ≥25;
- 119 broader enrichment candidates;
- Mantell is no longer misclassified as weak.

## Verification

- Canonical validator: **pass** — 146 cases, 144 timeline events, 5 location modes.
- Missing referenced lead assets: **0**.
- Desktop browser QA: **pass** — 146 cases, 144 timeline events, 121 markers, 0 console/page errors.
- Mobile browser QA: **pass** — 146 cases, Map/Cases/Dossier present, 0 console/page errors.
- Visual QA: Washington desktop/mobile and Aztec desktop render without broken media, clipping, or overlap.

Browser evidence: `qa/browser-qa-2026-07-24/`.
