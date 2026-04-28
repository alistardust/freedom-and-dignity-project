#!/usr/bin/env python3
"""
P4 Systemic Overlay Remediation — PolicyOS Pillar Audit 2026-04-27

Covers:
  P4-A  AIGV overlay: LABR-AIGV, ENVR-AIGV
  P4-B  Affirmative duty funding mechanisms (THRV-0003 compliance):
        HLTH-FUND, EDUC-FUND, LABR-FUND, IMMG-FUND, HOUS-FUND, INFR-FUND (extend)
  P4-C  Perverse incentive review (PAOS-TEST-0004):
        CNSR-PINC, TAXN-PINC, LABR-PINC, IMMG-PINC

Safe against concurrent P3 writes:
  - WAL journal mode
  - Exponential-backoff retry on OperationalError: database is locked
  - Fully idempotent: checks subdomain and position existence before every insert
"""

import sqlite3
import time
import random
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "policy" / "catalog" / "policy_catalog_v2.sqlite"
MAX_RETRIES = 5


def connect_wal(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn


def retry_execute(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> sqlite3.Cursor:
    """Execute with exponential-backoff retry on database-locked errors."""
    delay = 1
    for attempt in range(MAX_RETRIES + 1):
        try:
            return conn.execute(sql, params)
        except sqlite3.OperationalError as exc:
            if "database is locked" in str(exc) and attempt < MAX_RETRIES:
                jitter = random.uniform(0, 0.5)
                print(f"  [retry {attempt + 1}/{MAX_RETRIES}] DB locked — waiting {delay + jitter:.1f}s")
                time.sleep(delay + jitter)
                delay = min(delay * 2, 8)
            else:
                raise


def subdomain_exists(conn: sqlite3.Connection, code: str, domain: str) -> bool:
    row = retry_execute(conn, "SELECT 1 FROM subdomains WHERE code=? AND domain=?", (code, domain)).fetchone()
    return row is not None


def position_exists(conn: sqlite3.Connection, position_id: str) -> bool:
    row = retry_execute(conn, "SELECT 1 FROM positions WHERE id=?", (position_id,)).fetchone()
    return row is not None


def get_max_seq(conn: sqlite3.Connection, domain: str, subdomain: str) -> int:
    row = retry_execute(
        conn,
        "SELECT COALESCE(MAX(seq), 0) AS max_seq FROM positions WHERE domain=? AND subdomain=?",
        (domain, subdomain),
    ).fetchone()
    return int(row["max_seq"])


def ensure_subdomain(conn: sqlite3.Connection, code: str, domain: str, name: str, stats: dict) -> None:
    if subdomain_exists(conn, code, domain):
        stats["subdomains_skipped"] += 1
        return
    retry_execute(
        conn,
        "INSERT INTO subdomains (code, domain, name) VALUES (?, ?, ?)",
        (code, domain, name),
    )
    stats["subdomains_added"] += 1
    print(f"  + subdomain {domain}-{code}: {name}")


def insert_position(
    conn: sqlite3.Connection,
    domain: str,
    subdomain: str,
    seq: int,
    short_title: str,
    full_statement: str,
    plain_language: str,
    stats: dict,
) -> None:
    position_id = f"{domain}-{subdomain}-{seq:04d}"
    if position_exists(conn, position_id):
        stats["positions_skipped"] += 1
        stats["skipped_ids"].append(position_id)
        return
    retry_execute(
        conn,
        """INSERT INTO positions
           (id, domain, subdomain, seq, short_title, full_statement, plain_language,
            is_cross_domain, status, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'CANONICAL', datetime('now'), datetime('now'))""",
        (position_id, domain, subdomain, seq, short_title[:120], full_statement, plain_language),
    )
    stats["positions_added"] += 1
    stats["added_by_subdomain"][f"{domain}-{subdomain}"] = (
        stats["added_by_subdomain"].get(f"{domain}-{subdomain}", 0) + 1
    )
    print(f"  + {position_id}: {short_title[:80]}")


def add_positions_for_group(
    conn: sqlite3.Connection,
    positions: list[dict],
    stats: dict,
) -> None:
    """Insert a list of positions, auto-assigning seq numbers from current max."""
    # Track next seq per (domain, subdomain) within this run
    seq_cache: dict[tuple[str, str], int] = {}

    for pos in positions:
        domain = pos["domain"]
        subdomain = pos["subdomain"]
        key = (domain, subdomain)
        if key not in seq_cache:
            seq_cache[key] = get_max_seq(conn, domain, subdomain)
        seq_cache[key] += 1
        insert_position(
            conn,
            domain,
            subdomain,
            seq_cache[key],
            pos["short_title"],
            pos["full_statement"],
            pos["plain_language"],
            stats,
        )


# ---------------------------------------------------------------------------
# Position data
# ---------------------------------------------------------------------------

SUBDOMAINS: list[tuple[str, str, str]] = [
    # (code, domain, name)
    # P4-A
    ("AIGV", "LABR", "AI Governance"),
    ("AIGV", "ENVR", "AI Governance"),
    # P4-B
    ("FUND", "HLTH", "Funding Mechanisms"),
    ("FUND", "EDUC", "Funding Mechanisms"),
    ("FUND", "LABR", "Funding Mechanisms"),
    ("FUND", "IMMG", "Funding Mechanisms"),
    ("FUND", "HOUS", "Funding Mechanisms"),
    # INFR-FUND already exists — no-op from ensure_subdomain
    # P4-C
    ("PINC", "CNSR", "Perverse Incentive Review"),
    ("PINC", "TAXN", "Perverse Incentive Review"),
    ("PINC", "LABR", "Perverse Incentive Review"),
    ("PINC", "IMMG", "Perverse Incentive Review"),
]

POSITIONS: list[dict] = [
    # -----------------------------------------------------------------------
    # P4-A: LABR-AIGV
    # -----------------------------------------------------------------------
    {
        "domain": "LABR",
        "subdomain": "AIGV",
        "short_title": "AI-assisted hiring and screening — disclosure, adverse action, and EEOC enforcement",
        "full_statement": (
            "Any employer using AI tools for resume screening, interview scoring, or candidate ranking "
            "must: (a) disclose AI use to all applicants at the time of application; (b) include in any "
            "adverse action notice the specific algorithmic factors that contributed to the decision; "
            "(c) bear the burden of proof that the AI system does not produce discriminatory outcomes on "
            "protected characteristics. The Equal Employment Opportunity Commission has primary enforcement "
            "authority. Employers must retain algorithmic audit records for 5 years and produce them upon "
            "EEOC request."
        ),
        "plain_language": (
            "If an employer uses AI to screen or rank job applicants, they must tell you about it. If you're "
            "rejected, they must explain what the AI flagged. The employer — not you — must prove their AI "
            "system isn't discriminatory."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "AIGV",
        "short_title": "Pre-deployment bias audit for workforce AI — employers with >100 workers",
        "full_statement": (
            "Employers with more than 100 employees that use AI systems in performance management, scheduling, "
            "discipline, or termination decisions must: (a) conduct an independent bias audit of those systems "
            "at least annually; (b) disclose audit results to affected workers and, upon request, to recognized "
            "collective bargaining units; (c) document remediation steps for any identified disparate impact. "
            "Audits must be conducted by independent third parties, not the AI vendor. DOL and EEOC have joint "
            "enforcement authority."
        ),
        "plain_language": (
            "Companies with more than 100 workers that use AI to manage, schedule, or discipline employees "
            "must have those systems audited every year by an outside reviewer — not the company that sold "
            "them the AI. Workers and their unions can request the results."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "AIGV",
        "short_title": "Worker challenge rights for AI-based adverse employment decisions",
        "full_statement": (
            "Workers subject to AI-based adverse employment decisions — including termination, demotion, "
            "involuntary schedule reduction, and denial of promotion — have the following rights: "
            "(a) a right to request human review of any adverse decision within 30 days; "
            "(b) a right to a written explanation of the algorithmic factors that contributed to the decision, "
            "in plain language; (c) no final adverse decision may be issued solely on the basis of algorithmic "
            "output without a human reviewer having considered the explanation and the worker's response. "
            "Waivers of these rights are void. Enforcement through DOL with private right of action."
        ),
        "plain_language": (
            "If an AI system plays a role in firing you, cutting your hours, or passing you over for a "
            "promotion, you have the right to demand that a real person review the decision and explain "
            "what the AI said about you. No employer can fire someone based solely on an algorithm's output."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "AIGV",
        "short_title": "Algorithmic wage-setting as per se antitrust violation",
        "full_statement": (
            "The use of AI or algorithmic platforms that coordinate wage suppression across competing employers "
            "constitutes a per se violation of the Sherman Antitrust Act. Platform operators that provide "
            "wage-benchmarking or compensation-setting tools used by multiple competing employers bear joint "
            "and several liability for wage suppression outcomes. Affected workers have a private right of "
            "action for treble damages. The DOJ Antitrust Division and FTC have concurrent enforcement "
            "authority. Nothing in this position limits broader wage-fixing enforcement under existing law."
        ),
        "plain_language": (
            "Using AI tools to coordinate pay levels across competing companies — essentially letting an "
            "algorithm fix wages industry-wide — is treated as a form of illegal price-fixing. Companies "
            "that do it, and the platforms that enable it, can be sued by workers and prosecuted by the "
            "Justice Department."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "AIGV",
        "short_title": "Non-waiver clause — AI challenge rights cannot be signed away in employment agreements",
        "full_statement": (
            "Workers' rights to organize, bargain collectively, and file complaints under federal and state "
            "labor law may not be conditioned on waiver of rights to challenge AI-based employment decisions. "
            "Any provision in an employment agreement, arbitration clause, or terms-of-service document that "
            "conditions employment, continued employment, or employment benefits on waiver of AI challenge "
            "rights is void and unenforceable as against public policy. This prohibition applies to pre-dispute "
            "mandatory arbitration clauses that would require AI challenge claims to be decided outside the "
            "NLRB or federal court system."
        ),
        "plain_language": (
            "Employers cannot require workers to sign away their right to challenge AI-based employment "
            "decisions as a condition of getting or keeping a job. Any clause that tries to do this is "
            "automatically void."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-A: ENVR-AIGV
    # -----------------------------------------------------------------------
    {
        "domain": "ENVR",
        "subdomain": "AIGV",
        "short_title": "AI in environmental permitting — disclosure and right to human review",
        "full_statement": (
            "AI systems used in environmental permit review or impact assessment must: "
            "(a) be disclosed by the reviewing agency to the applicant and to affected communities; "
            "(b) allow affected communities and applicants to request human review of any AI-assisted "
            "determination; (c) not be the sole basis for permit denial or approval — a qualified human "
            "reviewer must independently consider the AI output and provide a written finding. "
            "This requirement applies to EPA, Army Corps of Engineers, state environmental agencies acting "
            "under federal delegation, and contractors operating on their behalf."
        ),
        "plain_language": (
            "If a government agency uses AI to help decide whether to approve or deny an environmental "
            "permit, it must tell you about it. You or your community can request that a human being "
            "review the decision. No permit can be granted or denied solely because an algorithm said so."
        ),
    },
    {
        "domain": "ENVR",
        "subdomain": "AIGV",
        "short_title": "Algorithmic pollution monitoring — independent audit and anti-opacity enforcement",
        "full_statement": (
            "AI-based emissions monitoring systems used for regulatory compliance reporting must: "
            "(a) undergo independent third-party audits annually, with audit methodologies and findings "
            "published publicly; (b) not be deployed in ways that use algorithmic opacity — including "
            "trade secret claims — to shield compliance data from EPA or state agency review; "
            "(c) be subject to EPA authority to require parallel manual monitoring when audit findings "
            "indicate reliability concerns. Operators of non-compliant monitoring systems bear liability "
            "for any enforcement gap attributable to algorithmic error or opacity."
        ),
        "plain_language": (
            "Companies that use AI to track their pollution levels for regulatory reporting must have "
            "those systems independently audited every year. They cannot hide behind 'the algorithm is "
            "a trade secret' to avoid environmental enforcement. The EPA can always require manual checks."
        ),
    },
    {
        "domain": "ENVR",
        "subdomain": "AIGV",
        "short_title": "Pre-deployment validation for AI used in regulatory climate and environmental modeling",
        "full_statement": (
            "AI systems used by federal agencies to model climate impact, species endangerment, or pollution "
            "dispersion for regulatory decision-making must: (a) be validated against real-world observational "
            "data before regulatory deployment, with validation methodology, data sources, and accuracy "
            "metrics publicly disclosed; (b) be subject to independent scientific review by a body not "
            "affiliated with the system developer; (c) be updated when post-deployment real-world data "
            "reveals systematic divergence from model predictions exceeding established error thresholds. "
            "Undisclosed or unvalidated models may not form the primary basis for final regulatory determinations."
        ),
        "plain_language": (
            "AI systems that federal agencies use to predict climate and environmental impacts for making "
            "regulatory decisions must be tested against real data before use, and those test results must "
            "be published. If the model turns out to be significantly wrong in practice, it must be updated."
        ),
    },
    {
        "domain": "ENVR",
        "subdomain": "AIGV",
        "short_title": "AI in precision agriculture — disclosure of optimization criteria and EPA oversight",
        "full_statement": (
            "AI-driven precision agriculture tools that affect pesticide application, irrigation and water "
            "usage, or land management at scale must: (a) disclose their optimization criteria and constraint "
            "parameters to operators and, upon request, to regulators; (b) be subject to EPA oversight where "
            "systems optimize solely for yield without environmental sustainability constraints — including "
            "pesticide load minimization, water conservation, or soil health benchmarks. Operators deploying "
            "systems that demonstrably increase pesticide runoff or water consumption relative to conventional "
            "management are not shielded from environmental liability by algorithmic decision-making."
        ),
        "plain_language": (
            "AI farming tools that control how pesticides or water are used must explain what they're "
            "optimizing for. If a tool is designed purely to maximize crop yield without regard to "
            "environmental impact, the EPA can regulate it. Using an algorithm doesn't protect a farmer "
            "or agribusiness from liability for environmental damage."
        ),
    },
    {
        "domain": "ENVR",
        "subdomain": "AIGV",
        "short_title": "Human accountability for AI-assisted environmental enforcement decisions",
        "full_statement": (
            "Federal agency employees who rely on AI outputs to make enforcement decisions — including "
            "penalty assessments, compliance determinations, and referrals for prosecution — bear "
            "individual professional accountability for those decisions. An AI output does not transfer, "
            "diminish, or eliminate the accountability of the human decision-maker. 'The algorithm "
            "recommended this outcome' is not a complete defense in administrative proceedings, "
            "Inspector General investigations, or civil litigation arising from enforcement actions. "
            "Agencies must document the human reviewer's independent assessment alongside any AI output "
            "used in enforcement files."
        ),
        "plain_language": (
            "Government employees who use AI to make environmental enforcement decisions are still "
            "personally responsible for those decisions. Saying 'the computer told me to' is not a "
            "defense. The agency must keep records showing a real person reviewed and approved each "
            "enforcement action."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: HLTH-FUND
    # -----------------------------------------------------------------------
    {
        "domain": "HLTH",
        "subdomain": "FUND",
        "short_title": "Universal healthcare funding floor — mandatory appropriation not subject to discretionary cuts",
        "full_statement": (
            "Federal funding for universal healthcare coverage shall be established as a mandatory "
            "appropriation, removing it from the annual discretionary appropriations process. The funding "
            "floor is defined as the federal expenditure level sufficient to achieve universal enrollment "
            "in coverage meeting the essential health benefits standard established under the ACA or its "
            "successor statute. The mandatory floor may be adjusted upward by Congress but not reduced "
            "below the enrollment-sufficiency threshold by discretionary action or continuing resolution."
        ),
        "plain_language": (
            "Federal funding for universal health coverage is written into law as a guaranteed baseline "
            "that Congress cannot quietly cut by failing to pass a budget. It must be enough to cover "
            "everyone at a defined minimum level of benefits."
        ),
    },
    {
        "domain": "HLTH",
        "subdomain": "FUND",
        "short_title": "Fiscal authority and authorization path for universal healthcare funding",
        "full_statement": (
            "The Department of Health and Human Services, acting in coordination with the Centers for "
            "Medicare and Medicaid Services and the Department of the Treasury, is designated the primary "
            "fiscal authority for the universal healthcare funding mechanism. Funding authorization requires "
            "a joint resolution of Congress specifying: (a) the coverage standard to be achieved; "
            "(b) the enrollment target and timeline; (c) the premium and cost-sharing structure for "
            "enrollees. Annual actuarial certification by CMS is required to confirm that appropriated "
            "funding meets the enrollment-sufficiency threshold."
        ),
        "plain_language": (
            "HHS, CMS, and the Treasury Department jointly manage the money for universal health coverage. "
            "Congress must pass a resolution specifying who gets covered, at what level, and how premiums "
            "work. Every year, CMS must certify that the funding is actually enough to cover everyone as "
            "promised."
        ),
    },
    {
        "domain": "HLTH",
        "subdomain": "FUND",
        "short_title": "Healthcare funding sustainability — dedicated trust fund with diversified revenue",
        "full_statement": (
            "A dedicated healthcare trust fund shall be established with revenue drawn from three sources: "
            "(a) employer contributions scaled to payroll, with rates differentiated by employer size and "
            "sector; (b) pharmaceutical manufacturer contributions based on domestic prescription drug sales "
            "volume, phased in over five years; (c) a general revenue backstop triggered automatically when "
            "trust fund balances fall below a six-month reserve threshold. An actuarial soundness review "
            "shall be conducted by the Congressional Budget Office every five years, with mandatory "
            "legislative action required within two years of a finding of actuarial imbalance."
        ),
        "plain_language": (
            "The healthcare fund is supported by contributions from employers, drug companies, and the "
            "general government budget as a backup. Every five years, the CBO checks whether the math "
            "still works. If it doesn't, Congress must fix it within two years."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: EDUC-FUND
    # -----------------------------------------------------------------------
    {
        "domain": "EDUC",
        "subdomain": "FUND",
        "short_title": "Public education funding floor — mandatory per-pupil appropriation with cost-of-living adjustment",
        "full_statement": (
            "Federal funding for public education shall be established as a mandatory appropriation ensuring "
            "that no state falls below a federally defined per-pupil expenditure floor. The floor shall be "
            "set at the 90th percentile of current state per-pupil spending at the time of enactment and "
            "adjusted annually using a cost-of-living index. States that fall below the floor receive "
            "supplemental federal grants conditioned on maintaining existing state funding levels — no "
            "supplanting of state funds with federal funds is permitted. DOE is designated the fiscal "
            "authority with GAO oversight."
        ),
        "plain_language": (
            "Every state must spend at least a federally defined minimum amount per student. States that "
            "can't meet this floor get federal help — but they can't use that federal money to replace "
            "state spending they were already making. The floor goes up each year with the cost of living."
        ),
    },
    {
        "domain": "EDUC",
        "subdomain": "FUND",
        "short_title": "Universal pre-K and childcare authorization — joint HHS/Education funding with quality conditions",
        "full_statement": (
            "A dedicated federal program for universal pre-kindergarten and childcare access shall be "
            "established under the joint authority of the Department of Health and Human Services and "
            "the Department of Education. The program shall be funded through: (a) an employer payroll "
            "contribution phased in over three years; (b) a progressive income surtax on households "
            "above the 90th percentile income threshold; (c) general revenue. States receive block "
            "grants conditioned on meeting federally defined quality standards (staff-to-child ratios, "
            "educator credentialing, and developmental curriculum requirements) and demonstrating "
            "geographic access parity between urban and rural communities."
        ),
        "plain_language": (
            "The federal government will fund universal pre-K and childcare through employer contributions, "
            "a tax on high-income households, and the general budget. States get the money as grants, but "
            "only if they meet quality and access standards — including in rural areas."
        ),
    },
    {
        "domain": "EDUC",
        "subdomain": "FUND",
        "short_title": "Student debt relief fiscal mechanism — DOE authority with multi-source offset",
        "full_statement": (
            "The Department of Education is authorized to cancel qualifying federal student loan debt "
            "pursuant to its authority under the Higher Education Act, subject to the following fiscal "
            "conditions: (a) the budgetary cost of cancellation is offset over ten years through: "
            "reduction in future federal loan origination fees; income-contingent repayment program "
            "surplus projections certified by CBO; and a one-time surtax on institutional endowments "
            "exceeding $1 billion in assets. (b) Cancellation eligibility criteria, benefit caps, and "
            "income thresholds shall be established by regulation and subject to Congressional review "
            "under the Congressional Review Act."
        ),
        "plain_language": (
            "The Department of Education has the authority to cancel qualifying federal student loans. "
            "The cost is offset through reduced loan fees, projected repayment surpluses, and a one-time "
            "tax on university endowments over $1 billion. Congress can review the rules."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: LABR-FUND
    # -----------------------------------------------------------------------
    {
        "domain": "LABR",
        "subdomain": "FUND",
        "short_title": "Universal portable benefits funding — employer contributions proportional to hours worked",
        "full_statement": (
            "A federally administered portable benefits account system shall be funded through mandatory "
            "employer contributions proportional to hours worked by each worker, regardless of employment "
            "classification — including full-time employees, part-time employees, and independent "
            "contractors. The Department of Labor is designated the fiscal authority. Contribution rates "
            "shall be set by notice-and-comment rulemaking and adjusted annually to reflect benefit costs. "
            "Employers that misclassify workers to avoid contribution obligations are subject to retroactive "
            "contribution liability plus a 25% penalty. The portable benefits account travels with the "
            "worker across employers and is not forfeited upon job change."
        ),
        "plain_language": (
            "Every employer — including those that rely on gig workers and contractors — must pay into "
            "a portable benefits account for every hour their workers put in. The account belongs to "
            "the worker and moves with them from job to job. The Labor Department sets and enforces the "
            "contribution rates."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "FUND",
        "short_title": "Worker transition and retraining — expanded TAA as mandatory appropriation",
        "full_statement": (
            "Trade Adjustment Assistance shall be expanded to cover all forms of job displacement, not "
            "limited to trade-related causes, and funded as a mandatory appropriation. The Department of "
            "Labor is designated the fiscal authority. States administer retraining programs through "
            "federally certified providers subject to federal quality standards including: "
            "(a) completion rates; (b) employment placement rates within 12 months; "
            "(c) wage replacement rates at 24 months post-completion. Workers subject to displacement "
            "from automation, industry consolidation, plant closure, or employer insolvency are eligible "
            "for the same benefits as trade-displaced workers."
        ),
        "plain_language": (
            "The federal worker retraining program is expanded to cover everyone who loses a job — not "
            "just workers displaced by trade deals. It's funded as a guaranteed budget item, not subject "
            "to annual cuts. States run the programs but must meet federal standards for results."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "FUND",
        "short_title": "NLRB enforcement funding floor — mandatory appropriation at $500M annually",
        "full_statement": (
            "National Labor Relations Board enforcement funding shall be established as a mandatory "
            "appropriation not subject to appropriations riders or rescissions. The annual funding floor "
            "is set at $500 million in 2024 dollars, adjusted annually for inflation using the CPI-W index. "
            "Funds are designated for: case processing and investigation; worker outreach and know-your-"
            "rights programs; anti-retaliation enforcement and back-pay collection. Congress may appropriate "
            "above the floor but may not reduce funding below it without a two-thirds vote of both chambers. "
            "Appropriations riders that restrict NLRB enforcement authority are prohibited."
        ),
        "plain_language": (
            "The federal agency that protects workers' rights to organize and join unions must receive "
            "at least $500 million per year in guaranteed funding, adjusted for inflation. Congress cannot "
            "quietly defund it through budget riders. The money goes to handling worker complaints, "
            "outreach, and enforcement."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: IMMG-FUND
    # -----------------------------------------------------------------------
    {
        "domain": "IMMG",
        "subdomain": "FUND",
        "short_title": "Immigration court funding floor — mandatory appropriation to eliminate backlog within 5 years",
        "full_statement": (
            "The immigration court system, operating under the Executive Office for Immigration Review, "
            "shall be funded as a mandatory appropriation at a level sufficient to eliminate the pending "
            "case backlog within five years and maintain current docket levels thereafter. EOIR is "
            "designated the primary fiscal authority within DOJ. The annual funding formula shall be "
            "based on case volume per immigration judge, with a target caseload ceiling to be established "
            "by regulation. An annual CBO review shall certify that appropriated funds are sufficient to "
            "meet the caseload ceiling. Funding shall not be conditioned on removal rate targets."
        ),
        "plain_language": (
            "Immigration courts are guaranteed enough federal funding to clear their backlog within five "
            "years and keep pace with new cases after that. The annual budget is calculated from actual "
            "caseloads, not from how many people are deported — the funding can't be tied to removal "
            "targets."
        ),
    },
    {
        "domain": "IMMG",
        "subdomain": "FUND",
        "short_title": "Immigrant integration services — mandatory appropriation with HHS/DHS joint authority",
        "full_statement": (
            "Federal funding for immigrant integration services — including language access programs, "
            "legal orientation programs, civic integration, and employment authorization assistance — "
            "shall be established as a mandatory appropriation. The Department of Health and Human "
            "Services and the Department of Homeland Security share joint fiscal authority. The funding "
            "formula allocates resources to states based on immigrant population size and service gap "
            "analysis updated every three years by the Census Bureau. States and localities that "
            "establish local integration programs are eligible for matching federal grants conditioned "
            "on non-discrimination in service delivery."
        ),
        "plain_language": (
            "Federal funding for helping immigrants learn English, understand their rights, become "
            "citizens, and get work authorization is guaranteed by law and divided among states based "
            "on where immigrants actually live. States that run their own programs can get matching "
            "federal dollars as long as they serve everyone fairly."
        ),
    },
    {
        "domain": "IMMG",
        "subdomain": "FUND",
        "short_title": "Immigration legal representation — federal public defender equivalent funded as mandatory appropriation",
        "full_statement": (
            "A federal legal representation program equivalent in function to a public defender system "
            "shall be established for immigration proceedings. The Department of Justice is designated "
            "the fiscal authority. Funding shall be sufficient to provide legal representation for: "
            "(a) all detained persons in immigration removal proceedings; (b) all unaccompanied minors "
            "in immigration proceedings regardless of detention status. The program shall be implemented "
            "through grants to nonprofit legal service providers, law school immigration clinics, and "
            "qualified pro bono networks. No means test may be applied to detained persons or "
            "unaccompanied minors."
        ),
        "plain_language": (
            "Everyone held in immigration detention and every unaccompanied child in immigration court "
            "is entitled to a free lawyer, funded by the federal government. The money goes to nonprofit "
            "legal groups and law school clinics — not a government bureaucracy. You don't have to prove "
            "you're poor enough to qualify."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: HOUS-FUND
    # -----------------------------------------------------------------------
    {
        "domain": "HOUS",
        "subdomain": "FUND",
        "short_title": "Affordable housing production floor — $50B annual mandatory appropriation through HUD",
        "full_statement": (
            "Federal funding for affordable housing production shall be established as a mandatory "
            "appropriation with an annual floor of $50 billion in 2024 dollars, adjusted annually "
            "using the construction cost index. The Department of Housing and Urban Development is "
            "designated the primary fiscal authority. Funds shall be distributed through: "
            "(a) expansion of the Low-Income Housing Tax Credit program; "
            "(b) the public housing capital fund for repair and new construction; "
            "(c) direct construction grants to states and municipalities that meet affordability "
            "and anti-displacement conditions. At least 30% of production funding shall be directed "
            "to deeply affordable units at or below 30% of area median income."
        ),
        "plain_language": (
            "The federal government must spend at least $50 billion per year — adjusted for construction "
            "costs — building affordable homes. HUD manages the money, distributing it through tax "
            "credits, direct grants, and public housing funds. At least a third must go to housing for "
            "people with the lowest incomes."
        ),
    },
    {
        "domain": "HOUS",
        "subdomain": "FUND",
        "short_title": "Housing voucher universal entitlement — Section 8 converted from discretionary to mandatory program",
        "full_statement": (
            "The Section 8 Housing Choice Voucher program shall be converted from a discretionary "
            "appropriation to an entitlement program. Every household that meets program eligibility "
            "criteria shall receive a housing voucher as a legal right, with no waitlist. The Department "
            "of Housing and Urban Development is designated the fiscal authority. The funding formula "
            "shall be based on fair market rent by metropolitan statistical area, updated annually. "
            "Landlord participation incentives shall be funded separately from the voucher entitlement. "
            "Means testing may not be structured to create waitlists that effectively deny the entitlement."
        ),
        "plain_language": (
            "Section 8 housing vouchers become a guaranteed right like Social Security or Medicaid — "
            "if you qualify, you get one. No more years-long waitlists. The federal government must "
            "fund enough vouchers for everyone who is eligible."
        ),
    },
    {
        "domain": "HOUS",
        "subdomain": "FUND",
        "short_title": "Homelessness response — Housing First permanent supportive housing as mandatory appropriation",
        "full_statement": (
            "Permanent supportive housing and rapid rehousing programs shall be funded as mandatory "
            "appropriations under joint authority of the Department of Housing and Urban Development "
            "and the Department of Health and Human Services. Funding shall be conditioned on grantee "
            "compliance with the Housing First model — prioritizing immediate housing placement without "
            "preconditions such as sobriety, treatment participation, or employment. Performance metrics "
            "for grantees shall include: (a) median days from identification to housing placement; "
            "(b) housing stability rates at 12 months; (c) reduction in chronic street homelessness. "
            "Grantees that fail performance thresholds after two consecutive years lose eligibility "
            "for new awards but retain existing commitments."
        ),
        "plain_language": (
            "Federal funding to end homelessness is guaranteed — not subject to annual budget fights. "
            "The programs that receive this money must use the Housing First approach: give people "
            "housing immediately, without demanding they first get sober or get a job. Success is "
            "measured by how quickly and stably people are housed."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-B: INFR-FUND (extend existing subdomain — new positions appended)
    # -----------------------------------------------------------------------
    {
        "domain": "INFR",
        "subdomain": "FUND",
        "short_title": "Infrastructure maintenance floor — mandatory appropriation indexed to condition grade",
        "full_statement": (
            "Federal funding for maintenance of critical infrastructure — including bridges, water "
            "and wastewater systems, the electrical grid, and public transit — shall be established "
            "as a mandatory appropriation. The annual funding floor shall be indexed to infrastructure "
            "age and condition grade as reported in the Federal Highway Administration bridge inventory, "
            "EPA water infrastructure assessments, and DOE grid reliability reports. The Departments "
            "of Transportation, Energy, and the EPA share joint fiscal authority based on sector. "
            "Maintenance funding shall be treated separately from capital construction funding and "
            "may not be diverted to new construction projects."
        ),
        "plain_language": (
            "The federal government must guarantee funding every year to maintain roads, bridges, "
            "water systems, and the electrical grid — and the amount is tied to how bad the condition "
            "of those systems actually is. Maintenance money cannot be raided to pay for new "
            "construction projects."
        ),
    },
    {
        "domain": "INFR",
        "subdomain": "FUND",
        "short_title": "Public broadband and connectivity — universal service obligation at 100Mbps by 2030",
        "full_statement": (
            "A universal service obligation for broadband connectivity shall be established and funded "
            "through reform of the FCC Universal Service Fund. The contribution base shall be expanded "
            "to include all broadband service providers and edge providers above a defined revenue "
            "threshold, not limited to voice telephony carriers. Funding shall be sufficient to achieve "
            "100% coverage at a minimum download speed of 100 Mbps and upload speed of 20 Mbps by 2030, "
            "prioritizing unserved and underserved communities. Recipients of USF broadband funds must "
            "offer low-income service tiers at regulated rates and may not impose data caps on those tiers."
        ),
        "plain_language": (
            "Everyone in the country must have access to fast, affordable internet by 2030. The fund "
            "that pays for this is expanded to include tech companies, not just phone carriers. "
            "Internet providers that receive this funding must offer affordable plans to low-income "
            "households with no data caps."
        ),
    },
    {
        "domain": "INFR",
        "subdomain": "FUND",
        "short_title": "Climate resilience infrastructure trust fund — carbon fee, FEMA, and Treasury green bonds",
        "full_statement": (
            "A dedicated climate resilience infrastructure trust fund shall be established for climate "
            "adaptation projects — including sea walls, coastal flood control, inland flood control, "
            "wildfire prevention infrastructure, and urban heat island mitigation. Revenue sources: "
            "(a) a carbon fee on fossil fuel producers and importers, with fee schedule established "
            "by statute and adjusted for emissions reductions trajectory; (b) FEMA mitigation grant "
            "matching funds redirected from post-disaster relief; (c) proceeds from Treasury-issued "
            "green bonds designated for climate infrastructure. The Council on Environmental Quality "
            "and FEMA share joint fiscal authority. Projects must demonstrate climate risk reduction "
            "per dollar invested as a condition of funding."
        ),
        "plain_language": (
            "A permanent federal fund for building climate defenses — sea walls, flood control, "
            "wildfire prevention — is funded through fees on fossil fuel companies, money shifted "
            "from disaster cleanup to prevention, and government green bonds. Every project must "
            "show it actually reduces climate risk."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-C: CNSR-PINC
    # -----------------------------------------------------------------------
    {
        "domain": "CNSR",
        "subdomain": "PINC",
        "short_title": "Regulatory revolving door — 5-year cooling-off period for FTC/CFPB senior officials",
        "full_statement": (
            "Consumer protection agencies face structural capture risk when senior officials cycle "
            "between regulated industries and enforcement roles. Counter-design: a 5-year post-"
            "government employment cooling-off period shall apply to senior officials of the FTC and "
            "CFPB — defined as GS-15 and above or SES-equivalent — prohibiting them from accepting "
            "compensated employment with, or providing compensated consulting services to, any entity "
            "that was a subject of enforcement action or rulemaking during their tenure. The Office "
            "of Government Ethics shall administer the restriction with automatic disqualification "
            "upon violation. Violations shall be treated as criminal conflict-of-interest offenses."
        ),
        "plain_language": (
            "Senior officials at the FTC and CFPB cannot take jobs with companies they regulated "
            "for five years after leaving government. This is intended to prevent the agencies from "
            "going easy on industries because their officials are angling for private sector jobs. "
            "Violating this rule is a crime."
        ),
    },
    {
        "domain": "CNSR",
        "subdomain": "PINC",
        "short_title": "Complaint data suppression — intake volume as positive performance metric, annual GAO audit",
        "full_statement": (
            "Consumer protection agencies that measure success by complaint resolution rates have a "
            "structural incentive to suppress or downgrade complaint intake in order to improve "
            "reported metrics. Counter-design: (a) complaint intake volume shall be classified as "
            "a positive performance metric for consumer protection agency leadership — high complaint "
            "volume indicates effective outreach and public trust, not poor performance; (b) the "
            "Government Accountability Office shall conduct an annual independent audit of complaint "
            "intake handling, downgrading, and resolution practices at the FTC and CFPB; (c) "
            "algorithmic or administrative complaint triage systems that systematically downgrade "
            "or route away complaints from protected groups shall be treated as a potential "
            "discriminatory practice subject to OIG referral."
        ),
        "plain_language": (
            "Consumer protection agencies shouldn't be measured by how few complaints come in — "
            "that creates an incentive to ignore or bury complaints. Instead, receiving many "
            "complaints means people trust the agency enough to report problems. The GAO audits "
            "the agencies every year to make sure they're not gaming the numbers."
        ),
    },
    {
        "domain": "CNSR",
        "subdomain": "PINC",
        "short_title": "Settlement maximization vs. deterrence — mandatory appropriation and ring-fenced restitution fund",
        "full_statement": (
            "Agencies that rely on settlement revenue for operating budgets develop a structural "
            "incentive to pursue high-dollar settlements in individual cases rather than pursuing "
            "systemic deterrence through rulemaking, industry-wide enforcement, or criminal referrals. "
            "Counter-design: (a) consumer protection agency operating budgets shall be funded "
            "exclusively through mandatory appropriations, not through settlement revenue; "
            "(b) all monetary settlements and civil penalties collected by the FTC and CFPB shall "
            "be deposited into a dedicated consumer restitution fund administered by Treasury, "
            "not returned to the agency budget; (c) agency performance metrics shall include "
            "deterrence indicators — industry-wide compliance rates, recidivism rates among "
            "sanctioned entities, and systemic rule changes achieved — not settlement revenue maximization."
        ),
        "plain_language": (
            "Consumer protection agencies shouldn't be financially dependent on the fines and "
            "settlements they collect — that creates pressure to go for the biggest payout rather "
            "than fixing systemic problems. Settlement money goes to consumers, not back to the agency. "
            "Agency performance is measured by whether industries actually change their behavior."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-C: TAXN-PINC
    # -----------------------------------------------------------------------
    {
        "domain": "TAXN",
        "subdomain": "PINC",
        "short_title": "Audit disparate impact — IRS required to publish audit rates by income decile with mandatory rebalancing",
        "full_statement": (
            "IRS algorithmic audit selection that systematically over-selects low-income EITC claimants "
            "relative to high-income returns constitutes a structural injustice and undermines public "
            "confidence in tax administration. Counter-design: (a) the IRS shall publish an annual "
            "report disclosing audit initiation rates broken down by income decile; (b) if the audit "
            "rate for the bottom income quintile exceeds the audit rate for the top income quintile "
            "by more than 5 times, the IRS is required to implement a rebalancing plan within one "
            "fiscal year; (c) algorithm selection criteria for automated audit triggers must be "
            "disclosed to the Treasury Inspector General and subject to annual disparate impact review. "
            "This requirement applies to both individual and business returns."
        ),
        "plain_language": (
            "The IRS must publicly report how often it audits people at different income levels. "
            "If it's auditing low-income households more than five times as often as wealthy ones, "
            "it has to rebalance. The audit selection algorithm must be independently reviewed for "
            "discriminatory impact."
        ),
    },
    {
        "domain": "TAXN",
        "subdomain": "PINC",
        "short_title": "Tax expenditure capture — distributional analysis required for all expenditures over $1B",
        "full_statement": (
            "Tax expenditures — including deductions, exclusions, preferential rates, and refundable "
            "credits — are disproportionately captured by high-income filers, creating a regressive "
            "subsidy structure embedded in the tax code. Counter-design: (a) all tax expenditures "
            "with an annual revenue cost exceeding $1 billion must undergo a distributional analysis "
            "by the Joint Committee on Taxation before renewal or extension, showing benefit "
            "distribution by income quintile; (b) sunset provisions are required for all tax "
            "expenditures, with a maximum term of 10 years before mandatory reauthorization; "
            "(c) tax expenditures that deliver more than 50% of their total benefit to the top "
            "income quintile must include a phase-out schedule or be redesigned as refundable credits."
        ),
        "plain_language": (
            "Every major tax break worth over $1 billion per year must be analyzed to show who actually "
            "benefits — and that analysis must be public before Congress renews it. Tax breaks expire "
            "every 10 years and must be reapproved. If a tax break mostly helps the wealthy, it must "
            "be redesigned or phased out."
        ),
    },
    {
        "domain": "TAXN",
        "subdomain": "PINC",
        "short_title": "Tax complexity as compliance barrier — IRS Direct File made permanent and fully funded",
        "full_statement": (
            "Tax code complexity disproportionately burdens low-income and moderate-income filers who "
            "cannot afford professional tax preparation assistance, effectively imposing a time and "
            "money tax on filing compliance. Counter-design: (a) IRS Direct File shall be made a "
            "permanent program and fully resourced to serve all filers, with free filing guaranteed "
            "for all filers with income below $150,000; (b) the IRS is prohibited from entering into "
            "agreements that restrict its authority to provide free filing services in competition "
            "with commercial preparers; (c) the Department of the Treasury shall conduct a complexity "
            "reduction review every 5 years, identifying provisions that impose compliance costs "
            "disproportionate to their revenue yield, with mandatory Congressional consideration of "
            "simplification legislation within two years of each review."
        ),
        "plain_language": (
            "Filing taxes shouldn't require paying a private company to help you. The IRS's free "
            "filing program is made permanent and must be fully funded. The IRS can't sign agreements "
            "that limit free filing to protect tax prep companies. Every five years, the Treasury "
            "must identify parts of the tax code that are needlessly complicated and report to Congress."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-C: LABR-PINC
    # -----------------------------------------------------------------------
    {
        "domain": "LABR",
        "subdomain": "PINC",
        "short_title": "NLRB capture — fixed staggered terms, removal only for cause, Senate-confirmed general counsel",
        "full_statement": (
            "National Labor Relations Board composition and general counsel appointment processes "
            "are structurally vulnerable to capture by business interests through politically "
            "timed appointments and at-will removal. Counter-design: (a) NLRB members shall serve "
            "staggered fixed five-year terms and may be removed only for cause, defined as neglect "
            "of duty, malfeasance, or conviction of a felony; (b) the NLRB General Counsel shall "
            "be nominated by the President and confirmed by the Senate, with a mandatory confirmation "
            "hearing within 60 days of nomination; (c) acting general counsel appointments may not "
            "exceed 90 days; (d) no more than three of five NLRB members may be from the same "
            "political party at any time."
        ),
        "plain_language": (
            "The NLRB — the federal agency that protects workers' right to organize — is redesigned "
            "so it can't be captured by business-friendly appointees. Board members serve fixed terms "
            "and can only be fired for serious misconduct, not political reasons. The top prosecutor "
            "must be confirmed by the Senate, and no single party can control the full board."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "PINC",
        "short_title": "Misclassification as cost arbitrage — ABC test codified with rebuttable presumption of liability",
        "full_statement": (
            "Employers have a structural financial incentive to misclassify workers as independent "
            "contractors in order to avoid payroll taxes, benefit obligations, workers' compensation "
            "premiums, and labor law protections. Counter-design: (a) the ABC test for employee "
            "classification shall be codified in federal statute, applicable to all federal labor "
            "and employment law protections; (b) misclassification of a worker who meets the ABC "
            "test criteria for employee status creates a rebuttable presumption of employer liability "
            "for all unpaid wages, benefits, and taxes; (c) affected workers have a private right "
            "of action for misclassification with a three-year statute of limitations; (d) employers "
            "who misclassify workers to avoid labor law compliance are ineligible for federal "
            "contracts for five years following a finding of willful misclassification."
        ),
        "plain_language": (
            "Calling your workers 'contractors' to avoid paying them benefits and following labor "
            "laws is a structural financial incentive that the law directly counters. Federal law "
            "codifies a standard test for who counts as an employee. If you misclassify workers, "
            "you're presumed liable for everything you owe them. Workers can sue, and repeat "
            "violators lose federal contracts."
        ),
    },
    {
        "domain": "LABR",
        "subdomain": "PINC",
        "short_title": "Union election delay as union-busting — 25-day election timeline with post-election legal review",
        "full_statement": (
            "Employers can suppress union organizing by using legal challenges and procedural motions "
            "to delay representation elections indefinitely, gaining time to conduct sustained "
            "anti-union campaigns while worker support erodes. Counter-design: (a) representation "
            "elections must occur within 25 calendar days of a valid petition; (b) all pre-election "
            "legal challenges shall be resolved post-election — they do not delay the election itself; "
            "(c) any employer conduct that the NLRB finds constitutes interference with or restraint "
            "of employees' Section 7 rights during the 25-day period triggers automatic card-check "
            "recognition of the union; (d) employers found to have engaged in bad-faith delay tactics "
            "bear litigation costs in subsequent NLRB proceedings."
        ),
        "plain_language": (
            "Employers currently delay union elections for months or years by filing legal challenges, "
            "giving them time to pressure workers to vote no. This rule requires elections within "
            "25 days. Legal challenges are resolved after the vote, not before. If the employer "
            "illegally interferes with organizing, the union wins automatically."
        ),
    },
    # -----------------------------------------------------------------------
    # P4-C: IMMG-PINC
    # -----------------------------------------------------------------------
    {
        "domain": "IMMG",
        "subdomain": "PINC",
        "short_title": "Detention bed quota — repeal mandates and require individualized flight-risk determination",
        "full_statement": (
            "Congressional mandates specifying minimum immigration detention bed counts create a "
            "structural financial and institutional incentive for immigration enforcement agencies "
            "to detain rather than use alternatives to detention, regardless of individual risk "
            "factors. Counter-design: (a) statutory bed count mandates for immigration detention "
            "shall be repealed; (b) detention shall be authorized only where an immigration judge "
            "makes an individualized written finding of flight risk or danger to the community, "
            "applying a preponderance-of-the-evidence standard; (c) alternatives to detention "
            "programs — including case management, electronic monitoring, and community supervision "
            "— shall be presumed over detention unless the individualized finding establishes that "
            "no alternative adequately addresses the risk identified."
        ),
        "plain_language": (
            "Congress currently requires ICE to keep a minimum number of people in immigration "
            "detention at all times, creating pressure to arrest and hold people just to fill beds. "
            "This rule repeals that requirement. Detention is only allowed when a judge individually "
            "decides a specific person poses a flight risk or safety concern. Otherwise, community "
            "supervision programs are used instead."
        ),
    },
    {
        "domain": "IMMG",
        "subdomain": "PINC",
        "short_title": "Private prison profit motive — prohibit federal immigration detention contracts with private companies",
        "full_statement": (
            "Private immigration detention facility operators earn profit based on length of detention "
            "and per-diem bed fees, creating a structural incentive to maximize detention duration "
            "and oppose policy reforms that would reduce detention rates. Counter-design: "
            "(a) federal immigration detention contracts with private, for-profit prison companies "
            "shall be prohibited; existing contracts shall not be renewed upon expiration; "
            "(b) immigration detention shall be conducted only in government-operated federal "
            "facilities or in facilities operated by nonprofit organizations under performance-"
            "based agreements that do not include per-diem incentive structures; "
            "(c) nonprofit operators must disclose full financial statements including executive "
            "compensation to ICE and to the public annually."
        ),
        "plain_language": (
            "Private prison companies make more money the longer immigrants are detained, giving "
            "them a financial interest in keeping people locked up. This rule bans federal contracts "
            "with private detention companies. Detention can only happen in government facilities "
            "or nonprofit-run facilities — with financial transparency required."
        ),
    },
    {
        "domain": "IMMG",
        "subdomain": "PINC",
        "short_title": "Enforcement metrics that incentivize quantity over justice — replace removal count with multi-factor metrics",
        "full_statement": (
            "Immigration enforcement agencies measured primarily by aggregate removal numbers "
            "develop institutional pressure to pursue easily-found low-priority individuals — "
            "long-settled community members with no criminal record — rather than allocating "
            "resources to serious public safety cases, which are harder to prosecute. "
            "Counter-design: (a) removal count alone may not serve as the primary performance "
            "metric for immigration enforcement agencies or their sub-units; (b) required "
            "performance metrics must include: share of enforcement actions directed at persons "
            "with serious criminal convictions; court appearance rates among persons on ATD programs; "
            "asylum grant rates as a measure of case quality; and average time from identification "
            "to final order; (c) performance evaluations and funding allocations that rely solely "
            "on removal numbers are prohibited."
        ),
        "plain_language": (
            "Immigration enforcement agencies are currently judged by how many people they deport. "
            "That creates pressure to go after easy targets — long-settled residents with no "
            "criminal record — instead of serious cases. This rule requires agencies to be measured "
            "by case quality and public safety outcomes, not just removal numbers."
        ),
    },
]


def main() -> None:
    stats: dict = {
        "subdomains_added": 0,
        "subdomains_skipped": 0,
        "positions_added": 0,
        "positions_skipped": 0,
        "skipped_ids": [],
        "added_by_subdomain": {},
    }

    print(f"Connecting to: {DB_PATH}")
    conn = connect_wal(DB_PATH)

    try:
        with conn:
            print("\n── Ensuring subdomains ──")
            for code, domain, name in SUBDOMAINS:
                ensure_subdomain(conn, code, domain, name, stats)
            # INFR-FUND already exists — verify it's there
            if subdomain_exists(conn, "FUND", "INFR"):
                print(f"  ~ subdomain INFR-FUND already exists (will append positions)")
                stats["subdomains_skipped"] += 1
            else:
                # Should not happen, but guard defensively
                retry_execute(conn, "INSERT INTO subdomains (code, domain, name) VALUES (?,?,?)",
                              ("FUND", "INFR", "Funding Mechanisms"))
                stats["subdomains_added"] += 1
                print("  + subdomain INFR-FUND: Funding Mechanisms")

            print("\n── Inserting positions ──")
            add_positions_for_group(conn, POSITIONS, stats)

    finally:
        conn.close()

    print("\n" + "═" * 60)
    print("P4 REMEDIATION SUMMARY")
    print("═" * 60)
    print(f"  Subdomains added:    {stats['subdomains_added']}")
    print(f"  Subdomains skipped:  {stats['subdomains_skipped']}")
    print(f"  Positions added:     {stats['positions_added']}")
    print(f"  Positions skipped:   {stats['positions_skipped']}")
    if stats["skipped_ids"]:
        print(f"  Skipped IDs:         {', '.join(stats['skipped_ids'])}")
    print("\n  Added per subdomain:")
    for sub_key, count in sorted(stats["added_by_subdomain"].items()):
        print(f"    {sub_key}: {count}")
    total = stats["positions_added"] + stats["positions_skipped"]
    print(f"\n  Total positions processed: {total}")
    print("═" * 60)


if __name__ == "__main__":
    main()
