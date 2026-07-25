#!/usr/bin/env python3
from pathlib import Path
import json
import time

try:
    from playwright.sync_api import sync_playwright
except Exception as exc:  # pragma: no cover - explicit operator message
    raise SystemExit(
        "Playwright is required. In this Hermes environment run: "
        "PYTHONPATH=/tmp/pw npm run atlas:qa"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CASE_COUNT = len(json.loads((ROOT / "atlas-data.json").read_text())["cases"])
HTML = ROOT / "atlas-fresh.html"
QA = ROOT / "qa"
QA.mkdir(exist_ok=True)
URL = HTML.resolve().as_uri() + f"?qa={int(time.time())}"

SCREENSHOTS = {
    "world": QA / "atlas-coordinate-rebuild-world.png",
    "phoenix_normal": QA / "atlas-coordinate-rebuild-phoenix-normal.png",
    "pantex_normal": QA / "atlas-coordinate-rebuild-pantex-normal.png",
    "greece_swir": QA / "atlas-next-tranche-greece-swir.png",
    "greece_swir_dossier": QA / "atlas-next-tranche-greece-swir-dossier.png",
    "gulf_parent": QA / "atlas-depth-gulf-series-parent.png",
    "gulf_balloon": QA / "atlas-depth-gulf-balloon-child.png",
    "gulf_parent_dossier": QA / "atlas-depth-gulf-series-dossier.png",
    "greece_series": QA / "atlas-depth-greece-series-parent.png",
    "greece_series_dossier": QA / "atlas-depth-greece-series-dossier.png",
    "minot": QA / "atlas-depth-minot.png",
    "minot_dossier": QA / "atlas-depth-minot-dossier.png",
    "jal_route": QA / "atlas-geometry-jal-route.png",
    "rb47_route": QA / "atlas-geometry-rb47-route.png",
    "nimitz_area": QA / "atlas-geometry-nimitz-area.png",
    "valentich_route": QA / "atlas-geometry-valentich-route.png",
    "belgian_area": QA / "atlas-geometry-belgian-area.png",
    "himalayan_parent": QA / "atlas-himalayan-series-parent.png",
    "himalayan_child": QA / "atlas-himalayan-series-child.png",
    "navy_parent": QA / "atlas-navy-series-parent.png",
    "gimbal": QA / "atlas-modern-gimbal.png",
    "gofast": QA / "atlas-modern-gofast.png",
    "aguadilla": QA / "atlas-modern-aguadilla.png",
    "shag_harbour": QA / "atlas-historical-shag-harbour.png",
    "coyne": QA / "atlas-historical-coyne.png",
    "trindade": QA / "atlas-historical-trindade.png",
    "stephenville": QA / "atlas-historical-stephenville.png",
    "langley": QA / "atlas-sensitive-site-langley.png",
    "malmstrom": QA / "atlas-sensitive-site-malmstrom.png",
    "rendlesham": QA / "atlas-sensitive-site-rendlesham.png",
    "phoenix_highcontrast": QA / "atlas-coordinate-rebuild-phoenix-highcontrast.png",
    "pantex_highcontrast": QA / "atlas-coordinate-rebuild-pantex-highcontrast.png",
    "los_alamos_highcontrast": QA / "atlas-coordinate-rebuild-los-alamos-highcontrast.png",
    "cheyenne_highcontrast": QA / "atlas-coordinate-rebuild-cheyenne-highcontrast.png",
    "malmstrom_highcontrast": QA / "atlas-coordinate-rebuild-malmstrom-highcontrast.png",
}

ANCHORS = {
    "phoenix_normal": "BF-1997-PH-01",
    "pantex_normal": "BF-2015-PX-04",
    "greece_swir": "BF-2024-GR-25",
    "gulf_parent": "BF-2020-AG-00",
    "gulf_balloon": "BF-2020-AG-D7",
    "greece_series": "BF-2023-GR-00",
    "minot": "BF-1968-MN-01",
    "jal_route": "BF-1986-JAL-01",
    "rb47_route": "BF-1957-RB-01",
    "nimitz_area": "BF-2004-NM-01",
    "valentich_route": "BF-1978-VL-01",
    "belgian_area": "BF-1989-BW-01",
    "himalayan_parent": "BF-1968-HIM-01",
    "himalayan_child": "BF-1968-HIM-07",
    "navy_parent": "BF-2015-NAV-01",
    "gimbal": "BF-2015-GIMBAL-01",
    "gofast": "BF-2015-GOFAST-01",
    "aguadilla": "BF-2013-AG-01",
    "shag_harbour": "BF-1967-SH-01",
    "coyne": "BF-1973-CY-01",
    "trindade": "BF-1958-TR-01",
    "stephenville": "BF-2008-SV-01",
    "langley": "BF-2023-LG-01",
    "malmstrom": "BF-1967-MA-01",
    "rendlesham": "BF-1980-RF-01",
    "phoenix_highcontrast": "BF-1997-PH-01",
    "pantex_highcontrast": "BF-2015-PX-04",
    "los_alamos_highcontrast": "BF-1949-LA-00",
    "cheyenne_highcontrast": "BF-2022-CS-01",
    "malmstrom_highcontrast": "BF-1967-MA-01",
}

GEOMETRY_CASES = {
    "BF-1986-JAL-01", "BF-1957-RB-01", "BF-1978-VL-01",
    "BF-2004-NM-01", "BF-1997-PH-01", "BF-1989-BW-01",
}

HIGH_CONTRAST_CSS = """
#stateLines { opacity: .82 !important; mix-blend-mode: normal !important; }
.us-state-line { stroke: #ffdf5a !important; stroke-width: .09 !important; filter: drop-shadow(0 0 .45px rgba(255,223,90,.45)) !important; }
.land { stroke: rgba(220,235,250,.18) !important; }
"""

NEW_CASES = [
    "BF-2023-LG-01",
    "BF-2004-NM-01",
    "BF-1957-RB-01",
    "BF-1986-JAL-01",
    "BF-1967-MA-01",
    "BF-1980-RF-01",
    "BF-1976-TH-01",
    "BF-1997-PH-01",
    "BF-1989-BW-01",
    "BF-1977-CL-01",
    "BF-2015-PX-04",
    "BF-1949-LA-00",
    "BF-2022-IQ-02",
    "BF-2023-BC-01",
    "BF-1973-SS-01",
    "BF-2025-USIC-01",
    "BF-2023-IQ-20",
    "BF-2023-GR-33",
    "BF-2023-SY-74",
    "BF-2024-GR-25",
    "BF-2020-AG-00",
    "BF-2020-AG-D3",
    "BF-2020-AG-D4",
    "BF-2020-AG-D5A",
    "BF-2020-AG-D5B",
    "BF-2020-AG-D6",
    "BF-2020-AG-D7",
    "BF-2023-GR-00",
    "BF-2023-GR-35",
    "BF-1968-MN-01",
]
HIMALAYAN_CASES = [f"BF-1968-HIM-{number:02d}" for number in range(1, 8)]
MODERN_CASES = ["BF-2015-NAV-01", "BF-2015-GIMBAL-01", "BF-2015-GOFAST-01", "BF-2013-AG-01"]
HISTORICAL_CASES = ["BF-1967-SH-01", "BF-1973-CY-01", "BF-1958-TR-01", "BF-2008-SV-01"]
SOURCE_CASES = NEW_CASES + HIMALAYAN_CASES + MODERN_CASES + HISTORICAL_CASES

def select_case(page, case_id):
    page.evaluate(
        """(caseId) => {
            if (typeof window.selectCase !== 'function') throw new Error('selectCase is not available');
            window.selectCase(caseId, true);
        }""",
        case_id,
    )
    page.wait_for_timeout(220)

with sync_playwright() as p:
    launch = {"headless": True}
    system_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if system_chrome.exists():
        launch["executable_path"] = str(system_chrome)
    browser = p.chromium.launch(**launch)
    page = browser.new_page(viewport={"width": 1208, "height": 867}, device_scale_factor=1)
    console_errors = []
    page_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.goto(URL, wait_until="load")
    page.wait_for_timeout(500)

    page.screenshot(path=str(SCREENSHOTS["world"]), full_page=True)
    geometry_checks = {}
    for key in ["phoenix_normal", "pantex_normal", "greece_swir", "gulf_parent", "gulf_balloon", "greece_series", "minot", "jal_route", "rb47_route", "nimitz_area", "valentich_route", "belgian_area", "himalayan_parent", "himalayan_child", "navy_parent", "gimbal", "gofast", "aguadilla", "shag_harbour", "coyne", "trindade", "stephenville", "langley", "malmstrom", "rendlesham"]:
        case_id = ANCHORS[key]
        select_case(page, case_id)
        page.screenshot(path=str(SCREENSHOTS[key]), full_page=True)
        if case_id in GEOMETRY_CASES:
            geometry_checks[case_id] = page.evaluate(
                """(caseId) => {
                    const layer = document.querySelector(`#caseGeometry [data-id="${caseId}"]`);
                    const shape = layer?.querySelector('.case-geometry-shape');
                    return {
                        selected: state.selectedCaseId,
                        rendered: Boolean(layer && shape),
                        pathLength: shape?.getAttribute('d')?.length || 0,
                        kind: layer?.dataset.kind || '',
                        ariaLabel: layer?.getAttribute('aria-label') || '',
                    };
                }""",
                case_id,
            )

    page.add_style_tag(content=HIGH_CONTRAST_CSS)
    for key in ["phoenix_highcontrast", "pantex_highcontrast", "los_alamos_highcontrast", "cheyenne_highcontrast", "malmstrom_highcontrast"]:
        select_case(page, ANCHORS[key])
        page.screenshot(path=str(SCREENSHOTS[key]), full_page=True)

    new_case_sources = {}
    for case_id in SOURCE_CASES:
        select_case(page, case_id)
        new_case_sources[case_id] = page.evaluate(
            """(caseId) => {
                if (typeof openFullCase !== 'function') throw new Error('openFullCase is not available');
                openFullCase(caseId);
                const sourceTab = document.querySelector('#caseDrawer [data-tab="sources"]');
                if (!sourceTab) throw new Error(`sources tab missing for ${caseId}`);
                sourceTab.click();
                const panel = document.querySelector('#caseDrawer [data-panel="sources"]');
                return {
                    selected: state.selectedCaseId,
                    links: panel ? panel.querySelectorAll('.file-link').length : 0,
                    missing: panel ? panel.querySelectorAll('.file-missing').length : 0,
                    drawerOpen: document.getElementById('drawerBackdrop').classList.contains('open'),
                };
            }""",
            case_id,
        )
        if case_id == "BF-2024-GR-25":
            page.screenshot(path=str(SCREENSHOTS["greece_swir_dossier"]), full_page=True)
        elif case_id == "BF-2020-AG-00":
            page.screenshot(path=str(SCREENSHOTS["gulf_parent_dossier"]), full_page=True)
        elif case_id == "BF-2023-GR-00":
            page.screenshot(path=str(SCREENSHOTS["greece_series_dossier"]), full_page=True)
        elif case_id == "BF-1968-MN-01":
            page.screenshot(path=str(SCREENSHOTS["minot_dossier"]), full_page=True)
        page.evaluate("closeFullCase()")

    series_checks = page.evaluate(
        """() => {
            const parentId = 'BF-1968-HIM-01';
            const childIds = Array.from({length: 6}, (_, i) => `BF-1968-HIM-${String(i + 2).padStart(2, '0')}`);
            const parent = atlasData.cases.find(c => c.id === parentId);
            const children = childIds.map(id => atlasData.cases.find(c => c.id === id));
            const timeline = atlasData.timeline || [];
            return {
                parentPresent: Boolean(parent),
                parentRole: parent?.recordRole || '',
                parentCounted: parent?.countInCaseTotals,
                childIds: parent?.childCaseIds || [],
                childrenPresent: children.every(Boolean),
                childOrders: children.map(c => c?.seriesOrder),
                childSeriesIds: [...new Set(children.map(c => c?.seriesId))],
                childTimelineIds: timeline.filter(e => e.seriesId === parentId).map(e => e.caseId),
                parentTimelineCount: timeline.filter(e => e.caseId === parentId).length,
            };
        }"""
    )

    navy_series_checks = page.evaluate(
        """() => {
            const parentId = 'BF-2015-NAV-01';
            const childIds = ['BF-2015-GIMBAL-01', 'BF-2015-GOFAST-01'];
            const parent = atlasData.cases.find(c => c.id === parentId);
            const children = childIds.map(id => atlasData.cases.find(c => c.id === id));
            const timeline = atlasData.timeline || [];
            return {
                parentPresent: Boolean(parent),
                parentRole: parent?.recordRole || '',
                parentCounted: parent?.countInCaseTotals,
                childIds: parent?.childCaseIds || [],
                childrenPresent: children.every(Boolean),
                childOrders: children.map(c => c?.seriesOrder),
                childSeriesIds: [...new Set(children.map(c => c?.seriesId))],
                childTimelineIds: timeline.filter(e => e.seriesId === parentId).map(e => e.caseId),
                parentTimelineCount: timeline.filter(e => e.caseId === parentId).length,
            };
        }"""
    )

    depth_series_checks = page.evaluate(
        """() => [
            ['BF-2020-AG-00', ['BF-2020-AG-D3','BF-2020-AG-D4','BF-2020-AG-D5A','BF-2020-AG-D5B','BF-2020-AG-D6','BF-2020-AG-D7']],
            ['BF-2023-GR-00', ['BF-2023-GR-33','BF-2023-GR-35']],
        ].map(([parentId, childIds]) => {
            const parent = atlasData.cases.find(c => c.id === parentId);
            const children = childIds.map(id => atlasData.cases.find(c => c.id === id));
            const timeline = atlasData.timeline || [];
            return {
                parentId,
                parentRole: parent?.recordRole || '',
                parentCounted: parent?.countInCaseTotals,
                declaredChildren: parent?.childCaseIds || [],
                expectedChildren: childIds,
                childrenPresent: children.every(Boolean),
                childSeriesIds: [...new Set(children.map(c => c?.seriesId))],
                childOrders: children.map(c => c?.seriesOrder),
                timelineChildren: timeline.filter(e => e.seriesId === parentId).map(e => e.caseId),
                parentTimelineCount: timeline.filter(e => e.caseId === parentId).length,
            };
        })"""
    )

    metrics = page.evaluate(
        """() => {
            const selected = document.querySelector('.atlas-marker.selected');
            const stateLines = document.querySelectorAll('#stateLines .us-state-line');
            return {
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
                stateLineCount: stateLines.length,
                countryPathCount: document.querySelectorAll('.continents .land').length,
                selectedTransform: selected ? selected.getAttribute('transform') : null,
                selectedId: selected ? selected.dataset.id : null,
                atlasDataCases: typeof atlasData !== 'undefined' ? atlasData.cases.length : null,
                generatedProjection: typeof atlasData !== 'undefined' ? [...new Set(atlasData.cases.map(c => c.projection).filter(Boolean))].slice(0, 5) : [],
            };
        }"""
    )
    browser.close()

report = {
    "url": URL,
    "screenshots": {k: str(v) for k, v in SCREENSHOTS.items()},
    "consoleErrors": console_errors,
    "pageErrors": page_errors,
    "newCaseSources": new_case_sources,
    "geometryChecks": geometry_checks,
    "seriesChecks": series_checks,
    "navySeriesChecks": navy_series_checks,
    "depthSeriesChecks": depth_series_checks,
    "metrics": metrics,
}
(QA / "atlas-browser-qa.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
source_failures = [case_id for case_id, row in new_case_sources.items() if not row["drawerOpen"] or row["links"] < 1 or row["missing"]]
geometry_failures = [case_id for case_id, row in geometry_checks.items() if row["selected"] != case_id or not row["rendered"] or row["pathLength"] < 8 or row["kind"] not in {"reference route", "approximate area"}]
expected_children = set(HIMALAYAN_CASES[1:])
series_failure = (
    not series_checks["parentPresent"]
    or series_checks["parentRole"] != "series-parent"
    or series_checks["parentCounted"] is not False
    or set(series_checks["childIds"]) != expected_children
    or not series_checks["childrenPresent"]
    or set(series_checks["childOrders"]) != set(range(1, 7))
    or series_checks["childSeriesIds"] != ["BF-1968-HIM-01"]
    or set(series_checks["childTimelineIds"]) != expected_children
    or len(series_checks["childTimelineIds"]) != 6
    or series_checks["parentTimelineCount"] != 0
)
expected_navy_children = {"BF-2015-GIMBAL-01", "BF-2015-GOFAST-01"}
navy_series_failure = (
    not navy_series_checks["parentPresent"]
    or navy_series_checks["parentRole"] != "series-parent"
    or navy_series_checks["parentCounted"] is not False
    or set(navy_series_checks["childIds"]) != expected_navy_children
    or not navy_series_checks["childrenPresent"]
    or set(navy_series_checks["childOrders"]) != {1, 2}
    or navy_series_checks["childSeriesIds"] != ["BF-2015-NAV-01"]
    or set(navy_series_checks["childTimelineIds"]) != expected_navy_children
    or len(navy_series_checks["childTimelineIds"]) != 2
    or navy_series_checks["parentTimelineCount"] != 0
)
depth_series_failure = any(
    row["parentRole"] != "series-parent"
    or row["parentCounted"] is not False
    or set(row["declaredChildren"]) != set(row["expectedChildren"])
    or not row["childrenPresent"]
    or row["childSeriesIds"] != [row["parentId"]]
    or set(row["childOrders"]) != set(range(1, len(row["expectedChildren"]) + 1))
    or set(row["timelineChildren"]) != set(row["expectedChildren"])
    or row["parentTimelineCount"] != 0
    for row in depth_series_checks
)
if console_errors or page_errors or metrics.get("horizontalOverflow") or metrics.get("atlasDataCases") != EXPECTED_CASE_COUNT or source_failures or geometry_failures or series_failure or navy_series_failure or depth_series_failure:
    raise SystemExit(1)
