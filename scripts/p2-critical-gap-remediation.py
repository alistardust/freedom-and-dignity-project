"""
P2 Critical Gap Remediation — PolicyOS Pillar Audit 2026-04-27

Adds new policy positions to address critical gaps in 5 pillars:
  CORT — Access to Justice (new ACJT subdomain, 6 positions)
  SCIS — Enforcement Circuits (new ENFC subdomain, 5 positions)
  TERM — Enforcement Circuits (new ENFC subdomain, 4 positions)
  INFR — AIGV overlay + Independent Oversight (new AIGV + IOBD subdomains, 8 positions)
  LEGL — Independent Ethics Enforcement (new IECE subdomain, 5 positions)

Idempotent: skips positions and subdomains that already exist.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "policy" / "catalog" / "policy_catalog_v2.sqlite"
TIMESTAMP = "2026-04-27 00:00:00"


def get_next_seq(cursor: sqlite3.Cursor, domain: str, subdomain: str) -> int:
    cursor.execute(
        "SELECT COALESCE(MAX(seq), 0) FROM positions WHERE domain=? AND subdomain=?",
        (domain, subdomain),
    )
    return cursor.fetchone()[0] + 1


def ensure_subdomain(cursor: sqlite3.Cursor, code: str, domain: str, name: str) -> None:
    cursor.execute(
        "SELECT 1 FROM subdomains WHERE code=? AND domain=?", (code, domain)
    )
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO subdomains (code, domain, name) VALUES (?, ?, ?)",
            (code, domain, name),
        )
        print(f"  + subdomain {domain}-{code}: {name}")


def insert_position(
    cursor: sqlite3.Cursor,
    domain: str,
    subdomain: str,
    seq: int,
    short_title: str,
    full_statement: str,
    plain_language: str,
    is_cross_domain: int = 0,
) -> bool:
    """Insert position if it does not already exist. Returns True if inserted."""
    position_id = f"{domain}-{subdomain}-{seq:04d}"
    cursor.execute("SELECT 1 FROM positions WHERE id=?", (position_id,))
    if cursor.fetchone():
        print(f"  ~ skip {position_id} (already exists)")
        return False
    assert len(short_title) <= 120, f"short_title too long ({len(short_title)}): {short_title}"
    cursor.execute(
        """
        INSERT INTO positions
            (id, domain, subdomain, seq, short_title, full_statement,
             plain_language, is_cross_domain, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'CANONICAL', ?, ?)
        """,
        (
            position_id, domain, subdomain, seq,
            short_title, full_statement, plain_language,
            is_cross_domain, TIMESTAMP, TIMESTAMP,
        ),
    )
    print(f"  + {position_id}: {short_title[:70]}...")
    return True


# ---------------------------------------------------------------------------
# P2-A: CORT — Access to Justice (ACJT subdomain, 6 positions)
# ---------------------------------------------------------------------------

def remediate_cort(cursor: sqlite3.Cursor) -> int:
    print("\n[P2-A] CORT — Access to Justice")
    ensure_subdomain(cursor, "ACJT", "CORT", "Access to Justice")
    added = 0

    positions = [
        (
            1,
            "Right to counsel in civil proceedings involving housing, custody, or government benefits",
            "Congress must establish by statute a federal right to appointed counsel in civil proceedings where "
            "the opposing party is the government or where the subject matter is (a) eviction or foreclosure "
            "resulting in housing loss, (b) child custody or parental termination, or (c) denial, suspension, "
            "or termination of federal or state government benefits. Courts must appoint qualified counsel at no "
            "cost to the party who qualifies under federal poverty guidelines at 200% or below. Appointment must "
            "occur no later than 10 business days after filing. Federal funding for appointed civil counsel must "
            "be appropriated separately from criminal defense funding and may not be offset against it.",
            "If you are being taken to court and could lose your home, your children, or your government "
            "benefits, you have the right to a free lawyer if you cannot afford one. The government must assign "
            "you a qualified attorney within two weeks of the case being filed.",
        ),
        (
            2,
            "Court filing fee waivers — no denial of court access due to inability to pay",
            "No federal or state court receiving federal funding may deny a person access to any civil proceeding "
            "solely due to inability to pay court filing fees, service fees, or mandatory administrative costs. "
            "Every court must maintain a publicly accessible, plain-language fee waiver application. Courts must "
            "process fee waiver applications within 5 business days; silence constitutes grant. Courts may not "
            "require documentation of expenses beyond a signed affidavit of financial hardship. Fee waiver "
            "denials must state specific written reasons and must provide a mechanism for administrative appeal "
            "without additional cost. Repeated systemic denial of fee waivers is grounds for loss of federal "
            "court assistance funding.",
            "Courts cannot turn you away from filing a lawsuit just because you cannot pay the fees. You can "
            "request a fee waiver by signing a simple form stating you cannot afford it, and the court must "
            "decide within five days. Denying fee waivers without explanation is prohibited.",
        ),
        (
            3,
            "Mandatory arbitration clauses void for civil rights, wage, and safety claims",
            "Mandatory pre-dispute arbitration clauses in consumer contracts, employment agreements, nursing home "
            "admission agreements, and franchise agreements are void and unenforceable as against public policy "
            "when the claim arises under (a) federal or state civil rights law, (b) wage and hour law, "
            "(c) workplace safety or health law, or (d) any law establishing consumer product or service safety "
            "obligations. The right to bring or participate in a class or collective action in court or before an "
            "arbitrator may not be waived by pre-dispute agreement for any such claim. Post-dispute voluntary "
            "arbitration agreements remain enforceable. Any contract term that purports to waive these rights is "
            "void, and the remainder of the contract survives. The Federal Arbitration Act does not preempt this "
            "provision pursuant to Congressional authority under Section 5 of the Fourteenth Amendment.",
            "If you sign a contract with a forced arbitration clause, that clause cannot stop you from taking "
            "your employer, landlord, or a company to court for civil rights violations, unpaid wages, or safety "
            "injuries. You also cannot be forced to give up your right to join a class action lawsuit for these "
            "types of claims.",
        ),
        (
            4,
            "Federal baseline funding for civil legal aid organizations",
            "Congress must establish a permanent baseline federal appropriation for the Legal Services "
            "Corporation (LSC) of no less than $1 billion annually, indexed to inflation, sufficient to provide "
            "legal aid services to all individuals at or below 200% of the federal poverty level who seek "
            "assistance in civil matters. States receiving federal court improvement funding must demonstrate "
            "that their state legal aid capacity, measured in cases closed per 1,000 eligible residents, meets "
            "or exceeds a federally established minimum standard published annually by the LSC. States failing "
            "to meet minimum capacity standards for two consecutive years face a 15% reduction in federal court "
            "improvement funds until compliance is restored. LSC-funded organizations may not be prohibited from "
            "representing clients in any category of civil legal matter, including immigration and public "
            "benefits, absent a specific compelling government interest finding by Congress.",
            "The federal government must fund enough legal aid lawyers to help low-income people with civil "
            "legal problems like eviction, benefits denials, and family law. States that want federal court "
            "funding must show they have enough legal aid capacity. Congress cannot block legal aid lawyers from "
            "helping clients with most civil legal issues.",
        ),
        (
            5,
            "Language access in court proceedings — certified interpreters and translated documents at no cost",
            "In all federal court proceedings and in all state court proceedings in courts receiving federal "
            "funding, any party or witness with limited English proficiency has the right to a certified "
            "interpreter at no cost to that party, for the duration of all hearings, depositions, and "
            "court-ordered proceedings. Courts must maintain a roster of certified interpreters for all "
            "languages spoken by 1% or more of the state or county population and must provide interpreter "
            "access for all other languages within 10 business days of request. All court forms, summonses, "
            "orders, and judgments in matters involving an LEP party must be translated into that party's "
            "primary language before service or entry of judgment. Remote interpreter services are permitted "
            "where in-person is not available, subject to quality standards published by the Administrative "
            "Office of the U.S. Courts. Noncompliance is grounds for reversal of adverse judgment on appeal.",
            "If you do not speak English well, you have the right to a free certified interpreter in any court "
            "hearing. Courts must also translate official documents — like summonses and court orders — into "
            "your language before serving them on you. This applies to both federal courts and state courts "
            "that receive federal funding.",
        ),
        (
            6,
            "ADA compliance and accessible formats mandatory for all federally funded courts",
            "All federal courts and all state courts receiving federal funding must be in full compliance with "
            "the Americans with Disabilities Act Title II by no later than two years from enactment. Compliance "
            "includes physical accessibility of all courtrooms and ancillary spaces, availability of assistive "
            "listening devices, captioning services, and accessible document formats (including screen-reader "
            "compatible electronic documents) for all parties and witnesses with disabilities. Remote and "
            "hybrid court proceedings must include real-time captioning and screen-reader accessible platforms "
            "as a default, not an accommodation requiring advance request. Courts must designate an ADA "
            "Compliance Officer and publish annual accessibility audit results. Federal court improvement "
            "funding is contingent on annual certification of ADA compliance. Failure to comply after two years "
            "results in mandatory corrective action plans and potential funding suspension administered by the "
            "Administrative Office of the U.S. Courts.",
            "Every court must be fully accessible to people with disabilities — including physical access, "
            "hearing assistance, captioning, and accessible documents. Courts that get federal money must "
            "publish yearly reports on their accessibility and can lose funding if they fail to comply.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in positions:
        if insert_position(cursor, "CORT", "ACJT", seq, short_title, full_statement, plain_language):
            added += 1

    print(f"  → {added} positions added to CORT-ACJT")
    return added


# ---------------------------------------------------------------------------
# P2-B: SCIS — Enforcement Circuits (ENFC subdomain, 5 positions)
# ---------------------------------------------------------------------------

def remediate_scis(cursor: sqlite3.Cursor) -> int:
    print("\n[P2-B] SCIS — Enforcement Circuits")
    ensure_subdomain(cursor, "ENFC", "SCIS", "Enforcement Circuits")
    added = 0

    positions = [
        (
            1,
            "Independent federal science integrity enforcement body — structure and jurisdiction",
            "Congress must establish by statute an Independent Science Integrity Board (ISIB) as an independent "
            "federal agency not housed within any executive department. The ISIB must have: (a) a seven-member "
            "governing board appointed by the President with Senate confirmation for staggered six-year terms, "
            "removable only for cause; (b) jurisdiction over all federal agencies that produce, fund, or rely "
            "on scientific research in regulatory decision-making; (c) authority to investigate, on its own "
            "initiative or upon complaint, allegations of political interference with scientific findings, "
            "data suppression, or coerced alteration of agency scientific conclusions; and (d) enforcement "
            "powers including mandatory corrective action orders, public findings of violation, referral to "
            "the Inspector General, and referral to the Department of Justice for criminal prosecution where "
            "applicable. Failure by an agency to respond to a corrective action order within 60 days triggers "
            "an automatic notification to Congress and a 30-day stay of the agency's final rule relying on the "
            "contested findings.",
            "A new independent agency — the Independent Science Integrity Board — would protect federal "
            "scientific findings from political interference. It would have real power to investigate "
            "violations, order corrections, and refer cases to the Justice Department. If an agency ignores "
            "its orders, its related rules are automatically paused while Congress is notified.",
        ),
        (
            2,
            "Federal agency scientific advisory panels — independence, conflict of interest, and correction",
            "All federal agency scientific advisory committees established under the Federal Advisory Committee "
            "Act must meet the following independence standards: (a) no more than 25% of members may be "
            "currently employed by or have received more than $10,000 from entities regulated by or seeking "
            "approval from the agency in the prior three years; (b) the chair must be a non-industry scientist; "
            "(c) all waivers of conflict of interest standards must be publicly disclosed within 10 business "
            "days of grant. The designated enforcement actor for violations of these standards is the ISIB, "
            "which may (i) void advisory committee findings, (ii) order reconstitution of the committee, "
            "and (iii) direct the agency to publish a mandatory correction to any rule or guidance that relied "
            "on the conflicted findings. Agencies must certify conflict of interest compliance to the ISIB "
            "annually. Noncompliance triggers a mandatory 90-day review of any pending advisory committee "
            "recommendations.",
            "Government scientific advisory panels — the expert committees that advise agencies on policy — "
            "must be independent and free of industry conflicts. If the rules are violated, the Independent "
            "Science Integrity Board can throw out the tainted advice and require the agency to redo it. "
            "Agencies must certify compliance every year.",
        ),
        (
            3,
            "Research integrity enforcement — ORI jurisdiction, mandatory timelines, and funding consequences",
            "The Office of Research Integrity (ORI) within the Department of Health and Human Services must "
            "have statutory authority and adequate staffing to (a) receive and investigate all complaints of "
            "research misconduct at institutions receiving federal research funding; (b) complete preliminary "
            "assessments within 60 days and full investigations within 12 months of formal inquiry opening; "
            "and (c) publish final findings and dispositions publicly, subject to whistleblower identity "
            "protections. Institutions must submit their own investigation reports to ORI within the statutory "
            "deadline; failure to submit timely reports results in mandatory suspension of new federal grant "
            "awards to the institution for the affected research area until compliance is restored. Institutions "
            "that fail to take corrective action on ORI findings within 90 days face suspension of all federal "
            "research funding. Retaliation against complainants is an independent violation subject to ORI "
            "enforcement separate from the underlying misconduct proceeding.",
            "The Office of Research Integrity investigates fraud and misconduct in federally funded research. "
            "Universities must respond to its findings quickly or lose the ability to receive new federal "
            "research grants. Final investigation results must be made public so the scientific community and "
            "the public can trust research integrity.",
        ),
        (
            4,
            "Prohibition on suppression of scientific findings — enforcement and mandatory disclosure",
            "No officer, employee, or political appointee of the executive branch may direct, order, or "
            "coerce any federal scientist or agency to suppress, alter, delay publication of, or classify for "
            "non-national-security reasons any scientific finding, dataset, or assessment produced with "
            "federal funds. The designated enforcement actor is the Inspector General of the relevant agency "
            "or, where the IG is implicated or unavailable, the Government Accountability Office. Any federal "
            "scientist or agency employee who has personal knowledge of such suppression must report to the "
            "Inspector General; failure by supervisors to forward such reports is an independent violation. "
            "Upon a finding of unlawful suppression, the IG must (a) order mandatory public disclosure of "
            "the suppressed findings within 30 days and (b) refer the matter to the Department of Justice. "
            "Federal employees who report suppression in good faith are protected as whistleblowers under "
            "the Whistleblower Protection Act; the agency bears the burden of proving non-retaliation.",
            "No one in the executive branch can order a federal scientist to hide, delay, or change their "
            "research findings for political reasons. The agency's Inspector General investigates violations "
            "and can force the government to make suppressed findings public within 30 days. Scientists who "
            "report suppression are protected from retaliation.",
        ),
        (
            5,
            "Space infrastructure safety — independent review board, public reporting, and corrective action",
            "All major space infrastructure programs operated by or under contract with NASA, the Department "
            "of Defense Space Force, or NOAA must establish a Standing Safety and Mission Assurance Review "
            "Board (SMARB) independent of the program office. The SMARB must: (a) include at least two "
            "independent external safety experts not employed by NASA, DOD, or any prime contractor; "
            "(b) conduct mission-ready reviews and publish unredacted findings (except for classified "
            "national security programs) within 60 days of completion; (c) have authority to issue a "
            "flight-hold recommendation that triggers mandatory Congressional notification and a 30-day "
            "review period before a program office may override. In the event of mission failure involving "
            "loss of life or loss of a major orbital asset, the SMARB must convene a root-cause investigation "
            "within 10 days and publish findings within 180 days. Non-compliance with SMARB corrective "
            "action requirements results in mandatory suspension of program funding increments until "
            "corrective actions are certified complete.",
            "Major space programs — like rockets and satellites — must have independent safety review boards "
            "that can pause a mission and notify Congress if they find serious safety problems. When something "
            "goes wrong — especially if lives are lost — a full public investigation must happen within "
            "six months. Programs that ignore safety orders lose funding.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in positions:
        if insert_position(cursor, "SCIS", "ENFC", seq, short_title, full_statement, plain_language):
            added += 1

    print(f"  → {added} positions added to SCIS-ENFC")
    return added


# ---------------------------------------------------------------------------
# P2-C: TERM — Enforcement Circuits (ENFC subdomain, 4 positions)
# ---------------------------------------------------------------------------

def remediate_term(cursor: sqlite3.Cursor) -> int:
    print("\n[P2-C] TERM — Enforcement Circuits")
    ensure_subdomain(cursor, "ENFC", "TERM", "Enforcement Circuits")
    added = 0

    positions = [
        (
            1,
            "FEC as primary enforcement actor for term limit compliance — jurisdiction and consequences",
            "The Federal Election Commission (FEC) is designated as the primary enforcement actor for "
            "compliance with any federal statutory or constitutionally enacted term limits applicable to "
            "members of Congress and federal officeholders. The FEC must: (a) maintain a public term "
            "compliance registry updated within 5 business days of any qualifying event; (b) upon credible "
            "complaint or sua sponte determination that a candidate or officeholder has exceeded term limits, "
            "initiate a formal compliance proceeding within 15 days; (c) publish a finding within 60 days "
            "of opening a proceeding; and (d) upon a finding of violation, issue a mandatory referral to the "
            "relevant state election authority for ballot removal and to the Sergeant-at-Arms of the "
            "applicable chamber for enforcement of disqualification. FEC inaction for more than 60 days "
            "on a pending complaint is subject to mandamus in U.S. district court by any registered voter "
            "in the affected jurisdiction.",
            "The Federal Election Commission enforces term limits for members of Congress and federal "
            "officials. It must investigate complaints within two weeks and publish a decision within "
            "60 days. If a candidate has exceeded their term limit, the FEC must notify state election "
            "officials to remove them from the ballot. If the FEC does nothing, voters can take them "
            "to federal court.",
        ),
        (
            2,
            "OGE as primary enforcement actor for disclosure requirement violations — timelines and consequences",
            "The Office of Government Ethics (OGE) is designated as the primary enforcement actor for "
            "violations of financial disclosure requirements applicable to federal elected officials, "
            "nominees, and political appointees. OGE must: (a) publish a complete compliance calendar "
            "and public delinquency list updated within 5 business days of any missed filing deadline; "
            "(b) initiate a formal investigation within 20 days of a missed, late, or materially "
            "deficient disclosure filing; (c) complete investigation and publish findings within 90 days; "
            "and (d) upon a finding of willful violation, make a mandatory referral to the Department of "
            "Justice and, for elected officials, to the Ethics Committee of the relevant chamber. "
            "Civil fines for late disclosure begin at $500 per day after a 10-day cure period and escalate "
            "to $5,000 per day for disclosures more than 60 days late. No grace period applies to "
            "officeholders who have previously received two or more late-filing notices in the prior "
            "four-year period.",
            "The Office of Government Ethics is responsible for making sure federal officials file their "
            "required financial disclosure forms on time and accurately. It must investigate violations "
            "quickly and refer serious violations to the Justice Department. Late filers face escalating "
            "daily fines, with no second chances for repeat offenders.",
        ),
        (
            3,
            "Independent fitness assessment board — composition, timelines, appellate mechanism, and consequences",
            "An Independent Presidential and Congressional Fitness Board (IPCFB) must be established "
            "by statute as an independent agency. The IPCFB must be composed of: (a) five board members "
            "appointed jointly by the majority and minority leaders of both chambers of Congress, subject "
            "to confirmation, serving five-year staggered terms removable only for cause; (b) all members "
            "must be licensed physicians, psychiatrists, neuropsychologists, or public health professionals "
            "with no current or prior political appointment and no partisan registration activity in the "
            "prior 10 years. Upon formal referral from (i) two-thirds of the relevant chamber's members, "
            "(ii) the Vice President, or (iii) the Cabinet acting under the Twenty-Fifth Amendment, "
            "the IPCFB must convene within 7 days, complete its assessment within 30 days using "
            "standardized validated cognitive and physical fitness instruments, and publish its findings "
            "within 5 days of completion. The affected officeholder may appeal findings to the U.S. Court "
            "of Appeals for the D.C. Circuit within 10 days; the court must issue a ruling within 20 days "
            "of the appeal. A finding of incapacity is not self-executing but is transmitted to the "
            "relevant constitutional mechanism (25th Amendment, impeachment, or chamber expulsion "
            "proceedings) for action.",
            "An independent board of medical professionals — not politicians — would assess whether a "
            "federal officeholder is mentally and physically fit to serve. It can only be triggered by "
            "formal action from Congress or under the Twenty-Fifth Amendment. The board must finish its "
            "review within 30 days, and the official can appeal to a federal court. A finding of "
            "incapacity does not automatically remove anyone — it starts the official constitutional process.",
        ),
        (
            4,
            "Congressional challenge procedure for term limit circumvention — standing, procedure, and review",
            "Any registered voter in a congressional district or state represented by an officeholder "
            "alleged to have circumvented federal term limits has standing to bring a challenge in U.S. "
            "district court. The challenge must be filed with a complaint alleging specific facts "
            "constituting circumvention, including but not limited to relinquishment and re-acquisition "
            "of citizenship, resignation and re-election within a prohibited period, or appointment to "
            "fill a vacancy followed by election. Upon filing, the court must schedule a hearing within "
            "15 days and issue a ruling within 30 days of the hearing. The challenged officeholder bears "
            "the burden of demonstrating compliance. An unsuccessful challenge brought in bad faith is "
            "subject to attorney fee shifting. Any ruling of circumvention is immediately appealable to "
            "the court of appeals for the circuit, which must decide within 30 days. Pending appeal, the "
            "officeholder may continue to serve unless the district court issues a stay.",
            "Any voter in a politician's district or state can go to federal court if they believe the "
            "politician is trying to get around term limits. The court must hold a hearing quickly and "
            "issue a ruling within 30 days. The politician must prove they are in compliance — the "
            "burden is on them, not the challenger.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in positions:
        if insert_position(cursor, "TERM", "ENFC", seq, short_title, full_statement, plain_language):
            added += 1

    print(f"  → {added} positions added to TERM-ENFC")
    return added


# ---------------------------------------------------------------------------
# P2-D: INFR — AIGV overlay + Independent Oversight (AIGV + IOBD, 8 positions)
# ---------------------------------------------------------------------------

def remediate_infr(cursor: sqlite3.Cursor) -> int:
    print("\n[P2-D] INFR — AIGV overlay + Independent Oversight")

    ensure_subdomain(cursor, "AIGV", "INFR", "AI Governance in Infrastructure")
    ensure_subdomain(cursor, "IOBD", "INFR", "Independent Oversight Body")
    added = 0

    aigv_positions = [
        (
            1,
            "AI in infrastructure management — human override, explainability, and independent audit",
            "Algorithmic and AI-driven decision-making systems used in the management of critical "
            "infrastructure — including power grid dispatch, water treatment operations, and public "
            "transit routing and scheduling — must satisfy the following requirements: (a) all automated "
            "decisions with material operational consequences must be subject to immediate human override "
            "by a qualified operator at all times; (b) the decision logic underlying any consequential "
            "automated action must be explainable in plain English upon request by any operator or "
            "regulator; (c) all such systems must undergo independent third-party algorithmic audits at "
            "least every two years, with audit findings published publicly; (d) no AI system may be "
            "granted autonomous authority over safety-critical shutdowns or emergency response without "
            "independent safety certification from the relevant sector regulator (FERC, EPA, or FTA). "
            "Vendors of non-compliant systems are liable for infrastructure failures attributable to the "
            "non-compliant AI feature.",
            "AI systems that help manage power grids, water systems, and public transit must always have "
            "a human who can override them. They must be able to explain their decisions in plain language, "
            "and they must be independently audited every two years. No AI system can be put in charge of "
            "emergency shutdowns without independent safety approval.",
        ),
        (
            2,
            "Autonomous transit systems — safety certification, liability, human supervision, and incident review",
            "Autonomous or semi-autonomous transit vehicles and systems operating on public infrastructure "
            "must obtain certification from the Federal Transit Administration (FTA) or the National "
            "Highway Traffic Safety Administration (NHTSA), as appropriate, prior to revenue service. "
            "Certification requires demonstration of (a) operational safety performance equal to or "
            "better than the human baseline for the mode and route type; (b) a human supervision "
            "protocol with a qualified operator reachable within 60 seconds; (c) mandatory event data "
            "recording and preservation for five years; and (d) third-party liability insurance of no "
            "less than $50 million per vehicle system. In the event of any incident resulting in injury, "
            "death, or property damage exceeding $100,000, an independent incident review board convened "
            "by the National Transportation Safety Board (NTSB) must commence within 15 days and publish "
            "findings within 180 days. Liability for incidents resulting from an AI system failure vests "
            "jointly in the vehicle operator and the AI system vendor, not the transit agency.",
            "Self-driving buses, trains, and transit vehicles must pass federal safety tests before "
            "carrying passengers. They must have a human supervisor reachable within one minute and "
            "be covered by substantial insurance. If someone is injured, an independent federal review "
            "must happen. The company that made the AI system shares liability for injuries caused by "
            "system failures.",
        ),
        (
            3,
            "Smart grid AI and algorithmic utility pricing — transparency, bias audit, and anti-discrimination",
            "Algorithmic pricing systems used by electric and gas utilities subject to FERC or state PUC "
            "jurisdiction must: (a) disclose the pricing model's core variables and weighting methodology "
            "in plain language to the relevant utility regulator upon request; (b) undergo an independent "
            "algorithmic bias audit at least every two years to detect any differential pricing outcomes "
            "correlated with race, income level, zip code, or other protected or proxy characteristics; "
            "(c) publish audit results publicly and submit to the regulator; and (d) correct any "
            "identified discriminatory outcome within 12 months of audit finding or face suspension of "
            "the algorithmic pricing authority pending corrective action certified by the regulator. "
            "Demand-response programs using AI must demonstrate that participation benefits and curtailment "
            "burdens are distributed equitably across income levels. FERC must issue a rulemaking "
            "implementing these requirements within 18 months of enactment.",
            "When electric and gas utilities use AI to set prices, those AI systems must be open to "
            "inspection by regulators. They must be tested every two years to make sure they are not "
            "charging higher prices to lower-income neighborhoods or communities of color. If bias is "
            "found, utilities must fix it within a year or lose the right to use AI pricing.",
        ),
        (
            4,
            "Predictive maintenance AI — public reporting and prohibition on inequitable algorithmic prioritization",
            "AI and algorithmic systems used by federal, state, or local governments or their contractors "
            "to prioritize infrastructure maintenance, repair, or capital investment decisions must: "
            "(a) publish the prioritization criteria and model weights to the relevant oversight authority "
            "annually; (b) include an equity review demonstrating that algorithmic prioritization does "
            "not systematically correlate with race, income, or political affiliation of the communities "
            "served by the infrastructure in question; (c) report the results of the equity review "
            "publicly, alongside a geographic breakdown of investment prioritization outcomes; and "
            "(d) be subject to audit by the relevant Inspector General or the Federal Infrastructure "
            "Oversight Board (FIOB, established under INFR-IOBD-0001). Any finding that AI-driven "
            "prioritization systematically disadvantages protected communities triggers a mandatory "
            "corrective action plan within 90 days. Federal grants for infrastructure maintenance are "
            "conditioned on certification of equity review compliance.",
            "If a government uses AI to decide which roads, bridges, or utilities to fix first, it must "
            "prove that the AI is not systematically neglecting lower-income neighborhoods or communities "
            "of color. The results must be published publicly every year. If the AI is found to be unfair, "
            "the government must fix the problem within 90 days or lose federal grant funding.",
        ),
        (
            5,
            "Critical infrastructure cybersecurity — mandatory standards, incident reporting, and corrective action",
            "Operators of critical infrastructure in the sixteen sectors designated by CISA — including "
            "energy, water, transportation, and communications — must comply with mandatory minimum "
            "cybersecurity standards developed by CISA in consultation with sector-specific agencies. "
            "Standards must be reviewed and updated at least every three years. In the event of a "
            "cybersecurity incident affecting critical infrastructure systems, the operator must report "
            "the incident to CISA within 72 hours of discovery. Failure to report within 72 hours "
            "results in civil fines of $25,000 per day until reporting is complete. Operators must "
            "submit a post-incident corrective action plan within 90 days of a significant incident. "
            "CISA must designate an independent Infrastructure Cybersecurity Oversight Panel to review "
            "compliance with mandatory standards, conduct unannounced inspections, and publish annual "
            "sector-level compliance reports. Operators failing CISA compliance inspections receive a "
            "mandatory 90-day remediation order; repeat failure triggers suspension of federal contracts "
            "or operating licenses in regulated sectors.",
            "Companies that run critical infrastructure — like power grids, water systems, and "
            "communications networks — must meet minimum cybersecurity standards and report cyberattacks "
            "to the federal government within 72 hours. Missing the deadline costs $25,000 a day. "
            "An independent oversight panel checks compliance and publishes yearly reports, and companies "
            "that repeatedly fail can lose federal contracts.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in aigv_positions:
        if insert_position(cursor, "INFR", "AIGV", seq, short_title, full_statement, plain_language):
            added += 1

    iobd_positions = [
        (
            1,
            "Federal Infrastructure Oversight Board — independent agency, jurisdiction, and reporting",
            "Congress must establish a Federal Infrastructure Oversight Board (FIOB) as an independent "
            "federal agency not housed within any Cabinet department. The FIOB must have: (a) a "
            "seven-member governing board appointed by the President with Senate confirmation, serving "
            "staggered five-year terms removable only for cause; (b) jurisdiction over all infrastructure "
            "projects receiving more than $50 million in federal funding, including direct grants, "
            "federal loan guarantees, and tax credit financing; (c) authority to conduct audits, "
            "subpoena records, and commission independent engineering assessments; (d) the responsibility "
            "to publish an annual Infrastructure Performance Report covering cost, schedule, safety, "
            "equity, and condition metrics across all sectors; and (e) enforcement authority to "
            "recommend suspension of federal funding increments for projects materially out of compliance "
            "with performance benchmarks, subject to review by the relevant appropriations committee "
            "within 30 days. The FIOB must maintain a publicly accessible project database with real-time "
            "expenditure and performance data.",
            "A new independent federal agency — the Federal Infrastructure Oversight Board — would "
            "oversee all major infrastructure projects paid for with federal money. It would audit "
            "projects, publish a yearly performance report covering safety, costs, and fairness, and "
            "recommend cutting funding to projects that are seriously off track. Its database would "
            "be publicly available so anyone can track how federal infrastructure money is being spent.",
        ),
        (
            2,
            "Infrastructure safety incident database — mandatory cross-sector reporting, public access, trend analysis",
            "The Federal Infrastructure Oversight Board (FIOB) must maintain a publicly accessible, "
            "standardized cross-sector infrastructure safety incident database covering all federally "
            "funded infrastructure projects and all regulated infrastructure operators. Operators must "
            "report to the database any safety incident resulting in injury, death, unplanned service "
            "interruption exceeding four hours, or damage exceeding $500,000, within 72 hours of "
            "discovery. The database must be (a) searchable by sector, operator, geography, and "
            "incident type; (b) updated in near-real time with submitted reports; (c) accompanied by "
            "annual FIOB-published trend analysis identifying systemic safety patterns, high-risk "
            "operators, and under-resourced infrastructure categories; and (d) linked to corrective "
            "action tracking so the public can see whether mandated remediation has occurred. Failure "
            "to report a qualifying incident triggers civil fines administered by the FIOB. Three or "
            "more unreported incidents in any 12-month period triggers automatic referral to the "
            "relevant Inspector General.",
            "All operators of federally funded infrastructure must report safety incidents — injuries, "
            "deaths, or major service outages — to a public database within 72 hours. The database will "
            "be searchable by anyone and will include yearly trend analysis so the government and the "
            "public can spot patterns of unsafe infrastructure before they become disasters.",
        ),
        (
            3,
            "Infrastructure equity auditing — independent oversight of geographic and demographic equity in investment",
            "The Federal Infrastructure Oversight Board (FIOB) must conduct or commission an independent "
            "equity audit of federal infrastructure investment at least every four years, covering: "
            "(a) geographic distribution of federal infrastructure investment per capita, disaggregated "
            "by urbanicity, census region, and county poverty rate; (b) demographic equity of "
            "infrastructure condition scores, disaggregated by race and income of communities served; "
            "(c) equity of public participation processes in project selection and siting; and "
            "(d) infrastructure investment in communities designated as disadvantaged under the Council "
            "on Environmental Quality's Climate and Economic Justice Screening Tool or equivalent "
            "successor methodology. The FIOB must publish a public equity report within 120 days of "
            "each audit. Any finding that federal infrastructure investment systematically disadvantages "
            "protected communities triggers a mandatory 18-month corrective action process, including "
            "prioritization guidance to federal grant programs. Congress must hold a public hearing on "
            "each equity audit report within 180 days of publication.",
            "Every four years, the Federal Infrastructure Oversight Board must audit whether federal "
            "infrastructure spending is fair — whether lower-income communities and communities of "
            "color are getting their share of investment. The results must be made public, and if "
            "serious inequities are found, the government must fix its grant priorities. Congress must "
            "hold a public hearing on every equity audit.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in iobd_positions:
        if insert_position(cursor, "INFR", "IOBD", seq, short_title, full_statement, plain_language):
            added += 1

    print(f"  → {added} positions added to INFR (AIGV + IOBD)")
    return added


# ---------------------------------------------------------------------------
# P2-E: LEGL — Independent Ethics and Conduct Enforcement (IECE subdomain, 5 positions)
# ---------------------------------------------------------------------------

def remediate_legl(cursor: sqlite3.Cursor) -> int:
    print("\n[P2-E] LEGL — Independent Ethics and Conduct Enforcement")
    ensure_subdomain(cursor, "IECE", "LEGL", "Independent Ethics and Conduct Enforcement")
    added = 0

    positions = [
        (
            1,
            "Independent Congressional Ethics Commission — structure, jurisdiction, and enforcement powers",
            "Congress must establish by statute an Independent Congressional Ethics Commission (ICEC) "
            "as a permanent body with the following structure: (a) nine commissioners — two appointed "
            "by majority party leadership, two appointed by minority party leadership of each chamber, "
            "and five appointed jointly by the Chief Justice and the Chief Judge of the U.S. Court of "
            "Appeals for the D.C. Circuit — serving staggered six-year terms removable only for cause; "
            "(b) the five independent commissioners must not currently hold or have held in the prior "
            "10 years any partisan elected office or partisan appointed position; (c) the independent "
            "commissioners must constitute a majority for any enforcement action. The ICEC has "
            "jurisdiction over all Members of Congress, their staff, and congressional contractors for "
            "violations of federal ethics law, financial disclosure requirements, and conduct standards. "
            "Enforcement powers include: mandatory investigation upon credible complaint, subpoena "
            "authority, public findings of violation, civil fines, referral to the Department of Justice "
            "for criminal prosecution, and public recommendation for censure, suspension, or expulsion "
            "to the relevant chamber. Chambers must act on ICEC expulsion recommendations within 30 days "
            "or publish written findings explaining inaction.",
            "A new independent ethics commission — with a majority of non-politicians — would investigate "
            "misconduct by members of Congress and their staff. It would have real enforcement power: "
            "it can subpoena records, fine violators, refer cases to prosecutors, and publicly recommend "
            "expulsion. Congress would have to vote on expulsion recommendations within 30 days, or "
            "explain in writing why they did not.",
        ),
        (
            2,
            "Ethics investigation timelines and transparency — mandatory public reporting within 180 days",
            "All ethics investigations conducted by the Independent Congressional Ethics Commission (ICEC) "
            "must be completed within 180 days of formal complaint acceptance, with a single 60-day "
            "extension permitted upon written findings of complexity. The ICEC must publish (a) a "
            "public docket of all pending investigations, updated weekly, identifying the respondent "
            "and the general category of violation alleged (without prejudging the merits); (b) the "
            "final determination and its legal and factual basis within 30 days of completion; and "
            "(c) any minority commissioner dissent simultaneously with the majority finding. No final "
            "determination may be sealed, withheld from publication, or classified for non-national-"
            "security reasons. Any determination to dismiss a complaint must also be published with "
            "reasons. The ICEC must publish an annual report summarizing the number of complaints "
            "received, investigated, dismissed, and resolved, and the types and frequency of violations "
            "found. Congressional staff may not direct or delay ICEC publication of findings.",
            "The independent ethics commission must finish investigations within 180 days and publish "
            "its findings publicly. It cannot bury or delay findings forever. Every pending investigation "
            "must be listed on a public docket so the public knows what is being investigated, and "
            "every final outcome — including dismissed cases — must be published with an explanation.",
        ),
        (
            3,
            "Financial disclosure enforcement — OGE concurrent jurisdiction, automatic referral, no repeat grace",
            "The Office of Government Ethics (OGE) has concurrent jurisdiction with the Independent "
            "Congressional Ethics Commission (ICEC) over financial disclosure violations by Members of "
            "Congress and their senior staff. Failure to file a required financial disclosure form by "
            "the statutory deadline automatically triggers a referral to both OGE and ICEC within "
            "5 business days of the missed deadline, without requiring a separate complaint. OGE must "
            "initiate a formal proceeding within 15 days of referral. Civil fines begin at $200 per day "
            "after a 10-day cure period for first-time violations; for any Member or staffer who has "
            "previously received a late-filing finding within the prior eight years, no cure period "
            "applies and fines begin immediately at $1,000 per day. Willful failure to file — defined "
            "as non-filing more than 60 days beyond the deadline — constitutes a federal misdemeanor "
            "referred to the Department of Justice by OGE. All delinquency actions are published "
            "publicly by OGE within 10 days of initiation.",
            "Members of Congress and senior staff who fail to file their required financial disclosure "
            "forms are automatically referred to the ethics commission and the Office of Government "
            "Ethics — no complaint needed. Fines start after 10 days, and repeat offenders face "
            "immediate, higher fines with no grace period. Going more than 60 days without filing "
            "is a federal crime.",
        ),
        (
            4,
            "Conflict of interest voting prohibition — mandatory recusal procedure, enforcement, and vote invalidation",
            "No Member of Congress may vote on any legislation, amendment, or resolution in which they "
            "have a personal financial interest — defined as a direct financial stake, or a financial "
            "stake held by an immediate family member, in any entity that would be materially and "
            "distinctively affected by the measure's passage. A Member who identifies a potential "
            "conflict must file a written recusal notice with the relevant chamber's Ethics Clerk within "
            "48 hours of a bill's scheduling for a vote. The Independent Congressional Ethics Commission "
            "(ICEC) is the enforcement actor for recusal violations. Upon a finding that a Member voted "
            "in violation of this prohibition, the ICEC must (a) publish a public violation finding "
            "within 30 days; (b) refer the Member to the relevant chamber for censure; and (c) certify "
            "the violation to the Clerk of the relevant chamber. Any vote cast in violation of this "
            "provision, if the vote was determinative and the Member's non-participation would have "
            "changed the outcome, is subject to judicial review for invalidation upon petition by any "
            "Member or any directly affected party. The Member bears the burden of demonstrating "
            "non-materiality of the conflict.",
            "Members of Congress cannot vote on laws that directly benefit their own financial holdings "
            "or their family's. They must file a recusal notice within 48 hours of a bill being "
            "scheduled. The independent ethics commission investigates violations, and if a "
            "conflict-tainted vote was the deciding vote on legislation, a court can invalidate it.",
        ),
        (
            5,
            "Constitutional mechanism for deliberate legislative inaction — independent judicial review trigger",
            "Where a court of competent jurisdiction, upon petition by any party with standing, finds "
            "that Congress has failed for more than 18 months to act on a matter as to which the "
            "Constitution imposes an affirmative duty — including but not limited to the duty to "
            "conduct oversight of the executive branch, the duty to declare war before committing "
            "U.S. armed forces to sustained combat operations, and the duty to provide for the "
            "apportionment of the House following each decennial census — the court may issue a "
            "declaratory judgment finding a breach of constitutional duty. The declaratory judgment "
            "does not compel specific legislative action but may (a) authorize the petitioner to seek "
            "mandamus to compel committee scheduling of relevant measures; (b) direct publication of "
            "the finding in the Congressional Record; and (c) serve as the basis for an independent "
            "Inspector General referral to the Government Accountability Office for a compliance audit. "
            "Standing is available to the Executive Branch, to States, and to individuals who "
            "demonstrate concrete, particularized harm from the inaction. No appropriations for "
            "congressional administrative operations may be used for litigation opposing such petitions.",
            "If Congress deliberately refuses to do something the Constitution requires — like overseeing "
            "the president, declaring war before sending troops into combat, or updating House district "
            "maps after a census — a court can declare that Congress has violated its constitutional "
            "duty. This does not force Congress to pass a specific law, but it creates a public record "
            "of the failure and can trigger an independent audit by the Government Accountability Office.",
        ),
    ]

    for seq, short_title, full_statement, plain_language in positions:
        if insert_position(cursor, "LEGL", "IECE", seq, short_title, full_statement, plain_language):
            added += 1

    print(f"  → {added} positions added to LEGL-IECE")
    return added


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(f"Connecting to DB: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    total_added = 0
    try:
        total_added += remediate_cort(cursor)
        total_added += remediate_scis(cursor)
        total_added += remediate_term(cursor)
        total_added += remediate_infr(cursor)
        total_added += remediate_legl(cursor)
        conn.commit()
        print(f"\n✓ Done. {total_added} positions added total.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    # Print final counts
    print("\nFinal position counts:")
    conn2 = sqlite3.connect(str(DB_PATH))
    c2 = conn2.cursor()
    for domain in ["CORT", "SCIS", "TERM", "INFR", "LEGL"]:
        c2.execute("SELECT COUNT(*) FROM positions WHERE domain=?", (domain,))
        cnt = c2.fetchone()[0]
        print(f"  {domain}: {cnt}")
    conn2.close()


if __name__ == "__main__":
    main()
