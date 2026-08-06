import fs from 'node:fs';
import assert from 'node:assert/strict';

const data = JSON.parse(fs.readFileSync('atlas-data.json', 'utf8'));
const app = fs.readFileSync('atlas-app.js', 'utf8');
const orbital = data.cases.filter(c => c.mode === 'orbital');

assert.equal(data.cases.length, 147, 'canonical case count must remain 147');
assert.equal(orbital.length, 26, 'Orbital/Lunar layer must contain exactly 26 records');

const roles = new Map();
const allowedRoles = new Set(['corpus-record', 'event-dossier']);
for (const c of orbital) {
  const e = c.orbitalEvidence;
  assert.ok(e && typeof e === 'object', `${c.id}: missing orbitalEvidence`);
  assert.equal(e.schemaVersion, 1, `${c.id}: unsupported orbitalEvidence schema`);
  assert.ok(allowedRoles.has(e.architectureRole), `${c.id}: invalid architectureRole`);
  assert.match(e.recordType || '', /\S/, `${c.id}: missing recordType`);
  assert.match(e.officialRecord || '', /\S/, `${c.id}: missing officialRecord`);
  assert.match(e.interpretationStatus || '', /\S/, `${c.id}: missing interpretationStatus`);
  for (const field of ['supports', 'doesNotEstablish', 'limitations']) {
    assert.ok(Array.isArray(e[field]) && e[field].length > 0, `${c.id}: ${field} must be non-empty`);
    e[field].forEach((text, i) => assert.match(text, /\S/, `${c.id}: ${field}[${i}] empty`));
  }
  const serialized = JSON.stringify(e);
  assert.doesNotMatch(serialized, /\/Users\/|\/Volumes\/|file:\/\//i, `${c.id}: private path leak`);
  roles.set(e.architectureRole, (roles.get(e.architectureRole) || 0) + 1);
}
assert.equal(roles.get('corpus-record'), 24, 'expected 24 corpus records');
assert.equal(roles.get('event-dossier'), 2, 'expected 2 curated event dossiers');

const pairs = [
  ['BF-NASA-D021', 'BF-1965-G7-01'],
  ['BF-NASA-D007', 'BF-1973-SL-01'],
];
for (const [corpusId, eventId] of pairs) {
  const corpus = orbital.find(c => c.id === corpusId);
  const event = orbital.find(c => c.id === eventId);
  assert.equal(corpus.orbitalEvidence.relatedCaseId, eventId, `${corpusId}: event link drift`);
  assert.equal(corpus.orbitalEvidence.relationship, 'corpus-source-for-event', `${corpusId}: relationship drift`);
  assert.equal(event.orbitalEvidence.relatedCaseId, corpusId, `${eventId}: corpus link drift`);
  assert.equal(event.orbitalEvidence.relationship, 'curated-event-from-corpus', `${eventId}: relationship drift`);
}

for (const caseId of ['BF-1965-G7-01', 'BF-1973-SL-01']) {
  const c = orbital.find(x => x.id === caseId);
  assert.equal(c.status, 'CURATED EVENT · PRIMARY PASSAGE NOT LOCALLY MAPPED', `${caseId}: event status drift`);
  assert.match(c.quoteConfidence, /^Medium\b/, `${caseId}: quote confidence must remain qualified`);
  assert.equal(c.orbitalEvidence.interpretationStatus, 'primary-passage-unmapped', `${caseId}: passage boundary drift`);
}
assert.match(orbital.find(c => c.id === 'BF-NASA-D021').orbitalEvidence.doesNotEstablish.join(' '), /does not contain.*bogey/i, 'Gemini 7 corpus-page boundary drift');
assert.match(orbital.find(c => c.id === 'BF-NASA-D007').orbitalEvidence.doesNotEstablish.join(' '), /do not contain.*one or two objects/i, 'Skylab corpus-page boundary drift');
for (const caseId of ['BF-NASA-VM1','BF-NASA-VM2','BF-NASA-VM3','BF-NASA-VM4','BF-NASA-VM5','BF-NASA-VM6']) {
  const c = orbital.find(x => x.id === caseId);
  assert.equal(c.orbitalEvidence.recordType, 'released-annotated-visual', `${caseId}: visual record type drift`);
  assert.match(c.sourceQuality, /annotated visual-material artifact/i, `${caseId}: native-frame custody must not be implied`);
}
const d032 = orbital.find(c => c.id === 'BF-NASA-D032').orbitalEvidence;
assert.equal(d032.interpretationStatus, 'released-image-context-unresolved', 'D032: unresolved visual-mark status drift');
assert.match(d032.supports.join(' '), /small angular mark/i, 'D032: visible angular mark must remain documented');
assert.match(d032.doesNotEstablish.join(' '), /does not establish.*identity.*motion.*distance.*scale/i, 'D032: single-frame boundary drift');

assert.match(app, /function orbitalEvidenceLensHtml\(c\)/, 'orbital Evidence Lens renderer missing');
assert.match(app, /Official record boundary/, 'orbital boundary heading missing');
assert.match(app, /What the record supports/, 'orbital supports label missing');
assert.match(app, /What remains unresolved/, 'orbital limitations label missing');
assert.match(app, /orbitalEvidenceLensHtml\(c\)/, 'orbital renderer not wired');

console.log(JSON.stringify({status:'PASS', cases:data.cases.length, orbital:orbital.length, roles:Object.fromEntries(roles)}, null, 2));
