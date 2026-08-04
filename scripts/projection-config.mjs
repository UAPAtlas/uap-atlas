export const VIEWBOX = { width: 100, height: 62 };
export const FIT_EXTENT = [[3, 4], [97, 58]];
export const PROJECTION = 'geoNaturalEarth1';
export const PROJECTION_VERSION = 'natural-earth-geoNaturalEarth1-fitExtent-v1';
export const COUNTRY_SOURCE = 'data/geo/ne_50m_admin_0_countries.geojson';
export const ADMIN1_SOURCE = 'data/geo/ne_50m_admin_1_states_provinces.geojson';

export function roundCoord(value) {
  return Number(value.toFixed(2));
}
