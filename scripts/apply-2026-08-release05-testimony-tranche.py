#!/usr/bin/env python3
"""Admit four explicitly lower-confidence Release 05 testimony cases.

The tranche preserves official-record custody while refusing to treat FBI interview
records or witness reconstructions as FBI confirmation, sensor corroboration, or
proof of a shared triangle phenomenon.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas-data.json"
MANIFEST = ROOT / "public-source-manifest.json"
INDEX = ROOT / "source-file-index.json"
LEDGER = ROOT / "research/pursue-release05-intake-ledger.json"
REVIEW = ROOT / "research/pursue-release05-new-case-admission-review.md"
REPORT = ROOT / "research/pursue-release05-lower-confidence-testimony-tranche.md"
WAR = "https://www.war.gov/UFO/?releaseDate=Release+05&release=05"


def load(path: Path):
    return json.loads(path.read_text())


def dump(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def source_record(identifier, title, sha256, pages, supports, limitations, reconstruction=False):
    if reconstruction:
        return {
            "citation": f"{identifier} · FBI-released witness reconstruction accompanying {title}",
            "sourceType": "official-digital-rendering-reconstruction",
            "provenance": "Exact reconstruction published by the U.S. Department of War in PURSUE Release 05; original local file hash-verified against the retained download",
            "locator": identifier,
            "url": WAR,
            "sha256": sha256,
            "sourcePageImages": pages,
            "supports": ["Preserves a released visual reconstruction of the witness description"],
            "limitations": ["Witness reconstruction only; not event photography, sensor data, independent corroboration, or an FBI factual conclusion"],
        }
    return {
        "citation": f"FBI FD-302 interview record concerning {title}, {identifier}",
        "sourceType": "primary-official-witness-interview-record",
        "provenance": "Exact PDF published by the U.S. Department of War in PURSUE Release 05; full local copy hash-verified against the retained download",
        "locator": identifier + (" · PDF p. 3" if identifier == "FBI-UAP-D024" else " · PDF pp. 1–3" if identifier == "FBI-UAP-D026" else " · PDF pp. 1–2"),
        "url": WAR,
        "sha256": sha256,
        "sourcePageImages": pages,
        "supports": supports,
        "limitations": limitations,
    }


def public_source(ids):
    return [{
        "label": "War.gov — PURSUE Release 05",
        "url": WAR,
        "publisher": "U.S. Department of War",
        "access": "Public official release landing page",
        "scope": "official-release-custody",
        "note": f"Official custody page for {ids}. The FD-302 documents interview content and the paired visual is a witness reconstruction; neither constitutes FBI confirmation of the event.",
    }]


CASES = [
    {
        "id": "BF-2002-BG-01",
        "title": "Bagram Silent Triangle Report",
        "date": "JUN 2002",
        "year": 2002,
        "location": "Bagram Air Base, Afghanistan",
        "mode": "approximate",
        "lon": 69.2649,
        "lat": 34.9461,
        "expectedCountry": "Afghanistan",
        "geometryExpectation": "country",
        "coordinatePrecision": "facility-centroid-approximate",
        "coordinateBasis": "Bagram Air Base representative point; the released interview identifies Bagram but provides no exact observer position",
        "agency": "FBI",
        "domain": "GOVERNMENT / INSTITUTIONAL",
        "status": "DOCUMENTED TESTIMONY · UNRESOLVED",
        "confidence": "OFFICIAL INTERVIEW RECORD · LOWER-CONFIDENCE TESTIMONY",
        "summary": "An FBI FD-302 entered in 2024 records a reservist pilot's recollection of a June 2002 pre-dawn observation at Bagram. The witness said stars were obscured as a very large, silent triangular form moved west to east; a second pilot reportedly saw the passage and reacted immediately. The account was recorded roughly 22 years later, and the released packet contains no contemporaneous report, native imagery, measurement data, or separately released interview of the second pilot.",
        "keyFact": "The source establishes that the FBI documented the pilot's retrospective account—not that the FBI confirmed a 500-foot object moving at 150 knots.",
        "official": "The FD-302 explicitly contains neither recommendations nor conclusions of the FBI. D025 is a witness reconstruction and not event imagery.",
        "gap": "Missing are a contemporaneous report, independently released second-pilot statement, operational logs, radar or sensor records, precise observer geometry, native imagery, and analytical disposition.",
        "whyItMatters": "It preserves a reported two-observer military-aviator encounter at Bagram while illustrating the severe evidentiary limits of a decades-later official interview record.",
        "sources": ["FBI-UAP-D024 · retrospective FD-302 account", "FBI-UAP-D025 · witness reconstruction"],
        "sourceLabel": "FBI FD-302 / witness reconstruction",
        "sourceLocator": "FBI-UAP-D024",
        "relatedCaseIds": ["BF-2026-RL-01"],
        "keyQuote": "It appeared as if something huge went overhead, from west to east, and was an equilateral triangle shape.",
        "quoteSource": "FBI-UAP-D024, FD-302 continuation, PDF p. 3",
        "quoteConfidence": "High transcription confidence for the recorded interview wording; independent event verification is unavailable because the account was recorded roughly 22 years later.",
        "heroFact": "The released visual is a reconstruction of the witness account—not a photograph of the reported object.",
        "significance": "Lower-confidence testimony",
        "sourceQuality": "One retrospective official witness-interview record plus one released reconstruction; no independently released contemporaneous or sensor evidence.",
        "image": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg",
        "images": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D024-pdf-page-003.png"],
        "caseTypes": ["witness-report"],
        "evidenceModes": ["retrospective-testimony", "witness-reconstruction"],
        "environment": ["terrestrial", "military-airfield"],
        "outcome": "unresolved",
        "confidenceModel": {"record": "confirmed", "anomaly": "undetermined", "provenance": "primary-source"},
        "temporal": {"dateLabel": "JUN 2002", "year": 2002, "startDateTime": None, "endDateTime": None, "timezone": "Afghanistan local time", "timeOfDay": "approximately 04:30 local", "durationSeconds": None, "precision": "month/time-of-night", "eventForm": "single-event"},
        "geospatial": {"geometry": {"type": "Point", "coordinates": [69.2649, 34.9461]}, "role": "representative-centroid", "precision": "facility-centroid-approximate", "uncertaintyKm": 8, "basis": "Bagram Air Base representative point; exact observer position is not public"},
        "sourceRecords": [
            source_record("FBI-UAP-D024", "the Bagram 2002 triangle report", "949c9dc80fb247c6ea12d6750cebe629f00c37930f9572a9d0ef43365d5d4489", ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D024-pdf-page-003.png"], ["Records the primary witness's description of a silent west-to-east passage that obscured stars", "Records that a second pilot reportedly observed the same passage and reacted immediately"], ["Interviewed roughly 22 years after the event", "Estimated size and speed were subjective; the witness said the full shape could not be seen", "The second pilot is not independently interviewed in the released packet", "An FD-302 records interview content; it is not an FBI factual finding"]),
            source_record("FBI-UAP-D025", "the Bagram 2002 triangle report", "52c2fd0e4306488e6d7e1c682d0c5ee97ba1b9294774bea8617fc8fc7113e6b6", ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg"], [], [], True),
        ],
        "phenomena": {"shapes": ["triangle"], "objectCount": 1, "luminosity": "none reported", "motion": ["west-to-east", "steady", "silent"], "effects": ["reported-star-obscuration"]},
        "observation": {"witnessCount": 2, "witnessRoles": ["reservist pilot interviewed retrospectively", "second pilot reported through primary witness"], "sensors": ["unaided visual"], "durationSeconds": None, "independentWitnessGroups": 1},
        "taxonomyOriginal": {"domain": "WITNESS NARRATIVE", "status": "UNRESOLVED", "confidence": "LOWER-CONFIDENCE TESTIMONY"},
        "taxonomyVersion": "atlas-controlled-v1",
        "heroVisual": {"src": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg", "mediaType": "image", "visualType": "official-witness-reconstruction", "caption": "FBI-released digital rendering accompanying the Bagram witness account.", "provenance": "FBI-UAP-D025, released through PURSUE Release 05", "evidenceStatus": "Witness reconstruction only; not event imagery or independent corroboration.", "isEventEvidence": False},
        "publicSources": public_source("FBI-UAP-D024 and D025"),
        "evidenceBoundary": {"established": ["An official FD-302 records a pilot's retrospective account of a June 2002 Bagram observation.", "The account says a second pilot also observed the passage.", "A released digital rendering illustrates the primary witness's description."], "notEstablished": ["That a 500-foot object traveled at 150 knots; both figures were subjective estimates.", "The identity, altitude, physical dimensions, origin, or extraordinary performance of the reported form.", "Independent confirmation by the second pilot, sensors, contemporaneous records, or the FBI.", "A relationship to the other testimony cases or a common triangle phenomenon.", "That D025 is a photograph or sensor product."], "competingExplanations": ["Aircraft or formation misperception, cloud or atmospheric obscuration, dark-adaptation and geometry errors, memory reconstruction over two decades, and an unresolved physical object remain possible."]},
    },
    {
        "id": "BF-2023-CST-01",
        "title": "Colorado Springs Translucent Triangle Report",
        "date": "OCT 2023",
        "year": 2023,
        "location": "Colorado Springs, Colorado",
        "mode": "approximate",
        "lon": -104.8214,
        "lat": 38.8339,
        "expectedCountry": "United States of America",
        "expectedAdmin1": "Colorado",
        "geometryExpectation": "admin1",
        "coordinatePrecision": "city-centroid-redacted-address",
        "coordinateBasis": "Colorado Springs city centroid; the residence address and exact October date are redacted",
        "agency": "FBI",
        "domain": "GOVERNMENT / INSTITUTIONAL",
        "status": "DOCUMENTED TESTIMONY · UNRESOLVED",
        "confidence": "OFFICIAL INTERVIEW RECORD · LOWER-CONFIDENCE TESTIMONY",
        "summary": "A 2026 FBI FD-302 records two witnesses' October 2023 report of a silent triangular form passing over their Colorado Springs residence for about four seconds. The primary witness described an almost translucent silhouette, surrounding haze or distortion, a silver-blue trailing band, and a rapid bank toward vertical without an apparent course change. Estimated altitude and size were subjective; the packet contains no native image, sensor data, or independent technical corroboration.",
        "keyFact": "The witnesses reportedly separated before comparing recollections, but both accounts remain part of one retrospective household witness group rather than independent sensor confirmation.",
        "official": "The FBI documented the interview. It did not confirm the reported object's properties, and D027 is a witness reconstruction only.",
        "gap": "Missing are exact event date/address, native imagery, aviation or weather correlation, measured geometry, contemporaneous reports, independent sensor data, and FBI analytical disposition.",
        "whyItMatters": "The record preserves a short-duration two-witness account with a released reconstruction while remaining distinct from the 2022 Cheyenne Mountain case and the separate 2023 red-light report.",
        "sources": ["FBI-UAP-D026 · FD-302", "FBI-UAP-D027 · witness reconstruction"],
        "sourceLabel": "FBI FD-302 / witness reconstruction",
        "sourceLocator": "FBI-UAP-D026",
        "relatedCaseIds": ["BF-2022-CS-01", "BF-2023-CSR-01"],
        "keyQuote": "When first spotted the UAP he thought it appeared almost see-through, and it had what appeared to be a haze or distortion around it.",
        "quoteSource": "FBI-UAP-D026, FD-302 continuation, PDF p. 2",
        "quoteConfidence": "High for the recorded witness wording; event interpretation remains uncorroborated.",
        "heroFact": "The four-second event has two reported witnesses; D027 is a witness reconstruction, not event imagery, and no native sensor record is released.",
        "significance": "Lower-confidence testimony",
        "sourceQuality": "One official household-witness interview record and one reconstruction; retrospective, short-duration, and without independent sensor corroboration.",
        "image": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg",
        "images": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-001.png", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-002.png", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-003.png"],
        "caseTypes": ["witness-report"], "evidenceModes": ["retrospective-testimony", "witness-reconstruction"], "environment": ["terrestrial", "residential"], "outcome": "unresolved",
        "confidenceModel": {"record": "confirmed", "anomaly": "undetermined", "provenance": "primary-source"},
        "temporal": {"dateLabel": "OCT 2023", "year": 2023, "startDateTime": None, "endDateTime": None, "timezone": "MDT", "timeOfDay": "approximately 22:50", "durationSeconds": 4, "precision": "redacted-day/minute-reported", "eventForm": "single-event"},
        "geospatial": {"geometry": {"type": "Point", "coordinates": [-104.8214, 38.8339]}, "role": "representative-centroid", "precision": "city-centroid-redacted-address", "uncertaintyKm": 25, "basis": "Colorado Springs city centroid; exact residence is redacted"},
        "sourceRecords": [
            source_record("FBI-UAP-D026", "the Colorado Springs translucent-triangle report", "a6eb053699dcf7c2fdfe2d37bd4be8ef980c58e3f5595c7bee41ab1f7450bfe0", [f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-{p:03d}.png" for p in (1,2,3)], ["Records a roughly four-second two-witness observation over a Colorado Springs residence", "Preserves descriptions of silence, apparent translucency or distortion, a trailing silver-blue band and unusual banking"], ["Interview occurred in 2026, more than two years after the event", "Altitude, size and appearance are subjective estimates", "No native image, sensor data, technical verification, or independent analytical conclusion is included", "An FD-302 records interview content; it is not an FBI factual finding"]),
            source_record("FBI-UAP-D027", "the Colorado Springs translucent-triangle report", "207f31090a4f187a365c552d45b1e0f3eb2aa47541dd9a8b0d1f7b5769c5d0ab", ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg"], [], [], True),
        ],
        "phenomena": {"shapes": ["triangle"], "objectCount": 1, "luminosity": "silver-blue trailing band reported", "motion": ["northeast-to-southwest", "fast", "banked-near-vertical"], "effects": ["reported-haze-or-distortion"]},
        "observation": {"witnessCount": 2, "witnessRoles": ["primary residential witness", "spouse witness"], "sensors": ["unaided visual"], "durationSeconds": 4, "independentWitnessGroups": 1},
        "taxonomyOriginal": {"domain": "WITNESS NARRATIVE", "status": "UNRESOLVED", "confidence": "LOWER-CONFIDENCE TESTIMONY"}, "taxonomyVersion": "atlas-controlled-v1",
        "heroVisual": {"src": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg", "mediaType": "image", "visualType": "official-witness-reconstruction", "caption": "FBI-released digital rendering accompanying the translucent-triangle account.", "provenance": "FBI-UAP-D027, released through PURSUE Release 05", "evidenceStatus": "Witness reconstruction only; not event imagery or independent corroboration.", "isEventEvidence": False},
        "publicSources": public_source("FBI-UAP-D026 and D027"),
        "evidenceBoundary": {"established": ["An official FD-302 records two household witnesses' retrospective account of an October 2023 observation.", "The primary account reports a four-second silent triangular passage with distortion-like appearance.", "A released visual illustrates the witness description."], "notEstablished": ["Measured altitude, dimensions, speed, bank angle, translucency, propulsion, or extraordinary performance.", "Independent confirmation outside the household witness group or by sensors.", "A relationship to BF-2022-CS-01, BF-2023-CSR-01, or a common triangle phenomenon.", "That D027 is event imagery or an FBI-confirmed depiction."], "competingExplanations": ["Aircraft or UAS viewed under poor geometry, atmospheric haze, visual persistence or contrast effects, memory reconstruction, and an unresolved physical object remain possible."]},
    },
    {
        "id": "BF-2011-DT-01",
        "title": "Large Dark Triangle with Lights Report",
        "date": "JUN–JUL 2011",
        "year": 2011,
        "location": "United States [REDACTED]",
        "mode": "redacted",
        "lon": -98.5, "lat": 39.8, "expectedCountry": "United States of America", "geometryExpectation": "country",
        "coordinatePrecision": "country-redacted-generalized", "coordinateBasis": "Map-only generalized continental U.S. centroid; the released interview redacts the event location",
        "agency": "FBI", "domain": "GOVERNMENT / INSTITUTIONAL", "status": "DOCUMENTED TESTIMONY · UNRESOLVED", "confidence": "OFFICIAL INTERVIEW RECORD · LOWER-CONFIDENCE TESTIMONY",
        "summary": "A 2025 FBI FD-302 records two interviewees' recollection of a June or July 2011 nighttime event at a redacted U.S. location. They described a large, low, dark triangular form with three recessed diffuse white corner lights moving north for 10–15 seconds with a low pulsing hum. A third person was reportedly present, but the released record contains no native video, contemporaneous report, exact location, or independent sensor corroboration.",
        "keyFact": "Reported dimensions of roughly 200 by 100 feet and altitude near 800 feet were witness estimates made years later, not measured values.",
        "official": "The FBI documented retrospective interviews; the form contains no FBI recommendation or conclusion. D029 is a reconstruction rather than event imagery.",
        "gap": "Missing are exact location/date, contemporaneous reports, native media, a released third-witness statement, measured geometry, environmental and aviation correlation, sensor records, and analytical disposition.",
        "whyItMatters": "The record preserves a multi-person account with unusual size and sound descriptions while remaining a lower-confidence retrospective testimony case.",
        "sources": ["FBI-UAP-D028 · FD-302", "FBI-UAP-D029 · witness reconstruction"], "sourceLabel": "FBI FD-302 / witness reconstruction", "sourceLocator": "FBI-UAP-D028", "relatedCaseIds": ["BF-2026-RL-01"],
        "keyQuote": "The object had a car-sized white light in each of its three corners that emitted a diffuse glow and were recessed back a bit from the corners.", "quoteSource": "FBI-UAP-D028, FD-302 continuation, PDF p. 2", "quoteConfidence": "High for the recorded witness wording; dimensions, altitude and event interpretation remain unverified.",
        "heroFact": "D029 is a witness reconstruction, not event imagery; two witnesses were interviewed, the location is redacted, and no native video was captured.", "significance": "Lower-confidence testimony", "sourceQuality": "One official retrospective multi-witness interview record plus one reconstruction; no contemporaneous or sensor evidence.",
        "image": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg", "images": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D028-pdf-page-001.png", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D028-pdf-page-002.png"],
        "caseTypes": ["witness-report"], "evidenceModes": ["retrospective-testimony", "witness-reconstruction"], "environment": ["terrestrial", "residential"], "outcome": "unresolved", "confidenceModel": {"record": "confirmed", "anomaly": "undetermined", "provenance": "primary-source"},
        "temporal": {"dateLabel": "JUN–JUL 2011", "year": 2011, "startDateTime": None, "endDateTime": None, "timezone": None, "timeOfDay": "about 20:00–21:00", "durationSeconds": None, "durationRangeSeconds": [10, 15], "precision": "month-range/time-range", "eventForm": "single-event"},
        "geospatial": {"geometry": {"type": "Point", "coordinates": [-98.5,39.8]}, "role": "representative-centroid", "precision": "country-redacted-generalized", "uncertaintyKm": 2000, "basis": "Map-only generalized continental U.S. centroid; exact event location is redacted"},
        "sourceRecords": [
            source_record("FBI-UAP-D028", "the 2011 large dark triangle report", "6a1c229de51ed47cff5de843b0cc4592e1ff691f1ed20254ada15d267e0942bb", [f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D028-pdf-page-{p:03d}.png" for p in (1,2)], ["Records two interviewees' descriptions of a large dark triangular form with three diffuse corner lights", "Records a 10–15-second northbound passage and a low pulsing hum"], ["Interviews occurred in 2025, approximately 14 years after the event", "Exact location and date are redacted or uncertain", "Size and altitude are subjective estimates", "No native video, contemporaneous report, released third-witness interview, or independent sensor evidence is included", "An FD-302 records interview content; it is not an FBI factual finding"]),
            source_record("FBI-UAP-D029", "the 2011 large dark triangle report", "465e4e3ff6d3e49a2b6891326e5d537f4ce7d3c406b8c8cf3271d9bde04e36db", ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg"], [], [], True),
        ],
        "phenomena": {"shapes": ["triangle"], "objectCount": 1, "luminosity": "three diffuse white corner lights", "motion": ["northbound", "slow", "steady"], "effects": ["reported-low-pulsing-hum"]},
        "observation": {"witnessCount": 3, "witnessRoles": ["two witnesses interviewed in one FD-302", "third person reported present"], "sensors": ["unaided visual", "auditory"], "durationSeconds": None, "durationRangeSeconds": [10, 15], "independentWitnessGroups": 1},
        "taxonomyOriginal": {"domain": "WITNESS NARRATIVE", "status": "UNRESOLVED", "confidence": "LOWER-CONFIDENCE TESTIMONY"}, "taxonomyVersion": "atlas-controlled-v1",
        "heroVisual": {"src": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg", "mediaType": "image", "visualType": "official-witness-reconstruction", "caption": "FBI-released digital rendering accompanying the 2011 witness account.", "provenance": "FBI-UAP-D029, released through PURSUE Release 05", "evidenceStatus": "Witness reconstruction only; not event imagery or independent corroboration.", "isEventEvidence": False},
        "publicSources": public_source("FBI-UAP-D028 and D029"),
        "evidenceBoundary": {"established": ["An official FD-302 records two interviewees' retrospective account of a 2011 event.", "The account reports a dark triangular form, three lights, and a pulsing hum.", "A released visual illustrates the witness description."], "notEstablished": ["Measured dimensions, altitude, speed, identity, origin, or extraordinary performance.", "Independent confirmation by the reported third person, contemporaneous records, sensors, or the FBI.", "A relationship to other triangle reports or a common phenomenon.", "That D029 is event imagery."], "competingExplanations": ["Aircraft or formation lights, UAS, low-frequency environmental sound, geometry and size misperception, memory reconstruction over 14 years, and an unresolved physical object remain possible."]},
    },
    {
        "id": "BF-2023-CSR-01",
        "title": "Colorado Springs Red-Light Triangle Report",
        "date": "OCT 2023", "year": 2023, "location": "Colorado Springs, Colorado", "mode": "approximate", "lon": -104.8214, "lat": 38.8339,
        "expectedCountry": "United States of America", "expectedAdmin1": "Colorado", "geometryExpectation": "admin1", "coordinatePrecision": "city-centroid-redacted-worksite", "coordinateBasis": "Colorado Springs city centroid; exact worksite and October date are redacted",
        "agency": "FBI", "domain": "GOVERNMENT / INSTITUTIONAL", "status": "DOCUMENTED TESTIMONY · UNRESOLVED", "confidence": "OFFICIAL INTERVIEW RECORD · LOWER-CONFIDENCE TESTIMONY",
        "summary": "A 2025 FBI FD-302 records a single witness's October 2023 report of a large dark equilateral triangle emerging from an apparently distorted cloud over Colorado Springs, with diffuse red lights at its corners. The witness estimated rapid acceleration, unusual banking, and later phone-call distortion. Those size, altitude, speed and interference claims are subjective and technically unverified; the released packet contains no native event media or independent sensor corroboration.",
        "keyFact": "The reported Mach 1–2 speed, 3,000–5,000-foot altitude, parking-lot scale and phone interference are witness estimates or recollections—not measurements established by the FBI record.",
        "official": "The FBI documented one retrospective interview and released a reconstruction. Neither constitutes factual confirmation or calibrated performance evidence.",
        "gap": "Missing are exact date/worksite, native imagery, independent witnesses, phone records or RF analysis, measured geometry, aviation/weather correlation, sensor data, and FBI analytical disposition.",
        "whyItMatters": "The case preserves a detailed modern report and reconstruction while demonstrating why spectacular performance claims require measurement and independent corroboration.",
        "sources": ["FBI-UAP-D030 · FD-302", "FBI-UAP-D031 · witness reconstruction"], "sourceLabel": "FBI FD-302 / witness reconstruction", "sourceLocator": "FBI-UAP-D030", "relatedCaseIds": ["BF-2022-CS-01", "BF-2023-CST-01"],
        "keyQuote": "It then almost instantaneously accelerated to possibly Mach 1 or 2.", "quoteSource": "FBI-UAP-D030, FD-302 continuation, PDF p. 2", "quoteConfidence": "High for the recorded witness wording; the estimate was not independently measured or technically verified.",
        "heroFact": "D031 is a witness reconstruction, not event imagery; no event photograph or technical phone-interference record is released.", "significance": "Lower-confidence testimony", "sourceQuality": "One official retrospective witness interview plus one reconstruction; no independent witness, native media, sensor or technical corroboration.",
        "image": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg", "images": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D030-pdf-page-001.png", "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D030-pdf-page-002.png"],
        "caseTypes": ["witness-report"], "evidenceModes": ["retrospective-testimony", "witness-reconstruction"], "environment": ["terrestrial", "urban"], "outcome": "unresolved", "confidenceModel": {"record": "confirmed", "anomaly": "undetermined", "provenance": "primary-source"},
        "temporal": {"dateLabel": "OCT 2023", "year": 2023, "startDateTime": None, "endDateTime": None, "timezone": "MDT", "timeOfDay": "between 20:00 and 21:30", "durationSeconds": None, "precision": "redacted-day/time-range", "eventForm": "single-event"},
        "geospatial": {"geometry": {"type": "Point", "coordinates": [-104.8214,38.8339]}, "role": "representative-centroid", "precision": "city-centroid-redacted-worksite", "uncertaintyKm": 25, "basis": "Colorado Springs city centroid; exact worksite is redacted"},
        "sourceRecords": [
            source_record("FBI-UAP-D030", "the Colorado Springs red-light triangle report", "1ac0068c5a4f77c1bb2029971fc5e768d84ea921e3ac3122701746e548b12f06", [f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D030-pdf-page-{p:03d}.png" for p in (1,2)], ["Records a single witness's description of a large dark triangle with three diffuse red corner lights", "Records reported acceleration, unconventional banking and later apparent phone-call distortion"], ["Single retrospective witness interviewed in 2025", "Size, altitude, speed and bank angle are subjective estimates", "No native event media, independent witness, phone/RF record, or sensor data is included", "An FD-302 records interview content; it is not an FBI factual finding"]),
            source_record("FBI-UAP-D031", "the Colorado Springs red-light triangle report", "33f6602ddc5c73a5b2e7ee1898ef5b51dc895e31ab27e0d2f15eab17c10461bc", ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg"], [], [], True),
        ],
        "phenomena": {"shapes": ["triangle"], "objectCount": 1, "luminosity": "three diffuse red corner lights", "motion": ["southbound", "reported-rapid-acceleration", "reported-opposite-bank"], "effects": ["reported-phone-call-distortion", "reported-visual-distortion"]},
        "observation": {"witnessCount": 1, "witnessRoles": ["civilian witness"], "sensors": ["unaided visual"], "durationSeconds": None, "independentWitnessGroups": 1},
        "taxonomyOriginal": {"domain": "WITNESS NARRATIVE", "status": "UNRESOLVED", "confidence": "LOWER-CONFIDENCE TESTIMONY"}, "taxonomyVersion": "atlas-controlled-v1",
        "heroVisual": {"src": "assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg", "mediaType": "image", "visualType": "official-witness-reconstruction", "caption": "FBI-released digital rendering accompanying the red-light triangle account.", "provenance": "FBI-UAP-D031, released through PURSUE Release 05", "evidenceStatus": "Witness reconstruction only; not event imagery or independent corroboration.", "isEventEvidence": False},
        "publicSources": public_source("FBI-UAP-D030 and D031"),
        "evidenceBoundary": {"established": ["An official FD-302 records one witness's retrospective account of an October 2023 event.", "The account reports a large triangular form, three red lights, unusual motion and later call distortion.", "A released visual illustrates the witness description."], "notEstablished": ["Mach-level speed, altitude, dimensions, bank angle, phone interference, identity, origin, or extraordinary performance.", "Independent confirmation by another witness, technical records, sensors, or the FBI.", "A relationship to BF-2022-CS-01, BF-2023-CST-01, or a common triangle phenomenon.", "That D031 is event imagery."], "competingExplanations": ["Aircraft or UAS, atmospheric cloud and contrast effects, geometry and speed misperception, ordinary call degradation, memory reconstruction, and an unresolved physical object remain possible."]},
    },
]

TIMELINE = [
    {"id": "TL-2002-BG-TRIANGLE", "year": 2002, "date": "JUN 2002", "type": "incident", "caseId": "BF-2002-BG-01", "title": "Bagram silent triangle report", "desc": "A later FBI interview records a reservist pilot's report of a large silent triangular form passing over Bagram, with a second pilot reportedly present."},
    {"id": "TL-2011-DT-LIGHTS", "year": 2011, "date": "JUN–JUL 2011", "type": "incident", "caseId": "BF-2011-DT-01", "title": "Large dark triangle with lights report", "desc": "A 2025 FBI interview records a multi-person retrospective account of a low dark triangle with three lights and a pulsing hum at a redacted U.S. location."},
    {"id": "TL-2023-CST", "year": 2023, "date": "OCT 2023", "type": "incident", "caseId": "BF-2023-CST-01", "title": "Colorado Springs translucent triangle report", "desc": "A 2026 FBI interview records two household witnesses' four-second report of a silent distortion-shrouded triangular form."},
    {"id": "TL-2023-CSR", "year": 2023, "date": "OCT 2023", "type": "incident", "caseId": "BF-2023-CSR-01", "title": "Colorado Springs red-light triangle report", "desc": "A 2025 FBI interview records one witness's report of a large triangular form with three red lights and subjectively estimated rapid acceleration."},
]

atlas = load(ATLAS)
case_ids = {c["id"] for c in atlas["cases"]}
new_ids = {c["id"] for c in CASES}
if case_ids & new_ids and not new_ids.issubset(case_ids):
    raise SystemExit("Refusing partial testimony-tranche state")
if not (case_ids & new_ids):
    if len(atlas["cases"]) != 151:
        raise SystemExit(f"Expected 151-case closure baseline, got {len(atlas['cases'])}")
    atlas["cases"].extend(CASES)
else:
    replacements = {c["id"]: c for c in CASES}
    atlas["cases"] = [replacements.get(c["id"], c) for c in atlas["cases"]]

timeline_ids = {t["id"] for t in atlas["timeline"]}
for row in TIMELINE:
    if row["id"] not in timeline_ids:
        atlas["timeline"].append(row)
dump(ATLAS, atlas)

manifest = load(MANIFEST)
for c in CASES:
    manifest[c["id"]] = c["publicSources"]
dump(MANIFEST, manifest)

index = load(INDEX)
index_rows = {
    "FBI-UAP-D024": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D024-pdf-page-003.png", WAR],
    "FBI-UAP-D024 · PDF p. 3": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D024-pdf-page-003.png", WAR],
    "FBI-UAP-D025": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D025-witness-reconstruction.jpg", WAR],
    "FBI-UAP-D026": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-{p:03d}.png" for p in (1,2,3)], WAR],
    "FBI-UAP-D026 · PDF pp. 1–3": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D026-pdf-page-{p:03d}.png" for p in (1,2,3)], WAR],
    "FBI-UAP-D027": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D027-witness-reconstruction.jpg", WAR],
    "FBI-UAP-D028": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D028-pdf-page-{p:03d}.png" for p in (1,2)], WAR],
    "FBI-UAP-D028 · PDF pp. 1–2": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D028-pdf-page-{p:03d}.png" for p in (1,2)], WAR],
    "FBI-UAP-D029": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D029-witness-reconstruction.jpg", WAR],
    "FBI-UAP-D030": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D030-pdf-page-{p:03d}.png" for p in (1,2)], WAR],
    "FBI-UAP-D030 · PDF pp. 1–2": [*[f"assets/sources/PURSUE-RELEASE-05/FBI-UAP-D030-pdf-page-{p:03d}.png" for p in (1,2)], WAR],
    "FBI-UAP-D031": ["assets/sources/PURSUE-RELEASE-05/FBI-UAP-D031-witness-reconstruction.jpg", WAR],
}
for key, value in index_rows.items():
    index[key] = value
dump(INDEX, index)

ledger = load(LEDGER)
map_by_identifier = {
    "FBI-UAP-D024": "BF-2002-BG-01", "FBI-UAP-D025": "BF-2002-BG-01",
    "FBI-UAP-D026": "BF-2023-CST-01", "FBI-UAP-D027": "BF-2023-CST-01",
    "FBI-UAP-D028": "BF-2011-DT-01", "FBI-UAP-D029": "BF-2011-DT-01",
    "FBI-UAP-D030": "BF-2023-CSR-01", "FBI-UAP-D031": "BF-2023-CSR-01",
}
for row in ledger["records"]:
    ident = row["filename"].split("_", 1)[0]
    if ident in map_by_identifier:
        row["atlasDisposition"] = "integrated-lower-confidence-testimony"
        row["atlasMappings"] = [map_by_identifier[ident]]
        row["boundary"] = "Official FBI interview record or paired witness reconstruction; admitted as lower-confidence testimony without independent sensor confirmation or cross-case phenomenon inference."
        if ident in {"FBI-UAP-D025", "FBI-UAP-D027", "FBI-UAP-D029", "FBI-UAP-D031"}:
            row["mediaBoundary"] = "Witness reconstruction/artwork, not a photograph, sensor product, or independent corroboration."
dump(LEDGER, ledger)

review = REVIEW.read_text()
review = review.replace("### 4. 2023 Colorado Springs dark translucent triangle — ADD IN TESTIMONY TRANCHE", "### 4. 2023 Colorado Springs dark translucent triangle — ADMITTED AS LOWER-CONFIDENCE TESTIMONY")
review = review.replace("### 5. 2002 Bagram silent triangle — ADD IN TESTIMONY TRANCHE", "### 5. 2002 Bagram silent triangle — ADMITTED AS LOWER-CONFIDENCE TESTIMONY")
review = review.replace("### 6. 2023 Colorado Springs large triangle with red lights — ADD IN TESTIMONY TRANCHE", "### 6. 2023 Colorado Springs large triangle with red lights — ADMITTED AS LOWER-CONFIDENCE TESTIMONY")
review = review.replace("### 7. 2011 large dark triangle — ADD IN TESTIMONY TRANCHE", "### 7. 2011 large dark triangle — ADMITTED AS LOWER-CONFIDENCE TESTIMONY")
REVIEW.write_text(review)

REPORT.write_text("""# PURSUE Release 05 lower-confidence testimony tranche

**Completed:** 2026-08-08
**Scope:** Four user-authorized testimony cases derived from FBI-UAP-D024–D031.

## Admissions

- `BF-2002-BG-01` — Bagram Silent Triangle Report
- `BF-2023-CST-01` — Colorado Springs Translucent Triangle Report
- `BF-2011-DT-01` — Large Dark Triangle with Lights Report
- `BF-2023-CSR-01` — Colorado Springs Red-Light Triangle Report

## Evidence boundary

All four dossiers are explicitly labeled lower-confidence testimony. The FBI records establish that interviews were documented, not that the reported facts were independently confirmed. D025, D027, D029 and D031 are witness reconstructions, not event imagery. Subjective size, altitude, speed and identity estimates are not measurements. The four admissions do not establish a common triangle phenomenon and do not increase Blackfile confidence in exotic technology or non-human origin.
""")

print("Applied Release 05 lower-confidence testimony tranche: 4 cases")
