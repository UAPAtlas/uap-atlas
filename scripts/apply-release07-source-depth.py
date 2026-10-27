#!/usr/bin/env python3
"""Idempotent, scoped Release 07 source-depth overlay for two existing dossiers."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ATLAS=ROOT/'atlas-data.json'
LEDGER=ROOT/'research/pursue-release07-intake-ledger.json'
records=json.loads(LEDGER.read_text())['files']
import re
def record_id(filename):
 match=re.match(r'((?:DOW|FBI|EOP|USG)-UAP-D\d+)',filename)
 assert match,filename
 return match.group(1)
by_id={record_id(r['filename']):r for r in records}
for key in ('DOW-UAP-D168','DOW-UAP-D173','DOW-UAP-D174','DOW-UAP-D175'):
 assert by_id[key]['sha256'] and by_id[key]['mirrorHashMatch'] is True

def source(key,citation,locator,supports,limitations):
 r=by_id[key]
 return {'citation':citation,'sourceType':'official-release-contractor-report',
  'provenance':'Department of War PURSUE Release 07; contractor-produced record in official release custody',
  'locator':locator,'url':r['sourceUrl'],'sha256':r['sha256'],
  'supports':supports,'limitations':limitations}

program_sources=[
 source('DOW-UAP-D168','DOW-UAP-D168 · BAASS Project Management Plan, December 2008','pp. 1–2, 7–11',
  ['Names contract HHM402-08-C-0072 and describes BAASS technical and investigative plans.','Requests access to allegedly government-held films and material.'],
  ['A request or contractor premise does not establish that any alleged film, sample or craft existed or was transferred.']),
 source('DOW-UAP-D173','DOW-UAP-D173 · BAASS Monthly Report, November 2009','pp. 5–10, 19–50, 107–114, 126–155',
  ['Documents contractor field reporting, MUFON intake, Utah Ranch experiments and a Northern Tier access problem.','The Modesto blue-light case is attributed to contemporaneous blue-lit model gliders on pp. 8–10; p. 155 records lack of Need to Know for proposed classified-archive work.'],
  ['Ranch germination sheet is blank; medical summary for the blue-orb account is redacted, preventing independent diagnosis/causation review.','Field narratives and collected samples do not establish anomalous materials; pp. 117–125 researcher-threat discussion is retracted on p. 126.']),
 source('DOW-UAP-D174','DOW-UAP-D174 · Utah Ranch Investigation Report, April 2010','pp. 30–38',
  ['Laboratory letter p. 37 reports that three submitted hair samples shared a canine HVI sequence common in domestic dogs.','BAASS interpretation p. 38 identifies the fourth sample as raccoon.'],
  ['Sample-specific ordinary-animal results do not determine every separate ranch account.','The reviewed pages do not establish an anomalous organism or independent causal link between environmental readings and claimed events.']),
 source('DOW-UAP-D175','DOW-UAP-D175 · BAASS Self-Assessment of UAP Analysis Capabilities, November 2010','pp. 11–13, 33–48',
  ['Documents BAASS analytical and simulation capabilities and its retrospective Nimitz parameter study.','Page 33 says hard data and exact duration were lacking; calculations used testimony and assumed 0.5–10 second intervals.'],
  ['Extreme velocity/acceleration values are conditional model outputs, not newly released instrument measurements.','CFD illustrations are simulations, not original event imagery or proof of recovered hardware.'])]

j=json.loads(ATLAS.read_text());cases={c['id']:c for c in j['cases']}
assert {'BF-SF-09','BF-2004-NM-01'}<=cases.keys()
program=cases['BF-SF-09'];nimitz=cases['BF-2004-NM-01']
for c, wanted in [(program,program_sources),(nimitz,[program_sources[-1]])]:
 keys={s['citation'] for s in wanted}
 c['sourceRecords']=[s for s in c['sourceRecords'] if s.get('citation') not in keys]+wanted
program['sourceQuality']=(
 'Official DIA/DoW AAWSAP contracting, technical and contractor reports plus AARO KONA BLUE history establish program funding, plans, field methods and later institutional disposition. '
 'Release 07 D168/D173–D175 documents BAASS assertions and activities, while D173 records conventional resolutions and access limits and D174 reports ordinary animal hair identifications; no transferred non-human material is authenticated.')
program['keyFact']=(
 'The AAWSAP/BAASS program is documented. Release 07 contractor files show plans and fieldwork, but the ranch hair samples tested as ordinary animals and proposed access to alleged material is not a custody transfer. '
 'KONA BLUE was never approved or supplied with material.')
nimitz['sourceQuality']=(
 'The 13-page public executive-summary copy and official DoD/DVIDS FLIR1 record document the reporting chain; the public copy lacks its originating-office release chain. '
 'Release 07 BAASS D175 is a contractor modeling study: its page 33 acknowledges little hard data and unknown event duration, then varies assumed time from 0.5 to 10 seconds. The modeled extremes are not new SPY-1 measurements.')
nimitz['keyFact']=(
 'Nimitz is an officially acknowledged Navy UAP encounter with witness and sensor implications beyond the public FLIR clip; BAASS Release 07 speed/acceleration figures are conditional modeling, not newly recovered radar data.')
program['sourceUpdateCard']={
 'title':'Release 07 · BAASS plans, tests and access limits',
 'findings':['D168 documents the contractor plan and requests for alleged material access; D173 documents fieldwork and a model-glider resolution; D174 pp. 37–38 reports ordinary canine/raccoon hair identifications.'],
 'limitations':['A contractor request is not a transfer or authenticated craft. D173 p. 155 says classified-archive access was on hold; its blue-orb medical summary is redacted. These sample results do not resolve every separate ranch report.'],
 'status':'Released program records · claims and custody kept separate'}
nimitz['sourceUpdateCard']={
 'title':'Release 07 · Nimitz performance-model boundary',
 'findings':['BAASS D175 pp. 33–35 modeled Nimitz speed and acceleration using testimony and an assumed 0.5–10-second event-duration range.'],
 'limitations':['D175 p. 33 says hard data and exact duration were lacking. Its extreme figures and CFD images are conditional analysis, not newly released SPY-1 radar data or event imagery.'],
 'status':'Contractor model · not instrumented measurement'}
text=json.dumps(j,ensure_ascii=False,indent=2)+'\n'
if ATLAS.read_text()!=text:ATLAS.write_text(text)
print('scopeCaseIds', ['BF-SF-09','BF-2004-NM-01'],'sourceRecordsAdded',len(program_sources)+1)
