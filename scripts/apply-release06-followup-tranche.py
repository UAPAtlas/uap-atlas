#!/usr/bin/env python3
"""Apply scoped Release 06 follow-up tranche updates."""
from __future__ import annotations
import json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'atlas-data.json'
SRC_INDEX = ROOT / 'source-file-index.json'
PUB_MANIFEST = ROOT / 'public-source-manifest.json'
RENDER_SRC = Path('/tmp/uap-release06-pages')

SCOPE_EXISTING = {'BF-1952-TM-01', 'BF-2022-ME-01'}
ADD_IDS = {'BF-1950-OK-01', 'BF-2023-CO-LE-01'}
IMG_MAP = {
    'D105-p252-252.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D105-pdf-page-252.png',
    'D105-p253-253.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D105-pdf-page-253.png',
    'D102-p037-037.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-037.png',
    'D102-p038-038.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-038.png',
    'D102-p039-039.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-039.png',
    'D102-p113-113.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-113.png',
    'D102-p121-121.png': 'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-121.png',
    'D10-p001-1.png': 'assets/sources/PURSUE-RELEASE-01/DOW-UAP-D10-pdf-page-001.png',
    'D10-p006-6.png': 'assets/sources/PURSUE-RELEASE-01/DOW-UAP-D10-pdf-page-006.png',
}

def load(p):
    with open(p) as f: return json.load(f)
def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
def case(data, cid):
    return next(c for c in data['cases'] if c['id'] == cid)
def upsert_record(c, citation_starts, rec):
    records = c.setdefault('sourceRecords', [])
    records[:] = [r for r in records if not str(r.get('citation','')).startswith(citation_starts)]
    records.insert(0, rec)
def upsert_case(data, new):
    data['cases'] = [c for c in data['cases'] if c['id'] != new['id']] + [new]
def upsert_timeline(data, entry):
    data['timeline'] = [t for t in data.get('timeline', []) if t.get('caseId') != entry['caseId']] + [entry]
def add_unique(arr, vals):
    for v in vals:
        if v not in arr: arr.append(v)

def main():
    for src, rel in IMG_MAP.items():
        s = RENDER_SRC / src
        if s.exists():
            d = ROOT / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(s, d)
    data = load(DATA)
    before_ids = {c['id'] for c in data['cases']}

    tm = case(data, 'BF-1952-TM-01')
    tm['summary'] = ('Navy Chief Photographer Delbert Newhouse filmed about ten to twelve maneuvering white objects near Tremonton, Utah, on 2 July 1952. '
        'The Release 06 Blue Book packet preserves both the public-release memo and the technical disagreement: Navy/PIC analysis argued for self-luminous/light-source images under assumptions; Baker remained cautious; and a later Air Force press-room memo favored bird reflections/seagulls. Newhouse’s own statement did not provide measured range, speed, size, altitude or distance.')
    tm['keyFact'] = ('Release 06 D102 pp. 37–39 shows officials debating whether to release the movie without comment, avoid questions about the Navy report, or use a gulls/balloons line while additional tests remained possible; the same packet preserves Newhouse’s narrower unmeasured witness statement and later technical disagreement.')
    tm['heroFact'] = tm['keyFact']
    tm['sourceQuality'] = ('Exact NARA case-file and motion-picture custody with copy-generation evidence: D098 says the analyzed Utah film was a duplicate of a copy; the camera original and full laboratory ledger remain unlocated. Joined by D098 Navy/PIC analysis and Release 06 D102/D103/D104/D154 context. D102 deepens the record by showing public-information strategy, brightness-method objections, proposed gull/balloon tests, Newhouse’s unmeasured statement, and later Air Force bird-reflection language. It supports institutional process and analytical disagreement, not proof of an extraterrestrial coverup.')
    tm['gap'] = ('Primary gap: the first-generation 16 mm camera film, complete laboratory chain-of-custody/measurement worksheets, and reproducible range/brightness geometry needed to adjudicate Navy/PIC, Baker, and Air Force bird-reflection interpretations.')
    tm['sourceUpdateCard'] = {
        'title': 'Release 06 source update — public release vs. technical disagreement',
        'finding': 'D102 pp. 37–39 records Air Force concern that withholding reports could imply “hot” material, discussion of release without comment and avoiding questions about the Navy report, and alternatives including gulls/balloons language plus proposed additional testing.',
        'boundary': 'This is evidence of release-management and methodological disagreement. It does not prove that officials knew the objects were non-human or that any later seagull explanation was knowingly false.',
        'sourcePages': ['D102 pp. 37–39, 113, 121, 126–127']
    }
    upsert_record(tm, 'DOW-UAP-D102 focused follow-up', {
        'citation': 'DOW-UAP-D102 focused follow-up · Tremonton public-release memo, Newhouse statement, and Air Force seagull memo',
        'sourceType': 'primary-case-file-follow-up',
        'provenance': 'Department of War PURSUE Release 06',
        'locator': 'D102 PDF pp. 37–39, 113, 121, 126–127',
        'url': 'https://www.war.gov/UFO/?releaseDate=Release+06&release=06',
        'sourcePageImages': [IMG_MAP['D102-p037-037.png'], IMG_MAP['D102-p038-038.png'], IMG_MAP['D102-p039-039.png'], IMG_MAP['D102-p113-113.png'], IMG_MAP['D102-p121-121.png']],
        'supports': ['public-release memo language about “hot” material and risk of another flap', 'methodological objection to Navy brightness analysis and proposed gull/balloon tests', 'Newhouse statement that no range/speed/size/altitude/distance estimate was possible'],
        'limitations': ['does not recover native first-generation film', 'does not resolve Navy/PIC, Baker, and Air Force interpretive disagreement', 'supports public-information management and technical dispute, not an extraterrestrial finding']
    })

    me = case(data, 'BF-2022-ME-01')
    me['summary'] = ('Three source-specific May 2022 Middle East records are now separated inside this dossier: legacy D10 reports five UAPs observed over roughly four hours with possible-bird language; D106 reports periodic FMV/MTS observation of 1–2 m UAPs around 20:26Z/21:00Z; D109 reports a distinct 05:24Z–07:04Z affected observation period with similar 1–2 m and 80–180 mph language. Same region and shape family do not establish one continuous event.')
    me['keyFact'] = ('D10, D106, and D109 are related USCENTCOM Middle East mission records, but their object counts, timing and observation contexts differ; Atlas now treats their claims as source-specific observations rather than one merged event field.')
    me['heroFact'] = me['keyFact']
    me['observation'] = {
        'witnessCount': None,
        'witnessRoles': ['redacted USCENTCOM mission/reporting personnel'],
        'sensors': ['FMV/MTS feed or mission-report sensor context'],
        'durationSeconds': None,
        'independentWitnessGroups': None,
        'sourceSpecificObservations': [
            {'source': 'DOW-UAP-D10', 'objects': 'five objects reported', 'duration': 'roughly four hours reported', 'boundary': 'possible birds/identification uncertainty retained; native sensor file absent'},
            {'source': 'DOW-UAP-D106', 'timeUtc': 'around 20:26Z / 21:00Z', 'objects': 'multiple 1–2 m UAPs', 'reportedSpeed': '80–180 mph', 'boundary': 'altitude undetermined; not merged with D109'},
            {'source': 'DOW-UAP-D109', 'timeUtc': '05:24Z–07:04Z affected observation period', 'objects': 'sporadic 1–2 m UAPs', 'reportedSpeed': '80–180 mph', 'boundary': 'dust/return-to-POI context; not merged with D106'}
        ]
    }
    me['temporal'] = {'dateLabel': 'MAY 2022', 'year': 2022, 'precision': 'month', 'eventForm': 'related-source-family', 'sourceSpecificTimes': {'DOW-UAP-D106': 'around 20:26Z / 21:00Z', 'DOW-UAP-D109': '05:24Z–07:04Z'}}
    me['sourceQuality'] = 'Primary mission reports D10, D106 and D109; all performance values are source-reported/estimated from redacted mission context, with native FMV/WSV absent. Legacy unaided-visual/USAF missile-crew fields were removed because D10/D106/D109 do not support them.'
    me['sourceUpdateCard'] = {'title': 'Release 06 reconciliation — related reports, not one merged track', 'finding': 'D106 and D109 share 1–2 m / 80–180 mph language but have distinct times and report contexts; original D10 preserves separate legacy five-object/four-hour/possible-birds language.', 'boundary': 'Atlas keeps the reports in one related-family dossier but separates the source-specific observations. Same region/shape is not treated as proof of a single continuous event.', 'sourcePages': ['D10 pp. 1, 6', 'D106 pp. 1, 6', 'D109 pp. 1, 5–6']}
    upsert_record(me, 'DOW-UAP-D10 source-specific observation', {'citation': 'DOW-UAP-D10 source-specific observation · Middle East mission report, May 2022', 'sourceType': 'primary-military-mission-report', 'provenance': 'Department of War Release 01', 'locator': 'D10 PDF pp. 1, 6', 'sourcePageImages': [IMG_MAP['D10-p001-1.png'], IMG_MAP['D10-p006-6.png']], 'supports': ['legacy five-object / roughly four-hour observation language', 'official mission-report custody', 'possible-bird identification uncertainty retained'], 'limitations': ['native sensor file absent', 'redactions prevent independent reconstruction', 'does not support inherited USAF missile crew or unaided-visual fields']})

    ok = {
        'id': 'BF-1950-OK-01', 'title': 'Okinawa Object-in-Water Recovery Inquiry', 'date': 'NOV 1950', 'year': 1950, 'location': 'Okinawa, Japan (Oku/Hedo location unresolved)', 'mode': 'approximate', 'lon': 128.25, 'lat': 26.75, 'agency': 'USAF / ATIC', 'domain': 'AIR-SEA / RECOVERY INQUIRY', 'status': 'OFFICIAL INQUIRY · NO RECOVERY DOCUMENTED', 'confidence': 'CONFIRMED RECORD · WITNESS REPORT UNVERIFIED', 'summary': 'Release 06 D105 preserves an official inquiry into T/Sgt Emery Guzi’s report that an unidentified object had fallen into the sea near Okinawa in November 1950. The record asked whether the object could be located, recovered or examined, but turned on unresolved geography: shallow water near Oku versus much deeper water near Hedo/Redo Saki. No actual recovery or final disposition appears in the reviewed packet.', 'official': True, 'gap': 'Missing original interview/sketch, hydrographic/aeronautical enclosures, ATIC reinterview response and final disposition.', 'sources': ['DOW-UAP-D105 pp. 126, 252–253'], 'image': IMG_MAP['D105-p253-253.png'], 'keyFact': 'D105 pp. 252–253 documents a recovery-feasibility tasking for Guzi’s Okinawa object-in-water report; it does not document recovery.', 'heroFact': 'Official tasking asked if a reported object in the sea near Okinawa could be located/recovered, but the site was uncertain and no recovery result is present.', 'whyItMatters': 'It is a rare early official recovery-feasibility inquiry with a named witness and a specific missing follow-up chain.', 'sourceQuality': 'Primary official file pages; strong for existence of the inquiry and missing follow-up, weak for the reported object itself.', 'sourceLabel': 'DOW-UAP-D105 pp. 252–253', 'sourceLocator': 'DOW-UAP-D105-OKINAWA-1950', 'quoteConfidence':'Medium — selected wording is traceable to released official pages, but event interpretation remains witness-report only.', 'significance':'Adds an early official recovery-feasibility inquiry while preserving missing follow-up boundaries.', 'relatedCaseIds':['BF-1952-TM-01'], 'acquisitionTargets':[{'targetType':'original-interview-and-sketch','description':'Original Guzi interview, sketch/map/enclosures, or witness statement referenced by the Okinawa inquiry','status':'publicly-unavailable','publicOnlyResult':'Not present in reviewed Release 06 pages','lastPublicAudit':'2026-09-22','auditScope':'release06-public-pages'},{'targetType':'atic-follow-up-and-recovery-disposition','description':'ATIC reinterview response, map attachments, recovery attempt notes, or final disposition','status':'publicly-unavailable','publicOnlyResult':'No follow-up or recovery result located in the released packet','lastPublicAudit':'2026-09-22','auditScope':'release06-public-pages'}], 'confidenceModel': {'record':'official-record', 'anomaly':'low-witness-report-only', 'provenance':'primary-release-page'},  'caseTypes': ['case-record','recovery-inquiry','witness-report'], 'evidenceModes': ['official-document','witness-report'], 'environment': ['maritime'], 'outcome': 'no-recovery-documented; follow-up-missing', 'temporal': {'dateLabel': 'NOV 1950', 'year': 1950, 'precision': 'month', 'eventForm': 'single-report-with-follow-up-tasking'}, 'geospatial': {'basis': 'approximate Okinawa placeholder; released source itself flags Oku vs Hedo/Redo Saki uncertainty', 'precision': 'regional-island placeholder', 'geometry': {'type':'Point','coordinates':[128.25,26.75]}}, 'coordinateBasis': 'regional placeholder from source-stated Okinawa/Oku/Hedo uncertainty', 'coordinatePrecision': 'regional', 'geometryExpectation': 'region', 'sourceUpdateCard': {'title':'Release 06 admission — recovery inquiry, not recovered object', 'finding':'D105 pp. 252–253 asks ATIC to reinterrogate Guzi because recovery feasibility depended on whether the reported sea impact was near shallow Oku lagoon or deeper Hedo/Redo Saki.', 'boundary':'The packet does not include a recovery, object examination, reinterview answer or final evaluation.', 'sourcePages':['D105 pp. 252–253']}, 'sourceRecords': [{'citation':'DOW-UAP-D105 · Okinawa object-in-water recovery-feasibility correspondence', 'sourceType':'primary-official-correspondence', 'provenance':'Department of War PURSUE Release 06', 'locator':'PDF pp. 252–253 (related routing p. 126)', 'url':'https://www.war.gov/UFO/?releaseDate=Release+06&release=06', 'sourcePageImages':[IMG_MAP['D105-p252-252.png'], IMG_MAP['D105-p253-253.png']], 'supports':['named-witness report by T/Sgt Emery Guzi', 'official request to resolve location and recovery feasibility', 'geographical uncertainty between Oku lagoon and Hedo/Redo Saki'], 'limitations':['no original interview/sketch in packet', 'no hydrographic/aeronautical enclosures in packet', 'no recovery or final disposition documented']}], 'observation': {'witnessCount':1, 'witnessRoles':['T/Sgt Emery Guzi'], 'sensors':['witness report'], 'durationSeconds':None, 'independentWitnessGroups':1}, 'phenomena': {'shape':'object reported fallen into sea', 'count':1}, 'heroVisual': {'src':IMG_MAP['D105-p253-253.png'], 'mediaType':'image', 'visualType':'official-document-page', 'caption':'D105 p. 253 recovery-feasibility tasking for the Okinawa object-in-water report.', 'provenance':'Department of War PURSUE Release 06', 'evidenceStatus':'Documentary record page; not event imagery.', 'isEventEvidence':False}, 'publicSources':[{'label':'PURSUE Release 06 landing page','url':'https://www.war.gov/UFO/?releaseDate=Release+06&release=06'}], 'images':[{'src':IMG_MAP['D105-p253-253.png'], 'caption':'D105 p. 253 Okinawa recovery-feasibility correspondence.', 'kind':'official-document-page', 'rank':1}], 'evidenceDepthStatus':'release06-admitted'}
    co = {'id':'BF-2023-CO-LE-01','title':'Colorado Law-Enforcement Orb Transcript','date':'OCT 2023','year':2023,'location':'Colorado, United States (REDACTED exact location)','mode':'redacted','lon':-105.5,'lat':39.0,'agency':'OUSD(I&S) / local law enforcement','domain':'LOCAL LAW ENFORCEMENT / VIDEO TRANSCRIPT','status':'OFFICIAL TRANSCRIPT · NATIVE VIDEO ABSENT','confidence':'OFFICIAL CUSTODY · WITNESS-ONLY EVENT','summary':'A one-page OUSD(I&S) edited transcript records a Colorado law-enforcement officer narrating an October 2023 UAP/orb video: an orb about 300 ft up, stationary for about 15 minutes, later moving closer, and “I did check radar, there is no aircraft flying in the area.” The released PDF is transcript custody only; the native video/audio is not embedded, and the radar statement is a no-aircraft check rather than radar tracking of the orb.','official':True,'gap':'Native source video/audio, complete metadata, unedited transcript and any dispatch/radar logs are missing.','sources':['LLE-UAP-D001 p. 1'],'image':'assets/sources/PURSUE-RELEASE-06/LLE-UAP-D001-pdf-page-001.png','keyFact':'LLE-UAP-D001 is a readable official edited transcript of a Colorado law-enforcement UAP/orb video, not the video itself; “radar checked” means no aircraft in area, not radar corroboration of the orb.','heroFact':'Official custody for an edited transcript; witness-video event remains uncorroborated without native media or radar logs.','whyItMatters':'It preserves a distinctive modern law-enforcement witness-video transcript while forcing a clean custody/event distinction.','sourceQuality':'Official transcript custody; low-to-medium event evidentiary weight because native video/audio and radar logs are absent.','sourceLabel':'LLE-UAP-D001 p. 1','sourceLocator':'LLE-UAP-D001-COLORADO-2023','quoteConfidence':'Medium — transcript wording is traceable to the released official page, but native video/audio is absent.','significance':'Adds a modern official-custody law-enforcement transcript while preserving missing native-media and radar-log boundaries.','relatedCaseIds':['BF-2023-WUS-03'],'acquisitionTargets':[{'targetType':'native-video-audio','description':'Native unedited law-enforcement video/audio file and metadata for the Colorado orb recording','status':'publicly-unavailable','publicOnlyResult':'Release provides an edited transcript page only','lastPublicAudit':'2026-09-22','auditScope':'release06-public-pages'},{'targetType':'dispatch-radar-logs','description':'Dispatch/CAD records, radar query logs, or contemporaneous corroborating records for the reported no-aircraft check','status':'publicly-unavailable','publicOnlyResult':'No dispatch or radar log included with LLE-UAP-D001','lastPublicAudit':'2026-09-22','auditScope':'release06-public-pages'}],'confidenceModel': {'record':'official-record', 'anomaly':'low-witness-report-only', 'provenance':'primary-release-page'},'caseTypes':['case-record','law-enforcement-witness','transcript-only'], 'evidenceModes':['official-transcript','witness-video-described'], 'environment':['ground-observer'], 'outcome':'native-video-missing; no-radar-track-documented', 'coordinateBasis':'state-level placeholder because identifying location is edited out', 'coordinatePrecision':'state', 'geometryExpectation':'region', 'temporal':{'dateLabel':'OCT 2023','year':2023,'precision':'month','eventForm':'single-witness-video-transcript'}, 'geospatial':{'basis':'state-level Colorado placeholder; identifying info edited out', 'precision':'state', 'geometry':{'type':'Point','coordinates':[-105.5,39.0]}}, 'sourceUpdateCard':{'title':'Release 06 admission — transcript custody, not radar corroboration','finding':'The officer narrates an orb about 300 ft up, stationary for about 15 minutes and later moving closer; the transcript says radar showed no aircraft flying in the area.','boundary':'The PDF contains no native video/audio and does not say radar tracked the orb. Do not link it to anonymous MP4s or PR130/PR131 stills without exact metadata.' ,'sourcePages':['LLE-UAP-D001 p. 1']}, 'sourceRecords':[{'citation':'LLE-UAP-D001 · Transcript of an Unresolved UAP Report, Colorado, October 2023','sourceType':'official-edited-transcript', 'provenance':'Department of War PURSUE Release 06 / OUSD(I&S)', 'locator':'PDF p. 1', 'url':'https://www.war.gov/UFO/?releaseDate=Release+06&release=06', 'sourcePageImages':['assets/sources/PURSUE-RELEASE-06/LLE-UAP-D001-pdf-page-001.png'], 'supports':['official custody for an edited transcript', 'law-enforcement officer narration of orb/video', 'statement that radar check showed no aircraft in the area'], 'limitations':['native video/audio not embedded or released in this PDF', 'identifying information edited out', 'radar statement is not radar tracking/corroboration of the object']}], 'observation':{'witnessCount':1,'witnessRoles':['local law-enforcement officer'],'sensors':['witness video described in transcript','radar checked for aircraft only'], 'durationSeconds':900, 'independentWitnessGroups':1}, 'phenomena':{'shape':'orb','count':1,'reportedAltitude':'about 300 ft (witness statement)'}, 'heroVisual':{'src':'assets/sources/PURSUE-RELEASE-06/LLE-UAP-D001-pdf-page-001.png','mediaType':'image','visualType':'official-document-page','caption':'LLE-UAP-D001 p. 1 edited transcript of the Colorado law-enforcement orb report.','provenance':'Department of War PURSUE Release 06','evidenceStatus':'Documentary transcript page; not event imagery.','isEventEvidence':False}, 'publicSources':[{'label':'PURSUE Release 06 landing page','url':'https://www.war.gov/UFO/?releaseDate=Release+06&release=06'}], 'images':[{'src':'assets/sources/PURSUE-RELEASE-06/LLE-UAP-D001-pdf-page-001.png','caption':'LLE-UAP-D001 p. 1 edited transcript page.','kind':'official-document-page','rank':1}], 'evidenceDepthStatus':'release06-admitted'}
    for c in (ok, co): upsert_case(data, c)
    upsert_timeline(data, {'id':'TL-1950-OK-INQUIRY','date':'1950-11','year':1950,'type':'official inquiry','title':'Okinawa object-in-water recovery inquiry','caseId':'BF-1950-OK-01','desc':'Official correspondence asks whether T/Sgt Emery Guzi’s reported object in the sea near Okinawa could be located or recovered; no recovery is documented.'})
    upsert_timeline(data, {'id':'TL-2023-CO-LE-ORB','date':'2023-10','year':2023,'type':'official transcript','title':'Colorado law-enforcement orb transcript','caseId':'BF-2023-CO-LE-01','desc':'OUSD(I&S) releases an edited transcript of a local law-enforcement officer narrating an orb video; native video and radar corroboration are absent.'})
    for cid in ['BF-1952-TM-01', 'BF-2022-ME-01', 'BF-1950-OK-01', 'BF-2023-CO-LE-01']:
        u = case(data, cid).get('sourceUpdateCard') or {}
        if 'finding' in u or 'boundary' in u:
            findings = [u.pop('finding')] if 'finding' in u else []
            limitations = [u.pop('boundary')] if 'boundary' in u else []
            if u.get('sourcePages'):
                limitations.append('Source pages: ' + ', '.join(u.pop('sourcePages')))
            u['findings'] = findings
            u['limitations'] = limitations
            u['status'] = 'Release 06 focused update'
    for cid, token in [('BF-1952-TM-01', 'RELEASE06-TREMONTON-MEMO'), ('BF-2022-ME-01', 'RELEASE06-MAY2022-REPORTS')]:
        c = case(data, cid)
        c['sources'] = [s for s in c['sources'] if s != token] + [token]
    dump(DATA, data)

    sidx = load(SRC_INDEX)
    sidx['RELEASE06-TREMONTON-MEMO'] = [f'assets/sources/PURSUE-RELEASE-06/DOW-UAP-D102-pdf-page-{n:03d}.png' for n in [37,38,39,113,121]]
    sidx['RELEASE06-MAY2022-REPORTS'] = [f'assets/sources/PURSUE-RELEASE-06/DOW-UAP-{token}-pdf-page-{n:03d}.png' for token,n in [('D106',1),('D106',6),('D109',1),('D109',6)]]
    sidx['DOW-UAP-D105-OKINAWA-1950'] = [IMG_MAP['D105-p252-252.png'], IMG_MAP['D105-p253-253.png'], 'https://www.war.gov/UFO/?releaseDate=Release+06&release=06']
    sidx['LLE-UAP-D001-COLORADO-2023'] = ['assets/sources/PURSUE-RELEASE-06/LLE-UAP-D001-pdf-page-001.png', 'https://www.war.gov/UFO/?releaseDate=Release+06&release=06']
    sidx['DOW-UAP-D10-ME-2022'] = [IMG_MAP['D10-p001-1.png'], IMG_MAP['D10-p006-6.png'], 'https://www.war.gov/UFO/']
    dump(SRC_INDEX, sidx)
    pm = load(PUB_MANIFEST)
    for cid,label,note in [('BF-1950-OK-01','PURSUE Release 06 — D105 Okinawa pages','Official release landing page; local Atlas carries rendered page derivatives for pp. 252–253.'), ('BF-2023-CO-LE-01','PURSUE Release 06 — LLE-UAP-D001 transcript','Official release landing page; local Atlas carries the rendered transcript page.')]:
        pm[cid] = [{'label':label,'publisher':'U.S. Department of War','url':'https://www.war.gov/UFO/?releaseDate=Release+06&release=06','access':'Public landing page','scope':'official-release','note':note}]
    dump(PUB_MANIFEST, pm)
    after_ids = {c['id'] for c in data['cases']}
    print(json.dumps({'added': sorted(after_ids-before_ids), 'cases': len(data['cases']), 'timeline': len(data.get('timeline',[])), 'orbital': sum(1 for c in data['cases'] if c.get('mode')=='orbital')}, indent=2))
if __name__ == '__main__': main()
