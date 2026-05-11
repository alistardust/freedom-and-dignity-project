# Buy-Now-Pay-Later (BNPL) Policy Overview
## Research Summary and Policy Framework Development

**Date:** May 2026  
**Status:** Ready for adversarial review via PolicyOS iteration process

---

## EXECUTIVE SUMMARY

The platform currently has a BNPL position (CNSR-PDLS-0007) that classifies BNPL as consumer credit subject to TILA/ECOA with mandatory APR disclosure. This research and policy development work:

1. **Validates the core position:** BNPL should be treated as credit, not as an exempted financial service
2. **Identifies critical gaps** in the existing proposal that prevent effective regulation
3. **Proposes an expanded framework** addressing the specific harms BNPL creates that traditional credit regulation doesn't capture
4. **Tests assumptions** about trade-offs between consumer protection and economic inclusion

**Core finding:** BNPL is not inherently predatory. The product enables genuine economic participation for lower-income and younger consumers. However, current BNPL practice is deliberately misaligned with consumer welfare (through business model design, merchant incentives, loose underwriting, fee extraction, and psychological design). Proper regulation protects consumers while preserving the product's genuine benefits.

---

## PART I: RESEARCH FINDINGS

### Consumer Harm Data

**Default and Delinquency Rates**

| Metric | Finding | Source |
|--------|---------|--------|
| Overall default rate | 2-3% | CFPB 2025; Motley Fool 2025; Richmond Fed 2026 |
| Deep-subprime (FICO <580) default rate | 3.5% | CFPB 2025 (Motley Fool 2025) |
| Prime borrower default rate | <1% | CFPB 2025; Motley Fool 2025 |
| Late payment rate (≥1 missed payment) | 34-41% of users | Chargeflow 2026; Motley Fool 2025 |

**Interpretation:** Default rates are measurably lower than credit cards (8.8% delinquency, ~10% default rate among BNPL users' credit cards). However, the 34-41% late payment rate paired with 2-3% default rate suggests **debt prioritization**—consumers are paying BNPL before other obligations. This is a harm that default-rate metrics miss.

**Consumer Regret and Unaffordability**

- 25% of BNPL users report regretting their purchase after realizing the debt (Motley Fool 2025)
- 59% used BNPL to finance purchases they couldn't otherwise afford (Motley Fool 2025)
- 49% of users report at least one problem: overspending (24%), missed payment (16%), regret (15%) (Bankrate 2025)

---

### Debt Stacking and Credit Reporting Gaps

**The Loan Stacking Problem**

- 63% of BNPL borrowers have simultaneous loans (CFPB 2025)
- 32% have loans across multiple BNPL firms in same period (CFPB 2025)
- Heavy BNPL users (>1 loan/month) carry $453 more in personal loans and $871 more in credit card debt than comparable non-users (CFPB 2025)

**Why This Matters:** Without credit bureau reporting, lenders cannot see the full debt picture. Underwriting decisions are made with incomplete information. This is not accidental—it's a structural feature that enables approval of borrowers who would fail affordability assessment if their full debt was visible.

**Underwriting Degradation:** BNPL approval rates increased from 56% (2019) to 79% (2022), driven by use of "counteroffers"—the lender's term for loosening underwriting standards (CFPB 2025). This is not improved risk selection; it's deliberate approval expansion.

---

### Business Model and Revenue Structure

**How BNPL Lenders Make Money**

Primary revenue streams (Richmond Fed 2025; Affirm 2025):
- Merchant fees: 3-6% of transaction + $0.20-0.30 per transaction
- Late fees: 13% of BNPL industry revenue (2021); Klarna's late fees grew 42% in 2024 (Affirm 2025)
- Interest on longer-term loans (for lenders offering 6-month+ terms)
- Interchange fees from BNPL-branded debit cards

**The Perverse Incentive Structure**

The current model creates direct financial incentives to:
1. **Approve marginal borrowers** (lender knows BNPL will be repaid before credit cards; approval expands accessible market)
2. **Encourage higher spending** (AOV lift 20-40% means more transaction volume and higher fees)
3. **Profit from default** (late fees represent material revenue stream; 42% growth in 2024 for Klarna)

**Merchant Incentive Alignment:** Merchants benefit from BNPL through AOV lift (15-40%) and conversion rate improvement (20-30% in some cases). This creates mutual interest between lender and merchant in pushing BNPL at checkout, regardless of whether it's in the consumer's interest.

---

### Psychological and Behavioral Effects

**Payment Salience Reduction**

Peer-reviewed research (2018-2025) documents that BNPL design features systematically reduce "payment salience"—the psychological experience of spending money:

- Deferred payments reduce immediate "pain of payment" (behavioral finance literature)
- Installment framing ("just $50/week") makes cost feel smaller than total amount
- Urgency cues (countdown timers, fake scarcity) increase impulsive purchasing
- Easy approval removes friction that normally constrains spending

**Impact on Vulnerable Populations:** 18-24 year-olds are disproportionately affected. BNPL represents 28% of their total unsecured debt vs. 17% average (CFPB 2025). This population also reports highest regret rates and most difficulty with payment discipline.

**Evidence base:** Motley Fool (2025), Brookings (2025), Bankrate (2025), and 10+ peer-reviewed studies in systematic literature review (MDPI 2026).

---

### Regulatory Landscape Context

**Federal Regulation Status (Current)**

The CFPB issued an interpretive rule in May 2024 that would have classified BNPL as credit card for TILA purposes. This rule was:
- Challenged by industry (Financial Technology Association lawsuit, Oct 2024)
- Withdrawn by CFPB (March 2025)
- Formally rescinded (June 2025)
- Not being enforced; CFPB redirecting resources elsewhere (May 2025)

**Why It Was Withdrawn:** CFPB stated the rule was "procedurally defective" and applied "ill-fitting open-end credit regulations to closed-end loans." The FTA argued open-end credit framework was inappropriate for short-term, fixed-schedule products. Both points have merit—TILA's revolving credit framework is a poor fit for installment loans.

**State-Level Activity:** 
- New York passed aggressive BNPL licensing law (2025)
- Nevada passed light-touch BNPL law (2025)
- Most states using existing payday lending frameworks
- No national standard; regulatory patchwork creates arbitrage opportunity

---

## PART II: EXISTING PLATFORM POSITION

### Current Rule: CNSR-PDLS-0007

**What It Covers:**
- Classification of BNPL as consumer credit
- Application of TILA requirements (APR disclosure)
- Application of ECOA requirements (equal credit opportunity)
- Private right of action and class action rights
- Halt to debt collection during active consumer disputes

**What It Does NOT Address:**
- Credit bureau reporting requirement
- Affordability assessment standards
- Late fees (not mentioned)
- Merchant incentive regulation
- Loan stacking prevention
- Psychological/dark pattern mitigation
- Small business merchant access
- Payment frequency alignment with income cycles

---

## PART III: CRITICAL GAPS ANALYSIS

### Gap 1: Credit Reporting Mandatory

**Finding:** 63% of BNPL borrowers have simultaneous loans. Without credit bureau reporting, loan stacking cannot be prevented and affordability assessment cannot work.

**Evidence:** CFPB 2025; Richmond Fed 2025; approval rate increase from 56% to 79% driven by loose underwriting, not better risk selection.

**Proposed Addition:** Mandatory credit bureau reporting within 30 days of origination. Borrower cannot opt out. This enables other lenders to see the full debt picture.

**Likely Challenge:** Administrative burden on lenders to establish credit bureau integrations. Counter: credit card lenders do this routinely; infrastructure already exists.

---

### Gap 2: Affordability Assessment Required (Extended-Term Loans)

**Finding:** BNPL approval rates jumped 56% → 79% through "counteroffers"—loosening underwriting, not improving it. 61% of users have subprime/deep-subprime credit; 59% used BNPL for purchases they couldn't otherwise afford.

**Proposed Addition:** For loans exceeding 4 payments or 4 weeks, documented income verification and debt-to-income ratio assessment required (43% DTI cap). Tier 1 (short-term, 0% interest) uses simplified assessment only.

**Likely Challenge:** Lenders will argue this adds friction and cost, reducing access. Counter: Affirm demonstrates ability-to-repay works at scale; it's a competitive differentiator for them.

---

### Gap 3: Late Fee Prohibition

**Finding:** Late fees represent 13% of BNPL industry revenue (2021); grew 42% in 2024 for Klarna. This is a profit center for default, creating perverse incentive to approve borrowers expected to miss payments.

**Decision Made:** Outright ban. No late fees at any point. Default addressed through credit reporting, account closure, collection action.

**Rationale:** 
- Simplest possible rule (protection & simplicity were prioritized)
- Already proven viable (Affirm runs profitably with zero late fees)
- Removes extraction mechanism entirely
- Aligns lender incentives: lender profits only when borrower repays successfully

**Likely Challenge:** "How will lenders deter default without fees?" Counter: Credit damage, account closure, and collection action provide real consequences. Late fees don't actually deter default; they extract from people already struggling.

---

### Gap 4: Interest Rate Cap and Structure

**Finding:** BNPL currently offers 0% interest on short-term. No statutory cap on longer-term products currently offered (Affirm's 36-month option runs up to 29% APR in some cases).

**Decision Made:** 
- Tier 1 (≤4 payments or ≤4 weeks): 0% mandatory
- Tier 2 (extended term): 10% APR cap maximum

**Rationale for 10%:**
- Covers lender cost of capital (~6-8%) + default loss (~3-5%) + servicing (~2%)
- Significantly below subprime installment loan rates (15-25%)
- Below credit card rates for subprime (24-29%)
- Allows lender viability (critical: if lenders fail, access disappears)

**Tradeoffs Considered & Rejected:**
- **6% cap:** Attractive for consumer protection, but below lender cost of capital. Requires either merchant fee subsidy or product becomes unprofitable.
- **No cap/market rate:** Would allow 25%+ APR on extended-term BNPL, turning it into debt trap territory.
- **Class-based caps** (different rates by credit score): More precise, but complex to administer and easy to game.

---

### Gap 5: Payment Frequency Alignment

**Finding:** ~80% of U.S. workers are paid bi-weekly or monthly. Current BNPL assumes weekly payments. Misalignment creates structural default risk.

**Decision Made:** Borrower chooses payment frequency (weekly, bi-weekly, or monthly) matching their documented pay cycle at origination. Lender cannot impose frequency that doesn't match income pattern.

**Rationale:** This is a product design flaw, not a consumer behavior problem. Fixing it reduces default risk for both lender and borrower without regulatory burden.

**Likely Challenge:** None. This is straightforward and benefits everyone.

---

### Gap 6: Real-Time Loan Stacking Prevention Registry

**Finding:** 63% of BNPL borrowers have simultaneous loans. Credit bureau reporting alone can't prevent stacking because loans originate within minutes. Need real-time visibility.

**Decision Made:** CFPB operates real-time BNPL loan registry. All lenders query before origination and report within 24 hours. Lenders can impose reasonable aggregate limits.

**Rationale:** Only mechanism that prevents cascading debt in real-time.

**Likely Challenge:** 
- CFPB capacity/funding (requires infrastructure investment)
- Lender resistance to information-sharing
- Defining "reasonable" aggregate limits

**Counter to challenges:**
- CFPB already operates consumer complaint database; real-time registry is incremental infrastructure
- Lenders already share data with credit bureaus; this is parallel system
- Aggregate limits defined by statute (e.g., $2,000-3,000 for subprime borrowers)

---

### Gap 7: Dark Pattern and Point-of-Sale Regulation

**Finding:** BNPL design features (urgency, prominence, framing as installments) systematically reduce payment salience and increase impulsive purchasing. Behavioral research shows disclosure alone doesn't counter these effects.

**Decision Made:** 
- Prohibit countdown timers, fake scarcity, pre-selection specific to BNPL
- Require point-of-sale disclosure of total cost (not framed as installments), complete payment schedule, APR, and aggregate BNPL debt
- Require equal visual prominence with credit card and debit card options

**Rationale:** Dark patterns are profitable precisely because they work. Regulation must address the design itself, not just require disclosure of something already designed to obscure.

**Likely Challenge:** 
- "How do we define dark patterns objectively?" 
- "Isn't this limiting merchant design freedom?"

**Counter:**
- Countdown timers, fake urgency, pre-selection are objectively identifiable design patterns
- Merchants can still promote BNPL; they just can't use manipulation
- Equal-prominence requirement is easy to audit (design review)

---

### Gap 8: Small Business Merchant Access

**Finding:** Merchant fees (3-6%) exclude small retailers from offering BNPL, which prevents small businesses from benefiting from AOV lift and conversion improvements.

**Decision Made:** Tiered merchant fees. Small business (<$5M revenue) charged lower rates than large merchants. Small business eligible for additional support.

**Rationale:** Enables small business participation in BNPL ecosystems; supports economic inclusion for merchants as well as consumers.

**Likely Challenge:** 
- BNPL lenders resist fee caps (reduces profit)
- Defining "small business" (revenue threshold)
- Enforcement/verification of business size

**Counter:**
- Large merchants can absorb higher fees; small ones cannot. Progressive fee structure is consistent with platform values (economic inclusion > investor profit)
- Revenue threshold is objective (tax return verification)
- Lenders already have merchant verification process

---

## PART IV: IDEAS DISCUSSED AND REJECTED

### Rejected: Hard Duration Cap (e.g., "max 12 weeks")

**Why It Was Considered:** Prevents BNPL from creeping into payday lending territory (52+ week terms). Clear bright-line rule.

**Why It Was Rejected:** 
- Not necessary if payment frequency alignment and affordability assessment work properly
- Creates arbitrary boundary (why 12 weeks vs. 16?)
- Prevents BNPL from serving legitimate longer-term needs (furniture, appliances, emergency vet)
- More flexible to allow duration if underlying protections are strong

**What Replaced It:** Payment frequency alignment + affordability assessment + interest rate cap. Together these prevent debt traps without arbitrary duration limits.

**Risk:** Without hard cap, extended-term BNPL could become debt trap territory if regulation weakens. Mitigated by: affordability requirement (borrower must be able to repay), interest rate cap (10% vs. payday's 300%), and credit reporting (other lenders can see it).

---

### Rejected: Late Fee Cap ($25 One-Time) Instead of Outright Ban

**Why It Was Considered:** Allows some consequence for default without extraction. Simple rule. Precedent in traditional lending.

**Why It Was Rejected:**
- $25 is trivial consequence (3% of typical debt; less than one day of payday lending)
- Creates admin complexity: "when does it apply?", "what about restoration?", "what if borrower doesn't restore?"
- Late fees are not necessary deterrent if credit damage + account closure + collection exist
- If lender doesn't profit from default, they're incentivized to prevent it, not collect fees on it

**What Replaced It:** Complete ban. Default addressed through credit reporting, account closure, collection action, and statutory interest (if applicable).

**Risk:** No direct fee consequence for default. Mitigated by: substantial credit damage (visible to future lenders), account closure (loss of BNPL access), and collection action (legal/wage garnishment consequences).

---

### Rejected: Rate Based on Borrower Creditworthiness (Class-Based Rates)

**Why It Was Considered:** More precise pricing (deep-subprime borrowers cost more to fund; should pay more). Analogous to credit card pricing.

**Why It Was Rejected:**
- Complexity: requires separate underwriting for each class; easy to game
- Disparate impact risk: class-based rates can correlate with race/ethnicity
- BNPL's advantage over credit cards is simplicity; class-based pricing removes that
- 10% cap is already subprime-inclusive (covers cost for riskiest borrowers)

**What Replaced It:** Single 10% cap for all Tier 2 loans, regardless of borrower credit quality.

**Risk:** Lender may not approve deep-subprime borrowers at 10% rate. Mitigated by: merchant fees should cover acquisition cost; lender still profits on merchant side; if lender refuses to serve subprime, that's a competitive opportunity for other lenders.

---

### Rejected: 6% Interest Rate Cap

**Why It Was Considered:** Strong consumer protection signal; below prime lending rates.

**Why It Was Rejected:** 
- Below lender cost of capital for subprime borrowers
- Forces merchant fee subsidy or lender exits market
- If lender exits, less access, not more
- 10% is still significantly below payday (300%+) and subprime installment (15-25%)

**What Replaced It:** 10% cap with justification based on cost of capital + default loss.

**Risk:** 10% seems high compared to prime rates (~6-8%). But comparing BNPL subprime to prime rates is wrong comparison; should compare to subprime installment (15-25%). From that perspective, 10% is protective.

---

### Rejected: Government Subsidy for Small Business Merchant Fees

**Why It Was Considered:** Would lower merchant costs; accelerate small business adoption.

**Why It Was Rejected:** 
- Uses general tax revenue (wealth/income tax) to subsidize BNPL platform fees
- Platform values suggest: private companies should bear cost of regulatory compliance, not taxpayers
- More efficient: tiered fee structure where large merchants subsidize small business (alignment with value hierarchy: small business participation > investor profit)

**What Replaced It:** Tiered merchant fees. Small business gets lower rate; large business pays higher rate. BNPL lender absorbs the margin difference.

**Risk:** BNPL lenders resist; may reduce overall BNPL availability. Mitigated by: competitive pressure (lenders who offer small business rates gain access to underserved market) and regulation (fee cap is mandate, not suggestion).

---

## PART V: FRAMEWORK SUMMARY

### Tier 1 Products: Short-Term, Zero-Interest
- ≤4 payments OR ≤4 weeks duration
- 0% APR (mandatory)
- Simplified assessment (soft credit check)
- Payment frequency borrower's choice
- No reporting exemption (must report to credit bureaus)
- No late fees

**Purpose:** Genuine short-term cash flow gaps. Frictionless access for lower-income consumers.

### Tier 2 Products: Extended-Term, Capped-Interest
- >4 payments AND >4 weeks duration
- 10% APR maximum
- Full affordability assessment (income verification, DTI cap 43%)
- Stacking check (query real-time registry)
- Payment frequency borrower's choice
- Credit bureau reporting mandatory
- No late fees

**Purpose:** Larger purchases (furniture, appliances, emergency needs) where affordability can be demonstrated. Still protective vs. subprime lending alternatives.

### System Requirements
- Real-time BNPL loan registry (operated by CFPB)
- Credit bureau integration (lenders report; other lenders can see)
- Dark pattern prohibition and point-of-sale disclosure standards
- Merchant fee tiering (small business at lower rates)
- Private right of action for consumers

---

## PART VI: RESEARCH CITATIONS

### Primary Data Sources

**Consumer Use and Harm:**
- CFPB (January 2025). Buy Now, Pay Later Study. https://files.consumerfinance.gov/f/documents/cfpb_BNPL_Report_2025_01.pdf
- Federal Reserve Board (May 2026). Economic Well-Being of U.S. Households survey.
- Motley Fool (November 2025). 2025 Buy Now, Pay Later Trends Study.
- Bankrate (May 2025). Buy Now, Pay Later Survey. https://www.bankrate.com/loans/personal-loans/buy-now-pay-later-survey/

**Market Analysis and Business Model:**
- Richmond Federal Reserve (February 2026). Buy Now, Pay Later Trends and Implications. https://www.richmondfed.org/publications/research/economic_brief/2026/eb_26-05
- Richmond Federal Reserve (October 2025). Buy Now, Pay Later: Market Impact and Policy Considerations. https://www.richmondfed.org/publications/research/economic_brief/2025/eb_25-03
- Affirm Holdings (March 2025). Q4 2024 Earnings and Investor Presentation.
- M2P Fintech (August 2021). Six Profitable BNPL Business Models. https://m2pfintech.com/blog/six-profitable-bnpl-business-models-to-unlock-infinite-value/
- Chargeflow (February 2026). Buy Now, Pay Later Statistics 2026. https://www.chargeflow.io/blog/buy-now-pay-later-statistics

**Psychological and Behavioral Research:**
- MDPI (January 2026). The Psychology of BNPL: A Systematic Review of Impulsive Buying and Post-Purchase Regret (2018-2025). https://www.mdpi.com/0718-1876/21/2/43
- Brookings Register (November 2025). BNPL Usage Rises Alongside Late Payments and Regret.
- Various peer-reviewed studies (2018-2025) on behavioral finance, payment salience, and installment framing effects.

**Regulatory Context:**
- CFPB (May 2024). BNPL Interpretive Rule. Federal Register.
- CFPB (March 2025). Statement on BNPL Rule Withdrawal.
- Payments Dive (November 2025). Regulatory Patchwork Vexes BNPL. https://www.paymentsdive.com/news/regulatory-patchwork-vexes-bnpl/806120/
- Morgan Stanley (April 2025). Buy Now, Pay Later Growth Raises Concerns. https://www.morganstanley.com/insights/articles/buy-now-pay-later-trends-2025

---

## PART VII: DEPENDENCIES AND IMPLEMENTATION

This framework depends on prior platform positions being active:

1. **CFPB Structural Independence** (CNSR-CFPS-0001, CNSR-CFPS-0004)
   - Restructure as five-member commission
   - Independent funding
   - Removal only for cause
   - **Why:** Without independence, CFPB can't enforce BNPL regulation against industry pressure (as happened 2024-2025)

2. **CFPB Jurisdiction Expansion** (CNSR-CFPS-0005)
   - Explicit authority over all BNPL lenders
   - Direct civil money penalty authority
   - Full supervisory authority regardless of charter
   - **Why:** Currently, CFPB authority over BNPL is ambiguous and has been under attack

3. **Credit Reporting Reform** (CNSR-CRDS series)
   - Accurate credit reporting and dispute rights
   - Real-time consumer access
   - Burden of proof on lender
   - **Why:** BNPL credit reporting integration requires credit bureau infrastructure improvements

4. **Private Right of Action** (CNSR-CFPS-0003, CNSR-PDLS-0007)
   - Consumers can sue for violations
   - Class actions permitted
   - Damages available
   - **Why:** Distributed enforcement makes regulation durable against agency underfunding or political pressure

---

## PART VIII: QUESTIONS FOR ADVERSARIAL REVIEW

### Logical Consistency Questions

1. **Payment Frequency Alignment:** Is requiring borrower-chosen payment frequency aligned to income cycle sufficient to prevent structural default risk? Or does it just shift default to different failure mode (unexpected job loss, income reduction)?

2. **10% Interest Cap Math:** At 10% APR for extended-term BNPL serving deep-subprime borrowers, does the lender actually break even? If not, what prevents market exit?

3. **Affordability Assessment Burden:** If Tier 2 requires full affordability assessment (income verification, DTI), how is this materially different from traditional installment lending? If it's similar, why not just push consumers to installment loans instead of extending BNPL?

4. **Stacking Registry Real-Time Requirement:** Is 24-hour reporting realistic? What about loans originated at 11 PM and reported the next day? Can consumer originate another loan at 11:30 PM before first is registered?

### Trade-Off and Values Questions

5. **Market Availability:** If regulation substantially increases lender costs (affordability assessment, credit reporting, registry participation), do some lenders exit the market? Result: less access for subprime borrowers who benefit from BNPL today.

6. **Small Business Fee Tiering:** If large merchants subsidize small business through higher fees, do large merchants pass costs to consumers through higher prices? Net result: regressive (everyone pays more; small business gets benefit).

7. **Zero Late Fees:** Without late fees, what deters intentional default? Only answer is: credit damage + collection action. Is that sufficient? Or is this policy vulnerable to high default rates making the whole model unviable?

### Implementation Questions

8. **CFPB Capacity:** Building and operating real-time BNPL registry is non-trivial infrastructure. Does CFPB have budget/staffing? If not, where does it come from?

9. **State Regulatory Conflict:** NY has aggressive BNPL law; other states have light-touch laws. How does federal framework coordinate with state-level regulation? What happens in conflicting jurisdictions?

10. **Enforcement Priority:** CFPB currently stretched thin. If this framework requires enforcement (monitoring dark patterns, auditing affordability assessments, investigating merchant fee violations), what existing enforcement work gets deprioritized?

### Gap and Vulnerability Questions

11. **Threshold Gaming:** Is a small business <$5M revenue threshold stable? Or will BNPL lenders structure as multiple $4.9M subsidiaries to access small business rates?

12. **Loan Size Loopholes:** Does Tier 1 (≤4 payments) create incentive for small loans ($50-100) with high approval rate (thin margin but high volume)? Is this healthy or just shifting extraction to volume?

13. **Regulatory Capture Risk:** BNPL industry will lobby against these rules. What mechanisms prevent watering down after initial adoption?

14. **Long-Term Durability:** If economic conditions tighten and BNPL becomes recession-period debt trap, is regulation sufficient? Or does framework need emergency circuit-breaker provisions?

---

## PART IX: CONCLUSION

This framework is designed to:

✓ **Protect vulnerable consumers** from debt accumulation and extraction (credit reporting prevents stacking; affordability assessment prevents debt traps; zero late fees remove extraction mechanism)

✓ **Enable economic participation** for lower-income and younger consumers (Tier 1 remains zero-interest and frictionless; Tier 2 at 10% APR significantly below alternatives)

✓ **Align lender incentives** with consumer welfare (merchant fees + interest on successful repayment; zero late fees remove profit from default)

✓ **Preserve small business access** to payment infrastructure (tiered merchant fees; small business cost structure enables adoption)

✓ **Remain enforceable and durable** against political pressure and regulatory capture (private right of action + CFPB independence required)

The core claim: **BNPL is not the problem. Unregulated BNPL is the problem.** Proper regulation converts BNPL from a debt-trap product into a genuine tool for economic inclusion.

---

**Ready for adversarial review and PolicyOS iteration.**
