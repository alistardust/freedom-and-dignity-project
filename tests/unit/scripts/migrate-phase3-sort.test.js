import { CLASS_RENAMES } from '../../../scripts/migrate-policy-areas.js';

test('Phase 3 class renames are sorted longest-first', () => {
  const names = CLASS_RENAMES.map(([from]) => from);
  for (let i = 0; i < names.length - 1; i++) {
    expect(names[i].length).toBeGreaterThanOrEqual(names[i + 1].length);
  }
});

test('No class name in the rename list is a prefix of a longer class name that appears later', () => {
  const names = CLASS_RENAMES.map(([from]) => from);
  for (let i = 0; i < names.length; i++) {
    for (let j = i + 1; j < names.length; j++) {
      expect(names[j].startsWith(names[i])).toBe(false);
    }
  }
});
