#!/usr/bin/env python3
"""Idempotently deepen Washington 1952, Socorro 1964, and Killeen 1954."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
INDEX = ROOT / "source-file-index.json"
PUBLIC = ROOT / "public-source-manifest.json"


def uniq(values):
    return list(dict.fromkeys(value for value in values if value))


def merge_public(existing, additions):
    by_url = {item.get("url"): item for item in existing if isinstance(item, dict) and item.get("url")}
    for item in additions:
        by_url[item["url"]] = item
    return list(by_url.values())


def main():
    atlas = json.loads(ATLAS.read_text())
    index = json.loads(INDEX.read_text())
    public_manifest = json.loads(PUBLIC.read_text())
    cases = {case["id"]: case for case in atlas["cases"]}

    dc = cases["BF-1952-DC-01"]
    dc_hero = "assets/evidence/DC-FLAP-1952/legacy-page-code-recovery/NARA-PBB90/NARA-PBB90-127_Fold3-12645597_WFM-38572393.jpg"
    dc_ruppelt = "assets/evidence/DC-FLAP-1952/DC-1952-Ruppelt-Staff-Study-NAID-461457646-p34.jpg"
    dc_pbb129 = "assets/evidence/DC-FLAP-1952/legacy-page-code-recovery/NARA-PBB90/NARA-PBB90-129_Fold3-12645610_WFM-38572395.jpg"
    dc.update({
        "summary": "On 19–20 and 26–27 July 1952, Washington National and Andrews AFB personnel reported unidentified radar targets around defended capital airspace, concurrent visual observations, and interceptor responses. The surviving record documents two distinct weekend clusters, fragmented investigative handoffs, and an Air Force public response culminating in the 29 July press conference.",
        "official": "The Air Force publicly emphasized temperature inversion and anomalous propagation. CAA Technical Development Report No. 180 later modeled weather-related false targets, but its public copy concentrates on the first weekend and later August observations rather than fully reproducing the 26–27 July sequence. Controllers and some aircrew disputed a purely weather-based account.",
        "gap": "Raw Washington National and Andrews radar plots, scope photographs or recordings, complete controller logs/audio, interceptor mission records, and any completed Bolling/Headquarters Command follow-up investigation have not been recovered in the public packet. The exact correlation between radar, visual reports, and individual scrambles therefore cannot be independently reconstructed.",
        "date": "19–27 JUL 1952",
        "image": dc_hero,
        "images": uniq([dc_hero, dc_ruppelt, dc_pbb129, "assets/source_previews/BF-1952-DC-01_source_image.png"]),
        "heroVisual": {
            "src": dc_hero,
            "mediaType": "image",
            "visualType": "official-spot-intelligence-report",
            "caption": "Continuation of the 20 July Andrews AFB spot-intelligence report, preserving control-tower entries and Washington Center reports of unidentified radar targets.",
            "provenance": "USAF OSI District 4 file; T1206 roll 90, frame 0127; Fold3 image 12645597",
            "evidenceStatus": "Contemporaneous official event record; documents reported targets and visual observations but is not raw radar data and does not establish object identity.",
            "isEventEvidence": True,
        },
        "keyQuote": "The need for the time and personnel to make field investigations was best exemplified by the Washington D.C. radar sighting.",
        "quoteSource": "Capt. Edward J. Ruppelt, Staff Study—1952, NARA NAID 461457646, corpus p. 34 (internal page 3)",
        "quoteConfidence": "confirmed primary-source quotation; visually verified",
        "sourceQuality": "Multiple official records with exact NARA/Fold3 custody; raw radar and complete operational logs remain absent.",
        "sourceLabel": "NARA RG 341 / USAF OSI / CAA",
        "sourceLocator": "DC-FLAP-1952 · NARA NAIDs 28944268, 28944476, 28944529, 28944560, 28944603, 28944612, 461457646; T1206 roll 90 frames 0127–0129",
        "sources": [
            "DC-FLAP-1952 · 37 recovered T1206 roll 11 pages hosted in six exact NARA file units",
            "USAF OSI District 4 spot-intelligence report · T1206 roll 90, frames 0127–0129",
            "Ruppelt Staff Study—1952 · NARA NAID 461457646, corpus p. 34",
            "CAA Technical Development Report No. 180 · May 1953 public scan",
            "Reports telephoned to OIN on 28 July 1952 · recovered Blue Book pages",
        ],
        "sourceRecords": [
            {
                "citation": "DC-JULY-1952-NARA-S3 · recovered Project Blue Book pages",
                "sourceType": "official-project-blue-book-record-set",
                "provenance": "NARA RG 341 / T1206 roll 11; exact host NAIDs 28944268, 28944476, 28944529, 28944560, 28944603, 28944612",
                "locator": "MAXW-PBB11 frames 0916, 1084–1091, 1149–1151, 1170–1176, 1190–1198, 1208–1211, 1214–1218",
                "supports": ["contemporaneous-sighting-reports", "official-message-routing", "July-1952-investigative-record", "multiple-reporting-locations"],
                "limitations": ["current-NARA-file-unit-titles-mismatch-adjacent-frame-spans", "not-a-continuous-complete-case-file", "raw-radar-data-absent"],
            },
            {
                "citation": "ANDREWS-OSI-SPOT-REPORT · unidentified objects sighted at Andrews AFB, 20 July 1952",
                "sourceType": "contemporaneous-spot-intelligence-report",
                "provenance": "USAF OSI District 4; T1206 roll 90; exact Fold3 roll/frame crosswalk",
                "locator": "NARA-PBB90-127–129; Fold3 images 12645597, 12645604, 12645610",
                "supports": ["Washington-Center-reported-five-targets", "Andrews-control-tower-log", "concurrent-visual-reports", "interoffice-investigative-handoff"],
                "limitations": ["originating-OSI-office-recorded-no-investigation", "raw-radar-plots-absent", "promised-Bolling-follow-up-not-recovered"],
            },
            {
                "citation": "RUPPELT-STAFF-STUDY-1952 · internal Blue Book program review",
                "sourceType": "official-program-staff-study",
                "provenance": "NARA RG 341, Project Blue Book Administrative Files",
                "locator": "NARA NAID 461457646, corpus p. 34 (internal p. 3)",
                "supports": ["Washington-radar-case-cited-as-field-investigation-failure", "ATIC-personnel-shortage", "delayed-investigative-response"],
                "limitations": ["program-review-not-raw-event-record", "page-addresses-investigative-capacity-not-target-identity", "prepared-before-full-second-weekend-analysis"],
            },
            {
                "citation": "CAA Technical Development Report No. 180 · Preliminary Study of Unidentified Targets Observed on Air Traffic Control Radars",
                "sourceType": "official-technical-analysis-public-copy",
                "provenance": "Civil Aeronautics Administration, May 1953; public CUFON archival scan",
                "locator": "DC-1952-CAA-radar-targets-preliminary-study.pdf, 21 pages",
                "supports": ["official-anomalous-propagation-model", "weather-related-false-target-analysis", "radar-environment-context"],
                "limitations": ["public-copy-is-private-archive-derivative", "does-not-fully-reproduce-July-26-27-sequence", "does-not-supply-raw-scope-data"],
            },
            {
                "citation": "OIN-REPORTS-1952-07-28 · reports telephoned to Office of Naval Intelligence",
                "sourceType": "official-report-transcription-and-recovered-pages",
                "provenance": "Blue Book/NARA T1206 pages, with public transcription wrapper",
                "locator": "MAXW-PBB11-1214–1218; DC-1952-Reports-Telephoned-to-OIN-1952-07-28.pdf",
                "supports": ["multiple-27-July-report-locations", "post-event-intelligence-routing", "civilian-and-airport-reporting"],
                "limitations": ["telephoned-reports-not-independent-investigation", "wrapper-is-secondary", "reports-do-not-establish-object-identity"],
            },
        ],
        "phenomena": {
            "shapes": ["lights", "circular-object"],
            "objectCount": None,
            "luminosity": "orange and white lights reported in portions of the record",
            "motion": ["variable-speed-radar-targets", "direction-changes", "targets-reported-near-aircraft"],
            "effects": ["fighter-interceptor-response", "capital-airspace-alert"],
        },
        "observation": {
            "witnessCount": None,
            "witnessRoles": ["Washington National radar controllers", "Andrews AFB control-tower personnel", "military and civilian pilots", "ground observers"],
            "sensors": ["Washington National Airport radar", "Andrews AFB radar", "unaided visual"],
            "durationSeconds": None,
            "independentWitnessGroups": 4,
        },
        "temporal": {
            "dateLabel": "19–27 JUL 1952",
            "year": 1952,
            "startDateTime": "1952-07-19T23:40:00-04:00",
            "endDateTime": "1952-07-28T00:30:00-04:00",
            "timezone": "EDT",
            "durationSeconds": None,
            "precision": "day",
            "eventForm": "event-series",
        },
    })
    dc_public = [
        {
            "access": "Public",
            "label": "NARA Catalog — Ruppelt Staff Study, 1952",
            "publisher": "National Archives and Records Administration",
            "scope": "official-program-review-exact-record",
            "url": "https://catalog.archives.gov/id/461457646",
            "note": "Exact 51-object staff study; corpus p. 34 documents ATIC's inability to investigate the Washington radar sighting immediately.",
        },
        {
            "access": "Subscription",
            "label": "Fold3 — Andrews AFB spot-intelligence report, T1206 roll 90 frame 0127",
            "publisher": "Fold3",
            "scope": "exact-microfilm-frame",
            "url": "https://www.fold3.com/image/12645597/",
            "note": "Exact full-resolution microfilm frame; Atlas preserves a local scan. Subscription may be required.",
        },
    ]
    dc["publicSources"] = merge_public(dc.get("publicSources", []), dc_public)

    soc = cases["BF-1964-SC-01"]
    soc_hero = "assets/evidence/SOCORRO-1964/SOCORRO-1964-landing-site-photo-markers.png"
    soc_p9 = "assets/evidence/SOCORRO-1964/SOCORRO-1964-FBI-p09-FBI-airtel-witness-and-traces.jpg"
    soc_p15 = "assets/evidence/SOCORRO-1964/SOCORRO-1964-FBI-p15-FBI-field-trace-description.jpg"
    soc_p30 = "assets/evidence/SOCORRO-1964/SOCORRO-1964-FBI-p30-FBI-Air-Force-no-explanation.jpg"
    soc.update({
        "summary": "On 24 April 1964, Socorro police officer Lonnie Zamora reported a landed oval object, two small figures, a roar and flame, and a rapid departure south of Socorro. Same-day responders documented four regular ground depressions, burned grass patches, and smaller circular marks. The FBI record shows military investigators could not explain Zamora's observations; Project Blue Book ultimately carried the case as unidentified.",
        "official": "Project Blue Book classified Socorro as unidentified. FBI liaison records quote Kirtland AFB personnel as unable to explain Zamora's observations and impressed by his sincerity. Those records confirm the report, response, and trace documentation; they do not establish what caused the marks or identify the reported object.",
        "gap": "The public packet does not provide a modern reproducible soil/vegetation analysis, a complete trace-sample custody ledger, or independent photographic evidence of the object. Zamora was the only known direct witness to the object and figures, and the insignia-sketch chain diverges across later retellings.",
        "image": soc_hero,
        "images": uniq([soc_hero, soc_p9, soc_p15, soc_p30, "assets/source_previews/BF-1964-SC-01_source_image.jpg"]),
        "sourceQuality": "Exact NARA Blue Book custody plus FBI liaison and field memoranda; physical traces were documented but causal identity remains unresolved.",
        "sourceLabel": "NARA Project Blue Book / FBI",
        "sourceLocator": "SOCORRO-1964 · NARA NAID 302532129; FBI file pp. 9, 14–15, 30–31",
        "sources": [
            "SOCORRO-1964 · Project Blue Book site-photograph packet · NARA NAID 302532129",
            "FBI Albuquerque airtel, 28 April 1964 · FBI file p. 9",
            "FBI field memorandum, 8 May 1964 · FBI file pp. 14–15",
            "FBI liaison record of Kirtland AFB assessment · FBI file pp. 30–31",
        ],
        "sourceRecords": [
            {
                "citation": "SOCORRO-BLUE-BOOK · Socorro Project BLUE BOOK file and site photographs",
                "sourceType": "official-project-blue-book-case-file",
                "provenance": "NARA RG 341, exact file unit NAID 302532129",
                "locator": "25-page site-photograph packet",
                "supports": ["same-day-official-investigation", "landing-site-photographs", "reported-ground-traces", "Blue-Book-unidentified-status"],
                "limitations": ["photographs-do-not-show-object", "trace-causation-not-established", "complete-laboratory-custody-not-recovered"],
            },
            {
                "citation": "FBI-AIRTEL-1964-04-28 · witness and initial trace summary",
                "sourceType": "contemporaneous-federal-liaison-record",
                "provenance": "Federal Bureau of Investigation, Albuquerque field office",
                "locator": "SOCORRO-1964-FBI-file-31p.pdf, p. 9",
                "supports": ["Zamora-described-as-sober-dependable-mature", "oval-object-report", "roar-and-flame", "four-depressed-areas", "four-smouldering-areas"],
                "limitations": ["FBI-policy-was-liaison-not-investigation", "summary-relies-on-Zamora-report", "does-not-identify-object"],
            },
            {
                "citation": "FBI-FIELD-MEMORANDUM-1964-05-08 · site observations",
                "sourceType": "contemporaneous-federal-field-observation",
                "provenance": "Federal Bureau of Investigation, Special Agent D. Arthur Byrnes Jr.",
                "locator": "SOCORRO-1964-FBI-file-31p.pdf, pp. 14–15",
                "supports": ["four-regular-depressions-measured", "three-burned-grass-patches-inside-depressions", "one-burned-area-outside", "three-smaller-circular-marks"],
                "limitations": ["observations-document-condition-not-cause", "no-object-photograph", "no-modern-forensic-analysis"],
            },
            {
                "citation": "FBI-KIRTLAND-LIAISON-1964-04-28 · Air Force assessment",
                "sourceType": "contemporaneous-federal-liaison-record",
                "provenance": "FBI record of Kirtland AFB investigator statements",
                "locator": "SOCORRO-1964-FBI-file-31p.pdf, pp. 30–31",
                "supports": ["Air-Force-could-not-explain-observations", "investigators-impressed-by-Zamora-sincerity", "first-responders-found-burning-areas-and-indentations"],
                "limitations": ["FBI-records-secondhand-Air-Force-statements", "not-final-Blue-Book-disposition-card", "explanation-absence-is-not-origin-proof"],
            },
        ],
        "phenomena": {
            "shapes": ["oval", "egg-shaped"],
            "objectCount": 1,
            "luminosity": "whitish object; bluish-orange flame during departure",
            "motion": ["landed-or-grounded", "slow-vertical-rise", "rapid-departure-over-mountain"],
            "effects": ["roaring-sound", "flame", "ground-depressions", "burned-grass"],
        },
        "observation": {
            "witnessCount": 1,
            "witnessRoles": ["Lonnie Zamora, Socorro police officer", "law-enforcement and military trace-scene responders"],
            "sensors": ["unaided visual", "site photography", "physical-trace inspection"],
            "durationSeconds": None,
            "independentWitnessGroups": 1,
        },
    })

    kl = cases["BF-1954-KL-01"]
    kl_p151 = "assets/evidence/KILLEEN-1954/KILLEEN-1954-NARA-NAID-310994070-p151-balloon-analysis.jpg"
    kl_p152 = "assets/evidence/KILLEEN-1954/KILLEEN-1954-NARA-NAID-310994070-p152-investigator-conclusion.jpg"
    kl.update({
        "date": "20–24 NOV 1954",
        "summary": "At least 16 members of the 8455th DU Military Police Company at Gray AFB's Danger Area 343 reported a silver-glowing oval object during 20–24 November 1954. The primary 24 November observation lasted about 2.5 minutes: the object climbed on a steep 50–60° path and departed southwest at very high apparent speed without a trail or exhaust. Captain Clarence Magee's 4602D AISS investigation endorsed the witnesses' reliability and tested, then rejected, a weather-balloon explanation.",
        "official": "The surviving 155-object 4602D AISS field file does not contain the later ATIC/Blue Book disposition. Within the field report, Captain Magee concluded the military-police witnesses were reliable, that they were observing something foreign to them, and that the reports were not stimulated imagination. A weather balloon was shown to a witness and rejected as a color match; Magee also found 0–3 knot winds inconsistent with the reported rate of disappearance.",
        "gap": "The final ATIC record card or closure memorandum has not been recovered, so the formal Blue Book disposition remains unknown. No radar track, photograph, physical sample, or instrumented speed measurement appears in the field file; performance estimates remain visual judgments under poor weather conditions.",
        "image": kl_p152,
        "images": uniq([kl_p152, kl_p151, *kl.get("images", [])]),
        "heroVisual": {
            "src": kl_p152,
            "mediaType": "image",
            "visualType": "official-investigator-conclusion",
            "caption": "Captain Clarence Magee's 4602D AISS assessment endorsing the military-police witnesses' reliability and rejecting stimulated imagination.",
            "provenance": "NARA RG 341, 4602D AISS field file, NAID 310994070, corpus p. 152",
            "evidenceStatus": "Primary-source investigator assessment; confirms the official evaluation of the witnesses, not the object's identity.",
            "isEventEvidence": True,
        },
        "keyFact": "Sixteen military-police witnesses were questioned in a 155-page field investigation; the investigator endorsed their reliability and rejected the tested balloon hypothesis.",
        "heroFact": "A 155-page AISS investigation backed 16 military-police witnesses and rejected a weather balloon in 0–3 knot winds.",
        "keyQuote": "By virtue of their position, the reliability of the sighters must be beyond question. It is therefore believed that they are sighting an object which is foreign to them, and these sightings are not the result of stimulated imagination.",
        "quoteSource": "Capt. Clarence A. Magee, 4602D AISS Air Intelligence Information Report, NARA NAID 310994070, corpus p. 152",
        "quoteConfidence": "confirmed primary-source quotation; OCR and scan visually verified",
        "sourceQuality": "Complete exact NARA 4602D AISS field packet (155 digital objects); final ATIC/Blue Book disposition absent.",
        "sourceLocator": "NARA NAID 310994070, 155 digital objects; decisive analysis at corpus pp. 151–152",
        "sources": [
            "KILLEEN-1954-NARA-310994070 · complete 4602D AISS field file, 155 digital objects",
            "ATIC Form 164 witness questionnaires · corpus pp. 3–148",
            "Air Intelligence Information Report · corpus pp. 149–155",
        ],
        "sourceRecords": [
            {
                "citation": "KILLEEN-1954-NARA-310994070 · complete 4602D AISS field file",
                "sourceType": "official-field-investigation-packet",
                "provenance": "NARA RG 341, Case Files of 4602D AISS on UFO Sightings, NAID 310994070",
                "locator": "155 digital objects; 20–24 November 1954",
                "supports": ["sixteen-military-personnel-named", "individual-questionnaires", "field-investigation", "Espionage-Act-marking", "multi-day-reporting"],
                "limitations": ["final-ATIC-disposition-absent", "no-radar-or-photography", "official-custody-does-not-identify-object"],
            },
            {
                "citation": "KILLEEN-WITNESS-QUESTIONNAIRES · ATIC Form 164 set",
                "sourceType": "firsthand-military-witness-questionnaires",
                "provenance": "8455th DU Military Police Company submissions to 4602D AISS",
                "locator": "NARA NAID 310994070, corpus pp. 3–148",
                "supports": ["multiple-named-witnesses", "oval-silver-glow-description", "steep-ascent", "rapid-southwest-departure", "approximately-two-and-one-half-minute-duration"],
                "limitations": ["same-unit-witness-cluster", "visual-estimates-not-instrumented", "low-cloud-and-half-mile-visibility"],
            },
            {
                "citation": "MAGEE-BALLOON-ANALYSIS · 4602D AISS field report",
                "sourceType": "official-investigator-analysis",
                "provenance": "Capt. Clarence A. Magee, 4602D AISS",
                "locator": "NARA NAID 310994070, corpus p. 151",
                "supports": ["weather-balloon-shown-to-witness", "color-match-rejected", "wash-tub-to-speck-in-one-minute", "zero-to-three-knot-winds-inconsistent-with-reported-velocity"],
                "limitations": ["single-witness-balloon-comparison", "no-measured-object-range", "wind-analysis-does-not-identify-object"],
            },
            {
                "citation": "MAGEE-RELIABILITY-ASSESSMENT · 4602D AISS field report",
                "sourceType": "official-investigator-conclusion",
                "provenance": "Capt. Clarence A. Magee, 4602D AISS",
                "locator": "NARA NAID 310994070, corpus p. 152",
                "supports": ["witness-reliability-endorsed", "object-foreign-to-witnesses", "stimulated-imagination-rejected"],
                "limitations": ["investigator-assessment-not-object-identification", "final-Blue-Book-disposition-not-in-packet"],
            },
        ],
        "phenomena": {
            "shapes": ["oval"],
            "objectCount": 1,
            "luminosity": "silver glow",
            "motion": ["steep-50-to-60-degree-ascent", "rapid-straight-trajectory", "southwest-horizontal-departure"],
            "effects": ["no-trail", "no-exhaust", "no-reported-sound"],
        },
        "observation": {
            "witnessCount": 16,
            "witnessRoles": ["8455th DU Military Police Company personnel", "commissioned and enlisted military witnesses"],
            "sensors": ["unaided visual"],
            "durationSeconds": 150,
            "independentWitnessGroups": 1,
        },
        "temporal": {
            "dateLabel": "20–24 NOV 1954",
            "year": 1954,
            "startDateTime": "1954-11-20",
            "endDateTime": "1954-11-24",
            "timezone": None,
            "durationSeconds": 150,
            "durationRangeSeconds": None,
            "precision": "day",
            "eventForm": "event-series",
        },
    })

    index["DC-FLAP-1952"] = uniq(index.get("DC-FLAP-1952", []) + [dc_hero, dc_ruppelt, dc_pbb129, "https://catalog.archives.gov/id/461457646", "https://www.fold3.com/image/12645597/"])
    index["SOCORRO-1964"] = uniq(index.get("SOCORRO-1964", []) + [soc_p9, soc_p15, soc_p30, "https://catalog.archives.gov/id/302532129"])
    index["KILLEEN-1954"] = uniq(index.get("KILLEEN-1954", []) + [kl_p151, kl_p152, "https://catalog.archives.gov/id/310994070"])

    for case in (dc, soc, kl):
        public_manifest[case["id"]] = case["publicSources"]

    ATLAS.write_text(json.dumps(atlas, indent=2, ensure_ascii=False) + "\n")
    INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    PUBLIC.write_text(json.dumps(public_manifest, indent=2, ensure_ascii=False) + "\n")
    print("Enriched BF-1952-DC-01, BF-1964-SC-01, and BF-1954-KL-01")


if __name__ == "__main__":
    main()
