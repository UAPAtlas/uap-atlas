#!/usr/bin/env python3
"""Apply the August 2026 exact-20 quality/acquisition enrichment tranche.

Public-only audit: no outreach, forms, accounts, purchases, or records requests.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "atlas-data.json"

QUALITY_SCOPE = [
    "BF-SF-08", "BF-SF-13", "BF-1978-KK-01", "BF-2020-AS-01", "BF-1944-FF-01",
    "BF-1977-CL-01", "BF-2025-YS-01", "BF-1989-BW-01", "BF-SF-04",
]
ACQUISITION_SCOPE = [
    "BF-1987-GB-01", "BF-1994-AR-01", "BF-1933-MG-01", "BF-1975-TW-01",
    "BF-1996-VG-01", "BF-SF-12", "BF-1966-WS-01", "BF-1973-PG-01",
    "BF-1978-VL-01", "BF-2014-CH-01", "BF-SF-06",
]
SCOPE = QUALITY_SCOPE + ACQUISITION_SCOPE


def target(target_type: str, description: str, status: str, result: str, *, locator: str | None = None, reason: str | None = None) -> dict:
    out = {
        "targetType": target_type,
        "description": description,
        "status": status,
        "publicOnlyResult": result,
    }
    if locator:
        out["locator"] = locator
    if reason:
        out["reasonNeeded"] = reason
    return out


P = {
    "BF-SF-08": {
        "sourceQuality": "Public report-copy custody for the English COMETA translation, with local PDF/page-image custody and an Internet Archive public mirror. The mapped source verifies the report title, COMETA authorship/translation context, and published argument, but not official French government endorsement or the unpublished underlying case dossiers.",
        "quoteConfidence": "High for the report title and English-translation text visible in the mapped PDF; institutional authorship does not make the report an official French state finding.",
    },
    "BF-SF-13": {
        "domain": "CIVILIAN / CONTACTEE CORPUS",
        "sourceQuality": "Secondary/public-claim trail with local representative image custody only. The Atlas holds reproductions and cultural/skeptical context, but no neutral custody for original negatives, films, recordings, or alleged samples.",
        "quoteConfidence": "Medium for the existence and cultural influence of the long-running Meier/FIGU claim corpus; low for authentication because original-media/sample custody and neutral technical analysis are not mapped.",
        "observation": {"witnessCount": None, "witnessRoles": ["claimant", "FIGU associates/followers", "public commentators"], "sensors": ["photographic/film"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("original-media-and-sample-custody", "Documented neutral custody for original Meier negatives, films, recordings, and alleged metal samples", "publicly-unavailable", "No neutral original-media or sample custody was recovered", reason="Required before any authentication-related upgrade."),
            target("first-party-corpus-index", "Stable first-party FIGU corpus index with exact image/date provenance", "publicly-unavailable", "No stable first-party provenance index is currently mapped"),
            target("independent-technical-analysis", "Independent technical analyses with media/sample chain-of-custody documentation", "publicly-unavailable", "No neutral custody-complete technical packet was recovered"),
        ],
    },
    "BF-1978-KK-01": {
        "sourceQuality": "Partial official-record custody: an Archives New Zealand/RNZAF-DSIR investigation page is locally held with provenance, alongside public film-frame media. First-generation TV1/Fogarty film, the Crockett copy, native radar logs, complete analytical workpapers, and final disposition remain unmapped.",
        "quoteConfidence": "High for the recovered official savingram wording; filmed/radar object interpretation remains unresolved because native film, radar, and complete workpaper custody is missing.",
        "acquisitionTargets": [
            target("first-generation-film", "First-generation TV1/Fogarty film and Crockett film copy", "publicly-unavailable", "Public frame/media trail exists; native film material was not recovered"),
            target("radar-and-analysis-records", "Native Wellington ATC/radar logs, timing records, and DSIR/RNZAF analytical workpapers", "publicly-unavailable", "No native radar/timing/workpaper packet was recovered"),
            target("final-official-disposition", "Final RNZAF/DSIR disposition or closure record", "publicly-unavailable", "Current recovered official page is interim/provisional"),
        ],
    },
    "BF-2020-AS-01": {
        "sourceQuality": "Official War.gov range-fouler report/debrief trail with local DOW-UAP-D44 and D56 page-image custody. D44 visibly supports the reported tracking details and phrase 'a few abrupt directional changes'; the Atlas does not hold the native sensor packet, platform metadata, radar data, or analytical workpapers.",
        "quoteConfidence": "High for 'a few abrupt directional changes' and other wording visible on the locally held DOW-UAP-D44 report page; low for performance or object interpretation beyond the released form.",
        "acquisitionTargets": [
            target("complete-official-release", "Complete public DOW-UAP-D44/D56 record packet with release metadata", "partially-recovered", "D44/D56 page-image custody is held; complete release packet and text layer remain incomplete"),
            target("native-sensor-packet", "Native sensor media, platform metadata, radar data, and analytical workpapers", "publicly-unavailable", "No native sensor/metadata/analysis packet was recovered"),
        ],
    },
    "BF-1944-FF-01": {
        "sourceQuality": "Exact AFHRA catalog custody plus public transcription custody. The Atlas has AFHRA call numbers/reel-frame locators and a CUFON transcription of wartime diary text, but not the underlying microfilm images or complete original packet.",
        "quoteConfidence": "Medium for the transcribed wartime diary wording and exact AFHRA catalog locators; not high until the cited December 1944 entries are checked against original microfilm scans.",
        "acquisitionTargets": [
            target("afhra-war-diary-microfilm", "AFHRA IRIS 60059 / call SQ-FI-415-HI / reel 0000000848 / frames 1519–1631", "locator-only", "Exact archive locator recovered; scans are not held", reason="Needed to verify the 415th Night Fighter Squadron diary quotation."),
            target("afhra-operations-microfilm", "AFHRA IRIS 60074 / call SQ-FI-415-SU-OP-S / reel 848 / frames 1763–1867", "locator-only", "Exact archive locator recovered; scans are not held"),
            target("afhra-wwii-notes-microfilm", "AFHRA IRIS 1026183 / call SQ-FI-415-SU-PE / reel 33170 / frame 886 onward", "locator-only", "Exact archive locator recovered; scans are not held"),
        ],
    },
    "BF-1977-CL-01": {
        "sourceQuality": "Brazilian Arquivo Nacional primary-document custody with local PDF and page-image custody for Informação 1802/320/ADE/77, pp. 4–5. The mapped pages support the quoted medical/witness-report passage and internal skepticism, but not original-negative custody or independent medical-record attachments.",
        "quoteConfidence": "High for the quoted Portuguese passage on the locally held Arquivo Nacional PDF pages 4–5; medical-causation and photographic-authentication claims remain limited by missing attachments and original negatives.",
    },
    "BF-2025-YS-01": {
        "sourceQuality": "Official DVIDS/AARO public-release record with local frame custody for DOW-UAP-PR104 / DOD_111830027. The source supports release metadata and an informational video description, but supplies no platform identification, range data, sensor metadata, or analytical conclusion.",
        "quoteConfidence": "High for the DVIDS title, metadata, and informational description; the source expressly disclaims analytical judgment, investigative conclusion, or factual determination about the area's nature or significance.",
        "summary": "USINDOPACOM submitted an infrared-video UAP report to AARO for the Yellow Sea. DVIDS describes the submission as 18 seconds of footage while public video metadata lists 00:00:15; the visible description says the sensor pans from 00:01–00:15 to track an area of contrast resembling a six-pointed star. The release supplies no analytical attribution.",
    },
    "BF-1989-BW-01": {
        "sourceQuality": "Mixed public-copy custody: a Belgian Air Force report page image for the F-16 scramble/radar narrative plus a COBEPS 2012 retrospective PDF. These support official/public investigation history and wave-scale context, but raw radar tapes, calibrated data, and a complete native official publication chain remain absent.",
        "quoteConfidence": "High for the Belgian Air Force quotation read from the mapped report page image and high for page-verified COBEPS retrospective statements; public-copy custody does not establish raw radar performance or extraordinary origin.",
    },
    "BF-SF-04": {
        "domain": "SCIENTIFIC / HISTORICAL CONTEXT",
        "environment": ["terrestrial", "academic-institution"],
        "keyQuote": "The Role of Gravitation in Physics — Report from the 1957 Chapel Hill Conference",
        "quoteSource": "CHAPELHILL-1957 proceedings title page, visually verified in local Atlas custody",
        "quoteConfidence": "High for the exact title visible on the locally held proceedings title page; the proceedings provide scientific/historical context, not evidence of an operational anti-gravity vehicle or UAP event.",
        "sourceQuality": "Local primary proceedings custody for the 1957 Chapel Hill gravity conference, including the full PDF and visually verified title-page images. The public NARA link is collection-guide context rather than a case-specific proceedings locator; the file establishes conference context, not demonstrated gravity control.",
        "observation": {"witnessCount": None, "witnessRoles": ["physicists", "conference organizers", "scientific participants"], "sensors": [], "durationSeconds": None, "independentWitnessGroups": None},
    },
    "BF-1987-GB-01": {
        "mode": "approximate",
        "sourceQuality": "Public custody is limited to an exact Rice University finding-aid locator for Richard F. Haines Ufology papers, MS 0706, Series VIII, Box 11, Folder 12, 'UFO photos: Gulf Breeze, Florida, 1990.' It establishes institutional folder custody, not displayed original Walters media or first-generation chain of custody from the 1987–1988 series.",
        "quoteConfidence": "Medium for the public photo-series/controversy record and Rice archival metadata; no authenticated-original image statement or first-generation custody packet is publicly mapped.",
        "observation": {"witnessCount": None, "witnessRoles": ["civilian photographer", "civilian investigators"], "sensors": ["photographic/film", "unaided-visual"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("original-photographic-material", "Authenticated Walters original Polaroids, negatives if any, first-generation prints, and complete camera/processing custody for the 1987–1988 series", "publicly-unavailable", "No authenticated original or first-generation custody packet was recovered"),
            target("institutional-folder-contents", "Public digital objects or item-level inventory from Rice MS 0706, Series VIII, Box 11, Folder 12", "locator-only", "Finding aid is public; folder contents are not displayed", locator="https://archives.library.rice.edu/repositories/2/archival_objects/330044"),
        ],
    },
    "BF-1994-AR-01": {
        "sourceQuality": "Page-verified Cynthia Hind/UFO AFRINEWS Nos. 11–12 reporting is held locally as derivative scans/renders, and direct public publisher-site PDFs are accessible for both issues. This strengthens the near-contemporaneous publication layer, not original interview footage, field notes, drawings custody, official packets, or soil-lab records.",
        "quoteConfidence": "High transcription confidence for the page-verified AFRINEWS quotation; the publication layer does not substitute for original 1994 field-archive or official custody.",
        "observation": {"witnessCount": 62, "witnessRoles": ["students/schoolchildren", "civilian investigators", "journalists"], "sensors": ["recorded-interviews", "witness-drawings", "unaided-visual"], "durationSeconds": None, "independentWitnessGroups": 1},
        "acquisitionTargets": [
            target("original-field-archive", "Complete unedited 1994 interview footage/audio/transcripts, witness drawings, and Mack/Hind field notes", "publicly-unavailable", "Direct AFRINEWS PDFs were recovered; original field materials were not"),
            target("publisher-custody", "First-party UFO AFRINEWS publisher custody or production files for Nos. 11–12", "partially-recovered", "Direct public PDFs are accessible; original publisher archive remains unverified"),
            target("official-investigation", "Official Zimbabwean government, Ariel School, or police investigative packet", "publicly-unavailable", "No official packet was recovered"),
            target("soil-sampling-records", "Raw laboratory data, sampling notes, and custody records for reported soil follow-up", "publicly-unavailable", "AFRINEWS reports follow-up but supplies no raw lab/custody records"),
        ],
    },
    "BF-1933-MG-01": {
        "sourceQuality": "Anonymous RS/33 document-chain claim plus later public research trail. The mapped Domenica del Corriere reproduction documents a 1933 lightning incident near Magenta/Novara, not a UFO crash, recovery, RS/33 office, or craft. No first-party Italian state archive file or custody chain for the alleged RS/33 materials is recovered.",
        "quoteConfidence": "High for the mapped contemporaneous lightning caption; low for the separate RS/33 recovery claim because the alleged cache is anonymous and no first-party 1930s state custody is mapped.",
        "observation": {"witnessCount": None, "witnessRoles": ["anonymous document source", "later civilian researchers"], "sensors": [], "durationSeconds": None, "independentWitnessGroups": None},
        "phenomena": {"shapes": [], "objectCount": None, "luminosity": None, "motion": [], "effects": []},
        "acquisitionTargets": [
            target("original-rs33-documents", "Original RS/33 documents with verifiable Italian state-archive accession, provenance, and physical custody", "publicly-unavailable", "No first-party Italian state-archive file or accession was recovered"),
            target("contemporaneous-state-records", "Contemporaneous Italian government, military, intelligence, police, or recovery records specific to the alleged 1933 craft event", "publicly-unavailable", "Mapped contemporaneous clipping is a lightning report, not a recovery record"),
            target("press-boundary-record", "Domenica del Corriere, 9 July 1933, p. 16 lightning caption", "duplicate-existing", "Already mapped; constrains rather than corroborates the claim", locator="https://archive.org/details/ufo-crash-at-vergiate"),
        ],
    },
    "BF-1975-TW-01": {
        "sourceQuality": "No complete Navajo County sheriff/search packet, dispatch logs, interview forms, search records, or original polygraph charts are in public/local custody. An Arizona Daily Sun clipping locator dated November 8, 1975 is identified, but public automated access is blocked, so exact article text is not treated as verified quotation.",
        "quoteConfidence": "Medium-low: the selected sentence is a case-summary formulation, not a page-verified primary quotation; sheriff/search and original polygraph records remain unmapped.",
        "phenomena": {"shapes": ["structured-craft", "light"], "objectCount": 1, "luminosity": "beam of light reported by witnesses", "motion": [], "effects": ["reported missing-person/search event", "reported physical impact/beam effect"]},
        "acquisitionTargets": [
            target("law-enforcement-packet", "Complete Navajo County Sheriff missing-person, dispatch, search, interview, and incident records", "publicly-unavailable", "No complete law-enforcement packet was recovered"),
            target("polygraph-custody", "Original polygraph charts, examiner worksheets/reports, and authenticated testing custody", "publicly-unavailable", "Complete original polygraph custody was not recovered"),
            target("contemporaneous-press", "Arizona Daily Sun clipping concerning Travis Walton, November 8, 1975", "locator-only", "Locator identified; text not publicly recovered due access barrier", locator="https://www.newspapers.com/article/arizona-daily-sun-travis-walton-nov-8-19/82602751/"),
        ],
    },
    "BF-1996-VG-01": {
        "sourceQuality": "Complete contemporaneous IstoÉ spread, 'O Caso do ET de Varginha,' 22 May 1996, pp. 29–32, is publicly accessible through Arquivo Nacional/SIAN and rendered in Atlas custody. It establishes archival custody of a magazine article containing witness claims and Army denials, not a military, police, medical, capture, transport, or physical-custody packet.",
        "quoteConfidence": "High for the page-verified 1996 IstoÉ article quotation; low event-corroboration confidence because archival custody authenticates the article, not the alleged creature/capture narrative.",
        "observation": {"witnessCount": None, "witnessRoles": ["civilian witnesses", "ufologists", "Brazilian Army personnel as alleged/denying parties"], "sensors": ["unaided-visual", "press reporting"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("official-incident-records", "Brazilian military, police, fire-service, and hospital records specific to the January 1996 allegations", "publicly-unavailable", "No official incident packet was recovered; SIAN recovery is press only"),
            target("medical-physical-custody", "Authenticated capture, transport, medical, pathology, or physical-custody records", "publicly-unavailable", "No such custody record was recovered"),
            target("contemporaneous-press-archive", "IstoÉ, 22 May 1996, pp. 29–32, SIAN BR_DFANBSB_ARX_0_0_0443", "duplicate-existing", "Already mapped and publicly accessible; supports press/reporting layer only", locator="https://imagem.sian.an.gov.br/acervo/derivadas/BR_DFANBSB_ARX/0/0/0443/BR_DFANBSB_ARX_0_0_0443_d0001de0001.pdf"),
        ],
    },
    "BF-SF-12": {
        "domain": "MEDIA / PROVENANCE",
        "status": "DOCUMENTED MEDIA HOAX · PRIMARY INTERVIEW/BROADCAST CUSTODY MISSING",
        "confidence": "CONFIRMED PUBLIC MEDIA CONTROVERSY · EXACT ADMISSION WORDING UNVERIFIED",
        "sourceQuality": "Secondary public context includes TIME's 2016 retrospective summarizing the 1995 broadcast controversy, the exact 2006 Eamonn Investigates admission source that remains missing, and John Humphreys production claims. The exact broadcast/interview, production documentation, and claimed original film master are not held.",
        "quoteConfidence": "Unverified for exact Santilli/Humphreys wording; medium only for TIME's attributed secondary summary. Do not present TIME paraphrase as exact Santilli speech.",
        "acquisitionTargets": [
            target("exact-2006-interview", "Exact Eamonn Investigates recording or transcript containing Santilli's characterization", "publicly-unavailable", "Secondary summaries and metadata found; exact recording/transcript not recovered"),
            target("broadcast-distribution-record", "First-generation 1995 broadcast/distribution record and production documentation", "publicly-unavailable", "No first-generation broadcast master or production packet recovered"),
            target("claimed-original-film-material", "Claimed original film master, camera negative, frames, or physical material with reviewable custody", "publicly-unavailable", "No claimed original material with reviewable custody recovered"),
            target("humphreys-admission-record", "Exact John Humphreys interview/admission recording or transcript and production documentation", "publicly-unavailable", "TIME secondary summary recovered; exact source not recovered"),
            target("secondary-public-context", "TIME 2016 retrospective", "recovered-new", "Accessible secondary source recovered; attribution boundary required", locator="https://time.com/4376871/alien-autopsy-hoax-history/"),
        ],
    },
    "BF-1966-WS-01": {
        "mode": "approximate",
        "sourceQuality": "Contemporaneous/public Westall press and student-drawing context plus State Library Victoria archival review; no complete RAAF, police, school-administration, Department of Civil Aviation, or NAA case packet has been publicly recovered or mapped.",
        "quoteConfidence": "High for preserved Atlas-held AFSR/press artifacts; unresolved for official-file claims because no complete official or contemporaneous administrative packet is mapped.",
        "observation": {"witnessCount": None, "witnessRoles": ["students/schoolchildren", "school staff"], "sensors": ["unaided-visual"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("official-case-packet", "RAAF, Department of Civil Aviation, NAA, police, school-administration, or related records specific to Westall, April 1966", "publicly-unavailable", "No complete official incident packet was recovered"),
            target("first-generation-witness-material", "Original statements, drawings, photographs, film, investigator files, or school-origin materials", "publicly-unavailable", "No complete first-generation corpus was recovered"),
        ],
    },
    "BF-1973-PG-01": {
        "mode": "approximate",
        "sourceQuality": "Historically documented Hickson/Parker report to local authorities plus a public local-history trail concerning a reported sheriff-room recording; no authenticated complete Jackson County sheriff packet, original audio custody chain, or complete timecoded transcript is mapped.",
        "quoteConfidence": "Low-to-medium for publicly circulated recording-trail wording; original audio custody, issuer/date-bearing complete transcript, and sheriff packet are not mapped.",
        "acquisitionTargets": [
            target("law-enforcement-case-packet", "Authenticated complete Jackson County sheriff case/interview packet", "publicly-unavailable", "No complete packet recovered"),
            target("original-audio", "Original or earliest-generation sheriff-room recording with custody history", "publicly-unavailable", "No original/earliest-generation audio custody recovered"),
            target("complete-transcript", "Complete transcript with issuer, date, page/timecode locators, and relation to original audio", "publicly-unavailable", "No custody-complete transcript recovered"),
            target("contemporaneous-authority-or-press-records", "Earliest complete authority report, interview logs, follow-up notes, or contemporaneous local press packet", "publicly-unavailable", "No complete earliest packet recovered"),
        ],
    },
    "BF-1978-VL-01": {
        "sourceQuality": "Exact official NAA catalog locator, official ATSB report locator, and inspected UFOr public transcript mirror. Current custody lacks the complete primary packet, direct official transcript/audio, complete search file, and radar/sensor records; none establishes UFO causation.",
        "quoteConfidence": "High for wording visible in the inspected UFOr transcript mirror; not high for direct official custody because the complete NAA/Department of Transport packet and original audio are not held.",
        "acquisitionTargets": [
            target("official-investigation-packet", "Complete NAA/Department of Transport packet B1497 V116/783/1047 / Barcode 10491375", "locator-only", "Exact catalog locator verified; packet not inspected"),
            target("official-transcript-or-audio", "Direct official final-communications transcript and original/earliest-generation ATC audio", "publicly-unavailable", "Only a public transcript mirror was inspected"),
            target("search-and-sensor-records", "Complete official search documentation, radar records, air-traffic records, and sensor/communications logs", "publicly-unavailable", "No complete records recovered"),
        ],
    },
    "BF-2014-CH-01": {
        "sourceQuality": "Public CEFAA/Chilean Navy release-reporting trail, accessible HuffPost report, public-video mirror derivatives, and Atlas-held frame/provenance. Native Navy media, embedded WESCAM telemetry, full metadata, agency workpapers, and custody remain unavailable.",
        "quoteConfidence": "Medium for the public CEFAA/Chilean Navy release-reporting trail and inspected mirror frame; low for exact agency-file wording, native metadata, or final analytic conclusion.",
        "observation": {"witnessCount": None, "witnessRoles": ["Chilean Navy aircrew", "CEFAA/technical analysts"], "sensors": ["infrared/thermal", "photographic/film"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("native-sensor-media", "Native 2014 Chilean Navy WESCAM/FLIR master with telemetry, file metadata, and custody record", "publicly-unavailable", "No native sensor master/metadata packet recovered"),
            target("agency-case-file", "Complete CEFAA/SEFAA analyst file, flight-track workpapers, aircraft data, meteorology, and disposition", "publicly-unavailable", "No complete agency analytical file recovered"),
        ],
    },
    "BF-SF-06": {
        "sourceQuality": "Rocket Pictures/Victor public-release trail plus Internet Archive full-program mirror; current custody documents a public media artifact, not the alleged original tape, agency custody, Victor identity/access, production master, or authenticated transfer chain.",
        "quoteConfidence": "High for the documented public-release artifact and Internet Archive program mirror; low for Area 51/S-4 provenance, Victor identity, original tape custody, and authenticity.",
        "observation": {"witnessCount": None, "witnessRoles": ["anonymous claimant", "media-production/distribution personnel"], "sensors": ["photographic/film"], "durationSeconds": None, "independentWitnessGroups": None},
        "acquisitionTargets": [
            target("original-or-production-master", "Original alleged Victor tape or Rocket Pictures production master with authenticated duplication/transfer custody", "publicly-unavailable", "No original or production master recovered"),
            target("identity-and-access-records", "Verifiable Victor identity/access evidence and production/forensic records", "publicly-unavailable", "No verified identity/access packet recovered"),
        ],
    },
}


def upsert_public_source(case: dict, label: str, payload: dict) -> None:
    sources = case.setdefault("publicSources", [])
    for index, item in enumerate(sources):
        if item.get("label") == label or item.get("url") == payload.get("url"):
            sources[index] = payload
            return
    sources.append(payload)


def upsert_source_record(case: dict, match: str, payload: dict) -> None:
    records = case.setdefault("sourceRecords", [])
    for index, item in enumerate(records):
        if match in str(item.get("citation", "")):
            merged = dict(item)
            merged.update(payload)
            records[index] = merged
            return
    records.append(payload)


def apply_custom(case: dict) -> None:
    cid = case["id"]
    if cid == "BF-SF-08":
        case.setdefault("confidenceModel", {})["provenance"] = "public-report-copy"
        case["sourceRecords"][0].update({"sourceType": "public-report-copy", "locator": "COMETA-1999; local English translation PDF p. 1"})
    elif cid == "BF-SF-13":
        case.setdefault("heroVisual", {}).update({"isEventEvidence": False, "evidenceStatus": "Claimed event-image reproduction; original-negative custody and authenticity are not established."})
        case["publicSources"] = [s for s in case.get("publicSources", []) if "NARA" not in str(s.get("label", ""))]
    elif cid == "BF-1944-FF-01":
        case["sourceRecords"][0]["sourceType"] = "archive-catalog-locator"
    elif cid == "BF-1977-CL-01":
        case.setdefault("heroVisual", {}).update({"isEventEvidence": False, "evidenceStatus": "Archival reproduction of an alleged Operation Prato photograph; original-negative custody is not established."})
    elif cid == "BF-2025-YS-01":
        case.setdefault("temporal", {})["durationSeconds"] = 15
        case.setdefault("observation", {})["durationSeconds"] = 15
    elif cid == "BF-1994-AR-01":
        upsert_source_record(case, "UFO AFRINEWS No. 11", {"sourceType": "near-contemporaneous-investigator-report-public-pdf", "provenance": "Cynthia Hind / UFO AFRINEWS No. 11; direct public publisher-site PDF accessible; Atlas also holds local derivative renders.", "locator": "UFO_AFRINEWS11-150.pdf#page=12-13", "sourceUrl": "http://ufoafrinews.com/pdfs/UFO_AFRINEWS11-150.pdf"})
        upsert_source_record(case, "UFO AFRINEWS No. 12", {"sourceType": "follow-up-investigator-report-public-pdf", "provenance": "Cynthia Hind / UFO AFRINEWS No. 12; direct public publisher-site PDF accessible; Atlas also holds local derivative renders.", "locator": "UFO_AFRINEWS12-150.pdf#page=6-7", "sourceUrl": "https://www.ufoafrinews.com/pdfs/UFO_AFRINEWS12-150.pdf"})
    elif cid == "BF-SF-12":
        time = {"label": "TIME — How an Alien Autopsy Hoax Captured the World's Imagination for a Decade", "url": "https://time.com/4376871/alien-autopsy-hoax-history/", "publisher": "TIME", "access": "Public", "scope": "secondary-media-history", "role": "contextual-analysis", "mediaKind": "article", "note": "Secondary retrospective; not the exact 2006 interview, broadcast master, or production packet."}
        upsert_public_source(case, time["label"], time)
        upsert_source_record(case, "How an Alien Autopsy Hoax", {"citation": "Nathalie Lagerfeld, 'How an Alien Autopsy Hoax Captured the World's Imagination for a Decade,' TIME, 21 June 2016", "sourceType": "secondary-media-history", "provenance": "Public TIME retrospective of the film controversy and reported admission narrative", "locator": "https://time.com/4376871/alien-autopsy-hoax-history/", "sourceUrl": "https://time.com/4376871/alien-autopsy-hoax-history/", "supports": ["Documents the public media-hoax/provenance controversy", "Summarizes the reported Santilli/Shoefield restoration narrative and Humphreys production claim"], "limitations": ["Not the exact 2006 interview or transcript", "Not a broadcast master, production packet, or original film custody record"]})
    elif cid == "BF-SF-06":
        for rec in case.get("sourceRecords", []):
            if rec.get("sourceType") == "public-release-program-mirror":
                rec.update({"provenance": "Internet Archive public full-program mirror and metadata endpoint; public-mirror custody only.", "sourceUrl": "https://archive.org/details/area-51-the-alien-interview-1997"})
    elif cid == "BF-1987-GB-01":
        for rec in case.get("sourceRecords", []):
            if rec.get("sourceType") == "institutional-archive-finding-aid":
                rec["limitations"] = ["Finding aid does not display folder contents or identify original Walters media", "1990 folder title does not establish custody continuity from the 1987–1988 series", "Institutional folder custody does not authenticate depicted objects"]


def main() -> None:
    data = json.loads(DATA.read_text())
    cases = data["cases"]
    by_id = {case["id"]: case for case in cases}
    missing = sorted(set(SCOPE) - set(by_id))
    if missing:
        raise SystemExit(f"missing scoped cases: {missing}")
    if set(P) != set(SCOPE) or len(SCOPE) != 20:
        raise SystemExit("patch map must equal the exact 20-case scope")

    before = {case["id"]: deepcopy(case) for case in cases}
    for cid in SCOPE:
        case = by_id[cid]
        for key, value in P[cid].items():
            case[key] = deepcopy(value)
        apply_custom(case)

    after = {case["id"]: case for case in cases}
    changed = {cid for cid in after if after[cid] != before[cid]}
    if not changed <= set(SCOPE):
        raise SystemExit(f"out-of-scope changed-case boundary: {sorted(changed - set(SCOPE))}")
    if len(cases) != 155 or len(data.get("timeline", [])) != 153:
        raise SystemExit("case/timeline cardinality changed")

    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "PASS", "alreadyApplied": not changed, "changedCaseIds": sorted(changed), "scopeCaseIds": SCOPE, "cases": len(cases), "timeline": len(data.get("timeline", []))}, indent=2))


if __name__ == "__main__":
    main()
