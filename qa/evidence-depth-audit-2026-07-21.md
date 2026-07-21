# UAP Atlas — Evidence Depth Audit & Enrichment Report
**Date:** July 21, 2026
**Total cases:** 144
**Status:** Completed — Atlas validates clean

---

## Audit Summary

| Metric | Before | After | Delta |
|---|---|---|---|
| Cases with `image` field | 140/144 (97%) | 142/144 (98%) | +2 |
| Cases with `images[]` carousel | 66/144 (46%) | 142/144 (98%) | +76 |
| Cases with `observation.witnessRoles` | 59/144 (41%) | 144/144 (100%) | +85 |
| Cases with `observation.sensors` | 60/144 (42%) | 144/144 (100%) | +84 |
| Cases with `phenomena.shapes` | 54/144 (38%) | 111/144 (77%) | +57 |
| Cases with `keyQuote` | 94/144 (65%) | 144/144 (100%) | +50 |
| Image files missing on disk | 1 | 0 | -1 |
| Carousel files missing on disk | 3 | 0 | -3 |

## Fixes Applied

### 1. File Integrity — Killeen BF-1954-KL-01
- **Issue:** Atlas referenced `killeen-1954_page-001.png` but files on disk were `killeen-1954_killeen-001.jpg` (different naming AND extension)
- **Fix:** Updated `image`, `images[]`, and `heroVisual.src` to reference actual .jpg files (5 carousel images instead of 3)

### 2. Missing Hero Images — 4 Cases
- **BF-1965-G7-01** (Gemini 7 Bogey): Added NASA-UAP-D021 pages as hero + carousel (3 pages)
- **BF-1973-SL-01** (Skylab Object): Added NASA-UAP-D7 pages as hero + carousel (3 pages)
- **BF-1955-USSR-01** (USSR 12,000 km/h): CIA blocks automated PDF download. **Manual action needed.**
- **BF-1951-YK-01** (Yorkshire Flying Saucer): CIA blocks automated PDF download. **Manual action needed.**

### 3. Evidence Enrichment — 93 Cases
- **Witness roles:** Extracted from summaries using pattern matching for pilot, military, law enforcement, civilian, scientific, intelligence, and named-individual categories
- **Sensors:** Extracted from summaries for radar, infrared/thermal, photographic/film, visual, electronic/signal, communications, targeting-pod, sonar, satellite
- **Shapes:** Extracted from summaries for 15+ shape categories (disc, cigar, sphere, triangle, crescent, light, fireball, formation, diamond, oval, etc.)
- **33 cases** have no shapes because they are document/program records (NASA debriefs, COMETA, AAWSAP, Grusch, etc.) where no visual shape description exists in the source

### 4. Key Quote Enrichment — 50 Cases
- Added quotable text from summaries for all 50 cases missing `keyQuote`
- Labeled as `web article quote — summary of record` where the quote is a summary rather than a page-located primary source quotation
- NASA debrief cases labeled as `summary of document record`

### 5. Carousel Images — 76 Cases
- Mapped source preview images to carousel arrays
- Mapped evidence directory files to carousel arrays for cases with existing evidence dirs (Nimitz, CEFAA, Omaha, Bennewitz, etc.)
- Himalayan series mapped to CIA-UAP-016 event-specific page renders

### 6. Generated File Rebuild
- Ran `node scripts/build-atlas-map.mjs` for D3 Natural Earth projection
- Hydrated `atlas-data.generated.json` with projected x/y coordinates (142 mapped, 2 orbital)
- Merged `mapGeometry` SVG paths for 6 geometry-pilot cases
- Validation: **ATLAS VALID: 144 cases, 142 timeline events, 5 location modes**

## Remaining Gaps (2 Cases)

| Case ID | Title | Issue | Action |
|---|---|---|---|
| BF-1955-USSR-01 | USSR — Objects at 12,000 km/h (Mach 10) | No image, no carousel — CIA-UAP-018 PDF download blocked | Download CIA-RDP81R00560R000100020012-7.pdf via browser, render pages with PyMuPDF |
| BF-1951-YK-01 | Yorkshire 'Perfect Flying Saucer' — RAF Standing Committee | No image, no carousel — CIA-UAP-014 PDF download blocked | Download CIA-RDP81R00560R000100020013-6.pdf via browser, render pages with PyMuPDF |

Both cases reference CIA FOIA reading room documents that block automated curl downloads. The documents are accessible at:
- `https://www.cia.gov/readingroom/document/cia-rdp81r00560r000100020012-7`
- `https://www.cia.gov/readingroom/document/cia-rdp81r00560r000100020013-6`

## Methodology
- Compared `atlas-data.json` against `atlas-data.before-canon-expansion.json` to identify 98 newly added cases
- Audited all 144 cases against the full schema (60+ fields per case)
- Verified file existence on disk for all `image` and `images[]` paths
- Cross-referenced with `source-file-index.json` and evidence directory inventory
- All enrichment extracted from existing summary/official/sourceRecords text — no external data added without source
