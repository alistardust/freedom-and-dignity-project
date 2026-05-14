'use strict';

const fs   = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..', 'src', 'pages', 'policy');

/**
 * Returns the file content with all card status markers removed:
 *   - class="policy-card STATUS"  ->  class="policy-card"
 *   - <span class="rule-badge">...</span>  ->  (removed)
 *   - <div class="rule-status">...</div>   ->  (removed)
 */
function stripStatusMarkersFromContent(content) {
  // Remove status modifier from policy-card class attribute.
  // Handles: status-included, status-updated, status-partial, status-missing,
  //          status-proposed, proposal, and any other status-* variant.
  let result = content.replace(
    /class="policy-card (?:status-[a-z-]+|proposal)"/g,
    'class="policy-card"'
  );

  // Remove <span class="rule-badge">...</span> (single line, no nesting).
  result = result.replace(/<span class="rule-badge">[^<]*<\/span>\n?/g, '');

  // Remove <div class="rule-status">...</div> (single line, no nesting).
  result = result.replace(/<div class="rule-status">[^<]*<\/div>\n?/g, '');

  // Validate: fail loudly if any markers remain (malformed HTML)
  const remaining = [];
  if (result.match(/<span class="rule-badge">/)) remaining.push('rule-badge spans');
  if (result.match(/<div class="rule-status">/)) remaining.push('rule-status divs');
  if (result.match(/class="policy-card (?:status-[a-z-]+|proposal)"/)) remaining.push('status class modifiers');
  if (remaining.length > 0) {
    throw new Error(`Failed to strip: ${remaining.join(', ')} (malformed HTML?)`);
  }

  return result;
}

function main() {
  const files = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.njk'));
  let totalFiles = 0;
  let totalChanges = 0;

  for (const file of files) {
    const filePath = path.join(SRC_DIR, file);
    const original = fs.readFileSync(filePath, 'utf8');
    const updated  = stripStatusMarkersFromContent(original);

    if (updated !== original) {
      fs.writeFileSync(filePath, updated, 'utf8');
      totalFiles++;
      // Count replacements (approximate: lines changed).
      const origLines = original.split('\n');
      const updLines  = updated.split('\n');
      totalChanges += Math.abs(origLines.length - updLines.length);
      console.log(`  updated: ${file}`);
    } else {
      console.log(`  no change: ${file}`);
    }
  }

  console.log(`\nDone. Modified ${totalFiles} files, ~${totalChanges} lines removed.`);
}

if (require.main === module) {
  main();
}

module.exports = { stripStatusMarkersFromContent };
