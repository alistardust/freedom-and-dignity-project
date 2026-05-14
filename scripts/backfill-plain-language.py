#!/usr/bin/env python3
"""Backfill plain_language (rule-plain) for IMMG, IMMI, and TAXN positions.

Updates both the SQLite catalog and the HTML pillar pages.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
IMMG_HTML = REPO_ROOT / "docs" / "policy" / "immigration.html"
TAXN_HTML = REPO_ROOT / "docs" / "policy" / "taxation-and-wealth.html"

# fmt: off
PLAIN_LANGUAGE: dict[str, str] = {
    # ── IMMG-ACCS  Access to Services ───────────────────────────────────────
    "IMMG-ACCS-0001": "Your immigration status can affect which programs you qualify for, but it cannot be used to deny you emergency medical care, basic education, or other protections the law guarantees everyone.",
    "IMMG-ACCS-0002": "Every child in the United States — regardless of immigration status — has the right to attend school and get the basic supports they need to learn and grow.",
    "IMMG-ACCS-0003": "Local services like healthcare, schools, and legal help should be easy for immigrants to use — not set up in ways that push people into hiding or leave them vulnerable to exploitation.",
    "IMMG-ACCS-0004": "Public services should offer clear information in multiple languages so immigrants can understand their rights, their responsibilities, and where to get help — without needing insider connections.",
    "IMMG-ACCS-0005": "People should be able to report a crime, get emergency help, go to school, or see a doctor without fear that doing so will trigger immigration enforcement against them.",
    "IMMG-ACCS-0006": "States and cities cannot turn hospitals, schools, or other everyday services into secret immigration checkpoints where people are reported or detained just for seeking help.",

    # ── IMMG-ADML  Administration ────────────────────────────────────────────
    "IMMG-ADML-0001": "The immigration system needs enough staff and funding to process cases in a reasonable amount of time — long delays cause real harm to people and families left in prolonged uncertainty.",
    "IMMG-ADML-0002": "Immigration rules should be simplified so ordinary people can follow them without needing expensive lawyers just to complete routine paperwork.",
    "IMMG-ADML-0003": "People going through the immigration process should be able to check their case status, get their documents, and find out what is happening — without fighting through a confusing or unresponsive system.",
    "IMMG-ADML-0004": "Immigration forms, legal notices, and deadlines should be written in plain language with clear guidance so people can understand what is being asked of them.",
    "IMMG-ADML-0005": "Speeding up the immigration process cannot come at the cost of fair, individualized review of each person's case.",
    "IMMG-ADML-0006": "Immigration applicants have the right to know their case status, see relevant records, and receive notice of key deadlines — in a format they can actually understand.",
    "IMMG-ADML-0007": "Government agencies cannot use constantly changing requirements, confusing standards, or sudden procedural shifts as a way to effectively deny applications without saying so directly.",
    "IMMG-ADML-0008": "When the government causes delays, loses records, or makes errors that hurt an applicant, the system must offer real remedies — not just shift all the burden back onto the person who was harmed.",

    # ── IMMG-ANTD  Anti-Discrimination ──────────────────────────────────────
    "IMMG-ANTD-0001": "Travel or immigration bans that single out people based on their religion or country of birth must be permanently ended and banned by law going forward.",
    "IMMG-ANTD-0002": "Immigration policies that fall unequally on people of certain religions or national origins must face the highest legal scrutiny, and people harmed by such policies must have the right to sue.",
    "IMMG-ANTD-0003": "The main federal immigration law must be updated to explicitly ban treating people differently based on religion or national origin when issuing visas, making entry decisions, or processing applications.",

    # ── IMMG-ASYS  Asylum System ─────────────────────────────────────────────
    "IMMG-ASYS-0001": "People fleeing danger and asking the U.S. for asylum — protection from persecution — must receive a real, fair hearing, not an automatic rejection before their story is even considered.",
    "IMMG-ASYS-0002": "The asylum system cannot set people up to fail with impossible deadlines, demands for documents they can't get, or assumptions it's safe to send them back when it clearly isn't.",
    "IMMG-ASYS-0003": "A real, accountable person — not an algorithm — must review asylum claims. No one should have their safety decided by a computer's guess about whether they're telling the truth.",
    "IMMG-ASYS-0004": "People who have a credible reason to fear returning home cannot be deported before they've had a meaningful chance to make their case and appeal a decision.",
    "IMMG-ASYS-0005": "Asylum systems must recognize that survivors of violence often struggle to tell their story clearly — trauma, language barriers, and missing documents are not proof that someone is lying.",
    "IMMG-ASYS-0006": "Asylum and refugee processes must be clear, timely, and humane — not built as obstacle courses designed to exhaust or discourage people with valid claims.",
    "IMMG-ASYS-0007": "The first screening to see if someone has a real fear of persecution must be designed to identify people who may qualify — not to screen them out as fast as possible through overly narrow rules.",
    "IMMG-ASYS-0008": "People seeking asylum need enough time, access to their records, and the help of a lawyer or trained representative to properly prepare their case.",
    "IMMG-ASYS-0009": "Asylum decisions must take into account that trauma disrupts memory, that language and cultural differences are real, and that many people fleeing danger have no papers to prove their story.",
    "IMMG-ASYS-0010": "Children, trafficking survivors, survivors of violence, LGBTQ+ people, and others with specific vulnerabilities must have asylum processes designed for their unique needs and safety.",
    "IMMG-ASYS-0011": "Holding people in detention cannot be used as a tactic to pressure them into dropping a valid asylum claim.",
    "IMMG-ASYS-0012": "When an asylum claim is denied, the person must receive a clear explanation in language they understand and have a real opportunity to appeal.",
    "IMMG-ASYS-0013": "Before sending someone back to their home country, officials must individually assess whether it's actually safe — not just assume it's safe because it usually is.",
    "IMMG-ASYS-0014": "Programs that force asylum seekers to wait in dangerous conditions in Mexico, or that require people to apply for safety in a third country they only passed through, must be permanently banned by law.",

    # ── IMMG-BRDS  Border ────────────────────────────────────────────────────
    "IMMG-BRDS-0001": "How the U.S. manages its borders must be legal, humane, and accountable — it cannot rely on indiscriminate force or treat people in degrading ways.",
    "IMMG-BRDS-0002": "Border enforcement officers must operate within constitutional limits — people near the border still have civil rights and human rights that must be protected.",
    "IMMG-BRDS-0003": "When force is used at the border, it must be tightly restricted, carefully documented, and reviewed by independent overseers after the fact.",
    "IMMG-BRDS-0004": "Border processing must be orderly and efficient, but speed cannot be used as an excuse to skip due process, ignore humanitarian claims, or deny people the right to challenge decisions.",
    "IMMG-BRDS-0005": "The military cannot take over border enforcement in ways that become permanent or remove civilian oversight and legal accountability.",
    "IMMG-BRDS-0006": "Border agents must use body cameras, and records must be kept so that abuses, injuries, and rights violations can be documented and investigated.",
    "IMMG-BRDS-0007": "Independent investigators must be able to look into deaths, abuse, use of force, and rights violations at the border and in border detention.",
    "IMMG-BRDS-0008": "Withholding food, water, medical care, shelter, hygiene, or the ability to communicate cannot be used to punish people or force compliance at the border.",
    "IMMG-BRDS-0009": "Facilities where people are held at the border must meet basic standards for healthcare, sanitation, temperature control, child safety, disability access, and keeping families together.",
    "IMMG-BRDS-0010": "Emergency border powers cannot be used indefinitely as a substitute for normal immigration law — they cannot permanently bypass legal protections.",
    "IMMG-BRDS-0011": "Military or military-style operations at the border must have strict limits and cannot replace civilian oversight or constitutional protections.",

    # ── IMMG-CITS  Citizenship ───────────────────────────────────────────────
    "IMMG-CITS-0001": "The path to U.S. citizenship should be clear, affordable, and actually achievable for people who meet the legal requirements — not blocked by red tape or excessive costs.",
    "IMMG-CITS-0002": "The citizenship process should not be designed to keep people out through high fees, long waits, or unnecessarily complicated steps.",
    "IMMG-CITS-0003": "Birthright citizenship — the right of anyone born on U.S. soil to be a citizen — must remain protected and cannot be quietly eliminated through reinterpretation of the law.",
    "IMMG-CITS-0004": "People who have lived here legally for many years should have fair, stable options to fully participate in civic life, including becoming citizens when they qualify.",
    "IMMG-CITS-0005": "Becoming a citizen should be a navigable process — one that doesn't require expensive lawyers or years of unnecessary waiting just to complete the required steps.",
    "IMMG-CITS-0006": "The citizenship process should not be clogged with unnecessary obstacles, backlogs, or fees that make it practically impossible for eligible people to complete.",
    "IMMG-CITS-0007": "Long-term residents should not be stuck in legal limbo where citizenship is technically available but so difficult to access that it remains effectively out of reach for most people.",
    "IMMG-CITS-0008": "Language support, accommodations, and clear guidance must be provided during the naturalization process so the right to become a citizen is meaningful in practice, not just on paper.",
    "IMMG-CITS-0009": "While the citizenship process can require civic knowledge, it cannot be designed as a cultural or ideological test used to exclude people who don't share certain values.",
    "IMMG-CITS-0010": "Application fees and requirements for citizenship must include waivers or public assistance so that people with lower incomes aren't simply priced out of becoming citizens.",

    # ── IMMG-CLMS  Climate Migration ─────────────────────────────────────────
    "IMMG-CLMS-0001": "The U.S. must create a special visa category for people forced to flee their homes because of climate disasters like rising seas, drought, or severe storms — these people are refugees even if the law doesn't yet call them that.",
    "IMMG-CLMS-0002": "People from countries experiencing major climate emergencies should automatically qualify for temporary protected status, meaning they can legally remain in the U.S. while their home country recovers.",
    "IMMG-CLMS-0003": "The U.S. should lead international efforts to create binding rules that formally protect people displaced by climate change under international law, since existing refugee law doesn't cover climate displacement.",

    # ── IMMG-CONS  Contractors ───────────────────────────────────────────────
    "IMMG-CONS-0001": "Private companies hired to help run immigration processing, transportation, surveillance, or services must follow the same rules and be held to the same standards as government agencies.",
    "IMMG-CONS-0002": "Contractors working on immigration cannot hide behind claims of trade secrecy or private-company status to escape oversight, public disclosure, or accountability in court.",
    "IMMG-CONS-0003": "Private immigration contractors must be regularly audited, reported on publicly, and subject to real penalties when they abuse people or break the rules.",
    "IMMG-CONS-0004": "No contract can reward companies for detaining more people, deporting more people, or denying more claims — these perverse incentives put profit ahead of people's rights.",
    "IMMG-CONS-0005": "Immigration service contracts must prioritize protecting people's rights and delivering quality care — not simply awarding work to whoever charges the least.",
    "IMMG-CONS-0006": "The government cannot split immigration functions across so many contractors that no single entity can be held responsible when someone is harmed.",
    "IMMG-CONS-0007": "People hurt by immigration contractors must be able to access records, file complaints, and pursue legal claims against both the company and the government that hired them.",
    "IMMG-CONS-0008": "Independent watchdogs must have full access to contractor-run facilities, records, communications, incident reports, and complaint data — no exceptions.",
    "IMMG-CONS-0009": "Core immigration functions — like making detention decisions, enforcing immigration law, and deciding cases — must be done by accountable government employees, not outsourced to private companies.",
    "IMMG-CONS-0010": "'Core immigration functions' includes detention decisions, deportation authority, case management, and access to legal records — these cannot legally be handed off to private contractors.",
    "IMMG-CONS-0011": "Private contractors can be used for things like facility maintenance, food services, translation, or technology — as long as they have no authority over people and make no rights-affecting decisions.",
    "IMMG-CONS-0012": "Contractors may never have authority to detain people, make enforcement decisions, or participate in legal proceedings — those powers must remain with accountable government officials.",
    "IMMG-CONS-0013": "No contract can tie contractor pay to the number of people detained, deported, or denied — any metric linked to taking away someone's liberty or rights is prohibited.",
    "IMMG-CONS-0014": "The government cannot indirectly outsource core immigration functions through layers of subcontractors, partnerships, or inter-agency agreements designed to get around contractor restrictions.",
    "IMMG-CONS-0015": "All permitted contractors must be subject to full public accountability — including transparency requirements, records access, audit authority, and the same legal liability as government agencies.",
    "IMMG-CONS-0016": "People harmed by contractor actions must be able to pursue full legal remedies against both the contractor and the responsible government entity — without procedural barriers blocking the way.",

    # ── IMMG-CRTS  Courts ────────────────────────────────────────────────────
    "IMMG-CRTS-0001": "Immigration courts must be structured to be independent, fair, and competent — they cannot function as rubber-stamp machines that automatically approve enforcement requests.",
    "IMMG-CRTS-0002": "Immigration courts should be shielded from political pressure, case quotas, and enforcement-first incentives that undermine judges' ability to decide cases fairly.",
    "IMMG-CRTS-0003": "People in immigration proceedings must have clear access to their records, hearing dates, evidence, and enough procedural guidance to meaningfully participate in their own case.",
    "IMMG-CRTS-0004": "Immigration judges must receive training on trauma, cultural competency, and human rights — these are high-stakes cases that affect people's lives and safety.",
    "IMMG-CRTS-0005": "Immigration courts should be removed from the Justice Department's control and reconstituted as an independent court, similar to other specialized federal courts, to protect against political interference.",
    "IMMG-CRTS-0006": "Emergency funding and judge hiring must be approved to clear the immigration court backlog within five years, so people are not left waiting years for a basic hearing.",

    # ── IMMG-DACA  DACA / Dreamers ───────────────────────────────────────────
    "IMMG-DACA-0001": "People brought to the United States as children — often called 'Dreamers' — deserve permanent legal protection and a clear, accessible pathway to citizenship.",
    "IMMG-DACA-0002": "DACA (Deferred Action for Childhood Arrivals) protections must be made permanent in law, not left dependent on executive decisions that can be reversed at any time.",

    # ── IMMG-DATA  Data & Surveillance ──────────────────────────────────────
    "IMMG-DATA-0001": "Immigration agencies cannot use mass data surveillance or commercially purchased data to build secret enforcement profiles on people or bypass normal legal processes.",
    "IMMG-DATA-0002": "Sharing immigration data with other government systems must be tightly limited, clearly justified, and transparent to the public — not used for unrelated tracking.",
    "IMMG-DATA-0003": "Immigration data is highly sensitive and cannot be used for unrelated profiling, sold for commercial purposes, or accessed for political targeting.",
    "IMMG-DATA-0004": "People must be able to challenge and correct inaccurate information in government databases that could affect their legal status, detention risk, or likelihood of deportation.",

    # ── IMMG-DETS  Detention ─────────────────────────────────────────────────
    "IMMG-DETS-0001": "Locking someone up in immigration detention must be a last resort — it cannot be used simply as an administrative convenience or as a way to scare people away from seeking legal protection.",
    "IMMG-DETS-0002": "No one can be held in immigration detention indefinitely — there must be a process and a timeline for review.",
    "IMMG-DETS-0003": "Places where immigrants are detained must meet strong standards for healthcare, sanitation, safety, dignity, and the ability to communicate with family and lawyers.",
    "IMMG-DETS-0004": "Alternatives to detention — like check-ins, ankle monitors, or community supervision — must be used when they can reasonably ensure someone shows up and doesn't pose a safety risk.",
    "IMMG-DETS-0005": "Every immigration detention case must be reviewed promptly and regularly — people cannot be held indefinitely without ongoing individual review.",
    "IMMG-DETS-0006": "Using offshore detention facilities or other legally murky arrangements to place people beyond the reach of U.S. law and oversight is prohibited.",
    "IMMG-DETS-0007": "Private, for-profit immigration detention facilities are prohibited — locking people up for profit creates the wrong incentives.",
    "IMMG-DETS-0008": "Detaining, transporting, or confining immigrants may not be outsourced to private companies seeking to make money from it.",
    "IMMG-DETS-0009": "The government cannot use private contractors as a way to escape accountability, transparency requirements, or the legal protections that apply to government-run detention.",
    "IMMG-DETS-0010": "All government-run immigration detention must meet strong standards for healthcare, mental health services, disability access, child safety, communication access, and humane treatment.",
    "IMMG-DETS-0011": "Deaths, injuries, medical neglect, sexual abuse, and serious rights violations in immigration custody must trigger mandatory independent investigations and public reporting.",
    "IMMG-DETS-0012": "Staff members involved in abuse, neglect, falsifying records, or retaliating against detained people must face real consequences, including removal from their positions.",

    # ── IMMG-DOCS  Documents & Identity ─────────────────────────────────────
    "IMMG-DOCS-0001": "Government agencies must accept updated legal identity documents — including name and gender changes — and cannot use conflicting rules across agencies to create barriers for transgender people.",
    "IMMG-DOCS-0002": "Changes to how sex and gender are recorded on passports and identity documents must be implemented in ways that don't create new travel barriers or safety risks for people who are affected.",

    # ── IMMG-DUES  Due Process ───────────────────────────────────────────────
    "IMMG-DUES-0001": "People in immigration proceedings must have meaningful due process — including proper notice, interpretation services, access to their records, and a real chance to be heard.",
    "IMMG-DUES-0002": "People must have timely access to a lawyer or trained representative in immigration cases — especially when they face detention, deportation, or separation from their family.",
    "IMMG-DUES-0003": "Immigration proceedings cannot use rushed scheduling, procedural traps, or systems that are too hard to navigate — these effectively deny people their rights without officially saying so.",
    "IMMG-DUES-0004": "Immigration decisions must be reviewable — they cannot be shielded from court oversight through excessive secrecy or unchecked government discretion.",
    "IMMG-DUES-0005": "Interpretation and translation services must be available at every important stage of immigration processing and court hearings — and must be free of charge.",
    "IMMG-DUES-0006": "All persons in the United States or under U.S. authority — regardless of immigration status — are entitled to fundamental legal protections, including due process and access to courts.",
    "IMMG-DUES-0007": "Immigration status cannot be used to strip someone of their right to a lawyer, judicial review, or basic procedural protections.",
    "IMMG-DUES-0008": "People held in immigration detention must have timely access to a lawyer — barriers that make legal representation practically impossible are unacceptable.",
    "IMMG-DUES-0009": "The right of habeas corpus — the ability to challenge your own detention in court — applies fully to everyone held under immigration authority and cannot be taken away through legal workarounds.",
    "IMMG-DUES-0010": "Decisions about immigration detention and deportation must remain subject to meaningful judicial review — courts cannot be stripped of the power to check government overreach.",
    "IMMG-DUES-0011": "No category of person under U.S. jurisdiction can be placed into a legal status that eliminates their access to courts or any real way to challenge their detention or removal.",
    "IMMG-DUES-0012": "Everyone facing deportation, detention, or an asylum hearing must have the right to a government-appointed lawyer if they cannot afford one.",
    "IMMG-DUES-0013": "Certified interpreters who match the person's language and dialect must be provided at every stage of immigration proceedings and custody — not just at the formal hearing.",

    # ── IMMG-ENFL  Enforcement / ICE ────────────────────────────────────────
    "IMMG-ENFL-0001": "ICE (Immigration and Customs Enforcement) as it currently operates should be abolished and replaced with narrower, rights-respecting structures that cannot reproduce its documented patterns of abuse.",
    "IMMG-ENFL-0002": "Any replacement for ICE must operate under strict legal limits, with independent oversight, public reporting, and enforceable civil rights protections built in from the start.",
    "IMMG-ENFL-0003": "Immigration enforcement agencies cannot use broad, unchecked discretion, fragmented secrecy, or deliberate cruelty as operational tools.",
    "IMMG-ENFL-0004": "Immigration enforcement must be structurally separated from humanitarian processing, asylum review, and support services — combining them creates abuse and undermines both purposes.",
    "IMMG-ENFL-0005": "Any replacement enforcement structure must include real anti-abuse safeguards — complaint systems, external investigations, decertification authority, and actual remedies for rights violations.",
    "IMMG-ENFL-0006": "Congress must phase out ICE and replace it with structurally separate enforcement bodies that are subject to different, more transparent accountability mechanisms.",
    "IMMG-ENFL-0007": "Immigration enforcement cannot be used to target people based on their politics, religion, race, or as retaliation against activists, journalists, or community members.",

    # ── IMMG-FAMS  Family ────────────────────────────────────────────────────
    "IMMG-FAMS-0001": "Separating families during immigration enforcement is prohibited except in the narrowest circumstances involving an immediate, documented safety emergency — and even then requires independent review.",
    "IMMG-FAMS-0002": "Immigration systems must actively work to keep families together and must have real processes for reunifying families and coordinating cases for family members.",
    "IMMG-FAMS-0003": "Children caught up in immigration systems must receive heightened protections — including access to care, education, a legal guardian, and processes that account for their age and development.",
    "IMMG-FAMS-0004": "Families cannot be forced into waiving their rights or agreeing to deportation through threats of family separation, longer detention, or withholding basic care.",
    "IMMG-FAMS-0005": "The federal government must create a remediation and family reunification fund for families torn apart under the Zero Tolerance policy and related enforcement actions.",

    # ── IMMG-INTL  Integration ───────────────────────────────────────────────
    "IMMG-INTL-0001": "Immigration policy should support immigrants in building stable lives — through language access, community support, work authorization, and predictable rules — rather than trapping people in prolonged uncertainty.",
    "IMMG-INTL-0002": "People waiting for immigration decisions should have clear rules about their right to work and carry on with daily life while their cases are pending.",
    "IMMG-INTL-0003": "Being stuck in legal limbo for years is not an acceptable long-term outcome for people who have built significant ties, have valid legal claims, or have lived here for a long time.",
    "IMMG-INTL-0004": "The immigration system should be designed so that people aren't afraid to send their kids to school, go to the doctor, or report a crime — fear of enforcement shouldn't follow people everywhere.",

    # ── IMMG-LABS  Labor ─────────────────────────────────────────────────────
    "IMMG-LABS-0001": "Employers cannot use a worker's immigration status as a threat to suppress wages, retaliate against complaints, or avoid following labor law.",
    "IMMG-LABS-0002": "All workers — regardless of immigration status — are protected by labor safety laws, minimum wage requirements, and anti-exploitation laws.",
    "IMMG-LABS-0003": "Reporting wage theft, unsafe working conditions, or labor trafficking must not expose workers to retaliatory deportation or immigration enforcement.",
    "IMMG-LABS-0004": "Work visa programs must be designed to reduce the power employers hold over workers — systems that leave workers completely dependent on one employer create conditions for abuse.",
    "IMMG-LABS-0005": "Work authorization pathways tied to a specific employer should not function as indentured servitude — workers must retain basic freedom to leave and seek better conditions.",
    "IMMG-LABS-0006": "No visa or work permit system can legally give a single employer total control over a worker's ability to remain in the country — that level of dependence enables exploitation.",
    "IMMG-LABS-0007": "Workers on employer-tied visas must be able to leave abusive or unsafe employers without immediately losing their legal status — some level of job portability is required.",
    "IMMG-LABS-0008": "Work authorization systems must include protections against trafficking, coercion, document confiscation, retaliation, and employers who manipulate immigration status as a tool of control.",
    "IMMG-LABS-0009": "Workers pursuing labor complaints, safety claims, or trafficking investigations must be shielded from immigration enforcement consequences while those proceedings are active.",
    "IMMG-LABS-0010": "Immigration labor pathways should be built around worker dignity, freedom to move between jobs, and fair bargaining — not just extracting labor from people with no other options.",
    "IMMG-LABS-0011": "The H-2A agricultural guest worker visa program must be reformed to give workers the right to organize, change employers, and live independently — not remain trapped in employer-controlled housing with no legal recourse.",

    # ── IMMG-OVRG  Oversight ─────────────────────────────────────────────────
    "IMMG-OVRG-0001": "Immigration agencies and detention facilities must be subject to real, independent oversight — with actual access to facilities, records, and decision-making patterns.",
    "IMMG-OVRG-0002": "Immigration agencies must publish clear, standardized data on detention, deportations, processing times, family separations, legal representation access, and rights complaints.",
    "IMMG-OVRG-0003": "When there are documented patterns of abuse, rights violations, discriminatory enforcement, or wrongful detention, mandatory corrective action and review must follow.",
    "IMMG-OVRG-0004": "Immigration officials and agencies cannot escape accountability by hiding behind secrecy, special legal processes, or fragmented responsibility spread across multiple agencies.",

    # ── IMMG-REFS  Refugees ──────────────────────────────────────────────────
    "IMMG-REFS-0001": "The United States should maintain a strong refugee resettlement program grounded in humanitarian responsibility, fair processes, and meaningful support for people rebuilding their lives.",
    "IMMG-REFS-0002": "Refugee admissions cannot be arbitrarily shut down through discriminatory exclusions, politically motivated freezes, or administrative sabotage of the resettlement system.",
    "IMMG-REFS-0003": "Refugee systems must have predictable, stable capacity — not be repeatedly dismantled and rebuilt based on political winds.",
    "IMMG-REFS-0004": "Who qualifies for refugee resettlement and how they are processed cannot be based on race, religion, national origin, sexual orientation, gender identity, political views, or other protected characteristics.",
    "IMMG-REFS-0005": "Refugee eligibility standards must be clear, transparent, and applied consistently — not manipulated based on political narratives or media attention.",
    "IMMG-REFS-0006": "Refugee resettlement must include real access to housing, healthcare, education, language support, legal help, and the resources people need to rebuild stable lives.",
    "IMMG-REFS-0007": "Refugee resettlement should coordinate with state and local institutions to support long-term integration — not leave refugees navigating confusing systems alone.",
    "IMMG-REFS-0008": "Refugees should have clear, accessible paths from initial arrival to permanent legal status and ultimately to citizenship, where appropriate.",
    "IMMG-REFS-0009": "Refugee resettlement functions cannot be structured in ways that give private organizations profit incentives over the rights and wellbeing of vulnerable people.",
    "IMMG-REFS-0010": "Refugee systems must be subject to strong public oversight, transparent data reporting, and anti-discrimination enforcement.",

    # ── IMMG-REMS  Removal / Deportation ────────────────────────────────────
    "IMMG-REMS-0001": "People cannot be deported to a country that isn't where they are from, haven't lived legally, or where their safety is not clearly established — it must be their actual home country or a place where they are safe.",
    "IMMG-REMS-0002": "No one can be deported to a country where they face a serious risk of persecution, torture, forced disappearance, trafficking, or other severe harm.",
    "IMMG-REMS-0003": "Deporting someone to a third country — one they weren't from or haven't lived in — requires strict legal standards, meaningful review, and proof that the person will be safe and lawfully admitted there.",
    "IMMG-REMS-0004": "Deportation proceedings must include proper notice, access to records, access to a lawyer, and enough time to challenge legal or factual errors before anyone is removed.",
    "IMMG-REMS-0005": "No one can be deported while a timely appeal, habeas petition, or other qualifying legal challenge is still pending — unless a court specifically orders it.",
    "IMMG-REMS-0006": "Deportation orders must be based on individual review — rushed, mass-processing systems that sacrifice accuracy for speed are not acceptable.",
    "IMMG-REMS-0007": "People facing deportation must have access to the full factual and legal basis for the government's case — including records, evidence, and the stated reasons for their removal.",
    "IMMG-REMS-0008": "The immigration system must have strong safeguards against wrongful deportation due to mistaken identity, record errors, citizenship errors, or failure to consider available legal defenses.",
    "IMMG-REMS-0009": "When credible evidence suggests a deportation may be unlawful, factually wrong, or a rights violation, removal must be paused while it is reviewed.",
    "IMMG-REMS-0010": "Wrongful deportation must trigger mandatory review, accountability investigation, and real remedies — including pathways for the person to return if they were wrongly removed.",
    "IMMG-REMS-0011": "Deportation decisions must consider family ties, caregiving responsibilities, disability, medical needs, and other serious humanitarian factors — these are not irrelevant details.",
    "IMMG-REMS-0012": "People cannot be deported in ways that deliberately cut off access to essential ongoing medical treatment without legal review and a safe medical transition plan.",
    "IMMG-REMS-0013": "Deportation cases involving children, families, people with disabilities, or medically vulnerable individuals require heightened review and extra safeguards.",
    "IMMG-REMS-0014": "Government agencies must publicly report standardized data on deportations, appeals, legal stays, wrongful-removal findings, and the countries people are sent to.",
    "IMMG-REMS-0015": "Expedited or summary deportation procedures — where people are removed very quickly with minimal review — must be tightly limited and cannot be used in ways that eliminate due process or humanitarian protections.",
    "IMMG-REMS-0016": "The transport and transfer of people being deported must be documented, auditable, and reviewable to prevent disappearance, abuse, or unlawful handoffs to other countries.",

    # ── IMMG-RGTS  Rights ────────────────────────────────────────────────────
    "IMMG-RGTS-0001": "Immigration policy must respect human rights, due process, family integrity, and equal dignity — while also maintaining lawful, orderly systems.",
    "IMMG-RGTS-0002": "Immigration systems cannot use cruelty, humiliation, indefinite limbo, or systematic fear as tools to deter people from seeking protection or legal status.",
    "IMMG-RGTS-0003": "Immigration law and how it is administered must be clear, consistent, transparent, and resistant to political manipulation or enforcement that changes based on who is in power.",
    "IMMG-RGTS-0004": "Where someone lives, what language they speak, how much money they have, or whether they can afford a lawyer cannot determine whether they can meaningfully navigate the immigration process.",
    "IMMG-RGTS-0005": "Immigration policy, enforcement, and court decisions cannot discriminate based on race, religion, sexual orientation, sex, gender identity, political views, or other protected characteristics.",
    "IMMG-RGTS-0006": "Immigration rules and processes must be written and applied consistently and neutrally — they cannot be structured in ways that produce discriminatory outcomes even if they don't say so explicitly.",
    "IMMG-RGTS-0007": "Selectively targeting people for immigration enforcement based on their race, religion, political views, or other protected characteristics is prohibited.",
    "IMMG-RGTS-0008": "The United States cannot create separate, reduced-rights legal systems for non-citizens that undermine equal protection principles guaranteed by the Constitution.",
    "IMMG-RGTS-0009": "Immigration status can affect specific legal outcomes, but it cannot be used to strip anyone of fundamental rights protections or basic legal dignity.",

    # ── IMMG-SLXS  Sanctuary / Local ────────────────────────────────────────
    "IMMG-SLXS-0001": "Local governments and communities have the right to adopt sanctuary policies — limiting their participation in federal immigration enforcement — to protect the safety and trust of their residents.",
    "IMMG-SLXS-0002": "The federal government cannot use funding threats or penalties to coerce cities and counties into becoming enforcement arms of the immigration system against their communities' wishes.",

    # ── IMMG-SRVS  Services ──────────────────────────────────────────────────
    "IMMG-SRVS-0001": "People in the United States must be able to get emergency medical care and necessary stabilization regardless of their immigration status.",
    "IMMG-SRVS-0002": "Seeking emergency care or medically necessary treatment cannot trigger immigration enforcement against the person seeking help, except in the narrowest possible circumstances.",
    "IMMG-SRVS-0003": "Immigration status cannot be used to deny medically necessary care to children, pregnant people, people with disabilities, or other vulnerable populations the law protects.",
    "IMMG-SRVS-0004": "Children must be able to attend public school without immigration authorities treating schools as enforcement zones or using school enrollment data to track families.",
    "IMMG-SRVS-0005": "Schools and educational institutions cannot be converted into routine immigration enforcement access points — education must remain a safe zone.",
    "IMMG-SRVS-0006": "Children's access to schooling and learning should not be undermined by immigration-related fear that keeps families away from schools.",
    "IMMG-SRVS-0007": "Healthcare, schools, shelters, and other essential services should have clear limits on immigration enforcement access so people can seek help without constant fear of deportation.",
    "IMMG-SRVS-0008": "Routinely using hospitals, schools, shelters, labor agencies, and service providers as covert immigration enforcement access points is prohibited.",
    "IMMG-SRVS-0009": "Public institutions must provide clear, multilingual information about which services are safe to access and what information can and cannot be shared with immigration authorities.",
    "IMMG-SRVS-0010": "When immigration status affects eligibility for specific benefits, the rules must be clear, consistently applied, and not used as tools of confusion, deterrence, or humiliation.",
    "IMMG-SRVS-0011": "Benefit systems cannot use confusing status rules, contradictory paperwork demands, or hidden information-sharing practices to quietly exclude people who are entitled to services.",
    "IMMG-SRVS-0012": "Children, mixed-status families, and other vulnerable households must be clearly protected from losing access to lawful services because of fear or household immigration complexity.",
    "IMMG-SRVS-0013": "Federal law must establish protected zones where civil immigration enforcement is prohibited — including schools, hospitals, churches, courthouses, and shelters.",

    # ── IMMG-STSS  Status / Legalization ─────────────────────────────────────
    "IMMG-STSS-0001": "Immigration policy should provide realistic paths to legal status for long-term residents with community ties — keeping people in permanent, precarious undocumented status is a policy choice, not an inevitability.",
    "IMMG-STSS-0002": "The process for adjusting or obtaining immigration status should be clear, affordable, and navigable — not blocked by excessive bureaucracy or arbitrary delays.",
    "IMMG-STSS-0003": "People who were brought to the U.S. as children or grew up here should have strong, permanent pathways to legal status and citizenship.",
    "IMMG-STSS-0004": "Immigration law should reduce long-term undocumented limbo by expanding workable legal pathways and addressing the backlogs that keep millions of people in legal uncertainty.",
    "IMMG-STSS-0005": "Who gets to adjust their status should consider family unity, work contributions, how long someone has lived here, and humanitarian factors — not just focus on penalties and exclusions.",
    "IMMG-STSS-0006": "The overall visa, green card, and permanent-residence system must be comprehensively reformed to reduce delays, arbitrariness, complexity, and structural unfairness.",
    "IMMG-STSS-0007": "Visa and permanent-residence systems should be simplified and made consistent so people aren't trapped in excessive bureaucracy, backlogs, and legal uncertainty.",
    "IMMG-STSS-0008": "Application fees and procedural requirements for visas and green cards should not be set so high that ordinary applicants are effectively excluded from applying.",
    "IMMG-STSS-0009": "Backlogs for family-based, employment-based, and humanitarian immigration must be reduced through real structural reform — not just short-term administrative fixes.",
    "IMMG-STSS-0010": "Legal status systems must include clearer timelines, transparent processes, and predictable adjudication standards so applicants aren't left in prolonged uncertainty about their future.",
    "IMMG-STSS-0011": "Status pathways must be designed to reduce situations where people's immigration status is entirely controlled by their employer, their spouse, or an arbitrary gatekeeper.",
    "IMMG-STSS-0012": "People stuck in long-term temporary-status limbo should have pathways to permanent status when their ties, residence, and contributions clearly justify it.",
    "IMMG-STSS-0013": "Temporary Protected Status — which allows people from certain countries to stay in the U.S. during crises — must be made permanent in law, with a clear path to citizenship for long-term holders.",
    "IMMG-STSS-0014": "A broad pathway to citizenship must be available that doesn't require people to be wealthy — no means testing or public charge history should block eligibility.",

    # ── IMMG-SYSR  System Reform ─────────────────────────────────────────────
    "IMMG-SYSR-0001": "Legal immigration pathways should be designed so that people can realistically comply with them — when legal options are too difficult or expensive, it drives people toward undocumented status.",
    "IMMG-SYSR-0002": "Immigration policy should be measured by how well it reduces fear, opacity, exploitation, and legal limbo — not just by how many people it detains or deports.",
    "IMMG-SYSR-0003": "Immigration systems must be evaluated on rights compliance, fairness, stability, and human outcomes — not only on enforcement numbers.",
    "IMMG-SYSR-0004": "Any future immigration reforms must be tested against principles of anti-abuse, anti-exploitation, and anti-fragmentation before they are implemented.",

    # ── IMMG-TRFS  Trafficking ───────────────────────────────────────────────
    "IMMG-TRFS-0001": "Immigration systems must include strong protections for trafficking and labor exploitation survivors — these people must never be forced to choose between reporting their abuse and risking deportation.",
    "IMMG-TRFS-0002": "People who report trafficking or forced labor must be protected from retaliatory detention or deportation while their claims are being investigated.",
    "IMMG-TRFS-0003": "Protections for trafficking survivors in the immigration system must be genuinely accessible — not buried behind narrow eligibility rules, discretionary barriers, or proof demands that are impossible to meet.",
    "IMMG-TRFS-0004": "Immigration and labor enforcement agencies must work together to identify employer-controlled visa arrangements that enable trafficking or status-based exploitation.",
    "IMMG-TRFS-0005": "Survivors of trafficking and severe exploitation should have durable, realistic pathways to safety, protection, and legal status.",

    # ── IMMG-VISS  Visas ─────────────────────────────────────────────────────
    "IMMG-VISS-0001": "Visa categories and legal entry pathways should be modernized to reduce arbitrary complexity, better reflect how people actually live and work, and cut unnecessary uncertainty.",
    "IMMG-VISS-0002": "Immigration pathways should be structured to reduce extreme wait times, backlogs, and bottlenecks that make lawful migration impractical for millions of people.",
    "IMMG-VISS-0003": "Green card and permanent-residence systems should have predictable timelines and transparent queue information so people know where they stand.",
    "IMMG-VISS-0004": "People applying for visas, green cards, and permanent residence must have meaningful access to their case status, file contents, and explanations for any delays or denials.",
    "IMMG-VISS-0005": "Application requirements should be simplified and standardized to reduce unnecessary legal expense, duplicative paperwork, and procedural traps.",
    "IMMG-VISS-0006": "Fees for visas, green cards, and permanent residence must be regulated so they don't function as wealth barriers that price out ordinary people.",
    "IMMG-VISS-0007": "Family-based and humanitarian immigration pathways should not be treated as less important than employer-sponsored pathways in ways that undermine family unity or human dignity.",
    "IMMG-VISS-0008": "Long-term residents with stable ties should have realistic pathways from temporary or uncertain status to permanent legal residence.",
    "IMMG-VISS-0009": "Immigration pathways should be stable enough that people aren't destabilized by sudden policy reversals or inconsistent adjudication standards that change between administrations.",
    "IMMG-VISS-0010": "The entire visa system must be modernized to reduce arbitrariness, backlog, complexity, and vulnerability to abuse — while preserving lawful, orderly migration.",
    "IMMG-VISS-0011": "Visa categories should be simplified and clarified so that applicants can understand their options without requiring expensive legal expertise to decode.",
    "IMMG-VISS-0012": "Overlapping or contradictory visa rules should be cleaned up to prevent arbitrary denials, inconsistent decisions, and needless procedural traps.",
    "IMMG-VISS-0013": "Visa pathways should reflect real family relationships, humanitarian needs, educational realities, and labor markets — not outdated assumptions or artificial scarcity created by bureaucratic inertia.",
    "IMMG-VISS-0014": "Visa processing must operate under clear target timelines with public reporting on delays, backlogs, and queue movement so people can plan their lives.",
    "IMMG-VISS-0015": "Applicants must be able to see real-time updates on their case and receive clear, understandable explanations for any delay, request for additional documents, or denial.",
    "IMMG-VISS-0016": "Letting cases sit unresolved for years cannot be used as a way to effectively deny applications without officially saying no.",
    "IMMG-VISS-0017": "Standards for visa adjudications must be clear and consistent — excessive, unchecked officer discretion produces arbitrary outcomes and is not a fair system.",
    "IMMG-VISS-0018": "Requests for additional documents or proof in visa cases must be proportional and tied to legitimate adjudication needs — not used as bureaucratic tools to stall or wear down applicants.",
    "IMMG-VISS-0019": "Applicants must have a meaningful chance to correct errors, add missing records, and respond to concerns before a final adverse decision is made.",
    "IMMG-VISS-0020": "Employment-based visa systems must reduce total employer control over workers — employees must be able to leave abusive situations or change jobs without immediately losing their legal status.",
    "IMMG-VISS-0021": "Student and trainee visa systems must protect against exploitation, confusion about status requirements, and arbitrary disruptions of lawful educational pathways.",
    "IMMG-VISS-0022": "Temporary visa programs should not trap people in prolonged precarious status when their long-term presence and contributions clearly justify a path to permanence.",
    "IMMG-VISS-0023": "Family-based visa systems should prioritize reuniting families and reduce the needless backlogs and procedural complexity that keep families apart for years.",
    "IMMG-VISS-0024": "Family-based applicants should not face excessive documentary or procedural burdens that block ordinary families from using the lawful pathways available to them.",
    "IMMG-VISS-0025": "Visa fees must be set at levels that cover legitimate administrative costs — not so high that they become exclusionary wealth filters.",
    "IMMG-VISS-0026": "Fee waivers, reductions, or public assistance should be available when the cost of applying for a visa would otherwise make lawful immigration practically inaccessible.",
    "IMMG-VISS-0027": "Visa systems must include clear mechanisms for people to move from temporary status to permanent residence when their residence, contributions, and stability justify it.",
    "IMMG-VISS-0028": "People should not be forced into endless cycles of temporary renewals when a permanent lawful path is more appropriate and makes more administrative sense.",
    "IMMG-VISS-0029": "People already in lawful immigration processes must be protected from sudden policy reversals that unfairly destabilize their pending or nearly complete applications.",
    "IMMG-VISS-0030": "Major changes to visa systems must include transition rules that protect people who were relying on existing rules — abrupt changes that upend lawful applicants and families are not acceptable.",

    # ── IMMI-ASYL  Asylum (IMMI domain) ─────────────────────────────────────
    "IMMI-ASYL-0001": "The U.S. must fully restore asylum processing at all ports of entry, repeal rules that bar asylum based on how someone entered the country, and guarantee every asylum seeker a full, fair hearing.",
    "IMMI-ASYL-0002": "The immigration court backlog must be eliminated by immediately hiring 2,000 more immigration judges, providing full funding, and converting immigration courts into an independent federal court.",
    "IMMI-ASYL-0003": "Congress must restore full access to the asylum system — repealing transit bars, metering policies, and Remain-in-Mexico-style programs — and fund enough immigration courts to process all asylum claims within one year.",

    # ── IMMI-DACA  DACA / Dreamers (IMMI) ───────────────────────────────────
    "IMMI-DACA-0001": "Congress must pass the Dream Act to give permanent legal status, work authorization, and a path to citizenship to all DACA recipients and other qualifying people who came to the U.S. as children.",
    "IMMI-DACA-0002": "Temporary Protected Status must be written into law with clear renewal standards, and anyone who has held TPS for five or more years must have a pathway to permanent residence.",
    "IMMI-DACA-0003": "Congress must immediately pass permanent legal status and a clear citizenship pathway for all DACA recipients and everyone who arrived in the U.S. before age 18 — no more delays, conditions, or political hostage-taking.",

    # ── IMMI-DETX  Detention (IMMI) ─────────────────────────────────────────
    "IMMI-DETX-0001": "Using family separation as an immigration enforcement tool is permanently prohibited — the government cannot separate children from their parents to deter people from seeking protection.",
    "IMMI-DETX-0002": "Immigration detention facilities cannot be run by private, for-profit companies — locking people up should never be a business model.",
    "IMMI-DETX-0003": "All immigration detention facilities must meet basic humane standards for healthcare, sanitation, safety, and legal access — and be subject to regular independent oversight.",

    # ── IMMI-ENFO  Enforcement (IMMI) ───────────────────────────────────────
    "IMMI-ENFO-0001": "ICE agents must wear body cameras during all enforcement operations, obtain a court-issued warrant before arresting anyone for civil immigration violations, and end the practice of deputizing local police as immigration enforcers.",

    # ── IMMI-ENFT  Local Enforcement ─────────────────────────────────────────
    "IMMI-ENFT-0001": "Local and state police cannot perform federal immigration enforcement duties — immigration enforcement is a federal responsibility, and mixing it with local policing undermines community trust and safety.",

    # ── IMMI-FMLY  Family Visas (IMMI) ──────────────────────────────────────
    "IMMI-FMLY-0001": "The massive backlog of family-based immigration applications must be cleared within 10 years by increasing annual visa allocations to 500,000 and recovering all unused visas from prior years.",

    # ── IMMI-ICRF  Independent Courts ───────────────────────────────────────
    "IMMI-ICRF-0001": "Immigration courts must be established as independent federal courts whose judges have job protections and cannot be fired or pressured based on how they rule.",
    "IMMI-ICRF-0002": "Every person facing deportation must have the right to a government-appointed lawyer at government expense if they cannot afford one.",
    "IMMI-ICRF-0003": "No one can be deported without a hearing before an immigration judge — regardless of how recently they arrived or where in the country they were encountered.",

    # ── IMMI-LABR  Labor (IMMI) ──────────────────────────────────────────────
    "IMMI-LABR-0001": "The H-2A agricultural visa program must be reformed to end employer-tied restrictions that enable labor trafficking, give workers the right to change employers without losing status, and apply all federal labor laws to agricultural guest workers.",
    "IMMI-LABR-0002": "All federal labor laws must be explicitly extended to all workers regardless of immigration status — and it must be a federal crime for any employer to threaten immigration enforcement against a worker who files a complaint or joins a union.",
    "IMMI-LABR-0003": "Domestic workers — including nannies, home care workers, and house cleaners — must receive full labor law protections, and a federal Domestic Worker Bill of Rights must establish minimum contract standards and dedicated enforcement.",

    # ── IMMI-RFGE  Refugees (IMMI) ───────────────────────────────────────────
    "IMMI-RFGE-0001": "The U.S. must immediately restore the annual refugee admissions ceiling to 125,000, commit to reaching 200,000 admissions per year within five years, and fully fund the resettlement infrastructure to meet those commitments.",
    "IMMI-RFGE-0002": "Congress must set the annual refugee admissions ceiling at a minimum of 125,000, streamline processing to eliminate multi-year delays, and stop using refugee admissions as a political bargaining chip.",

    # ═════════════════════════════════════════════════════════════════════════
    # TAXN — Taxation and Wealth
    # ═════════════════════════════════════════════════════════════════════════

    # ── TAXN-ADML  Tax Administration ────────────────────────────────────────
    "TAXN-ADML-0001": "The IRS should use modern technology to make filing taxes simpler for ordinary people — while also using that technology to better catch complex tax cheating by corporations and the wealthy.",
    "TAXN-ADML-0002": "Automated IRS systems must be transparent and subject to human review — people must be able to see how they work and challenge decisions made by algorithms.",
    "TAXN-ADML-0003": "Modernizing the IRS must prioritize making filing easier for regular taxpayers and improving fraud detection — not just upgrading internal systems.",
    "TAXN-ADML-0004": "IRS Direct File — the free government tax filing tool — must be made permanent and expanded to all 50 states so every taxpayer can file for free directly with the IRS.",
    "TAXN-ADML-0005": "For workers who only receive a W-2 wage, the IRS should pre-fill their return using data it already has — so filing taxes becomes as simple as checking and confirming, not starting from scratch.",

    # ── TAXN-AINL  AI & Labor Taxation ──────────────────────────────────────
    "TAXN-AINL-0001": "When companies use AI or automation to generate economic value, that value should contribute to public systems — just like wages paid to human workers do through payroll taxes.",
    "TAXN-AINL-0002": "Companies that replace large numbers of workers with machines or AI should pay into public systems to offset the cost their choices impose on those workers and their communities.",
    "TAXN-AINL-0003": "An AI tax applies when automation materially reduces the number of human workers at a company — it's not triggered by using automation for things humans weren't doing before.",
    "TAXN-AINL-0004": "Any tax on AI-driven labor displacement must be based on measurable, verifiable data — not estimates or assumptions that companies can easily manipulate.",
    "TAXN-AINL-0005": "Companies cannot escape AI labor taxes by reclassifying automated workers as contractors, outsourcing jobs, or restructuring on paper — the tax follows real economic displacement.",
    "TAXN-AINL-0006": "Companies cannot shift operations to other countries or subsidiaries to avoid paying AI-related taxes on labor displacement that happens in the U.S.",
    "TAXN-AINL-0007": "Revenue collected from AI and automation taxes should be used to help displaced workers retrain, find new jobs, and maintain their standard of living during the transition.",
    "TAXN-AINL-0008": "AI tax policy must be carefully designed to discourage reckless labor displacement while still allowing beneficial uses of technology that create new value and opportunities.",
    "TAXN-AINL-0009": "AI uses that genuinely improve safety, accessibility, or public benefit — like medical diagnostics or assistive technology — should be treated differently from AI used purely to cut labor costs.",
    "TAXN-AINL-0010": "Companies that have gained enormous market power or economic dominance through AI systems face additional obligations — their gains came partly from public infrastructure and should contribute back to it.",

    # ── TAXN-AUTS  Automation Tax ────────────────────────────────────────────
    "TAXN-AUTS-0001": "Companies that replace human workers with AI or automation should pay an 'AI worker tax' — a contribution to public systems that compensates for the payroll taxes and wages those workers would have paid.",
    "TAXN-AUTS-0002": "Revenue from AI and automation taxes should go toward supporting affected workers, funding public goods, and ensuring productivity gains are shared broadly — not just captured as corporate profit.",
    "TAXN-AUTS-0003": "Automation taxes should be designed to discourage companies from eliminating jobs without social responsibility — and to ensure the gains from automation benefit everyone, not just shareholders.",

    # ── TAXN-BEPS  Profit Shifting ───────────────────────────────────────────
    "TAXN-BEPS-0001": "Corporations must be taxed based on where they actually sell products, employ people, and operate — not just where their lawyers say they are 'headquartered' on paper.",
    "TAXN-BEPS-0002": "When companies charge their own subsidiaries for goods, services, or intellectual property, those prices must reflect actual market rates — not be inflated to shift profits to low-tax countries.",
    "TAXN-BEPS-0003": "Artificially routing profits to low-tax countries when the company does little or no real business there is tax avoidance — and must be treated as such.",

    # ── TAXN-CAPS  Capital Gains ─────────────────────────────────────────────
    "TAXN-CAPS-0001": "Money made from investments — like dividends, capital gains, and passive income — cannot be taxed at lower rates than money earned by working. A dollar of income is a dollar of income.",
    "TAXN-CAPS-0002": "Tax preferences for investment income that disproportionately benefit the wealthy — while people who work for wages pay higher rates — must be eliminated or reduced.",
    "TAXN-CAPS-0003": "Investment incentives that encourage genuinely productive long-term investment may be preserved — but only where they demonstrably serve a real public purpose.",
    "TAXN-CAPS-0004": "Capital gains — profits from selling investments — must be taxed in a way that does not allow the wealthy to systematically pay lower rates than people who earn wages.",
    "TAXN-CAPS-0005": "At extreme levels of wealth, gains on investments that haven't been sold yet — called 'unrealized gains' — may be subject to annual taxation, since waiting until sale allows decades of untaxed accumulation.",
    "TAXN-CAPS-0006": "The 'stepped-up basis' rule allows inherited assets to pass between generations tax-free on gains that occurred during the original owner's lifetime — this loophole must be closed.",
    "TAXN-CAPS-0007": "Compensation that is effectively payment for personal work and effort cannot be reclassified as investment income just to take advantage of lower capital gains tax rates.",
    "TAXN-CAPS-0008": "Carried interest — a tax break that lets investment fund managers pay capital gains rates instead of income tax rates on their compensation — must be treated as ordinary income.",

    # ── TAXN-CARR  Carried Interest ──────────────────────────────────────────
    "TAXN-CARR-0001": "The 'carried interest loophole' — which lets hedge fund and private equity managers pay lower tax rates than their assistants — must be permanently closed. All compensation for managing other people's money must be taxed as ordinary income.",

    # ── TAXN-CDRS  Disclosure ────────────────────────────────────────────────
    "TAXN-CDRS-0001": "Presidential, vice-presidential, and federal candidates must publicly release at least five years of their federal tax returns as a condition of appearing on the ballot or taking office.",
    "TAXN-CDRS-0002": "Senior executive branch officials must disclose their tax returns annually while they serve in government — public office requires public financial transparency.",
    "TAXN-CDRS-0003": "Large corporations must publicly disclose how much profit they report and how much tax they pay in each country where they operate — so the public can see whether they're paying their fair share.",
    "TAXN-CDRS-0004": "Organizations that spend money to influence elections — often called 'dark money' groups — must disclose who their donors are when they engage in electoral activity.",

    # ── TAXN-CORS  Corporate Tax ─────────────────────────────────────────────
    "TAXN-CORS-0001": "Corporate tax rates must be high enough to prevent companies from effectively paying nothing by shuffling profits through subsidiaries in low-tax countries.",
    "TAXN-CORS-0002": "Corporate tax systems must be designed to close the loopholes that allow profitable corporations to pay little or nothing in taxes.",
    "TAXN-CORS-0003": "Corporations cannot use shell companies, internal royalty payments, or other accounting arrangements to move profits out of the U.S. and avoid taxes on them.",
    "TAXN-CORS-0004": "Corporate taxes must be based on where companies actually do business and generate revenue — not on where they file paperwork.",
    "TAXN-CORS-0005": "All corporations must pay a minimum effective tax rate — a floor — so that no profitable company can use deductions and credits to pay nothing.",
    "TAXN-CORS-0006": "When calculating whether a corporation has paid the minimum tax, the calculation must account for everything the company does globally — not just domestic operations.",

    # ── TAXN-CTCS  Child Tax Credit ──────────────────────────────────────────
    "TAXN-CTCS-0001": "The Child Tax Credit must be made fully refundable and universal — meaning families who don't owe income taxes still receive the full benefit for every child.",
    "TAXN-CTCS-0002": "Child allowance payments should be made monthly so families can count on regular support — not once a year at tax time when the money may already be needed.",
    "TAXN-CTCS-0003": "The child allowance must be set at a level high enough to meaningfully reduce child poverty, and it must automatically increase with inflation so its value doesn't erode over time.",
    "TAXN-CTCS-0004": "Families should not have to file a complex tax return to receive child allowance payments — enrollment should be automatic so no eligible child is left out due to paperwork barriers.",
    "TAXN-CTCS-0005": "Children should receive the full child allowance through age 17, and students who continue their education may be eligible for an extended benefit through age 21.",

    # ── TAXN-DEDS  Deductions ────────────────────────────────────────────────
    "TAXN-DEDS-0001": "Business tax deductions must be tied to real, legitimate business expenses — they cannot be used to artificially reduce taxable income by claiming personal, inflated, or unrelated expenses.",
    "TAXN-DEDS-0002": "Excessive executive pay packages — especially those structured to minimize taxes — cannot be written off as ordinary business expenses to the same extent they are now.",
    "TAXN-DEDS-0003": "Corporations may not use excessive interest deductions from debt — especially debt taken on primarily to reduce taxes — to dramatically lower their taxable income.",
    "TAXN-DEDS-0004": "Internal transactions within a company — like loans or royalty payments between parent companies and subsidiaries — must be structured around real economic value, not used to move income to lower-tax entities.",
    "TAXN-DEDS-0005": "Business transactions that have no real economic purpose other than reducing taxes must not be treated as legitimate deductions — substance over form matters.",

    # ── TAXN-DMJS  Democratic Legitimacy ────────────────────────────────────
    "TAXN-DMJS-0001": "Tax policy must be written and enforced so that no wealthy individual, corporation, or politically connected actor can routinely get a better effective tax rate than ordinary working people.",
    "TAXN-DMJS-0002": "The legitimacy of the tax system depends on people being able to see that it works fairly — a system where the rich clearly pay less than they should breeds justified cynicism.",
    "TAXN-DMJS-0003": "The tax system must be visibly fair in practice — not just theoretically fair on paper while systematically delivering different outcomes for the well-connected versus everyone else.",
    "TAXN-DMJS-0004": "Simplicity, fairness, and enforceability are equally important goals for tax policy — a system that is simple but unfair, or fair but unenforceable, fails the public.",

    # ── TAXN-EITC  Earned Income Tax Credit ─────────────────────────────────
    "TAXN-EITC-0001": "The Earned Income Tax Credit — a tax benefit for working people with lower incomes — must be expanded and doubled, and extended to workers without children and to all eligible age groups.",
    "TAXN-EITC-0002": "The EITC's 'marriage penalty' — where two working people receive less credit after marrying than they did individually — must be eliminated.",

    # ── TAXN-ENFL  Enforcement ───────────────────────────────────────────────
    "TAXN-ENFL-0001": "The IRS must be fully funded and staffed to audit high-income filers and corporations at the same rates as working-class filers — right now, wealthy taxpayers are audited far less than low-income ones.",
    "TAXN-ENFL-0002": "Repeated, willful, or large-scale tax evasion must trigger serious criminal penalties, not just fines — treating tax fraud as a cost of doing business sends the wrong message.",
    "TAXN-ENFL-0003": "IRS audit resources and investigations must prioritize large-scale tax evasion, which costs the public hundreds of billions of dollars annually — not primarily target low-income filers.",
    "TAXN-ENFL-0004": "Accountants, lawyers, and financial advisers who facilitate tax fraud or help design abusive tax schemes must face real consequences — not just their clients.",
    "TAXN-ENFL-0005": "Tax enforcement must focus on large corporations and complex financial structures — not continue the current pattern of auditing working-class families at higher rates than the wealthy.",
    "TAXN-ENFL-0006": "Law firms, accounting firms, and other professional enablers of corporate tax avoidance must face regulatory consequences for designing or marketing schemes that cross into illegality.",
    "TAXN-ENFL-0007": "Corporations that repeatedly or on a large scale avoid taxes must face escalating consequences — not just quiet settlements that make avoidance cheaper than compliance.",
    "TAXN-ENFL-0008": "Corporations cannot use litigation delays, procedural maneuvers, and appeals to indefinitely postpone tax enforcement — there must be reasonable limits on delay tactics.",
    "TAXN-ENFL-0009": "Simplifying taxes for ordinary people and rigorously enforcing taxes on the wealthy and corporations are not competing goals — they must both be pursued together.",
    "TAXN-ENFL-0010": "IRS enforcement resources must be allocated based on where the biggest tax gaps are — and the data consistently shows those gaps are at the top of the income scale, not the bottom.",

    # ── TAXN-ENFO  IRS Enforcement (ENFO) ───────────────────────────────────
    "TAXN-ENFO-0001": "The IRS must be fully funded to audit wealthy taxpayers at the rates seen before 2010, the $600 billion annual gap between taxes owed and taxes paid must be closed, and criminal tax fraud by high-income filers must be prosecuted just as seriously as other crimes.",

    # ── TAXN-ENVS  Environmental Taxation ───────────────────────────────────
    "TAXN-ENVS-0001": "Tax policy must make companies pay for the environmental harm they cause — instead of letting them dump those costs onto the public, future generations, and nature.",
    "TAXN-ENVS-0002": "Environmental taxes must be designed to actually reduce pollution, not just generate revenue while allowing harm to continue unchecked.",
    "TAXN-ENVS-0003": "Environmental taxes and fees cannot be used as a license to pollute — paying a tax does not give a company the right to cause unlimited environmental damage.",
    "TAXN-ENVS-0004": "Carbon-intensive activities — like burning fossil fuels — may be subject to direct taxation based on the amount of carbon they emit.",
    "TAXN-ENVS-0005": "Environmental tax systems must rely on verified, independently audited emissions and pollution data — not company self-reporting that cannot be independently confirmed.",
    "TAXN-ENVS-0006": "Carbon pricing or equivalent environmental taxation must be comprehensive — it cannot be designed with so many exemptions that it fails to actually reduce emissions.",
    "TAXN-ENVS-0007": "Environmental taxes must distinguish between pollution that is truly unavoidable versus pollution that comes from prioritizing profit over cleaner alternatives that already exist.",
    "TAXN-ENVS-0008": "Large-scale extraction of water from rivers, aquifers, and other sources may be subject to taxation or fees to reflect the true cost of depleting shared public resources.",
    "TAXN-ENVS-0009": "Water-related taxes and pricing policies must account for local conditions — drought-stricken areas and water-abundant areas require different approaches.",
    "TAXN-ENVS-0010": "Large-scale industrial water use — by factories, agricultural operations, or data centers — may be subject to fees that reflect its impact on water availability for communities.",
    "TAXN-ENVS-0011": "Water taxation and fee systems must not undermine access to clean drinking water for households and communities — affordability and basic access must be protected.",
    "TAXN-ENVS-0012": "Polluting activities and the release of persistent toxic chemicals may be subject to taxes and fees that reflect the long-term cost of contamination.",
    "TAXN-ENVS-0013": "Tax and fee systems may be used to discourage harmful pollution and encourage cleaner alternatives — making it more expensive to pollute than to clean up operations.",
    "TAXN-ENVS-0014": "Environmental taxes must account for the full lifecycle harm of a product or activity — including how it is produced, used, and disposed of — not just its immediate emissions.",
    "TAXN-ENVS-0015": "Tax policy should incentivize making products that last longer, are easier to repair, and generate less waste — rewarding durability over disposability.",
    "TAXN-ENVS-0016": "Tax advantages may be offered to support repair businesses, refurbishment services, and reuse industries as part of a strategy to reduce waste and extend product lifetimes.",
    "TAXN-ENVS-0017": "Tax policy may impose higher costs on disposable, non-repairable, or short-lived products that generate excessive waste — making the true environmental cost visible in the price.",
    "TAXN-ENVS-0018": "Environmental tax systems must include strong anti-evasion rules — companies cannot use accounting tricks, legal structures, or offshore arrangements to avoid paying environmental obligations.",
    "TAXN-ENVS-0019": "Corporations cannot use carbon credits, offsets, or other financial instruments to eliminate environmental tax obligations without actually reducing the pollution they cause.",
    "TAXN-ENVS-0020": "Imports and cross-border supply chains may be subject to environmental border adjustments — charges that reflect the environmental cost of production in countries with lower standards.",
    "TAXN-ENVS-0021": "Revenue from environmental taxes should fund environmental cleanup, remediation, and restoration — not disappear into general budgets disconnected from the harm it addresses.",
    "TAXN-ENVS-0022": "Some environmental tax revenue should also be used to offset the cost impact on low- and middle-income households — making sure the burden of environmental policy doesn't fall hardest on those who can least afford it.",
    "TAXN-ENVS-0023": "Environmental tax systems must be designed so that lower-income households are not disproportionately burdened — progressive design or rebates must be built in.",
    "TAXN-ENVS-0024": "Environmental tax systems must be transparent and publicly understandable — people should be able to see what is being taxed, at what rate, and why.",
    "TAXN-ENVS-0025": "Companies subject to environmental taxes must keep detailed, verifiable records and provide them to regulators — not just self-report and hope no one checks.",
    "TAXN-ENVS-0026": "Environmental tax enforcement must coordinate with environmental regulators so that tax obligations and environmental rules reinforce each other rather than operating in silos.",
    "TAXN-ENVS-0027": "Deliberate fraud, concealment, or knowing misreporting in environmental tax filings must be treated as serious violations — not just technical errors subject to minor penalties.",
    "TAXN-ENVS-0028": "Executives, auditors, and responsible individuals within companies that commit environmental tax fraud may be held personally liable — not just the company itself.",
    "TAXN-ENVS-0029": "Repeated or systematic environmental tax violations must trigger escalating penalties, heightened oversight, and if necessary, loss of operating permits or other business licenses.",
    "TAXN-ENVS-0030": "Environmental taxation must work alongside — not replace — direct environmental regulation. Both tools are needed, and one cannot substitute for the other.",
    "TAXN-ENVS-0031": "Environmental taxes, fees, and incentives must be regularly reviewed and updated to reflect changes in technology, emissions data, and environmental conditions.",
    "TAXN-ENVS-0032": "Small businesses may receive proportional treatment or carveouts in environmental tax systems to avoid creating compliance burdens that fall disproportionately on smaller operators.",

    # ── TAXN-EQTS  Equal Pay ─────────────────────────────────────────────────
    "TAXN-EQTS-0001": "Equal pay and equal economic opportunity must be guaranteed regardless of race, gender, sexual orientation, disability, or other protected characteristics — pay discrimination is not just unfair, it's a tax policy issue too.",

    # ── TAXN-ESTS  Estate Tax ────────────────────────────────────────────────
    "TAXN-ESTS-0001": "When very large amounts of wealth pass from one generation to the next — through inheritance — those transfers must be taxed to prevent a small number of dynasties from accumulating permanent power over the economy.",
    "TAXN-ESTS-0002": "Estate and inheritance tax systems must be designed with meaningful rates and coverage — not riddled with so many exemptions and loopholes that they apply only on paper.",
    "TAXN-ESTS-0003": "Trusts, foundations, and other legal structures cannot be used to pass wealth between generations indefinitely while avoiding estate and inheritance taxes.",

    # ── TAXN-EXTS  Stock Buybacks / Extraction ───────────────────────────────
    "TAXN-EXTS-0001": "When corporations use profits to buy back their own stock — enriching shareholders without creating jobs or new products — those buybacks may be taxed or limited since they don't contribute to the broader economy.",
    "TAXN-EXTS-0002": "Tax policy must not give preferential treatment to financial engineering and short-term extraction of corporate value over real productive investment.",

    # ── TAXN-FSUB  Fossil Fuel Subsidies ────────────────────────────────────
    "TAXN-FSUB-0001": "Oil and gas companies can currently deduct the cost of drilling as a business expense immediately — this special tax break must be repealed so fossil fuel companies pay taxes like other businesses.",
    "TAXN-FSUB-0002": "Oil and gas companies can currently deduct a percentage of revenue from wells as they deplete — this 'percentage depletion' tax preference must be eliminated since it has no equivalent in other industries.",
    "TAXN-FSUB-0003": "Fossil fuel companies use a special accounting method called 'last-in, first-out' that lets them reduce their taxable profits — this tax advantage must be repealed for the oil and gas sector.",
    "TAXN-FSUB-0004": "Fossil fuel companies cannot claim accelerated tax depreciation on their capital equipment — this special advantage over other industries must end.",
    "TAXN-FSUB-0005": "Oil companies cannot claim credit for payments to foreign governments as if those payments were taxes — this foreign tax credit rule must be eliminated for the fossil fuel industry.",
    "TAXN-FSUB-0006": "A federal carbon price must apply to all fossil fuel combustion — making the environmental cost of carbon pollution visible in the price of oil, gas, and coal.",
    "TAXN-FSUB-0007": "All revenue recovered by repealing fossil fuel tax subsidies must go directly to funding the clean energy transition — not to other uses.",

    # ── TAXN-FTTS  Financial Transaction Tax ─────────────────────────────────
    "TAXN-FTTS-0001": "A small tax on financial transactions — like stock trades, bond trades, and derivatives — can discourage high-speed speculation that destabilizes markets while having minimal impact on ordinary long-term investors.",
    "TAXN-FTTS-0002": "Revenue from a financial transaction tax must be used for public investment, social insurance programs, or reducing the deficit — not simply offset other tax cuts for the wealthy.",
    "TAXN-FTTS-0003": "A financial transaction tax must be designed carefully so that it doesn't create undue burdens for ordinary retirement savers, pension funds, or small investors.",

    # ── TAXN-GBIS  Guaranteed Basic Income ──────────────────────────────────
    "TAXN-GBIS-0001": "Every person living in the U.S. should have access to a guaranteed minimum income floor — a basic level of financial security below which no one falls, regardless of employment status.",
    "TAXN-GBIS-0002": "People displaced from their jobs by automation, outsourcing, or economic disruption should automatically receive income support — not have to navigate a complex maze of applications.",
    "TAXN-GBIS-0003": "The enormous productivity gains generated by automation and AI should fund a broad social dividend — shared benefits for everyone, not just increased profits for shareholders.",
    "TAXN-GBIS-0004": "Building toward a universal income floor should start by strengthening existing programs — unemployment insurance, SNAP, disability benefits — as stepping stones toward broader coverage.",
    "TAXN-GBIS-0005": "Means-tested programs — those that cut off benefits sharply as income rises — must be redesigned to eliminate the 'welfare cliff' where earning more money can actually leave a family worse off.",

    # ── TAXN-GENL  General ───────────────────────────────────────────────────
    "TAXN-GENL-0001": "The overall tax system must be progressive — meaning those with higher incomes pay higher rates — and cannot shift a disproportionate share of the burden onto lower- and middle-income households.",

    # ── TAXN-GOVN  Governance ────────────────────────────────────────────────
    "TAXN-GOVN-0001": "The IRS and other tax agencies must be protected from regulatory capture — where industries or wealthy interests effectively take over the agencies meant to regulate them — as well as from political interference and deliberate underfunding.",
    "TAXN-GOVN-0002": "The revolving door between tax regulators and the industries they regulate — where officials leave government to work for the companies they once oversaw — must be restricted to prevent conflicts of interest.",

    # ── TAXN-HVNS  Tax Havens ────────────────────────────────────────────────
    "TAXN-HVNS-0001": "Individuals and corporations cannot escape U.S. tax obligations by moving money, profits, or assets to tax havens — places with very low tax rates — when there is no real economic activity there.",
    "TAXN-HVNS-0002": "The U.S. should impose strong rules to prevent corporations and wealthy individuals from using tax havens to avoid contributing to the public systems that support their wealth creation.",
    "TAXN-HVNS-0003": "Tax liability must follow who actually owns and controls assets and profits — not just whoever's name appears on a shell company or trust registered in a tax haven.",
    "TAXN-HVNS-0004": "Corporations that claim to be based offshore or report profits in low-tax countries must demonstrate genuine economic substance there — not just a mailbox address and a handful of employees.",
    "TAXN-HVNS-0005": "Extremely wealthy people who move their assets or legal residency to tax havens to avoid U.S. taxes must still pay taxes on the gains and income they accumulated while benefiting from U.S. systems.",
    "TAXN-HVNS-0006": "Anti-tax-haven rules must be targeted at abusive arrangements — they should not create burdens for ordinary people who live or work abroad or for legitimate international businesses.",
    "TAXN-HVNS-0007": "FATCA — the law requiring foreign banks to report American accounts — must be strengthened with escalating penalties and no exemptions for banks in allied countries.",

    # ── TAXN-INCS  Incentives ────────────────────────────────────────────────
    "TAXN-INCS-0001": "Tax incentives — special breaks given to encourage certain business behaviors — must be tied to measurable public benefits like affordable housing, fair wages, environmental performance, or durable investment.",
    "TAXN-INCS-0002": "Tax incentives cannot reward stock buybacks, financial manipulation, or short-term profit extraction — they exist to encourage behavior that benefits the public, not shareholders.",
    "TAXN-INCS-0003": "Public subsidies and tax advantages should favor businesses that create durable value, treat workers well, and invest in communities — not just those that maximize quarterly profits.",
    "TAXN-INCS-0004": "Corporate tax structures should reward genuine long-term investment and worker development — not financial engineering designed to extract value while minimizing tax.",
    "TAXN-INCS-0005": "Corporate tax incentives cannot reward offshoring jobs, suppressing wages, or evading environmental obligations — these behaviors harm the public good rather than serve it.",

    # ── TAXN-INDS  Industrial Policy ─────────────────────────────────────────
    "TAXN-INDS-0001": "The U.S. must develop a national manufacturing and industrial policy to strengthen domestic production and supply chains — leaving these entirely to market forces has created dangerous vulnerabilities.",
    "TAXN-INDS-0002": "Strategic industries vital to national security and economic resilience — like semiconductors, clean energy, and medical equipment — should receive targeted public investment and financing.",
    "TAXN-INDS-0003": "Critical supply chains must be diversified and resilient — the U.S. cannot be dependent on a single country or source for essential goods and materials.",
    "TAXN-INDS-0004": "The U.S. must develop a strategy for securing domestic and allied sources of rare earth minerals and other critical materials needed for clean energy and advanced technology.",
    "TAXN-INDS-0005": "Federal spending and contracts should prioritize domestically produced goods and materials — 'Buy America' requirements must be strengthened and enforced.",
    "TAXN-INDS-0006": "Industrial policy should support specific regions and manufacturing clusters — not just pour resources into already-thriving coastal cities — to spread economic opportunity more broadly.",
    "TAXN-INDS-0007": "Industrial policy should include support for worker-owned businesses and democratic enterprises — models that share profits and decision-making more broadly.",
    "TAXN-INDS-0008": "Investment in research and development — basic science, applied research, and technology development — is itself a form of industrial policy that creates long-term economic strength.",
    "TAXN-INDS-0009": "Trade policy must be aligned with industrial strategy — trade agreements should support domestic manufacturing and not undermine the industries the U.S. is trying to build.",
    "TAXN-INDS-0010": "Building a strong industrial workforce requires robust apprenticeship programs, vocational training, and manufacturing education pathways — these must be funded as part of industrial policy.",

    # ── TAXN-INSS  Insurance / AI ────────────────────────────────────────────
    "TAXN-INSS-0001": "AI systems cannot be used to deny, restrict, or reduce insurance coverage or claims without a real human reviewing and being accountable for the decision.",
    "TAXN-INSS-0002": "Human reviewers in insurance decisions must make genuinely independent judgments — they cannot simply rubber-stamp whatever an AI system recommends.",

    # ── TAXN-INTL  International Tax ─────────────────────────────────────────
    "TAXN-INTL-0001": "The U.S. should work with other countries to coordinate enforcement against tax havens, secrecy jurisdictions, and cross-border tax evasion — no country can solve this problem alone.",
    "TAXN-INTL-0002": "Trade relationships, banking access, sanctions, and diplomatic tools may be used to pressure countries that enable tax evasion by providing secrecy and minimal taxation.",
    "TAXN-INTL-0003": "Foreign policy and international treaty negotiations should support global tax transparency — making it harder for wealth to hide offshore.",
    "TAXN-INTL-0004": "The U.S. must implement the OECD global minimum corporate tax of 15%, and use a backstop mechanism to ensure U.S. companies pay that minimum even if other countries don't.",

    # ── TAXN-LOPS  Loopholes ─────────────────────────────────────────────────
    "TAXN-LOPS-0001": "Tax provisions whose primary purpose is enabling the wealthy and corporations to avoid, defer, or artificially reduce their taxes — without providing corresponding public benefit — must be eliminated.",
    "TAXN-LOPS-0002": "Corporate tax law must be regularly reviewed to identify and close new loopholes as they emerge — wealthy interests continuously find new ways to exploit the tax code.",

    # ── TAXN-LVTS  Land Value Tax ────────────────────────────────────────────
    "TAXN-LVTS-0001": "Land value taxation — a tax on the value of land itself, separate from buildings or improvements — can capture value created by public investment and community development, rather than rewarding landowners who simply sit on valuable property.",
    "TAXN-LVTS-0002": "A land value tax must exempt buildings and improvements on land — so that investing in and developing property is not penalized, only passive land speculation is.",
    "TAXN-LVTS-0003": "Holding land idle — sitting on vacant lots or undeveloped parcels in high-demand areas — should carry a higher tax burden since it withholds useful land from productive use.",

    # ── TAXN-OFSH  Offshore Tax ──────────────────────────────────────────────
    "TAXN-OFSH-0001": "U.S. corporations must pay a minimum 21% tax on all profits regardless of where they are booked — country-by-country tax reporting must be made public — and all tax haven arrangements must be presumed abusive unless the company can prove they reflect genuine economic activity.",

    # ── TAXN-PMTS  Progressive Marginal Tax ─────────────────────────────────
    "TAXN-PMTS-0001": "Federal income tax must apply steeply increasing rates on extreme income — people making tens of millions of dollars a year should pay a significantly higher marginal rate than the middle class.",
    "TAXN-PMTS-0002": "An alternative minimum tax must be maintained to prevent high-income earners from using deductions and credits to reduce their effective tax rate below a floor.",
    "TAXN-PMTS-0003": "The 'stepped-up basis' rule — which wipes out the tax owed on investment gains when someone dies and their heirs inherit the assets — must be eliminated or replaced.",

    # ── TAXN-RLEG  Religious Orgs (RLEG) ────────────────────────────────────
    "TAXN-RLEG-0001": "Religious organizations that publicly endorse or oppose political candidates must lose their tax-exempt status — using charitable status to influence elections is prohibited for all nonprofits.",
    "TAXN-RLEG-0002": "All religious organizations with over $500,000 in annual revenue must file public financial disclosures — large organizations that receive public tax benefits must be publicly accountable.",
    "TAXN-RLEG-0003": "The IRS must audit all religious organizations with over $25 million in annual revenue at least once every three years to ensure compliance with tax laws.",
    "TAXN-RLEG-0004": "Religious organizations must pay standard business taxes on commercial income that is unrelated to their actual religious mission — tax-exempt status is not a blanket business subsidy.",
    "TAXN-RLEG-0005": "Tax-exempt status must be revoked for any organization that uses its religious status as a tool to coerce, control, or financially exploit its members.",
    "TAXN-RLEG-0006": "Religious property tax exemptions must apply only to property actually used for religious purposes — not to commercial real estate, investments, or other assets held under a religious name.",

    # ── TAXN-RLGT  Religious Orgs (RLGT) ────────────────────────────────────
    "TAXN-RLGT-0001": "All religious organizations with over $1 million in annual revenue must file public financial disclosures like other nonprofits — and any religious organization that engages in partisan politics or endorses candidates must immediately lose its tax-exempt status.",

    # ── TAXN-SMBS  Small Business ────────────────────────────────────────────
    "TAXN-SMBS-0001": "Small businesses should receive subsidies, carveouts, or public support to help them provide healthcare coverage to their employees — healthcare requirements should not be a crushing burden on small employers.",

    # ── TAXN-SSCI  Social Security ───────────────────────────────────────────
    "TAXN-SSCI-0001": "The Social Security payroll tax currently stops applying to wages above about $168,000 — meaning wealthy earners pay a much lower percentage of their income into Social Security than everyone else. That cap must be eliminated.",
    "TAXN-SSCI-0002": "Revenue from taxes on AI and automation should supplement Social Security funding — as robots replace workers, the productivity gains should help sustain the retirement security those workers built.",
    "TAXN-SSCI-0003": "The Social Security minimum benefit — the guaranteed floor that protects the poorest retirees — must be substantially increased so that no one who worked their whole life retires in poverty.",
    "TAXN-SSCI-0004": "Years spent caring for children, elderly relatives, or people with disabilities should count toward Social Security benefits — unpaid caregiving is real work that deserves retirement credit.",
    "TAXN-SSCI-0005": "The retirement ages built into Social Security were not designed equally — workers in physically demanding jobs often cannot work as long as office workers. This inequity must be studied and addressed.",

    # ── TAXN-SUBS  Corporate Subsidies ──────────────────────────────────────
    "TAXN-SUBS-0001": "When corporations receive tax incentives tied to job creation promises, those incentives must include real clawback provisions — if the jobs don't materialize, the subsidy must be returned.",
    "TAXN-SUBS-0002": "Before approving major economic development subsidies, independent cost-benefit analysis must be required — taxpayers deserve to know whether the promised benefits are realistic.",
    "TAXN-SUBS-0003": "Federal economic development funds cannot be used to fuel bidding wars between states and cities competing to attract the same corporation — this raises corporate welfare costs without improving outcomes.",
    "TAXN-SUBS-0004": "Federal tax-exempt financing — a form of government subsidy — must not be used to fund professional sports stadiums that primarily benefit wealthy team owners.",
    "TAXN-SUBS-0005": "A mandatory federal registry of all state and local corporate subsidies must be created so that the public, researchers, and policymakers can see the true scale of corporate welfare.",

    # ── TAXN-SYSR  System Rules ──────────────────────────────────────────────
    "TAXN-SYSR-0001": "Tax policy must accomplish four things: raise revenue fairly, fund public goods, reduce dangerous inequality, and prevent the extraction of wealth from the society that made it possible.",

    # ── TAXN-TAXS  Anti-Wealth Hoarding ─────────────────────────────────────
    "TAXN-TAXS-0001": "Tax policy must actively prevent the hoarding of extreme wealth — allowing a small number of individuals to accumulate more wealth than they could spend in a thousand lifetimes concentrates power in ways that threaten democracy.",

    # ── TAXN-TRAN  Transparency ──────────────────────────────────────────────
    "TAXN-TRAN-0001": "The true owners of companies, trusts, and other asset-holding structures must be transparent to tax regulators — anonymous shell companies are a tool for hiding wealth and evading taxes.",
    "TAXN-TRAN-0002": "High-risk tax structures and large offshore holdings must be subject to enhanced disclosure requirements so regulators can identify and investigate potential evasion.",
    "TAXN-TRAN-0003": "Secrecy structures — like layered trusts and anonymous holding companies — that are designed primarily to hide who controls assets from tax authorities must be prohibited or sharply restricted.",
    "TAXN-TRAN-0004": "Large corporations must publicly report their revenue, profits, and taxes paid in every country where they operate — country-by-country reporting should be available to the public, not just regulators.",
    "TAXN-TRAN-0005": "Corporate ownership chains — including subsidiaries and holding companies — must be clearly disclosed so that regulators and the public can understand who ultimately owns and controls major businesses.",

    # ── TAXN-TVNG  Televangelist / Donation Fraud ────────────────────────────
    "TAXN-TVNG-0001": "Religious organizations that promise miraculous financial returns, healing, or supernatural benefits in exchange for donations must comply with consumer protection laws — and faith-based fundraising targeting elderly or financially vulnerable people must be subject to FTC oversight.",

    # ── TAXN-WLTH  Wealth Tax ────────────────────────────────────────────────
    "TAXN-WLTH-0001": "The U.S. must impose an annual wealth tax on net worth above $50 million — a small percentage tax each year on the total assets of the ultra-wealthy to begin addressing extreme inequality.",
    "TAXN-WLTH-0002": "When large amounts of wealth pass between generations through gifts or inheritance, the transfers must be taxed at rates high enough to actually reduce dynastic concentration — not just on paper.",
    "TAXN-WLTH-0003": "The stepped-up basis loophole — which allows investment gains to completely escape taxation when an heir inherits assets — must be permanently eliminated.",
    "TAXN-WLTH-0004": "The U.S. must aggressively enforce existing international tax compliance laws and expand them to end offshore tax evasion by the ultra-wealthy.",

    # ── TAXN-WTHS  Wealth Concentration ─────────────────────────────────────
    "TAXN-WTHS-0001": "Tax policy must more effectively reach concentrated wealth, investment gains, passive income, and other forms of non-labor wealth accumulation that current law taxes very lightly.",
    "TAXN-WTHS-0002": "Tax rules cannot systematically privilege people who accumulate wealth over people who earn wages — a tax system that taxes work more heavily than capital is both unfair and economically harmful.",
    "TAXN-WTHS-0003": "Extremely large accumulations of wealth may be subject to an annual wealth tax — a percentage of total net worth paid each year — to prevent runaway concentration of economic and political power.",
    "TAXN-WTHS-0004": "Tax systems must actively work to prevent extreme concentration of wealth — not just tax income, but address the growing gap in total assets held by the wealthiest few versus everyone else.",
    "TAXN-WTHS-0005": "Extremely large concentrations of wealth may be subject to additional tax mechanisms, beyond the income tax, designed specifically to address the destabilizing effects of oligarchic wealth.",
    "TAXN-WTHS-0006": "Wealth tax systems must include strong rules for valuing assets, preventing evasion, and enforcing compliance — a wealth tax without enforcement is not a real wealth tax.",
    "TAXN-WTHS-0007": "High-wealth individuals cannot use trusts, pass-through entities, or other legal structures to effectively escape wealth taxes while retaining control and benefit from their assets.",
    "TAXN-WTHS-0008": "Tax systems must apply heightened reporting requirements, enhanced audit rates, and stricter enforcement to very large concentrations of wealth — the higher the wealth, the more scrutiny.",
    "TAXN-WTHS-0009": "Artificially converting labor income — money earned by working — into capital income to take advantage of lower tax rates is tax avoidance and must be treated as such.",
    "TAXN-WTHS-0010": "Personal tax avoidance schemes that use complex entity structures to make income appear to come from a lower-taxed source must be treated as the avoidance they are.",
    "TAXN-WTHS-0011": "Dynasty trusts — legal structures that can hold wealth tax-free for many generations or even indefinitely — must be limited to a 50-year maximum term.",
    "TAXN-WTHS-0012": "GRATs — a tax planning technique that lets wealthy people transfer investment gains to heirs tax-free — must be reformed by requiring a meaningful minimum term and fixing the mortality discount rules exploited to eliminate taxes.",
    "TAXN-WTHS-0013": "Households with a net worth above $50 million must file annual asset disclosures with the IRS — extreme wealth must be visible to tax authorities to be properly taxed.",
}
# fmt: on


def update_database(plain_map: dict[str, str]) -> int:
    """Update plain_language in the positions table. Returns count updated."""
    conn = sqlite3.connect(DB_PATH)
    updated = 0
    with conn:
        for pos_id, text in plain_map.items():
            conn.execute(
                "UPDATE positions SET plain_language = ? WHERE id = ? AND (plain_language IS NULL OR plain_language = '')",
                (text, pos_id),
            )
            updated += conn.execute(
                "SELECT changes()"
            ).fetchone()[0]
    conn.close()
    return updated


def insert_rule_plain_into_html(html_path: Path, plain_map: dict[str, str]) -> int:
    """Insert <p class="rule-plain"> after <p class="rule-title"> for each card.
    Returns count of insertions made.
    """
    content = html_path.read_text(encoding="utf-8")
    count = 0

    for pos_id, plain_text in plain_map.items():
        # Match a card block that has this id= and doesn't already have rule-plain
        # The pattern looks for the card div, then rule-title, then rule-stmt
        pattern = re.compile(
            r'(id="' + re.escape(pos_id) + r'"[^>]*>.*?'
            r'<p class="rule-title">.*?</p>)'
            r'(\s*<p class="rule-stmt">)',
            re.DOTALL,
        )

        def make_replacement(m: re.Match, text: str = plain_text) -> str:
            return (
                m.group(1)
                + f'\n<p class="rule-plain">{text}</p>'
                + m.group(2)
            )

        new_content, n = pattern.subn(make_replacement, content)
        if n > 0:
            content = new_content
            count += n

    html_path.write_text(content, encoding="utf-8")
    return count


def main() -> None:
    immg_map = {k: v for k, v in PLAIN_LANGUAGE.items() if k.startswith(("IMMG-", "IMMI-"))}
    taxn_map = {k: v for k, v in PLAIN_LANGUAGE.items() if k.startswith("TAXN-")}

    print(f"Defined: {len(immg_map)} IMMG/IMMI entries, {len(taxn_map)} TAXN entries")

    # Update DB
    db_count = update_database(PLAIN_LANGUAGE)
    print(f"DB rows updated: {db_count}")

    # Update HTML
    immg_html_count = insert_rule_plain_into_html(IMMG_HTML, immg_map)
    print(f"immigration.html insertions: {immg_html_count}")

    taxn_html_count = insert_rule_plain_into_html(TAXN_HTML, taxn_map)
    print(f"taxation-and-wealth.html insertions: {taxn_html_count}")

    print("Done.")


if __name__ == "__main__":
    main()
