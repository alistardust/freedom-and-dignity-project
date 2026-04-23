#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


NUMERIC_SOURCE_PRIORITY = {
    "main-branch.txt": 1,
    "brainstorm-branch.txt": 2,
    "brainstorm-branch1part2.txt": 2,
    "comparisons-branch.txt": 3,
    "AI-statement-branch.txt": 4,
}

# Fetched directly from ChatGPT API — higher fidelity than copy-paste exports.
# These live under sources/chatgpt-fetched/ and use the same priority tiers.
FETCHED_SOURCE_PRIORITY = {
    "political_project_main.txt": 1,
    "branch_branch_political_project_main.txt": 1,
    "political_project_brainstorm.txt": 2,
    "branch_political_project_brainstorm.txt": 2,
    "political_project_comparisons.txt": 3,
}

NUMERIC_ROW_MIN_FIELDS = 4
RULE_ID_RE = re.compile(r"^[A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?$")
PROSE_RULE_ID_RE = re.compile(r"^([A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?)\s{1,2}(.+)$")
MIGRATION_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([A-Z]+)\s*\|\s*([^|]*)\|\s*$"
)
MANUAL_RULE_SEEDS = {
    "ECO-TAX-001": {
        "scope_code": "ECO",
        "family_code": "TAX",
        "statement": "Anti-wealth hoarding",
        "status": "PARTIAL",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21098,
    },
    "ADM-CHV-001": {
        "scope_code": "ADM",
        "family_code": "CHV",
        "statement": "Restore Chevron deference",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21099,
    },
    "ADM-AGY-001": {
        "scope_code": "ADM",
        "family_code": "AGY",
        "statement": "Congress explicitly empowered to create agencies",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21100,
    },
    "HLT-TRL-001": {
        "scope_code": "HLT",
        "family_code": "TRL",
        "statement": "Approvals and trials for new treatments funded and streamlined",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21157,
    },
    # ── Gun Policy (GUN scope) ─────────────────────────────────────────────────
    # Items 115–124 from main chat log; never received structured IDs upstream.
    # Additional rules (ACQ-002, TRN-001–003, RFL-001) sourced from brainstorm
    # log line 6385 (original detailed policy description).
    "GUN-REG-001": {
        "scope_code": "GUN",
        "family_code": "REG",
        "statement": "Amend the Constitution to explicitly affirm government authority to regulate firearms and weaponry",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17896,
    },
    "GUN-BAN-001": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Ban private ownership of weapons of war including automatic weapons and semi-automatic military analogues designed to evade regulation",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17912,
    },
    "GUN-BAN-002": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Definition of weapons of war must be evasion-resistant and cover both automatic weapons and demilitarized semi-automatic civilian versions",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-BAN-003": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Ban high-capacity ammunition magazines above a defined threshold",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-ACQ-001": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Require background checks for all firearm acquisitions",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17900,
    },
    "GUN-ACQ-002": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Background check requirement applies to all transfers including private sales and gun shows",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-ACQ-003": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Background check databases must be comprehensive, interoperable, and up to date",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-001": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require safety training as a condition of firearm ownership",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-002": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require de-escalation training as a condition of firearm ownership",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-003": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require secure storage of firearms; safe storage law as federal minimum standard",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-MHE-001": {
        "scope_code": "GUN",
        "family_code": "MHE",
        "statement": "Mental health evaluations for gun ownership must be narrowly tailored to dangerousness, not diagnosis category",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17904,
    },
    "GUN-MHE-002": {
        "scope_code": "GUN",
        "family_code": "MHE",
        "statement": "Prohibit blanket exclusion from firearm ownership based solely on a mental health diagnosis",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17908,
    },
    "GUN-RFL-001": {
        "scope_code": "GUN",
        "family_code": "RFL",
        "statement": "Establish federal minimum standards for red flag / extreme risk protection orders with due process protections",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-MIL-001": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Define 'well regulated militia' in enforceable constitutional and statutory terms",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17916,
    },
    "GUN-MIL-002": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Ban private armies and mercenary groups",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17920,
    },
    "GUN-MIL-003": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Require militias to maintain membership records, financial transparency, audits, insurance, and disclosed chain of command",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17924,
    },
    "GUN-MIL-004": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Federal and state governments must have oversight authority over militia training materials and requirements",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17928,
    },
    "GUN-MIL-005": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Provide mechanisms for regulated militias to train for disaster relief and search and rescue alongside first responders",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17932,
    },
    # ── Elections / Voter ID and Access (ELE-IDA scope) ──────────────────────
    "ELE-IDA-003": {
        "scope_code": "ELE",
        "family_code": "IDA",
        "statement": "If a state requires voter ID, it must provide free transportation to the nearest qualifying ID-issuing office for any eligible voter who lacks access; no voter may be disenfranchised by the inability to physically reach an ID office",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 16604,
    },
    "ELE-IDA-004": {
        "scope_code": "ELE",
        "family_code": "IDA",
        "statement": "States requiring voter ID must proactively identify and contact eligible voters who lack qualifying ID and offer enrollment in ID-assistance services; the burden of discovery must not fall entirely on the voter",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 16604,
    },
    "ELE-IDA-005": {
        "scope_code": "ELE",
        "family_code": "IDA",
        "statement": "Physical mobility must not be a barrier to obtaining voter ID; states requiring voter ID must provide ADA-compliant offices, home-visit ID services for voters who cannot travel, and fully functional mail and online application pathways that require no in-person trip",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 16604,
    },
    # ── Rights & Civil Liberties (RGT scope) ─────────────────────────────────
    "RGT-BOD-010": {
        "scope_code": "RGT",
        "family_code": "BOD",
        "statement": "Repeal the Comstock Act and any surviving federal provisions that suppress lawful healthcare or reproductive autonomy through archaic morality law",
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 35757,
    },
    # ── Infrastructure & Public Goods (INF scope) ─────────────────────────────
    # Items 177–187 from main chat log Section O (lines 18168–18213); supplemented
    # by structured INF-* rules from brainstorm log (lines 27852–27876).
    "INF-NET-001": {
        "scope_code": "INF",
        "family_code": "NET",
        "statement": "Internet and communications infrastructure must be treated as public infrastructure managed in the public interest",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18168,
    },
    "INF-NET-002": {
        "scope_code": "INF",
        "family_code": "NET",
        "statement": "ISPs may operate as service providers; physical network ownership must preserve public access and prevent monopoly control",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18172,
    },
    "INF-NET-003": {
        "scope_code": "INF",
        "family_code": "NET",
        "statement": "Universal internet access must be guaranteed in rural remote and underserved communities through public investment",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18176,
    },
    "INF-GRD-001": {
        "scope_code": "INF",
        "family_code": "GRD",
        "statement": "Modernize the national electrical grid for reliability resilience and clean energy capacity",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18180,
    },
    "INF-GRD-002": {
        "scope_code": "INF",
        "family_code": "GRD",
        "statement": "Transition to microgrid architecture to improve local resilience and reduce cascading failure risk",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18184,
    },
    "INF-GRD-003": {
        "scope_code": "INF",
        "family_code": "GRD",
        "statement": "Require a carbon-neutral or carbon-negative power grid",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27865,
    },
    "INF-ENR-001": {
        "scope_code": "INF",
        "family_code": "ENR",
        "statement": "Invest substantially in renewable energy generation and storage at national scale",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18188,
    },
    "INF-ENR-002": {
        "scope_code": "INF",
        "family_code": "ENR",
        "statement": "Streamline permitting and regulatory processes for nuclear energy projects that meet safety standards",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18192,
    },
    "INF-ENR-003": {
        "scope_code": "INF",
        "family_code": "ENR",
        "statement": "End oil and coal subsidies and redirect funding toward clean energy development",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27863,
    },
    "INF-ENR-004": {
        "scope_code": "INF",
        "family_code": "ENR",
        "statement": "Guarantee phaseout of oil and coal for energy production",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27864,
    },
    "INF-BLD-001": {
        "scope_code": "INF",
        "family_code": "BLD",
        "statement": "Modernize building and construction standards for energy efficiency and sustainable materials",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18204,
    },
    "INF-BLD-002": {
        "scope_code": "INF",
        "family_code": "BLD",
        "statement": "Require infrastructure systems and buildouts to be carbon neutral or carbon negative",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27866,
    },
    "INF-WAT-001": {
        "scope_code": "INF",
        "family_code": "WAT",
        "statement": "Build desalination and clean-water systems in water-scarce areas without depleting water tables or aquifers",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18196,
    },
    "INF-DAT-001": {
        "scope_code": "INF",
        "family_code": "DAT",
        "statement": "Large data centers must be carbon neutral or negative and must supply or offset their own power through dedicated clean energy sources",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18210,
    },
    "INF-RAIL-001": {
        "scope_code": "INF",
        "family_code": "RAIL",
        "statement": "Modernize the U.S. rail system",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27852,
    },
    "INF-RAIL-002": {
        "scope_code": "INF",
        "family_code": "RAIL",
        "statement": "Expand high-speed rail",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27853,
    },
    "INF-TRN-001": {
        "scope_code": "INF",
        "family_code": "TRN",
        "statement": "Expand public transportation systems",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27854,
    },
    "INF-TRN-002": {
        "scope_code": "INF",
        "family_code": "TRN",
        "statement": "Prioritize reliable affordable and accessible public transportation in infrastructure planning",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27855,
    },
    "INF-TRN-003": {
        "scope_code": "INF",
        "family_code": "TRN",
        "statement": "Phase out gasoline-only and internal-combustion-only passenger vehicles",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27874,
    },
    "INF-TRN-004": {
        "scope_code": "INF",
        "family_code": "TRN",
        "statement": "Require at minimum plug-in hybrid capability during transition periods where full electrification is not yet feasible",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27875,
    },
    "INF-TRN-005": {
        "scope_code": "INF",
        "family_code": "TRN",
        "statement": "Establish extremely strict fuel-efficiency standards during transition away from internal combustion vehicles",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 27876,
    },
    # ── Civil Access Infrastructure (CIV scope) ───────────────────────────────
    # Items 67–71 from main chat log Section D (lines 17684–17700); vital records
    # access as civic infrastructure belonging in the administrative state pillar.
    "CIV-VTL-001": {
        "scope_code": "CIV",
        "family_code": "VTL",
        "statement": "Vital records obtainable at any courthouse or records office not only the issuing location",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17684,
    },
    "CIV-VTL-002": {
        "scope_code": "CIV",
        "family_code": "VTL",
        "statement": "No requirement to travel to the issuing courthouse to obtain vital records",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17688,
    },
    "CIV-VTL-003": {
        "scope_code": "CIV",
        "family_code": "VTL",
        "statement": "Vital records access includes marriage licenses name changes birth certificates death certificates and related civil documents",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17692,
    },
    "CIV-VTL-004": {
        "scope_code": "CIV",
        "family_code": "VTL",
        "statement": "Certified vital records must be easily obtainable online by mail and in person",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17696,
    },
    "CIV-VTL-005": {
        "scope_code": "CIV",
        "family_code": "VTL",
        "statement": "Mailed vital records must be sent by certified trackable mail with delivery confirmation",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17700,
    },
    # ── Environment: national parks / wildlife / urban green space ─────────────
    # Items 175–176 from main chat log Section O (lines 18158–18167); added to
    # environment-and-agriculture.html as ENV-BIO-003 and ENV-BIO-004.
    "ENV-BIO-003": {
        "scope_code": "ENV",
        "family_code": "BIO",
        "statement": "Protect wildlife habitats and national parks from exploitation degradation and commercial encroachment",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18158,
    },
    "ENV-BIO-004": {
        "scope_code": "ENV",
        "family_code": "BIO",
        "statement": "Require urban green spaces with public access in city planning and development standards",
        "status": "MISSING",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 18163,
    },
    # ── Education (EDU scope) ──────────────────────────────────────────────────
    # Extracted from docs/pillars/education.html; canonical statements and line
    # numbers sourced from branch_political_project_brainstorm.txt.
    # EDU-SYS: System Foundations
    "EDU-SYS-001": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Education systems must provide universal access to high-quality learning that enables autonomy, economic mobility, critical thinking, and full participation in society.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43166,
    },
    "EDU-SYS-002": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Educational opportunity may not be determined by wealth, geography, race, disability, or family background.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43170,
    },
    "EDU-SYS-003": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Education systems must be designed for long-term human development, not short-term testing metrics or administrative convenience.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43174,
    },
    "EDU-SYS-004": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Access to education that is necessary for economic participation and mobility must not require long-term debt burdens.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43466,
    },
    "EDU-SYS-005": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Education is a public good and must be primarily delivered through a universal, high-quality, publicly governed system rather than market-based alternatives.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44260,
    },
    "EDU-SYS-006": {
        "scope_code": "EDU",
        "family_code": "SYS",
        "statement": 'Public education funding must be used to strengthen public systems and may not be diverted in ways that undermine universal access or quality.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44264,
    },
    # EDU-ACC: Access & Equity
    "EDU-ACC-001": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'All individuals must have access to free, high-quality primary and secondary education.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43182,
    },
    "EDU-ACC-002": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Access to higher education, vocational training, and lifelong learning must be broadly available and not restricted by financial barriers.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43186,
    },
    "EDU-ACC-003": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Educational systems must actively correct disparities in access, resources, and outcomes across regions and populations.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43190,
    },
    "EDU-ACC-004": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Students with disabilities must receive full access to education with appropriate accommodations and support systems.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43194,
    },
    "EDU-ACC-005": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Students must have access to safe and reliable transportation necessary to attend assigned or chosen schools.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43908,
    },
    "EDU-ACC-006": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Transportation systems may not be structured in ways that limit access to higher-quality schools based on geography or income.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43912,
    },
    "EDU-ACC-007": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Publicly funded education must be subject to transparency, non-discrimination, and accountability standards that ensure equal access and public oversight.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44332,
    },
    "EDU-ACC-008": {
        "scope_code": "EDU",
        "family_code": "ACC",
        "statement": 'Education systems receiving public funding may not exclude students based on ability, disability, behavior, religion, or economic status.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44336,
    },
    # EDU-FND: Funding
    "EDU-FND-001": {
        "scope_code": "EDU",
        "family_code": "FND",
        "statement": 'Education funding systems may not rely on local property wealth in ways that produce unequal educational quality.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43204,
    },
    "EDU-FND-002": {
        "scope_code": "EDU",
        "family_code": "FND",
        "statement": 'Public funding must ensure baseline parity of educational resources, facilities, staffing, and materials across all regions.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43208,
    },
    "EDU-FND-003": {
        "scope_code": "EDU",
        "family_code": "FND",
        "statement": 'Schools serving higher-need populations must receive additional resources sufficient to address those needs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43212,
    },
    # EDU-QLT: Quality
    "EDU-QLT-001": {
        "scope_code": "EDU",
        "family_code": "QLT",
        "statement": 'Education systems must provide high-quality instruction, materials, and learning environments that meet defined standards of effectiveness.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43220,
    },
    "EDU-QLT-002": {
        "scope_code": "EDU",
        "family_code": "QLT",
        "statement": 'Curriculum must include literacy, numeracy, science, history, civics, critical thinking, and media literacy.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43224,
    },
    "EDU-QLT-003": {
        "scope_code": "EDU",
        "family_code": "QLT",
        "statement": 'Education must prepare students for real-world skills, including financial literacy, digital literacy, and practical life competencies.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43228,
    },
    "EDU-QLT-004": {
        "scope_code": "EDU",
        "family_code": "QLT",
        "statement": 'Education systems must avoid overreliance on standardized testing as the primary measure of learning or school quality.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43232,
    },
    # EDU-WRK: Workforce / Teachers
    "EDU-WRK-001": {
        "scope_code": "EDU",
        "family_code": "WRK",
        "statement": 'Teachers must be compensated at levels that reflect their professional importance and enable long-term retention.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43242,
    },
    "EDU-WRK-002": {
        "scope_code": "EDU",
        "family_code": "WRK",
        "statement": 'Teachers must have access to training, continuing education, and professional development.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43246,
    },
    "EDU-WRK-003": {
        "scope_code": "EDU",
        "family_code": "WRK",
        "statement": 'Teacher workloads must be reasonable and may not rely on unpaid labor, chronic overtime, or burnout-driven expectations.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43250,
    },
    "EDU-WRK-004": {
        "scope_code": "EDU",
        "family_code": "WRK",
        "statement": 'Educators must have professional autonomy in instruction within established curriculum standards.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43254,
    },
    # EDU-STU: Student Well-being
    "EDU-STU-001": {
        "scope_code": "EDU",
        "family_code": "STU",
        "statement": 'Schools must support student physical, mental, and emotional well-being alongside academic development.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43262,
    },
    "EDU-STU-002": {
        "scope_code": "EDU",
        "family_code": "STU",
        "statement": 'Students must have access to counseling, mental health support, and safe learning environments.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43266,
    },
    "EDU-STU-003": {
        "scope_code": "EDU",
        "family_code": "STU",
        "statement": 'Disciplinary systems must be fair, proportional, and not contribute to systemic exclusion or harm.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43270,
    },
    # EDU-EXT: Exploitation Prevention
    "EDU-EXT-001": {
        "scope_code": "EDU",
        "family_code": "EXT",
        "statement": 'Educational systems may not be structured primarily for profit extraction at the expense of educational quality or access.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43280,
    },
    "EDU-EXT-002": {
        "scope_code": "EDU",
        "family_code": "EXT",
        "statement": 'Predatory practices in student lending, for-profit education, or certification programs must be prohibited or strictly regulated.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43284,
    },
    "EDU-EXT-003": {
        "scope_code": "EDU",
        "family_code": "EXT",
        "statement": 'Students may not be burdened with excessive debt for access to essential education.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43288,
    },
    # EDU-VOC: Vocational Education
    "EDU-VOC-001": {
        "scope_code": "EDU",
        "family_code": "VOC",
        "statement": 'Education systems must include strong vocational, technical, and apprenticeship pathways alongside traditional academic tracks.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43296,
    },
    "EDU-VOC-002": {
        "scope_code": "EDU",
        "family_code": "VOC",
        "statement": 'Vocational and technical education must be treated as equal in dignity and opportunity to academic pathways.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43300,
    },
    "EDU-VOC-003": {
        "scope_code": "EDU",
        "family_code": "VOC",
        "statement": 'Partnerships between education and industry must prioritize worker outcomes, not labor exploitation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43304,
    },
    # EDU-HED: Higher Education
    "EDU-HED-001": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Higher education must be financially accessible and may not require unsustainable debt burdens.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43312,
    },
    "EDU-HED-002": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Public investment in higher education must prioritize affordability, quality, and research integrity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43316,
    },
    "EDU-HED-003": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Student loan systems must include strong borrower protections, fair repayment structures, and relief mechanisms.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43320,
    },
    "EDU-HED-004": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Public community colleges, technical schools, and trade programs must be tuition-free for all eligible students.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43476,
    },
    "EDU-HED-005": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Tuition-free access must include core instructional costs and may not be undermined by hidden fees, administrative costs, or indirect barriers.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43480,
    },
    "EDU-HED-006": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Tuition-free programs must include part-time students, adult learners, and workers seeking reskilling or career transitions.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43486,
    },
    "EDU-HED-007": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Trade, vocational, and certification programs must receive funding parity and institutional support equivalent to academic pathways.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43490,
    },
    "EDU-HED-008": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Public investment in community and technical education must align with labor market needs while protecting workers from exploitation or wage suppression.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43496,
    },
    "EDU-HED-010": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Higher education must function as a public-interest system that expands knowledge, mobility, and opportunity rather than a debt-driven or prestige-gated market.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44959,
    },
    "EDU-HED-011": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Admissions processes must be fair, transparent, and may not privilege wealth, legacy status, donor influence, or other non-meritocratic advantages.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44967,
    },
    "EDU-HED-012": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions may not use admissions practices that systematically exclude students based on socioeconomic background, disability, or access to preparatory resources.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44971,
    },
    "EDU-HED-013": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Standardized testing may not be used as the sole or dominant admissions factor where it reinforces structural inequity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44975,
    },
    "EDU-HED-014": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must provide multiple pathways to admission, including transfer, adult entry, and non-traditional student access.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44979,
    },
    "EDU-HED-015": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions receiving public funding must be accountable for student outcomes, including graduation rates, employment outcomes, and debt burdens.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44987,
    },
    "EDU-HED-016": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Persistent failure to meet baseline outcome standards must trigger corrective action, funding conditions, or loss of eligibility for public support.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44991,
    },
    "EDU-HED-017": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions may not rely on enrollment growth or tuition expansion without corresponding improvements in quality and outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44995,
    },
    "EDU-HED-018": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must demonstrate responsible use of tuition and public funds, prioritizing instruction, student support, and academic quality over administrative expansion.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45003,
    },
    "EDU-HED-019": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Excessive administrative cost growth that does not improve student outcomes must be subject to review and corrective measures.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45007,
    },
    "EDU-HED-020": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Tuition increases must be justified, transparent, and subject to oversight where public funding is involved.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45011,
    },
    "EDU-HED-021": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must maintain stable, fairly compensated academic workforces and may not rely excessively on contingent or underpaid labor to deliver core instruction.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45021,
    },
    "EDU-HED-022": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Faculty must have academic freedom in research, teaching, and scholarship within established professional standards.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45025,
    },
    "EDU-HED-023": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Academic labor practices must align with broader labor standards, including fair pay, job security, and reasonable workloads.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45029,
    },
    "EDU-HED-024": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must maintain strong standards for academic integrity, research validity, and prevention of fraud, fabrication, or misconduct.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45037,
    },
    "EDU-HED-025": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Research funding and partnerships may not compromise academic independence or distort scientific outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45041,
    },
    "EDU-HED-026": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Conflicts of interest in research, funding, or publication must be disclosed and managed transparently.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45045,
    },
    "EDU-HED-027": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Accreditation systems must ensure educational quality and accountability without functioning as anti-competitive barriers to entry.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45055,
    },
    "EDU-HED-028": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Accreditation must be based on outcomes, quality, and student success rather than institutional prestige or legacy status.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45059,
    },
    "EDU-HED-029": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'New or alternative education providers must have pathways to accreditation if they meet defined quality and outcome standards.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45063,
    },
    "EDU-HED-030": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Students must have rights to fair treatment, due process in disciplinary actions, and protection from discrimination or retaliation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45071,
    },
    "EDU-HED-031": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must provide clear information on costs, outcomes, program value, and career pathways.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45075,
    },
    "EDU-HED-032": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Students may not be misled about job placement rates, earnings potential, or program effectiveness.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45079,
    },
    "EDU-HED-033": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions must maintain safe campus environments, including strong protections against harassment, assault, and abuse.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45087,
    },
    "EDU-HED-034": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Reporting systems must be accessible, fair, and not structured to protect institutional reputation over student safety.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45091,
    },
    "EDU-HED-035": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Students must be able to transfer credits between accredited institutions without unnecessary loss of progress.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45101,
    },
    "EDU-HED-036": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Public systems must establish standardized credit frameworks to improve mobility and reduce duplication of coursework.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45105,
    },
    "EDU-HED-037": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Prior learning, work experience, and non-traditional education must be recognized where appropriate.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45109,
    },
    "EDU-HED-038": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Public higher education institutions must serve broad societal goals including research, civic engagement, workforce development, and public knowledge.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45117,
    },
    "EDU-HED-039": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Institutions may not prioritize rankings, exclusivity, or prestige over access, affordability, and public impact.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45121,
    },
    "EDU-HED-040": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Higher education may not function primarily as a revenue extraction system through tuition, fees, or debt generation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45129,
    },
    "EDU-HED-041": {
        "scope_code": "EDU",
        "family_code": "HED",
        "statement": 'Financial models that depend on unsustainable student debt or misleading value propositions must be reformed or eliminated.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45133,
    },
    # EDU-LIF: Lifelong Learning
    "EDU-LIF-001": {
        "scope_code": "EDU",
        "family_code": "LIF",
        "statement": 'Individuals must have access to lifelong learning, reskilling, and continuing education throughout their lives.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43330,
    },
    "EDU-LIF-002": {
        "scope_code": "EDU",
        "family_code": "LIF",
        "statement": 'Public systems must support workers transitioning due to automation, economic change, or displacement.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43334,
    },
    # EDU-CIV: Civic Education
    "EDU-CIV-001": {
        "scope_code": "EDU",
        "family_code": "CIV",
        "statement": 'Education must include strong civic education covering government, rights, responsibilities, and democratic participation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43344,
    },
    "EDU-CIV-002": {
        "scope_code": "EDU",
        "family_code": "CIV",
        "statement": 'Students must be equipped to critically evaluate information, media, and political claims.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43348,
    },
    "EDU-CIV-003": {
        "scope_code": "EDU",
        "family_code": "CIV",
        "statement": 'Education systems may not be used for political indoctrination or suppression of factual inquiry.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43352,
    },
    # EDU-GOV: Governance
    "EDU-GOV-001": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Education systems must be transparent, accountable, and subject to oversight based on outcomes and fairness.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43360,
    },
    "EDU-GOV-002": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Policies must be evaluated based on student outcomes, equity, and long-term success rather than administrative metrics alone.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43364,
    },
    "EDU-GOV-003": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Communities must have meaningful input into education systems without enabling exclusion, discrimination, or resource inequity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43368,
    },
    "EDU-GOV-004": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Education systems must track and publicly report data on segregation, resource distribution, and student outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43920,
    },
    "EDU-GOV-005": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Persistent patterns of segregation or inequity must trigger mandatory corrective action at the state or federal level.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43924,
    },
    "EDU-GOV-006": {
        "scope_code": "EDU",
        "family_code": "GOV",
        "statement": 'Policies that worsen segregation or inequity must be subject to review, modification, or removal.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43928,
    },
    # EDU-DEBT: Student Debt
    "EDU-DEBT-001": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Broad federal student loan forgiveness must be implemented to reduce or eliminate existing unsustainable student debt burdens.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43506,
    },
    "EDU-DEBT-002": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Debt relief must prioritize borrowers most affected by economic hardship, predatory lending, or low-return educational outcomes while providing broad-based relief.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43510,
    },
    "EDU-DEBT-003": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Student loan systems must be restructured to prevent re-accumulation of unsustainable debt following forgiveness programs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43516,
    },
    "EDU-DEBT-004": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Interest structures, repayment systems, and loan servicing practices must be fair, transparent, and not designed for long-term extraction.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43520,
    },
    "EDU-DEBT-005": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Institutions with consistently poor student outcomes, high default rates, or misleading practices must be subject to penalties, funding restrictions, or loss of eligibility for federal aid.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43526,
    },
    "EDU-DEBT-006": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Educational institutions may not shift financial risk onto students while retaining disproportionate financial benefit.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43530,
    },
    "EDU-DEBT-007": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Predatory student lending practices, including deceptive marketing, abusive terms, or misrepresentation of outcomes, must be prohibited.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43538,
    },
    "EDU-DEBT-008": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Loan servicing must be regulated to ensure accurate information, fair treatment, and access to repayment options and relief programs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43542,
    },
    "EDU-DEBT-009": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Public education funding models should reduce reliance on student debt through direct funding, subsidies, or alternative financing mechanisms.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43552,
    },
    "EDU-DEBT-010": {
        "scope_code": "EDU",
        "family_code": "DEBT",
        "statement": 'Any alternative financing models must not replicate debt-like extraction or shift disproportionate risk onto students.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43556,
    },
    # EDU-SEC: Secularism
    "EDU-SEC-001": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Public education must remain religiously neutral, may not promote or endorse religious belief or non-belief, and must protect student freedom of conscience.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43651,
    },
    "EDU-SEC-002": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Public schools and their employees may not engage in religious indoctrination, proselytizing, or endorsement of any religion or belief system in their official capacity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43659,
    },
    "EDU-SEC-003": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'School policies, curricula, and official activities must not be structured to pressure, coerce, or incentivize religious participation or belief.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43663,
    },
    "EDU-SEC-004": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Public resources, instructional time, and school-sponsored platforms may not be used to promote or advance religious doctrine.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43667,
    },
    "EDU-SEC-005": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Students retain the right to individual religious expression, voluntary prayer, and student-led religious activity, provided it is not school-sponsored or coercive.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43677,
    },
    "EDU-SEC-006": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Schools must protect students from discrimination or retaliation based on religion, non-religion, or personal beliefs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43681,
    },
    "EDU-SEC-007": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Violations of religious neutrality or evidence-based curriculum standards must be subject to investigation, corrective action, and enforcement by appropriate educational and legal authorities.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43717,
    },
    "EDU-SEC-008": {
        "scope_code": "EDU",
        "family_code": "SEC",
        "statement": 'Students and families must have accessible mechanisms to report violations of religious neutrality or improper instruction.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43721,
    },
    # EDU-SCI: Science Curriculum
    "EDU-SCI-001": {
        "scope_code": "EDU",
        "family_code": "SCI",
        "statement": 'Science curricula in public education must be based on established scientific methods, empirical evidence, and peer-reviewed consensus.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43691,
    },
    "EDU-SCI-002": {
        "scope_code": "EDU",
        "family_code": "SCI",
        "statement": 'Non-scientific belief systems, including religious or metaphysical explanations, may not be taught as scientific theory within science curricula.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43695,
    },
    "EDU-SCI-003": {
        "scope_code": "EDU",
        "family_code": "SCI",
        "statement": 'Topics such as religion, philosophy, and cultural belief systems may be taught in appropriate academic contexts, including history or comparative religion, without endorsement or promotion.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43699,
    },
    "EDU-SCI-004": {
        "scope_code": "EDU",
        "family_code": "SCI",
        "statement": 'Concepts such as “Intelligent Design” or similar frameworks that lack empirical scientific basis may not be presented as scientific theory in public school science instruction.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43709,
    },
    # EDU-STR: Structural Equity
    "EDU-STR-001": {
        "scope_code": "EDU",
        "family_code": "STR",
        "statement": 'Education systems must not structurally produce or reinforce segregation by race, income, disability, or geography.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43804,
    },
    "EDU-STR-002": {
        "scope_code": "EDU",
        "family_code": "STR",
        "statement": 'School assignment systems must balance community access with fairness, diversity, and equal opportunity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43808,
    },
    # EDU-ZON: Zoning & Boundaries
    "EDU-ZON-001": {
        "scope_code": "EDU",
        "family_code": "ZON",
        "statement": 'School district boundaries and attendance zones may not be drawn or maintained in ways that produce extreme disparities in resources or outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43818,
    },
    "EDU-ZON-002": {
        "scope_code": "EDU",
        "family_code": "ZON",
        "statement": 'States must periodically review and adjust district boundaries to reduce segregation and improve equity in access and outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43822,
    },
    "EDU-ZON-003": {
        "scope_code": "EDU",
        "family_code": "ZON",
        "statement": 'Where local district structures produce persistent inequity, states must implement regional or multi-district systems to equalize opportunity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43828,
    },
    "EDU-ZON-004": {
        "scope_code": "EDU",
        "family_code": "ZON",
        "statement": 'Regional systems must include fair resource allocation, shared enrollment access, and transportation support.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43832,
    },
    # EDU-INT: Integration
    "EDU-INT-001": {
        "scope_code": "EDU",
        "family_code": "INT",
        "statement": 'Education systems must use lawful, evidence-based methods to promote socioeconomic and demographic diversity in schools.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43842,
    },
    "EDU-INT-002": {
        "scope_code": "EDU",
        "family_code": "INT",
        "statement": 'School assignment systems may incorporate multiple factors, including geography and socioeconomic indicators, to reduce segregation and improve access.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43846,
    },
    "EDU-INT-003": {
        "scope_code": "EDU",
        "family_code": "INT",
        "statement": 'Tracking, gifted programs, and selective admissions within public schools may not be structured in ways that systematically segregate students.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43852,
    },
    # EDU-CHO: School Choice
    "EDU-CHO-001": {
        "scope_code": "EDU",
        "family_code": "CHO",
        "statement": 'Public school choice systems must be designed to expand access and opportunity without increasing segregation or resource inequity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43862,
    },
    "EDU-CHO-002": {
        "scope_code": "EDU",
        "family_code": "CHO",
        "statement": 'Charter and alternative public schools must meet the same equity, access, and accountability standards as traditional public schools.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43866,
    },
    "EDU-CHO-003": {
        "scope_code": "EDU",
        "family_code": "CHO",
        "statement": 'School choice policies may not be used to exclude, screen, or indirectly filter students based on income, disability, or academic history.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43870,
    },
    # EDU-PRV: Private Schools
    "EDU-PRV-001": {
        "scope_code": "EDU",
        "family_code": "PRV",
        "statement": 'Public funds used for private education must be subject to strict accountability, non-discrimination, and educational-quality requirements.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43880,
    },
    "EDU-PRV-002": {
        "scope_code": "EDU",
        "family_code": "PRV",
        "statement": 'Voucher or subsidy programs may not enable segregation, exclusion, or diversion of public resources that materially harms public education systems.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43884,
    },
    "EDU-PRV-003": {
        "scope_code": "EDU",
        "family_code": "PRV",
        "statement": 'Policies that functionally replicate vouchers, including tax-credit schemes, education savings accounts, or indirect subsidy mechanisms, are subject to the same restrictions as voucher programs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44320,
    },
    "EDU-PRV-004": {
        "scope_code": "EDU",
        "family_code": "PRV",
        "statement": 'Public education resources, including funding, facilities, and staffing, may not be diverted to private operators in ways that degrade public system capacity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44324,
    },
    # EDU-AI: AI in Education
    "EDU-AI-001": {
        "scope_code": "EDU",
        "family_code": "AI",
        "statement": 'AI systems used in education must preserve enough provenance and reviewable records to permit challenge of grading, placement, discipline, or access decisions.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 42981,
    },
    "EDU-AI-002": {
        "scope_code": "EDU",
        "family_code": "AI",
        "statement": 'High-impact educational AI must undergo pre-deployment educational-impact, bias, and developmental-risk review before broad institutional use.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 42983,
    },
    "EDU-AI-003": {
        "scope_code": "EDU",
        "family_code": "AI",
        "statement": 'Educational AI may not silently shift from assistive tutoring or accessibility functions into delegated assessment, placement, or disciplinary authority.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 42985,
    },
    # EDU-DAT: Student Data
    "EDU-DAT-001": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Student data, behavior, and learning activity must be protected as sensitive information and may not be exploited for commercial, surveillance, or non-educational purposes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45240,
    },
    "EDU-DAT-002": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Schools and educational systems may collect only the data necessary to provide education, support services, and safety.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45248,
    },
    "EDU-DAT-003": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Collection of biometric, behavioral, psychological, or predictive data must be strictly limited and require strong justification and safeguards.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45252,
    },
    "EDU-DAT-004": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Student data may not be sold, traded, licensed, or used for advertising, profiling, or commercial purposes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45260,
    },
    "EDU-DAT-005": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Educational technology providers may not use student data to train unrelated commercial systems or models.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45264,
    },
    "EDU-DAT-006": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Schools may not implement pervasive or continuous surveillance systems that monitor student behavior beyond what is necessary for safety and educational function.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45272,
    },
    "EDU-DAT-007": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'AI or automated systems may not be used to profile, score, or predict student behavior, risk, or outcomes in ways that materially affect discipline, opportunity, or access without strong safeguards and human review.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45276,
    },
    "EDU-DAT-008": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Students and families must have the right to access, review, correct, and challenge data held about them.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45284,
    },
    "EDU-DAT-009": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Students and families must be informed of what data is collected, how it is used, and who has access to it.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45288,
    },
    "EDU-DAT-010": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Violations of student data protections must trigger investigation, penalties, and corrective action.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45296,
    },
    "EDU-DAT-011": {
        "scope_code": "EDU",
        "family_code": "DAT",
        "statement": 'Educational systems must maintain audit logs and oversight mechanisms for data access, use, and sharing.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 45300,
    },
    # EDU-ECE: Early Childhood Education
    "EDU-ECE-001": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood education and childcare are essential public goods and must be treated as foundational social infrastructure.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44441,
    },
    "EDU-ECE-002": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Access to high-quality early childhood education and childcare may not depend primarily on family wealth, geography, or employer benefit structure.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44443,
    },
    "EDU-ECE-003": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Universal access to high-quality pre-kindergarten must be guaranteed.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44447,
    },
    "EDU-ECE-004": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Affordable, high-quality childcare must be broadly available for infants, toddlers, and preschool-age children.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44449,
    },
    "EDU-ECE-005": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Access systems must include full-time, part-time, and flexible options sufficient to meet the needs of families, caregivers, and workers.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44451,
    },
    "EDU-ECE-006": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood programs must meet strong developmental, safety, staffing, and quality standards appropriate to child development.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44455,
    },
    "EDU-ECE-007": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood education must prioritize language development, social development, emotional development, play, curiosity, and foundational learning rather than narrow academic pressure alone.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44457,
    },
    "EDU-ECE-008": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood systems may not rely on low-quality custodial warehousing as a substitute for developmentally appropriate care and education.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44459,
    },
    "EDU-ECE-009": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood educators and childcare workers must be compensated at levels that reflect the importance and professional demands of their work.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44465,
    },
    "EDU-ECE-010": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood staffing systems must include training, credentialing pathways, continuing education, and workforce support.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44467,
    },
    "EDU-ECE-011": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare and early education systems may not rely on chronic underpayment, burnout, or unsustainable turnover to remain operational.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44469,
    },
    "EDU-ECE-012": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood systems must actively correct disparities in access and quality across income levels, disability status, race, language background, and geography.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44473,
    },
    "EDU-ECE-013": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Families in rural areas, lower-income communities, and underserved regions must receive targeted support to ensure equal practical access.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44475,
    },
    "EDU-ECE-014": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood systems must include strong inclusion and accommodation requirements for children with disabilities and developmental differences.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44477,
    },
    "EDU-ECE-015": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare and early childhood systems must be designed to support family stability, caregiver participation in work or education, and child well-being simultaneously.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44483,
    },
    "EDU-ECE-016": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Families may not be forced out of work, education, or training due to lack of accessible childcare.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44485,
    },
    "EDU-ECE-017": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Public funding models must reduce childcare costs to families to levels that are genuinely affordable in practice.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44487,
    },
    "EDU-ECE-018": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood and childcare funding must prioritize public, nonprofit, cooperative, and other non-extractive delivery systems over profit-maximizing structures.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44491,
    },
    "EDU-ECE-019": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Public funding may not be used to sustain low-quality, extractive, or poorly regulated childcare models.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44493,
    },
    "EDU-ECE-020": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Governments must directly build, support, or coordinate childcare capacity where private markets fail to provide sufficient access, affordability, or quality.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44495,
    },
    "EDU-ECE-021": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood providers must be subject to strong health, safety, staffing, and abuse-prevention standards.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44499,
    },
    "EDU-ECE-022": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Families must have access to clear information about provider quality, licensing status, complaints, inspections, and safety outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44501,
    },
    "EDU-ECE-023": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Repeated safety, neglect, abuse, or quality failures must trigger corrective action, sanctions, or loss of eligibility for public funding.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44503,
    },
    "EDU-ECE-024": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood systems should be coordinated with K–12 education, healthcare, disability services, and family support systems to improve continuity and outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44507,
    },
    "EDU-ECE-025": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Pre-K and childcare systems must include screening and early support for developmental, educational, and health needs with safeguards against stigma or exclusion.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44509,
    },
    "EDU-ECE-026": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare and early childhood systems may not be structured around administrative complexity, unstable eligibility, or reimbursement failures that undermine providers and families.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44513,
    },
    "EDU-ECE-027": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Families and providers must have clear, navigable access to enrollment, payment, subsidy, and support systems without excessive procedural burden.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44515,
    },
    "EDU-ECE-028": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood systems must be evaluated based on child development, safety, equity, family stability, and workforce sustainability rather than enrollment volume alone.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44519,
    },
    "EDU-ECE-029": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Early childhood policy must recognize long-term developmental and economic returns and may not treat childcare as merely a private household problem.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44521,
    },
    "EDU-ECE-030": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Universal access to high-quality childcare must be guaranteed as a public service for all families who require it.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44595,
    },
    "EDU-ECE-031": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare services must be provided at no cost or at minimal cost to families, with public funding covering the majority of system costs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44607,
    },
    "EDU-ECE-032": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Governments must ensure sufficient childcare capacity such that all families can access care without long waitlists, geographic exclusion, or scarcity barriers.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44630,
    },
    "EDU-ECE-033": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Where private markets fail to provide sufficient childcare capacity, public systems must directly build, expand, or operate childcare services.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44634,
    },
    "EDU-ECE-034": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare systems must provide hours and scheduling that align with real work patterns, including non-standard, shift-based, and part-time employment.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44642,
    },
    "EDU-ECE-035": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Childcare access may not be restricted to limited hours that effectively exclude working families.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44646,
    },
    "EDU-ECE-036": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Universal childcare systems may not exclude children based on disability, behavioral needs, family income, or parental employment status.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44654,
    },
    "EDU-ECE-037": {
        "scope_code": "EDU",
        "family_code": "ECE",
        "statement": 'Universal childcare systems must maintain quality, safety, staffing, and developmental standards and may not expand access at the expense of care quality.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44662,
    },
    # EDU-SPD: Special Education
    "EDU-SPD-001": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Children and students with disabilities have a right to free, high-quality, appropriate public education with the supports, accommodations, and services necessary for meaningful access and progress.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44783,
    },
    "EDU-SPD-002": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special education rights may not be weakened by funding shortfalls, staffing shortages, administrative burden, or district convenience.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44785,
    },
    "EDU-SPD-003": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Disability-related educational access must be treated as a civil-rights obligation, not a discretionary service.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44787,
    },
    "EDU-SPD-004": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Schools must identify, evaluate, and support students with disabilities or developmental differences in a timely and proactive manner.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44791,
    },
    "EDU-SPD-005": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Evaluation systems may not rely on delay, denial, or excessive procedural burden to avoid providing services.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44793,
    },
    "EDU-SPD-006": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Students must have access to re-evaluation and updated support when needs change or previous evaluations prove inadequate.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44795,
    },
    "EDU-SPD-007": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Families must have clear rights to request evaluation, independent assessment, and review of school determinations.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44797,
    },
    "EDU-SPD-008": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Students with disabilities must receive individualized supports and services sufficient to provide real educational benefit, not merely nominal access.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44801,
    },
    "EDU-SPD-009": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Individualized education plans and equivalent support structures must be specific, enforceable, and written in clear language.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44803,
    },
    "EDU-SPD-010": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Schools may not offer generic, under-scoped, or minimally compliant supports where stronger individualized supports are necessary.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44805,
    },
    "EDU-SPD-011": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Accommodations, therapies, assistive technology, and related services must be provided in a timely manner once identified as necessary.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44807,
    },
    "EDU-SPD-012": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Students with disabilities must be educated in inclusive settings to the maximum extent appropriate, with supports sufficient to make inclusion meaningful.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44811,
    },
    "EDU-SPD-013": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Separate placements may be used only where clearly necessary for the student’s needs and not as a convenience to the institution.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44813,
    },
    "EDU-SPD-014": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Inclusion policy must not become a pretext for denying specialized services, and specialized placement must not become a pretext for segregation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44815,
    },
    "EDU-SPD-015": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Schools and education systems must maintain sufficient numbers of qualified special-education teachers, aides, therapists, and related staff to meet student needs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44819,
    },
    "EDU-SPD-016": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Staffing shortages may not be used as justification for denying or reducing legally required services.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44821,
    },
    "EDU-SPD-017": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special-education personnel must receive strong training, ongoing support, and reasonable workloads sufficient to provide effective services.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44823,
    },
    "EDU-SPD-018": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Families must have meaningful participation rights in special-education planning, placement, review, and dispute processes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44827,
    },
    "EDU-SPD-019": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Schools must provide families with clear explanations of rights, services, options, timelines, and appeal procedures.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44829,
    },
    "EDU-SPD-020": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Families must have access to advocacy, translation, interpretation, and procedural support so rights are usable in practice.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44831,
    },
    "EDU-SPD-021": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Retaliation against families for asserting disability rights, requesting services, or challenging school decisions is prohibited.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44833,
    },
    "EDU-SPD-022": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special-education rights must be enforceable through accessible complaint systems, hearings, corrective action, judicial review, and meaningful remedies.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44837,
    },
    "EDU-SPD-023": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Dispute-resolution systems may not be structured to exhaust, outspend, or procedurally defeat families seeking lawful services.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44839,
    },
    "EDU-SPD-024": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Where schools fail to provide required services, remedies must include compensatory services, reimbursement, corrective plans, and additional enforcement where appropriate.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44841,
    },
    "EDU-SPD-025": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Repeated or systemic noncompliance with disability education obligations must trigger state or federal intervention, sanctions, and oversight.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44843,
    },
    "EDU-SPD-026": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Students with disabilities may not be disproportionately disciplined, excluded, restrained, or removed due to unmet support needs or disability-related behavior.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44847,
    },
    "EDU-SPD-027": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Disciplinary systems must account for disability, communication needs, trauma, and support failures before exclusionary measures are used.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44849,
    },
    "EDU-SPD-028": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Seclusion, restraint, and related coercive practices in educational settings must be strictly limited, transparently documented, and prohibited except under narrow emergency conditions.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44851,
    },
    "EDU-SPD-029": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Educational materials, platforms, facilities, and communications must be fully accessible to students with disabilities.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44855,
    },
    "EDU-SPD-030": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Students who need assistive technology, accessible materials, or adaptive tools must receive them without undue delay or cost shifting to families.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44857,
    },
    "EDU-SPD-031": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Digital education systems and educational technology must meet accessibility standards and may not exclude or degrade participation for disabled students.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44859,
    },
    "EDU-SPD-032": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special-education systems must monitor and correct disparities in identification, placement, discipline, service quality, and outcomes across race, language background, income, and geography.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44863,
    },
    "EDU-SPD-033": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Disability rights in education apply equally to students in early childhood, K–12, vocational, higher education, and lifelong-learning systems where relevant.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44865,
    },
    "EDU-SPD-034": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special-education systems must include transition planning for adulthood, including employment, higher education, independent living, and community participation.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44869,
    },
    "EDU-SPD-035": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Transition services may not be treated as optional or symbolic and must be tailored to the student’s actual goals and support needs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44871,
    },
    "EDU-SPD-036": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Education systems must collect and publish standardized data on evaluation timelines, service delivery, inclusion, discipline, dispute outcomes, and disability-related educational outcomes.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44875,
    },
    "EDU-SPD-037": {
        "scope_code": "EDU",
        "family_code": "SPD",
        "statement": 'Special-education policy must be evaluated on real student access, progress, inclusion, family usability, and long-term outcomes rather than formal compliance alone.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44877,
    },
    # EDU-HSG: Housing & Schools
    "EDU-HSG-001": {
        "scope_code": "EDU",
        "family_code": "HSG",
        "statement": 'Education policy must account for the relationship between housing patterns and school access, including the effects of zoning, affordability, and displacement.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43894,
    },
    "EDU-HSG-002": {
        "scope_code": "EDU",
        "family_code": "HSG",
        "statement": 'Governments must coordinate housing and education policy to reduce segregation and expand access to high-quality schools.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 43898,
    },
    # EDU-PUB: Public Schools
    "EDU-PUB-001": {
        "scope_code": "EDU",
        "family_code": "PUB",
        "statement": 'Governments must ensure that all public schools meet high standards of safety, quality, staffing, and resources sufficient to eliminate demand for private alternatives based on necessity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44302,
    },
    "EDU-PUB-002": {
        "scope_code": "EDU",
        "family_code": "PUB",
        "statement": 'Public education systems must be continuously evaluated and improved to address gaps in quality, access, and outcomes across all communities.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44306,
    },
    "EDU-PUB-003": {
        "scope_code": "EDU",
        "family_code": "PUB",
        "statement": 'Public education must include diverse program offerings, including specialized, vocational, and advanced academic pathways, within the public system.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44310,
    },
    # EDU-VCH: Vouchers
    "EDU-VCH-001": {
        "scope_code": "EDU",
        "family_code": "VCH",
        "statement": 'Public funds may not be used to subsidize private K–12 education through voucher, tax-credit, or equivalent programs.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44274,
    },
    "EDU-VCH-002": {
        "scope_code": "EDU",
        "family_code": "VCH",
        "statement": 'Education policy must prioritize strengthening public school systems rather than creating exit pathways from them.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44278,
    },
    "EDU-VCH-003": {
        "scope_code": "EDU",
        "family_code": "VCH",
        "statement": 'Limited exceptions may be permitted where necessary to ensure access for students whose needs cannot be met by available public systems, provided such programs are temporary, tightly regulated, and do not undermine public education funding or equity.',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 44288,
    },
    # EDU-FIN: Finance
    "EDU-FIN-001": {
        "scope_code": "EDU",
        "family_code": "FIN",
        "statement": 'EDU|FIN|Student loan debt forgiveness or large-scale restructuring|MISSING',
        "status": "INCLUDED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 22403,
    },
    # EDU-RGT: Constitutional Right
    "EDU-RGT-001": {
        "scope_code": "EDU", "family_code": "RGT",
        "statement": "All persons have a constitutionally protected right to quality public education",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 17936,
    },
    # EDU-CHR: Charter Schools
    "EDU-CHR-001": {
        "scope_code": "EDU", "family_code": "CHR",
        "statement": "Charter schools and private school voucher programs may not be structured to drain resources from the public school system without equivalent accountability and access requirements",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 43210,
    },
    # ── Housing (HOU scope) ───────────────────────────────────────────────────
    "HOU-RGT-001": {
        "scope_code": "HOU", "family_code": "RGT",
        "statement": "Housing policy must prioritize stable, safe, habitable, and affordable living conditions rather than treating shelter alone as sufficient",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37305,
    },
    "HOU-MKT-001": {
        "scope_code": "HOU", "family_code": "MKT",
        "statement": "Housing markets may not be structured so that large investors, private equity, or concentrated ownership outcompete ordinary residents for primary homes at scale",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37355,
    },
    "HOU-SUP-001": {
        "scope_code": "HOU", "family_code": "SUP",
        "statement": "Housing policy must expand the supply of affordable and moderate-cost housing in high-demand areas through zoning and land-use reform that removes unnecessary barriers to building",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37365,
    },
    "HOU-GEN-001": {
        "scope_code": "HOU", "family_code": "GEN",
        "statement": "Housing policy must include proactive anti-gentrification measures to protect existing residents from displacement caused by rising land values, redevelopment, or speculative investment",
        "status": "PROPOSED", "source_name": "branch_branch_political_project_main.txt", "line_number": 18216,
    },
    "HOU-VAC-001": {
        "scope_code": "HOU", "family_code": "VAC",
        "statement": "Purchase of homes in developing or supply-constrained areas for prolonged vacancy or speculative holding should be prohibited or heavily taxed",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37483,
    },
    "HOU-TEN-001": {
        "scope_code": "HOU", "family_code": "TEN",
        "statement": "Tenants must have meaningful protection from retaliatory eviction, rent increases designed to displace, and lease terms that systematically disadvantage renters relative to landlords",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37420,
    },
    "HOU-PUB-001": {
        "scope_code": "HOU", "family_code": "PUB",
        "statement": "Public and social housing must be maintained as a permanent, non-privatizable component of the housing supply in high-cost and underserved communities",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 37390,
    },
    # ── Taxation (TAX scope) ──────────────────────────────────────────────────
    "TAX-SYS-001": {
        "scope_code": "TAX", "family_code": "SYS",
        "statement": "Tax policy must raise revenue fairly, sustain public goods, reduce destabilizing inequality, and prevent extraction of wealth from the social systems that made it possible",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45617,
    },
    "TAX-GEN-001": {
        "scope_code": "TAX", "family_code": "GEN",
        "statement": "Tax systems must be progressive overall and may not shift disproportionate burden onto lower-income or middle-income households",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45625,
    },
    "TAX-WTH-001": {
        "scope_code": "TAX", "family_code": "WTH",
        "statement": "Tax policy must more effectively reach concentrated wealth, capital gains, passive income, and other forms of non-labor wealth accumulation",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45633,
    },
    "TAX-CAP-001": {
        "scope_code": "TAX", "family_code": "CAP",
        "statement": "Income derived from capital, including dividends, capital gains, and passive income, may not be taxed at lower effective rates than income derived from labor",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45793,
    },
    "TAX-HVN-001": {
        "scope_code": "TAX", "family_code": "HVN",
        "statement": "Individuals and corporations may not evade tax obligations by shifting residence, profits, assets, or ownership structures to tax havens without corresponding real economic substance",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45651,
    },
    "TAX-COR-001": {
        "scope_code": "TAX", "family_code": "COR",
        "statement": "Corporate tax rates must be sufficient to prevent profit-shifting, tax avoidance through subsidiary structures, and the effective zero-rating of domestic income through offshore arrangements",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45670,
    },
    "TAX-ENF-001": {
        "scope_code": "TAX", "family_code": "ENF",
        "statement": "The IRS must be funded and staffed to enforce tax law equitably across income levels, with audit rates for high-income and corporate filers not systematically lower than for working-class filers",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 45790,
    },
    # ── Consumer Rights (CON scope) ───────────────────────────────────────────
    "CON-OWN-001": {
        "scope_code": "CON", "family_code": "OWN",
        "statement": "Purchase of a physical product conveys full access to its core functionality and such functionality may not be restricted behind ongoing subscription fees",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39043,
    },
    "CON-OWN-002": {
        "scope_code": "CON", "family_code": "OWN",
        "statement": "Ownership of a product may not be converted into a subscription dependency through software locks, paywalls, or post-sale feature restrictions",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39047,
    },
    "CON-FTR-001": {
        "scope_code": "CON", "family_code": "FTR",
        "statement": "Manufacturers may not artificially disable or withhold functionality that is technically available in hardware solely to create paid upgrade tiers",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39091,
    },
    "CON-TRN-005": {
        "scope_code": "CON", "family_code": "TRN",
        "statement": "Post-sale changes that move previously included features behind paywalls are prohibited",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39121,
    },
    "CON-ENF-001": {
        "scope_code": "CON", "family_code": "ENF",
        "statement": "Violations of ownership-based functionality rules must result in mandatory feature restoration, consumer restitution, and penalties",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39129,
    },
    "CON-ENF-002": {
        "scope_code": "CON", "family_code": "ENF",
        "statement": "Consumers must have a private right of action where product functionality is unlawfully restricted after purchase",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 39133,
    },
    # ── Legislative Reform (LEG scope) ───────────────────────────────────────
    "LEG-DRF-001": {
        "scope_code": "LEG", "family_code": "DRF",
        "statement": "A constitutional amendment or equivalent binding rule should establish drafting standards for all new federal laws",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 35721,
    },
    "LEG-DRF-002": {
        "scope_code": "LEG", "family_code": "DRF",
        "statement": "Every new law must include a plain-language statement of intent, purpose, and context",
        "status": "INCLUDED", "source_name": "branch_branch_political_project_main.txt", "line_number": 17724,
    },
    "LEG-PRO-001": {
        "scope_code": "LEG", "family_code": "PRO",
        "statement": "Legislative procedure may not allow indefinite minority obstruction of legislation through mechanisms such as unlimited debate without resolution",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 47657,
    },
    "LEG-DMJ-001": {
        "scope_code": "LEG", "family_code": "DMJ",
        "statement": "Legislative systems must prevent structural minority rule where a minority of the population can consistently control or block national policy",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 47703,
    },
    "LEG-RPL-001": {
        "scope_code": "LEG", "family_code": "RPL",
        "statement": "Repeal the Alien Enemies Act framework and related emergency-authority structures that enable abuse against non-citizens through vague wartime or insurrection logic",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 35755,
    },
    "LEG-SEN-003": {
        "scope_code": "LEG", "family_code": "SEN",
        "statement": "The Senate may serve as a review, delay, and revision body rather than a co-equal veto chamber for all legislation",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 47639,
    },
    # ── Labor (LAB scope) ─────────────────────────────────────────────────────
    "LAB-RGT-001": {
        "scope_code": "LAB", "family_code": "RGT",
        "statement": "All workers are entitled to fair wages, safe working conditions, reasonable hours, and protection from discrimination and retaliation",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 40921,
    },
    "LAB-PAY-001": {
        "scope_code": "LAB", "family_code": "PAY",
        "statement": "Workers must receive compensation sufficient to meet basic living standards including housing food healthcare and transportation",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 40937,
    },
    "LAB-PAY-002": {
        "scope_code": "LAB", "family_code": "PAY",
        "statement": "The federal minimum wage must be set at a level sufficient for a single full-time worker to meet basic living expenses and must be automatically indexed to inflation",
        "status": "INCLUDED", "source_name": "branch_branch_political_project_main.txt", "line_number": 17972,
    },
    "LAB-LVE-001": {
        "scope_code": "LAB", "family_code": "LVE",
        "statement": "Workers are entitled to paid leave including vacation sick leave parental leave and medical leave",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 40975,
    },
    "LAB-COL-001": {
        "scope_code": "LAB", "family_code": "COL",
        "statement": "Workers have the right to organize unionize and engage in collective bargaining without retaliation or interference",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 41061,
    },
    "LAB-CLS-001": {
        "scope_code": "LAB", "family_code": "CLS",
        "statement": "Worker classification must reflect actual working conditions and may not be manipulated to avoid providing benefits or protections",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 41049,
    },
    "LAB-SUR-001": {
        "scope_code": "LAB", "family_code": "SUR",
        "statement": "Employers may not use invasive surveillance systems that undermine worker privacy dignity or autonomy without clear necessity and proportionality",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 40997,
    },
    "LAB-SFT-001": {
        "scope_code": "LAB", "family_code": "SFT",
        "statement": "All workers have the right to a safe workplace and employers must prevent foreseeable harm without placing cost burdens on workers to enforce their own safety",
        "status": "INCLUDED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 41030,
    },
    # ── Justice: Police Militarization (JUS-MIL scope) ───────────────────────
    "JUS-MIL-001": {
        "scope_code": "JUS", "family_code": "MIL",
        "statement": "Ban police use of automatic weapons, weapons of war, explosives, grenades, and armored vehicles equipped with offensive weapons",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18072,
    },
    "JUS-MIL-002": {
        "scope_code": "JUS", "family_code": "MIL",
        "statement": "Police militarization rules apply to federal agencies including the FBI and similar law enforcement bodies",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18084,
    },
    "JUS-MIL-003": {
        "scope_code": "JUS", "family_code": "MIL",
        "statement": "Where military capabilities are genuinely necessary for a law enforcement operation, the National Guard rather than local police should be deployed under appropriate authorization",
        "status": "PROPOSED", "source_name": "branch_branch_political_project_main.txt", "line_number": 18088,
    },
    # ── Justice: Capital Punishment (JUS-CAP scope) ───────────────────────────
    "JUS-CAP-001": {
        "scope_code": "JUS", "family_code": "CAP",
        "statement": "Eliminate the death penalty except for war crimes and crimes against humanity adjudicated through international processes",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18016,
    },
    # ── Environment: Parks & Urban Green Space (ENV-PKS, ENV-URB) ────────────
    "ENV-PKS-001": {
        "scope_code": "ENV", "family_code": "PKS",
        "statement": "Federal and state governments must protect wildlife habitats and national parks from privatization, extraction, and degradation",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18160,
    },
    "ENV-URB-001": {
        "scope_code": "ENV", "family_code": "URB",
        "statement": "Cities and municipalities must provide and maintain publicly accessible green spaces proportional to population density",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18164,
    },
    # ── Economy: Antitrust (ECO-ANT scope) ───────────────────────────────────
    "ECO-ANT-001": {
        "scope_code": "ECO", "family_code": "ANT",
        "statement": "Strengthen federal antitrust enforcement to prevent and break up market concentration that harms consumers workers or democratic governance",
        "status": "MISSING", "source_name": "branch_branch_political_project_main.txt", "line_number": 18120,
    },
    "ECO-ANT-002": {
        "scope_code": "ECO", "family_code": "ANT",
        "statement": "Require consumer goods to be designed for durability repairability and right to repair rather than planned obsolescence",
        "status": "PROPOSED", "source_name": "branch_branch_political_project_main.txt", "line_number": 18124,
    },
    "ECO-ANT-003": {
        "scope_code": "ECO", "family_code": "ANT",
        "statement": "Algorithmic price coordination between competing market participants is prohibited as a form of per se antitrust violation",
        "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 22990,
    },

    # ── Audit-expansion anchors (all scopes) ────────────────────────────────
    # ADM
    "ADM-ADJ-001": {"scope_code": "ADM", "family_code": "ADJ", "statement": 'Agency adjudication systems must provide clear notice, records access, explanation of decisions, and meaningful appeal rights.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-CAP-001": {"scope_code": "ADM", "family_code": "CAP", "statement": 'Agencies must be structurally insulated from regulated-industry capture, including through conflict-of-interest rules, transparency requirements, and limits on revolving-door influence.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-CIV-001": {"scope_code": "ADM", "family_code": "CIV", "statement": 'Career federal employees in competitive service positions may not be reclassified into at-will employment categories — whether through executive order, administrative action, or regulatory change — in', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-CON-001": {"scope_code": "ADM", "family_code": "CON", "statement": 'Enshrine core federal departments (Labor Education Justice Defense) in the Constitution', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-COO-001": {"scope_code": "ADM", "family_code": "COO", "statement": 'Agencies with overlapping jurisdiction must coordinate enforcement, data sharing, and standards where necessary to prevent fragmentation, gaps, or contradictory obligations.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-ENF-001": {"scope_code": "ADM", "family_code": "ENF", "statement": 'Agencies must have sufficient investigatory powers, subpoena authority, audit authority, and access to records necessary to enforce the law effectively.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-FND-001": {"scope_code": "ADM", "family_code": "FND", "statement": 'Agencies charged with protecting rights, public safety, markets, health, labor, environment, or democratic systems must receive stable and adequate funding sufficient to carry out their lawful mission', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-IND-001": {"scope_code": "ADM", "family_code": "IND", "statement": 'Agencies must be protected from arbitrary defunding, bad-faith understaffing, or politically motivated obstruction intended to disable lawful enforcement.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-MAJ-001": {"scope_code": "ADM", "family_code": "MAJ", "statement": 'Congress must affirmatively exercise its authority to confirm agency power for major regulatory actions — those with vast economic and political significance — through clear statutory language, so tha', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-OVR-001": {"scope_code": "ADM", "family_code": "OVR", "statement": 'Major agencies must have independent internal oversight functions, including inspectors general or equivalent bodies with access to records and investigatory authority.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-PUB-001": {"scope_code": "ADM", "family_code": "PUB", "statement": 'Agency rulemaking and oversight processes must include meaningful public participation, but may not be designed so that organized bad-faith obstruction can paralyze necessary regulation.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-RGT-001": {"scope_code": "ADM", "family_code": "RGT", "statement": 'Agency authority may not be exercised through arbitrary, discriminatory, retaliatory, or legally unsupported action.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-RUL-001": {"scope_code": "ADM", "family_code": "RUL", "statement": 'Agencies must have authority to issue, revise, and clarify rules within their statutory mandate in response to technological, economic, scientific, and social change.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-SCI-001": {"scope_code": "ADM", "family_code": "SCI", "statement": 'Agencies relying on scientific, medical, technical, or economic evidence must maintain scientific-integrity standards that protect findings from political or commercial distortion.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-SYS-001": {"scope_code": "ADM", "family_code": "SYS", "statement": 'Administrative agencies are legitimate constitutional instruments of democratic governance and must exist to implement, enforce, and adapt public-interest law in areas requiring expertise, continuity,', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-TRN-001": {"scope_code": "ADM", "family_code": "TRN", "statement": 'Agencies must publish clear public information about mission, rules, enforcement priorities, audits, major actions, and outcome data.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ADM-WBL-001": {"scope_code": "ADM", "family_code": "WBL", "statement": 'Federal employees who report illegal orders, scientific misconduct, regulatory capture, unlawful political interference with enforcement decisions, or other agency wrongdoing through lawful disclosure', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # CON
    "CON-ALG-001": {"scope_code": "CON", "family_code": "ALG", "statement": 'Pricing algorithms, personalized offer systems, and consumer targeting tools may not produce discriminatory outcomes based on protected characteristics&#x2014;including race, color, national origin, s', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-CNS-001": {"scope_code": "CON", "family_code": "CNS", "statement": 'Products may not require proprietary consumables or subscription-based supply systems where compatible alternatives are feasible.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-CRD-001": {"scope_code": "CON", "family_code": "CRD", "statement": 'Credit reporting agencies must maintain accurate consumer files, must conduct genuine investigations of consumer disputes rather than cursory procedural reviews, and must promptly correct verified err', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-DBR-001": {"scope_code": "CON", "family_code": "DBR", "statement": 'Commercial data brokers that compile, sell, or share consumer profiles must register with a federal authority, disclose the categories of data they collect and the sources from which they collect it, ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-DRK-001": {"scope_code": "CON", "family_code": "DRK", "statement": 'Interface designs that deliberately manipulate consumer choices through misdirection, false urgency, hidden options, confusing visual hierarchy, or other deceptive techniques are prohibited as unfair ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-FEE-001": {"scope_code": "CON", "family_code": "FEE", "statement": 'Hidden fees, junk fees, drip pricing, and post-selection fee inflation are prohibited.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-GEN-001": {"scope_code": "CON", "family_code": "GEN", "statement": 'Consumer protection law must prohibit deceptive, coercive, exploitative, or structurally unfair business practices even where no single transaction appears individually extreme.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-QLT-001": {"scope_code": "CON", "family_code": "QLT", "statement": 'Consumer products must meet minimum durability, safety, and quality standards appropriate to their category and expected use.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-SUB-001": {"scope_code": "CON", "family_code": "SUB", "statement": 'Subscription models may not be structured to replace ownership where ownership remains feasible and the primary purpose is recurring extraction rather than genuine service delivery.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "CON-WAR-001": {"scope_code": "CON", "family_code": "WAR", "statement": 'Warranty systems must be understandable, fair, and enforceable and may not rely on procedural traps or vague exclusions to avoid responsibility.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # COR
    "COR-AGF-001": {"scope_code": "COR", "family_code": "AGF", "statement": 'Concentration in agricultural processing&#x2014;including meatpacking, poultry processing, grain trading, and food distribution&#x2014;must be subject to active antitrust enforcement, including review', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-ALG-001": {"scope_code": "COR", "family_code": "ALG", "statement": 'Algorithmic systems may not be used to coordinate prices, rents, fees, or other market behavior in ways that function as collusion or anti-competitive alignment.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-ANT-001": {"scope_code": "COR", "family_code": "ANT", "statement": 'Anti-monopoly law must be strengthened to prevent excessive concentration in essential consumer, infrastructure, technology, healthcare, housing, food, and communications markets.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-ASF-001": {"scope_code": "COR", "family_code": "ASF", "statement": 'The federal government and any state or local law enforcement agency receiving federal equitable sharing funds may not civilly forfeit property without first obtaining a criminal conviction of the pro', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-AUD-001": {"scope_code": "COR", "family_code": "AUD", "statement": 'Corporate audits must follow standardized formats and regulatory frameworks similar to tax filings.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-CAP-001": {"scope_code": "COR", "family_code": "CAP", "statement": 'Industry may not dominate the bodies that regulate, score, audit, or oversee its own conduct.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-CON-001": {"scope_code": "COR", "family_code": "CON", "statement": 'Concentration of economic power that undermines competition, public access, democratic accountability, or system integrity is prohibited and must be prevented or corrected.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-EMO-001": {"scope_code": "COR", "family_code": "EMO", "statement": 'Congress must enact a statute establishing a clear cause of action, enforcement mechanism, and standing rules for emoluments clause violations (Art. I, § 9, cl. 8 and Art. II, § 1, cl. 7). The statute', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-ENF-001": {"scope_code": "COR", "family_code": "ENF", "statement": 'Antitrust and consumer-protection enforcement agencies must have sufficient staffing, technical expertise, funding, and independence to police concentrated and technologically complex markets.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-ETH-001": {"scope_code": "COR", "family_code": "ETH", "statement": 'Ban lobbyists from governing industries', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-FAR-001": {"scope_code": "COR", "family_code": "FAR", "statement": 'The Foreign Agents Registration Act (22 U.S.C. §§ 611–621) must be strengthened with mandatory criminal referral for willful non-registration, expanded DOJ enforcement capacity with dedicated investig', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-FIN-001": {"scope_code": "COR", "family_code": "FIN", "statement": 'Ban corporate political donations', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-HAT-001": {"scope_code": "COR", "family_code": "HAT", "statement": 'Hatch Act violations (5 U.S.C. §§ 7321–7326) by senior political appointees and Senate-confirmed officials must carry criminal penalties and mandatory removal from office upon a second violation. The ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-INT-001": {"scope_code": "COR", "family_code": "INT", "statement": 'The United States must fully implement all obligations under the United Nations Convention Against Corruption (UNCAC), which the U.S. ratified in 2006. This requires: completing the UNCAC self-assessm', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-LAW-001": {"scope_code": "COR", "family_code": "LAW", "statement": 'Corporate officers, executives, and responsible individuals may be held criminally liable for violations, including negligence and failure of oversight.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-MKT-001": {"scope_code": "COR", "family_code": "MKT", "statement": 'Markets must serve the public interest and may not be structured primarily to maximize extraction, lock-in, or concentration of private power.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-MPY-001": {"scope_code": "COR", "family_code": "MPY", "statement": 'Concentration of employer power in geographic or occupational labor markets that demonstrably suppresses wages, limits job choices, or prevents effective collective bargaining constitutes an antitrust', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-NMD-001": {"scope_code": "COR", "family_code": "NMD", "statement": 'Further consolidation of local newspaper, broadcast, and digital news media ownership must be prohibited or restricted by FCC and DOJ to prevent any entity from achieving dominant control over the loc', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-OWN-001": {"scope_code": "COR", "family_code": "OWN", "statement": 'The beneficial ownership reporting framework established by the Corporate Transparency Act (31 U.S.C. § 5336) must be extended to require disclosure in a publicly searchable database, not merely a Fin', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-PEQ-001": {"scope_code": "COR", "family_code": "PEQ", "statement": 'Private-equity and other highly leveraged ownership models may not be used to strip assets, degrade quality, extract short-term gains, and leave consumers workers or communities with the harm.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-PIS-001": {"scope_code": "COR", "family_code": "PIS", "statement": 'Firms operating in essential sectors including housing, healthcare, food, communications, utilities, education technology, and transportation are subject to heightened public-interest obligations.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "COR-TRN-001": {"scope_code": "COR", "family_code": "TRN", "statement": 'Dominant firms in essential sectors must disclose key metrics related to concentration, support windows, warranty denial rates, repair restrictions, and pricing structure.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # EDU
    "EDU-BND-001": {"scope_code": "EDU", "family_code": "BND", "statement": 'Every K–12 student must have reliable broadband internet access at home and a suitable device for schoolwork; school districts must identify and close connectivity gaps with the support of federal fun', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "EDU-DIS-001": {"scope_code": "EDU", "family_code": "DIS", "statement": 'Schools must transition away from zero-tolerance, punitive discipline policies toward restorative justice approaches that repair harm and keep students in school; schools may not impose exclusionary d', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "EDU-LIB-001": {"scope_code": "EDU", "family_code": "LIB", "statement": 'K–12 teachers must be protected from disciplinary action, termination, or legal jeopardy for teaching factual, peer-reviewed content in history, science, civics, or social studies, including topics th', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "EDU-STD-001": {"scope_code": "EDU", "family_code": "STD", "statement": 'EDU|STD|Education standards must include protections against political or ideological indoctrination|MISSING', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # ENV
    "ENV-AI-001": {"scope_code": "ENV", "family_code": "AI", "statement": 'AI used in infrastructure, energy, water, transport, or environmental management must be constrained by public-safety, resilience, and environmental-protection obligations above efficiency or profit g', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-AUD-001": {"scope_code": "ENV", "family_code": "AUD", "statement": 'Corporations must file standardized environmental audits on a quarterly basis.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-BIO-001": {"scope_code": "ENV", "family_code": "BIO", "statement": 'Protect and restore migratory patterns for animals through infrastructure and land-use planning', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-CLI-001": {"scope_code": "ENV", "family_code": "CLI", "statement": 'All major federal infrastructure programs and agencies responsible for transportation, energy, water, public health, and housing must develop and maintain current climate adaptation plans that assess ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-CLN-001": {"scope_code": "ENV", "family_code": "CLN", "statement": 'Environmental policy must include active cleanup and remediation of existing pollution, waste accumulation, and ecological damage rather than focusing only on prevention of future harm.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-COR-001": {"scope_code": "ENV", "family_code": "COR", "statement": 'Establish general anti-greenwashing standards prohibiting false misleading or selectively incomplete environmental claims by companies organizations or public entities', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-CPX-001": {"scope_code": "ENV", "family_code": "CPX", "statement": 'The United States must implement a carbon pricing mechanism — whether a direct carbon fee, a cap-and-trade system, or equivalent — that requires all significant sources of greenhouse gas emissions to ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-DES-001": {"scope_code": "ENV", "family_code": "DES", "statement": 'Products and packaging must be designed for recyclability, reuse, or safe degradation, minimizing mixed materials and non-recoverable components.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-ENF-001": {"scope_code": "ENV", "family_code": "ENF", "statement": 'Entities responsible for environmental contamination through waste leakage or mismanagement must be held liable for cleanup, remediation, and damages.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-EPR-001": {"scope_code": "ENV", "family_code": "EPR", "statement": 'Producers are responsible for the full lifecycle of their products, including collection, recycling, disposal, and environmental impact mitigation.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-ESC-001": {"scope_code": "ENV", "family_code": "ESC", "statement": 'Waste systems must be designed to prevent materials from escaping into natural environments, including waterways, oceans, and ecosystems.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-IND-001": {"scope_code": "ENV", "family_code": "IND", "statement": 'Industrial processes must minimize waste output and prevent release of materials into surrounding ecosystems.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-INF-001": {"scope_code": "ENV", "family_code": "INF", "statement": 'Waste management infrastructure must prevent leakage into the environment through proper containment, transport, and processing systems.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-JUS-001": {"scope_code": "ENV", "family_code": "JUS", "statement": 'Environmental permitting processes must include a cumulative environmental burden analysis for proposed facilities; new permits for industrial polluters, hazardous waste facilities, and other signific', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-PKG-001": {"scope_code": "ENV", "family_code": "PKG", "statement": 'Excessive packaging and non-essential materials must be reduced through regulation and design standards.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-PLS-001": {"scope_code": "ENV", "family_code": "PLS", "statement": 'Production and use of single-use plastics and non-essential disposable materials should be reduced, restricted, or phased out where viable alternatives exist.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-POL-001": {"scope_code": "ENV", "family_code": "POL", "statement": 'Establish stronger national standards to reduce and monitor noise pollution', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-REC-001": {"scope_code": "ENV", "family_code": "REC", "statement": 'Recycling systems must be expanded, standardized, and modernized to handle current material volumes and complexity.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-REG-001": {"scope_code": "ENV", "family_code": "REG", "statement": 'The Environmental Protection Agency must be constitutionally established, funded, and empowered to enforce environmental protections.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-SPC-001": {"scope_code": "ENV", "family_code": "SPC", "statement": 'Establish rules for orbital sanitation and removal or mitigation of space junk', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-SYS-001": {"scope_code": "ENV", "family_code": "SYS", "statement": 'Waste reduction, recyclability, repairability, and durability requirements must be integrated across consumer protection, manufacturing, housing, and infrastructure policy.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-TRN-001": {"scope_code": "ENV", "family_code": "TRN", "statement": 'Governments must track and publish data on waste generation, recycling rates, environmental leakage, and material flows.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-WST-001": {"scope_code": "ENV", "family_code": "WST", "statement": 'Waste generation must be minimized at the source, and materials must be managed to prevent environmental release, accumulation, and long-term ecological harm.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "ENV-WTR-001": {"scope_code": "ENV", "family_code": "WTR", "statement": 'Access to safe, affordable drinking water is a fundamental right; federal law must establish enforceable minimum standards for water quality and access, require state and federal agencies to prioritiz', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # HLT
    "HLT-AI-001": {"scope_code": "HLT", "family_code": "AI", "statement": 'AI systems in healthcare must be treated as high-risk systems requiring strict standards for safety efficacy accountability and patient protection', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-APL-001": {"scope_code": "HLT", "family_code": "APL", "statement": 'Patients and providers must have access to fast meaningful and independent appeal processes for adverse coverage or service decisions', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-CLM-001": {"scope_code": "HLT", "family_code": "CLM", "statement": 'Coverage systems must include treatment for climate-related health conditions — heat illness, expanded-range vector-borne diseases, air quality-driven respiratory conditions, and mental health impacts', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-COV-001": {"scope_code": "HLT", "family_code": "COV", "statement": 'Ban tiered healthcare coverage', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-CRN-001": {"scope_code": "HLT", "family_code": "CRN", "statement": 'Coverage systems must classify post-acute sequelae of infectious disease — including Long COVID and post-viral syndromes — as chronic conditions requiring ongoing specialist care, occupational and phy', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-CST-001": {"scope_code": "HLT", "family_code": "CST", "statement": 'Deductibles copays and out-of-pocket cost structures must not make covered care practically inaccessible', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-DNT-001": {"scope_code": "HLT", "family_code": "DNT", "statement": 'Coverage systems must include comprehensive dental care — preventive, restorative, periodontal, and oral surgery services — as part of the mandatory floor of medically necessary care; dental care may ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-EMP-001": {"scope_code": "HLT", "family_code": "EMP", "statement": 'Employers may not satisfy healthcare obligations by offering only high-deductible plans that shift unreasonable cost burden onto workers', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-JUS-001": {"scope_code": "HLT", "family_code": "JUS", "statement": 'Every person in state or federal custody has a constitutional right to healthcare meeting community standards; correctional facilities must provide timely access to medical, dental, mental health, and', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-MAT-001": {"scope_code": "HLT", "family_code": "MAT", "statement": 'Every state must maintain a maternal mortality review committee with authority to investigate all pregnancy-related deaths; results must be reported publicly in race-disaggregated form and used to dev', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-NET-001": {"scope_code": "HLT", "family_code": "NET", "statement": 'Health plans must maintain adequate networks for all covered services including specialty care mental healthcare emergency care and chronic-condition management', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-OVR-001": {"scope_code": "HLT", "family_code": "OVR", "statement": 'Coverage entities must publicly report denial rates appeal outcomes prior authorization burden network adequacy failures and major access complaints in standardized formats', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-PAU-001": {"scope_code": "HLT", "family_code": "PAU", "statement": 'Prior authorization requirements must be strictly limited to categories with clear evidence of necessity and may not be used indiscriminately across routine care', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-RSR-001": {"scope_code": "HLT", "family_code": "RSR", "statement": 'Public healthcare and research policy must increase funding for neglected conditions medications and treatment gaps that lack commercial incentives but have significant public-health impact', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-RX-001": {"scope_code": "HLT", "family_code": "RX", "statement": 'Drug coverage systems must include broad access to medically necessary prescriptions and may not use formularies as hidden denial systems', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HLT-TRN-001": {"scope_code": "HLT", "family_code": "TRN", "statement": 'Until universal single-payer healthcare is implemented all healthcare coverage systems must be regulated to protect patients from denial delay fragmentation and extractive practices', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # HOU
    "HOU-ALT-001": {"scope_code": "HOU", "family_code": "ALT", "statement": 'Housing policy should promote nonprofit housing, cooperative housing, resident-owned models, and community land trusts as durable anti-extraction alternatives.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-BLD-001": {"scope_code": "HOU", "family_code": "BLD", "statement": 'Housing policy should expand investment in sustainable, renewable, environmentally responsible, and durable building materials and construction methods.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-CLT-001": {"scope_code": "HOU", "family_code": "CLT", "statement": 'Government must recognize community land trusts and shared-equity homeownership models as a legitimate, permanent mechanism for preserving long-term housing affordability and must provide stable publi', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-EVI-001": {"scope_code": "HOU", "family_code": "EVI", "statement": 'Evictions may only occur through a transparent legal process with due process, adequate notice, and opportunity to respond.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-EXT-001": {"scope_code": "HOU", "family_code": "EXT", "statement": 'Housing may not be treated primarily as an extraction vehicle where ownership, management, or financing structures predictably undermine affordability, maintenance, or stability.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-FIN-001": {"scope_code": "HOU", "family_code": "FIN", "statement": 'Mortgage lending must prohibit predatory terms, deceptive structures, and risk-shifting practices that disproportionately harm borrowers.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-HAB-001": {"scope_code": "HOU", "family_code": "HAB", "statement": 'All housing receiving public subsidy, public voucher support, or public contract support must meet strong habitability, safety, sanitation, accessibility, and maintenance standards.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-HML-001": {"scope_code": "HOU", "family_code": "HML", "statement": 'Housing policy must adopt a Housing First approach that prioritizes stable housing as the foundation for addressing homelessness.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-HOA-001": {"scope_code": "HOU", "family_code": "HOA", "statement": 'Homeowner associations must be subject to strong limits on abuse, selective enforcement, retaliatory fines, and arbitrary restrictions on residents.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-INS-001": {"scope_code": "HOU", "family_code": "INS", "statement": 'Homeownership affordability must account for insurance costs, which must be regulated to remain accessible and non-exploitative.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-IZN-001": {"scope_code": "HOU", "family_code": "IZN", "statement": 'Residential developments above a defined unit threshold must include a specified percentage of permanently affordable units, or must make an in-lieu payment to an affordable housing fund used exclusiv', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-LND-001": {"scope_code": "HOU", "family_code": "LND", "statement": 'Public land should be prioritized for development of affordable and social housing rather than sold for short-term revenue maximization.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-MHO-001": {"scope_code": "HOU", "family_code": "MHO", "statement": 'Residents of mobile home parks and manufactured housing communities must receive adequate notice, right of first refusal or purchase opportunity, and relocation assistance when their park is sold, red', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-OVR-001": {"scope_code": "HOU", "family_code": "OVR", "statement": 'Federal, state, and local governments must collect and publish standardized data on affordability, vacancy, code violations, ownership concentration, investor acquisition, and habitability enforcement', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-OWN-001": {"scope_code": "HOU", "family_code": "OWN", "statement": 'Federal and state policy must address the long-term rise in housing purchase costs relative to incomes and inflation through supply reform, anti-speculation measures, and affordability-focused ownersh', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-PRS-001": {"scope_code": "HOU", "family_code": "PRS", "statement": 'Housing policy must preserve existing affordable housing stock and prevent loss of livable low-cost units through neglect, demolition, speculative conversion, or predatory redevelopment.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-QLT-001": {"scope_code": "HOU", "family_code": "QLT", "statement": 'Residential construction must meet stronger quality and durability standards and may not rely on systematically cheap, short-lived materials or methods that undermine long-term habitability.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-REG-001": {"scope_code": "HOU", "family_code": "REG", "statement": 'Housing regulations must prioritize safety, durability, habitability, and long-term livability over short-term cost reduction.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-RNT-001": {"scope_code": "HOU", "family_code": "RNT", "statement": 'Rent increases must be subject to reasonable limits or stabilization mechanisms in markets experiencing rapid or destabilizing price growth.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-RPR-001": {"scope_code": "HOU", "family_code": "RPR", "statement": 'Residents and property owners have the right to repair, maintain, and modify their homes without unnecessary restriction, provided safety and structural integrity are preserved.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-SOI-001": {"scope_code": "HOU", "family_code": "SOI", "statement": 'Landlords, property managers, and rental listing platforms may not refuse to rent to, discriminate against, or impose different terms on tenants based on the lawful source of their income, including h', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-SUB-001": {"scope_code": "HOU", "family_code": "SUB", "statement": 'Housing subsidies may not be structured in ways that increase purchasing power without increasing housing supply or affordability.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-SYS-001": {"scope_code": "HOU", "family_code": "SYS", "statement": 'Federal and state housing policy must identify and address the cumulative legal, financial, tax, zoning, ownership, and market structures that caused housing costs to outpace general inflation and inc', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "HOU-TAX-001": {"scope_code": "HOU", "family_code": "TAX", "statement": 'Property tax systems must protect long-term owner-occupants from displacement due to rising assessed values.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # IMM
    "IMM-ACC-001": {"scope_code": "IMM", "family_code": "ACC", "statement": 'Immigration status may affect specific program eligibility but may not be used to deny emergency care basic education or other core rights-protective systems guaranteed under law', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-ADM-001": {"scope_code": "IMM", "family_code": "ADM", "statement": 'Immigration systems must be funded and staffed to reduce backlogs and delays that create injustice through prolonged uncertainty', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-ASY-001": {"scope_code": "IMM", "family_code": "ASY", "statement": 'People seeking asylum or humanitarian protection must have meaningful access to fair screening full adjudication and protection from summary rejection where credible claims exist', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-BRD-001": {"scope_code": "IMM", "family_code": "BRD", "statement": 'Border governance must be lawful humane and accountable and may not rely on indiscriminate force or degrading treatment', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-CIT-001": {"scope_code": "IMM", "family_code": "CIT", "statement": 'Pathways to citizenship should be clear affordable and realistically attainable for people who meet established criteria', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-CLM-001": {"scope_code": "IMM", "family_code": "CLM", "statement": 'The United States must establish a humanitarian visa category for individuals displaced by the direct effects of climate change — including sea-level rise, desertification, severe weather events, and ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-CON-001": {"scope_code": "IMM", "family_code": "CON", "statement": 'Private contractors involved in immigration processing transportation surveillance case management or service delivery must be subject to full public-law accountability standards', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-CRT-001": {"scope_code": "IMM", "family_code": "CRT", "statement": 'Immigration adjudication systems must be structured for independence fairness and competence and may not function as rubber-stamp enforcement mechanisms', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-DAT-001": {"scope_code": "IMM", "family_code": "DAT", "statement": 'Immigration systems may not use broad data surveillance or commercially acquired data to bypass due process or create shadow enforcement profiles', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-DET-001": {"scope_code": "IMM", "family_code": "DET", "statement": 'Immigration detention must be strictly limited and may not be used as a default administrative convenience or deterrence mechanism', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-DOC-001": {"scope_code": "IMM", "family_code": "DOC", "statement": 'Immigration and travel document systems must respect updated legal identity information and may not impose contradictory marker rules across agencies', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-DUE-001": {"scope_code": "IMM", "family_code": "DUE", "statement": 'People in immigration proceedings must have meaningful due process including notice interpretation access to records and opportunity to be heard', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-ENF-001": {"scope_code": "IMM", "family_code": "ENF", "statement": 'Immigration and Customs Enforcement in its current form should be abolished and replaced with narrower rights-constrained and transparently governed structures that cannot reproduce its current abuse ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-FAM-001": {"scope_code": "IMM", "family_code": "FAM", "statement": 'Family separation in immigration enforcement is prohibited except under narrowly defined and reviewable conditions involving immediate safety necessity', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-INT-001": {"scope_code": "IMM", "family_code": "INT", "statement": 'Immigration policy should support stable local integration through language access community support lawful work access and predictable process rather than prolonged precarity', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-LAB-001": {"scope_code": "IMM", "family_code": "LAB", "statement": 'Immigration status may not be used by employers to suppress wages retaliate against workers or evade labor law', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-OVR-001": {"scope_code": "IMM", "family_code": "OVR", "statement": 'Immigration agencies and detention systems must be subject to strong independent oversight with access to facilities records and decision patterns', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-REF-001": {"scope_code": "IMM", "family_code": "REF", "statement": 'The United States should maintain a robust refugee resettlement system grounded in humanitarian responsibility due process and long-term integration support', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-REM-001": {"scope_code": "IMM", "family_code": "REM", "statement": 'People may not be deported to countries that are not their country of origin nationality lawful residency or another country where lawful admission and safety are clearly established', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-RGT-001": {"scope_code": "IMM", "family_code": "RGT", "statement": 'Immigration policy must respect human rights due process family integrity and equal dignity while maintaining lawful and orderly systems', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-SRV-001": {"scope_code": "IMM", "family_code": "SRV", "statement": 'People within United States jurisdiction must have access to emergency healthcare and medically necessary stabilization regardless of immigration status', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-STS-001": {"scope_code": "IMM", "family_code": "STS", "statement": 'Immigration policy should provide realistic lawful pathways to status for long-term residents with community ties rather than preserving permanent precarity', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-SYS-001": {"scope_code": "IMM", "family_code": "SYS", "statement": 'Lawful immigration pathways should be designed to reduce unnecessary irregularity black-market dependence and exploitative limbo by making legal compliance realistically attainable', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-TRF-001": {"scope_code": "IMM", "family_code": "TRF", "statement": 'Immigration systems must include strong protections for survivors of trafficking coercion labor exploitation and abuse and may not force them to choose between safety and immigration jeopardy', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "IMM-VIS-001": {"scope_code": "IMM", "family_code": "VIS", "statement": 'Visa categories and lawful-entry pathways should be modernized to reduce arbitrary complexity mismatch with real-world needs and unnecessary precarity', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # INF
    "INF-AFD-001": {"scope_code": "INF", "family_code": "AFD", "statement": 'Federal law must establish affordability standards and subsidy mechanisms ensuring that all households can access minimum adequate levels of internet service, electricity, and clean water regardless o', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "INF-EQJ-001": {"scope_code": "INF", "family_code": "EQJ", "statement": 'Major infrastructure siting decisions — including highways, power plants, transmission lines, pipelines, data centers, waste facilities, and industrial operations receiving federal permits or funding ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "INF-LBR-001": {"scope_code": "INF", "family_code": "LBR", "statement": 'All infrastructure projects receiving federal funding, financing, loan guarantees, or tax benefits must pay prevailing wages as determined under the Davis-Bacon Act, and must ensure that workers engag', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # JUD
    "JUD-ETH-001": {"scope_code": "JUD", "family_code": "ETH", "statement": 'Supreme Court term limits', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-INT-001": {"scope_code": "JUD", "family_code": "INT", "statement": 'Require intent-based interpretation', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-LGO-001": {"scope_code": "JUD", "family_code": "LGO", "statement": 'Congress may reinstate a federal statute invalidated by the Supreme Court on constitutional grounds by passing it again with a two-thirds majority in both chambers within ten years of the decision; th', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-NOM-001": {"scope_code": "JUD", "family_code": "NOM", "statement": 'The Senate must hold confirmation hearings and vote on judicial nominees within 90 days; failure to act results in automatic confirmation.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-OVR-001": {"scope_code": "JUD", "family_code": "OVR", "statement": 'Judicial oversight mechanisms', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-REC-001": {"scope_code": "JUD", "family_code": "REC", "statement": 'Strong recusal standards', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-SHD-001": {"scope_code": "JUD", "family_code": "SHD", "statement": 'Emergency or shadow docket orders issued without full briefing and argument must require a supermajority of the court and must include written justification.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-SIZ-001": {"scope_code": "JUD", "family_code": "SIZ", "statement": 'Supreme Court size must be set by constitutional amendment or supermajority statute to prevent partisan court-packing by simple majority.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "JUD-VEN-001": {"scope_code": "JUD", "family_code": "VEN", "statement": 'Prevent judge and venue shopping', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # LAB
    "LAB-AI-001": {"scope_code": "LAB", "family_code": "AI", "statement": 'AI systems used in employment must preserve logs, scoring logic, and decision records sufficient for worker challenge, audit, and enforcement.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-AUT-001": {"scope_code": "LAB", "family_code": "AUT", "statement": 'Employers must provide meaningful notice, consultation, and transition planning before major automation or restructuring that materially affects employment.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-BEN-001": {"scope_code": "LAB", "family_code": "BEN", "statement": 'Workers must have reliable access to core benefits including healthcare leave retirement protection unemployment protection and disability protection regardless of job type or employer structure.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-CBA-001": {"scope_code": "LAB", "family_code": "CBA", "statement": 'Employers must engage in good-faith bargaining following union recognition and may not delay or avoid reaching an initial agreement.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-CLM-001": {"scope_code": "LAB", "family_code": "CLM", "statement": 'All workers have an enforceable right to protection from dangerous heat conditions, including mandatory rest periods, access to cool water and shade, acclimatization protocols, and emergency response ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-COE-001": {"scope_code": "LAB", "family_code": "COE", "statement": 'Employers may not use economic dependency, scheduling control, or benefit withholding to coerce workers into accepting unfair conditions.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-DOM-001": {"scope_code": "LAB", "family_code": "DOM", "statement": 'Domestic workers&#x2014;including nannies, housekeepers, home health aides, and household employees&#x2014;must receive full coverage under the National Labor Relations Act, Fair Labor Standards Act, ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-ENF-001": {"scope_code": "LAB", "family_code": "ENF", "statement": 'Labor law violations must be subject to meaningful enforcement, including penalties, restitution, and corrective action.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-GIG-001": {"scope_code": "LAB", "family_code": "GIG", "statement": 'Workers performing labor through platforms or digital systems are entitled to full labor protections regardless of classification structure.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-GOV-001": {"scope_code": "LAB", "family_code": "GOV", "statement": 'Workers should have meaningful representation in firm governance where firm decisions materially affect wages, safety, scheduling, surveillance, automation, or long-term employment stability.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-HRS-001": {"scope_code": "LAB", "family_code": "HRS", "statement": 'Work schedules must be predictable, reasonable, and not subject to arbitrary or last-minute changes without compensation.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-NCP-001": {"scope_code": "LAB", "family_code": "NCP", "statement": 'Non-compete agreements must be banned or strictly limited for workers below senior executive level, as approximately 30 million workers&#x2014;roughly one in five&#x2014;are subject to non-compete agr', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-OWN-001": {"scope_code": "LAB", "family_code": "OWN", "statement": 'Labor policy should promote worker ownership, cooperative enterprise models, employee equity participation, and shared-governance systems.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-PBN-001": {"scope_code": "LAB", "family_code": "PBN", "statement": 'Social insurance systems and workplace benefits&#x2014;including paid leave, retirement savings, healthcare contributions, and training credits&#x2014;must be designed to be portable across employers ', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-PLT-001": {"scope_code": "LAB", "family_code": "PLT", "statement": 'Workers managed by algorithms, platforms, or automated systems must have the right to collectively bargain over pay, conditions, and algorithmic governance.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-PRL-001": {"scope_code": "LAB", "family_code": "PRL", "statement": 'Incarcerated workers performing labor may not be compelled to work without compensation bearing a reasonable relationship to the value of their labor, and the Thirteenth Amendment exception for punish', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-RET-001": {"scope_code": "LAB", "family_code": "RET", "statement": 'Workers must have access to retirement-saving systems that are portable, transparent, and not dependent on continuous employment with a single employer.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-SCH-001": {"scope_code": "LAB", "family_code": "SCH", "statement": 'Workers in retail, food service, hospitality, and other industries with variable scheduling must receive their work schedules at least 14 days in advance to allow planning for childcare, transportatio', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-SYS-001": {"scope_code": "LAB", "family_code": "SYS", "statement": 'Labor systems must ensure fair compensation, safe conditions, dignity, autonomy, and protection from exploitation.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-TRN-001": {"scope_code": "LAB", "family_code": "TRN", "statement": 'Employers must disclose key employment conditions, including wages, schedules, benefits, and surveillance practices.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-UNN-001": {"scope_code": "LAB", "family_code": "UNN", "statement": 'Union formation processes must be timely, transparent, and free from employer interference or delay tactics.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "LAB-WRK-001": {"scope_code": "LAB", "family_code": "WRK", "statement": 'Establish a standard 4-day 32-hour work week without reduction in pay', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # MED
    "MED-NET-001": {"scope_code": "MED", "family_code": "NET", "statement": 'Internet service providers must treat all legal internet traffic equally without throttling, blocking, prioritizing, or charging differential rates based on content, source, destination, or service ty', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "MED-OWN-001": {"scope_code": "MED", "family_code": "OWN", "statement": 'No single entity may own more than one daily newspaper, one television broadcast station, and one radio station in the same local market; the FCC must apply and enforce structural media ownership limi', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "MED-PLT-001": {"scope_code": "MED", "family_code": "PLT", "statement": 'Digital platforms with significant user reach must publish clear, specific, and consistently applied content moderation policies; must provide users with written reasons for content removal or account', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "MED-PUB-001": {"scope_code": "MED", "family_code": "PUB", "statement": 'Federal funding for public media — including the Corporation for Public Broadcasting, NPR, PBS, and their affiliates — must be guaranteed through multi-year appropriations or a dedicated funding strea', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # TAX
    "TAX-ADM-001": {"scope_code": "TAX", "family_code": "ADM", "statement": 'Tax administration systems should use automation, data matching, and modern technology to simplify filing for ordinary taxpayers and improve enforcement against complex evasion.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-AI-001": {"scope_code": "TAX", "family_code": "AI", "statement": 'Economic value generated through automation and AI must contribute to public systems similarly to human labor and traditional economic activity.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-BEP-001": {"scope_code": "TAX", "family_code": "BEP", "statement": 'Corporate income must be taxed based on real economic activity, including sales, workforce, and physical presence, rather than legal entity location alone.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-CDR-001": {"scope_code": "TAX", "family_code": "CDR", "statement": 'Candidates for President, Vice President, and federal elected offices must publicly disclose their federal income tax returns for a minimum of five recent years as a condition of ballot access or conf', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-DED-001": {"scope_code": "TAX", "family_code": "DED", "statement": 'Deductions must be directly tied to legitimate business activity and may not be used to artificially reduce taxable income through unrelated or inflated expenses.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-DMJ-001": {"scope_code": "TAX", "family_code": "DMJ", "statement": 'Tax policy must be written and administered so that no class of wealth holder, corporation, or politically connected actor can routinely buy more favorable effective treatment than ordinary people.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-ENV-001": {"scope_code": "TAX", "family_code": "ENV", "statement": 'Environmental tax policy must internalize environmental harms that are currently externalized onto the public, future generations, and ecosystems.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-EST-001": {"scope_code": "TAX", "family_code": "EST", "statement": 'Large intergenerational wealth transfers must be taxed to prevent permanent economic stratification and dynastic concentration of power.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-EXT-001": {"scope_code": "TAX", "family_code": "EXT", "statement": 'Stock buybacks and similar financial extraction mechanisms may be subject to taxation or limitation where they do not contribute to productive investment.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-FTT-001": {"scope_code": "TAX", "family_code": "FTT", "statement": 'Financial transactions in stocks, bonds, and derivatives markets may be subject to a small transaction tax that discourages high-frequency speculation while leaving long-term investment largely unaffe', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-GOV-001": {"scope_code": "TAX", "family_code": "GOV", "statement": 'Tax policy and enforcement agencies must be protected from regulatory capture, political interference, and deliberate underfunding.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-INC-001": {"scope_code": "TAX", "family_code": "INC", "statement": 'Tax incentives must be tied to measurable public-good outcomes such as affordability, labor standards, environmental performance, durable investment, or public benefit.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-INT-001": {"scope_code": "TAX", "family_code": "INT", "statement": 'The United States should pursue international agreements and coordinated enforcement against tax havens, secrecy jurisdictions, and cross-border tax evasion.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-LOP-001": {"scope_code": "TAX", "family_code": "LOP", "statement": 'Tax provisions that primarily enable avoidance, deferral, or artificial reduction of tax liability without corresponding public benefit must be eliminated.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-LVT-001": {"scope_code": "TAX", "family_code": "LVT", "statement": 'Tax policy may employ land value taxation to capture the unearned appreciation of land created by public investment, community development, and natural scarcity rather than by the landowner&#x2019;s e', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TAX-TRN-001": {"scope_code": "TAX", "family_code": "TRN", "statement": 'Beneficial ownership of companies, trusts, major asset-holding structures, and tax-relevant entities must be transparent to regulators and enforceable through reporting rules.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    # TEC
    "TEC-AGE-001": {"scope_code": "TEC", "family_code": "AGE", "statement": 'Prohibit mandatory identity-based age verification systems that require government ID biometric data or persistent tracking to access lawful content', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-AI-001": {"scope_code": "TEC", "family_code": "AI", "statement": 'High-risk AI systems must be subject to heightened governance review before deployment', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-ALG-001": {"scope_code": "TEC", "family_code": "ALG", "statement": 'People must be told when AI or algorithmic systems materially influence ranking eligibility triage moderation or access decisions', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-AUD-001": {"scope_code": "TEC", "family_code": "AUD", "statement": 'Covered AI systems must support independent auditing for safety bias reliability and misuse', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-AUT-001": {"scope_code": "TEC", "family_code": "AUT", "statement": 'High-risk autonomous systems must not be deployed where failure could cause loss of liberty bodily harm or deprivation of rights without strict safeguards', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-BIO-001": {"scope_code": "TEC", "family_code": "BIO", "statement": 'Ban mass facial recognition in public spaces for general law-enforcement or administrative use', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-CHD-001": {"scope_code": "TEC", "family_code": "CHD", "statement": 'AI systems directed at children or likely to be used by minors are subject to heightened safety, privacy, manipulation, and developmental protections.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-DAT-001": {"scope_code": "TEC", "family_code": "DAT", "statement": 'Prohibit cross-agency fusion of surveillance datasets except where specifically authorized by statute, subject to judicial oversight, publicly disclosed in general terms, and subject to periodic reaut', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-DEM-001": {"scope_code": "TEC", "family_code": "DEM", "statement": 'AI systems may not be used to generate, distribute, or amplify deceptive election content intended to mislead voters about candidates, voting procedures, ballot access, or election outcomes.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-EDU-001": {"scope_code": "TEC", "family_code": "EDU", "statement": 'AI systems in education must enhance learning without replacing human instruction critical thinking or equitable access to education', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-ENV-001": {"scope_code": "TEC", "family_code": "ENV", "statement": 'AI systems and infrastructure must not externalize environmental costs and must operate within sustainable limits for energy water materials and ecological impact', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-FIN-001": {"scope_code": "TEC", "family_code": "FIN", "statement": 'AI systems in finance credit and insurance must not undermine fairness transparency equal access or protection from discrimination in essential economic systems', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-GOV-001": {"scope_code": "TEC", "family_code": "GOV", "statement": 'AI systems used by government or public-service entities must not undermine due process equal protection transparency accountability or access to rights and services', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-HAR-001": {"scope_code": "TEC", "family_code": "HAR", "statement": 'Digital platforms with significant user bases must implement effective, consistently enforced systems to detect, prevent, and remediate targeted harassment campaigns, coordinated abuse, non-consensual', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-IMM-001": {"scope_code": "TEC", "family_code": "IMM", "statement": 'Ban use of opaque or unreviewable AI systems in immigration enforcement detention or deportation decisions', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-INF-001": {"scope_code": "TEC", "family_code": "INF", "statement": 'AI systems deployed in critical infrastructure must meet heightened standards for safety, cybersecurity, resilience, human override, and incident response.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-JUD-001": {"scope_code": "TEC", "family_code": "JUD", "statement": 'AI systems may not be used to determine sentencing bail or punishment in criminal justice proceedings', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-LAB-001": {"scope_code": "TEC", "family_code": "LAB", "statement": 'AI systems in employment must not undermine worker rights dignity privacy or fair access to economic opportunity', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-MED-001": {"scope_code": "TEC", "family_code": "MED", "statement": 'AI-driven recommender systems may not be optimized primarily for outrage, compulsion, polarization, or misinformation spread where such optimization predictably harms public discourse.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-MHC-001": {"scope_code": "TEC", "family_code": "MHC", "statement": 'AI mental-health tools may assist but must not replace qualified clinicians in diagnosis crisis evaluation or high-risk treatment decisions', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-MIL-001": {"scope_code": "TEC", "family_code": "MIL", "statement": 'Use of AI in military and intelligence contexts must preserve meaningful human control accountability and compliance with constitutional and international law', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-MKT-001": {"scope_code": "TEC", "family_code": "MKT", "statement": 'The use of shared algorithmic systems, common pricing software, or AI-driven pricing models that coordinate prices or suppress competition among nominally competing entities in housing, labor markets,', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-OVR-001": {"scope_code": "TEC", "family_code": "OVR", "statement": 'Require public registration and disclosure of all government AI surveillance systems including purpose authority data sources and oversight structure', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-PRV-001": {"scope_code": "TEC", "family_code": "PRV", "statement": 'Individuals have the right to access lawful online content and services without mandatory identity verification', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-PUB-001": {"scope_code": "TEC", "family_code": "PUB", "statement": 'The federal government must fund, develop, and maintain publicly accessible AI infrastructure — including foundational models, compute resources, and training datasets — to ensure that AI capability i', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-SCI-001": {"scope_code": "TEC", "family_code": "SCI", "statement": 'AI systems may not be used to fabricate research data, images, citations, peer-review identities, or other scientific artifacts in ways that misrepresent truth or authorship.', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-SUR-001": {"scope_code": "TEC", "family_code": "SUR", "statement": 'Ban warrantless mass surveillance', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
    "TEC-SYN-001": {"scope_code": "TEC", "family_code": "SYN", "statement": 'Synthetic media must not be used to deceive the public about real people or events in ways that cause harm, manipulate democratic processes, or undermine individual rights', "status": "PROPOSED", "source_name": "branch_political_project_brainstorm.txt", "line_number": 0},
}
MANUAL_POLICY_ITEM_TO_RULE_ID = {
    192: "TRM-LIM-001",
    193: "TRM-LIM-002",
    194: "TRM-LIM-003",
    195: "TRM-RUN-001",
    196: "TRM-RUN-002",
    197: "TRM-VAC-001",
    198: "TRM-VAC-002",
    199: "TRM-VAC-003",
    200: "COR-ETH-002",
    201: "COR-ETH-003",
    202: "COR-ETH-004",
    203: "COR-ETH-005",
    204: "COR-ETH-006",
    205: "COR-ETH-007",
    206: "COR-ETH-008",
    207: "COR-ETH-009",
    208: "COR-ETH-010",
    209: "COR-ETH-010",
    210: "HLT-MHC-001",
    211: "HLT-STD-002",
    212: "HLT-STD-001",
    213: "HLT-TRL-001",
    214: "HLT-TRL-001",
    215: "HLT-PHR-001",
    216: "HLT-PHR-002",
    217: "HLT-SUP-001",
    218: "HLT-SUP-002",
    219: "HLT-SUP-003",
    220: "HLT-SUP-004",
    221: "HLT-PHR-003",
    222: "HLT-EMS-001",
    223: "HLT-EMS-002",
    224: "HLT-ACC-001",
    225: "HLT-ACC-002",
    226: "HLT-ACC-003",
    227: "HLT-STD-005",
    228: "HLT-STD-008",
    229: "HLT-STD-006",
    230: "HLT-STD-007",
    231: "HLT-STD-008",
    232: "HLT-STD-001",
    233: "HLT-STD-009",
    234: "HLT-STD-008",
    235: "HLT-STD-011",
    236: "HLT-STD-008",
    237: "HLT-STD-005",
    238: "HLT-STD-007",
    239: "HLT-STD-010",
    240: "HLT-STD-008",
    241: "HLT-STD-009",
    242: "HLT-STD-001",
    243: "HLT-STD-009",
    244: "HLT-STD-010",
    245: "HLT-STD-011",
    246: "HLT-STD-002",
    247: "SYS-GEO-001",
    248: "SYS-GEO-002",
    249: "SYS-GEO-003",
    250: "SYS-GEO-004",
    251: "SYS-GEO-005",
    252: "HLT-TEL-001",
    253: "HLT-TEL-002",
    254: "SYS-GEO-002",
    255: "SYS-GEO-001",
    256: "SYS-GEO-002",
    257: "SYS-GEO-003",
    258: "SYS-GEO-004",
    259: "SYS-GEO-005",
    260: "SYS-GEO-003",
    261: "SYS-FED-001",
    262: "SYS-FED-002",
    263: "SYS-FED-003",
    264: "SYS-FED-004",
    265: "SYS-FED-005",
    266: "SYS-FED-004",
    267: "MED-PRS-001",
    268: "MED-PRS-002",
    269: "MED-PRS-003",
    270: "MED-PRS-004",
    271: "COR-WHB-001",
    272: "MED-PRS-005",
    273: "MED-PRS-006",
    274: "MED-PRS-007",
    275: "MED-PRS-008",
    276: "COR-WHB-001",
    277: "MED-PRS-009",
    278: "JUS-DRG-001",
    279: "JUS-DRG-002",
    280: "HLT-STD-012",
    281: "JUS-DRG-003",
    282: "JUS-DRG-004",
    283: "HLT-STD-013",
    284: "JUS-DRG-005",
    285: "HLT-REB-001",
    286: "HLT-REB-002",
    287: "HLT-REB-003",
    288: "HLT-REB-004",
    289: "HLT-REB-005",
    290: "HLT-REB-006",
    291: "HLT-REB-007",
    292: "RGT-BOD-001",
    # ── New seeds: HOU, TAX, LAB, EDU, JUS-MIL, ENV, ECO-ANT ─────────────────
    125: "EDU-RGT-001",
    132: "LAB-PAY-001",
    133: "LAB-PAY-002",
    138: "HOU-RGT-001",
    139: "LAB-LVE-001",
    143: "JUS-CAP-001",
    157: "JUS-MIL-001",
    158: "JUS-MIL-001",
    163: "TAX-GEN-001",
    164: "TAX-WTH-001",
    167: "ECO-ANT-001",
    175: "ENV-PKS-001",
    176: "ENV-URB-001",
    188: "HOU-GEN-001",
}


@dataclass(frozen=True)
class SourceFile:
    name: str
    path: Path
    priority: int


@dataclass
class PolicyOccurrence:
    item_id: int
    source_name: str
    line_number: int
    statement: str
    status: str
    target: str
    notes: str
    raw_line: str


@dataclass
class RuleOccurrence:
    rule_id: str
    source_name: str
    line_number: int
    scope_code: str
    family_code: str
    statement: str
    status: str
    raw_line: str


@dataclass
class RecordLinkOccurrence:
    source_record_type: str
    source_record_id: str
    target_record_type: str
    target_record_id: str
    relationship_type: str
    source_name: str
    line_number: int
    label: str
    status: str
    target_file: str
    notes: str
    raw_line: str


@dataclass
class ProseRuleMention:
    rule_id: str
    source_name: str
    line_number: int
    description: str
    raw_line: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import structured policy items and rule IDs from branch chat logs."
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root. Defaults to the current script's repo.",
    )
    parser.add_argument(
        "--db",
        default=None,
        type=Path,
        help="Path to the SQLite database. Defaults to <repo>/data/policy_catalog.sqlite.",
    )
    return parser.parse_args()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_source_files(chat_dir: Path) -> list[SourceFile]:
    files: list[SourceFile] = []
    for name, priority in NUMERIC_SOURCE_PRIORITY.items():
        path = chat_dir / name
        if path.exists():
            files.append(SourceFile(name=name, path=path, priority=priority))
    fetched_dir = chat_dir.parent  # chatgpt-fetched files are now directly under sources/
    for name, priority in FETCHED_SOURCE_PRIORITY.items():
        path = fetched_dir / name
        if path.exists():
            files.append(SourceFile(name=name, path=path, priority=priority))
    return files


def parse_numeric_occurrences(source: SourceFile) -> list[PolicyOccurrence]:
    occurrences: list[PolicyOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("\t")
        if len(parts) < NUMERIC_ROW_MIN_FIELDS or not parts[0].isdigit():
            continue

        parts += [""] * (5 - len(parts))
        item_id, statement, status, target = parts[:4]
        notes = parts[4] if len(parts) > 4 else ""
        occurrences.append(
            PolicyOccurrence(
                item_id=int(item_id),
                source_name=source.name,
                line_number=line_number,
                statement=statement.strip(),
                status=status.strip(),
                target=target.strip(),
                notes=notes.strip(),
                raw_line=line,
            )
        )
    return occurrences


def parse_rule_occurrences(source: SourceFile) -> list[RuleOccurrence]:
    occurrences: list[RuleOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("|")
        if len(parts) != 5:
            continue
        rule_id, scope_code, family_code, statement, status = (part.strip() for part in parts)
        if not RULE_ID_RE.match(rule_id):
            continue
        occurrences.append(
            RuleOccurrence(
                rule_id=rule_id,
                source_name=source.name,
                line_number=line_number,
                scope_code=scope_code,
                family_code=family_code,
                statement=statement,
                status=status,
                raw_line=line,
            )
        )
    return occurrences


def parse_record_link_occurrences(source: SourceFile) -> list[RecordLinkOccurrence]:
    occurrences: list[RecordLinkOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        match = MIGRATION_ROW_RE.match(line)
        if not match:
            continue
        old_id, new_id, label, target_file, status, notes = (part.strip() for part in match.groups())
        occurrences.append(
            RecordLinkOccurrence(
                source_record_type="policy_item",
                source_record_id=old_id,
                target_record_type="rule_item",
                target_record_id=new_id,
                relationship_type="migrated_to",
                source_name=source.name,
                line_number=line_number,
                label=label,
                status=status,
                target_file=target_file,
                notes=notes,
                raw_line=line,
            )
        )
    return occurrences


def parse_prose_rule_mentions(source: SourceFile) -> list[ProseRuleMention]:
    mentions: list[ProseRuleMention] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or "|" in stripped:
            continue
        match = PROSE_RULE_ID_RE.match(stripped)
        if not match:
            continue
        rule_id, description = match.groups()
        mentions.append(
            ProseRuleMention(
                rule_id=rule_id,
                source_name=source.name,
                line_number=line_number,
                description=description.strip(),
                raw_line=line,
            )
        )
    return mentions


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS source_files (
            id INTEGER PRIMARY KEY,
            source_name TEXT NOT NULL UNIQUE,
            relative_path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            source_priority INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policy_items (
            item_id INTEGER PRIMARY KEY,
            canonical_statement TEXT NOT NULL,
            status TEXT NOT NULL,
            target TEXT NOT NULL,
            notes TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policy_item_occurrences (
            id INTEGER PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES policy_items(item_id) ON DELETE CASCADE,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            statement TEXT NOT NULL,
            status TEXT NOT NULL,
            target TEXT NOT NULL,
            notes TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(item_id, source_id, line_number, raw_line)
        );

        CREATE TABLE IF NOT EXISTS rule_items (
            rule_id TEXT PRIMARY KEY,
            scope_code TEXT NOT NULL,
            family_code TEXT NOT NULL,
            canonical_statement TEXT NOT NULL,
            status TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rule_occurrences (
            id INTEGER PRIMARY KEY,
            rule_id TEXT NOT NULL REFERENCES rule_items(rule_id) ON DELETE CASCADE,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            scope_code TEXT NOT NULL,
            family_code TEXT NOT NULL,
            statement TEXT NOT NULL,
            status TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(rule_id, source_id, line_number, raw_line)
        );

        CREATE TABLE IF NOT EXISTS record_links (
            id INTEGER PRIMARY KEY,
            source_record_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            target_record_type TEXT NOT NULL,
            target_record_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            canonical_label TEXT NOT NULL,
            status TEXT NOT NULL,
            target_file TEXT NOT NULL,
            notes TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL,
            UNIQUE (source_record_type, source_record_id, target_record_type, target_record_id, relationship_type)
        );

        CREATE TABLE IF NOT EXISTS record_link_occurrences (
            id INTEGER PRIMARY KEY,
            source_record_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            target_record_type TEXT NOT NULL,
            target_record_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            label TEXT NOT NULL,
            status TEXT NOT NULL,
            target_file TEXT NOT NULL,
            notes TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                raw_line
            )
        );

        CREATE TABLE IF NOT EXISTS prose_rule_mentions (
            id INTEGER PRIMARY KEY,
            rule_id TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            description TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(rule_id, source_id, line_number, raw_line)
        );

        DROP VIEW IF EXISTS catalog_entries;
        CREATE VIEW catalog_entries AS
        SELECT
            'policy_item' AS record_type,
            CAST(item_id AS TEXT) AS record_id,
            NULL AS scope_code,
            NULL AS family_code,
            canonical_statement AS statement,
            status,
            target,
            notes,
            occurrence_count,
            source_count
        FROM policy_items
        UNION ALL
        SELECT
            'rule_item' AS record_type,
            rule_id AS record_id,
            scope_code,
            family_code,
            canonical_statement AS statement,
            status,
            NULL AS target,
            NULL AS notes,
            occurrence_count,
            source_count
        FROM rule_items;

        DROP VIEW IF EXISTS deduped_catalog_entries;
        CREATE VIEW deduped_catalog_entries AS
        SELECT
            ce.record_type,
            ce.record_id,
            ce.scope_code,
            ce.family_code,
            ce.statement,
            ce.status,
            ce.target,
            ce.notes,
            ce.occurrence_count,
            ce.source_count
        FROM catalog_entries ce
        WHERE NOT (
            ce.record_type = 'policy_item'
            AND EXISTS (
                SELECT 1
                FROM record_links rl
                WHERE rl.relationship_type = 'migrated_to'
                  AND rl.source_record_type = 'policy_item'
                  AND rl.target_record_type = 'rule_item'
                  AND rl.source_record_id = ce.record_id
            )
        );

        DROP VIEW IF EXISTS unresolved_prose_rule_mentions;
        CREATE VIEW unresolved_prose_rule_mentions AS
        SELECT
            prm.rule_id,
            sf.source_name,
            prm.line_number,
            prm.description,
            prm.raw_line
        FROM prose_rule_mentions prm
        JOIN source_files sf ON sf.id = prm.source_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM rule_items ri
            WHERE ri.rule_id = prm.rule_id
        );

        CREATE INDEX IF NOT EXISTS idx_policy_items_status ON policy_items(status);
        CREATE INDEX IF NOT EXISTS idx_policy_items_target ON policy_items(target);
        CREATE INDEX IF NOT EXISTS idx_policy_occurrences_source ON policy_item_occurrences(source_id, item_id);
        CREATE INDEX IF NOT EXISTS idx_rule_items_scope_family ON rule_items(scope_code, family_code);
        CREATE INDEX IF NOT EXISTS idx_rule_items_status ON rule_items(status);
        CREATE INDEX IF NOT EXISTS idx_rule_occurrences_source ON rule_occurrences(source_id, rule_id);
        CREATE INDEX IF NOT EXISTS idx_record_links_source ON record_links(source_record_type, source_record_id);
        CREATE INDEX IF NOT EXISTS idx_record_links_target ON record_links(target_record_type, target_record_id);
        CREATE INDEX IF NOT EXISTS idx_record_link_occurrences_source ON record_link_occurrences(source_id, source_record_id);
        CREATE INDEX IF NOT EXISTS idx_prose_rule_mentions_rule_id ON prose_rule_mentions(rule_id);
        """
    )


def reset_import_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DELETE FROM prose_rule_mentions;
        DELETE FROM record_link_occurrences;
        DELETE FROM record_links;
        DELETE FROM rule_occurrences;
        DELETE FROM rule_items;
        DELETE FROM policy_item_occurrences;
        DELETE FROM policy_items;
        DELETE FROM source_files;
        """
    )


def insert_source_files(conn: sqlite3.Connection, repo_root: Path, sources: Iterable[SourceFile]) -> dict[str, int]:
    source_ids: dict[str, int] = {}
    for source in sources:
        text = source.path.read_text(encoding="utf-8")
        cursor = conn.execute(
            """
            INSERT INTO source_files (source_name, relative_path, sha256, source_priority)
            VALUES (?, ?, ?, ?)
            """,
            (
                source.name,
                str(source.path.relative_to(repo_root)),
                sha256_text(text),
                source.priority,
            ),
        )
        source_ids[source.name] = int(cursor.lastrowid)
    return source_ids


def choose_policy_canonical(occurrences: list[PolicyOccurrence], source_priority: dict[str, int]) -> PolicyOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.statement)),
    )[0]


def choose_rule_canonical(occurrences: list[RuleOccurrence], source_priority: dict[str, int]) -> RuleOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.statement)),
    )[0]


def choose_record_link_canonical(
    occurrences: list[RecordLinkOccurrence], source_priority: dict[str, int]
) -> RecordLinkOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.label)),
    )[0]


def import_policy_items(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[PolicyOccurrence],
) -> None:
    grouped: dict[int, list[PolicyOccurrence]] = {}
    for occurrence in occurrences:
        grouped.setdefault(occurrence.item_id, []).append(occurrence)

    for item_id, item_occurrences in sorted(grouped.items()):
        canonical = choose_policy_canonical(item_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO policy_items (
                item_id,
                canonical_statement,
                status,
                target,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                canonical.statement,
                canonical.status,
                canonical.target,
                canonical.notes,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(item_occurrences),
                len({occ.source_name for occ in item_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO policy_item_occurrences (
                item_id,
                source_id,
                line_number,
                statement,
                status,
                target,
                notes,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item_id,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.statement,
                    occ.status,
                    occ.target,
                    occ.notes,
                    occ.raw_line,
                )
                for occ in item_occurrences
            ],
        )


def import_rule_items(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[RuleOccurrence],
) -> None:
    grouped: dict[str, list[RuleOccurrence]] = {}
    for occurrence in occurrences:
        grouped.setdefault(occurrence.rule_id, []).append(occurrence)

    for rule_id, rule_occurrences in sorted(grouped.items()):
        canonical = choose_rule_canonical(rule_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO rule_items (
                rule_id,
                scope_code,
                family_code,
                canonical_statement,
                status,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rule_id,
                canonical.scope_code,
                canonical.family_code,
                canonical.statement,
                canonical.status,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(rule_occurrences),
                len({occ.source_name for occ in rule_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO rule_occurrences (
                rule_id,
                source_id,
                line_number,
                scope_code,
                family_code,
                statement,
                status,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    rule_id,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.scope_code,
                    occ.family_code,
                    occ.statement,
                    occ.status,
                    occ.raw_line,
                )
                for occ in rule_occurrences
            ],
        )


def import_record_links(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[RecordLinkOccurrence],
) -> None:
    grouped: dict[tuple[str, str, str, str, str], list[RecordLinkOccurrence]] = {}
    for occurrence in occurrences:
        key = (
            occurrence.source_record_type,
            occurrence.source_record_id,
            occurrence.target_record_type,
            occurrence.target_record_id,
            occurrence.relationship_type,
        )
        grouped.setdefault(key, []).append(occurrence)

    for key, link_occurrences in sorted(grouped.items()):
        canonical = choose_record_link_canonical(link_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO record_links (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                canonical_label,
                status,
                target_file,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                canonical.source_record_type,
                canonical.source_record_id,
                canonical.target_record_type,
                canonical.target_record_id,
                canonical.relationship_type,
                canonical.label,
                canonical.status,
                canonical.target_file,
                canonical.notes,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(link_occurrences),
                len({occ.source_name for occ in link_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO record_link_occurrences (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                label,
                status,
                target_file,
                notes,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    occ.source_record_type,
                    occ.source_record_id,
                    occ.target_record_type,
                    occ.target_record_id,
                    occ.relationship_type,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.label,
                    occ.status,
                    occ.target_file,
                    occ.notes,
                    occ.raw_line,
                )
                for occ in link_occurrences
            ],
        )


def import_prose_rule_mentions(
    conn: sqlite3.Connection, source_ids: dict[str, int], mentions: list[ProseRuleMention]
) -> None:
    conn.executemany(
        """
        INSERT INTO prose_rule_mentions (
            rule_id,
            source_id,
            line_number,
            description,
            raw_line
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                mention.rule_id,
                source_ids[mention.source_name],
                mention.line_number,
                mention.description,
                mention.raw_line,
            )
            for mention in mentions
        ],
    )


def get_line_from_source(source: SourceFile, line_number: int) -> str:
    lines = source.path.read_text(encoding="utf-8").splitlines()
    if line_number < 1 or line_number > len(lines):
        return ""
    return lines[line_number - 1]


def insert_manual_rule_seeds(
    conn: sqlite3.Connection, sources: dict[str, SourceFile], source_ids: dict[str, int]
) -> None:
    for rule_id, seed in MANUAL_RULE_SEEDS.items():
        exists = conn.execute("SELECT 1 FROM rule_items WHERE rule_id = ?", (rule_id,)).fetchone()
        if exists:
            continue
        source = sources[seed["source_name"]]
        raw_line = get_line_from_source(source, seed["line_number"])
        conn.execute(
            """
            INSERT INTO rule_items (
                rule_id,
                scope_code,
                family_code,
                canonical_statement,
                status,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1)
            """,
            (
                rule_id,
                seed["scope_code"],
                seed["family_code"],
                seed["statement"],
                seed["status"],
                source_ids[seed["source_name"]],
                seed["line_number"],
            ),
        )
        conn.execute(
            """
            INSERT INTO rule_occurrences (
                rule_id,
                source_id,
                line_number,
                scope_code,
                family_code,
                statement,
                status,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rule_id,
                source_ids[seed["source_name"]],
                seed["line_number"],
                seed["scope_code"],
                seed["family_code"],
                seed["statement"],
                seed["status"],
                raw_line,
            ),
        )


def apply_manual_policy_item_links(conn: sqlite3.Connection) -> None:
    current_ids = tuple(str(item_id) for item_id in MANUAL_POLICY_ITEM_TO_RULE_ID)
    placeholders = ", ".join("?" for _ in current_ids)
    conn.execute(
        f"""
        DELETE FROM record_link_occurrences
        WHERE source_record_type = 'policy_item'
          AND relationship_type = 'migrated_to'
          AND source_record_id IN ({placeholders})
        """,
        current_ids,
    )
    conn.execute(
        f"""
        DELETE FROM record_links
        WHERE source_record_type = 'policy_item'
          AND relationship_type = 'migrated_to'
          AND source_record_id IN ({placeholders})
        """,
        current_ids,
    )

    for item_id, target_rule_id in MANUAL_POLICY_ITEM_TO_RULE_ID.items():
        policy_row = conn.execute(
            """
            SELECT
                p.canonical_statement,
                p.canonical_source_id,
                p.canonical_line_number,
                p.status,
                COALESCE(pio.raw_line, '')
            FROM policy_items p
            LEFT JOIN policy_item_occurrences pio
              ON pio.item_id = p.item_id
             AND pio.source_id = p.canonical_source_id
             AND pio.line_number = p.canonical_line_number
            WHERE p.item_id = ?
            """,
            (item_id,),
        ).fetchone()
        rule_row = conn.execute(
            """
            SELECT canonical_statement, status
            FROM rule_items
            WHERE rule_id = ?
            """,
            (target_rule_id,),
        ).fetchone()
        if not policy_row or not rule_row:
            continue

        policy_statement, source_id, line_number, _policy_status, raw_line = policy_row
        rule_statement, rule_status = rule_row
        notes = "Context-based conversion to the later structured ID corpus."
        conn.execute(
            """
            INSERT INTO record_links (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                canonical_label,
                status,
                target_file,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES ('policy_item', ?, 'rule_item', ?, 'migrated_to', ?, ?, '', ?, ?, ?, 1, 1)
            """,
            (
                str(item_id),
                target_rule_id,
                rule_statement,
                rule_status,
                notes,
                source_id,
                line_number,
            ),
        )
        conn.execute(
            """
            INSERT INTO record_link_occurrences (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                label,
                status,
                target_file,
                notes,
                raw_line
            )
            VALUES ('policy_item', ?, 'rule_item', ?, 'migrated_to', ?, ?, ?, ?, '', ?, ?)
            """,
            (
                str(item_id),
                target_rule_id,
                source_id,
                line_number,
                rule_statement,
                rule_status,
                notes,
                raw_line,
            ),
        )


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    db_path = (args.db or (repo_root / "data" / "policy_catalog.sqlite")).resolve()
    chat_dir = repo_root / "sources" / "chat-logs"
    sources = get_source_files(chat_dir)
    source_lookup = {source.name: source for source in sources}

    if not sources:
        raise SystemExit(f"No chat logs found under {chat_dir}")

    all_source_priority = {**NUMERIC_SOURCE_PRIORITY, **FETCHED_SOURCE_PRIORITY}

    all_policy_occurrences: list[PolicyOccurrence] = []
    all_rule_occurrences: list[RuleOccurrence] = []
    all_record_link_occurrences: list[RecordLinkOccurrence] = []
    all_prose_rule_mentions: list[ProseRuleMention] = []
    for source in sources:
        all_policy_occurrences.extend(parse_numeric_occurrences(source))
        all_rule_occurrences.extend(parse_rule_occurrences(source))
        all_record_link_occurrences.extend(parse_record_link_occurrences(source))
        all_prose_rule_mentions.extend(parse_prose_rule_mentions(source))

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        create_schema(conn)
        reset_import_tables(conn)
        source_ids = insert_source_files(conn, repo_root, sources)
        import_policy_items(conn, source_ids, all_source_priority, all_policy_occurrences)
        import_rule_items(conn, source_ids, all_source_priority, all_rule_occurrences)
        insert_manual_rule_seeds(conn, source_lookup, source_ids)
        import_record_links(conn, source_ids, all_source_priority, all_record_link_occurrences)
        apply_manual_policy_item_links(conn)
        import_prose_rule_mentions(conn, source_ids, all_prose_rule_mentions)
        conn.commit()

        policy_count = conn.execute("SELECT COUNT(*) FROM policy_items").fetchone()[0]
        policy_occurrence_count = conn.execute("SELECT COUNT(*) FROM policy_item_occurrences").fetchone()[0]
        rule_count = conn.execute("SELECT COUNT(*) FROM rule_items").fetchone()[0]
        rule_occurrence_count = conn.execute("SELECT COUNT(*) FROM rule_occurrences").fetchone()[0]
        record_link_count = conn.execute("SELECT COUNT(*) FROM record_links").fetchone()[0]
        record_link_occurrence_count = conn.execute("SELECT COUNT(*) FROM record_link_occurrences").fetchone()[0]
        prose_rule_mention_count = conn.execute("SELECT COUNT(*) FROM prose_rule_mentions").fetchone()[0]

    print(f"Imported {policy_count} canonical policy items from {policy_occurrence_count} occurrences.")
    print(f"Imported {rule_count} canonical rule items from {rule_occurrence_count} occurrences.")
    print(
        f"Imported {record_link_count} canonical dedupe links from {record_link_occurrence_count} occurrences."
    )
    print(f"Imported {prose_rule_mention_count} contextual ID mentions.")
    print(f"Database written to {db_path}")


if __name__ == "__main__":
    main()
