#!/usr/bin/env python3
"""Idempotently admit one bounded Release 07 triangle testimony event family."""
import copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'atlas-data.json'; INDEX=ROOT/'source-file-index.json'; MANIFEST=ROOT/'public-source-manifest.json'
ledger=json.loads((ROOT/'research/pursue-release07-intake-ledger.json').read_text())['files']
records={r['filename'].split('-',3)[0]+'-'+r['filename'].split('-',3)[1]+'-'+r['filename'].split('-',3)[2]:r for r in ledger}
C='BF-2026-TR-01'; T='TL-2026-TR-01'; A='DOW-UAP-D176'; F='FBI-UAP-D043'
for token in (A,F):
 assert records[token]['mirrorHashMatch'] is True and records[token]['sha256']
P='assets/sources/PURSUE-RELEASE-07/'
paths={token:[f'{P}{token}-pdf-page-{page:03}-display.jpg' for page in pages] for token,pages in ((A,(1,2,3)),(F,(1,2)))}
assert all((ROOT/path).is_file() and (ROOT/path).stat().st_size<350_000 for ps in paths.values() for path in ps)
def source(token,citation,locator,supports,limitations):
 r=records[token]
 return {'citation':f'{token} · {citation}',
  'sourceType':'primary-official-witness-debrief' if token==A else 'primary-official-witness-interview-record',
  'provenance':'Department of War PURSUE Release 07 custody; public mirror SHA-256 matches independent archive metadata, but official-origin byte identity was not independently verified. This is a report of witness statements, not an agency finding validating the described object.',
  'locator':locator,'url':r['sourceUrl'],'sha256':r['sha256'],'sourcePageImages':paths[token],
  'supports':supports,'limitations':limitations}
geo='Map-only generalized continental U.S. centroid; the released records redact the event location. Not a sighting coordinate.'
sources=[
 source(A,'AARO joint witness debrief memorandum for record, 2026','PDF pp. 1–3; p. 1 overview, pp. 2–3 chronology',
 ['Records two primary observers and a third thermal-observation-post caller describing one dark triangular form over a western ridge and canyon.',
  'AARO reports an initial call at 2023 local and phases of approximately 10 seconds ascent, 20 seconds hover and 2–3 seconds departure.',
  'Records unaided/binocular observation and use of handheld thermal optics; p. 3 expressly says no instrumented speed measurement was obtained.'],
 ['Interviewees are anonymized and the event date and precise location are redacted.',
  'No original visual/thermal file, calibrated distance, measured velocity or independent sensor log is included in the released memorandum.',
  'The memorandum warns that witness interpretations are not conclusive intrinsic object features or performance characteristics.',
  'The FBI companion witness statement instead says 1923 hours and approximately three seconds total; neither account resolves the conflict.']),
 source(F,'FD-302 with co-signed witness statement and uncatalogued visual attachments, 2026','PDF pp. 1–2 testimony; pp. 3–11 uncatalogued landscape/triangle visual attachments',
 ['Preserves the co-signed agents’ account of a dark triangular form, handheld thermal viewing and movement near a ridge.',
  'The statement records 1923 hours and approximately three seconds total, not the AARO 2023 local / multi-phase timing.'],
 ['The FD-302 explicitly contains neither recommendations nor conclusions of the FBI.',
  'Attached pp. 3–11 contain landscape/triangle illustrations without visible captions or capture-chain documentation proving event photography; they are unverified illustrations, not event imagery or independent corroboration.',
  'Reported size, range, thermal appearance and velocity are witness estimates, not calibrated sensor outputs.',
  'The same witness event appears in the AARO debrief; two government documents do not establish two independent event families.'])]
case={
 'id':C,'title':'2026 Ridge-Line Triangle Report','date':'[REDACTED] 2026','year':2026,
 'location':'United States [REDACTED]','mode':'redacted','lon':-98.5,'lat':39.8,
 'expectedCountry':'United States of America','geometryExpectation':'country',
 'coordinatePrecision':'country-redacted-generalized','coordinateBasis':geo,
 'agency':'FBI / AARO','domain':'GOVERNMENT / INSTITUTIONAL','status':'DOCUMENTED TESTIMONY · UNRESOLVED',
 'confidence':'OFFICIAL WITNESS RECORDS · LOWER-CONFIDENCE TESTIMONY',
 'summary':'A 2026 AARO debrief and FBI FD-302 preserve overlapping accounts of one reported dark triangular form near a ridge. The records conflict: the FBI statement gives 1923 hours and approximately three seconds total, while AARO gives 2023 local and approximately 10 + 20 + 2–3 seconds for ascent, hover and departure. These are witness accounts, not calibrated flight data or independent agency confirmation.',
 'keyFact':'One witness-event family appears in both records, but time and duration are materially inconsistent; no instrumented speed measurement was obtained.',
 'heroFact':'Lower-confidence testimony: one event, conflicting 1923 vs 2023 local and ~3 seconds vs 10 + 20 + 2–3 seconds. FBI attachments are unverified illustrations, not event imagery.',
 'official':'The AARO memorandum records a joint witness debrief; the FD-302 records a co-signed witness statement and is not an FBI factual finding. Release custody confirms the records, not the described object or performance.',
 'gap':'Missing are the redacted exact date/site, original thermal or optical recordings, calibrated range, instrumented speed measurement, sensor logs, aviation/UAS correlation and any analytical closure. The 1923/2023 local-time and three-second/multi-phase discrepancies remain unresolved.',
 'whyItMatters':'Two agency-held records preserve a distinctive same-event multi-observer report while exposing a material chronology conflict that must remain visible rather than being smoothed into a high-performance claim.',
 'sources':[A,F],'sourceLabel':'AARO debrief / FBI FD-302','sourceLocator':A,
 'relatedCaseIds':['BF-2026-RL-01'],'keyQuote':'No instrumented speed measurement was obtained.',
 'quoteSource':'DOW-UAP-D176, AARO memorandum for record, PDF p. 3',
 'quoteConfidence':'High transcription confidence for the AARO memorandum; the reported event and performance are not independently verified.',
 'significance':'Lower-confidence testimony',
 'sourceQuality':'Two official records of an overlapping 2026 witness event. FBI pp. 3–11 include uncatalogued unverified illustrations, not established event photography or independent sensor data. Exact location/date redacted; chronology conflicts.',
 'sourceFamilyRelationship':'same-witness-event',
 'image':paths[A][0],'images':[paths[A][0],paths[F][0],paths[A][1],paths[F][1],paths[A][2]],
 'caseTypes':['witness-report'],'evidenceModes':['testimony','reported-handheld-thermal-observation'],
 'environment':['terrestrial'],'outcome':'unresolved',
 'confidenceModel':{'record':'confirmed','anomaly':'undetermined','provenance':'primary-source'},
 'temporal':{'dateLabel':'[REDACTED] 2026','year':2026,'startDateTime':None,'endDateTime':None,'timezone':None,'durationSeconds':None,'precision':'year-redacted-conflicting-time','eventForm':'single-event-multi-phase-reported'},
 'geospatial':{'geometry':{'type':'Point','coordinates':[-98.5,39.8]},'role':'representative-centroid','precision':'country-redacted-generalized','uncertaintyKm':2000,'basis':geo},
 'sourceRecords':sources,
 'phenomena':{'shapes':['triangle'],'objectCount':1,'luminosity':None,'motion':['reported-vertical-ascent','reported-hover','reported-horizontal-departure'],'effects':[]},
 'observation':{'witnessCount':3,'witnessRoles':['two primary law-enforcement observers','one secondary thermal-post caller'],'sensors':['unaided visual','binoculars','reported handheld thermal monocular'],'durationSeconds':None,'independentWitnessGroups':1},
 'taxonomyOriginal':{'domain':'WITNESS NARRATIVE','status':'UNRESOLVED','confidence':'LOWER-CONFIDENCE TESTIMONY'},'taxonomyVersion':'atlas-controlled-v1',
 'heroVisual':{'src':paths[A][0],'mediaType':'image','visualType':'official-document-page','caption':'AARO debrief page; documentary evidence of witness reporting, not event imagery.','provenance':'DOW-UAP-D176, PDF p. 1, PURSUE Release 07','evidenceStatus':'Official document page; not a photograph or sensor recording of the event.','isEventEvidence':False},
 'publicSources':[{'label':f'War.gov — PURSUE Release 07 · {token}','url':records[token]['sourceUrl'],'publisher':'U.S. Department of War','access':'Official public PDF endpoint; may block automated clients','scope':'exact-released-record','note':'Official custody for a witness record; no agency conclusion confirming an anomalous craft.'} for token in (A,F)],
 'evidenceBoundary':{'established':['AARO and FBI released records documenting overlapping witness descriptions of one reported 2026 triangle event.','The records disagree on reported time and duration.'],
 'notEstablished':['Calibrated speed, range, altitude, object identity or propulsion.','Original event photography or thermal recording; FBI attached visuals have unverified provenance.','Independent witness groups or an FBI finding confirming the object.','Any connection to the linked 2026 red-light case; the link is documentary-form comparison only.'],
 'competingExplanations':['Conventional UAS or aircraft observed at uncertain distance, with terrain/low-light and handheld narrow-field optics affecting apparent motion; the available records cannot test these against raw data.']}}
timeline={'id':T,'year':2026,'date':'[REDACTED] 2026','type':'incident','caseId':C,'title':'Ridge-line triangle witness report','desc':'AARO and FBI records preserve one multi-observer triangle report with conflicting 1923/2023 time and three-second versus multi-phase duration; no calibrated speed or native event imagery is public.'}

def save(path,payload):
 encoded=json.dumps(payload,ensure_ascii=False,indent=2)+'\n'
 if path.read_text()!=encoded:path.write_text(encoded)
a=json.loads(ATLAS.read_text())
old=[c for c in a['cases'] if c['id']==C]
assert len(old)<=1
existing=[t for t in a['timeline'] if t['id']==T]
assert len(existing)<=1 and all(t.get('caseId')==C for t in existing)
a['cases']=[c for c in a['cases'] if c['id']!=C]+[case]
a['timeline']=[t for t in a['timeline'] if t['id']!=T]+[timeline]
# Preserve the published registry order; a global re-sort causes unrelated churn.
save(ATLAS,a)
idx=json.loads(INDEX.read_text());manifest=json.loads(MANIFEST.read_text())
for token in (A,F):idx[token]=paths[token]+[records[token]['sourceUrl']]
manifest[C]=case['publicSources']
save(INDEX,idx);save(MANIFEST,manifest)
print('applied',C,T,'source tokens',A,F,'case/timeline',len(a['cases']),len(a['timeline']))
