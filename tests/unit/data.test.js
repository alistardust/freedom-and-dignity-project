/**
 * Unit tests for docs/assets/js/data.js
 * Verifies the ARP data structure is complete and internally consistent.
 */

import { readFileSync } from 'fs';
import { resolve } from 'path';

// Load data.js in Node by stripping the window.ARP assignment and evaluating
const src = readFileSync(resolve('docs/assets/js/data.js'), 'utf8');
const ARP = (() => {
  const window = {};
  eval(src); // eslint-disable-line no-eval
  return window.ARP;
})();

// ── FOUNDATIONS ──────────────────────────────────────────────────────────────

describe('ARP.foundations', () => {
  test('has exactly 5 foundations', () => {
    expect(ARP.foundations).toHaveLength(5);
  });

  test.each(ARP.foundations)('foundation "$title" has all required fields', (f) => {
    expect(typeof f.id).toBe('string');
    expect(f.id.length).toBeGreaterThan(0);
    expect(typeof f.title).toBe('string');
    expect(typeof f.color).toBe('string');
    expect(f.color).toMatch(/^#[0-9a-fA-F]{3,6}$/);
    expect(Array.isArray(f.pillars)).toBe(true);
    expect(f.pillars.length).toBeGreaterThan(0);
    expect(Array.isArray(f.demands)).toBe(true);
    expect(Array.isArray(f.rejects)).toBe(true);
  });

  test('foundation IDs are unique', () => {
    const ids = ARP.foundations.map(f => f.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

// ── PILLARS ───────────────────────────────────────────────────────────────────

describe('ARP.pillars', () => {
  test('has exactly 23 pillars', () => {
    expect(ARP.pillars).toHaveLength(23);
  });

  test.each(ARP.pillars)('pillar "$title" has all required fields', (p) => {
    expect(typeof p.id).toBe('string');
    expect(p.id.length).toBeGreaterThan(0);
    expect(typeof p.title).toBe('string');
    expect(typeof p.foundation).toBe('string');
    expect(typeof p.summary).toBe('string');
    expect(p.summary.length).toBeGreaterThan(0);
    expect(Array.isArray(p.points)).toBe(true);
    expect(p.points.length).toBeGreaterThan(0);
  });

  test('pillar IDs are unique', () => {
    const ids = ARP.pillars.map(p => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  test('every pillar foundation ID resolves to a real foundation', () => {
    const foundationIds = new Set(ARP.foundations.map(f => f.id));
    ARP.pillars.forEach(p => {
      expect(foundationIds.has(p.foundation),
        `pillar "${p.id}" has unknown foundation "${p.foundation}"`
      ).toBe(true);
    });
  });

  test('all foundation.pillars entries resolve to real pillar IDs', () => {
    const pillarIds = new Set(ARP.pillars.map(p => p.id));
    ARP.foundations.forEach(f => {
      f.pillars.forEach(pid => {
        expect(pillarIds.has(pid),
          `foundation "${f.id}" references unknown pillar "${pid}"`
        ).toBe(true);
      });
    });
  });
});

// ── HELPERS ───────────────────────────────────────────────────────────────────

describe('ARP.getFoundation()', () => {
  test('returns the correct foundation by ID', () => {
    const f = ARP.getFoundation('clean-democracy');
    expect(f).toBeDefined();
    expect(f.title).toBe('Clean Democracy');
  });

  test('returns undefined for an unknown ID', () => {
    expect(ARP.getFoundation('nonexistent')).toBeUndefined();
  });
});

describe('ARP.getPillarsByFoundation()', () => {
  test('returns only pillars belonging to the given foundation', () => {
    const pillars = ARP.getPillarsByFoundation('freedom-to-thrive');
    expect(pillars.length).toBeGreaterThan(0);
    pillars.forEach(p => expect(p.foundation).toBe('freedom-to-thrive'));
  });

  test('all 23 pillars are covered across foundations', () => {
    const total = ARP.foundations.reduce((sum, f) =>
      sum + ARP.getPillarsByFoundation(f.id).length, 0);
    expect(total).toBe(23);
  });

  test('returns empty array for unknown foundation', () => {
    expect(ARP.getPillarsByFoundation('nonexistent')).toHaveLength(0);
  });
});

// ── WINDOW EXPOSURE ───────────────────────────────────────────────────────────

describe('window.ARP', () => {
  test('is exposed on window so app.js guard works', () => {
    expect(ARP).toBeDefined();
    expect(ARP.foundations).toBeDefined();
    expect(ARP.pillars).toBeDefined();
  });
});
