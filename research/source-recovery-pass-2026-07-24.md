# Source Recovery Pass — Ghost Rockets / Foo Fighters / Priority Public Records

**Date:** 2026-07-24  
**Atlas scope:** Existing 146-case UAP Atlas only  
**Control files:**

- `atlas-data.json`
- `source-file-index.json`
- `source-files/evidence-depth/GHOSTROCKETS-1946-CUSTODY-MAP.json`
- `research/atlas-nara-crosswalk-2026-07-22.json`

## Executive result

This pass promoted one material recovery into the live Atlas source layer:

- `BF-1946-GR-01` — Scandinavian Ghost Rockets now has an explicit 12-scan custody-map record and 12 local deployable PDF assets.

It did **not** over-promote unresolved leads:

- Foo Fighters still has exact AFHRA catalog custody but no recovered public microfilm images.
- Kecksburg still has a primary federal-court FOIA/legal anchor, not recovery proof.
- Aztec still has strong contradiction/fraud records, not crash evidence.
- Westall still has press/institutional archive support, not a recovered RAAF/police/school file.

## Promoted recovery

### `BF-1946-GR-01` — Scandinavian Ghost Rockets

Previous deployed state: official Riksarkivet topic and internal order citation were present, but the stronger local custody map was not fully promoted into deployable Atlas data.

Promoted state:

- Official archive creator: **Försvarsstaben**.
- Responsible unit: **Flyg- och luftförsvarsavdelningen**.
- Official series context: **Rymdprojektilkommittén**.
- Repository: **Riksarkivet i Täby / Krigsarkivet**.
- NAD/context lead: `Arkis f9c6788e-df68-414d-8f3e-ea41cb6946a9`.
- Internal reference: **Fst/L 12/6 1946 nr 7:49**.
- Strict mapped scans: **12**.
- Visual checks: `000682.pdf`, `000955.pdf`.
- Local deployable PDFs copied to:
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000183.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000203.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000301.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000498.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000682.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/000955.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/001115.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/001461.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/001570.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/001850.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/001981.pdf`
  - `assets/evidence/GHOSTROCKETS-1946/mapped-pdfs/002001.pdf`

### Explicit boundary

This is **not** a first-party Riksarkivet scan package. The public PDFs are Internet Archive derivatives from a private uploader. The promoted claim is narrower and stronger:

> the PDFs contain the same internal Swedish military reference and map back to the official Riksarkivet/Krigsarkivet record family, but exact volume/item shelfmarks and corpus completeness remain unresolved.

## Cases evaluated but not newly promoted

### `BF-1944-FF-01` — Foo Fighters

Already promoted:

- AFHRA IRIS `60059` — 415th NFS war diary, reel `0000000848`, frames `1519–1631`.
- AFHRA IRIS `60074` — daily operations reports, reel `0000000848`, frames `1763–1867`.
- AFHRA IRIS `1026183` — WWII notes, reel `33170`, frame `886` onward.

No new public original microfilm images were recovered in this pass. The next productive action remains an AFHRA electronic-copy request using `research/followup-record-recovery-2026-07-22/ARCHIVAL-REQUEST-DRAFTS.md`.

### `BF-1965-KB-01` — Kecksburg

Already promoted:

- *Kean v. NASA*, 480 F. Supp. 2d 150 (D.D.C. 2007), Civil Action No. 03-2500.

Boundary preserved: the opinion documents the FOIA/search dispute; it does **not** establish object recovery or physical chain of custody.

### `BF-1948-AZ-01` — Aztec

Already promoted:

- J. P. Cahn, 1952 *True* article scan.
- J. P. Cahn, 1956 *True* follow-up scan.
- FBI Vault Silas Newton six-part collection.

Boundary preserved: this strengthens the fraud/contradiction classification; it does **not** support a crash-retrieval claim.

### `BF-1966-WS-01` — Westall

Current support remains:

- State Library Victoria archival review.
- Dandenong Journal contemporary headline/sketch material.
- AFSR editor note.

No complete RAAF, police, or school administrative file was recovered in this pass.

## Crosswalk state after patch

| Case | Score | Remaining reasons | Public URLs | Local PDFs | Local custody files |
|---|---:|---|---:|---:|---:|
| `BF-1946-GR-01` Ghost Rockets | 5 | historical case lacks exact NAID; quote not verified to primary page | 8 | 12 | 18 |
| `BF-1944-FF-01` Foo Fighters | 6 | historical case lacks exact NAID; no complete local PDF; high-significance dossier | 3 | 0 | 6 |
| `BF-1965-KB-01` Kecksburg | 7 | historical case lacks exact NAID; no complete local PDF; quote not verified | 2 | 0 | 3 |
| `BF-1948-AZ-01` Aztec | 5 | historical case lacks exact NAID; no complete local PDF | 4 | 0 | 6 |
| `BF-1966-WS-01` Westall | 8 | one structured source record; historical case lacks exact NAID; no complete local PDF | 3 | 0 | 4 |

## Next recovery moves

1. **Foo Fighters:** send/request AFHRA electronic copies for IRIS `60059`, `60074`, `1026183`.
2. **Ghost Rockets:** request exact Riksarkivet volume/item shelfmarks for the `Fst/L 12/6 1946 nr 7:49` file family.
3. **Westall:** search/request Australian National Archives / RAAF / Victoria Police / school administrative files.
4. **Kecksburg:** locate NASA post-litigation search-return records and any Army recovery/transport chain.
5. **Aztec:** page-index FBI Newton Parts 01–06 for exact Aztec/Scully/Cahn references.
