# Three-case provenance tranche — 2026-08-05

## Scope

This bounded tranche covers exactly:

- `BF-1997-PH-01` — Phoenix Lights
- `BF-1978-VL-01` — Valentich disappearance
- `BF-1973-PG-01` — Pascagoula report

No cases, UI, navigation, NARA crosswalk, or unrelated queue work were added. Research was restricted to existing local holdings and public URLs; no outreach, forms, accounts, purchases, or records requests were used.

## Evidence corrections

### Phoenix Lights

The dossier now separates two analytically distinct windows rather than treating March 13 as one event:

1. earlier moving-formation / large-dark-object reports across Arizona; and
2. later stationary lights near Phoenix associated in contemporaneous press reporting with Maryland Air National Guard A-10 illumination flares.

Fife Symington's 2007 CNN commentary is classified as a firsthand retrospective, not an official investigation or contemporaneous primary case file. The July 25, 1997 *Las Vegas Sun* report is classified as contemporaneous press quoting Arizona and Maryland Air National Guard spokespeople, not as custody of the underlying sortie, range, or flare-expenditure records. The local nighttime-light preview is now context, not authenticated event evidence.

### Valentich

The dossier now separates three evidence layers:

- the National Archives of Australia item is an exact official catalog locator;
- the ATSB URL is an exact official report locator whose payload was unavailable to direct inspection during this tranche; and
- the inspected UFOr PDF is a public/private mirror of the final-communications transcript, not direct NAA or Department of Transport custody.

The mirror supports the wording of Valentich's reported communications, including his description of an unidentified object and rough engine running. It does not establish the object's identity, a causal relationship, or the cause of the disappearance. Claims about official conclusions, search chronology, radar, debris, and complete packet contents were not upgraded without direct page inspection.

### Pascagoula

The dossier now distinguishes:

- a historically documented Hickson/Parker report to local authorities;
- a public local-history trail concerning a reported covert sheriff-room recording; and
- the underlying object, entity, and abduction claims, which remain testimonial.

The Hinds Community College page verifies the existence of a public page devoted to the 1973 recording context, but the Atlas does not hold the original audio, a coherent custody history, a complete authenticated transcript, or the sheriff case packet. The exact Hickson quotation remains qualified as publicly circulated wording rather than authenticated original-audio custody. Law enforcement has been removed from the witness-role field. The WLOX historical-marker material remains cultural context only.

## Queue dispositions

All three cases moved from `quality_upgrade` to structured `acquisition_target`. This is not a completeness promotion; it records that further wording work cannot close the decisive custody gaps.

- Phoenix: ANG sortie/flare records, range logs, FAA/radar records, original videos, synchronized witness corpus.
- Valentich: complete NAA/DoT packet, direct official transcript/audio custody, official search and sensor documentation.
- Pascagoula: complete sheriff packet, original audio and custody history, complete timecoded transcript, contemporaneous interview logs.

After deterministic audit regeneration, Atlas operational triage is:

- true gaps: 0
- quality upgrades: 10
- acquisition targets: 18
- complete: 118

## Reproducibility and regression

A focused regression was written before the data patch and failed on the stale Phoenix `CIA archive` source label. The completed contract asserts all three evidence boundaries, all three structured acquisition dispositions, the exact three case IDs and three linked timeline IDs, and legacy-generator safeguards.

The obsolete canon/honorable-mention bootstrap generators now refuse to recreate the evidence-audited Valentich and Pascagoula records if those records are absent. The bounded mutator records the final deterministic three-case patch. NARA crosswalk outputs were intentionally not regenerated because this is a non-NARA provenance tranche.

## Decisive records still unavailable

- Phoenix: underlying Maryland ANG sortie/flare-expenditure records, Barry M. Goldwater Range logs, contemporaneous FAA/radar data, original full-resolution video custody, synchronized witness chronology.
- Valentich: directly inspected complete NAA/Department of Transport file, direct official transcript/audio custody, complete search documentation, complete radar/sensor record.
- Pascagoula: authenticated complete Jackson County sheriff packet, original recording with custody history, complete issued/timecoded transcript, earliest complete interview logs.
