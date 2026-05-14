'use strict';

const fs   = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const SRC_DIR = path.join(__dirname, '..', 'src', 'pages', 'policy');
const DB_PATH = path.join(__dirname, '..', 'policy', 'catalog', 'policy_catalog_v2.sqlite');

/**
 * Extract all policy-card div blocks from content.
 * Uses nesting depth counting to correctly handle nested divs inside cards
 * (e.g. rule-header, rule-body). A naive regex would stop at the first
 * nested </div>, capturing only the rule-header fragment.
 */
function extractCardBlocks(content) {
  const blocks = [];
  let searchFrom = 0;

  while (true) {
    const startIdx = content.indexOf('<div class="policy-card"', searchFrom);
    if (startIdx === -1) break;

    let depth = 0;
    let i = startIdx;

    while (i < content.length) {
      if (content.startsWith('<div', i) && (content[i + 4] === ' ' || content[i + 4] === '>' || content[i + 4] === '\n' || content[i + 4] === '\t')) {
        depth++;
        i += 4;
      } else if (content.startsWith('</div>', i)) {
        depth--;
        if (depth === 0) {
          blocks.push(content.slice(startIdx, i + 6));
          searchFrom = i + 6;
          break;
        }
        i += 6;
      } else {
        i++;
      }
    }

    if (depth !== 0) break; // malformed HTML, stop searching
  }

  return blocks;
}

/**
 * Parse all policy cards from a .njk file.
 * Returns an array of { id, ruleNotes } objects.
 * Only returns cards that have a rule-notes paragraph AND no rule-body paragraph
 * (rule-body presence = proposal card, handled in Phase 4, not here).
 */
function parseCards(content) {
  const cards = [];

  for (const block of extractCardBlocks(content)) {
    const idMatch = block.match(/id="([^"]+)"/);
    if (!idMatch) continue;
    const cardId = idMatch[1];

    // Skip proposal cards (have rule-body, regardless of any additional classes).
    if (block.includes('class="rule-body')) continue;

    // Extract rule-notes text (may span multiple lines).
    const notesMatch = block.match(/<p class="rule-notes">([\s\S]*?)<\/p>/);
    if (!notesMatch) continue;

    cards.push({ id: cardId, ruleNotes: notesMatch[1].trim() });
  }

  return cards;
}

function main() {
  const db = new Database(DB_PATH);

  const files = fs.readdirSync(SRC_DIR).filter(f => f.endsWith('.njk'));
  const unmatched = [];
  let totalUpdated = 0;

  try {
    // Prepare inside try so any schema error (e.g. Phase 1 not run) closes the DB cleanly.
    const updateStmt = db.prepare('UPDATE positions SET rule_notes = ? WHERE id = ?');

    for (const file of files) {
      const filePath = path.join(SRC_DIR, file);
      const content  = fs.readFileSync(filePath, 'utf8');
      const cards    = parseCards(content);

      for (const { id, ruleNotes } of cards) {
        const result = updateStmt.run(ruleNotes, id);
        if (result.changes === 0) {
          unmatched.push({ file, id });
        } else {
          totalUpdated++;
        }
      }
    }
  } finally {
    db.close();
  }

  console.log(`\nUpdated ${totalUpdated} rows in DB.`);

  if (unmatched.length > 0) {
    console.warn(`\nWARNING: ${unmatched.length} card IDs found in HTML with no matching DB row:`);
    for (const { file, id } of unmatched) {
      console.warn(`  [${file}] ${id}`);
    }
    console.warn('\nThese IDs should be investigated and backfilled into the DB manually,');
    console.warn('or tracked as known gaps before Phase 4 begins.');
  } else {
    console.log('All IDs matched successfully.');
  }
}

if (require.main === module) {
  main();
}

module.exports = { extractCardBlocks, parseCards };
