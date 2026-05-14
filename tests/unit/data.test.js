/**
 * Unit tests for docs/assets/js/data.js
 * Verifies the siteData object structure is complete and internally consistent.
 */

import { readFileSync } from 'fs';
import { resolve } from 'path';

// Load data.js in Node by stripping the window.siteData assignment and evaluating
const src = readFileSync(resolve('docs/assets/js/data.js'), 'utf8');
const siteData = (() => {
  const window = {};
  eval(src); // eslint-disable-line no-eval
  return window.siteData;
})();

// Single source of truth for expected counts.
// Update these when intentionally adding policy areas or foundations to data.js.
const POLICY_AREA_COUNT     = siteData.policyAreas.length;      // currently 26
const FOUNDATION_COUNT = siteData.foundations.length;  // currently 5

// ── FOUNDATIONS ──────────────────────────────────────────────────────────────

describe('siteData.foundations', () => {
  test(`has exactly ${FOUNDATION_COUNT} foundations`, () => {
    expect(siteData.foundations).toHaveLength(FOUNDATION_COUNT);
  });

  test.each(siteData.foundations)('foundation "$title" has all required fields', (f) => {
    expect(typeof f.id).toBe('string');
    expect(f.id.length).toBeGreaterThan(0);
    expect(typeof f.title).toBe('string');
    expect(typeof f.color).toBe('string');
    expect(f.color).toMatch(/^#[0-9a-fA-F]{3,6}$/);
    expect(Array.isArray(f.policyAreas)).toBe(true);
    expect(f.policyAreas.length).toBeGreaterThan(0);
    expect(Array.isArray(f.demands)).toBe(true);
    expect(Array.isArray(f.rejects)).toBe(true);
  });

  test('foundation IDs are unique', () => {
    const ids = siteData.foundations.map(f => f.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

// ── POLICY AREAS ──────────────────────────────────────────────────────────────

describe('siteData.policyAreas', () => {
  test(`has exactly ${POLICY_AREA_COUNT} policy areas`, () => {
    expect(siteData.policyAreas).toHaveLength(POLICY_AREA_COUNT);
  });

  test.each(siteData.policyAreas)('policy area "$title" has all required fields', (p) => {
    expect(typeof p.id).toBe('string');
    expect(p.id.length).toBeGreaterThan(0);
    expect(typeof p.title).toBe('string');
    expect(typeof p.foundation).toBe('string');
    expect(typeof p.summary).toBe('string');
    expect(p.summary.length).toBeGreaterThan(0);
    expect(Array.isArray(p.points)).toBe(true);
    expect(p.points.length).toBeGreaterThan(0);
  });

  test('policy area IDs are unique', () => {
    const ids = siteData.policyAreas.map(p => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  test('every policy area foundation ID resolves to a real foundation', () => {
    const foundationIds = new Set(siteData.foundations.map(f => f.id));
    siteData.policyAreas.forEach(p => {
      expect(foundationIds.has(p.foundation),
        `policy area "${p.id}" has unknown foundation "${p.foundation}"`
      ).toBe(true);
    });
  });

  test('all foundation.policy areas entries resolve to real policy area IDs', () => {
    const policyAreaIds = new Set(siteData.policyAreas.map(p => p.id));
    siteData.foundations.forEach(f => {
      f.policyAreas.forEach(pid => {
        expect(policyAreaIds.has(pid),
          `foundation "${f.id}" references unknown policy area "${pid}"`
        ).toBe(true);
      });
    });
  });
});

// ── HELPERS ───────────────────────────────────────────────────────────────────

describe('siteData.getFoundation()', () => {
  test('returns the correct foundation by ID', () => {
    const f = siteData.getFoundation('clean-democracy');
    expect(f).toBeDefined();
    expect(f.title).toBe('Clean Democracy');
  });

  test('returns undefined for an unknown ID', () => {
    expect(siteData.getFoundation('nonexistent')).toBeUndefined();
  });
});

describe('siteData.getPolicyAreasByFoundation()', () => {
  test('returns only policy areas belonging to the given foundation', () => {
    const policyAreas = siteData.getPolicyAreasByFoundation('freedom-to-thrive');
    expect(policyAreas.length).toBeGreaterThan(0);
    policyAreas.forEach(p => expect(p.foundation).toBe('freedom-to-thrive'));
  });

  test(`all ${POLICY_AREA_COUNT} policy areas are covered across foundations`, () => {
    const total = siteData.foundations.reduce((sum, f) =>
      sum + siteData.getPolicyAreasByFoundation(f.id).length, 0);
    expect(total).toBe(POLICY_AREA_COUNT);
  });

  test('returns empty array for unknown foundation', () => {
    expect(siteData.getPolicyAreasByFoundation('nonexistent')).toHaveLength(0);
  });
});

// ── WINDOW EXPOSURE ───────────────────────────────────────────────────────────

describe('window.siteData', () => {
  test('is exposed on window so app.js guard works', () => {
    expect(siteData).toBeDefined();
    expect(siteData.foundations).toBeDefined();
    expect(siteData.policyAreas).toBeDefined();
  });
});

// ── POLICYOS FAMILIES ─────────────────────────────────────────────────────────

describe('policyosFamilies', function () {
  it('is defined on siteData', function () {
    expect(siteData.policyosFamilies).toBeDefined();
  });

  it('has exactly 11 entries (System Principles only)', function () {
    // 11 PLOS families; Authoring OS families are not included in the JS runtime array
    expect(siteData.policyosFamilies).toHaveLength(11);
  });

  it('every entry has code, label, anchor, and summary', function () {
    siteData.policyosFamilies.forEach(function (f) {
      expect(f.code).toBeTruthy();
      expect(f.label).toBeTruthy();
      expect(f.anchor).toBeTruthy();
      expect(f.summary).toBeTruthy();
    });
  });

  it('KERN is the first family', function () {
    expect(siteData.policyosFamilies[0].code).toBe('KERN');
  });
});

// ── POLICYOS OVERLAYS ─────────────────────────────────────────────────────────

describe('policyosOverlays', function () {
  it('is defined on siteData', function () {
    expect(siteData.policyosOverlays).toBeDefined();
  });

  it('has exactly 25 policy area entries', function () {
    expect(Object.keys(siteData.policyosOverlays)).toHaveLength(25);
  });

  it('every entry is a non-empty array of {code, type} objects', function () {
    Object.values(siteData.policyosOverlays).forEach(function (overlays) {
      expect(overlays.length).toBeGreaterThan(0);
      overlays.forEach(function (o) {
        expect(o.code).toBeTruthy();
        expect(['mandatory', 'conditional']).toContain(o.type);
      });
    });
  });

  it('KERN is mandatory for every policy area', function () {
    Object.entries(siteData.policyosOverlays).forEach(function ([slug, overlays]) {
      var kern = overlays.find(function (o) { return o.code === 'KERN'; });
      expect(kern, slug + ' should have KERN overlay').toBeDefined();
      expect(kern.type).toBe('mandatory');
    });
  });
});
