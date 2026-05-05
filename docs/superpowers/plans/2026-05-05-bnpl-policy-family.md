# BNPL Policy Family Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the nine-card BNPL policy family to the Consumer Rights pillar, retire CNSR-PDLS-0007, and backfill all changes into the SQLite catalog.

**Architecture:** Three parallel changes that must land in a single commit: (1) SQLite DB insert of the BNPL subdomain and nine positions plus legacy map update; (2) HTML removal of the retired CNSR-PDLS-0007 card and insertion of the new BNPL family block; (3) E2E test assertions verifying the new family renders and the retired card is gone. Cross-reference additions to five existing cards are included in the same HTML commit.

**Tech Stack:** SQLite (sqlite3 CLI), HTML, Playwright (E2E), Vitest (unit, no changes needed)

---

## Chunk 1: E2E Test Scaffolding and DB Changes

### Task 1: Write failing E2E tests for the BNPL family

**Files:**
- Modify: `tests/e2e/site.spec.js`

- [ ] **Step 1.1: Add the BNPL describe block to site.spec.js**

Insert this block immediately after the closing `}` of the last `for` loop block (after line 153, before the `// ── COMPARE PAGES` comment):

```javascript
// ── CONSUMER RIGHTS — BNPL FAMILY ────────────────────────────────────────────

test.describe('Consumer Rights — BNPL family', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/pillars/consumer-rights.html');
  });

  test('BNPL family section is present', async ({ page }) => {
    // fam-con-bnpl inserted after PDL family, before CFP family
    await expect(page.locator('#fam-con-bnpl')).toBeAttached();
  });

  test('all 9 BNPL policy card IDs render', async ({ page }) => {
    for (const cardId of [
      'CNSR-BNPL-0001', 'CNSR-BNPL-0002', 'CNSR-BNPL-0003',
      'CNSR-BNPL-0004', 'CNSR-BNPL-0005', 'CNSR-BNPL-0006',
      'CNSR-BNPL-0007', 'CNSR-BNPL-0008', 'CNSR-BNPL-0009',
    ]) {
      await expect(page.locator(`#${cardId}`)).toBeAttached();
    }
  });

  test('retired CNSR-PDLS-0007 card is absent', async ({ page }) => {
    await expect(page.locator('#CNSR-PDLS-0007')).not.toBeAttached();
  });
});
```

- [ ] **Step 1.2: Run E2E tests to confirm the new assertions fail**

```bash
npm run test:e2e -- --grep "BNPL family"
```

Expected output: 3 tests fail. "BNPL family section is present" and "all 9 BNPL policy card IDs render" fail because the HTML does not yet have the family. "retired CNSR-PDLS-0007 card is absent" fails because CNSR-PDLS-0007 still exists.

---

### Task 2: Insert BNPL subdomain and nine positions into the DB

**Files:**
- Modify: `policy/catalog/policy_catalog_v2.sqlite` (via sqlite3 CLI)

- [ ] **Step 2.1: Insert BNPL subdomain and all nine positions in one atomic transaction**

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite <<'SQL'
BEGIN;

INSERT INTO subdomains (code, domain, name)
VALUES ('BNPL', 'CNSR', 'Buy Now, Pay Later');

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0001', 'CNSR', 'BNPL', 1,
  'BNPL products classified as consumer credit in two tiers: Tier 1 simplified rules, Tier 2 full underwriting',
  'Buy-now-pay-later products -- including pay-in-four, deferred-payment, and point-of-sale installment credit products -- constitute consumer credit subject to the Truth in Lending Act (15 U.S.C. § 1601 et seq.) and the Equal Credit Opportunity Act (15 U.S.C. § 1691 et seq.) without exception based on product structure, term length, number of payments, or fee model. BNPL products are classified into two tiers: Tier 1 (four or fewer payments and four weeks or fewer in duration) and Tier 2 (more than four payments or more than four weeks in duration). Tier 1 lenders must comply with Sections 0002, 0004, 0005, 0006, 0007, 0008, and 0009. Tier 2 lenders must comply with all sections including 0003. No BNPL lender may initiate or continue debt collection activity on a disputed transaction while a consumer dispute is pending resolution under TILA Section 170 or ECOA. Violations give rise to private rights of action under the applicable statutes, including class action rights.',
  'Buy-now-pay-later services are consumer credit and must follow the same protection rules as other lending. Short-term zero-interest plans (Tier 1) have streamlined rules; longer-term plans (Tier 2) require income verification and have a 10% interest cap.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0002', 'CNSR', 'BNPL', 2,
  'BNPL lenders must report all originations, payment history, and defaults to all three major consumer credit bureaus',
  'Every BNPL lender must report all originations, payment history, and defaults for all Tier 1 and Tier 2 loans to all three major consumer credit bureaus within 30 days of origination. Reporting must continue on a monthly basis for the life of the loan. Borrowers may not waive this reporting requirement as a condition of loan origination or at any subsequent time. Dispute rights under the Fair Credit Reporting Act (15 U.S.C. § 1681 et seq.) apply to BNPL tradelines in the same manner as any other credit tradeline. Lenders must furnish corrected information to credit bureaus within 30 days of receiving a valid consumer dispute.',
  'Every BNPL loan must be reported to the credit bureaus. Lenders cannot hide your debt from other lenders. This prevents people from taking on more debt than they can handle across multiple BNPL services at once.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0003', 'CNSR', 'BNPL', 3,
  'Tier 2 BNPL loans require documented affordability assessment with income verification and 43% DTI cap',
  'Before originating any Tier 2 BNPL loan, the lender must: (1) verify the borrower''s income through a documented source that is not entirely self-reported (acceptable sources include bank statement analysis, payroll data, tax returns, or third-party income verification services); (2) calculate the borrower''s total monthly debt obligations including the proposed BNPL loan; and (3) confirm that total debt obligations do not exceed 43% of verified monthly gross income (DTI cap). The lender must retain affordability assessment documentation for a minimum of three years from origination and must provide it to the CFPB or state regulator upon request. Originating a Tier 2 loan without documented affordability assessment constitutes an unfair, deceptive, or abusive act or practice under 12 U.S.C. § 5531.',
  'For BNPL plans lasting longer than 4 payments or 4 weeks, lenders must verify that you can actually afford to repay. They have to check your income and your existing debts before approving the loan.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0004', 'CNSR', 'BNPL', 4,
  'BNPL lenders may not assess any fee for missed, late, or returned payments; statutory penalty of $500 per violation',
  'No BNPL lender may assess any fee of any kind in connection with a missed, late, or returned payment, regardless of how that fee is labeled or structured. This prohibition applies to all Tier 1 and Tier 2 products and may not be waived by contract or by borrower agreement. Default consequences are limited to: adverse credit bureau reporting under Section 0002, suspension or closure of the borrower''s BNPL account, and civil collection action permitted under applicable state law. Charging a prohibited fee constitutes an unfair, deceptive, or abusive act or practice under 12 U.S.C. § 5531. Charging a prohibited fee also gives rise to a private right of action for actual damages, a statutory penalty of $500 per violation, and reasonable attorney fees and costs; this right of action arises independently of TILA''s finance charge definition, which does not encompass late payment charges under Regulation Z 12 C.F.R. § 1026.4(c)(2).',
  'BNPL lenders cannot charge fees for missed or late payments -- period. If you miss a payment, the consequences are the same as any other debt: credit damage, account closure, and collection. There is no fee.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0005', 'CNSR', 'BNPL', 5,
  'Tier 1 BNPL must carry 0% APR; Tier 2 BNPL may not exceed 10% APR inclusive of all fees; cap is uniform',
  'Tier 1 BNPL products must carry a 0% annual percentage rate, inclusive of all fees. No charge of any kind may be assessed on a Tier 1 product except the principal amount of the purchase, and any such charge must be included in the APR calculation. Tier 2 BNPL products may not carry an annual percentage rate exceeding 10%, inclusive of all fees and charges. The APR cap applies uniformly and may not vary by borrower credit score, creditworthiness assessment, or any characteristic of the borrower. APR must be calculated and disclosed in TILA-compliant format before the consumer completes the purchase transaction. Lenders may not circumvent the rate cap through fee structures, add-on products, or product recharacterization.',
  'Short-term BNPL (Tier 1) must always be zero percent interest. Longer-term BNPL (Tier 2) cannot charge more than 10% annual interest. The rate cannot change based on your credit score.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0006', 'CNSR', 'BNPL', 6,
  'BNPL payment due dates must be aligned to the borrower''s documented income pay cycle; frequency set at origination',
  'Before originating any BNPL loan, the lender must document the borrower''s income payment cycle (weekly, bi-weekly, semi-monthly, or monthly) and set payment due dates aligned to that cycle. The lender may not impose a payment frequency that does not correspond to the borrower''s documented pay cycle. Borrowers must be offered the option to choose weekly, bi-weekly, semi-monthly, or monthly payment schedules at origination; this choice must be confirmed in writing and must appear in the loan agreement. Payment frequency may not be modified by the lender after origination without the borrower''s written consent. Pay cycle documentation is retained as part of the origination record and subject to CFPB examination.',
  'Your BNPL payments must be scheduled to match when you actually get paid. If you''re paid monthly, your payments cannot be set to weekly. You choose the schedule at the start.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0007', 'CNSR', 'BNPL', 7,
  'CFPB must operate a real-time BNPL registry; lenders must query before origination and report within one hour',
  'The CFPB must operate a centralized, real-time BNPL loan registry. Before originating any BNPL loan (Tier 1 or Tier 2), the lender must query the registry and receive a confirmation code. Every origination must be reported to the registry within one hour of closing. In the event of a documented registry system outage, lenders may proceed on a 24-hour delayed reporting basis, with the outage documented in lender records and reported to the CFPB. The registry is non-public and accessible only to BNPL lenders for origination query purposes. A federal default aggregate limit of $2,500 applies to borrowers with a FICO score below 620, with no FICO score on file, or with an equivalent score from an alternative scoring model that falls below the equivalent of a 620 FICO; originating a loan that would exceed this limit without affirmative documented underwriting justification constitutes an unfair, deceptive, or abusive act or practice. Lenders may impose lower or higher aggregate limits above the federal floor through their own underwriting policies, subject to CFPB guidelines. Within 90 days of the end of the first full calendar quarter of registry operation, the CFPB must publish a baseline report documenting the number of Tier 2 BNPL originations to borrowers with FICO scores below 620 or no FICO score on file in that quarter; this baseline is the reference point for all subsequent market monitoring. If the number of such originations drops more than 25% in any rolling 18-month period measured quarterly against that baseline, the CFPB must report to Congress within 60 days describing market conditions and recommending corrective action.',
  'A government registry tracks all active BNPL loans in real time. Before approving a new loan, every BNPL lender must check the registry to see how much you already owe across all BNPL services. This prevents debt from stacking up across multiple providers.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0008', 'CNSR', 'BNPL', 8,
  'BNPL checkout must ban countdown timers and pre-selection and require three disclosures before purchase',
  'BNPL lenders and merchants integrating BNPL at point of sale are jointly responsible for compliance with the following design requirements. Prohibited design elements: countdown timers of any kind associated with BNPL offers; false scarcity signals implying BNPL availability is limited or time-sensitive; and pre-selection of BNPL as the default payment method. Required disclosures before the consumer completes a purchase: (1) the total cost of the purchase expressed as a single dollar amount, not framed as installment amounts; (2) the complete payment schedule including all due dates and amounts; and (3) the borrower''s current aggregate BNPL debt balance across all providers as reported by the real-time registry under Section 0007. BNPL must be displayed with visual prominence equal to or less than credit card and debit card payment options; BNPL may not receive preferential placement, larger button size, brighter color treatment, or other visual design advantage. Violations of this section by either the BNPL lender or the merchant constitute unfair, deceptive, or abusive acts or practices.',
  'BNPL checkout cannot use countdown timers, fake ''limited time'' pressure, or pre-selected BNPL as the default payment option. Before you confirm a purchase, you must see the total cost, your full payment schedule, and how much BNPL debt you already have.',
  0, 'PROPOSED'
);

INSERT INTO positions (id, domain, subdomain, seq, short_title, full_statement, plain_language, is_cross_domain, status)
VALUES (
  'CNSR-BNPL-0009', 'CNSR', 'BNPL', 9,
  'BNPL lenders may not charge small merchants more than 60% of the large-merchant fee rate for the same product',
  'BNPL lenders may not charge small merchants a merchant fee rate greater than 60% of the merchant fee rate charged to large merchants for the same BNPL product tier and term structure. The reference rate for this comparison is the large-merchant rate published on the lender''s quarterly fee schedule under this section; if the lender publishes a rate range rather than a single rate, the reference rate is the midpoint of that range. A "small merchant" is defined as any merchant whose parent company or controlling entity has total annual revenue below $5 million, as established by the most recently filed federal business tax return. Aggregate parent-company or controlling-entity revenue is used to determine size classification; entities may not achieve small-merchant status through subsidiary or affiliate structuring that reduces individual-entity revenue below the threshold. BNPL lenders must publish their merchant fee schedules, including the small-merchant rate and large-merchant rate, on a publicly accessible webpage updated no less than quarterly. BNPL lenders may not refuse to provide BNPL services to small merchants solely on the basis of transaction volume. The merchant fee tiering requirement is a condition of BNPL lender registration and supervision under CFPB authority (12 U.S.C. § 5512); it applies as a regulatory obligation on covered persons providing consumer financial products or services, with the consumer-facing purpose of ensuring small business merchant access to payment infrastructure that serves those businesses'' consumer customers. Enforcement authority is held jointly by the CFPB under 12 U.S.C. § 5512 and by the FTC under Section 5 of the FTC Act (15 U.S.C. § 45) as an unfair method of competition affecting commerce. Civil penalties of up to $10,000 per merchant per calendar year apply for violations of the fee-tiering requirement.',
  'BNPL lenders must charge small businesses (under $5 million in annual revenue) no more than 60% of the rate they charge large businesses. This lets small businesses afford BNPL without subsidizing it from tax revenue.',
  0, 'PROPOSED'
);

COMMIT;
SQL
```

- [ ] **Step 2.2: Verify all nine positions and the subdomain inserted correctly**

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite \
  "SELECT id, seq, status, substr(short_title,1,60) FROM positions WHERE subdomain='BNPL' ORDER BY seq;"
```

Expected output: 9 rows, ids CNSR-BNPL-0001 through 0009, all status=PROPOSED.

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite \
  "SELECT code, domain, name FROM subdomains WHERE code='BNPL';"
```

Expected output: `BNPL|CNSR|Buy Now, Pay Later`

---

### Task 3: Update the legacy map and deprecate CNSR-PDLS-0007

**Files:**
- Modify: `policy/catalog/policy_catalog_v2.sqlite` (via sqlite3 CLI)

The current legacy_id_map has a self-referential row: old_id=CNSR-PDLS-0007 → new_id=CNSR-PDLS-0007. Update it to point to CNSR-BNPL-0001 and deprecate the position.

- [ ] **Step 3.1: Update legacy map and deprecate position in one transaction**

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite <<'SQL'
BEGIN;

UPDATE legacy_id_map
SET new_id = 'CNSR-BNPL-0001',
    notes  = 'Retired; superseded by CNSR-BNPL-0001 (full BNPL policy family)'
WHERE old_id = 'CNSR-PDLS-0007';

UPDATE positions
SET status     = 'DEPRECATED',
    updated_at = datetime('now')
WHERE id = 'CNSR-PDLS-0007';

COMMIT;
SQL
```

- [ ] **Step 3.2: Verify**

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite \
  "SELECT old_id, new_id, notes FROM legacy_id_map WHERE old_id='CNSR-PDLS-0007';"
```

Expected: `CNSR-PDLS-0007|CNSR-BNPL-0001|Retired; superseded by CNSR-BNPL-0001 (full BNPL policy family)`

```bash
sqlite3 policy/catalog/policy_catalog_v2.sqlite \
  "SELECT id, status FROM positions WHERE id='CNSR-PDLS-0007';"
```

Expected: `CNSR-PDLS-0007|DEPRECATED`

- [ ] **Step 3.3: Commit DB changes**

Note: `tests/e2e/site.spec.js` was modified in Task 1 but is committed in Chunk 2 Task 8 together with the HTML changes. This commit covers only the DB.

```bash
git add policy/catalog/policy_catalog_v2.sqlite
git commit -m "feat(db): add BNPL subdomain and 9 positions; retire CNSR-PDLS-0007

- Insert BNPL subdomain into subdomains table
- Insert CNSR-BNPL-0001 through 0009 (status: PROPOSED)
- Update legacy_id_map: CNSR-PDLS-0007 -> CNSR-BNPL-0001
- Deprecate CNSR-PDLS-0007

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Chunk 2: HTML Changes, Cross-References, and Final Verification

### Task 4: Remove CNSR-PDLS-0007 from HTML and update counts

**Files:**
- Modify: `docs/pillars/consumer-rights.html`

The PDL family currently shows `0/7 active` and includes 7 cards (PDLS-0001 through 0007). Removing CNSR-PDLS-0007 reduces it to 6. The stats-bar currently reads Total: 134, Active: 78, Proposed: 56. After removing 1 proposal and adding 9 proposals: Total: 142, Active: 78, Proposed: 64.

- [ ] **Step 4.1: Remove the CNSR-PDLS-0007 card block**

Delete the entire block from `docs/pillars/consumer-rights.html` (currently lines 1504-1514):

```html
<div class="policy-card proposal" id="CNSR-PDLS-0007">
<div class="rule-header">
<code class="rule-id">CNSR-PDLS-0007</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Buy-now-pay-later products are consumer credit subject to TILA and ECOA; mandatory APR disclosure required; no debt collection while a consumer dispute is pending</p>
<p class="rule-plain">'Buy now, pay later' services are subject to the same consumer protection rules as credit cards — they must disclose the true cost in APR terms and cannot collect debt while a consumer dispute is pending.</p>
<p class="rule-stmt">Buy-now-pay-later products — including pay-in-four, deferred-payment, and point-of-sale installment credit products — constitute consumer credit subject to the Truth in Lending Act (15 U.S.C. § 1601 et seq.) and the Equal Credit Opportunity Act (15 U.S.C. § 1691 et seq.) without exception based on product structure, term length, or number of payments. BNPL lenders must disclose the effective annual percentage rate of the product — including all fees — in TILA-compliant format before the consumer completes the purchase transaction. No BNPL lender may initiate or continue debt collection activity on a disputed transaction while a consumer dispute is pending resolution. TILA and ECOA violations by BNPL lenders give rise to private rights of action under the applicable statutes, including class action rights.</p>
<p class="rule-notes">BNPL products proliferated partly by structuring payments as installment loans to avoid TILA's open-end credit disclosure requirements. The CFPB's 2022 BNPL market monitoring report found that BNPL users skew toward younger, lower-income, and financially fragile populations. <!-- [VERIFY] --> The CFPB issued interpretive guidance in 2024 indicating BNPL lenders are card issuers under TILA, but interpretive letters are less durable than statutory mandates and are easily reversed by a subsequent administration. Cross-reference: CNSR-PDLS-0001 (usury cap), CNSR-CFPS-0005 (CFPB jurisdiction expansion).</p>
</div>
```

- [ ] **Step 4.2: Update PDL family-count from 0/7 to 0/6**

Change:
```html
<span class="family-count">0/7 active</span>
```
To:
```html
<span class="family-count">0/6 active</span>
```

- [ ] **Step 4.3: Update the stats-bar counts**

Change (at the top of the `#pil-intro` section):
```html
<div class="stat-item"><span class="stat-num">134</span><span class="stat-label">Total Positions</span></div>
<div class="stat-item"><span class="stat-num" style="color:#1e8449">78</span><span class="stat-label">Active</span></div>
<div class="stat-item"><span class="stat-num" style="color:#c9952a">0</span><span class="stat-label">Partial</span></div>
<div class="stat-item"><span class="stat-num" style="color:#888">56</span><span class="stat-label">Proposed</span></div>
```
To:
```html
<div class="stat-item"><span class="stat-num">142</span><span class="stat-label">Total Positions</span></div>
<div class="stat-item"><span class="stat-num" style="color:#1e8449">78</span><span class="stat-label">Active</span></div>
<div class="stat-item"><span class="stat-num" style="color:#c9952a">0</span><span class="stat-label">Partial</span></div>
<div class="stat-item"><span class="stat-num" style="color:#888">64</span><span class="stat-label">Proposed</span></div>
```

---

### Task 5: Insert the BNPL family HTML block

**Files:**
- Modify: `docs/pillars/consumer-rights.html`

Insert the entire block below immediately before the line:
```html
<div class="policy-family" id="fam-con-cfp">
```

(Currently at line 1517, immediately after the PDL family's closing `</div></div>`)

- [ ] **Step 5.1: Insert the complete BNPL family block**

```html
<div class="policy-family" id="fam-con-bnpl">
<div class="family-header">
<span class="family-code">CON</span>
<span class="family-title">BNPL — Buy Now, Pay Later Regulation</span>
<span class="family-count">0/9 active</span>
</div>
<div class="rule-grid">
<div class="policy-card proposal" id="CNSR-BNPL-0001">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Buy-now-pay-later products are consumer credit subject to TILA and ECOA; two-tier framework classifies all BNPL products</p>
<p class="rule-plain">Buy-now-pay-later services are consumer credit and must follow the same protection rules as other lending. Short-term zero-interest plans (Tier 1) have streamlined rules; longer-term plans (Tier 2) require income verification and have a 10% interest cap.</p>
<p class="rule-stmt">Buy-now-pay-later products -- including pay-in-four, deferred-payment, and point-of-sale installment credit products -- constitute consumer credit subject to the Truth in Lending Act (15 U.S.C. § 1601 et seq.) and the Equal Credit Opportunity Act (15 U.S.C. § 1691 et seq.) without exception based on product structure, term length, number of payments, or fee model. BNPL products are classified into two tiers: Tier 1 (four or fewer payments and four weeks or fewer in duration) and Tier 2 (more than four payments or more than four weeks in duration). Tier 1 lenders must comply with Sections 0002, 0004, 0005, 0006, 0007, 0008, and 0009. Tier 2 lenders must comply with all sections including 0003. No BNPL lender may initiate or continue debt collection activity on a disputed transaction while a consumer dispute is pending resolution under TILA Section 170 or ECOA. Violations give rise to private rights of action under the applicable statutes, including class action rights.</p>
<p class="rule-notes">BNPL products proliferated partly by structuring installment loans to avoid TILA open-end credit disclosure requirements. The CFPB issued interpretive guidance in 2024 classifying BNPL lenders as card issuers under TILA, but interpretive letters are less durable than statutory mandates and were rescinded in 2025. Statutory classification eliminates the structuring incentive. The two-tier framework follows the model identified in CFPB (2025) and Richmond Fed (2026) research distinguishing short-term, zero-interest pay-in-four from longer-term interest-bearing installment products. Cross-reference: CNSR-CFPS-0005 (CFPB jurisdiction), CNSR-CFPS-0003 (private right of action baseline).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0002">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">BNPL lenders must report all originations, payment history, and defaults to all three major consumer credit bureaus within 30 days</p>
<p class="rule-plain">Every BNPL loan must be reported to the credit bureaus. Lenders cannot hide your debt from other lenders. This prevents people from taking on more debt than they can handle across multiple BNPL services at once.</p>
<p class="rule-stmt">Every BNPL lender must report all originations, payment history, and defaults for all Tier 1 and Tier 2 loans to all three major consumer credit bureaus within 30 days of origination. Reporting must continue on a monthly basis for the life of the loan. Borrowers may not waive this reporting requirement as a condition of loan origination or at any subsequent time. Dispute rights under the Fair Credit Reporting Act (15 U.S.C. § 1681 et seq.) apply to BNPL tradelines in the same manner as any other credit tradeline. Lenders must furnish corrected information to credit bureaus within 30 days of receiving a valid consumer dispute.</p>
<p class="rule-notes">CFPB (2025) found 63% of BNPL borrowers carry simultaneous loans; 32% hold loans across multiple firms in the same period. Without mandatory reporting, underwriting decisions are made with incomplete debt pictures -- a structural feature of the current market that enables approval of borrowers who would fail affordability assessment with full visibility. Richmond Fed (2026) documents BNPL approval rate growth from 56% (2019) to 79% (2022) driven by loosened underwriting, not improved risk selection. Mandatory reporting enables affordability assessment to function and reduces systemic risk from loan stacking. Cross-reference: CNSR-CRDS-0001 (credit reporting accuracy baseline), CNSR-BNPL-0007 (real-time registry).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0003">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Tier 2 BNPL loans require documented affordability assessment with income verification and 43% DTI cap before origination</p>
<p class="rule-plain">For BNPL plans lasting longer than 4 payments or 4 weeks, lenders must verify that you can actually afford to repay. They have to check your income and your existing debts before approving the loan.</p>
<p class="rule-stmt">Before originating any Tier 2 BNPL loan, the lender must: (1) verify the borrower's income through a documented source that is not entirely self-reported (acceptable sources include bank statement analysis, payroll data, tax returns, or third-party income verification services); (2) calculate the borrower's total monthly debt obligations including the proposed BNPL loan; and (3) confirm that total debt obligations do not exceed 43% of verified monthly gross income (DTI cap). The lender must retain affordability assessment documentation for a minimum of three years from origination and must provide it to the CFPB or state regulator upon request. Originating a Tier 2 loan without documented affordability assessment constitutes an unfair, deceptive, or abusive act or practice under 12 U.S.C. § 5531.</p>
<p class="rule-notes">BNPL approval rates increased from 56% to 79% between 2019 and 2022 through "counteroffers," the industry term for loosened underwriting standards (CFPB 2025). 59% of users report using BNPL for purchases they could not otherwise afford (Motley Fool 2025). The 43% DTI cap follows the CFPB's Qualified Mortgage ability-to-repay standard, providing a known and defensible threshold. Affirm demonstrates that ability-to-repay assessment is commercially viable at scale and functions as a competitive differentiator. Tier 1 is excluded because the combination of zero APR, four-payment maximum, and credit reporting adequately bounds risk without adding friction to short-term zero-cost products. Cross-reference: CNSR-BNPL-0007 (registry query, which must also be completed as part of this assessment).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0004">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0004</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">BNPL lenders may not assess any fee for missed, late, or returned payments; $500 statutory penalty per violation</p>
<p class="rule-plain">BNPL lenders cannot charge fees for missed or late payments -- period. If you miss a payment, the consequences are the same as any other debt: credit damage, account closure, and collection. There is no fee.</p>
<p class="rule-stmt">No BNPL lender may assess any fee of any kind in connection with a missed, late, or returned payment, regardless of how that fee is labeled or structured. This prohibition applies to all Tier 1 and Tier 2 products and may not be waived by contract or by borrower agreement. Default consequences are limited to: adverse credit bureau reporting under Section 0002, suspension or closure of the borrower's BNPL account, and civil collection action permitted under applicable state law. Charging a prohibited fee constitutes an unfair, deceptive, or abusive act or practice under 12 U.S.C. § 5531. Charging a prohibited fee also gives rise to a private right of action for actual damages, a statutory penalty of $500 per violation, and reasonable attorney fees and costs; this right of action arises independently of TILA's finance charge definition, which does not encompass late payment charges under Regulation Z 12 C.F.R. § 1026.4(c)(2).</p>
<p class="rule-notes">Late fees represented 13% of BNPL industry revenue in 2021 and grew 42% in a single year for Klarna (Affirm 2025; Richmond Fed 2025). A revenue stream that grows fastest when borrowers fail creates direct financial incentives to approve borrowers expected to miss payments. Eliminating late fees aligns lender profit with borrower success: the lender earns merchant fees and interest only when the borrower repays. Affirm operates profitably with a zero late-fee model at scale, demonstrating commercial viability. The concern that late fees deter default is not supported by evidence -- behavioral research shows late fees extract from people already struggling rather than preventing default (MDPI 2026). Credit damage, account closure, and collection action provide real consequences without creating an extraction mechanism. The $500 flat statutory penalty was set at the midpoint of the $100--$1,000 range used in TILA § 130, FCRA § 616, and EFTA § 915, trading judicial discretion for predictability and ease of consumer enforcement. Cross-reference: CNSR-FEES-0001 (junk fee prohibition baseline).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0005">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0005</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Tier 1 BNPL products must carry 0% APR; Tier 2 products may not exceed 10% APR inclusive of all fees; rate cap is uniform</p>
<p class="rule-plain">Short-term BNPL (Tier 1) must always be zero percent interest. Longer-term BNPL (Tier 2) cannot charge more than 10% annual interest. The rate cannot change based on your credit score.</p>
<p class="rule-stmt">Tier 1 BNPL products must carry a 0% annual percentage rate, inclusive of all fees. No charge of any kind may be assessed on a Tier 1 product except the principal amount of the purchase, and any such charge must be included in the APR calculation. Tier 2 BNPL products may not carry an annual percentage rate exceeding 10%, inclusive of all fees and charges. The APR cap applies uniformly and may not vary by borrower credit score, creditworthiness assessment, or any characteristic of the borrower. APR must be calculated and disclosed in TILA-compliant format before the consumer completes the purchase transaction. Lenders may not circumvent the rate cap through fee structures, add-on products, or product recharacterization.</p>
<p class="rule-notes">The research documents Affirm extended-term products reaching 29% APR in some cases (Richmond Fed 2026). The 10% cap was calibrated to cover lender cost of capital (6--8%) plus expected default loss (3--5%) plus servicing costs (approximately 2%), providing a commercially viable floor while remaining significantly below subprime installment loan rates (15--25%) and subprime credit card rates (24--29%). A 6% cap was considered and rejected as below lender cost of capital for subprime borrowers, likely causing market exit. A class-based (credit-tiered) rate was rejected for complexity and disparate impact risk. The uniform cap prevents race-correlated differential pricing while remaining viable for the full credit spectrum. Cross-reference: CNSR-PDLS-0001 (usury cap baseline for other lending products).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0006">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0006</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">BNPL payment due dates must be aligned to the borrower's documented income pay cycle; borrower chooses frequency at origination</p>
<p class="rule-plain">Your BNPL payments must be scheduled to match when you actually get paid. If you're paid monthly, your payments cannot be set to weekly. You choose the schedule at the start.</p>
<p class="rule-stmt">Before originating any BNPL loan, the lender must document the borrower's income payment cycle (weekly, bi-weekly, semi-monthly, or monthly) and set payment due dates aligned to that cycle. The lender may not impose a payment frequency that does not correspond to the borrower's documented pay cycle. Borrowers must be offered the option to choose weekly, bi-weekly, semi-monthly, or monthly payment schedules at origination; this choice must be confirmed in writing and must appear in the loan agreement. Payment frequency may not be modified by the lender after origination without the borrower's written consent. Pay cycle documentation is retained as part of the origination record and subject to CFPB examination.</p>
<p class="rule-notes">Approximately 80% of U.S. workers are paid bi-weekly or monthly (Bureau of Labor Statistics payroll data). Standard BNPL products assume weekly payments. Frequency misalignment is a structural product design flaw -- not a borrower behavior problem -- that creates predictable default risk when payment due dates fall before the borrower's next paycheck. This is a low-regulatory-burden fix with no adverse effect on lender economics: the total amount owed is unchanged; only the schedule shifts. It benefits both borrower (reduced structural default risk) and lender (reduced actual default rate). Cross-reference: CNSR-BNPL-0003 (affordability assessment, which must document income cycle as part of verification).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0007">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0007</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">CFPB must operate a real-time BNPL registry; lenders must query before origination and report within one hour of closing</p>
<p class="rule-plain">A government registry tracks all active BNPL loans in real time. Before approving a new loan, every BNPL lender must check the registry to see how much you already owe across all BNPL services. This prevents debt from stacking up across multiple providers.</p>
<p class="rule-stmt">The CFPB must operate a centralized, real-time BNPL loan registry. Before originating any BNPL loan (Tier 1 or Tier 2), the lender must query the registry and receive a confirmation code. Every origination must be reported to the registry within one hour of closing. In the event of a documented registry system outage, lenders may proceed on a 24-hour delayed reporting basis, with the outage documented in lender records and reported to the CFPB. The registry is non-public and accessible only to BNPL lenders for origination query purposes. A federal default aggregate limit of $2,500 applies to borrowers with a FICO score below 620, with no FICO score on file, or with an equivalent score from an alternative scoring model that falls below the equivalent of a 620 FICO; originating a loan that would exceed this limit without affirmative documented underwriting justification constitutes an unfair, deceptive, or abusive act or practice. Lenders may impose lower or higher aggregate limits above the federal floor through their own underwriting policies, subject to CFPB guidelines. Within 90 days of the end of the first full calendar quarter of registry operation, the CFPB must publish a baseline report documenting the number of Tier 2 BNPL originations to borrowers with FICO scores below 620 or no FICO score on file in that quarter; this baseline is the reference point for all subsequent market monitoring. If the number of such originations drops more than 25% in any rolling 18-month period measured quarterly against that baseline, the CFPB must report to Congress within 60 days describing market conditions and recommending corrective action.</p>
<p class="rule-notes">CFPB (2025) found 63% of BNPL borrowers carry simultaneous loans and 32% hold loans from multiple firms in the same period. Credit bureau reporting alone (Section 0002) cannot prevent stacking because loan origination decisions happen within minutes and bureau tradelines may not appear for up to 30 days. Only a real-time registry prevents cascading same-day debt. The one-hour reporting window closes the parallel origination vulnerability: two lenders querying a registry before either reports leaves the same gap that credit bureaus have. A one-hour window does not materially change lender operations (automated reporting is standard in payment infrastructure) but substantially closes the gap. The CFPB already operates consumer complaint and enforcement databases; real-time registry is incremental infrastructure, not a novel capability. The 90-day baseline publication window is operationally feasible because the CFPB operates the registry directly and holds the data in real time with no third-party collection lag; the CFPB already publishes monthly credit card market reports within approximately 30 days of month-end, making 90 days a comfortable ceiling even for the first-quarter publication. Cross-reference: CNSR-CFPS-0001 (CFPB independence, required for registry to function without political interference), CNSR-BNPL-0002 (credit bureau reporting), CNSR-BNPL-0003 (registry query is required as part of Tier 2 affordability assessment).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0008">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0008</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">BNPL checkout must prohibit countdown timers, false scarcity, and BNPL pre-selection; require total cost, payment schedule, and aggregate debt disclosure</p>
<p class="rule-plain">BNPL checkout cannot use countdown timers, fake "limited time" pressure, or pre-selected BNPL as the default payment option. Before you confirm a purchase, you must see the total cost, your full payment schedule, and how much BNPL debt you already have.</p>
<p class="rule-stmt">BNPL lenders and merchants integrating BNPL at point of sale are jointly responsible for compliance with the following design requirements. Prohibited design elements: countdown timers of any kind associated with BNPL offers; false scarcity signals implying BNPL availability is limited or time-sensitive; and pre-selection of BNPL as the default payment method. Required disclosures before the consumer completes a purchase: (1) the total cost of the purchase expressed as a single dollar amount, not framed as installment amounts; (2) the complete payment schedule including all due dates and amounts; and (3) the borrower's current aggregate BNPL debt balance across all providers as reported by the real-time registry under Section 0007. BNPL must be displayed with visual prominence equal to or less than credit card and debit card payment options; BNPL may not receive preferential placement, larger button size, brighter color treatment, or other visual design advantage. Violations of this section by either the BNPL lender or the merchant constitute unfair, deceptive, or abusive acts or practices.</p>
<p class="rule-notes">Peer-reviewed behavioral finance research (MDPI 2026, systematic review 2018--2025) documents that BNPL design systematically reduces "payment salience" -- the psychological experience of spending -- through installment framing, urgency cues, and frictionless approval. 49% of users report at least one problem including overspending, missed payment, or regret (Bankrate 2025). 18--24 year-olds carry BNPL as 28% of their unsecured debt vs. 17% average (CFPB 2025). Disclosure alone does not counter design effects (Brookings 2025); the prohibited design elements must be removed, not merely disclosed around. The equal-prominence requirement is objectively auditable through design review. The joint-liability rule prevents lenders from attributing violations to merchant design and vice versa. Cross-reference: CNSR-DRKS-0001 (dark pattern prohibition baseline), CNSR-BNPL-0007 (registry provides the aggregate debt figure required for the third mandatory disclosure).</p>
</div>
<div class="policy-card proposal" id="CNSR-BNPL-0009">
<div class="rule-header">
<code class="rule-id">CNSR-BNPL-0009</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">BNPL lenders may not charge small merchants a merchant fee rate exceeding 60% of the rate charged to large merchants for the same product</p>
<p class="rule-plain">BNPL lenders must charge small businesses (under $5 million in annual revenue) no more than 60% of the rate they charge large businesses. This lets small businesses afford BNPL without subsidizing it from tax revenue.</p>
<p class="rule-stmt">BNPL lenders may not charge small merchants a merchant fee rate greater than 60% of the merchant fee rate charged to large merchants for the same BNPL product tier and term structure. The reference rate for this comparison is the large-merchant rate published on the lender's quarterly fee schedule under this section; if the lender publishes a rate range rather than a single rate, the reference rate is the midpoint of that range. A "small merchant" is defined as any merchant whose parent company or controlling entity has total annual revenue below $5 million, as established by the most recently filed federal business tax return. Aggregate parent-company or controlling-entity revenue is used to determine size classification; entities may not achieve small-merchant status through subsidiary or affiliate structuring that reduces individual-entity revenue below the threshold. BNPL lenders must publish their merchant fee schedules, including the small-merchant rate and large-merchant rate, on a publicly accessible webpage updated no less than quarterly. BNPL lenders may not refuse to provide BNPL services to small merchants solely on the basis of transaction volume. The merchant fee tiering requirement is a condition of BNPL lender registration and supervision under CFPB authority (12 U.S.C. § 5512); it applies as a regulatory obligation on covered persons providing consumer financial products or services, with the consumer-facing purpose of ensuring small business merchant access to payment infrastructure that serves those businesses' consumer customers. Enforcement authority is held jointly by the CFPB under 12 U.S.C. § 5512 and by the FTC under Section 5 of the FTC Act (15 U.S.C. § 45) as an unfair method of competition affecting commerce. Civil penalties of up to $10,000 per merchant per calendar year apply for violations of the fee-tiering requirement.</p>
<p class="rule-notes">Current BNPL merchant fees of 3--6% plus per-transaction fees create prohibitive costs for small retailers that large merchants can absorb (Richmond Fed 2025). Small businesses cannot benefit from BNPL's documented AOV lift (20--40%) and conversion improvement (20--30%) when fee structures price them out. Government subsidy for merchant fees was considered and rejected because it transfers regulatory compliance costs to taxpayers; tiered fees shift the cost to large merchants, which is consistent with the platform's value that small business participation takes priority over investor profit maximization. The anti-fragmentation rule (aggregate parent-company revenue) prevents BNPL lenders from being gamed by structured subsidiaries. The 60% threshold (meaning small merchants pay no more than 60% of the large-merchant rate) was chosen as sufficient to make small business participation economically viable without forcing lenders below their cost of service for small accounts.</p>
</div>
</div>
</div>
```

- [ ] **Step 5.2: Verify the BNPL block is in the correct position in the file**

```bash
grep -n "fam-con-bnpl\|fam-con-cfp\|fam-con-pdl" docs/pillars/consumer-rights.html
```

Expected output (order matters):
```
...    fam-con-pdl
...    fam-con-bnpl
...    fam-con-cfp
```

- [ ] **Step 5.3: Verify all 9 BNPL card IDs are present**

```bash
grep -c "CNSR-BNPL-000" docs/pillars/consumer-rights.html
```

Expected: 18 (each card ID appears twice: once in the `id` attribute and once in the `<code>` element)

---

### Task 6: Add cross-references to five existing cards

**Files:**
- Modify: `docs/pillars/consumer-rights.html`

All five edits are to the end of existing `<p class="rule-notes">` elements. Make each edit individually.

- [ ] **Step 6.1: Add cross-reference to CNSR-PDLS-0001 rule-notes**

In the CNSR-PDLS-0001 card (search for `id="CNSR-PDLS-0001"`), find the rule-notes paragraph ending with:
```
Cross-reference: CON-GEN-005 (exploitative terms), HOU-FIN-001 (mortgage predatory lending).</p>
```
Change to:
```
Cross-reference: CON-GEN-005 (exploitative terms), HOU-FIN-001 (mortgage predatory lending), CNSR-BNPL-0001 (BNPL products subject to this usury cap framework).</p>
```

- [ ] **Step 6.2: Add cross-reference to CNSR-PDLS-0002 rule-notes**

In the CNSR-PDLS-0002 card, find the rule-notes paragraph ending with:
```
Cross-reference: CON-PDL-001 (rate caps), CON-GEN-001 (exploitative practices).</p>
```
Change to:
```
Cross-reference: CON-PDL-001 (rate caps), CON-GEN-001 (exploitative practices), CNSR-BNPL-0001 (BNPL rollover and debt stacking addressed separately).</p>
```

- [ ] **Step 6.3: Add cross-reference to CNSR-PDLS-0003 rule-notes**

In the CNSR-PDLS-0003 card, find the rule-notes paragraph ending with:
```
Cross-reference: CON-PDL-001, CON-PDL-002, CON-ENF (enforcement).</p>
```
Change to:
```
Cross-reference: CON-PDL-001, CON-PDL-002, CON-ENF (enforcement), CNSR-BNPL-0001 (BNPL products subject to targeted-community protections).</p>
```

- [ ] **Step 6.4: Add cross-reference to CNSR-PDLS-0004 rule-notes**

In the CNSR-PDLS-0004 card, find the rule-notes paragraph ending with:
```
Cross-reference: CNSR-PDLS-0001 (rate cap baseline), CNSR-PDLS-0002 (rollover prohibition).</p>
```
Change to:
```
Cross-reference: CNSR-PDLS-0001 (rate cap baseline), CNSR-PDLS-0002 (rollover prohibition), CNSR-BNPL-0001 (BNPL products subject to this 36% cap framework; BNPL-specific 10% cap is stricter).</p>
```

- [ ] **Step 6.5: Add cross-reference to CNSR-CRDS-0001 rule-notes**

In the CNSR-CRDS-0001 card (search for `id="CNSR-CRDS-0001"`), find the rule-notes paragraph. It currently ends with:
```
...The rule imposes reinvestigation requirements for disputed items but does not require proactive accuracy monitoring for non-disputed errors that a bureau should reasonably detect.</p>
```
Append before the closing `</p>`:
```
 Cross-reference: CNSR-BNPL-0002 (BNPL mandatory credit bureau reporting integrates with this accuracy requirement).
```

---

### Task 7: Run the full test suite

- [ ] **Step 7.1: Run unit tests**

```bash
npm run test:unit
```

Expected: All tests pass. No count assertions in data.test.js are affected (no new pillar, no data.js change).

- [ ] **Step 7.2: Run E2E tests for the BNPL family specifically**

```bash
npm run test:e2e -- --grep "BNPL family"
```

Expected: All 3 tests pass.
- "BNPL family section is present" passes (fam-con-bnpl exists)
- "all 9 BNPL policy card IDs render" passes (all 9 ids present)
- "retired CNSR-PDLS-0007 card is absent" passes (PDLS-0007 removed)

- [ ] **Step 7.3: Run the full E2E suite**

```bash
npm run test:e2e
```

Expected: All tests pass. The Consumer Rights pillar page tests ("has correct title", "has Purpose section", etc.) should still pass since only card content changed, not page structure.

---

### Task 8: Commit HTML changes

- [ ] **Step 8.1: Stage and commit all HTML changes**

```bash
git add docs/pillars/consumer-rights.html tests/e2e/site.spec.js
git commit -m "feat(consumer-rights): add BNPL policy family; retire CNSR-PDLS-0007

- Remove CNSR-PDLS-0007 (thin TILA/ECOA card; superseded)
- Add BNPL family (fam-con-bnpl) with 9 proposal cards:
  CNSR-BNPL-0001 two-tier classification framework
  CNSR-BNPL-0002 mandatory credit bureau reporting
  CNSR-BNPL-0003 Tier 2 affordability assessment (43% DTI)
  CNSR-BNPL-0004 late fee prohibition (\$500 PRA per violation)
  CNSR-BNPL-0005 APR caps (0% Tier 1, 10% Tier 2, uniform)
  CNSR-BNPL-0006 payment frequency alignment to pay cycle
  CNSR-BNPL-0007 real-time CFPB loan stacking registry
  CNSR-BNPL-0008 dark pattern prohibition and POS disclosure
  CNSR-BNPL-0009 tiered merchant fees for small business access
- Update PDL family-count from 0/7 to 0/6
- Update stats-bar: 134->142 total, 56->64 proposed
- Add BNPL cross-references to PDLS-0001, 0002, 0003, 0004, CRDS-0001
- Add E2E tests: family present, all 9 cards render, PDLS-0007 absent

Spec: docs/superpowers/specs/2026-05-03-bnpl-policy-family-design.md

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

### Task 9: Update repo documentation

**Files:**
- Modify: `.github/current-state.md`

- [ ] **Step 9.1: Verify research file exists and update current-state.md**

First confirm the BNPL research file is present:

```bash
ls policy/research/bnpl/bnpl_policy_overview.md
```

Expected: file listed with no error.

Then make two targeted edits:

**Edit 1 — update policy card count** (Known open items section):

Old:
```
- **Policy card audit** — **complete** as of May 2026; zero `status-missing` cards remain across all 25 pillars; 2,773 cards at `status-included`
```

New:
```
- **Policy card audit** — **complete** as of May 2026; zero `status-missing` cards remain across all 25 pillars; 2,781 cards at `status-included` (+8 net: Consumer Rights BNPL family added, CNSR-PDLS-0007 retired)
```

**Edit 2 — add BNPL research doc** (Research documents section):

Old:
```
- `pillars/` — per-pillar background research used to draft policy cards
```

New:
```
- `pillars/` — per-pillar background research used to draft policy cards
- `bnpl/bnpl_policy_overview.md` — BNPL market analysis, regulatory framework gaps, enforcement history; source document for CNSR-BNPL-0001 through 0009
```

- [ ] **Step 9.2: Commit documentation update**

```bash
git add .github/current-state.md
git commit -m "docs(current-state): record BNPL family addition and PDLS-0007 retirement

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```
