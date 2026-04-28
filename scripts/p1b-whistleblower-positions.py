#!/usr/bin/env python3
"""
P1-B: Add whistleblower (WBLS) subdomain and positions to 13 pillars.

Compliance target: KERN-0027 (whistleblower protection — employment-status-agnostic,
non-waivable, with specified enforcement actor).

Domains already covered: ADMN (WBLS), CRPT (WBLS), JUST (WHTS).
Domains thin but rated adequate: HLTH (one SCIS position).

This script adds a full WBLS subdomain with 4 positions per domain to:
    ANTR, CNSR, EDUC, ELEC, ENVR, GUNS, HOUS, IMMG, INFR, LABR,
    MDIA, RGHT, SCIS, TAXN, TERM

Run from repo root:
    python3 scripts/p1b-whistleblower-positions.py

Idempotent: skips domains where WBLS subdomain already exists.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "policy" / "catalog" / "policy_catalog_v2.sqlite"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %Human:%M:%S")

# Per-domain WBLS position data.
# Each entry: (short_title, full_statement, plain_language)
WBLS_POSITIONS: dict[str, list[tuple[str, str, str]]] = {
    "ANTR": [
        (
            "Antitrust whistleblower protection — scope and beneficiaries",
            "Any employee, contractor, agent, or consultant of a corporation, trade association, "
            "or government agency who reports anticompetitive practices, merger fraud, price-fixing, "
            "market allocation, bid rigging, monopolistic abuse, or violations of antitrust law to "
            "any federal or state authority must receive whistleblower protection regardless of "
            "employment status, citizenship, or the form of their reporting relationship.",
            "Anyone who reports illegal business practices — like companies fixing prices or "
            "blocking competition — is protected from losing their job or being punished, no matter "
            "how they're employed.",
        ),
        (
            "Anti-retaliation prohibition for antitrust reporters — private right of action with "
            "treble damages",
            "No employer, corporation, trade association, or government entity may retaliate "
            "against any person for reporting antitrust violations, cooperating with antitrust "
            "investigations, or providing information to the DOJ Antitrust Division, the FTC, or "
            "any state attorney general. Retaliation includes termination, demotion, reduced hours, "
            "harassment, blacklisting, or initiation of retaliatory litigation. Victims of "
            "retaliation have a private right of action with treble damages and mandatory "
            "attorney's fee awards.",
            "Companies can't fire, demote, or punish people for reporting anti-competitive "
            "behavior. If they do, the victim can sue and recover three times their actual damages, "
            "plus legal fees.",
        ),
        (
            "Enforcement of antitrust whistleblower protections — DOJ and FTC jurisdiction",
            "The DOJ Antitrust Division and FTC must each maintain whistleblower intake programs "
            "with structural independence from industry review. Retaliation complaints must be "
            "processed within 180 days. The enforcement actor for retaliation claims is the DOJ "
            "Civil Rights Division or the applicable state attorney general, structurally "
            "independent of the antitrust investigation itself.",
            "The Justice Department and the FTC each run protected reporting programs. If someone "
            "is retaliated against, they can file a complaint that must be handled within "
            "six months.",
        ),
        (
            "Antitrust whistleblower protections are non-waivable — no contract may abrogate",
            "Antitrust whistleblower protections may not be waived by any employment contract, "
            "nondisclosure agreement, arbitration clause, settlement agreement, or confidentiality "
            "provision. Any contractual term purporting to prohibit or penalize the reporting of "
            "antitrust violations to any government authority is void as against public policy.",
            "No contract — not an NDA, not an arbitration agreement, not a settlement — can take "
            "away your right to report price-fixing or other illegal business practices to the "
            "government.",
        ),
    ],
    "CNSR": [
        (
            "Consumer whistleblower protection — scope and beneficiaries",
            "Any person — including employees, contractors, consumers, or members of the public — "
            "who reports consumer fraud, deceptive trade practices, product safety violations, "
            "illegal debt collection, discriminatory lending, predatory pricing, or violations of "
            "consumer protection law to any federal or state authority must receive whistleblower "
            "protection regardless of employment status or citizenship.",
            "Anyone who reports fraud against consumers — whether they're an employee, contractor, "
            "or just a customer who found out about it — is protected from retaliation.",
        ),
        (
            "Anti-retaliation prohibition for consumer protection reporters",
            "No employer, corporation, or government entity may retaliate against any person for "
            "reporting consumer protection violations, cooperating with CFPB, FTC, or state "
            "attorney general investigations, or providing information in consumer fraud proceedings. "
            "Retaliation includes termination, demotion, blacklisting, harassment, or filing "
            "retaliatory civil or administrative claims. Retaliated persons have a private right "
            "of action with reinstatement, back pay, and attorney's fees.",
            "Companies can't punish anyone for reporting consumer fraud. Victims of retaliation "
            "can go to court and get their job back, lost wages, and legal fees paid.",
        ),
        (
            "CFPB and FTC as enforcement actors for consumer whistleblower retaliation",
            "The CFPB and FTC must maintain accessible, confidential intake channels for consumer "
            "whistleblower complaints. Retaliation complaints must be processed within 180 days. "
            "State attorneys general may exercise concurrent jurisdiction over retaliation claims "
            "within their states. The enforcement actor for retaliation complaints must be "
            "structurally independent of the consumer fraud investigation.",
            "The Consumer Financial Protection Bureau and the FTC each take confidential reports "
            "and must respond within six months. State attorneys general can also act.",
        ),
        (
            "Consumer whistleblower protections are non-waivable — void contract terms",
            "Consumer whistleblower protections may not be waived by any employment contract, "
            "nondisclosure agreement, arbitration clause, or confidentiality provision. Any "
            "contractual term that prohibits or penalizes the reporting of consumer protection "
            "violations to any government authority is void as against public policy and "
            "unenforceable in any proceeding.",
            "No NDA, arbitration clause, or settlement can take away your right to report "
            "consumer fraud to the government. Any contract that tries to do that is not valid.",
        ),
    ],
    "EDUC": [
        (
            "Education whistleblower protection — scope and beneficiaries",
            "Any teacher, school administrator, staff member, contractor, student, parent, or "
            "education researcher who reports civil rights violations, educational fraud, misuse "
            "of public education funds, academic misconduct, illegal discrimination in educational "
            "institutions, or violations of student data privacy law to any federal or state "
            "authority must receive whistleblower protection regardless of employment or enrollment "
            "status.",
            "Anyone in or around a school — teachers, students, parents, staff — who reports "
            "civil rights violations, fraud, or illegal discrimination is protected from "
            "punishment or retaliation.",
        ),
        (
            "Anti-retaliation prohibition for education reporters — includes students and parents",
            "No school, school district, educational institution, or government agency may "
            "retaliate against any person for reporting violations of education law or civil "
            "rights, cooperating with DOE Office of Inspector General or Office for Civil Rights "
            "investigations, or providing information in education fraud proceedings. Protections "
            "explicitly extend to students (including suspension, expulsion, or grade retaliation) "
            "and to parents (including denial of services). Private right of action available.",
            "Schools can't punish students, parents, or teachers for reporting wrongdoing. "
            "Retaliation includes bad grades, expulsion, firing, or denying services. "
            "Victims can sue.",
        ),
        (
            "DOE OIG and OCR as enforcement actors for education whistleblower retaliation",
            "The DOE Office of Inspector General and the Office for Civil Rights must each "
            "maintain accessible, confidential whistleblower intake channels. Retaliation "
            "complaints must receive an initial determination within 180 days. State education "
            "agencies receiving federal funds must adopt equivalent anti-retaliation procedures "
            "as a condition of federal funding.",
            "The Department of Education's inspector general and civil rights office each take "
            "confidential reports and must respond within six months. States that receive federal "
            "education funds must have the same protections.",
        ),
        (
            "Education whistleblower protections are non-waivable — void contract terms",
            "Education whistleblower protections may not be waived by any employment contract, "
            "enrollment agreement, nondisclosure agreement, or settlement. Any contractual term "
            "that prohibits or penalizes reporting of education law violations to any government "
            "authority is void as against public policy.",
            "No contract, enrollment agreement, or NDA can take away your right to report "
            "wrongdoing to education authorities. Any clause that tries is not enforceable.",
        ),
    ],
    "ELEC": [
        (
            "Election integrity whistleblower protection — scope and beneficiaries",
            "Any election worker, poll worker, election administrator, campaign staff member, "
            "voter registration worker, or government employee who reports voter suppression, "
            "election fraud, campaign finance violations, interference with voter registration, "
            "voting system tampering, or violations of election law to any federal or state "
            "authority must receive whistleblower protection regardless of employment status, "
            "party affiliation, or citizenship.",
            "Anyone involved in running or observing elections who reports voter suppression, "
            "fraud, or campaign finance violations is protected from retaliation — regardless "
            "of which party they work for.",
        ),
        (
            "Anti-retaliation prohibition for election integrity reporters",
            "No government entity, political party, campaign, or election authority may retaliate "
            "against any person for reporting violations of election law, cooperating with DOJ "
            "Civil Rights Division or FEC investigations, or providing information in election "
            "fraud proceedings. Retaliation includes termination, removal from election duties, "
            "threats, intimidation, or filing retaliatory criminal or civil claims. Private right "
            "of action available with attorney's fees.",
            "Election workers and campaign staff can't be fired, removed, or threatened for "
            "reporting election fraud or voter suppression. Victims can sue and recover costs.",
        ),
        (
            "DOJ Civil Rights Division and FEC as enforcement actors for election reporters",
            "The DOJ Civil Rights Division and the FEC must each maintain accessible, "
            "confidential intake channels for election integrity whistleblower complaints. "
            "Retaliation complaints must receive an initial determination within 90 days given "
            "the time-sensitive nature of electoral processes. State attorneys general may "
            "exercise concurrent jurisdiction.",
            "The Justice Department's Civil Rights Division and the Federal Election Commission "
            "each take confidential reports and must respond within 90 days. That's faster than "
            "other programs because elections are time-sensitive.",
        ),
        (
            "Election whistleblower protections are non-waivable — no political agreement "
            "may abrogate",
            "Election integrity whistleblower protections may not be waived by any employment "
            "contract, party agreement, confidentiality provision, or settlement. Any agreement "
            "purporting to prohibit or penalize the reporting of election law violations to any "
            "government authority is void as against public policy.",
            "No employment contract or party agreement can stop someone from reporting election "
            "fraud or voter suppression to the government. Any such agreement is not valid.",
        ),
    ],
    "ENVR": [
        (
            "Environmental whistleblower protection — scope and beneficiaries",
            "Any person — including employees, contractors, agency scientists, agricultural "
            "workers, or members of the public — who reports violations of environmental law, "
            "agricultural safety regulations, pesticide contamination, pollution events, species "
            "protection violations, or scientific misconduct by regulated entities to any federal "
            "or state authority must receive whistleblower protection regardless of employment "
            "status or citizenship.",
            "Anyone who reports pollution, illegal pesticide use, or other environmental "
            "violations — whether they're a company employee, a farm worker, or just a citizen "
            "who witnessed it — is protected from retaliation.",
        ),
        (
            "Anti-retaliation prohibition for environmental reporters — includes scientific "
            "dissent",
            "No employer, regulated entity, contractor, or government agency may retaliate "
            "against any person for reporting environmental law violations, cooperating with EPA "
            "or state environmental agency investigations, publishing or disclosing scientific "
            "findings that contradict regulated industry positions, or providing information in "
            "environmental enforcement proceedings. Scientific dissent and publication of "
            "inconvenient research findings constitute protected conduct. Private right of action "
            "available.",
            "Companies and agencies can't punish employees or scientists for reporting "
            "environmental violations or publishing research findings that the industry "
            "doesn't like. Victims can sue.",
        ),
        (
            "EPA OIG as enforcement actor for environmental whistleblower retaliation — "
            "structural independence required",
            "The EPA Office of Inspector General must maintain an accessible, confidential "
            "environmental whistleblower intake program, structurally independent from EPA "
            "enforcement programs to prevent conflicts of interest. State environmental agencies "
            "must adopt equivalent anti-retaliation mechanisms as a condition of EPA delegation "
            "authority. Retaliation complaints must receive an initial determination within "
            "180 days.",
            "The EPA inspector general runs a confidential reporting program. State "
            "environmental agencies must have the same protections to receive federal authority. "
            "Cases must be decided within six months.",
        ),
        (
            "Environmental whistleblower protections are non-waivable — void confidentiality "
            "terms",
            "Environmental whistleblower protections may not be waived by any employment "
            "contract, nondisclosure agreement, settlement, or confidentiality provision. "
            "Any term purporting to prohibit or penalize the reporting of environmental "
            "violations to any government authority is void as against public policy.",
            "No NDA, settlement, or contract can stop someone from reporting environmental "
            "violations to the government. Any clause that tries is not valid.",
        ),
    ],
    "GUNS": [
        (
            "Firearm safety whistleblower protection — scope and beneficiaries",
            "Any person — including employees of firearm dealers or manufacturers, law "
            "enforcement personnel, background check system workers, or members of the public "
            "— who reports illegal gun trafficking, straw purchases, unlicensed dealing, "
            "failure to conduct required background checks, illegal firearm modifications, or "
            "violations of firearm safety storage laws to any federal or state authority must "
            "receive whistleblower protection regardless of employment status.",
            "Anyone who reports illegal gun sales, trafficking, or safety violations is "
            "protected from retaliation — whether they work in a gun shop, in law enforcement, "
            "or are just someone who witnessed the violation.",
        ),
        (
            "Anti-retaliation prohibition for firearm safety reporters",
            "No employer, firearms dealer, manufacturer, law enforcement agency, or government "
            "entity may retaliate against any person for reporting violations of firearm law, "
            "cooperating with ATF investigations, or providing information in firearm trafficking "
            "proceedings. Retaliation includes termination, threats, physical intimidation, or "
            "filing retaliatory claims. Private right of action available.",
            "Employers in the gun industry and law enforcement agencies can't fire or threaten "
            "anyone for reporting illegal gun activity. Victims of retaliation can sue.",
        ),
        (
            "ATF OIG as enforcement actor for firearm safety whistleblower retaliation",
            "The ATF Office of Inspector General must maintain an accessible, confidential "
            "intake program for firearm safety whistleblower complaints. Retaliation complaints "
            "must receive an initial determination within 180 days. The enforcement actor for "
            "retaliation claims must be structurally independent of the underlying ATF "
            "investigation.",
            "The ATF's inspector general runs a confidential reporting program and must respond "
            "to retaliation complaints within six months.",
        ),
        (
            "Firearm whistleblower protections are non-waivable — no dealer agreement may "
            "abrogate",
            "Firearm safety whistleblower protections may not be waived by any employment "
            "contract, dealer licensing agreement, nondisclosure agreement, or confidentiality "
            "provision. Any contractual term that prohibits or penalizes reporting of "
            "firearm law violations to any government authority is void as against "
            "public policy.",
            "No employment contract or dealer agreement can stop someone from reporting "
            "illegal gun activity to the government. Any such clause is not valid.",
        ),
    ],
    "HOUS": [
        (
            "Housing whistleblower protection — scope and beneficiaries",
            "Any person — including tenants, homebuyers, housing workers, contractors, appraisers, "
            "lenders, or members of the public — who reports housing discrimination, fair housing "
            "violations, predatory lending, tenant harassment, building code violations "
            "concealment, subsidized housing fraud, or illegal eviction practices to any federal "
            "or state authority must receive whistleblower protection regardless of employment "
            "status, housing status, or citizenship.",
            "Anyone who reports housing discrimination, illegal evictions, predatory loans, or "
            "fraud in subsidized housing is protected from retaliation — whether they're a "
            "tenant, a housing worker, or just someone who witnessed it.",
        ),
        (
            "Anti-retaliation prohibition for housing reporters — includes tenants and "
            "prospective buyers",
            "No landlord, housing provider, lender, real estate agent, contractor, government "
            "agency, or housing authority may retaliate against any person for reporting "
            "housing law violations, cooperating with HUD or state fair housing agency "
            "investigations, or providing information in housing discrimination proceedings. "
            "Retaliation against tenants includes eviction, rent increases, denial of services, "
            "or harassment. Private right of action available.",
            "Landlords, lenders, and real estate agents can't evict, harass, or punish tenants "
            "or anyone else for reporting housing discrimination or fraud. Victims can sue.",
        ),
        (
            "HUD OIG and state fair housing agencies as enforcement actors for housing "
            "whistleblower retaliation",
            "HUD's Office of Inspector General must maintain an accessible, confidential "
            "housing whistleblower intake program. State fair housing agencies receiving HUD "
            "funding must adopt equivalent anti-retaliation mechanisms. Retaliation complaints "
            "must receive an initial determination within 180 days.",
            "HUD's inspector general runs a confidential reporting program. State fair housing "
            "agencies that receive federal money must have the same protections.",
        ),
        (
            "Housing whistleblower protections are non-waivable — void lease and contract terms",
            "Housing whistleblower protections may not be waived by any lease, employment "
            "contract, nondisclosure agreement, or settlement. Any lease clause or contract "
            "term that prohibits or penalizes the reporting of housing law violations to any "
            "government authority is void as against public policy and unenforceable in any "
            "proceeding.",
            "No lease or contract can stop someone from reporting housing discrimination or "
            "fraud to the government. Any clause that tries is not valid.",
        ),
    ],
    "IMMG": [
        (
            "Immigration enforcement whistleblower protection — scope and beneficiaries",
            "Any person — including non-citizens, detained individuals, legal permanent residents, "
            "citizens, immigration attorneys, detention facility workers, and community advocates "
            "— who reports immigration enforcement abuse, civil rights violations in detention "
            "facilities, contractor fraud in immigration facilities, illegal detention conditions, "
            "due process violations, or violations of asylum law to any federal or state authority "
            "must receive whistleblower protection regardless of immigration status.",
            "Anyone who reports abuse in immigration detention or violations of immigration "
            "law — including people who are themselves undocumented — is protected from "
            "retaliation. Immigration status cannot be used as a basis for retaliation.",
        ),
        (
            "Anti-retaliation prohibition for immigration reporters — immigration status may "
            "not be used as retaliation",
            "No immigration authority, detention contractor, government agency, or employer may "
            "retaliate against any person for reporting immigration enforcement abuse, cooperating "
            "with DHS OIG or DOJ Civil Rights Division investigations, or providing information "
            "in immigration proceedings. Using immigration enforcement action as retaliation "
            "against a reporter — including initiating removal proceedings against a complainant "
            "— constitutes prohibited retaliation. Private right of action available.",
            "The government can't use deportation or immigration enforcement as a tool to punish "
            "people who report abuse. Retaliating through immigration enforcement is explicitly "
            "illegal. Victims can sue.",
        ),
        (
            "DHS OIG and DOJ Civil Rights Division as enforcement actors for immigration "
            "whistleblower retaliation",
            "The DHS Office of Inspector General and the DOJ Civil Rights Division must jointly "
            "maintain accessible, confidential intake channels for immigration whistleblower "
            "complaints. Given the elevated risks to non-citizen reporters, expedited review "
            "procedures must be available for any complainant who faces imminent removal action. "
            "Retaliation complaints must receive an initial determination within 90 days.",
            "The DHS inspector general and the Justice Department's Civil Rights Division both "
            "take confidential reports. Complaints from people facing deportation must be "
            "reviewed faster — within 90 days.",
        ),
        (
            "Immigration whistleblower protections are non-waivable — void contract and "
            "detention agreement terms",
            "Immigration whistleblower protections may not be waived by any employment contract, "
            "detention agreement, settlement, or confidentiality provision. Any term that "
            "prohibits or penalizes reporting of immigration law violations or detention abuse "
            "to any government authority is void as against public policy.",
            "No detention contract or employment agreement can stop someone from reporting "
            "immigration abuse to the government. Any such clause is not valid.",
        ),
    ],
    "INFR": [
        (
            "Infrastructure safety whistleblower protection — scope and beneficiaries",
            "Any person — including contractors, inspectors, engineers, government workers, "
            "utility employees, or members of the public — who reports infrastructure safety "
            "violations, falsified inspection records, pipeline safety hazards, dam or bridge "
            "structural concerns, water system contamination, cybersecurity vulnerabilities in "
            "critical infrastructure, or contractor fraud in public works projects to any "
            "federal or state authority must receive whistleblower protection regardless of "
            "employment status.",
            "Anyone who reports unsafe infrastructure — a cracked bridge, a contaminated water "
            "system, a falsified safety inspection — is protected from retaliation, whether "
            "they work for the company or just found out about it.",
        ),
        (
            "Anti-retaliation prohibition for infrastructure safety reporters",
            "No contractor, infrastructure operator, government agency, utility, or public works "
            "authority may retaliate against any person for reporting infrastructure safety "
            "violations, cooperating with DOT, FERC, EPA, or sector-specific OIG investigations, "
            "or providing information in infrastructure safety proceedings. Retaliation includes "
            "termination, blacklisting from contracting, threats, or filing retaliatory claims. "
            "Private right of action available.",
            "Construction companies, utilities, and government agencies can't fire or punish "
            "anyone for reporting infrastructure safety problems. Victims can sue.",
        ),
        (
            "Sector OIGs and DOT as enforcement actors for infrastructure safety whistleblower "
            "retaliation",
            "The DOT Office of Inspector General, FERC, EPA, and sector-specific OIGs must "
            "each maintain accessible, confidential intake channels for infrastructure safety "
            "whistleblower complaints within their jurisdiction. A coordinated intake portal "
            "must allow reporters to submit complaints without pre-identifying the responsible "
            "agency. Retaliation complaints must receive an initial determination within "
            "180 days.",
            "Multiple federal agencies each run confidential reporting programs for infrastructure "
            "safety. There must also be a single portal where you can report without knowing "
            "which agency is responsible.",
        ),
        (
            "Infrastructure safety whistleblower protections are non-waivable — void "
            "contractor terms",
            "Infrastructure safety whistleblower protections may not be waived by any "
            "employment contract, government contract, nondisclosure agreement, or "
            "confidentiality provision. Any contractual term that prohibits or penalizes "
            "reporting of infrastructure safety violations to any government authority is void "
            "as against public policy and unenforceable in any proceeding.",
            "No government contract, employment agreement, or NDA can stop someone from "
            "reporting dangerous infrastructure to authorities. Any such clause is not valid.",
        ),
    ],
    "LABR": [
        (
            "Labor law whistleblower protection — scope and beneficiaries",
            "Any worker — including employees, independent contractors, gig workers, day "
            "laborers, seasonal workers, domestic workers, and workers regardless of immigration "
            "status — who reports workplace safety violations, wage theft, anti-organizing "
            "retaliation, illegal hiring practices, child labor violations, or violations of "
            "labor law to any federal or state authority must receive whistleblower protection "
            "regardless of employment status.",
            "Any worker — including gig workers, undocumented workers, and domestic workers "
            "— who reports wage theft, unsafe conditions, or anti-union retaliation is protected "
            "from being fired or punished. Immigration status cannot be used against them.",
        ),
        (
            "Anti-retaliation prohibition for labor law reporters — immigration status may "
            "not be used as retaliation",
            "No employer, contractor, staffing agency, or government entity may retaliate against "
            "any worker for reporting labor law violations, cooperating with OSHA, NLRB, or DOL "
            "investigations, filing wage claims, or supporting organizing activity. Using "
            "immigration enforcement action as retaliation against a reporting worker constitutes "
            "prohibited retaliation. Retaliation includes termination, reduced hours, schedule "
            "manipulation, threats, or blacklisting. Private right of action with reinstatement "
            "and back pay.",
            "Employers can't fire, cut hours, or threaten workers for reporting labor violations "
            "or supporting a union. Using deportation threats as retaliation is explicitly "
            "illegal. Victims can sue and get their job back.",
        ),
        (
            "NLRB, OSHA, and DOL as enforcement actors for labor whistleblower retaliation",
            "OSHA must maintain an accessible, confidential whistleblower program covering "
            "all statutes within its jurisdiction. The NLRB must maintain equivalent protections "
            "for workers reporting organizing interference and anti-union retaliation. The DOL "
            "Wage and Hour Division must maintain equivalent protections for wage theft reporters. "
            "Retaliation complaints must receive an initial determination within 180 days.",
            "OSHA, the NLRB, and the Labor Department's wage enforcement office each run "
            "confidential reporting programs. All must respond to retaliation complaints within "
            "six months.",
        ),
        (
            "Labor whistleblower protections are non-waivable — void arbitration and "
            "employment contract terms",
            "Labor law whistleblower protections may not be waived by any employment contract, "
            "arbitration clause, nondisclosure agreement, or settlement. Any contractual term "
            "that prohibits or penalizes the reporting of labor law violations to any government "
            "authority is void as against public policy.",
            "No employment contract, NDA, or arbitration clause can stop a worker from "
            "reporting labor violations to the government. Any such clause is not enforceable.",
        ),
    ],
    "MDIA": [
        (
            "Media and information integrity whistleblower protection — scope and beneficiaries",
            "Any journalist, media employee, platform worker, researcher, government "
            "communications staff member, or member of the public who reports disinformation "
            "campaigns, coordinated inauthentic behavior, illegal platform censorship or "
            "algorithmic manipulation, violations of campaign finance disclosure laws in media, "
            "or illegal interference with press freedom to any federal or state authority must "
            "receive whistleblower protection regardless of employment status.",
            "Journalists, platform employees, and anyone who reports disinformation campaigns "
            "or illegal media manipulation are protected from retaliation — whether they work "
            "for the platform or are independent reporters.",
        ),
        (
            "Anti-retaliation prohibition for media integrity reporters — includes source "
            "protection",
            "No media organization, platform, advertiser, political campaign, or government "
            "entity may retaliate against any person for reporting media law violations, "
            "cooperating with FCC, FEC, or DOJ investigations, or disclosing disinformation "
            "operations. Shield law protections for source confidentiality must accompany "
            "anti-retaliation protections — reporters may not be compelled to disclose sources "
            "as part of their complaint. Private right of action available.",
            "Media companies and platforms can't punish journalists or employees for reporting "
            "illegal practices. Reporters who come forward also keep their sources confidential. "
            "Victims can sue.",
        ),
        (
            "FCC, FEC, and DOJ as enforcement actors for media whistleblower retaliation",
            "The FCC, FEC, and DOJ (for media-related antitrust and disinformation violations) "
            "must each maintain accessible, confidential intake channels for media integrity "
            "whistleblower complaints. State attorneys general may exercise concurrent "
            "jurisdiction. Retaliation complaints must receive an initial determination within "
            "180 days.",
            "The FCC, FEC, and Justice Department each take confidential reports about media "
            "violations. State attorneys general can also act. Cases must be decided within "
            "six months.",
        ),
        (
            "Media whistleblower protections are non-waivable — void confidentiality and "
            "employment terms",
            "Media integrity whistleblower protections may not be waived by any employment "
            "contract, nondisclosure agreement, platform terms of service, or settlement. "
            "Any term that prohibits or penalizes the reporting of media law violations to any "
            "government authority is void as against public policy.",
            "No employment contract, NDA, or platform terms of service can stop someone from "
            "reporting media violations to authorities. Any such clause is not valid.",
        ),
    ],
    "RGHT": [
        (
            "Civil rights whistleblower protection — scope and beneficiaries",
            "Any person — including civil rights attorneys, community advocates, government "
            "employees, law enforcement personnel, or members of the public — who reports civil "
            "rights violations, surveillance abuses, unlawful discriminatory enforcement, "
            "constitutional rights deprivation under color of law, or violations of equal "
            "protection and due process to any federal or state authority must receive "
            "whistleblower protection regardless of employment status, citizenship, or the "
            "nature of the reported violation.",
            "Anyone who reports civil rights violations — discrimination, illegal surveillance, "
            "or constitutional rights abuses — is protected from retaliation, whether they work "
            "for the government or are just a citizen reporting what they witnessed.",
        ),
        (
            "Anti-retaliation prohibition for civil rights reporters — protected from civil "
            "and criminal prosecution",
            "No government agency, law enforcement entity, employer, or private party may "
            "retaliate against any person for reporting civil rights violations, cooperating "
            "with DOJ Civil Rights Division investigations, or providing information in civil "
            "rights proceedings. Retaliation includes termination, demotion, intimidation, "
            "threat of prosecution, selective enforcement, or filing retaliatory claims. "
            "Civil rights whistleblowers must be protected from prosecutorial retaliation. "
            "Private right of action available.",
            "The government can't fire, threaten, or selectively prosecute anyone for "
            "reporting civil rights violations. Victims can sue.",
        ),
        (
            "DOJ Civil Rights Division and independent civil rights ombudsperson as "
            "enforcement actors",
            "The DOJ Civil Rights Division must maintain an accessible, confidential intake "
            "program for civil rights whistleblower complaints. An independent civil rights "
            "ombudsperson — structurally independent from the DOJ — must be available to "
            "receive complaints where the DOJ itself is the subject of the reported violation. "
            "Retaliation complaints must receive an initial determination within 180 days.",
            "The DOJ's Civil Rights Division takes confidential reports about civil rights "
            "violations. But if the DOJ itself is the problem, an independent ombudsperson "
            "takes the complaint. Cases must be decided within six months.",
        ),
        (
            "Civil rights whistleblower protections are non-waivable — void government and "
            "private agreement terms",
            "Civil rights whistleblower protections may not be waived by any employment "
            "contract, government contract, nondisclosure agreement, plea agreement, or "
            "settlement. Any term that prohibits or penalizes reporting of civil rights "
            "violations to any government authority is void as against public policy.",
            "No contract, NDA, plea deal, or settlement can stop someone from reporting civil "
            "rights violations to the government. Any such clause is not valid.",
        ),
    ],
    "SCIS": [
        (
            "Scientific integrity whistleblower protection — scope and beneficiaries",
            "Any researcher, agency scientist, contractor, graduate student, academic employee, "
            "peer reviewer, or journal editor who reports scientific misconduct, data "
            "falsification, plagiarism, improper classification of scientific data for "
            "political purposes, suppression of research findings by government agencies, or "
            "violations of research integrity standards to any federal, state, or institutional "
            "authority must receive whistleblower protection regardless of employment or "
            "academic status.",
            "Scientists, researchers, students, and peer reviewers who report data falsification, "
            "suppression of findings, or other research misconduct are protected from retaliation "
            "— including loss of grants, tenure denial, or being blacklisted from publishing.",
        ),
        (
            "Anti-retaliation prohibition for scientific integrity reporters — includes "
            "academic and grant protections",
            "No employer, government agency, institution, journal, funding body, or contractor "
            "may retaliate against any person for reporting scientific misconduct, cooperating "
            "with NSF, NIH, NASA, or other agency OIG investigations, or publishing findings "
            "that contradict politically or commercially preferred conclusions. Retaliation "
            "includes termination, grant revocation, publication blacklisting, tenure denial, "
            "or intimidation. Private right of action available.",
            "Research institutions, agencies, and publishers can't fire, deny tenure, "
            "revoke grants, or blacklist researchers for reporting misconduct or publishing "
            "inconvenient findings. Victims can sue.",
        ),
        (
            "NSF OIG, NASA OIG, and OSTP as enforcement actors for scientific integrity "
            "whistleblower retaliation",
            "The NSF Office of Inspector General, NASA Office of Inspector General, and NIH "
            "Office of Research Integrity must each maintain accessible, confidential intake "
            "channels for scientific integrity whistleblower complaints within their "
            "jurisdiction. The White House Office of Science and Technology Policy (OSTP) "
            "must maintain a cross-agency scientific integrity coordination function. "
            "Retaliation complaints must receive an initial determination within 180 days.",
            "The inspector generals at NSF, NASA, and NIH each take confidential reports "
            "about research misconduct. OSTP coordinates across agencies. Cases must be "
            "decided within six months.",
        ),
        (
            "Scientific integrity whistleblower protections are non-waivable — void "
            "grant and institutional agreement terms",
            "Scientific integrity whistleblower protections may not be waived by any "
            "employment contract, grant agreement, institutional policy, nondisclosure "
            "agreement, or confidentiality provision. Any term that prohibits or penalizes "
            "the reporting of scientific misconduct to any government or institutional "
            "authority is void as against public policy.",
            "No grant agreement, employment contract, or institutional policy can stop "
            "a researcher from reporting scientific misconduct. Any such clause is not valid.",
        ),
    ],
    "TAXN": [
        (
            "Tax integrity whistleblower protection — scope and beneficiaries",
            "Any person — including employees of corporations or accounting firms, tax attorneys, "
            "financial advisors, bank employees, or members of the public — who reports tax "
            "fraud, illegal underpayment, abusive tax shelter schemes, fraudulent valuations, "
            "improper charitable deductions, or illegal tax evasion to the IRS or any state "
            "tax authority must receive whistleblower protection regardless of employment status "
            "or their own tax compliance status.",
            "Anyone who reports tax fraud or illegal tax evasion to the IRS or state tax "
            "authorities is protected from retaliation — even if they were involved in the "
            "scheme and are now cooperating.",
        ),
        (
            "Anti-retaliation prohibition for tax integrity reporters",
            "No employer, corporation, accounting firm, law firm, or government entity may "
            "retaliate against any person for reporting tax fraud violations, cooperating with "
            "IRS Criminal Investigation or the IRS Whistleblower Office, or providing "
            "information in tax enforcement proceedings. Retaliation includes termination, "
            "demotion, blacklisting, threats, or filing retaliatory civil claims. Private right "
            "of action with reinstatement and back pay.",
            "Employers and accounting firms can't fire or punish anyone for reporting tax "
            "fraud to the IRS. Victims can sue and get their job and lost wages back.",
        ),
        (
            "IRS Whistleblower Office as enforcement actor for tax integrity retaliation — "
            "structural independence required",
            "The IRS Whistleblower Office must maintain an accessible, confidential intake "
            "program for tax integrity whistleblower complaints, structurally independent from "
            "IRS examination and audit functions. Retaliation complaints must receive an initial "
            "determination within 180 days. The IRS Whistleblower Award Program must be "
            "maintained with mandatory awards of 15–30 percent of collected tax proceeds for "
            "qualifying submissions.",
            "The IRS Whistleblower Office runs a confidential reporting program, and must respond "
            "to retaliation complaints within six months. People who report tax fraud can also "
            "receive a portion of the taxes that are recovered.",
        ),
        (
            "Tax integrity whistleblower protections are non-waivable — void employment and "
            "advisory agreement terms",
            "Tax integrity whistleblower protections may not be waived by any employment "
            "contract, accounting engagement letter, nondisclosure agreement, or settlement. "
            "Any contractual term that prohibits or penalizes reporting of tax fraud to any "
            "government authority is void as against public policy.",
            "No employment contract, NDA, or accounting agreement can stop someone from "
            "reporting tax fraud to the IRS. Any such clause is not valid.",
        ),
    ],
    "TERM": [
        (
            "Term limits and fitness whistleblower protection — scope and beneficiaries",
            "Any staff member, election administrator, government employee, public official, "
            "or member of the public who reports violations of term limit requirements, "
            "circumvention of mandatory disclosure obligations, manipulation of fitness "
            "assessment processes, or cover-ups of disqualifying conditions for officeholders "
            "to any federal or state authority must receive whistleblower protection regardless "
            "of employment status or political affiliation.",
            "Anyone who reports that an officeholder has violated term limits, hidden "
            "disqualifying conditions, or manipulated fitness reviews is protected from "
            "retaliation — no matter who they work for or what party is involved.",
        ),
        (
            "Anti-retaliation prohibition for term limits and fitness reporters",
            "No government agency, political party, election authority, or employer may "
            "retaliate against any person for reporting violations of term limit or disclosure "
            "requirements, cooperating with Office of Special Counsel, GAO, or OIG "
            "investigations, or providing information in fitness assessment proceedings. "
            "Retaliation includes termination, removal from office or duties, threats, "
            "intimidation, or filing retaliatory claims. Private right of action available.",
            "Government agencies and parties can't fire or punish staff for reporting "
            "term limit violations or fitness assessment fraud. Victims can sue.",
        ),
        (
            "Office of Special Counsel and GAO as enforcement actors for term limits and "
            "fitness whistleblower retaliation",
            "The Office of Special Counsel must maintain an accessible, confidential intake "
            "program for term limits and fitness whistleblower complaints. The GAO must have "
            "authority to investigate fitness assessment manipulation upon receipt of a credible "
            "complaint. Retaliation complaints must receive an initial determination within "
            "180 days.",
            "The Office of Special Counsel runs a confidential reporting program. The GAO "
            "can investigate fitness assessment manipulation when a credible complaint is filed. "
            "Cases must be decided within six months.",
        ),
        (
            "Term limits and fitness whistleblower protections are non-waivable",
            "Whistleblower protections for term limit and fitness violations may not be waived "
            "by any employment contract, government contract, party agreement, nondisclosure "
            "agreement, or settlement. Any term purporting to prohibit or penalize reporting "
            "of term limit or fitness violations to any government authority is void as against "
            "public policy.",
            "No employment contract, party agreement, or NDA can stop someone from reporting "
            "term limit violations or fitness assessment fraud. Any such clause is not valid.",
        ),
    ],
}


def subdomain_exists(conn: sqlite3.Connection, domain: str, code: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM subdomains WHERE domain=? AND code=?", (domain, code)
    ).fetchone()
    return row is not None


def next_seq(conn: sqlite3.Connection, domain: str, subdomain: str) -> int:
    row = conn.execute(
        "SELECT MAX(seq) FROM positions WHERE domain=? AND subdomain=?",
        (domain, subdomain),
    ).fetchone()
    return (row[0] or 0) + 1


def add_wbls_for_domain(conn: sqlite3.Connection, domain: str) -> None:
    positions = WBLS_POSITIONS[domain]

    if subdomain_exists(conn, domain, "WBLS"):
        print(f"  SKIP {domain}-WBLS (subdomain already exists)")
        return

    conn.execute(
        "INSERT INTO subdomains (code, domain, name) VALUES (?,?,?)",
        ("WBLS", domain, "Whistleblower protections"),
    )

    for i, (short_title, full_statement, plain_language) in enumerate(positions, start=1):
        position_id = f"{domain}-WBLS-{i:04d}"
        conn.execute(
            """
            INSERT INTO positions
                (id, domain, subdomain, seq, short_title, full_statement,
                 plain_language, status, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                position_id,
                domain,
                "WBLS",
                i,
                short_title[:120],
                full_statement,
                plain_language,
                "CANONICAL",
                "2026-04-27 00:00:00",
                "2026-04-27 00:00:00",
            ),
        )
        print(f"  + {position_id}: {short_title[:60]}…")


def main() -> None:
    if not DB_PATH.exists():
        sys.exit(f"DB not found: {DB_PATH}")

    domains = sorted(WBLS_POSITIONS.keys())
    print(f"Adding WBLS positions to {len(domains)} domains…\n")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")

    try:
        for domain in domains:
            print(f"{domain}:")
            add_wbls_for_domain(conn, domain)
        conn.commit()
        print("\nCommitted.")
    except Exception as exc:
        conn.rollback()
        sys.exit(f"Rolled back: {exc}")
    finally:
        conn.close()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM positions WHERE subdomain='WBLS' AND status='CANONICAL'"
    ).fetchone()[0]
    conn.close()
    print(f"\nTotal WBLS positions in DB (all domains): {count}")


if __name__ == "__main__":
    main()
