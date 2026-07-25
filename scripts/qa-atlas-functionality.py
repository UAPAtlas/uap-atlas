#!/usr/bin/env python3
"""Focused end-to-end functionality and responsive visual audit for the Atlas desktop app."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--html", default=str(ROOT / "atlas-fresh.html"))
parser.add_argument("--out", default=str(ROOT / "qa" / "atlas-functionality"))
args = parser.parse_args()
html = Path(args.html).resolve()
out = Path(args.out).resolve()
out.mkdir(parents=True, exist_ok=True)
url = html.as_uri() + f"?qa={int(time.time())}"

results: dict[str, object] = {"html": str(html), "url": url, "screenshots": {}, "checks": {}}
console_errors: list[str] = []
page_errors: list[str] = []


def visible_metrics(page):
    return page.evaluate("""() => ({
      width: innerWidth,
      height: innerHeight,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      scrollHeight: document.documentElement.scrollHeight,
      clientHeight: document.documentElement.clientHeight,
      desktopBlocked: getComputedStyle(document.body,'::before').content.includes('desktop workspace'),
      cases: atlasData.cases.length,
      mainRows: document.querySelectorAll('.case-row').length,
      drawerOpen: document.getElementById('drawerBackdrop').classList.contains('open'),
    })""")


def screenshot(page, name):
    target = out / f"{name}.png"
    page.screenshot(path=str(target), full_page=True)
    results["screenshots"][name] = str(target)


with sync_playwright() as p:
    launch = {"headless": True}
    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if chrome.exists():
        launch["executable_path"] = str(chrome)
    browser = p.chromium.launch(**launch)

    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.goto(url, wait_until="load")
    page.wait_for_timeout(800)

    initial = visible_metrics(page)
    assert initial["cases"] == 146, initial
    assert initial["mainRows"] == 120, initial
    assert initial["scrollWidth"] == initial["clientWidth"] and not initial["desktopBlocked"], initial
    assert not initial["drawerOpen"], initial
    screenshot(page, "desktop-wide-initial")

    # Search + Case Stack selection must focus/zoom map without opening dossier.
    page.locator("#caseSearch").fill("Roswell")
    page.wait_for_timeout(250)
    assert page.locator(".case-row").count() == 1
    selected_id = page.locator(".case-row").first.get_attribute("data-id")
    page.locator(".case-row").first.click()
    page.wait_for_timeout(750)
    stack_focus = page.evaluate("""id => ({
      selected: state.selectedCaseId,
      zoom: state.zoom,
      view: svg.getAttribute('viewBox'),
      drawer: document.getElementById('drawerBackdrop').classList.contains('open'),
      activeRow: document.querySelector('.case-row.active')?.dataset.id,
      selectedMarker: document.querySelector('.atlas-marker.selected')?.dataset.id,
      cta: Boolean(document.querySelector('.detail [data-open-case]')),
      title: document.querySelector('.detail .case-title')?.textContent,
      expected: cases.find(c=>c.id===id)?.title,
    })""", selected_id)
    assert stack_focus["selected"] == selected_id and stack_focus["activeRow"] == selected_id, stack_focus
    assert stack_focus["zoom"] > 1 and stack_focus["view"] != "0 0 100 62", stack_focus
    assert not stack_focus["drawer"] and stack_focus["cta"], stack_focus
    assert stack_focus["title"] == stack_focus["expected"], stack_focus
    screenshot(page, "desktop-case-stack-map-focus")

    # Explicit dossier action, all tabs, Evidence Lens, sources, and close behavior.
    page.locator(".detail .cta").click()
    page.wait_for_timeout(450)
    dossier = page.evaluate("""() => ({
      open: document.getElementById('drawerBackdrop').classList.contains('open'),
      tabs: [...document.querySelectorAll('#caseDrawer .drawer-tab')].map(x=>x.textContent.trim()),
      lens: document.querySelectorAll('#caseDrawer .evidence-lens').length,
      carousel: document.querySelectorAll('#caseDrawer .drawer-evidence').length,
      title: document.querySelector('#caseDrawer .case-title')?.textContent,
    })""")
    assert dossier["open"] and dossier["tabs"] == ["BRIEF", "TIMELINE", "OFFICIAL POSITION", "RECORD GAPS", "FILES / SOURCES"], dossier
    assert dossier["lens"] == 1 and dossier["carousel"] == 1, dossier
    screenshot(page, "desktop-dossier-brief")
    for tab in ["timeline", "official", "gaps", "sources"]:
        page.locator(f'#caseDrawer [data-tab="{tab}"]').click()
        assert page.locator(f'#caseDrawer [data-panel="{tab}"].active').count() == 1
    source_panel = page.locator('#caseDrawer [data-panel="sources"]')
    source_counts = page.evaluate("""() => {
      const p=document.querySelector('#caseDrawer [data-panel="sources"]');
      return {links:p?.querySelectorAll('a[href]').length||0, disclosures:p?.querySelectorAll('.file-missing,.file-unavailable,.source-disclosure').length||0, text:(p?.innerText||'').length};
    }""")
    assert source_counts["text"] > 40 and source_counts["links"] >= 1, source_counts
    screenshot(page, "desktop-dossier-sources")
    page.locator("#caseDrawer .drawer-close").click()
    page.wait_for_timeout(200)
    assert not page.locator("#drawerBackdrop").evaluate("e=>e.classList.contains('open')")

    # Map marker selection also focuses without opening the dossier.
    page.locator("#caseSearch").fill("")
    page.wait_for_timeout(200)
    page.locator("[data-zoom='reset']").click()
    page.wait_for_timeout(650)
    marker_id = page.locator(".atlas-marker:not(.orbital-aggregate)").first.get_attribute("data-id")
    page.locator(f'.atlas-marker[data-id="{marker_id}"]').first.dispatch_event("click")
    page.wait_for_timeout(700)
    marker_focus = page.evaluate("""id=>({selected:state.selectedCaseId,zoom:state.zoom,drawer:document.getElementById('drawerBackdrop').classList.contains('open')})""", marker_id)
    assert marker_focus["selected"] == marker_id and marker_focus["zoom"] > 1 and not marker_focus["drawer"], marker_focus

    # Timeline nodes focus the map; filters and institutional toggle update state.
    page.locator(".signal-node").first.dispatch_event("click")
    page.wait_for_timeout(650)
    timeline_focus = page.evaluate("""()=>({selected:state.selectedCaseId,event:state.selectedEventId,zoom:state.zoom,drawer:document.getElementById('drawerBackdrop').classList.contains('open')})""")
    assert timeline_focus["selected"] and timeline_focus["event"] and timeline_focus["zoom"] > 1 and not timeline_focus["drawer"], timeline_focus
    agency_value = page.locator("#agencyFilter option").nth(1).get_attribute("value")
    page.locator("#agencyFilter").select_option(agency_value)
    page.wait_for_timeout(200)
    filtered = page.locator(".case-row").count()
    assert 0 < filtered < 120, (agency_value, filtered)
    page.locator("#toggleInstitutional").click()
    assert page.evaluate("state.institutional") is False
    page.locator("#toggleInstitutional").click()
    assert page.evaluate("state.institutional") is True
    page.evaluate("resetAtlasHome()")
    page.wait_for_timeout(650)

    # Orbital aggregate remains a separate 26-record evidence layer.
    page.locator(".orbital-aggregate").dispatch_event("click")
    page.wait_for_timeout(350)
    orbital = page.evaluate("""()=>({mode:state.stackMode,rows:document.querySelectorAll('.case-row').length,title:document.getElementById('stackTitle').textContent})""")
    assert orbital == {"mode": "orbital", "rows": 26, "title": "Orbital / Lunar Evidence"}, orbital
    page.locator("#stackReturn").click()
    page.wait_for_timeout(250)
    assert page.evaluate("state.stackMode") == "main"
    assert page.locator(".case-row").count() == 120

    # Zoom controls plus keyboard separation: row Enter focuses; global Enter explicitly opens.
    page.locator("[data-zoom='reset']").click()
    page.wait_for_timeout(650)
    assert abs(page.evaluate("state.zoom") - 1) < 0.01
    page.locator("[data-zoom='in']").click()
    page.wait_for_timeout(650)
    assert page.evaluate("state.zoom") > 1
    page.evaluate("resetAtlasHome()")
    keyboard_id = page.locator(".case-row").first.get_attribute("data-id")
    page.locator(".case-row").first.focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(650)
    keyboard_focus = page.evaluate("""id=>({selected:state.selectedCaseId,zoom:state.zoom,drawer:document.getElementById('drawerBackdrop').classList.contains('open')})""", keyboard_id)
    assert keyboard_focus["selected"] == keyboard_id and keyboard_focus["zoom"] > 1 and not keyboard_focus["drawer"], keyboard_focus

    # Deep-link hash opens the requested dossier and close clears case state.
    deep = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    deep_errors: list[str] = []
    deep.on("pageerror", lambda exc: deep_errors.append(str(exc)))
    deep.goto(url + "#case=BF-1947-RW-01", wait_until="load")
    deep.wait_for_timeout(650)
    deep_state = deep.evaluate("""()=>({selected:state.selectedCaseId,open:document.getElementById('drawerBackdrop').classList.contains('open'),hash:location.hash})""")
    assert deep_state["selected"] == "BF-1947-RW-01" and deep_state["open"] and "case=BF-1947-RW-01" in deep_state["hash"], deep_state
    deep.locator("#caseDrawer .drawer-close").click()
    assert "case=" not in deep.evaluate("location.hash")
    assert not deep_errors, deep_errors
    deep.close()

    # Representative visual breakpoints; desktop is intentionally supported above 1080px.
    visual_metrics = {}
    for width, height, name in [(1280, 800, "desktop-laptop"), (1180, 820, "desktop-compact")]:
        vp = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors: list[str] = []
        vp.on("pageerror", lambda exc, errors=errors: errors.append(str(exc)))
        vp.goto(url, wait_until="load")
        vp.wait_for_timeout(550)
        metric = visible_metrics(vp)
        assert metric["scrollWidth"] == metric["clientWidth"] and not metric["desktopBlocked"] and not errors, (metric, errors)
        screenshot(vp, name)
        visual_metrics[name] = metric
        vp.close()

    results["checks"] = {
        "initial": initial,
        "caseStackFocus": stack_focus,
        "dossier": dossier,
        "sources": source_counts,
        "markerFocus": marker_focus,
        "timelineFocus": timeline_focus,
        "orbital": orbital,
        "deepLink": deep_state,
        "visualMetrics": visual_metrics,
    }
    browser.close()

results["consoleErrors"] = console_errors
results["pageErrors"] = page_errors
assert not console_errors and not page_errors, (console_errors, page_errors)
(out / "audit.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({"status": "PASS", "screenshots": len(results["screenshots"]), "audit": str(out / "audit.json"), "checks": results["checks"]}, indent=2))
