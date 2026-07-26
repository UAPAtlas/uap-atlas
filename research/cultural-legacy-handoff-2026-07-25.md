# UAP Atlas Cultural Legacy — Release handoff

**Completed:** 2026-07-25
**Scope:** Full 146-case cultural-context review
**Release direction:** Public publication explicitly authorized by Jimmy

## Final result

All **146 existing dossiers** were assessed exactly once. Cultural Legacy remains an optional context layer and does not alter incident evidence, confidence, source counts, Evidence Lens, operational triage, or the fixed 146-case corpus.

- **13 implemented Cultural Legacy records**
- **0 deferred candidates**
- **133 reviewed with no consequential case-specific artifact located**
- **146 total cases preserved**
- **120 terrestrial Case Stack records preserved**
- **26 Orbital/Lunar records preserved**

## Implemented records

1. `BF-1944-FF-01` — Foo Fighters — band name
2. `BF-1947-KA-01` — “Flying saucer” enters the modern vocabulary
3. `BF-1947-RW-01` — International UFO Museum and Roswell UFO Festival
4. `BF-1951-YK-01` — Yorkshire Evening Press Topcliffe front page
5. `BF-1961-BH-01` — New Hampshire historical highway marker
6. `BF-1965-KB-01` — Kecksburg acorn monument and UFO Festival
7. `BF-1973-PG-01` — Pascagoula UFO historical marker
8. `BF-1975-TW-01` — *Fire in the Sky*
9. `BF-SF-13` — *The X-Files* — “I Want to Believe”
10. `BF-1980-RF-01` — Rendlesham Forest UFO Trail
11. `BF-1994-AR-01` — *Ariel Phenomenon*
12. `BF-1996-VG-01` — Memorial do ET and Varginha’s civic identity
13. `BF-1997-PH-01` — *The Phoenix Lights Documentary*

Every record includes a direct case relationship, date/period, local context image, alt text, source locator, creator/publisher credit, and the fixed boundary **“Cultural context — not case evidence.”**

## Media policy

Jimmy clarified that Atlas is a personal-use application and directed publication of the completed cards. Copyright clearance is therefore not used as a local inclusion gate. Provenance remains mandatory.

- Clearly licensed/public-domain media retains its license and license URL.
- Other media is labeled with an honest `rightsStatus`, such as **“Copyrighted theatrical artwork — source credited.”**
- No cultural image is stored in `heroVisual`, `images`, `evidenceImages`, Evidence Lens, or source-file counts.
- All cultural media remains isolated under `assets/context/`.

## Runtime and regression fixes

1. **Structured evidence-image normalization** — fixed a pre-existing `[object Object]` request exposed by the Betty and Barney Hill dossier. `evidenceItems()` now supports string paths and structured image records.
2. **Single-entry architecture** — canonical `atlas-mobile.html` remains a 550-byte compatibility redirect; the root application is the single responsive runtime.
3. **Rights metadata renderer** — Cultural Legacy supports either linked license metadata or source-credited `rightsStatus` text without fabricating a license.
4. **Targetable browser QA** — the 13-case cultural harness can test canonical HTML, deployment HTML, or a live URL.

## Verification

- Cultural contract: **PASS — 13 cases / 13 records**
- Exact reconciliation: **PASS — 146 = 13 implemented + 0 deferred + 133 none**
- Canonical runtime sync: **PASS — 146 cases / 120 projected**
- Deployment runtime sync: **PASS — 146 cases / 120 projected**
- Source availability: **PASS — 813 indexed / 677 actionable / 136 custody-only / 0 unavailable**
- Evidence Lens: **PASS — 146 cases**
- Navigation and single-entry contracts: **PASS**
- Canonical cultural browser QA: **PASS — 26 states / 13 cases / desktop + mobile**
- Deployment cultural browser QA: **PASS — 26 states / 13 cases / desktop + mobile**
- Canonical desktop/mobile/map regression: **PASS — zero console/page errors**
- Deployment desktop/mobile regression: **PASS**

## Durable files

- `atlas-data.json`
- `atlas-fresh.html`
- `atlas-responsive.html`
- `atlas-mobile.html`
- `assets/context/`
- `scripts/test-cultural-legacy.mjs`
- `scripts/qa-cultural-legacy.py`
- `scripts/reconcile-cultural-legacy-research.py`
- `research/cultural-legacy-tranche-2026-07-25.json`
- `research/cultural-legacy-tranche-2026-07-25.md`

## Release verification still required after push

- GitHub Actions Pages conclusion: success
- Live root HTTP 200
- All 13 context assets HTTP 200/206 with `image/*` MIME
- Live runtime contains 146 cases and 13 cultural records
- Live desktop/mobile cultural QA passes all 26 states
- Legacy `atlas-mobile.html` deep-link redirect remains functional
