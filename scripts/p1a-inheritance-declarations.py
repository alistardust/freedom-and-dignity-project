#!/usr/bin/env python3
"""
P1-A: Add PolicyOS inheritance declarations to all 25 pillar overview.md files.

Compliance target: PAOS-TEST-0003 (inheritance declaration requirement).
Source data: policyos_pillar_audit_2026-04-27.md

Run from repo root:
    python3 scripts/p1a-inheritance-declarations.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKER = "## PolicyOS Inheritance Declaration"

# Per-pillar data keyed by domain code.
# overlays: from audit "Applicable overlays" line (minus "KERN (universal) + ")
# rating: audit overall rating
# notes: 2-4 key compliance notes from the audit
# cross_pillar: cross-pillar or cross-foundation inheritance notes
PILLAR_DATA: dict[str, dict] = {
    "ADMN": {
        "path": "policy/foundations/accountable_power/administrative_state/overview.md",
        "overlays": "ENFA, FEDR, REGD, AIGV, PRIV",
        "rating": "Adequate",
        "notes": [
            "KERN-0027 (whistleblower): Covered — WBLS-0001/0002/0003 address federal employees "
            "and contractors. One of the few pillars with explicit WBLS subdomain.",
            "KERN-0002/0004/0005 (accountability, unchecked power, attributable authority): Strong "
            "coverage via CIVL, OVRG, CAPS, INDS, TRAN subdomains.",
            "AIGV overlay: Partial — AI in agency adjudication underspecified; AINL subdomain "
            "present but scope unclear.",
            "PRIV overlay: Partial — data collection practices across administrative agencies not "
            "addressed as a structural design constraint.",
            "Ecological duty gap: No position on what happens when agencies responsible for "
            "environmental protection structurally fail that duty (Value 8 absent).",
        ],
        "cross_pillar": [
            "Shares enforcement architecture patterns with EXEC (executive power) and CHKS "
            "(checks and balances); agency-specific enforcement circuits should be consistent.",
            "SCIS subdomain addresses scientific integrity; see also SCIS pillar (science, "
            "technology, and space) for research-specific positions.",
        ],
    },
    "ANTR": {
        "path": "policy/foundations/clean_democracy/antitrust_and_corporate_power/overview.md",
        "overlays": "ENFA, REGD, ECON, PRIV, AIGV",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — employees who report anticompetitive practices "
            "have no platform-level protection. P1-B gap.",
            "KERN-0015 (foreseeable abuse design): Some abuse path analysis present in CAPS and "
            "ENFC; revolving door addressed. Algorithmic market manipulation abuse paths absent.",
            "AIGV overlay: ALGO and ALGP subdomains address algorithmic collusion and market "
            "manipulation. Partial — AI in merger review and enforcement not addressed.",
            "ENFA overlay: ENFC and ENFL subdomains present but enforcement actors for new "
            "AI-driven market offenses underspecified.",
        ],
        "cross_pillar": [
            "Closely coupled to MDIA (information and media) — platform concentration positions "
            "appear in both; ANTR-MDIA cross-domain positions may apply.",
            "ECON overlay shared with TAXN, LABR, CNSR — market power positions should be "
            "consistent across these pillars.",
        ],
    },
    "CHKS": {
        "path": "policy/foundations/accountable_power/checks_and_balances/overview.md",
        "overlays": "FEDR, DEMO, AIGV",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protection for officials or staff who report "
            "violations of constitutional checks.",
            "ENFA overlay: Absent — enforcement architecture for checks and balances violations "
            "not defined. This is the pillar's deepest gap: who enforces structural accountability?",
            "AIGV overlay: AINL subdomain (7 positions) present and strong for AI governance "
            "structural requirements.",
            "KERN-0013 (challenge/appeal): ACCS-0001 present; but challenge rights for "
            "emergency power declarations and executive branch violations — underspecified.",
        ],
        "cross_pillar": [
            "Strongly coupled to EXEC (executive power) and LEGL (legislative reform) — "
            "enforcement architecture decisions here affect both.",
            "FEDR overlay links to ADMN for federalism design consistency.",
        ],
    },
    "CNSR": {
        "path": "policy/foundations/real_freedom/consumer_rights/overview.md",
        "overlays": "ENFA, REGD, ECON, PRIV, GEOG",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protection for consumer fraud reporters "
            "or employees who expose deceptive practices. P1-B gap.",
            "PRIV overlay: Thin — consumer data privacy beyond basic notice-and-consent not "
            "addressed as a structural design constraint.",
            "GEOG overlay: Geographic access disparities in consumer protection (rural, "
            "low-income communities) underaddressed.",
            "ENFA overlay: CFPB and FTC enforcement referenced; but failure consequences for "
            "regulatory capture of these bodies absent.",
        ],
        "cross_pillar": [
            "Overlaps with TECH (technology and AI) on data privacy and algorithmic consumer "
            "harm — TECH positions may govern digital consumer contexts.",
            "ECON overlay connects to ANTR (antitrust) — monopolistic pricing as consumer harm "
            "should be consistent across pillars.",
        ],
    },
    "CORT": {
        "path": "policy/foundations/accountable_power/courts_and_judicial_system/overview.md",
        "overlays": "ENFA, REGD, FEDR, DEMO, PRIV",
        "rating": "Critical gaps",
        "notes": [
            "Access to justice: Critical gap — no positions on civil legal aid, right to counsel "
            "in civil proceedings, or structural barriers to court access.",
            "KERN-0027 (whistleblower): Implicitly covered by CRPT pillar (qui tam, universal "
            "whistleblower); court-specific reporter protection absent.",
            "KERN-0014 (access not defeated by burden): Court filing fees, mandatory arbitration "
            "clauses, and standing doctrine barriers to access unaddressed.",
            "ENFA overlay: Judicial ethics enforcement relies on Congress self-enforcement — "
            "structural independence of judicial conduct oversight not addressed.",
        ],
        "cross_pillar": [
            "Access-to-justice gap is partly addressed by JUST (equal justice and policing) "
            "and RGHT (rights and civil liberties) — cross-pillar inheritance needed.",
            "FEDR overlay: federal vs. state court jurisdiction design should be consistent "
            "with CHKS and EXEC positions on federal power.",
        ],
    },
    "CRPT": {
        "path": "policy/foundations/clean_democracy/anti_corruption/overview.md",
        "overlays": "ENFA, REGD, DEMO, PRIV",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Strong — WBLS subdomain with 3 positions including "
            "qui tam expansion, universal private right of action, and federal anti-SLAPP statute.",
            "KERN-0015 (foreseeable abuse design): Revolving door (RVDS), disclosure (DSCS), "
            "financial conflicts (FCFL) addressed. Dark money and foreign influence pathways "
            "present.",
            "ENFA overlay: Independent enforcement architecture underspecified — positions "
            "define prohibitions but enforcement actors weak.",
            "DEMO overlay: Electoral corruption and campaign finance positions present; "
            "structural corruption of democratic institutions addressed.",
        ],
        "cross_pillar": [
            "CRPT whistleblower framework (WBLS-0001/0002/0003) is a platform-level standard "
            "that other pillars should inherit for their domain-specific WBLS positions.",
            "Overlaps with ELEC (elections) on campaign finance; positions should be "
            "consistent and non-duplicative.",
        ],
    },
    "EDUC": {
        "path": "policy/foundations/freedom_to_thrive/education/overview.md",
        "overlays": "ENFA, GEOG, FEDR, THRV, PRIV, DEMO, AIGV",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for teachers, staff, students, "
            "or parents who report civil rights violations or educational fraud. P1-B gap.",
            "THRV overlay: Broad coverage of education as a material right; funding equity "
            "and access positions strong.",
            "AIGV overlay: Present — AI in education addressed; but algorithmic grading, "
            "surveillance of students, and predictive tracking underspecified.",
            "KERN-0014 (access not defeated by burden): Geographic access and cost barriers "
            "addressed; disability access in education underspecified.",
        ],
        "cross_pillar": [
            "THRV overlay shared with HLTH, HOUS, LABR, INFR — education as a material "
            "necessity should be framed consistently with other THRV pillars.",
            "PRIV overlay: Student data privacy connects to TECH (technology and AI) positions "
            "on data collection; TECH positions may govern EdTech contexts.",
        ],
    },
    "ELEC": {
        "path": "policy/foundations/clean_democracy/elections_and_representation/overview.md",
        "overlays": "ENFA, GEOG, FEDR, DEMO, AIGV, PRIV",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for election workers or "
            "campaign staff who report voter suppression or election fraud. P1-B gap.",
            "AIGV overlay: Present but thin — AI in election administration and disinformation "
            "partially addressed; autonomous campaign targeting systems absent.",
            "ENFA overlay: Enforcement for voter suppression and election fraud "
            "underspecified — actor, trigger, and failure consequences incomplete.",
            "KERN-0014 (access not defeated by burden): Voter ID, registration barriers, "
            "polling place access partially addressed; mail voting and accessibility gaps.",
        ],
        "cross_pillar": [
            "Closely coupled to CRPT (anti-corruption) for campaign finance enforcement "
            "and MDIA (information and media) for election disinformation.",
            "DEMO overlay shared with CHKS, EXEC, LEGL — democratic accountability "
            "mechanisms should be architecturally consistent.",
        ],
    },
    "ENVR": {
        "path": "policy/foundations/freedom_to_thrive/environment_and_agriculture/overview.md",
        "overlays": "ENFA, ECOL, FEDR, REGD, ECON, GEOG",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for environmental law "
            "reporters or agency scientists who expose regulatory violations. P1-B gap.",
            "ECOL overlay: Strong — ecological habitability (Value 8) is the pillar's core; "
            "climate, pollution, species protection, and ecosystem health addressed.",
            "KERN-0015 (foreseeable abuse design): Agricultural subsidy capture, regulatory "
            "capture of EPA partially addressed; fossil fuel industry abuse pathways "
            "underspecified.",
            "ECON overlay: Agricultural economic justice (FARM, FOOD subdomains) present; "
            "but environmental cost externalization design constraints absent.",
        ],
        "cross_pillar": [
            "ECOL overlay shared with HLTH (pollution and health outcomes), HOUS (environmental "
            "justice in housing siting), INFR (clean infrastructure), IMMG (climate migration). "
            "Ecological positions must be consistent across all ECOL-bearing pillars.",
            "ADMN pillar's ecological duty gap (agencies failing environmental protection) "
            "connects directly to ENVR enforcement architecture.",
        ],
    },
    "EXEC": {
        "path": "policy/foundations/accountable_power/executive_power/overview.md",
        "overlays": "ENFA, FEDR, DEMO, PRIV, AIGV",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no explicit protections for executive branch "
            "employees or officials who report unconstitutional or illegal executive action.",
            "AIGV overlay: AI in executive decision-making, AI-enabled surveillance by "
            "executive agencies, and AI in military/national security contexts underaddressed.",
            "KERN-0004 (unchecked power): Emergency powers, executive privilege, and pardon "
            "power abuse partially addressed; self-dealing and personal enrichment constraints "
            "thin.",
            "ENFA overlay: Enforcement actors for executive overreach underspecified — "
            "Congress and courts referenced but institutional failure scenarios absent.",
        ],
        "cross_pillar": [
            "Strongly coupled to CHKS (checks and balances) and LEGL (legislative reform) — "
            "executive power constraints must form a coherent constitutional architecture.",
            "ADMN pillar addresses agency-level accountability; EXEC addresses the principal. "
            "These should be read together.",
        ],
    },
    "FPOL": {
        "path": "policy/foundations/equal_justice/foreign_policy/overview.md",
        "overlays": "ENFA, DEMO, PRIV, ECOL",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — national security and diplomatic "
            "whistleblowers have no coverage (e.g., violations of international law, "
            "illegal arms transfers).",
            "ECOL overlay: Present — climate foreign policy, international environmental "
            "agreements, and climate justice globally addressed.",
            "KERN-0016 (no coercion/deprivation): International obligations and "
            "extraterritorial human rights enforcement underspecified.",
            "ENFA overlay: Enforcement of foreign policy commitments and treaty obligations "
            "absent — actor, trigger, and failure consequence missing.",
        ],
        "cross_pillar": [
            "ECOL overlay connects to ENVR (environment and agriculture) — international "
            "climate commitments must be consistent with domestic ENVR positions.",
            "PRIV overlay: Surveillance and intelligence-sharing positions connect to TECH "
            "and RGHT (rights and civil liberties).",
        ],
    },
    "GUNS": {
        "path": "policy/foundations/real_freedom/gun_policy/overview.md",
        "overlays": "ENFA, GEOG, FEDR, REGD, PRIV",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for persons who report "
            "illegal gun trafficking, straw purchases, or unlicensed dealing. P1-B gap.",
            "ENFA overlay: Enforcement architecture incomplete — background check enforcement "
            "actors and failure consequences underspecified; ATF authority gaps not addressed.",
            "KERN-0015 (foreseeable abuse design): Straw purchase loopholes and "
            "ghost gun pathways partially addressed; illegal modification supply chains absent.",
            "GEOG overlay: State preemption of local gun laws addressed; but rural-urban "
            "enforcement capacity disparities absent.",
        ],
        "cross_pillar": [
            "RGHT (rights and civil liberties) governs Second Amendment rights framing; "
            "GUNS governs the regulatory architecture. These must be consistent.",
            "JUST (equal justice and policing) addresses gun violence in policing contexts; "
            "cross-pillar consistency required on use-of-force and community safety.",
        ],
    },
    "HLTH": {
        "path": "policy/foundations/freedom_to_thrive/healthcare/overview.md",
        "overlays": "ENFA, GEOG, FEDR, THRV, AIGV, ECOL, ECON, PRIV, REGD",
        "rating": "Adequate",
        "notes": [
            "KERN-0027 (whistleblower): Thin — SCIS subdomain has one position on scientific "
            "whistleblowers; broader healthcare fraud and patient safety reporting absent.",
            "THRV overlay: Strong — healthcare as material necessity (Value 6) is the "
            "pillar's core; universal coverage, affordability, and access addressed.",
            "AIGV overlay: Present — AI diagnostics, algorithmic care rationing, and "
            "predictive health risk scoring addressed.",
            "ECOL overlay: Present — environmental health, pollution impacts, and climate "
            "health outcomes addressed.",
        ],
        "cross_pillar": [
            "THRV overlay shared with EDUC, HOUS, LABR, INFR — healthcare as material "
            "necessity should be framed consistently with other THRV pillars.",
            "PRIV overlay connects to TECH (patient data, health surveillance) and RGHT "
            "(medical privacy as a civil liberty).",
        ],
    },
    "HOUS": {
        "path": "policy/foundations/freedom_to_thrive/housing/overview.md",
        "overlays": "ENFA, GEOG, FEDR, THRV, ECON, ECOL, PRIV, REGD, AIGV",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for reporters of housing "
            "discrimination, predatory lending, or building safety concealment. P1-B gap.",
            "AIGV overlay: Present but thin — algorithmic housing discrimination (automated "
            "denial, rental pricing algorithms) partially addressed.",
            "THRV overlay: Present — housing as material necessity strong; but funding "
            "mechanisms for affordable housing construction underspecified.",
            "KERN-0015 (foreseeable abuse design): Eviction abuse paths and landlord "
            "retaliation addressed; zoning capture and NIMBYism as an abuse path absent.",
        ],
        "cross_pillar": [
            "ECOL overlay connects to ENVR (environmental justice in housing siting, "
            "pollution proximity) and INFR (infrastructure access for housing).",
            "JUST (equal justice) shares housing discrimination enforcement; RGHT shares "
            "fair housing as a civil rights issue.",
        ],
    },
    "IMMG": {
        "path": "policy/foundations/equal_justice/immigration/overview.md",
        "overlays": "ENFA, GEOG, FEDR, THRV, PRIV, ECOL",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for immigration detainees "
            "or advocates who report detention abuse or due process violations. P1-B gap.",
            "KERN-0014 (access not defeated by burden): Legal representation access, language "
            "access, and geographic detention location as access barriers partially addressed.",
            "ECOL overlay: Climate migration and climate refugee protections present — "
            "climate displacement as a rights trigger.",
            "THRV overlay: Present — immigration as a human dignity and material security "
            "issue; but asylum seeker basic needs guarantees thin.",
        ],
        "cross_pillar": [
            "JUST (equal justice and policing) and IMMG share enforcement abuse contexts "
            "— immigration enforcement civil rights positions must be consistent.",
            "RGHT (rights and civil liberties) governs due process protections that apply "
            "to immigration proceedings; cross-pillar inheritance required.",
        ],
    },
    "INFR": {
        "path": "policy/foundations/freedom_to_thrive/infrastructure_and_public_goods/overview.md",
        "overlays": "ENFA, GEOG, FEDR, THRV, ECOL, ECON, AIGV",
        "rating": "Critical gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for infrastructure safety "
            "reporters (pipeline safety, dam inspection falsification, bridge safety). P1-B gap.",
            "AIGV overlay: Entirely absent — AI in infrastructure management (smart grid, "
            "traffic systems, predictive maintenance, autonomous transit) unaddressed. "
            "Critical emerging risk area.",
            "ENFA overlay: Partial — no independent infrastructure oversight body specified; "
            "enforcement depends on sector-specific regulators without platform-level "
            "enforcement architecture.",
            "KERN-0026 (systemic failure/corrective action): WATS-0003 (dam safety) is "
            "the only example; broader infrastructure failure corrective action absent.",
        ],
        "cross_pillar": [
            "THRV overlay shared with HLTH, EDUC, HOUS, LABR — infrastructure access as "
            "a material necessity must be consistent.",
            "ECOL overlay connects to ENVR — clean infrastructure transition positions "
            "must be architecturally consistent with environmental positions.",
        ],
    },
    "JUST": {
        "path": "policy/foundations/equal_justice/equal_justice_and_policing/overview.md",
        "overlays": "ENFA, GEOG, FEDR, PRIV, AIGV, ECON, DEMO",
        "rating": "Adequate",
        "notes": [
            "KERN-0027 (whistleblower): Covered — WHTS subdomain addresses whistleblower "
            "protections and incentives; STNG-0001 includes officer whistleblower protection "
            "for quota pressure reporting.",
            "AIGV overlay: Present — AI in policing, predictive policing, facial recognition, "
            "and algorithmic sentencing addressed.",
            "KERN-0013 (challenge/appeal): Strong — due process, appeal rights, and civilian "
            "oversight mechanisms present.",
            "ECON overlay: Economic justice in policing (fines, fees, civil asset forfeiture) "
            "addressed.",
        ],
        "cross_pillar": [
            "Rights and Civil Liberties (RGHT) is a co-primary pillar for individual rights "
            "in policing contexts — RGHT inherits JUST enforcement architecture.",
            "IMMG shares enforcement abuse contexts; HOUS shares housing discrimination "
            "enforcement — positions should be read together.",
        ],
    },
    "LABR": {
        "path": "policy/foundations/freedom_to_thrive/labor_and_workers_rights/overview.md",
        "overlays": "ENFA, ECON, THRV, PRIV, GEOG, AIGV",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for workers who report "
            "safety violations, wage theft, or anti-organizing retaliation. P1-B gap.",
            "AIGV overlay: Partial — AI in hiring, algorithmic scheduling, and worker "
            "surveillance addressed; automated workforce reduction and AI wage-setting absent.",
            "THRV overlay: Strong — fair wages, safe conditions, and economic security "
            "as material necessities addressed.",
            "ENFA overlay: NLRB and DOL enforcement referenced; failure consequences for "
            "regulatory capture of labor enforcement bodies underspecified.",
        ],
        "cross_pillar": [
            "THRV overlay shared with HLTH, EDUC, HOUS, INFR — labor rights as material "
            "security must be framed consistently.",
            "ECON overlay connects to TAXN (wealth and inequality) and ANTR (corporate power) "
            "— labor market concentration positions should be consistent.",
        ],
    },
    "LEGL": {
        "path": "policy/foundations/accountable_power/legislative_reform/overview.md",
        "overlays": "ENFA, DEMO, FEDR",
        "rating": "Critical gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for congressional staff or "
            "officials who report violations of legislative ethics or constitutional duties.",
            "ENFA overlay: Critical gap — ethics enforcement relies entirely on Congress "
            "self-enforcement; no independent enforcement actor specified anywhere in the pillar.",
            "KERN-0004 (unchecked power): Term limits and gerrymandering positions address "
            "structural power; but filibuster abuse and legislative gridlock as unchecked "
            "power pathways absent.",
            "FEDR overlay: Federalism design in legislative context (federal vs. state "
            "legislative preemption) underspecified.",
        ],
        "cross_pillar": [
            "CHKS (checks and balances) and EXEC (executive power) are closely coupled — "
            "legislative reform positions must form a coherent constitutional architecture.",
            "CRPT (anti-corruption) covers congressional corruption and revolving door; "
            "LEGL and CRPT positions should be non-duplicative.",
        ],
    },
    "MDIA": {
        "path": "policy/foundations/clean_democracy/information_and_media/overview.md",
        "overlays": "ENFA, REGD, DEMO, PRIV, AIGV, ECON",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for journalists, platform "
            "employees, or government communications staff who expose disinformation or "
            "media law violations. P1-B gap.",
            "AIGV overlay: Present — AI-generated disinformation, algorithmic amplification, "
            "and AI in editorial decisions addressed.",
            "ECON overlay: Media consolidation and platform market power addressed via "
            "ANTR cross-domain positions; but platform economic coercion of journalists absent.",
            "KERN-0015 (foreseeable abuse design): Foreign disinformation and state-sponsored "
            "interference partially addressed; domestic political capture of media "
            "infrastructure absent.",
        ],
        "cross_pillar": [
            "ANTR (antitrust) governs media consolidation — MDIA and ANTR positions on "
            "platform power must be consistent.",
            "ELEC (elections) shares election disinformation contexts; cross-pillar "
            "consistency required.",
        ],
    },
    "RGHT": {
        "path": "policy/foundations/equal_justice/rights_and_civil_liberties/overview.md",
        "overlays": "ENFA, PRIV, DEMO, ECON, GEOG",
        "rating": "High gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for civil rights defenders "
            "or attorneys who report constitutional rights deprivations. P1-B gap.",
            "PRIV overlay: Strong — surveillance, digital privacy, and Fourth Amendment "
            "protections addressed.",
            "ENFA overlay: Enforcement architecture for civil rights violations "
            "underspecified — DOJ Civil Rights Division and private right of action present "
            "but failure consequences thin.",
            "KERN-0014 (access not defeated by burden): Geographic and economic access "
            "barriers to civil rights enforcement partially addressed.",
        ],
        "cross_pillar": [
            "Shared pillar — primary home is equal_justice foundation; also appears under "
            "real_freedom foundation. Positions here are inherited by both foundations.",
            "JUST (equal justice and policing) inherits RGHT enforcement architecture for "
            "policing contexts. IMMG inherits RGHT due process positions.",
        ],
    },
    "SCIS": {
        "path": "policy/foundations/freedom_to_thrive/science_technology_space/overview.md",
        "overlays": "ENFA, THRV, FEDR, AIGV, ECOL",
        "rating": "Critical gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for researchers, agency "
            "scientists, or contractors who report scientific misconduct or data suppression. "
            "P1-B gap.",
            "ENFA overlay: 19 positions with no enforcement circuits — actor, trigger, and "
            "failure consequence absent across virtually all positions. Most critical "
            "structural gap in the platform.",
            "AIGV overlay: Present but thin — AI in scientific research and space "
            "infrastructure underaddressed.",
            "THRV overlay: Science as a public good and driver of material wellbeing "
            "partially addressed; research funding as a THRV duty underspecified.",
        ],
        "cross_pillar": [
            "ADMN pillar covers agency science integrity (SCIS subdomain) — ADMN-SCIS "
            "positions govern how agencies handle scientific findings. SCIS pillar "
            "governs the research enterprise itself.",
            "ECOL overlay connects to ENVR — climate science and environmental research "
            "positions must be consistent.",
        ],
    },
    "TAXN": {
        "path": "policy/foundations/freedom_to_thrive/taxation_and_wealth/overview.md",
        "overlays": "ENFA, REGD, ECON, PRIV, FEDR",
        "rating": "Needs work",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for tax fraud reporters "
            "or employees who expose illegal tax evasion. P1-B gap.",
            "ECON overlay: Strong — wealth concentration, tax avoidance, and wealth taxes "
            "addressed.",
            "KERN-0015 (foreseeable abuse design): Tax shelter abuse paths and offshore "
            "evasion partially addressed; valuation fraud and charitable foundation abuse "
            "as tax avoidance mechanisms absent.",
            "ENFA overlay: IRS enforcement capacity and independence partially addressed; "
            "failure consequences for IRS budget capture absent.",
        ],
        "cross_pillar": [
            "ECON overlay connects to LABR (wage taxation fairness), ANTR (corporate tax "
            "avoidance as market power), and HOUS (housing wealth taxation).",
            "PRIV overlay: Tax return privacy connects to RGHT and TECH data privacy "
            "positions.",
        ],
    },
    "TECH": {
        "path": "policy/foundations/real_freedom/technology_and_ai/overview.md",
        "overlays": "ENFA, REGD, ECON, PRIV, AIGV, DEMO, FEDR, GEOG",
        "rating": "Adequate",
        "notes": [
            "AIGV overlay: Core overlay — 499 positions including AIGV-0001/0003/0004/0010/"
            "0012 explicitly stated for AI-specific risks even where universal KERN rules "
            "also apply.",
            "PRIV overlay: Strong — data privacy, surveillance architecture, and digital "
            "rights comprehensively addressed.",
            "KERN-0027 (whistleblower): Coverage through CRPT pillar qui tam provisions; "
            "tech-specific whistleblower protections (algorithm harm reporters, AI safety "
            "disclosures) may warrant explicit WBLS positions.",
            "ECON overlay: Platform market power, algorithmic pricing, and tech "
            "concentration addressed.",
        ],
        "cross_pillar": [
            "TECH AIGV positions are explicitly inherited by HLTH, JUST, ADMN, ELEC, HOUS, "
            "LABR, ENVR, FPOL, LEGL, SCIS for domain-specific AI governance.",
            "PRIV overlay positions govern digital privacy across all domains — TECH is the "
            "primary authority; other pillars inherit.",
        ],
    },
    "TERM": {
        "path": "policy/foundations/accountable_power/term_limits_and_fitness/overview.md",
        "overlays": "ENFA, DEMO",
        "rating": "Critical gaps",
        "notes": [
            "KERN-0027 (whistleblower): Absent — no protections for staff or officials who "
            "expose term limit violations, disclosure circumvention, or fitness assessment "
            "manipulation. P1-B gap.",
            "ENFA overlay: Absent — no enforcement actor specified for any of the "
            "disclosure, term limit, or fitness requirements. This is the pillar's single "
            "most critical structural gap.",
            "KERN-0013 (challenge/appeal): FITS-0003 (fitness assessment manipulation "
            "protection) present; but voter or candidate challenge rights for fitness "
            "assessments absent.",
            "Value tension: Age-based fitness requirements and equal-standing implications "
            "(NORM-0008) not surfaced — this tension requires explicit acknowledgment.",
        ],
        "cross_pillar": [
            "DEMO overlay shared with ELEC, CHKS, LEGL, EXEC — democratic accountability "
            "mechanisms across the accountable_power foundation must be architecturally "
            "consistent.",
            "CRPT (anti-corruption) covers disclosure and revolving door; TERM and CRPT "
            "positions on disclosure requirements should be non-duplicative.",
        ],
    },
}


OVERLAY_DESCRIPTIONS: dict[str, str] = {
    "ENFA": "Enforcement architecture — actors, triggers, failure consequences",
    "FEDR": "Federal-state structure — jurisdiction, preemption, interstate",
    "REGD": "Regulatory design — capture prevention, independence, revolving door",
    "AIGV": "AI governance — algorithmic systems, automated decision-making",
    "PRIV": "Privacy — data rights, surveillance limits, information control",
    "ECOL": "Ecological habitability — environment, climate, public health",
    "DEMO": "Democratic accountability — elections, representation, self-governance",
    "THRV": "Affirmative duty — material necessities, funding mechanisms",
    "ECON": "Economic justice — market power, wealth distribution, labor",
    "GEOG": "Geographic equity — rural access, regional disparities",
}


def build_declaration(domain: str, data: dict) -> str:
    overlays = data["overlays"]
    rating = data["rating"]
    notes = data["notes"]
    cross_pillar = data["cross_pillar"]

    overlay_list = [o.strip() for o in overlays.split(",")]

    overlay_rows = []
    for o in overlay_list:
        desc = OVERLAY_DESCRIPTIONS.get(o, "")
        overlay_rows.append(f"| {o} | {desc} |")

    notes_block = "\n".join(f"- {n}" for n in notes)
    cross_block = "\n".join(f"- {c}" for c in cross_pillar)

    return f"""
---

## PolicyOS Inheritance Declaration

*Compliance document per PAOS-TEST-0003. Established: 2026-04-27. Next review: per MAINT-0006.*

**Domain:** {domain}
**Audit status (2026-04-27):** {rating}

### Applicable overlays

KERN (universal — all 27 rules) applies to this pillar without exception.

| Overlay | Scope |
|---|---|
| KERN | Universal — all 27 rules; no domain-specific exclusions |
{chr(10).join(overlay_rows)}

### Key compliance notes

{notes_block}

### Cross-pillar interactions

{cross_block}
"""


def process_file(domain: str, data: dict) -> None:
    path = REPO_ROOT / data["path"]
    if not path.exists():
        print(f"  SKIP (not found): {path}", file=sys.stderr)
        return

    content = path.read_text(encoding="utf-8")
    if MARKER in content:
        print(f"  SKIP (already present): {domain}")
        return

    declaration = build_declaration(domain, data)
    path.write_text(content.rstrip() + "\n" + declaration, encoding="utf-8")
    print(f"  OK: {domain} → {data['path']}")


def main() -> None:
    print(f"Adding inheritance declarations to {len(PILLAR_DATA)} pillars…\n")
    for domain, data in sorted(PILLAR_DATA.items()):
        process_file(domain, data)
    print("\nDone.")


if __name__ == "__main__":
    main()
