# Evidence-Depth Tranche — Top 10 Crosswalk Cases

**Date:** 2026-07-24  
**Control file:** `research/atlas-nara-crosswalk-2026-07-22.json`  
**Scope:** First pass on the curated top 10 evidence-depth upgrade queue.

## Summary

This tranche did not add speculative evidence or new cases. It tightened the Atlas source records where the existing corpus already supported clearer claims, and made unresolved custody gaps more explicit.

## Cases reviewed

1. `BF-1948-MT-01` — Mantell Pursuit Fatality
2. `BF-1944-FF-01` — Foo Fighters, European Theater
3. `BF-1946-GR-01` — Scandinavian Ghost Rockets
4. `BF-1950-GF-01` — Great Falls / Mariana Film
5. `BF-1952-TM-01` — Tremonton / Newhouse Film
6. `BF-1956-LB-01` — Lakenheath-Bentwaters Radar-Visual Case
7. `BF-1965-KB-01` — Kecksburg Object Recovery Narrative
8. `BF-1948-AZ-01` — Aztec Crash Fraud
9. `BF-1953-RP-00` — Robertson Panel Recommendations
10. `BF-1966-WS-01` — Westall School Mass Sighting

## Cases already strong enough for this pass

These records already had explicit supports/limitations and/or exact custody sufficient for the current Atlas layer:

- **Mantell** — exact NARA NAID 28930550; witness/analysis pages visually verified. Remaining gap is independent balloon-launch/flight records, not Atlas source-record wording.
- **Foo Fighters** — AFHRA catalog custody + CUFON official-record transcription boundary already documented. Remaining gap is original microfilm scans.
- **Ghost Rockets** — Swedish archival family and internal order citation already documented. Remaining gap is item-level shelfmark/first-generation scan/RG 59 diplomatic file.
- **Great Falls** — exact NARA case file and motion-picture item custody present. Remaining gap is first-generation film / missing-frame chain.
- **Tremonton** — exact NARA case file and motion-picture item custody present. Remaining gap is first-generation 16 mm original / full lab ledger.
- **Robertson Panel** — source record already has concrete supports and limitations; remaining gap is restricted/missing implementation records.

## Patched cases

### `BF-1956-LB-01` — Lakenheath-Bentwaters

Filled empty supports/limitations for:

- `DOW-UAP-D096 · Project Blue Book correspondence`
- `CIA-UAP-015 · Project Blue Book Special Report No. 14`

Boundary now states that these are useful official-source/context paths but do **not** replace the exact NARA case file, raw radar plots, controller logs, voice recordings, or RAF interceptor mission records.

**Crosswalk score after patch:** 1  
**Remaining reasons:** no complete local PDF in mapped custody; high-significance dossier.

### `BF-1965-KB-01` — Kecksburg

Updated the primary public-record source to explicitly support only:

- the contested recovery narrative’s public/witness/FOIA-litigation context;
- the current research trail before any new archival recovery;
- separation of public narrative from unrecovered agency custody.

Limitations now explicitly say no original agency case file, recovery/transport record, complete contemporaneous witness packet, or chain-of-custody record is mapped.

**Crosswalk score after patch:** 7  
**Remaining reasons:** historical case lacks exact NAID; no complete local PDF; quote not verified to primary page.

### `BF-1948-AZ-01` — Aztec

Reframed the case as a fraud/contradiction boundary case, not as crash evidence. The source record now supports:

- Scully/Newton/GeBauer claim-chain context;
- fraud/contradiction classification;
- value as a hoax/disinformation boundary case.

Limitations now state that direct Cahn exposé, Scully text, and conviction/court-record citations are still needed for boss-grade certainty.

**Crosswalk score after patch:** 7  
**Remaining reasons:** historical case lacks exact NAID; no complete local PDF; quote not verified to primary page.

### `BF-1966-WS-01` — Westall

Updated source quality and the source record to cite the actual deployed evidence boundary:

- Dandenong Journal headline/sketch material;
- State Library Victoria archival review;
- AFSR editor note.

Limitations now explicitly state that no complete RAAF, police, or school administrative case file has been recovered, and that press/archive artifacts support occurrence/coverage rather than object identity.

**Crosswalk score after patch:** 8  
**Remaining reasons:** one structured source record; historical case lacks exact NAID; no complete local PDF.

## Verification

Regenerated:

- `atlas-fresh.html`
- `atlas-mobile.html`
- `assets/generated/atlas-map.json`
- `assets/generated/atlas-data.generated.json`
- `qa/atlas-data-code-audit.json`
- `qa/all-cases-final-source-coverage.json`
- `qa/source-depth-weak-case-priorities.json`
- `research/atlas-nara-crosswalk-2026-07-22.json`
- `research/atlas-nara-crosswalk-2026-07-22.md`

Audit state after patch:

```text
caseCount: 146
missingLocalAssets: 0
NARA statusCounts: exact-naid 21 / no-exact-nara-mapping 115 / collection-guide-only 10
```

## Next tranche recommendation

Do not continue polishing wording for records that already disclose their limits. The next productive work is source recovery for the remaining hard gaps:

1. **Ghost Rockets** — exact Swedish item-level shelfmark/scans + RG 59 diplomatic reporting.
2. **Foo Fighters** — AFHRA/NARA microfilm images for 415th NFS war diary and operations reports.
3. **Kecksburg** — NASA search/loss records, FBI/USAF local response records, recovery/transport chain.
4. **Aztec** — primary Cahn/Scully/conviction record packet for fraud classification.
5. **Westall** — RAAF/Australian National Archives/police/school administrative file search.
