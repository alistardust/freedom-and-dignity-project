#!/usr/bin/env python3
"""P3 high-gap pillar reinforcement — ELEC/MDIA/FPOL/HOUS/GUNS/CHKS/RGHT.

Inserts new subdomains and positions for the P3 PolicyOS audit remediation.
Fully idempotent: skips anything already present.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "policy" / "catalog" / "policy_catalog_v2.sqlite"

# ---------------------------------------------------------------------------
# New subdomains: (code, domain, name)
# ---------------------------------------------------------------------------
NEW_SUBDOMAINS = [
    ("AIGV", "ELEC", "AI governance for elections"),
    ("PRIV", "ELEC", "Voter privacy"),
    ("AIGV", "MDIA", "AI governance for media"),
    ("ENFC", "MDIA", "Enforcement circuit for media"),
    ("AIGV", "FPOL", "AI governance for foreign policy"),
    ("ENFC", "FPOL", "Enforcement circuit for foreign policy"),
    ("AIGV", "HOUS", "AI governance for housing"),
    ("PRIV", "HOUS", "Tenant privacy"),
    ("CHLG", "GUNS", "Challenge rights for firearms denials"),
    ("CAPT", "GUNS", "Anti-regulatory-capture for ATF"),
    ("ENFC", "CHKS", "Enforcement failure cascade for checks and balances"),
    ("AIGV", "CHKS", "AI governance for checks and balances"),
    ("ENFC", "RGHT", "Enforcement circuit for rights and civil liberties"),
]

# ---------------------------------------------------------------------------
# New positions: (domain, subdomain, short_title, full_statement, plain_language)
# IDs are computed at runtime using max-seq logic.
# ---------------------------------------------------------------------------
NEW_POSITIONS = [
    # ── ELEC-AIGV ────────────────────────────────────────────────────────────
    (
        "ELEC", "AIGV",
        "AI-generated electoral content — mandatory disclosure",
        (
            "AI-generated electoral content — including deepfakes, synthetic candidate "
            "likenesses, and AI-written campaign material — must carry mandatory disclosure "
            "labeling. Platforms bear an enforcement obligation to detect and label such "
            "content. A private right of action exists for voters or candidates harmed by "
            "unlabeled AI-generated electoral content."
        ),
        (
            "If a political ad, video, or message was made or significantly changed by AI, "
            "it must be clearly labeled as AI-generated. Websites and apps must enforce "
            "this rule, and people harmed by unlabeled AI content can sue."
        ),
    ),
    (
        "ELEC", "AIGV",
        "Pre-deployment algorithmic audit — election administration AI",
        (
            "Any AI system used in voter registration processing, ballot counting, or "
            "election administration must undergo an independent algorithmic audit before "
            "deployment. Audit results must be published publicly and available to "
            "election officials, oversight bodies, and the general public."
        ),
        (
            "Before any AI tool is used to run elections — like checking voter rolls or "
            "counting ballots — it must be independently tested and the results must be "
            "made public."
        ),
    ),
    (
        "ELEC", "AIGV",
        "AI voter suppression content — strict platform liability",
        (
            "AI-generated content that conveys false voting dates, locations, or "
            "eligibility information constitutes voter suppression. Platforms bear strict "
            "liability for hosting such content; no safe harbor applies. A 24-hour "
            "takedown requirement is mandatory upon notice or detection."
        ),
        (
            "Platforms are strictly responsible for removing AI-generated content that "
            "gives voters false information about when, where, or whether they can vote — "
            "and must do so within 24 hours of finding it."
        ),
    ),
    (
        "ELEC", "AIGV",
        "Human accountability — no AI final decisions on voter eligibility",
        (
            "No AI system may make final decisions on voter eligibility, ballot validity, "
            "or election certification. Human review is mandatory for all such decisions. "
            "Documented reasoning by the human reviewer must be retained as an official "
            "election record."
        ),
        (
            "A human official — not a computer — must make the final call on whether a "
            "vote counts or whether a voter is eligible. The human's reasoning must be "
            "written down and kept on file."
        ),
    ),
    (
        "ELEC", "AIGV",
        "Non-AI-escape clause — constitutional right to vote",
        (
            "The constitutional right to vote may not be denied, delayed, or burdened by "
            "algorithmic error. Any voter whose eligibility or ballot is affected by an "
            "AI system error is entitled to an immediate human override and remedy, "
            "including provisional ballot or reinstatement of registration."
        ),
        (
            "If a computer makes a mistake that stops someone from voting, that person "
            "has the right to have a human fix the error immediately — including being "
            "allowed to vote on the spot."
        ),
    ),
    # ── ELEC-PRIV ────────────────────────────────────────────────────────────
    (
        "ELEC", "PRIV",
        "Voter data minimization — no commercial use of registration data",
        (
            "Voter registration data collected for election administration purposes must "
            "be limited to information necessary for that purpose. Commercial sale or "
            "transfer of voter registration data to private parties is prohibited. "
            "Violations are subject to civil and criminal penalties."
        ),
        (
            "The government should only collect the voter information needed to run "
            "elections, and may not sell or share that information with businesses."
        ),
    ),
    (
        "ELEC", "PRIV",
        "Voter roll access restrictions — no bulk export for commercial targeting",
        (
            "Access to voter rolls by private parties must be limited, logged, and "
            "conditioned on a demonstrated legitimate use consistent with election "
            "oversight or academic research. Bulk data export of voter rolls for "
            "commercial targeting purposes is prohibited."
        ),
        (
            "Businesses and political campaigns cannot download the full voter list to "
            "target people for ads or outreach. Access is limited and must be logged."
        ),
    ),
    (
        "ELEC", "PRIV",
        "Voting system security — air gap, audit, and paper trail",
        (
            "Voting systems must be air-gapped or otherwise hardened against network "
            "intrusion. Source code for all voting systems is subject to independent "
            "security audit, with results available to election officials and authorized "
            "researchers. A paper audit trail is mandatory for all ballots cast."
        ),
        (
            "Voting machines must be protected from hacking, their software must be "
            "independently reviewed, and every vote must produce a paper record that "
            "can be checked."
        ),
    ),
    # ── MDIA-AIGV ────────────────────────────────────────────────────────────
    (
        "MDIA", "AIGV",
        "AI-generated news and synthetic media — mandatory disclosure labeling",
        (
            "All AI-generated or AI-substantially-modified news content and synthetic "
            "media must carry mandatory disclosure labeling. Platforms hosting such "
            "content bear an enforcement obligation. The FTC has authority to enforce "
            "these disclosure requirements as unfair or deceptive acts or practices."
        ),
        (
            "News articles or videos that were made or significantly altered by AI must "
            "be clearly labeled. Platforms that host them are responsible for enforcing "
            "this rule, and the FTC can take action against violators."
        ),
    ),
    (
        "MDIA", "AIGV",
        "Deepfake prohibition — electoral content within 60 days of election",
        (
            "AI-generated video or audio depicting real persons making false political "
            "statements is prohibited within 60 days of any federal, state, or local "
            "election. Exception applies only to clearly labeled satire that a reasonable "
            "viewer would understand as satirical. Violations are subject to injunctive "
            "relief and damages."
        ),
        (
            "Realistic fake videos or audio of politicians saying things they never said "
            "are banned in the two months before an election, unless they are clearly "
            "marked as satire."
        ),
    ),
    (
        "MDIA", "AIGV",
        "Algorithmic amplification disclosure — ranking factors and audit",
        (
            "Any platform using algorithmic content ranking must publicly disclose: the "
            "factors used in ranking, the weight assigned to engagement-maximizing "
            "signals, and whether the algorithm has been independently audited for "
            "radicalization pathways. Disclosure must be updated annually."
        ),
        (
            "Platforms that use algorithms to decide what content users see must explain "
            "how those algorithms work, including whether they push extreme content, and "
            "whether they have been independently checked."
        ),
    ),
    (
        "MDIA", "AIGV",
        "Pre-deployment audit — recommendation algorithms at scale",
        (
            "Platforms with more than 10 million monthly active users must submit "
            "recommendation algorithm audits to the FTC annually. Audit results must be "
            "made publicly available. Failure to submit triggers FTC enforcement action "
            "including civil penalties."
        ),
        (
            "Large platforms must have their recommendation algorithms independently "
            "reviewed every year and share the results with the public."
        ),
    ),
    (
        "MDIA", "AIGV",
        "Human editorial accountability — automated content moderation appeal",
        (
            "Automated content moderation decisions affecting political speech must be "
            "reviewable by a human editor upon request within 72 hours. No final "
            "moderation decision affecting political speech may be made solely by "
            "algorithm without an available appeal path to human review."
        ),
        (
            "If an algorithm removes or restricts political speech, the person affected "
            "can ask for a human to review that decision within 72 hours."
        ),
    ),
    # ── MDIA-ENFC ────────────────────────────────────────────────────────────
    (
        "MDIA", "ENFC",
        "Primary enforcement actors — FTC, FCC, DOJ, state AGs",
        (
            "Primary enforcement actors for media policy are: FTC (unfair or deceptive "
            "acts and practices), FCC (broadcast licensing conditions), DOJ Antitrust "
            "Division (ownership consolidation), and state attorneys general (consumer "
            "protection and competition law). Each actor maintains an independent "
            "complaint intake process."
        ),
        (
            "Federal and state agencies each have their own role in enforcing media "
            "rules, and each must have its own way for the public to report violations."
        ),
    ),
    (
        "MDIA", "ENFC",
        "Trigger conditions — documented violations and AI labeling failures",
        (
            "Enforcement is triggered by: documented ownership concentration above "
            "statutory thresholds, platform algorithm audit failures, AI content "
            "labeling violations, or retaliatory action against journalists by media "
            "owners or platforms. Each condition has independent enforcement authority "
            "without requiring the others to be present."
        ),
        (
            "Enforcement can be triggered whenever a media company violates ownership "
            "limits, fails an algorithm audit, skips AI labeling requirements, or "
            "punishes journalists for doing their jobs."
        ),
    ),
    (
        "MDIA", "ENFC",
        "Failure consequence — congressional review and structural separation",
        (
            "Failure to enforce documented media policy violations by the FTC or FCC "
            "triggers mandatory congressional review within 60 days. Federal courts may "
            "issue structural separation orders — including ownership divestiture — on "
            "DOJ petition where systemic enforcement failure is found."
        ),
        (
            "If federal agencies fail to enforce media rules, Congress must review the "
            "failure within 60 days. Courts can order media companies to break apart "
            "if the government has systematically failed to act."
        ),
    ),
    (
        "MDIA", "ENFC",
        "Journalist protection — private right of action against retaliation",
        (
            "Retaliation against journalists for publication, source protection, or "
            "platform criticism by an employer or platform triggers a private right of "
            "action in federal court. Employers may not require mandatory arbitration "
            "of retaliation claims. Injunctive relief, reinstatement, and damages are "
            "available remedies."
        ),
        (
            "Journalists who are punished for doing their jobs can sue in federal court. "
            "Employers cannot force journalists to settle retaliation claims through "
            "private arbitration."
        ),
    ),
    # ── FPOL-AIGV ────────────────────────────────────────────────────────────
    (
        "FPOL", "AIGV",
        "Autonomous weapons prohibition — no LAWS without human control",
        (
            "Lethal autonomous weapons systems (LAWS) that select and engage targets "
            "without meaningful human control are prohibited for United States development, "
            "deployment, and transfer. The United States shall advocate for and lead "
            "international treaty negotiations to establish a binding global ban on LAWS."
        ),
        (
            "The U.S. will not build, use, or sell weapons that can choose and kill "
            "targets on their own without a human making the decision. The U.S. will "
            "push for a global treaty banning such weapons."
        ),
    ),
    (
        "FPOL", "AIGV",
        "Human-in-the-loop — AI in targeting and strike authorization",
        (
            "Any use of AI in military targeting, strike authorization, or weapons "
            "deployment requires a documented human decision-maker who bears individual "
            "legal accountability for the decision. AI may support but not replace "
            "human judgment. Accountability chains must be preserved in all after-action "
            "records."
        ),
        (
            "A real person — not a computer — must make the final decision before any "
            "military strike. That person is personally responsible for the decision "
            "and it must be documented."
        ),
    ),
    (
        "FPOL", "AIGV",
        "AI in intelligence analysis — disclosure and analyst certification",
        (
            "AI-generated intelligence assessments used as the basis for policy decisions "
            "must be disclosed as AI-generated in all briefing materials. A human analyst "
            "must certify the assessment. No intelligence action, covert operation, or "
            "policy decision may be taken based solely on AI-generated output without "
            "human verification."
        ),
        (
            "When AI is used to analyze intelligence, decision-makers must know it was "
            "AI-generated, and a human analyst must sign off on it before it is used "
            "to make decisions."
        ),
    ),
    (
        "FPOL", "AIGV",
        "Foreign AI influence operations — national security threat designation",
        (
            "Foreign AI-powered disinformation campaigns targeting domestic United States "
            "political processes, elections, or public institutions are designated as "
            "national security threats. The United States shall respond through diplomatic, "
            "economic, and where necessary military countermeasures proportional to the "
            "severity of the interference."
        ),
        (
            "When foreign governments use AI to spread disinformation and interfere in "
            "U.S. elections or politics, the U.S. will treat it as a national security "
            "threat and respond accordingly."
        ),
    ),
    (
        "FPOL", "AIGV",
        "International AI governance — U.S. leadership in multilateral standards",
        (
            "The United States shall actively participate in and lead multilateral "
            "negotiations to establish binding international standards for AI in military "
            "applications, surveillance technology export controls, and election "
            "interference. The United States shall not export AI-enabled surveillance "
            "tools to governments with documented records of human rights abuses."
        ),
        (
            "The U.S. should lead the world in creating enforceable rules for military "
            "AI and AI-powered surveillance — and must not sell surveillance AI to "
            "governments that abuse human rights."
        ),
    ),
    # ── FPOL-ENFC ────────────────────────────────────────────────────────────
    (
        "FPOL", "ENFC",
        "Congressional oversight trigger — AI use in lethal military operations",
        (
            "Any use of AI in lethal military operations must be reported to the "
            "congressional intelligence and armed services committees within 48 hours "
            "of the operation. Covert action involving AI must be reported to the "
            "Gang of Eight. Classification of AI involvement does not excuse the "
            "reporting obligation."
        ),
        (
            "Every time AI is used in a military operation that kills people, Congress "
            "must be told within 48 hours. Secrecy rules do not eliminate this "
            "obligation."
        ),
    ),
    (
        "FPOL", "ENFC",
        "Challenge rights — AI-assisted targeting and designation",
        (
            "Persons subject to AI-assisted targeting decisions, no-fly listing, or "
            "sanctions designations have the right to challenge the basis of that "
            "designation before an Article III court or an independent national security "
            "tribunal with access to cleared counsel. The government bears the burden "
            "of justifying the designation."
        ),
        (
            "People placed on no-fly lists or sanction lists based on AI analysis have "
            "the right to challenge that decision in court, with a lawyer who has "
            "security clearance if needed."
        ),
    ),
    # ── HOUS-AIGV ────────────────────────────────────────────────────────────
    (
        "HOUS", "AIGV",
        "Algorithmic tenant screening — disclosure and adverse action explanation",
        (
            "Landlords using AI-based tenant screening tools must disclose their use to "
            "applicants before screening occurs. Applicants have the right to a plain-"
            "language explanation of any adverse action taken on the basis of AI "
            "screening. Landlords may not use AI screening tools that produce disparate "
            "impact by race, national origin, or other protected class without "
            "demonstrated business necessity."
        ),
        (
            "If a landlord uses AI to screen rental applicants, they must say so. "
            "Applicants who are rejected must be told why, and AI tools that unfairly "
            "screen out protected groups cannot be used."
        ),
    ),
    (
        "HOUS", "AIGV",
        "AI-based eviction prediction — audit requirement and prohibition on denial",
        (
            "Predictive eviction tools used by landlords or property managers must be "
            "audited annually for racial, socioeconomic, and disability-related bias. "
            "Use of such tools to preemptively deny housing to persons who have not "
            "violated any lease obligation is prohibited."
        ),
        (
            "AI tools that predict who might not pay rent or cause problems must be "
            "independently tested for bias every year, and cannot be used to reject "
            "applicants before they have actually done anything wrong."
        ),
    ),
    (
        "HOUS", "AIGV",
        "Algorithmic rent coordination — antitrust prohibition",
        (
            "Price-fixing through algorithmic rent coordination between competing "
            "landlords — whether implemented through shared software platforms or "
            "indirect data exchange — is prohibited under federal antitrust law. "
            "Platforms providing algorithmic rent-setting tools to competing landlords "
            "bear joint liability for resulting price-fixing violations."
        ),
        (
            "It is illegal for landlords to use software that coordinates rent prices "
            "with their competitors. Companies that sell such software are also "
            "responsible for the harm it causes."
        ),
    ),
    (
        "HOUS", "AIGV",
        "AI in mortgage underwriting — annual disparate impact audit",
        (
            "AI systems used in mortgage underwriting decisions must be audited annually "
            "for disparate impact by race, gender, national origin, and disability "
            "status. Adverse action notices for mortgage denials must specify the "
            "algorithmic factors contributing to the decision in plain language."
        ),
        (
            "AI used to decide who gets a mortgage must be checked every year to make "
            "sure it does not unfairly disadvantage protected groups, and applicants "
            "who are denied must be told the specific reasons."
        ),
    ),
    (
        "HOUS", "AIGV",
        "Human override — no adverse housing decision by algorithm alone",
        (
            "No adverse housing decision — including denial of rental application, "
            "initiation of eviction proceedings, or mortgage denial — may be made "
            "solely by algorithm without human review and documented reasoning. The "
            "human reviewer must have authority to override the algorithmic output."
        ),
        (
            "A person — not just a computer — must review and sign off on any decision "
            "to reject a rental application, start an eviction, or deny a mortgage. "
            "That person must have the power to override the AI's recommendation."
        ),
    ),
    # ── HOUS-PRIV ────────────────────────────────────────────────────────────
    (
        "HOUS", "PRIV",
        "Tenant data minimization — no resale; deletion on tenancy end",
        (
            "Landlords and property management platforms may collect only data necessary "
            "for housing administration. Resale of tenant data to third parties is "
            "prohibited. Tenant personal data must be deleted or anonymized within "
            "90 days of the end of tenancy, except where retention is required by law."
        ),
        (
            "Landlords can only collect the information they need to manage housing. "
            "They cannot sell tenant data, and must delete it within 90 days of a "
            "tenant moving out."
        ),
    ),
    (
        "HOUS", "PRIV",
        "Smart home surveillance limits — no mandatory monitoring as tenancy condition",
        (
            "Landlords may not require tenants to accept surveillance devices — including "
            "smart locks, cameras, or behavioral monitoring systems — as a condition of "
            "tenancy. Any monitoring technology present in a rental unit must be "
            "disclosed in writing before lease signing, with plain-language description "
            "of data collected and retention period."
        ),
        (
            "Landlords cannot force tenants to accept surveillance cameras or smart "
            "devices as a condition of renting. Any monitoring technology must be "
            "disclosed in writing before the lease is signed."
        ),
    ),
    (
        "HOUS", "PRIV",
        "Algorithmic surveillance in public housing — consent and HUD approval required",
        (
            "Use of facial recognition technology, behavioral prediction systems, or "
            "AI-based monitoring in federally funded public housing is prohibited without "
            "explicit written resident consent and HUD approval. HUD approval requires "
            "a public comment period and civil rights impact assessment."
        ),
        (
            "Public housing authorities cannot use facial recognition or AI surveillance "
            "on residents without each resident's written permission and federal approval "
            "following a public review process."
        ),
    ),
    # ── GUNS-CHLG ────────────────────────────────────────────────────────────
    (
        "GUNS", "CHLG",
        "Right to challenge NICS denial — written explanation and appeal",
        (
            "Any person denied a firearm purchase through the National Instant Criminal "
            "Background Check System (NICS) has the right to receive a written "
            "explanation of the specific basis for the denial and to file an "
            "administrative appeal within 30 days of the denial. The appeal process "
            "must be accessible, timely, and at no cost to the applicant."
        ),
        (
            "When someone is denied a gun purchase, they must receive a written "
            "explanation of why, and have 30 days to appeal the decision at no cost."
        ),
    ),
    (
        "GUNS", "CHLG",
        "Expedited appeal — identity mismatch and database error correction",
        (
            "Persons erroneously denied a firearm purchase based on identity mismatch "
            "or database error have the right to an expedited correction process "
            "completable within 72 hours. ATF bears the burden of proving the denial "
            "was correct. Interim relief pending correction is available upon "
            "demonstration of emergency need consistent with applicable law."
        ),
        (
            "When someone is denied a gun purchase because of a database mistake, they "
            "can request a fast 72-hour fix. The government must prove the denial was "
            "right, not the other way around."
        ),
    ),
    (
        "GUNS", "CHLG",
        "Judicial review — Article III review of final NICS denial",
        (
            "A final administrative denial of a firearm purchase is subject to de novo "
            "review by an Article III federal court. The person challenging the denial "
            "shall have access to the specific record basis for the denial. National "
            "security exceptions are reviewable by the court in camera to prevent "
            "abuse of the exception."
        ),
        (
            "If an appeal fails, the denied person can take the case to federal court. "
            "The court can review the evidence used to deny them, even if it is "
            "classified, to make sure the process was fair."
        ),
    ),
    # ── GUNS-CAPT ────────────────────────────────────────────────────────────
    (
        "GUNS", "CAPT",
        "ATF director independence — fixed term and for-cause removal only",
        (
            "The Director of the Bureau of Alcohol, Tobacco, Firearms and Explosives "
            "shall serve a fixed statutory term and may be removed only for cause. "
            "Senior ATF officials are subject to a five-year post-employment restriction "
            "on employment by or representation of the firearms industry."
        ),
        (
            "The head of ATF should have a fixed term in office and can only be fired "
            "for specific reasons, not political ones. Senior ATF officials cannot work "
            "for the gun industry for five years after leaving."
        ),
    ),
    (
        "GUNS", "CAPT",
        "Industry advisory panel limits — non-voting industry participation",
        (
            "Firearms industry representatives may participate in ATF regulatory advisory "
            "panels only in a non-voting advisory capacity. No ATF advisory panel may "
            "have a majority of members with financial ties to the firearms industry. "
            "Panel membership must be publicly disclosed."
        ),
        (
            "Gun industry representatives cannot control ATF advisory panels. They can "
            "share opinions but cannot vote, and must not make up the majority of any "
            "panel."
        ),
    ),
    (
        "GUNS", "CAPT",
        "Public interest representation — permanent seats on ATF advisory panels",
        (
            "ATF regulatory advisory panels must include permanent, funded seats for "
            "public health professionals with expertise in firearms violence, community "
            "violence intervention practitioners, and survivors of gun violence. These "
            "seats are not subject to reduction or elimination by executive action."
        ),
        (
            "Gun safety advocates, public health experts, and survivors of gun violence "
            "must have permanent seats on ATF advisory panels, and those seats cannot "
            "be removed by the administration."
        ),
    ),
    # ── CHKS-ENFC ────────────────────────────────────────────────────────────
    (
        "CHKS", "ENFC",
        "Enforcement cascade trigger — structural injunctions and congressional standing",
        (
            "When a co-equal branch of government fails to enforce constitutional limits "
            "on another branch, the judiciary retains authority to issue structural "
            "injunctions compelling compliance. Congressional standing to sue the "
            "executive branch for unconstitutional usurpation of legislative authority "
            "is established by statute."
        ),
        (
            "When one branch of government fails to check another, courts can step in "
            "and order compliance. Congress also has the legal right to sue the "
            "executive branch when the executive oversteps its authority."
        ),
    ),
    (
        "CHKS", "ENFC",
        "Anti-entrenchment — no provision may prevent future democratic authority",
        (
            "No congressional procedural rule, executive order, or agency regulation "
            "may be designed to prevent or structurally impede future elected majorities "
            "from exercising their constitutional authority. Such provisions are void "
            "as a matter of constitutional law and unenforceable."
        ),
        (
            "No law, rule, or executive order can be written to prevent future elected "
            "officials from changing it through normal democratic processes. Rules "
            "designed to entrench power are invalid."
        ),
    ),
    (
        "CHKS", "ENFC",
        "Emergency power limits — 90-day cap and congressional extension requirement",
        (
            "Executive emergency powers must specify a termination date not to exceed "
            "90 days from declaration. Extension beyond 90 days requires an affirmative "
            "vote of Congress. Federal courts retain jurisdiction to review the scope "
            "and factual basis of a declared emergency even during the emergency period."
        ),
        (
            "Presidential emergency powers last no more than 90 days unless Congress "
            "votes to extend them. Courts can review emergency declarations at any "
            "time to make sure they are being used appropriately."
        ),
    ),
    (
        "CHKS", "ENFC",
        "Enforcement actor independence — IGs, GAO, and CBO as congressional officers",
        (
            "Inspectors general, the Government Accountability Office, and the "
            "Congressional Budget Office are officers of Congress. They may not be "
            "removed by the executive except for cause determined by a bipartisan "
            "congressional panel. Their funding may not be reduced below the prior-year "
            "level through executive impoundment."
        ),
        (
            "Independent watchdog agencies like the GAO, CBO, and inspector generals "
            "serve Congress — not the President — and cannot be fired or defunded by "
            "the executive branch."
        ),
    ),
    (
        "CHKS", "ENFC",
        "Failure consequence — systematic defiance of courts triggers impeachment inquiry",
        (
            "Systematic executive refusal to comply with or enforce judicial orders "
            "triggers a mandatory impeachment inquiry by the House Judiciary Committee. "
            "Upon referral by the Committee, the Senate must commence trial proceedings "
            "within 60 days. Delay of trial proceedings by Senate leadership is subject "
            "to judicial mandamus."
        ),
        (
            "If a president repeatedly ignores court orders, the House must start an "
            "impeachment investigation, and the Senate must hold a trial within "
            "60 days of referral."
        ),
    ),
    # ── CHKS-AIGV ────────────────────────────────────────────────────────────
    (
        "CHKS", "AIGV",
        "AI in executive decision-making — disclosure and right to human review",
        (
            "Any executive agency use of AI systems in decisions that affect individual "
            "rights — including benefits determinations, enforcement actions, and "
            "regulatory classifications — must be disclosed to the affected person. "
            "Persons affected by AI-assisted agency decisions have a right to request "
            "human review of that decision."
        ),
        (
            "When a federal agency uses AI to make a decision affecting someone's "
            "rights or benefits, that person must be told, and can ask for a human "
            "to review the decision."
        ),
    ),
    (
        "CHKS", "AIGV",
        "AI surveillance of political opponents — federal crime",
        (
            "Use of federal intelligence or law enforcement AI tools to monitor "
            "political opponents, journalists, or civil society organizations based "
            "on protected political activity, association, or expression is prohibited. "
            "Directing or ordering such use is a federal crime punishable by "
            "imprisonment and permanent disqualification from federal employment."
        ),
        (
            "Using federal AI surveillance tools to spy on political opponents, "
            "journalists, or advocacy groups based on their political activity is a "
            "federal crime."
        ),
    ),
    (
        "CHKS", "AIGV",
        "Algorithmic redistricting — full disclosure and partisan optimization prohibited",
        (
            "AI-generated redistricting plans must be disclosed in full, including the "
            "optimization criteria, weighting, and training data used. Redistricting "
            "plans that use AI to optimize for partisan electoral outcomes are subject "
            "to strict scrutiny and shall be presumed unconstitutional unless the "
            "state demonstrates a compelling non-partisan justification."
        ),
        (
            "When AI is used to draw district maps, all the rules and data it used "
            "must be made public. Using AI to draw maps that give one party an "
            "advantage is presumed unconstitutional."
        ),
    ),
    # ── RGHT-ENFC ────────────────────────────────────────────────────────────
    (
        "RGHT", "ENFC",
        "Primary enforcement actors — DOJ, EEOC, HHS OCR, and state agencies",
        (
            "Primary enforcement actors for civil rights and civil liberties policy are: "
            "DOJ Civil Rights Division (federal rights violations and pattern-or-practice "
            "investigations), EEOC (employment discrimination), HHS Office for Civil "
            "Rights (healthcare discrimination), and state civil rights agencies "
            "(concurrent jurisdiction). Each actor maintains an independent complaint "
            "intake process accessible to the public."
        ),
        (
            "Multiple federal and state agencies each have their own role in enforcing "
            "civil rights laws, and each must have its own way for the public to report "
            "violations."
        ),
    ),
    (
        "RGHT", "ENFC",
        "Trigger conditions — pattern-or-practice, individual complaints, civil society",
        (
            "Enforcement is triggered by: documented pattern-or-practice violations by "
            "public or private actors, individual complaints meeting a threshold of "
            "credibility and specificity, civil society reporting with corroborating "
            "evidence, judicial referral, or inspector general findings. Any single "
            "trigger condition is sufficient to open an investigation."
        ),
        (
            "Civil rights enforcement can be started by a pattern of violations, "
            "individual complaints, reports from advocacy organizations, court "
            "referrals, or watchdog findings — and any one of these is enough."
        ),
    ),
    (
        "RGHT", "ENFC",
        "Failure consequence — congressional reporting, mandamus, and IG review",
        (
            "Failure to investigate credible pattern-or-practice civil rights violations "
            "triggers: mandatory reporting by the agency to Congress within 30 days, "
            "the right of civil society organizations to petition for a writ of mandamus "
            "to compel investigation, and referral for independent review by the "
            "relevant department's inspector general."
        ),
        (
            "If civil rights agencies fail to investigate credible violations, they must "
            "report to Congress within 30 days, and advocacy groups can sue to force an "
            "investigation."
        ),
    ),
    (
        "RGHT", "ENFC",
        "Private right of action — qualified immunity abolished for constitutional violations",
        (
            "Individuals whose civil rights are violated shall have a private right of "
            "action in federal court. Qualified immunity for federal officers sued for "
            "constitutional violations is abolished. State officers are subject to the "
            "same standard. Prevailing plaintiffs are entitled to attorneys' fees."
        ),
        (
            "People whose civil rights are violated can sue in federal court. Federal "
            "and state officials cannot use 'qualified immunity' to avoid being held "
            "accountable for violating constitutional rights."
        ),
    ),
    (
        "RGHT", "ENFC",
        "Anti-retaliation — personal liability and automatic removal for retaliation",
        (
            "Any federal official who retaliates against a person for exercising civil "
            "rights, filing a civil rights complaint, or testifying in a civil rights "
            "proceeding is subject to personal civil liability and automatic removal "
            "from federal employment. Mandatory arbitration of retaliation claims "
            "against federal employers is prohibited."
        ),
        (
            "Federal officials who punish people for asserting their civil rights or "
            "filing complaints can be personally sued and must be removed from their "
            "jobs. They cannot force retaliation cases into private arbitration."
        ),
    ),
]


def get_max_seq(cur: sqlite3.Cursor, domain: str, subdomain: str) -> int:
    cur.execute(
        "SELECT COALESCE(MAX(seq), 0) FROM positions WHERE domain = ? AND subdomain = ?",
        (domain, subdomain),
    )
    row = cur.fetchone()
    return row[0] if row else 0


def ensure_subdomain(cur: sqlite3.Cursor, code: str, domain: str, name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM subdomains WHERE code = ? AND domain = ?", (code, domain)
    )
    if cur.fetchone():
        return False
    cur.execute(
        "INSERT INTO subdomains (code, domain, name) VALUES (?, ?, ?)",
        (code, domain, name),
    )
    return True


def ensure_position(
    cur: sqlite3.Cursor,
    position_id: str,
    domain: str,
    subdomain: str,
    seq: int,
    short_title: str,
    full_statement: str,
    plain_language: str,
) -> bool:
    cur.execute("SELECT 1 FROM positions WHERE id = ?", (position_id,))
    if cur.fetchone():
        return False
    cur.execute(
        """INSERT INTO positions
               (id, domain, subdomain, seq, short_title, full_statement,
                plain_language, is_cross_domain, status, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'CANONICAL', datetime('now'), datetime('now'))""",
        (
            position_id,
            domain,
            subdomain,
            seq,
            short_title,
            full_statement,
            plain_language,
        ),
    )
    return True


def run() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    subdomain_added: int = 0
    subdomain_skipped: int = 0
    per_pillar: dict[str, int] = {}
    total_added: int = 0
    total_skipped: int = 0

    # Insert new subdomains
    for code, domain, name in NEW_SUBDOMAINS:
        added = ensure_subdomain(cur, code, domain, name)
        if added:
            subdomain_added += 1
            print(f"  + subdomain {domain}-{code}: {name}")
        else:
            subdomain_skipped += 1

    # Track running seq per (domain, subdomain) to assign IDs incrementally
    seq_cache: dict[tuple[str, str], int] = {}

    for domain, subdomain, short_title, full_statement, plain_language in NEW_POSITIONS:
        key = (domain, subdomain)
        if key not in seq_cache:
            seq_cache[key] = get_max_seq(cur, domain, subdomain)
        seq_cache[key] += 1
        seq = seq_cache[key]
        position_id = f"{domain}-{subdomain}-{seq:04d}"

        added = ensure_position(
            cur,
            position_id,
            domain,
            subdomain,
            seq,
            short_title,
            full_statement,
            plain_language,
        )
        if added:
            per_pillar[domain] = per_pillar.get(domain, 0) + 1
            total_added += 1
            print(f"  + {position_id}: {short_title[:60]}")
        else:
            total_skipped += 1
            print(f"  ~ SKIP {position_id} (already present)")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("P3 remediation summary")
    print("=" * 60)
    print(f"Subdomains added:   {subdomain_added}")
    print(f"Subdomains skipped: {subdomain_skipped}")
    print()
    print("Positions added per pillar:")
    for domain in sorted(per_pillar):
        print(f"  {domain}: {per_pillar[domain]}")
    print(f"\nTotal positions added:   {total_added}")
    print(f"Total positions skipped: {total_skipped}")


if __name__ == "__main__":
    run()
