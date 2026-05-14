/**
 * Unit tests for build-site.js helper functions.
 * Tests computeBase (url depth → base prefix) and computeCurrentPage (output path → href-relative path).
 */
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { computeBase, computeCurrentPage } = require('../../scripts/build-site.js');

describe('computeBase', () => {
  it('returns empty string for root-level pages', () => {
    expect(computeBase('docs/index.html')).toBe('');
    expect(computeBase('docs/problem.html')).toBe('');
    expect(computeBase('docs/policyos.html')).toBe('');
  });

  it('returns ../ for one-level subdirectory pages', () => {
    expect(computeBase('docs/policy/healthcare.html')).toBe('../');
    expect(computeBase('docs/compare/republican-party.html')).toBe('../');
  });

  it('returns ../../ for two-level subdirectory pages', () => {
    expect(computeBase('docs/foo/bar/baz.html')).toBe('../../');
  });
});

describe('computeCurrentPage', () => {
  it('returns bare filename for root-level pages', () => {
    expect(computeCurrentPage('docs/index.html')).toBe('index.html');
    expect(computeCurrentPage('docs/problem.html')).toBe('problem.html');
    expect(computeCurrentPage('docs/get-involved.html')).toBe('get-involved.html');
  });

  it('returns subdir/filename for subdirectory pages', () => {
    expect(computeCurrentPage('docs/policy/healthcare.html')).toBe('policy/healthcare.html');
    expect(computeCurrentPage('docs/compare/republican-party.html')).toBe('compare/republican-party.html');
  });
});
