# Orbital/Lunar Evidence Architecture Pass 2 — NASA Visual Materials

**Date:** 2026-07-25  
**Scope:** Dedicated Orbital/Lunar evidence architecture. No new cases, no outreach, no private acquisition.

## Cases patched

- `BF-NASA-VM1` — Apollo 12 Visual Material 1
- `BF-NASA-VM2` — Apollo 12 Visual Material 2
- `BF-NASA-VM3` — Apollo 12 Visual Material 3
- `BF-NASA-VM4` — Apollo 12 Visual Material 4
- `BF-NASA-VM5` — Apollo 12 Visual Material 5
- `BF-NASA-VM6` — Apollo 17 Visual Material

## Architecture applied

Each visual-material case now uses consistent released-record language:

### Supports

- identifies the item as an official released visual artifact, not a later unsourced internet image;
- confirms the Atlas has local image / preview / ROI mapping for visual review;
- anchors the record to a named NASA/War.gov source locator inside the Orbital/Lunar evidence layer.

### Limitations

- a still image does not establish object identity, distance, scale, trajectory, or origin;
- no full native mission sequence, calibration packet, camera geometry, or independent trajectory analysis is mapped;
- the record should be read as an unresolved released visual artifact, not standalone proof of anomalous craft.

## Separation check

The six records remain explicitly in:

```text
ORBITAL / NASA
```

They were not moved into the default main-stack interpretation path, and no new cases were added.

## Token / source-index status

No blocking token gaps were found. Each case source token resolves to local image/preview/ROI assets or evidence-depth notes.

## Local verification

```text
caseCount: 146
sourceRecordCount: 234
sourceDepthWeakCaseCount: 70
casesWithMappedLinks: 146
casesWithPublicSourceUrls: 146
missingLocalAssets: []
static invalid refs: 0
/Users paths: 0
file:// strings: 0
bad Commons file-page refs: 0
patched orbital visual records: 6/6
```

## Product note

After one more Orbital/Lunar batch, the Atlas is ready for a small UI/content enhancement: an intro/drawer note explaining how to read NASA/orbital evidence — released artifacts, custody strength, and interpretation limits.
