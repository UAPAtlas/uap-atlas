#!/usr/bin/env python3
"""Idempotently integrate the 2026-09-08 Valentich public mirror review."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "BF-1978-VL-01"
TIMELINE_ID = "TL-1978A"
INV_TOKEN = "VALENTICH-B1497-1978"
SAR_TOKEN = "VALENTICH-A4703-SAR"
INV_PDF = "source-files/public-mirrors/VALENTICH-1978/valentich_blackvault_fullpacket.pdf"
SAR_PDF = "source-files/public-mirrors/VALENTICH-1978/valentich_a4703_1978-1205_11485989.pdf"
INV_URL = "https://documents.theblackvault.com/documents/ufos/australia/B1497_V116-783-1047_10491375.pdf"
SAR_URL = "https://documents.theblackvault.com/documents/ufos/australia/A4703_1978-1205_11485989.pdf"

INV_PUBLIC = {
    "access": "Public mirror; local PDF held as custody-only research corpus",
    "label": "Black Vault mirror — NAA B1497 V116/783/1047 Valentich investigation file (316 pages)",
    "note": "Public mirror of released Department of Transport investigation material. Atlas cites inspected PDF pages 6–8, 12–17, 103–104; mirror custody does not prove direct NAA payload completeness or original audio/raw sensor custody.",
    "publisher": "The Black Vault / National Archives of Australia release mirror",
    "scope": "public-mirror-investigation-file-custody-only",
    "url": INV_URL,
}
SAR_PUBLIC = {
    "access": "Public mirror; local PDF held as custody-only research corpus",
    "label": "Black Vault mirror — NAA A4703 1978/1205 search-and-rescue file (218 pages)",
    "note": "Public mirror of released SAR material. Atlas cites pp.4–5 and p.22 for the MARSAR narrative and time-bounded search metrics; p.106 is an unrelated aircraft report and is excluded from this case.",
    "publisher": "The Black Vault / National Archives of Australia release mirror",
    "scope": "public-mirror-search-file-custody-only",
    "url": SAR_URL,
}

SOURCES = [
    f"{INV_TOKEN} · Black Vault mirror of NAA B1497 V116/783/1047",
    f"{SAR_TOKEN} · Black Vault mirror of NAA A4703 1978/1205",
    "VALENTICH-1978 · DoT transcript / National Archives of Australia file",
]

SOURCE_RECORDS = [
    {
        "citation": "Aircraft Accident Investigation Summary Report, approved 27 Apr 1982 · B1497 PDF pp.6–8",
        "sourceType": "released-department-of-transport-investigation-report-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia B1497 V116/783/1047, NAA barcode 10491375",
        "locator": INV_TOKEN,
        "pages": [6, 7, 8],
        "supports": [
            "Identifies Frederick Valentich, Cessna 182L VH-DSJ, and the event date as 21 October 1978",
            "Preserves the final communications including 1912:09: “it is hovering and it's not an aircraft”",
            "Records the official approved finding: “The reason for the disappearance of the aircraft has not been determined.”",
        ],
        "limitations": [
            "Does not identify the reported object or establish UFO causation",
            "Does not provide original flight-service audio custody",
            "Does not close raw radar or sensor provenance targets",
        ],
    },
    {
        "citation": "NAA access mask · B1497 PDF p.12, mask date 6 Mar 2012",
        "sourceType": "historical-access-mask-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia B1497 V116/783/1047",
        "locator": INV_TOKEN,
        "pages": [12],
        "supports": [
            "Documents a historical 2012 mask for approximately 0.5 cm of 1985–1992 material marked “Not in the open period”",
            "Shows the downloaded 316-page mirror should not be described as the complete archival file",
        ],
        "limitations": [
            "Does not establish that those later folios remain restricted today",
            "Does not enumerate the omitted folio page numbers",
            "Does not describe a national-security exemption finding",
        ],
    },
    {
        "citation": "RAN Research Laboratory cowl-flap correspondence, map, and photographs · B1497 PDF pp.13, 15–17",
        "sourceType": "released-investigation-correspondence-physical-debris-lead-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia B1497 V116/783/1047",
        "locator": INV_TOKEN,
        "pages": [13, 15, 16, 17],
        "supports": [
            "Records a Cessna 182 engine cowl flap found at Parry's Bay, Flinders Island, on 15 May 1983",
            "States the compatible serial-number range includes the missing aircraft",
            "Holds the related location map and two photographic views in the investigation mirror",
        ],
        "limitations": [
            "Does not uniquely identify the part as VH-DSJ debris",
            "The 14 October 1983 RAN transport explanation is a possible storm/current mechanism, not a confirmed drift track",
            "Cowl flaps can separate in flight and the finding does not determine the disappearance cause",
        ],
    },
    {
        "citation": "Materials Research Laboratories oil-sample result · B1497 PDF p.103",
        "sourceType": "released-laboratory-correspondence-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia B1497 V116/783/1047",
        "locator": INV_TOKEN,
        "pages": [103],
        "supports": [
            "Reports solvent extraction, gas chromatography, and mass spectrometry on oil samples",
            "Finds hydrocarbons more consistent with bunkering fuel oil than gasoline or lubricating oil",
        ],
        "limitations": [
            "Does not identify an aircraft-derived slick",
            "Sampling limitations remain part of the record",
        ],
    },
    {
        "citation": "M.J. Harwood radar-analysis minute · B1497 PDF p.104, duplicate p.110",
        "sourceType": "released-radar-analysis-minute-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia B1497 V116/783/1047",
        "locator": INV_TOKEN,
        "pages": [104, 110],
        "supports": [
            "Documents radar-related discussion of anomalous propagation and second-time-round returns",
            "Provides a conventional interpretation of controller notes",
        ],
        "limitations": [
            "Is a radar-analysis memo, not a raw radar track",
            "Does not verify a track of the object reported by Valentich",
            "Does not close the raw-sensor provenance target",
        ],
    },
    {
        "citation": "MARSAR/SAR SITREP narrative · A4703 PDF pp.4–5, 22",
        "sourceType": "released-search-and-rescue-file-public-mirror",
        "provenance": "Black Vault public mirror of National Archives of Australia A4703 1978/1205, NAA barcode 11485989",
        "locator": SAR_TOKEN,
        "pages": [4, 5, 22],
        "supports": [
            "Documents contemporaneous search operations after the disappearance",
            "Records seven civil aircraft searching 5,000 square nautical miles on 24 October 1978",
            "Records 62 hours 35 minutes of search flying to the 25 October SITREP reporting time, with further searching still planned before active operations were to cease at 1900 EST",
        ],
        "limitations": [
            "Search metrics are time-bounded, not final all-source search totals",
            "Search datums and projected splash points are planning estimates, not measured aircraft positions or UFO tracks",
            "SAR p.106 concerns different aircraft in the Tennant Creek–Darwin/Tindal area and is excluded from the Valentich case",
        ],
    },
    {
        "citation": "Atlas evidence-depth audit · 2026-07-18",
        "sourceType": "evidence-audit",
        "provenance": "Local Atlas audit derived from the current source inventory",
        "locator": "source-files/evidence-depth/VALENTICH-1978-evidence-depth.md",
        "supports": ["current source inventory", "explicit primary-record gaps", "provenance boundary"],
        "limitations": ["not an independent source", "does not corroborate the event narrative", "cannot substitute for missing primary records"],
    },
]

SOURCE_UPDATE_CARD = {
    "title": "2026 public-mirror source update",
    "status": "Default-visible boundary card",
    "findings": [
        "Released investigation and SAR PDFs are now held locally as custody-only public mirrors, with exact inspected pages mapped.",
        "The official report states: “The reason for the disappearance of the aircraft has not been determined.”",
        "The 1983 cowl flap is compatible with the missing aircraft's serial-number range, not identified as VH-DSJ debris.",
        "The sampled hydrocarbons were more consistent with bunkering fuel oil than gasoline or lubricating oil; the radar item is an analysis memo, not a raw object track.",
    ],
    "limitations": [
        "Original flight-service audio, raw radar/sensor provenance, later masked 1985–1992 folios, and direct-origin completeness remain open acquisition targets.",
        "The 2012 access mask is a historical access condition, not proof of a current restriction.",
        "SAR p.106 is unrelated aircraft material and is excluded.",
    ],
}

ACQ = [
    {"id":"valentich-b1497-public-mirror","label":"B1497 V116/783/1047 public mirror PDF", "status":"recovered-new", "locator": INV_PDF, "publicMirrorUrl": INV_URL},
    {"id":"valentich-a4703-public-mirror","label":"A4703 1978/1205 SAR public mirror PDF", "status":"recovered-new", "locator": SAR_PDF, "publicMirrorUrl": SAR_URL},
    {"id":"valentich-direct-naa-payload-completeness","label":"Direct NAA payload completeness/version check", "status":"open"},
    {"id":"valentich-1985-1992-masked-folios","label":"Later 1985–1992 folios represented by the 6 Mar 2012 access mask", "status":"open"},
    {"id":"valentich-original-flight-service-audio","label":"Original flight-service audio custody", "status":"open"},
    {"id":"valentich-raw-radar-sensor-provenance","label":"Complete raw radar/sensor provenance", "status":"open"},
    {"id":"valentich-later-folios-and-attachments","label":"Any later folios, attachments, and original-material classes beyond the released mirrors", "status":"open"},
]

def load(name): return json.loads((ROOT/name).read_text())
def dump(name, data): (ROOT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
def merge_by_url(existing, additions):
    out=[x for x in existing if x.get('url') not in {a['url'] for a in additions}]
    out.extend(additions)
    return out

def main():
    atlas=load('atlas-data.json')
    changed=[]
    case=next(c for c in atlas['cases'] if c['id']==CASE_ID)
    before=json.dumps(case, sort_keys=True, ensure_ascii=False)
    case.update({
        "keyQuote": "it is hovering and it's not an aircraft",
        "quoteSource": "Aircraft Accident Investigation Summary Report transcript, 1912:09 EST, 21 Oct 1978; B1497 PDF p.8",
        "quoteConfidence": "High for the recovered report quotation; lower for any causal interpretation beyond the recorded communications.",
        "sourceQuality": "Released Department of Transport investigation and search records held as Black Vault public-mirror PDFs, with identifying and consequential pages inspected. Direct NAA payload completeness, original flight-service audio, and raw radar provenance remain unresolved. Official-record custody does not establish the reported object's identity or disappearance causation.",
        "date": "21 OCT 1978",
        "summary": "Pilot Frederick Valentich, 20, reported an unidentified object with green lights pacing his Cessna over Bass Strait on 21 October 1978; the released investigation report preserves the final communications, including “it is hovering and it's not an aircraft,” before contact ended. Neither pilot nor aircraft was recovered, and the official cause finding remained unresolved.",
        "keyFact": "The recovered Department of Transport report preserves Valentich's final communication and states the disappearance cause was not determined.",
        "heroFact": "The recovered Department of Transport report preserves Valentich's final communication and states the disappearance cause was not determined.",
        "official": "The Aircraft Accident Investigation Summary Report, approved 27 April 1982, states: “The reason for the disappearance of the aircraft has not been determined.” The released file preserves the reported communications and supporting investigative material.",
        "gap": "Released investigation and SAR mirror PDFs are now held locally, but direct NAA payload completeness, original flight-service audio, raw radar/sensor provenance, and later 1985–1992 folios represented by a historical 2012 access mask remain open. The 1983 cowl flap was compatible with the missing aircraft's serial-number range but was not identified as VH-DSJ debris; the radar-analysis memo is not a raw object track.",
        "sources": SOURCES,
        "sourceLabel": "DoT investigation and SAR public mirrors",
        "sourceLocator": INV_TOKEN,
        "sourceRecords": SOURCE_RECORDS,
        "sourceUpdateCard": SOURCE_UPDATE_CARD,
        "acquisitionTargets": ACQ,
    })
    case['temporal']={"dateLabel":"21 OCT 1978","year":1978,"startDateTime":"1978-10-21T18:19:00+10:00","endDateTime":None,"timezone":"Australia/EST as source-labeled; GMT also appears in search reporting","durationSeconds":None,"precision":"day","eventForm":"single-event"}
    pubs=merge_by_url(case.get('publicSources', []), [INV_PUBLIC, SAR_PUBLIC])
    case['publicSources']=pubs
    after=json.dumps(case, sort_keys=True, ensure_ascii=False)
    if before!=after: changed.append(CASE_ID)
    for ev in atlas.get('timeline',[]):
        if ev.get('id')==TIMELINE_ID:
            b=json.dumps(ev, sort_keys=True, ensure_ascii=False)
            ev.update({"date":"21 OCT 1978","desc":"Valentich's final communications are preserved in the held investigation mirror, including “it is hovering and it's not an aircraft”; the official report states the disappearance cause was not determined."})
            if json.dumps(ev, sort_keys=True, ensure_ascii=False)!=b: changed.append(TIMELINE_ID)
    dump('atlas-data.json', atlas)
    sfi=load('source-file-index.json')
    sfi[INV_TOKEN]=[INV_PDF]
    sfi[SAR_TOKEN]=[SAR_PDF]
    # Keep legacy token but do not broadly duplicate PDFs there.
    dump('source-file-index.json', sfi)
    manifest=load('public-source-manifest.json')
    manifest[CASE_ID]=pubs
    dump('public-source-manifest.json', manifest)
    print(json.dumps({"scopeCaseIds":[CASE_ID],"scopeTimelineIds":[TIMELINE_ID],"changedIds":changed,"sourceIndexTokens":[INV_TOKEN,SAR_TOKEN],"publicManifestCaseIds":[CASE_ID]}, indent=2))
if __name__=='__main__': main()
