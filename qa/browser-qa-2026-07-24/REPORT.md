# UAP Atlas — Browser QA

**Date:** July 24, 2026
**Artifacts:** `atlas-fresh.html`, `atlas-mobile.html`

## Automated browser checks

- Desktop: 146 cases, 144 timeline events, 121 rendered map markers.
- Mobile: 146 cases; Map / Cases / Dossier navigation present.
- Fort Monmouth: teletype is slide one; exactly one timeline event.
- Washington 1952: NARA PBB90-127 is slide one; Ruppelt and CAA source records are embedded.
- Socorro: landing-site image is slide one.
- Killeen: investigator conclusion page is slide one.
- Aztec: visually verified Cahn 1952 opening spread is slide one.
- All tested lead images loaded with nonzero natural width.
- Desktop console/page errors: 0.
- Mobile console/page errors: 0.

## Visual review

- Washington desktop: clean, readable, restrained; no overlap, clipping, or broken media.
- Washington mobile at 390×844: carousel, thumbnails, tabs, and three-page navigation render correctly; no overlap or broken media.
- Aztec desktop: Cahn spread is correctly displayed as the lead documentary image; no broken media or layout defects. The source scan is naturally high-contrast/dark, but remains an accurate documentary preview.

## Evidence

- `results.json`
- `desktop-washington-dossier.png`
- `mobile-washington-dossier.png`
- `desktop-aztec-dossier.png`
