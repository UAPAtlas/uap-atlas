#!/usr/bin/env python3
"""Browser QA for every implemented Cultural Legacy dossier on desktop and mobile."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--html", default=str(ROOT / "atlas-responsive.html"))
parser.add_argument("--url")
parser.add_argument("--out", default="/tmp/uap-cultural-legacy-tranche-qa")
args = parser.parse_args()
HTML = Path(args.html).resolve()
BASE_URL = args.url or HTML.as_uri()
OUT = Path(args.out).resolve()
CASES = [
    "BF-1944-FF-01",
    "BF-1947-KA-01",
    "BF-1947-RW-01",
    "BF-1961-BH-01",
    "BF-1965-KB-01",
    "BF-1951-YK-01",
    "BF-1973-PG-01",
    "BF-1975-TW-01",
    "BF-SF-13",
    "BF-1980-RF-01",
    "BF-1994-AR-01",
    "BF-1996-VG-01",
    "BF-1997-PH-01",
]
VIEWPORTS = [
    ("desktop", 1440, 1000, False),
    ("mobile", 390, 844, True),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        launch = {"headless": True}
        chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if chrome.exists():
            launch["executable_path"] = str(chrome)
        browser = p.chromium.launch(**launch)
        passed = 0
        try:
            for viewport, width, height, mobile in VIEWPORTS:
                page = browser.new_page(
                    viewport={"width": width, "height": height},
                    is_mobile=mobile,
                    has_touch=mobile,
                )
                page_errors: list[str] = []
                console_errors: list[str] = []
                failed_requests: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.on(
                    "requestfailed",
                    lambda request: failed_requests.append(
                        f"{request.url} :: {request.failure or 'unknown failure'}"
                    )
                    if "net::ERR_ABORTED" not in str(request.failure or "")
                    else None,
                )
                page.on(
                    "console",
                    lambda message: console_errors.append(message.text)
                    if message.type == "error"
                    else None,
                )
                for case_id in CASES:
                    page_errors.clear()
                    console_errors.clear()
                    failed_requests.clear()
                    url = BASE_URL + f"#case={case_id}&page=dossier"
                    page.goto(url, wait_until="load")
                    page.wait_for_timeout(500)
                    assert page.evaluate("() => atlasData.cases.length") == 155
                    assert page.locator(".case-drawer").is_visible(), (viewport, case_id, "drawer")
                    card = page.locator(".cultural-legacy")
                    assert card.count() == 1 and card.is_visible(), (viewport, case_id, "card")
                    card.scroll_into_view_if_needed()
                    page.wait_for_timeout(250)
                    text = card.inner_text().upper()
                    assert "CULTURAL LEGACY" in text
                    assert "CONTEXT · NOT EVIDENCE" in text
                    image = card.locator("img")
                    image.wait_for(state="visible")
                    page.wait_for_function(
                        "image => image.complete",
                        arg=image.element_handle(),
                        timeout=15_000,
                    )
                    dimensions = image.evaluate(
                        "i => ({complete:i.complete,w:i.naturalWidth,h:i.naturalHeight})"
                    )
                    assert dimensions["complete"] and dimensions["w"] > 250 and dimensions["h"] > 200, (
                        viewport,
                        case_id,
                        dimensions,
                    )
                    links = card.locator(".cultural-meta a")
                    assert links.count() in (1, 2), (viewport, case_id, "source/license links", links.count())
                    for index in range(links.count()):
                        assert links.nth(index).get_attribute("href").startswith("https://")
                    meta_text = card.locator(".cultural-meta").inner_text().upper()
                    assert links.count() == 2 or "SOURCE CREDITED" in meta_text, (
                        viewport,
                        case_id,
                        "rights metadata",
                        meta_text,
                    )
                    assert card.locator(".cultural-image").get_attribute("href").startswith("https://")
                    assert page.evaluate(
                        "el => el.scrollWidth <= el.clientWidth + 1", card.element_handle()
                    ), (viewport, case_id, "card overflow")
                    carousel = page.locator("[data-carousel]")
                    if carousel.count():
                        payload = carousel.first.get_attribute("data-carousel") or ""
                        assert "assets/context/" not in payload, (viewport, case_id, "context leaked")
                    card.screenshot(path=str(OUT / f"{viewport}-{case_id}.png"))
                    assert not page_errors, (viewport, case_id, "page errors", page_errors)
                    assert not failed_requests, (viewport, case_id, "failed requests", failed_requests)
                    assert not console_errors, (
                        viewport,
                        case_id,
                        "console errors",
                        console_errors,
                        "failed requests",
                        failed_requests,
                    )
                    passed += 1
                page.close()
        finally:
            browser.close()
    print(f"Cultural Legacy browser QA PASS: {passed} states / {len(CASES)} cases / {len(VIEWPORTS)} viewports")
    print(OUT)


if __name__ == "__main__":
    main()
