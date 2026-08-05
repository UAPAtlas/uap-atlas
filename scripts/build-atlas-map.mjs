import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import * as d3 from 'd3-geo';
import {
  VIEWBOX,
  FIT_EXTENT,
  PROJECTION,
  PROJECTION_VERSION,
  COUNTRY_SOURCE,
  ADMIN1_SOURCE,
  roundCoord,
} from './projection-config.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const WRITE_HTML = process.argv.includes('--write-html');

function readJson(relPath) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, relPath), 'utf8'));
}

function writeJson(relPath, value) {
  const out = path.join(ROOT, relPath);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, `${JSON.stringify(value, null, 2)}\n`);
}

function attr(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function countryName(feature) {
  return feature.properties.ADMIN || feature.properties.NAME_LONG || feature.properties.NAME || 'Unknown';
}

function adminName(feature) {
  return feature.properties.name || feature.properties.name_en || feature.properties.name_local || 'Unknown';
}

function adminCountry(feature) {
  return feature.properties.admin || feature.properties.geonunit || feature.properties.gu_a3 || feature.properties.adm0_a3 || 'Unknown';
}

function makeProjection(countriesGeo) {
  return d3.geoNaturalEarth1().fitExtent(FIT_EXTENT, countriesGeo);
}

function mapGeometry(c, geoPath) {
  const geometry = c.geospatial?.geometry;
  if (!geometry || geometry.type === 'Point') return null;
  const d = geoPath(geometry);
  if (!d) return null;
  return {
    type: geometry.type,
    d,
    label: c.geospatial.geometryLabel || geometry.type,
    basis: c.geospatial.geometryBasis || c.geospatial.basis || '',
    confidence: c.geospatial.geometryConfidence || 'approximate',
    isObjectTrack: c.geospatial.geometryIsObjectTrack === true,
  };
}

function projectCase(c, projection, geoPath) {
  const mappedGeometry = mapGeometry(c, geoPath);
  const isOrbital = c.mode === 'orbital' || c.geometryExpectation === 'orbital';
  const hasLonLat = Number.isFinite(c.lon) && Number.isFinite(c.lat);
  if (isOrbital || !hasLonLat) {
    return {
      ...c,
      mapGeometry: mappedGeometry,
      coordinateGenerated: false,
      projection: isOrbital ? 'orbital-aggregate-layer' : 'unprojected-no-lonlat',
    };
  }
  const projected = projection([c.lon, c.lat]);
  if (!projected || !Number.isFinite(projected[0]) || !Number.isFinite(projected[1])) {
    return {
      ...c,
      mapGeometry: mappedGeometry,
      coordinateGenerated: false,
      projection: `${PROJECTION_VERSION}-failed`,
    };
  }
  return {
    ...c,
    mapGeometry: mappedGeometry,
    x: roundCoord(projected[0]),
    y: roundCoord(projected[1]),
    coordinateGenerated: true,
    projection: PROJECTION_VERSION,
  };
}

function buildMapPayload() {
  const atlasSource = fs.readFileSync(path.join(ROOT, 'atlas-data.json'));
  const countrySource = fs.readFileSync(path.join(ROOT, COUNTRY_SOURCE));
  const admin1Source = fs.readFileSync(path.join(ROOT, ADMIN1_SOURCE));
  const atlas = JSON.parse(atlasSource);
  const countriesGeo = JSON.parse(countrySource);
  const admin1Geo = JSON.parse(admin1Source);
  const sourceFingerprint = crypto.createHash('sha256')
    .update(atlasSource)
    .update(countrySource)
    .update(admin1Source)
    .update(PROJECTION_VERSION)
    .digest('hex');
  const projection = makeProjection(countriesGeo);
  const geoPath = d3.geoPath(projection).digits(2);

  const countries = countriesGeo.features
    .map((feature) => ({
      name: countryName(feature),
      isoA3: feature.properties.ADM0_A3 || feature.properties.ISO_A3 || '',
      d: geoPath(feature),
    }))
    .filter((feature) => feature.d)
    .sort((a, b) => a.name.localeCompare(b.name));

  const admin1 = admin1Geo.features
    .filter((feature) => adminCountry(feature) === 'United States of America')
    .map((feature) => ({
      country: 'United States of America',
      name: adminName(feature),
      postal: feature.properties.postal || '',
      kind: feature.properties.type_en || feature.properties.type || 'Admin 1',
      d: geoPath(feature),
    }))
    .filter((feature) => feature.d)
    .sort((a, b) => a.name.localeCompare(b.name));

  const projectedCases = atlas.cases.map((c) => projectCase(c, projection, geoPath));

  const payload = {
    meta: {
      projection: PROJECTION,
      projectionVersion: PROJECTION_VERSION,
      viewBox: `0 0 ${VIEWBOX.width} ${VIEWBOX.height}`,
      fitExtent: FIT_EXTENT,
      countrySource: COUNTRY_SOURCE,
      admin1Source: ADMIN1_SOURCE,
      sourceFingerprint,
      countryCount: countries.length,
      admin1Count: admin1.length,
      projectedCaseCount: projectedCases.filter((c) => c.coordinateGenerated).length,
      orbitalAggregateCount: projectedCases.filter((c) => c.geometryExpectation === 'orbital' || c.mode === 'orbital').length,
    },
    countries,
    admin1,
    cases: projectedCases.map((c) => ({
      id: c.id,
      x: c.x,
      y: c.y,
      lon: c.lon,
      lat: c.lat,
      mode: c.mode,
      expectedCountry: c.expectedCountry,
      expectedAdmin1: c.expectedAdmin1,
      geometryExpectation: c.geometryExpectation,
      mapGeometry: c.mapGeometry,
      projection: c.projection,
      coordinateGenerated: c.coordinateGenerated,
    })),
  };

  const hydratedAtlas = {
    ...atlas,
    cases: projectedCases,
  };

  return { payload, hydratedAtlas };
}

function replaceJsConstant(source, prefix, value) {
  const start = source.indexOf(prefix);
  if (start === -1) throw new Error(`Missing JS constant prefix: ${prefix}`);
  let i = start + prefix.length;
  while (/\s/.test(source[i])) i += 1;
  const valueStart = i;
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (; i < source.length; i += 1) {
    const ch = source[i];
    if (escaped) {
      escaped = false;
      continue;
    }
    if (ch === '\\') {
      escaped = true;
      continue;
    }
    if (quote) {
      if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (ch === '{' || ch === '[') depth += 1;
    if (ch === '}' || ch === ']') {
      depth -= 1;
      if (depth === 0) {
        const valueEnd = i + 1;
        return `${source.slice(0, valueStart)}${JSON.stringify(value)}${source.slice(valueEnd)}`;
      }
    }
  }
  throw new Error(`Could not find end of JS constant: ${prefix}`);
}

function mapMarkup(payload) {
  const countryPaths = payload.countries.map((feature) => (
    `<path class="land" data-country="${attr(feature.name)}" data-iso-a3="${attr(feature.isoA3)}" fill-rule="evenodd" d="${feature.d}"/>`
  )).join('\n          ');

  const adminPaths = payload.admin1.map((feature) => (
    `<path class="us-state-line" data-country="${attr(feature.country)}" data-admin1="${attr(feature.name)}" data-state="${attr(feature.name)}" data-postal="${attr(feature.postal)}" d="${feature.d}"/>`
  )).join('\n          ');

  return `<g id="countryLayer" class="country-layer" opacity=".98"><g class="continents">${countryPaths}</g></g>\n        <g id="stateLines" class="state-lines admin1-lines" aria-hidden="true" data-calibration="${PROJECTION_VERSION}">${adminPaths}</g>`;
}

function writeHtml(payload, hydratedAtlas) {
  const htmlPath = path.join(ROOT, 'atlas-fresh.html');
  const before = fs.readFileSync(htmlPath, 'utf8');
  let html = replaceJsConstant(before, 'const atlasData = ', hydratedAtlas);

  const sourceIndexPath = path.join(ROOT, 'source-file-index.json');
  if (fs.existsSync(sourceIndexPath)) {
    const sourceIndex = JSON.parse(fs.readFileSync(sourceIndexPath, 'utf8'));
    html = replaceJsConstant(html, 'const sourceFileIndex = ', sourceIndex);
  }
  const sourceAvailabilityPath = path.join(ROOT, 'source-availability.json');
  if (fs.existsSync(sourceAvailabilityPath)) {
    const sourceAvailability = JSON.parse(fs.readFileSync(sourceAvailabilityPath, 'utf8'));
    html = replaceJsConstant(html, 'const sourceAvailabilityIndex = ', sourceAvailability);
  }

  const layerPattern = /<g[^>]*(?:id="countryLayer"|opacity="\.98")[^>]*><g class="continents">[\s\S]*?<\/g><\/g>\s*<g id="stateLines" class="state-lines(?: admin1-lines)?" aria-hidden="true"[^>]*>[\s\S]*?<\/g>/;
  if (!layerPattern.test(html)) throw new Error('Could not locate country/state SVG layer block in atlas-fresh.html');
  html = html.replace(layerPattern, mapMarkup(payload));

  html = html.replace(
    /(?:\.country-layer,\.continents,\.land\{pointer-events:none\}\n)*\.state-lines\{[^}]+\}\n\.us-state-line\{[^}]+\}/,
    `.country-layer,.continents,.land{pointer-events:none}\n.state-lines{pointer-events:none;opacity:var(--state-line-alpha,.30);transition:opacity .18s ease;mix-blend-mode:screen}\n.us-state-line{fill:none;stroke:rgba(132,213,244,.66);stroke-width:.062;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke;filter:drop-shadow(0 0 .35px rgba(66,216,255,.24))}`
  );

  html = html.replace(
    /const alpha=clamp\([^;]+\);/,
    'const alpha=clamp(0.28 + (state.zoom-1)*0.075, 0.28, 0.72);'
  );

  fs.writeFileSync(htmlPath, html);
}

const { payload, hydratedAtlas } = buildMapPayload();
writeJson('assets/generated/atlas-map.json', payload);
writeJson('assets/generated/atlas-data.generated.json', hydratedAtlas);

if (WRITE_HTML) {
  writeHtml(payload, hydratedAtlas);
}

console.log(JSON.stringify({
  generated: 'assets/generated/atlas-map.json',
  wroteHtml: WRITE_HTML,
  projection: payload.meta.projectionVersion,
  countryCount: payload.meta.countryCount,
  admin1Count: payload.meta.admin1Count,
  projectedCaseCount: payload.meta.projectedCaseCount,
  orbitalAggregateCount: payload.meta.orbitalAggregateCount,
}, null, 2));
