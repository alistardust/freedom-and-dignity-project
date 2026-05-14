/**
 * Shared constants for Playwright E2E specs.
 * Imported by site.spec.js and mobile.spec.js.
 */

// Each entry: { slug: string, title: string }
// slug matches the filename at docs/policy/<slug>.html
const SAMPLE_POLICY_AREAS = [
  { slug: 'executive-power',               title: 'Executive Power' },
  { slug: 'elections-and-representation',  title: 'Elections' },
  { slug: 'anti-corruption',               title: 'Anti-Corruption' },
  { slug: 'equal-justice-and-policing',    title: 'Equal Justice' },
  { slug: 'rights-and-civil-liberties',    title: 'Rights' },
  { slug: 'courts-and-judicial-system',    title: 'Courts' },
  { slug: 'checks-and-balances',           title: 'Checks' },
  { slug: 'taxation-and-wealth',           title: 'Taxation' },
  { slug: 'healthcare',                    title: 'Healthcare' },
  { slug: 'antitrust-and-corporate-power', title: 'Antitrust' },
  { slug: 'information-and-media',         title: 'Information' },
  { slug: 'gun-policy',                    title: 'Gun Policy' },
  { slug: 'term-limits-and-fitness',       title: 'Term Limits' },
  { slug: 'administrative-state',          title: 'Administrative' },
  { slug: 'technology-and-ai',             title: 'Technology' },
  { slug: 'immigration',                   title: 'Immigration' },
  { slug: 'environment-and-agriculture',   title: 'Environment' },
  { slug: 'education',                     title: 'Education' },
  { slug: 'labor-and-workers-rights',      title: 'Labor' },
  { slug: 'housing',                       title: 'Housing' },
  { slug: 'consumer-rights',               title: 'Consumer' },
  { slug: 'data-rights-and-privacy',       title: 'Data Rights' },
  { slug: 'legislative-reform',            title: 'Legislative' },
  { slug: 'foreign-policy',                title: 'Foreign Policy' },
  { slug: 'science-technology-space',      title: 'Science Technology Space' },
];

module.exports = { SAMPLE_POLICY_AREAS };
