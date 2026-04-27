# Citation Audit — Freedom and Dignity Project

_Audit conducted: July 2025. Scope: all 25 pillar HTML files (`docs/pillars/*.html`)._
_This is an audit pass only — no content has been modified. All findings require human review before correction._

---

## Audit methodology

Three categories of citation issues were checked:

1. **Orphan footnotes** — footnotes defined in the `<ol class="footnotes">` reference list with `id="fnN"` but never cited inline with `href="#fnN"`. These may represent references added to the list without adding the corresponding inline citation, or inline citations accidentally removed without updating the reference list.

2. **Broken cross-references** — inline `href="#fnN"` anchors that reference a footnote ID not present in the reference list. A broken cross-reference would cause the link to point nowhere. _No broken cross-references were found in this audit._

3. **Uncited statistics in narrative text** — paragraph text containing numerical claims (percentages, large counts, dollar amounts) or research attribution language ("studies show," "research indicates," "according to a report") without a `<sup><a href="#fnN">` citation anchor on the same line. Rule card content (`rule-stmt`, `rule-plain`) was excluded from this check because policy positions may cite specific legal sources within the text itself; the focus was on research/evidence sections that make empirical claims requiring external sourcing.

---

## Summary of orphan footnotes by pillar

| Pillar | Orphan footnote IDs | Notes |
|---|---|---|
| consumer-rights | fn2 | fn2 is defined in reference list but no inline `href="#fn2"` found |
| environment-and-agriculture | fn3, fn8, fn9 | Three orphan references in reference list |
| housing | fn1, fn9–fn18 | fn1 and fn9 through fn18 are defined but never cited inline; only fn2–fn8 are used |
| information-and-media | fn4–fn11 | Only fn1–fn3 are cited inline; fn4–fn11 are orphan references |
| labor-and-workers-rights | fn8 | fn8 defined in reference list but no inline citation |
| rights-and-civil-liberties | fn10, fn11, fn12 | Three orphan references in reference list |

All other pillar files have matching inline citations and reference list entries.

---

## Detailed findings by pillar

---

### Pillar: administrative-state

**Uncited statistics in narrative paragraphs:**

- Line ~927: "In many states, less than 20% of TANF block grant funds reach families as cash assistance. States have used TANF funds…" — needs citation (Center on Budget and Policy Priorities TANF tracking data)
- Line ~1044: "Many states provide UI benefits well below 50% wage replacement, with some providing as little as $235/week maximum regardless…" — needs citation (DOL UI data or EPI state UI comparison)
- Line ~1063: "The U.S. has more than 40,000 special purpose districts — more units of local government than any other type — collecting…" — needs citation (Census Bureau Census of Governments)
- Line ~1073: "HOAs can legally foreclose on a home for as little as $3.24 in unpaid dues in some states. An estimated 74 million Americans…" — needs citation for both the $3.24 claim and the 74 million figure

---

### Pillar: anti-corruption

**Uncited statistics in narrative paragraphs:**

- Line ~847: "Employers spend an estimated $340 million annually on union avoidance consultants." — needs citation (EPI or NLRB data)
- Line ~875: "Native advertising is a $400 billion global industry. Studies show the majority of readers cannot distinguish native advertising from editorial content." — needs citation for both claims; the $400B figure needs sourcing; "studies show" requires a specific citation

---

### Pillar: antitrust-and-corporate-power

**Uncited statistics in narrative paragraphs:**

- Line ~852: "Apple's App Store and Google's Play Store collectively control virtually all smartphone app distribution. Both platforms charge 15–30%…" — the commission percentage claim needs citation (App Store and Google Play developer policies; FTC market study)
- Line ~916: "Pay-for-delay agreements — in which brand-name pharmaceutical manufacturers pay generic competitors to delay market entry — are estimated to cost consumers…" — needs citation if a cost figure is cited (FTC pay-for-delay study)

---

### Pillar: checks-and-balances

**Uncited statistics in narrative paragraphs:**

- Line ~1307: "Oversight boards that depend on the bodies they oversee for funding become captured — this is a documented pattern across federal inspectors general, state ethics commissions, and federal banking regulators." — "documented pattern" needs at least one citation to a study or report

---

### Pillar: consumer-rights

**Orphan footnotes:**
- `fn2` — Defined: FTC (2014). *Data brokers: A call for transparency and accountability*. No inline `href="#fn2"` citation was found in the document.

**Uncited statistics in narrative paragraphs:**

- Line ~1342: "Payday loans routinely carry APRs of 300–400%. Installment loans targeting subprime borrowers average 100%+ APR." — needs citation (CFPB payday lending report or NCUA data)
- Line ~1656: "Research shows Black filers are steered to Chapter 13 at significantly higher rates than white filers with comparable financial profiles." — "research shows" requires a specific citation

---

### Pillar: courts-and-judicial-system

**Uncited statistics in narrative paragraphs:**

- Line ~608: "An estimated 40,000 people are currently incarcerated for federal marijuana offenses; hundreds of thousands more have conviction records…" — needs citation (BOP inmate statistics; ACLU marijuana report)

---

### Pillar: education

**Uncited statistics in narrative paragraphs:**

- Line ~2442: "Addresses the adjunct labor crisis — over 70% of college instructors are now contingent workers…" — needs citation (AAUP or NCES Integrated Postsecondary Education Data System)
- Line ~2491: "Research consistently shows that high-quality early childhood education produces significant long-term benefits in educational attainment, earnings, and reduced criminal justice involvement." — "research consistently shows" requires at least one specific citation
- Line ~2521: "An estimated 1 in 6 children in the United States experiences food insecurity." — needs citation (USDA ERS food insecurity statistics or Feeding America)
- Line ~2745: "An estimated $1 billion or more in public funds flows to private school voucher programs annually across states. Studies show…" — "studies show" requires a specific citation; the $1B estimate needs sourcing

---

### Pillar: elections-and-representation

**Uncited statistics in narrative paragraphs:**

- Line ~685: "An estimated 470,000 to 500,000 people are held in pre-trial detention in the United States on any given day — the majority unconvicted." — needs citation (BJS jail statistics or Vera Institute)
- Line ~238: "The efficiency gap, developed by Nicholas Stephanopoulos and Eric McGhee, measures the difference between each party's wasted votes…" — the efficiency gap concept references should cite the original paper: Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review*, 82(2), 831–900.

---

### Pillar: environment-and-agriculture

**Orphan footnotes:**
- `fn3` — Defined in reference list but no inline `href="#fn3"` found.
- `fn8` — Defined in reference list but no inline `href="#fn8"` found.
- `fn9` — Defined in reference list but no inline `href="#fn9"` found.

**Uncited statistics in narrative paragraphs:**

- Line ~1155: "An estimated 9–12 million lead service lines still deliver drinking water in the United States." — needs citation (EPA Lead and Copper Rule data or AWWA lead service line inventory)
- Line ~1218: "PFAS chemicals are estimated to be present in the blood of approximately 97–99% of Americans." — needs citation (CDC NHANES biomonitoring data or ATSDR report)

---

### Pillar: equal-justice-and-policing

**Uncited statistics in narrative paragraphs:**

- Line ~570: "Criminalization of simple drug possession has not reduced drug use or addiction rates but produces approximately 1.3 million arrests annually." — needs citation (FBI UCR/NIBRS annual arrest data)
- Line ~908: "The U.S. Sentencing Commission found that, controlling for legally relevant factors, Black male defendants received sentences…" — this references the USSC; a specific report year and citation should be linked

---

### Pillar: foreign-policy

**Uncited statistics in narrative paragraphs:**

- Line ~1184: "The U.S. is the world's largest arms exporter, accounting for approximately 40% of global arms sales." — needs citation (SIPRI Arms Transfers Database)

---

### Pillar: gun-policy

**Uncited statistics in narrative paragraphs:**

- Line ~636: "Approximately 4.6 million children in the U.S. live in homes with loaded, unlocked guns." — needs citation (Everytown research or AAP study)
- Line ~636: "An estimated 380,000 firearms are stolen in the United States each year." — needs citation (FBI UCR property crime data or BJS survey)

---

### Pillar: healthcare

**Uncited statistics in narrative paragraphs:**

- Line ~1375: "The U.S. has approximately 11 psychiatric beds per 100,000 population, down from 340 per 100,000 in 1955." — needs citation (Treatment Advocacy Center report or SAMHSA data); this is in a research section without a `<sup>` citation; the section already has fn1–fn17 so this appears to be a gap in an already-cited research section

---

### Pillar: housing

**Orphan footnotes:**
- `fn1` — Defined: National Low Income Housing Coalition. (2024). *Out of reach 2024*. No inline `href="#fn1"` citation found; the back-reference from fn1 also points to `#ref1` which does not appear to exist.
- `fn9` — Defined: Scanlon & Whitehead (2023). *Social housing in Europe*. Marked `<!-- [VERIFY] -->`. Back-reference points to `#ref-publ0011-1` which has no matching inline anchor.
- `fn10` — Defined: City of Vienna (2023). *Wiener Wohnen annual report*. Marked `<!-- [VERIFY] -->`. Back-reference points to `#ref-publ0011-2`.
- `fn11` — Defined: Federal Reserve Bank of Atlanta (2023). *Single-family investor activity*. Marked `<!-- [VERIFY] -->`. Back-reference points to `#ref-inst0001-1`.
- `fn12` — Defined: National Association of Realtors (2023). Marked `<!-- [VERIFY] -->`. Back-reference points to `#ref-inst0001-2`.
- `fn13–fn18` — All defined in reference list but no inline citations found.

_Note: fn9–fn18 all carry `<!-- [VERIFY] -->` markers, indicating they were added to the reference list as placeholders without yet being inserted inline. These references and their source URLs require independent verification before inline citations can be added._

**Uncited statistics in narrative paragraphs:**

- Line ~1369: "Multiple randomized controlled trials and longitudinal studies — including the At Home/Chez Soi study and Pathways to Housing — show that Housing First…" — these specific study names are cited but no formal APA footnote anchors are present in this section
- Line ~1379: "As of the 2023 HUD AHAR, approximately 137,000 individuals met the definition of chronically homeless on a single night." — needs formal `<sup>` citation (HUD Annual Homeless Assessment Report)

---

### Pillar: immigration

**Uncited statistics in narrative paragraphs:**

- Line ~2446: "Approximately 600,000 people are currently enrolled in DACA." — needs citation (USCIS DACA population data)
- Line ~2495: "Approximately 70% of immigration detainees are held in private, for-profit facilities." — needs citation (ACLU immigration detention report or DHS OIG data)
- Line ~2543: "Asylum seekers who have legal representation are approximately 5 times more likely to be granted asylum than those without representation." — needs citation (TRAC Immigration or ILRC report)

---

### Pillar: information-and-media

**Orphan footnotes:**
- `fn4` — Defined: *FCC v. Prometheus Radio Project*, 592 U.S. 414 (2021). No inline citation found.
- `fn5` — Defined: FCC Sponsorship Identification Rules, 47 C.F.R. § 73.1212. No inline citation found.
- `fn6` — Defined: Abernathy, P. M. (2023). *The news desert crisis*. No inline citation found.
- `fn7` — Defined: Local Journalism Sustainability Act, H.R. 3940 (2021). No inline citation found.
- `fn8` — Defined: Corporation for Public Broadcasting Act, 47 U.S.C. § 396. No inline citation found.
- `fn9` — Defined: *Gonzalez v. Google LLC*, 598 U.S. 617 (2023). No inline citation found.
- `fn10` — Defined: Haugen testimony (2021). Marked `<!-- [VERIFY] -->`. No inline citation found.
- `fn11` — Defined: Klonick, K. (2018). *The new governors*. No inline citation found.

_Note: fn1–fn3 are cited inline. fn4–fn11 appear to have been added to the reference list in a batch without the corresponding inline anchors being placed in the text. This is a significant citation gap in this pillar._

**Uncited statistics in narrative paragraphs:**

- Line ~310: "Since 2005, roughly 2,900 local U.S. newspapers have closed — more than one-third of the total — leaving tens of millions…" — needs citation (UNC Hussman School News Desert report — this is Abernathy fn6, which is itself orphaned; the inline citation was apparently dropped when the reference list was expanded)
- Line ~676: "Native advertising revenue now exceeds traditional display advertising for many digital publishers. Studies show the majority of readers cannot distinguish native advertising from editorial content." — "studies show" requires a specific citation
- Line ~686: "The Senate Intelligence Committee found that Russian Internet Research Agency operations reached an estimated 126 million Facebook users." — needs citation (Senate Intelligence Committee Report, Vol. 2)

---

### Pillar: infrastructure-and-public-goods

**Uncited statistics in narrative paragraphs:**

- Line ~594: "Fare-free public transit eliminates the transaction cost and stigma of fare collection, increases ridership — particularly among low-income riders…" — "increases ridership" without a citation; research on fare-free transit outcomes (Tallinn, Luxembourg, specific U.S. cities) should be cited

---

### Pillar: labor-and-workers-rights

**Orphan footnotes:**
- `fn8` — Defined in reference list but no inline `href="#fn8"` citation found.

**Uncited statistics in narrative paragraphs:**

- Line ~2111: "Detention time costs commercial drivers an estimated $1.1 billion in lost earnings annually." — needs citation (ATRI trucking industry report or DOT data)

---

### Pillar: legislative-reform

**Uncited statistics in narrative paragraphs:**

- Line ~306: "The Senate's two-senators-per-state allocation produces representational disparities with no parallel in any advanced democracy." — the comparative claim should cite a source documenting other democracies' representational ratios
- Line ~857: "Members of Congress outperform the market by an average of 6–12% annually." — needs citation (Ziobrowski et al. study or more recent academic analysis)

---

### Pillar: rights-and-civil-liberties

**Orphan footnotes:**
- `fn10` — Defined: U.S. Department of Labor, WHD (2023). *Section 14(c) certificate holders and worker data*. Back-reference points to `#ref10`, which has no matching inline anchor.
- `fn11` — Defined: Social Security Administration (2024). *Hearing office average processing time workload data*. Back-reference points to `#ref11`.
- `fn12` — Defined: U.S. Census Bureau (2024). *Poverty status in the past 12 months by disability status*. Back-reference points to `#ref12`.

**Uncited statistics in narrative paragraphs:**

- Line ~683: "Approximately 120,000 workers with disabilities are employed at subminimum wages under Section 14(c) certificates." — fn10 covers this but is orphaned; the inline citation is missing
- Line ~744: "People with disabilities face poverty rates approximately double the national average — consistently 25–27% for working-age adults." — fn12 covers this but is orphaned; the inline citation is missing
- Line ~755: "An estimated 700,000+ people with disabilities are on Medicaid HCBS waiver waitlists nationwide, some waiting over a decade." — needs citation (KFF or CMS waiver waitlist data)

---

### Pillar: science-technology-space

**Uncited statistics in narrative paragraphs:**

- Line ~242: "Federal civilian research and development investment as a share of GDP has declined from a peak of approximately 1.9% in the 1960s…" — needs citation (AAAS R&D budget analysis or OSTP data)

---

### Pillar: taxation-and-wealth

**Uncited statistics in narrative paragraphs:**

- Line ~576: "The Federal Reserve's Distributional Financial Accounts document that the top 1% of U.S. households hold approximately 3[X]% of total wealth." — this references a specific Fed publication; a formal inline citation should be added (Federal Reserve DFA series, most recent quarter)
- Line ~585: "The preferential treatment of capital income over labor income — long-term capital gains taxed at 0–20% for federal purposes…" — the rate claim is accurate per current law but should be cited to IRS or CBO for documentation

---

### Pillar: technology-and-ai

**Uncited statistics in narrative paragraphs:**

- Line ~4733: "The FBI conducted an estimated 3.4 million backdoor searches of Section 702 data on U.S. persons in a single year without a warrant." — needs citation (PCLOB or Senate Judiciary Committee report; ODNI transparency report)
- Line ~4809: "The data broker industry generates an estimated $200 billion annually in the United States and operates with virtually no federal oversight." — needs citation (FTC data broker study or IBISWorld industry report)

---

### Pillar: term-limits-and-fitness

No orphan footnotes. No uncited statistics identified in narrative sections.

---

### Pillar: executive-power

No orphan footnotes. No uncited statistics identified in narrative sections beyond citations already present.

---

### Pillar: gun-policy

No orphan footnotes (previous issues resolved). Uncited statistics noted above.

---

### Pillar: foreign-policy

No orphan footnotes. Uncited statistic noted above.

---

## Priority order for remediation

Based on severity (orphan count + uncited statistics density), suggested remediation priority:

1. **information-and-media** — 8 orphan footnotes; fn4–fn11 all need inline placement; this is a structural citation gap, not just a missing source
2. **housing** — 11 orphan footnotes (fn1, fn9–fn18); fn9–fn18 marked `<!-- [VERIFY] -->` and need source verification before inline placement
3. **rights-and-civil-liberties** — fn10–fn12 orphaned; the inline statistics they were meant to support appear in the text without citations
4. **environment-and-agriculture** — fn3, fn8, fn9 orphaned; PFAS and lead service line statistics lack citations
5. **consumer-rights** — fn2 orphaned; payday loan statistics need sourcing
6. **labor-and-workers-rights** — fn8 orphaned
7. All pillars with uncited narrative statistics identified in sections above

---

_Audit conducted by automated scan + manual review. Line numbers are approximate (±2 lines) due to HTML formatting. Verify exact locations with `grep -n` before editing._
