#!/usr/bin/env python3
"""Apply the August 2026 exact-20 public acquisition audit tranche.

Public-only: no outreach, forms, accounts, purchases, records requests, or external writes.
This tranche records dated target-level dispositions so exhausted public paths are not
repeated, normalizes five legacy target lists, and adds only source layers recovered in
this pass. It does not alter case admission or anomaly/origin confidence.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "atlas-data.json"
AUDIT_DATE = "2026-08-08"
SCOPE = [
    "BF-1994-AR-01", "BF-SF-12", "BF-1975-TW-01", "BF-SF-13", "BF-1966-WS-01",
    "BF-1973-PG-01", "BF-1978-VL-01", "BF-1987-GB-01", "BF-2014-CH-01", "BF-SF-06",
    "BF-1933-MG-01", "BF-1965-KB-01", "BF-1996-VG-01", "BF-1997-PH-01", "BF-1944-FF-01",
    "BF-1990-CV-01", "BF-1978-KK-01", "BF-1980-CLD-01", "BF-2006-OH-01", "BF-2020-AS-01",
]


def target(target_type: str, description: str, status: str, result: str, *, locator: str | None = None) -> dict:
    out = {
        "targetType": target_type,
        "description": description,
        "status": status,
        "publicOnlyResult": result,
        "lastPublicAudit": AUDIT_DATE,
        "auditScope": "public-only",
    }
    if locator:
        out["locator"] = locator
    return out


NORMALIZED = {
    "BF-1965-KB-01": [
        target("agency-incident-and-recovery-records", "Underlying NASA, Army, USAF, local-response, recovery, or transport records specific to Kecksburg", "publicly-unavailable", "No contemporaneous agency incident/recovery/transport packet was recovered"),
        target("foia-litigation-and-search-record", "Complete Kean v. NASA litigation, post-settlement search, disclosure, and loss/destruction record packet", "partially-recovered", "Federal court opinion and a contemporaneous mirror of Leslie Kean's 2009 conclusion report are public; the complete NASA production and court docket are not mapped", locator="https://www.theufochronicles.com/2009/11/conclusion-of-nasa-lawsuit-concerning_10.html"),
    ],
    "BF-1997-PH-01": [
        target("guard-sortie-and-flare-records", "Maryland Air National Guard sortie and flare-expenditure records for March 13, 1997", "publicly-unavailable", "Official-site and public-web searches did not recover sortie, range, or flare-expenditure records"),
        target("range-faa-and-radar-records", "Barry M. Goldwater Range logs and contemporaneous FAA/radar records", "publicly-unavailable", "No event-specific official range, FAA, or radar packet was recovered"),
        target("original-video-and-witness-corpus", "Original full-resolution videos with custody and a time-synchronized witness corpus", "publicly-unavailable", "Public witness and media layers remain available, but no custody-complete synchronized corpus was recovered"),
    ],
    "BF-1990-CV-01": [
        target("original-photographic-material", "Original Calvine negatives and remaining reported photographic frames with first-generation custody", "publicly-unavailable", "The surviving public print and official handling record are mapped; original negatives and remaining frames were not recovered"),
        target("complete-mod-analysis-record", "Full-resolution MoD photographic-analysis attachments, routing records, and unwatermarked complete record pages", "partially-recovered", "TNA public-viewer pages 112-114 and the Sheffield Hallam analysis are mapped; full-resolution attachments and unwatermarked complete pages remain unavailable", locator="https://discovery.nationalarchives.gov.uk/details/r/C10130124"),
    ],
    "BF-1980-CLD-01": [
        target("court-origin-complete-file", "Complete federal court file and authenticated medical/legal exhibits for Cash v. United States", "partially-recovered", "The AFU/Quest mirror preserves a partial legal-file compilation and dismissal order; no complete court-origin docket or authenticated medical exhibits were recovered"),
        target("military-and-aviation-operations-records", "DoD, JAG, Army, Fort Hood, FAA, and unit flight-log records capable of testing the alleged CH-47 operation", "publicly-unavailable", "No event-specific official flight, unit, radar, or operations packet was recovered"),
    ],
    "BF-2006-OH-01": [
        target("native-faa-foia-production", "Complete FAA investigative and FOIA-production custody, including native tower recordings, NTAP radar files, and employee statements", "partially-recovered", "NARCAP TR-10 reproduces FAA facility records, transcripts, FOIA correspondence, and analyses of 13 NTAP files; the native audio/data production is not mapped", locator="https://www.narcap.org/s/NARCAP_TR-10.pdf"),
        target("complete-aviation-reconstruction", "Native weather, airport-operations, United Airlines, and time-synchronized witness records sufficient for a full aviation-event reconstruction", "publicly-unavailable", "No complete native United/airport operations and witness-custody packet was recovered"),
    ],
}

KECKSBURG_RECORD = {
    "citation": "Leslie Kean, 'The Conclusion of the NASA Lawsuit: Concerning the Kecksburg, PA UFO case of 1965' (November 2009 public mirror)",
    "sourceType": "first-party-author-conclusion-report-public-mirror",
    "provenance": "Contemporaneous public mirror of Leslie Kean's post-litigation conclusion report; not NASA-origin hosting or a complete court/NASA production",
    "locator": "https://www.theufochronicles.com/2009/11/conclusion-of-nasa-lawsuit-concerning_10.html",
    "supports": [
        "Records the author's account that the court-monitored post-settlement NASA search concluded in August 2009",
        "Provides a public conclusion layer for the FOIA litigation and search outcome",
        "Documents that the reported search did not produce a smoking-gun incident or recovery record",
    ],
    "limitations": [
        "Public mirror rather than the defunct original Coalition for Freedom of Information host",
        "Author report rather than NASA-origin production or a complete court docket",
        "Does not authenticate an anomalous object, recovery, transport, or non-human origin",
    ],
    "sourceUrl": "https://www.theufochronicles.com/2009/11/conclusion-of-nasa-lawsuit-concerning_10.html",
}
KECKSBURG_PUBLIC = {
    "label": "Leslie Kean — conclusion of the NASA Kecksburg lawsuit (2009 public mirror)",
    "url": "https://www.theufochronicles.com/2009/11/conclusion-of-nasa-lawsuit-concerning_10.html",
    "publisher": "Leslie Kean; public mirror by The UFO Chronicles",
    "access": "Public",
    "scope": "first-party-author-conclusion-report-public-mirror",
    "note": "Preserves the author's post-litigation conclusion report; not NASA-origin custody, a complete litigation file, or proof of recovery.",
}
CASH_CLAIMS_RECORD = {
    "citation": "CUFON — Cash/Landrum claims-for-damages document packet (public PDF mirror)",
    "sourceType": "public-mirror-partial-usaf-claims-records",
    "provenance": "CUFON PDF created in 2002 from documents it states were released by the U.S. Air Force in July 1993; public mirror, not Air Force-origin hosting or a complete claims/court file",
    "locator": "https://www.cufon.org/cufon/cashlanC.pdf",
    "supports": [
        "Preserves documents associated with claims filed through the Bergstrom AFB Staff Judge Advocate trail",
        "Provides an additional public record-copy layer distinct from the later federal litigation compilation",
    ],
    "limitations": [
        "Third-party public mirror with CUFON-supplied compilation context",
        "Not a complete Air Force claims file, court docket, hospital packet, or military-operations record",
        "Does not establish medical causation, object identity, or military responsibility",
    ],
    "sourceUrl": "https://www.cufon.org/cufon/cashlanC.pdf",
}
CASH_INTERVIEW_RECORD = {
    "citation": "CUFON — transcript of Bergstrom AFB interview of Betty Cash, Vickie Landrum, and Colby Landrum, 17 August 1981, parts 1–2",
    "sourceType": "public-transcript-mirror-of-reported-recording",
    "provenance": "CUFON transcription of a recording it states was provided by Betty Cash; public transcript mirror, not original audio or Air Force-origin transcript custody",
    "locator": "https://www.cufon.org/cufon/cashlani.htm",
    "supports": [
        "Preserves a detailed transcript attributed to the August 17, 1981 Bergstrom AFB Law Library interview",
        "Names the reported participants and records the witnesses' claims in an early post-event administrative setting",
    ],
    "limitations": [
        "Original or earliest-generation audio is not mapped",
        "CUFON states that the beginning of the recording is absent and makes no broader guarantee of transcript accuracy",
        "Witness statements and interviewer questions are not findings of medical causation, object identity, or military responsibility",
    ],
    "sourceUrl": "https://www.cufon.org/cufon/cashlani.htm",
    "continuationUrl": "https://www.cufon.org/cufon/cashlani2.htm",
}
CASH_PUBLIC = [
    {"access": "Public", "label": "CUFON — Cash/Landrum claims-for-damages document packet", "publisher": "Computer UFO Network", "scope": "public-claims-record-mirror", "url": "https://www.cufon.org/cufon/cashlanC.pdf", "note": "Partial public mirror of documents CUFON states were released by the Air Force; not a complete official claims, court, medical, or operations packet."},
    {"access": "Public", "label": "CUFON — Bergstrom AFB interview transcript, part 1", "publisher": "Computer UFO Network", "scope": "public-transcript-mirror", "url": "https://www.cufon.org/cufon/cashlani.htm", "note": "Transcript attributed to a recording supplied by Betty Cash; not original audio or Air Force-origin transcript custody."},
    {"access": "Public", "label": "CUFON — Bergstrom AFB interview transcript, part 2", "publisher": "Computer UFO Network", "scope": "public-transcript-mirror", "url": "https://www.cufon.org/cufon/cashlani2.htm", "note": "Continuation of the public transcript mirror; witness claims are not official findings."},
]
OHARE_FOIA_PUBLIC = {
    "access": "Public",
    "label": "GovernmentAttic — FAA FY2007 FOIA logs",
    "publisher": "GovernmentAttic mirror of FAA logs",
    "scope": "public-official-log-mirror",
    "url": "https://www.governmentattic.org/docs/FOIA_Logs_FAA_FY2007.pdf",
    "note": "Durable public locator for the already-mapped FAA FOIA-log family; not the native O'Hare tower audio, NTAP files, or complete FAA production.",
}


def append_unique(items: list, entry: dict, key: str) -> None:
    value = entry[key]
    for old in items:
        if isinstance(old, dict) and old.get(key) == value:
            old.update(deepcopy(entry))
            return
    items.append(deepcopy(entry))


def apply() -> None:
    data = json.loads(DATA.read_text())
    before = deepcopy(data)
    by_id = {case["id"]: case for case in data["cases"]}
    if len(SCOPE) != 20 or len(set(SCOPE)) != 20:
        raise SystemExit("exact-20 scope boundary failed")
    if not set(SCOPE) <= set(by_id):
        raise SystemExit("one or more scoped cases are absent")
    if len(data["cases"]) != 155 or len(data["timeline"]) != 153:
        raise SystemExit("155-case / 153-timeline boundary failed")

    for cid in SCOPE:
        case = by_id[cid]
        if cid in NORMALIZED:
            case["acquisitionTargets"] = deepcopy(NORMALIZED[cid])
        else:
            targets = case.get("acquisitionTargets") or []
            if not targets or not all(isinstance(item, dict) for item in targets):
                raise SystemExit(f"{cid}: expected structured acquisition targets")
            for item in targets:
                item["lastPublicAudit"] = AUDIT_DATE
                item["auditScope"] = "public-only"

    kecksburg = by_id["BF-1965-KB-01"]
    kecksburg["sourceQuality"] = "Verified federal-court custody for the NASA FOIA dispute, supplemented by a contemporaneous public mirror of Leslie Kean's 2009 post-litigation conclusion report. The court-monitored search outcome is documented, but the underlying contemporaneous incident, recovery, transport, and complete NASA production remain unrecovered."
    kecksburg["quoteConfidence"] = "High for the federal-court opinion; medium for the 2009 conclusion report because the accessible copy is a contemporaneous public mirror rather than the defunct original host. Neither layer authenticates the recovery narrative."
    kecksburg["gap"] = "The 2009 conclusion layer closes the basic litigation-outcome gap but not the evidence gap: original Army/local-response logs, NASA technical records tied to the event, complete disclosure/loss records, and any recovery or transport chain remain publicly unrecovered."
    append_unique(kecksburg.setdefault("sourceRecords", []), KECKSBURG_RECORD, "locator")
    append_unique(kecksburg.setdefault("publicSources", []), KECKSBURG_PUBLIC, "url")

    cash = by_id["BF-1980-CLD-01"]
    cash["sourceQuality"] = "Public document trail with three bounded mirror layers: the AFU/Quest partial federal legal-file compilation, CUFON's claims-for-damages packet, and CUFON's two-part transcript attributed to the August 17, 1981 Bergstrom AFB interview. These improve public legal/administrative record depth but are not a complete court-origin docket, authenticated hospital packet, native interview audio, or military-operations file."
    append_unique(cash.setdefault("sourceRecords", []), CASH_CLAIMS_RECORD, "locator")
    append_unique(cash.setdefault("sourceRecords", []), CASH_INTERVIEW_RECORD, "locator")
    for record in CASH_PUBLIC:
        append_unique(cash.setdefault("publicSources", []), record, "url")

    ohare = by_id["BF-2006-OH-01"]
    append_unique(ohare.setdefault("publicSources", []), OHARE_FOIA_PUBLIC, "url")

    after_by_id = {case["id"]: case for case in data["cases"]}
    changed = {cid for cid in after_by_id if before["cases"][list(by_id).index(cid)] != after_by_id[cid]}
    # Order-independent boundary verification.
    before_by_id = {case["id"]: case for case in before["cases"]}
    changed = {cid for cid in after_by_id if before_by_id[cid] != after_by_id[cid]}
    if changed and not changed <= set(SCOPE):
        raise SystemExit(f"changed-case boundary failed: {sorted(changed)}")
    if [case["id"] for case in before["cases"]] != [case["id"] for case in data["cases"]]:
        raise SystemExit("case identity/order changed")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"PASS: exact-20 acquisition audit applied; changed={len(changed)}; cases={len(data['cases'])}")


if __name__ == "__main__":
    apply()
