#!/usr/bin/env python3
"""Apply the bounded 2026-08-05 provenance corrections to exactly three cases."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "atlas-data.json"
PUBLIC_MANIFEST = ROOT / "public-source-manifest.json"
AUTHORIZED_CASE_IDS = {"BF-1997-PH-01", "BF-1978-VL-01", "BF-1973-PG-01"}
AUTHORIZED_TIMELINE_IDS = {"EV-1997-PH-01", "TL-1978A", "TL-1973B"}


def record(citation, source_type, provenance, locator, supports, limitations, **extra):
    value = {
        "citation": citation,
        "sourceType": source_type,
        "provenance": provenance,
        "locator": locator,
        "supports": supports,
        "limitations": limitations,
    }
    value.update(extra)
    return value


atlas = json.loads(DATA.read_text())
cases = {case["id"]: case for case in atlas["cases"]}
timeline = {event["id"]: event for event in atlas["timeline"]}
assert AUTHORIZED_CASE_IDS <= cases.keys()
assert AUTHORIZED_TIMELINE_IDS <= timeline.keys()

pascagoula = cases["BF-1973-PG-01"]
pascagoula.update({
    "quoteSource": "Publicly circulated sheriff-room recording/transcription trail attributed to Charles Hickson, October 11, 1973",
    "quoteConfidence": "Low-to-medium — wording is publicly circulated, but original audio custody and a complete authenticated transcript are not mapped.",
    "sourceQuality": "Witness report to local authorities plus a public trail concerning a reported covert sheriff-room recording; no authenticated complete sheriff packet, original audio, or complete transcript is mapped.",
    "summary": "Charles Hickson and Calvin Parker reported to local authorities that they had been taken aboard an object while fishing on the Pascagoula River. Public local-history sources preserve a trail concerning a reported covert recording made while they were left alone, but the Atlas does not hold the original audio, a complete authenticated transcript, or the sheriff case packet. The report is historically documented; the object and abduction claims remain testimonial.",
    "keyFact": "The public trail describes deputies covertly recording Hickson and Parker while they were alone; that unusual behavioral context documents the report but does not authenticate an abduction or identify an object.",
    "official": "Local authorities received the report and reportedly recorded the witnesses. The mapped public trail is not a complete law-enforcement file, and no official record in Atlas custody establishes the alleged object, entities, or abduction.",
    "gap": "No authenticated complete sheriff case packet, original/coherent audio custody chain, complete transcript with issuer/date/timecode, physical evidence chain, or independent sensor record is mapped.",
    "whyItMatters": "Pascagoula adds an unusual reported behavioral-context layer to a two-witness claim while remaining testimony rather than objective event proof.",
    "sourceLabel": "Public sheriff-room recording trail; original custody not mapped",
    "heroFact": "A public trail describes a reported covert sheriff-room recording of the two witnesses alone; original audio custody and a complete transcript remain unmapped.",
    "acquisitionTargets": [
        "Authenticated complete Jackson County sheriff case packet",
        "Original sheriff-room audio with custody history and complete timecoded transcript",
        "Contemporaneous interview logs and earliest authority report",
    ],
})
pascagoula["confidenceModel"]["provenance"] = "public-local-history-and-recording-trail"
pascagoula["observation"]["witnessRoles"] = ["civilian fishermen"]
pascagoula["sourceRecords"] = [
    record(
        "PASCAGOULA-1973 · public authority-report and sheriff-room recording trail",
        "witness-report-and-public-local-history-trail",
        "Hickson/Parker report to local authorities and Hinds Community College public recording page",
        "PASCAGOULA-1973",
        [
            "Documents that Hickson and Parker's account entered a local-authority and public-history trail",
            "Documents a public trail concerning a reported covert sheriff-room recording",
            "Supports the historical existence of the report, not the alleged event's reality",
        ],
        [
            "No authenticated complete sheriff case packet is mapped",
            "Original audio custody and a complete timecoded transcript are not mapped",
            "The recording trail does not prove abduction, object identity, entities, or non-human origin",
            "Later interviews and retellings must be separated from the earliest authority report",
        ],
        sourceUrl="https://libguides.hindscc.edu/paranormalms/pascagoula_abduction/1973_recording",
    ),
    record(
        "Atlas evidence-depth audit · 2026-07-18",
        "evidence-audit",
        "Local Atlas audit derived from the current source inventory",
        "source-files/evidence-depth/PASCAGOULA-1973-evidence-depth.md",
        ["current source inventory", "explicit primary-record gaps", "provenance boundary"],
        ["not an independent source", "does not corroborate the event narrative", "cannot substitute for missing primary records"],
    ),
]
pascagoula["heroVisual"]["provenance"] = "Later publicity context; not a sheriff record"
pascagoula["heroVisual"]["evidenceStatus"] = "Later witness/publicity context; not event imagery, a sheriff record, or an authenticated depiction of the alleged beings."
timeline["TL-1973B"]["desc"] = "A report to local authorities enters the public record; a public trail describes a reported covert recording, but original audio custody and the alleged event remain unverified."

valentich = cases["BF-1978-VL-01"]
valentich.update({
    "quoteSource": "Public mirror of a final-communications transcript attributed to the Australian Department of Transport, October 21, 1978",
    "quoteConfidence": "High for wording in the inspected public transcript mirror; direct official transcript/audio custody and the complete investigation packet are not locally held.",
    "sourceQuality": "Exact NAA catalog and ATSB report locators plus an inspected public transcript mirror; the complete primary packet is not locally held, and the record does not establish UFO causation.",
    "summary": "Pilot Frederick Valentich disappeared over Bass Strait after radioing Melbourne Flight Service that an unidentified object was near his aircraft and that his engine was running roughly. An inspected public transcript mirror preserves those reported communications; exact NAA and ATSB official locators identify the disappearance/investigation trail. Neither the transcript nor the locators establish what caused the disappearance or that the reported object caused it.",
    "keyFact": "A public copy of the final-communications transcript records Valentich reporting an unidentified object before contact was lost; it documents his report, not the object's identity or the cause of the disappearance.",
    "official": "NAA and ATSB publish exact locators for the official disappearance/investigation record. The complete packet and direct official transcript/audio custody are not mapped locally, so causal conclusions are not upgraded here.",
    "gap": "The complete NAA/Department of Transport investigation packet, direct official transcript/audio custody, full search documentation, and any complete radar/sensor chain remain unmapped; the public transcript mirror alone cannot establish causation.",
    "whyItMatters": "Valentich is an aviation disappearance with contemporaneous reported communications, but the evidentiary boundary is strict: disappearance and transcript trail are documented; UFO causation is not.",
    "sourceLabel": "Official locators / public transcript mirror",
    "heroFact": "A public transcript copy records Valentich's reported unidentified object before contact was lost; it does not establish the disappearance's cause.",
    "acquisitionTargets": [
        "Complete NAA/Department of Transport investigation packet B1497 V116/783/1047",
        "Direct official final-communications transcript and original audio custody record",
        "Complete official search documentation and radar/sensor records",
    ],
})
valentich["confidenceModel"]["provenance"] = "official-locators-and-public-transcript-mirror"
valentich["observation"]["witnessRoles"] = ["pilot"]
valentich["sourceRecords"] = [
    record(
        "National Archives of Australia · B1497 V116/783/1047",
        "catalog-locator-only",
        "National Archives of Australia RecordSearch",
        "Barcode 10491375; item B1497 V116/783/1047",
        ["Identifies the exact official archival file for the disappearance/investigation trail"],
        ["Catalog locator only in current Atlas custody", "File contents were not recovered or inspected in this tranche", "Does not establish UFO causation"],
        sourceUrl="https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/DetailsReports/ItemDetail.aspx?Barcode=10491375&isAv=N",
    ),
    record(
        "ATSB · Aircraft Accident Investigation Summary Report 197802563",
        "report-locator-only",
        "Australian Transport Safety Bureau",
        "Investigation report 197802563",
        ["Identifies the official accident-investigation summary endpoint for the disappearance"],
        ["Endpoint payload was unavailable to direct inspection in this tranche", "Locator alone does not verify specific conclusions or UFO causation"],
        sourceUrl="https://www.atsb.gov.au/sites/default/files/investigation-reports/197802563.pdf",
    ),
    record(
        "Valentich final communications · inspected UFOr public copy",
        "public-transcript-mirror",
        "UFO Research (NSW) public copy attributed to the Department of Transport transcript",
        "PDF pp. 1–2; 09:06:14–09:12:49 GMT",
        [
            "Records Valentich reporting an unidentified object, green light, metallic appearance, and rough engine running",
            "Records loss of communications after a final open-microphone interval",
        ],
        [
            "Private/public mirror rather than direct NAA or Department of Transport custody",
            "Bracketed audio interpretations are editorial annotations in the mirror",
            "The communications do not establish object identity or causal connection to the disappearance",
        ],
        sourceUrl="https://www.ufor.asn.au/wp-content/uploads/2015/04/FrederickValentichFinalCommunication.pdf",
    ),
    record(
        "Atlas evidence-depth audit · 2026-07-18",
        "evidence-audit",
        "Local Atlas audit derived from the current source inventory",
        "source-files/evidence-depth/VALENTICH-1978-evidence-depth.md",
        ["current source inventory", "explicit primary-record gaps", "provenance boundary"],
        ["not an independent source", "does not corroborate UFO causation", "cannot substitute for missing primary records"],
    ),
]
valentich["heroVisual"]["provenance"] = "Atlas editorial summary; official locators and public transcript mirror"
timeline["TL-1978A"]["desc"] = "Valentich's reported unidentified object appears in a public final-communications transcript copy before contact is lost; the record does not establish the cause of his disappearance."

phoenix = cases["BF-1997-PH-01"]
phoenix.update({
    "summary": "The March 13 record contains at least two analytically distinct windows: earlier moving-formation and large-dark-object reports across Arizona, and later stationary lights near Phoenix associated in contemporaneous press reporting with Maryland Air National Guard illumination flares. The flare account addresses the later light event, not automatically every earlier report.",
    "official": "A contemporaneous press report quoted Arizona and Maryland Air National Guard spokespeople describing an A-10 illumination-flare exercise south of Phoenix and jettisoned flares before return to Tucson. Symington's 2007 firsthand retrospective described a separate moving delta-shaped observation; no official case file or synchronized master chronology is mapped.",
    "gap": "A time-synchronized witness corpus, original full-resolution videos with custody, Maryland ANG sortie/flare-expenditure records, range logs, and contemporaneous FAA/radar records are needed to test each event window separately.",
    "sourceQuality": "Firsthand retrospective commentary plus contemporaneous press reporting; no official case file, sortie log, radar record, or original video custody is mapped.",
    "sourceLabel": "CNN firsthand commentary / contemporaneous press trail",
    "sourceLocator": "CNN commentary, November 9, 2007; Las Vegas Sun, July 25, 1997",
    "heroFact": "The earlier moving-formation reports and the later stationary-light/flare event are distinct evidence questions; one explanation cannot be applied to both without a synchronized record.",
    "acquisitionTargets": [
        "Maryland Air National Guard sortie and flare-expenditure records for March 13, 1997",
        "Barry M. Goldwater Range logs and contemporaneous FAA/radar records",
        "Original full-resolution videos with custody and a time-synchronized witness corpus",
    ],
})
phoenix["confidenceModel"]["provenance"] = "firsthand-retrospective-and-secondary-press"
phoenix["temporal"]["eventForm"] = "multi-phase-event"
phoenix["geospatial"].update({"role": "regional-report-corridor", "precision": "regional-corridor", "uncertaintyKm": 200})
phoenix["sourceRecords"] = [
    record(
        "Fife Symington CNN firsthand retrospective",
        "firsthand-retrospective-commentary",
        "CNN, November 9, 2007",
        "web commentary; no page",
        ["Symington's personal-observation claim", "reported delta shape and silence", "his distinction between his observation and flares"],
        ["Published ten years later", "Not an official investigation", "Does not establish a common cause for the statewide reports"],
        sourceUrl="https://www.cnn.com/2007/TECH/science/11/09/simington.ufocommentary/index.html",
    ),
    record(
        "Las Vegas Sun · Maryland Air National Guard flare report, July 25, 1997",
        "contemporaneous-press-attribution",
        "Las Vegas Sun report quoting Arizona ANG Capt. Eileen Bienz and Maryland ANG Capt. Drew Sullins",
        "July 25, 1997 article; no page",
        ["Documents the official-attributed A-10 illumination-flare account for later lights south of Phoenix", "Reports that the explanation did not appear to cover all earlier/northern sightings"],
        ["Press report rather than the underlying sortie, range, or flare-expenditure records", "Does not identify every reported light or resolve earlier moving-formation/large-object reports"],
        sourceUrl="https://lasvegassun.com/news/1997/jul/25/military-now-says-flares-may-be-cause-of-mysteriou/",
    ),
]
phoenix["heroVisual"].update({
    "visualType": "public-context-frame",
    "caption": "Nighttime-light context image used to represent the Phoenix Lights public record.",
    "evidenceStatus": "Atlas preview without original video custody; it cannot establish which event window is depicted and is not proof that the earlier reports and later flare event shared one cause.",
    "isEventEvidence": False,
})
phoenix["publicSources"] = [
    *[source for source in phoenix.get("publicSources", []) if "Las Vegas Sun" not in source.get("label", "")],
    {
        "access": "Public",
        "label": "Las Vegas Sun — Maryland Air National Guard flare report",
        "note": "Contemporaneous press report quoting Guard spokespeople; supports the later flare-event account, not every earlier moving-object report.",
        "publisher": "Las Vegas Sun",
        "scope": "contemporaneous-press-official-attribution",
        "url": "https://lasvegassun.com/news/1997/jul/25/military-now-says-flares-may-be-cause-of-mysteriou/",
    },
]
timeline["EV-1997-PH-01"]["desc"] = "Earlier moving-formation and large-object reports remain analytically separate from later stationary lights attributed in contemporaneous press reporting to Maryland ANG flares."

DATA.write_text(json.dumps(atlas, indent=2, ensure_ascii=False) + "\n")

manifest = json.loads(PUBLIC_MANIFEST.read_text())
for case_id in AUTHORIZED_CASE_IDS:
    manifest[case_id] = cases[case_id].get("publicSources", [])
PUBLIC_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

print(json.dumps({
    "status": "applied",
    "caseIds": sorted(AUTHORIZED_CASE_IDS),
    "timelineIds": sorted(AUTHORIZED_TIMELINE_IDS),
    "files": [str(DATA.relative_to(ROOT)), str(PUBLIC_MANIFEST.relative_to(ROOT))],
}, indent=2))
