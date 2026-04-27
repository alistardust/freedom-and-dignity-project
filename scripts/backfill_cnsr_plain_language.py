#!/usr/bin/env python3
"""Backfill plain_language text for all 177 CNSR policy positions.

Updates both:
  - data/policy_catalog_v2.sqlite (plain_language column)
  - docs/pillars/consumer-rights.html (rule-plain paragraph)
"""

import re
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
HTML_PATH = REPO_ROOT / "docs" / "pillars" / "consumer-rights.html"

# fmt: off
PLAIN_LANGUAGE: dict[str, str] = {
    # ── AGRS: Agricultural Equipment Right to Repair ──────────────────────────
    "CNSR-AGRS-0001": (
        "Farmers must be able to fully diagnose problems with their own equipment, "
        "just like a mechanic reads a car's error codes. Without this access, a "
        "broken tractor sits idle until the manufacturer's dealer is available."
    ),
    "CNSR-AGRS-0002": (
        "Equipment makers cannot force farmers to use only their own authorized "
        "dealers for repairs. You own the machine — you should be able to fix it "
        "yourself or hire whoever can get the job done."
    ),
    "CNSR-AGRS-0003": (
        "Manufacturers cannot use software to lock farmers out of repairing their "
        "own equipment. A software lock that blocks a lawful repair is prohibited."
    ),
    "CNSR-AGRS-0004": (
        "Equipment cannot be programmed to break down or run poorly just because "
        "you had it repaired by someone other than the manufacturer's dealer. "
        "Your repair choice cannot trigger artificial penalties."
    ),
    "CNSR-AGRS-0005": (
        "During planting or harvest season, a broken machine can cost a farmer "
        "an entire crop. Equipment must be repairable quickly — without artificial "
        "delays built into the repair system."
    ),
    "CNSR-AGRS-0006": (
        "Manufacturers cannot create systems that bottle up repairs during critical "
        "growing seasons. Repair must be accessible when farmers need it most."
    ),
    "CNSR-AGRS-0007": (
        "Repair parts, diagnostic tools, and service manuals must be available to "
        "farmers and independent shops at fair prices — not held hostage to inflate "
        "dealer service revenue."
    ),
    "CNSR-AGRS-0008": (
        "Buying a tractor means you own it — not just a license to use it under "
        "the manufacturer's rules. Contracts that turn equipment ownership into "
        "a limited-use license are prohibited."
    ),
    "CNSR-AGRS-0009": (
        "Contract clauses that try to stop you from repairing equipment you own "
        "are not legally binding. Your right to repair cannot be signed away in "
        "a purchase agreement."
    ),
    "CNSR-AGRS-0010": (
        "Manufacturers cannot use technical restrictions — like software locks or "
        "proprietary parts — to capture the entire repair market for their own "
        "equipment and shut out independent shops."
    ),
    "CNSR-AGRS-0011": (
        "When a repair restriction harms farmers during a critical season, "
        "regulators can act faster than normal to address it. Agricultural repair "
        "violations trigger an accelerated enforcement process."
    ),

    # ── ALGO: Algorithmic Pricing Fairness ────────────────────────────────────
    "CNSR-ALGO-0001": (
        "Pricing systems and targeting tools cannot produce discriminatory outcomes "
        "based on race, national origin, disability, or other protected "
        "characteristics — even if the algorithm never explicitly uses those labels."
    ),
    "CNSR-ALGO-0002": (
        "Companies cannot use pricing algorithms that charge more to people who "
        "appear financially desperate or otherwise vulnerable. Exploiting someone's "
        "hardship to extract higher prices is prohibited."
    ),
    "CNSR-ALGO-0003": (
        "You have the right to know when a company is using automated systems to "
        "shape what options you see or what prices you are offered. Algorithmic "
        "personalization must be disclosed."
    ),
    "CNSR-ALGO-0004": (
        "If an automated system makes a decision that harms you — like denying "
        "a loan or raising your rate — you must be able to get a human explanation "
        "of why. Purely opaque, unexplainable algorithmic decisions are prohibited."
    ),

    # ── ANTI: Anti-Competitive Repair Restrictions ────────────────────────────
    "CNSR-ANTI-0001": (
        "Manufacturers cannot limit all repairs to their own authorized service "
        "centers. Independent shops and consumers must be able to make lawful repairs "
        "without being locked out."
    ),
    "CNSR-ANTI-0002": (
        "Manufacturers cannot use digital rights management (DRM) or component "
        "pairing — chips that only recognize original parts — to block repairs "
        "you're otherwise allowed to make."
    ),
    "CNSR-ANTI-0003": (
        "Getting your device repaired by an independent shop does not void your "
        "warranty. A warranty can only be denied if the independent repair actually "
        "caused the problem you're claiming."
    ),

    # ── ANTS: Anti-Obsolescence Design ───────────────────────────────────────
    "CNSR-ANTS-0001": (
        "Products must be built to last and to be fixed, not designed to break "
        "down so consumers have to buy replacements. Planned obsolescence — "
        "deliberately engineering short lifespans — is prohibited."
    ),

    # ── ARBT: Arbitration ────────────────────────────────────────────────────
    "CNSR-ARBT-0001": (
        "When you sign a contract with a company, they cannot bury a clause that "
        "strips your right to sue them or join a class action. Pre-dispute mandatory "
        "arbitration clauses in consumer contracts and employment agreements are "
        "banned."
    ),
    "CNSR-ARBT-0002": (
        "If a company uses arbitration to resolve disputes, it must be clearly "
        "explained, genuinely voluntary, and conducted by a neutral arbitrator — "
        "not one hand-picked by the company. Outcomes must be published."
    ),

    # ── AUTO: Vehicle Ownership & Software ───────────────────────────────────
    "CNSR-AUTO-0001": (
        "Basic car functions — starting the engine, adjusting the climate, locking "
        "the doors — cannot be locked behind a monthly subscription fee. Core "
        "vehicle functions come with the car you purchased."
    ),
    "CNSR-AUTO-0002": (
        "Automakers cannot put safety-critical features like automatic emergency "
        "braking or lane-keep assist behind a paywall. Safety features must be "
        "fully included, not sold as add-on subscriptions."
    ),
    "CNSR-AUTO-0003": (
        "If a car is advertised with driver assistance features, all of those "
        "features must be available and active when you buy it — not unlocked "
        "later for an extra fee."
    ),
    "CNSR-AUTO-0004": (
        "Automakers cannot push software updates that make your car slower, less "
        "fuel efficient, or less capable than it was when you bought it. "
        "Updates must not degrade performance."
    ),
    "CNSR-AUTO-0005": (
        "When a manufacturer updates your car's software, you must be clearly told "
        "what changed and given a meaningful option to reverse the update if you "
        "choose."
    ),
    "CNSR-AUTO-0006": (
        "A car company cannot remotely disable or restrict features of a vehicle "
        "you own without your consent. Remote interference with your vehicle "
        "requires your knowledge and agreement."
    ),
    "CNSR-AUTO-0007": (
        "If a feature was included when you bought your car, it cannot be removed "
        "later by a software update or policy change. What you purchased is yours "
        "to keep."
    ),
    "CNSR-AUTO-0008": (
        "Self-driving and semi-autonomous vehicle systems must meet public safety "
        "standards reviewed by independent experts — not just the manufacturer's "
        "own certification. Public safety comes before brand reputation."
    ),
    "CNSR-AUTO-0009": (
        "The data your car collects about your driving belongs to you. You have "
        "the right to access it, take it to another service, and have it deleted."
    ),

    # ── BNKR: Bankruptcy ──────────────────────────────────────────────────────
    "CNSR-BNKR-0001": (
        "Student loan debt can be eliminated through bankruptcy, just like credit "
        "card debt or medical bills. Current law makes student loans nearly "
        "impossible to discharge, trapping people in debt even after financial ruin."
    ),
    "CNSR-BNKR-0002": (
        "If medical bills have pushed you to financial collapse, you can wipe them "
        "out through bankruptcy without a waiting period or extra legal hurdles. "
        "Getting sick should not permanently destroy your financial future."
    ),
    "CNSR-BNKR-0003": (
        "Bankruptcy law must protect the things people need most: retirement "
        "savings, the home you live in, and the tools you use to earn a living. "
        "Dollar limits on these protections must be updated to reflect today's costs."
    ),

    # ── CFPS: CFPB Authority ──────────────────────────────────────────────────
    "CNSR-CFPS-0001": (
        "The Consumer Financial Protection Bureau (CFPB) — the agency that "
        "investigates banks and financial companies that harm consumers — must "
        "have independent funding so it cannot be defunded by Congress at industry's "
        "request."
    ),
    "CNSR-CFPS-0002": (
        "The CFPB must be able to investigate any financial company, no matter "
        "what charter or label they use to describe themselves. No company should "
        "escape oversight by calling itself something other than a bank."
    ),
    "CNSR-CFPS-0003": (
        "When the CFPB catches a company breaking the law, the people who were "
        "harmed must be paid back — not just the company fined. Enforcement must "
        "include real restitution to real consumers."
    ),
    "CNSR-CFPS-0004": (
        "The CFPB must supervise large nonbank financial companies — including "
        "app-based lenders, payday lenders, and buy-now-pay-later services. "
        "Being a tech company does not exempt you from financial consumer protection."
    ),
    "CNSR-CFPS-0005": (
        "Consumer complaints filed with the CFPB must be publicly available and "
        "broken down by demographics, geography, and product type. Transparency "
        "about who is being harmed — and how — enables accountability."
    ),

    # ── CNSS: Consumable Supply Restrictions ──────────────────────────────────
    "CNSR-CNSS-0001": (
        "Products cannot be designed to force you to buy only the manufacturer's "
        "branded supplies when safe, compatible alternatives exist. Artificial "
        "lock-in to proprietary consumables is prohibited."
    ),
    "CNSR-CNSS-0002": (
        "Products must support refillable and reusable options where technically "
        "feasible, and compatible third-party alternatives must be permitted."
    ),
    "CNSR-CNSS-0003": (
        "Printers, medical devices, and industrial equipment cannot use software "
        "or embedded chips to block you from using compatible, less expensive "
        "supplies — such as third-party ink cartridges or generic replacement parts."
    ),
    "CNSR-CNSS-0004": (
        "Using supply restrictions to create artificial shortages or inflate "
        "prices for consumables is prohibited as anticompetitive. Markets for "
        "supplies must remain open to competition."
    ),

    # ── COMS: Commercial Equipment ────────────────────────────────────────────
    "CNSR-COMS-0001": (
        "Business owners have the same right to repair their equipment as "
        "individual consumers. Commercial use does not forfeit your right to "
        "repair what you own."
    ),
    "CNSR-COMS-0002": (
        "Manufacturers cannot block business owners or independent technicians "
        "from accessing the diagnostic information needed to identify and fix "
        "a problem with a machine."
    ),
    "CNSR-COMS-0003": (
        "A machine's error codes and fault messages must be accurate. Manufacturers "
        "cannot program equipment to obscure problems or produce misleading "
        "diagnostic readouts that hide the real issue."
    ),
    "CNSR-COMS-0004": (
        "In areas where authorized repair centers are scarce or unavailable, "
        "manufacturers cannot restrict all repairs to those centers. Access "
        "to repair must be practical, not just technically permitted."
    ),
    "CNSR-COMS-0005": (
        "Manufacturers cannot use software to force business owners to use "
        "only manufacturer-approved repair and service providers. Software-enforced "
        "service monopolies are prohibited."
    ),
    "CNSR-COMS-0006": (
        "Equipment cannot be designed in a way that predictably causes extended "
        "downtime during repair. Design choices that predictably harm business "
        "operations through unnecessary repair delays are prohibited."
    ),
    "CNSR-COMS-0007": (
        "If equipment repeatedly breaks down because design choices prevent "
        "proper repair, that pattern can be reviewed and challenged by regulators."
    ),
    "CNSR-COMS-0008": (
        "Manufacturers cannot hide how to repair their equipment or conceal "
        "known faults from the technicians who service it. Repair pathways "
        "must be transparent."
    ),
    "CNSR-COMS-0009": (
        "Manufacturers cannot block the use of third-party diagnostic and repair "
        "tools. Independent repair must have access to the technical interfaces "
        "needed to service the equipment."
    ),
    "CNSR-COMS-0010": (
        "Manufacturers cannot take active steps to undermine or interfere with "
        "independent repair services or third-party repair tools. Competition "
        "in repair markets must be protected."
    ),

    # ── CRDS: Credit Reporting ────────────────────────────────────────────────
    "CNSR-CRDS-0001": (
        "Credit reporting agencies must keep your file accurate, genuinely "
        "investigate when you dispute an error — not just rubber-stamp what "
        "the creditor says — and promptly correct verified mistakes."
    ),
    "CNSR-CRDS-0002": (
        "Medical bills cannot appear on your credit report. Getting sick and "
        "receiving care should not damage your credit score."
    ),
    "CNSR-CRDS-0003": (
        "You have the right to see your own credit report and score for free, "
        "on an ongoing basis — not just once a year. Knowing what lenders "
        "see about you is your right."
    ),
    "CNSR-CRDS-0004": (
        "When you dispute an error on your credit report, the credit bureau "
        "must prove the information is correct — it is not your job to prove it "
        "wrong. Verified errors must be fixed within 30 days."
    ),
    "CNSR-CRDS-0005": (
        "Employers and landlords cannot use your credit score against you unless "
        "there is a specific, documented reason it is relevant to the job or "
        "rental. General credit checks for unrelated purposes are prohibited."
    ),
    "CNSR-CRDS-0006": (
        "If you are appealing a medical bill or applying for financial assistance "
        "from a hospital, debt collection on that bill must pause while the "
        "process is underway."
    ),
    "CNSR-CRDS-0007": (
        "Medical debt can be eliminated through bankruptcy without extra hurdles "
        "or special requirements. Overwhelming medical bills should not be a "
        "permanent financial sentence."
    ),

    # ── CRPT: Cryptocurrency Consumer Protection ──────────────────────────────
    "CNSR-CRPT-0001": (
        "Right now it is unclear whether the SEC or the CFTC (two different "
        "federal regulators) oversees different types of digital assets. Congress "
        "must pass a clear law to close this regulatory gap and protect consumers."
    ),
    "CNSR-CRPT-0002": (
        "Stablecoins — digital currencies pegged to the dollar — must be backed "
        "dollar-for-dollar by actual cash or Treasury securities, audited monthly, "
        "and insured like bank deposits so consumers don't lose their money."
    ),
    "CNSR-CRPT-0003": (
        "Any cryptocurrency exchange serving U.S. customers must register with "
        "federal regulators and keep customer funds strictly separate from "
        "company funds, so your crypto is protected if the exchange collapses."
    ),
    "CNSR-CRPT-0004": (
        "Rug pulls, pump-and-dump schemes, and wash trading in crypto markets "
        "are federal crimes. Victims can sue for triple their losses to "
        "compensate for harm and deter future fraud."
    ),
    "CNSR-CRPT-0005": (
        "The government will not use taxpayer money to bail out cryptocurrency "
        "exchanges, stablecoin issuers, or crypto platforms. Investors who "
        "take on speculative risk bear that risk themselves."
    ),
    "CNSR-CRPT-0006": (
        "Large cryptocurrency mining operations must register with the EPA and "
        "Department of Energy, disclose how much energy they consume, and are "
        "not eligible for federal energy subsidies."
    ),

    # ── DATA: Data Rights ─────────────────────────────────────────────────────
    "CNSR-DATA-0001": (
        "Companies that collect and sell your personal information — called data "
        "brokers — must register with the FTC and must honor a universal registry "
        "where you can opt out of having your data sold."
    ),
    "CNSR-DATA-0002": (
        "Every person has the right to demand that any data broker permanently "
        "delete all personal information it holds about them. Data brokers must "
        "honor these requests."
    ),
    "CNSR-DATA-0003": (
        "Data brokers can only collect and keep information that is actually "
        "necessary for a specific purpose they have disclosed. Collecting "
        "everything just in case is prohibited."
    ),
    "CNSR-DATA-0004": (
        "Companies cannot sell your health information, precise location history, "
        "financial data, or biometric data without your explicit written consent. "
        "Sensitive personal data requires your active permission to be sold."
    ),

    # ── DBRK: Data Broker Rights ──────────────────────────────────────────────
    "CNSR-DBRK-0001": (
        "All companies that sell or share your personal information must register "
        "with the FTC and must stop selling your data within 15 days of your "
        "opt-out request."
    ),
    "CNSR-DBRK-0002": (
        "Companies cannot sell or share your reproductive health data, mental "
        "health records, substance use history, or biometric data without your "
        "explicit, informed, and revocable consent."
    ),
    "CNSR-DBRK-0003": (
        "Companies cannot sell your precise location data to data brokers. "
        "If law enforcement uses a geofence warrant to track your location, "
        "you must be notified within 90 days."
    ),
    "CNSR-DBRK-0004": (
        "You have the right to request a free annual report from any company "
        "that holds your personal data, so you can see exactly what they know "
        "about you."
    ),

    # ── DBRS: Data Broker Registration & Standards ────────────────────────────
    "CNSR-DBRS-0001": (
        "Companies that compile and sell consumer profiles must register with "
        "a federal authority, disclose where they get their data and who they "
        "sell it to, and honor deletion and opt-out requests."
    ),
    "CNSR-DBRS-0002": (
        "Data brokers cannot sell information that could be used to discriminate "
        "against people, stalk them, or target vulnerable individuals. The data "
        "market cannot be a tool for harm."
    ),
    "CNSR-DBRS-0003": (
        "When data brokers compile profiles used to make decisions about jobs, "
        "credit, or housing, they must follow the same rules that apply to "
        "credit bureaus under federal law (the FCRA)."
    ),
    "CNSR-DBRS-0004": (
        "The FTC must create a single registry where you can opt out of all "
        "data broker activity at once. Brokers must comply within 72 hours, "
        "and violations cost at least $1,000 per occurrence — with a private "
        "right to sue."
    ),

    # ── DEBT: Debt Collection ─────────────────────────────────────────────────
    "CNSR-DEBT-0001": (
        "Debt collectors cannot sue you for debts that are past their legal "
        "time limit ('zombie debt'). Debt buyers must prove they actually own "
        "the debt before suing. Medical debt must be permanently removed from "
        "all consumer credit reports."
    ),
    "CNSR-DEBT-0002": (
        "Debt collectors cannot sue or collect on debts past the legal statute "
        "of limitations. They must tell you the full history of a debt before "
        "contacting you. Medical debt cannot be sold to third-party collectors."
    ),

    # ── DESS: Design for Repairability ────────────────────────────────────────
    "CNSR-DESS-0001": (
        "Products must be designed so they can be reasonably taken apart for "
        "repair without being destroyed in the process. Products glued shut "
        "to prevent repair are prohibited in categories where repair is expected."
    ),
    "CNSR-DESS-0002": (
        "Parts that wear out over time — like batteries, filters, or gaskets — "
        "must be replaceable on their own. You should not have to replace an "
        "entire device just because one component wore out."
    ),
    "CNSR-DESS-0003": (
        "Manufacturers must publicly rate how repairable their products are. "
        "A repairability score gives consumers information to choose products "
        "that will last longer and cost less to maintain."
    ),

    # ── DLRS: Dollar Store Food Access ───────────────────────────────────────
    "CNSR-DLRS-0001": (
        "Congress must give local governments the power to limit how many dollar "
        "stores can open in areas that already lack access to grocery stores "
        "(called 'food deserts'), so these communities can attract real food "
        "retail instead."
    ),
    "CNSR-DLRS-0002": (
        "Congress must require large discount retail chains to offer fresh produce "
        "or nutritious food options in their locations in communities that lack "
        "access to full grocery stores."
    ),

    # ── DRKS: Dark Patterns ───────────────────────────────────────────────────
    "CNSR-DRKS-0001": (
        "Companies cannot design websites or apps to trick or manipulate you into "
        "choices you didn't mean to make — like fake countdown timers, hidden "
        "cancel buttons, or confusing opt-out flows. Manipulative design is "
        "prohibited."
    ),
    "CNSR-DRKS-0002": (
        "If you can sign up for a subscription online, you must be able to cancel "
        "it the same way. Companies cannot force you to call a phone number or "
        "navigate to a buried page to cancel."
    ),
    "CNSR-DRKS-0003": (
        "Apps and websites must default to protecting your data, not sharing it. "
        "You have to actively choose to share — not actively choose not to. "
        "Privacy-protective defaults are required."
    ),
    "CNSR-DRKS-0004": (
        "Any checkbox consenting to data collection, marketing, or terms must be "
        "unchecked by default. Your consent must be something you actively give, "
        "not something buried in a pre-ticked box."
    ),

    # ── ELCS: Electronics Ownership ──────────────────────────────────────────
    "CNSR-ELCS-0001": (
        "The full computing power of hardware you purchased cannot be artificially "
        "limited and then unlocked only for a monthly fee. Performance you paid "
        "for cannot be subscription-gated."
    ),
    "CNSR-ELCS-0002": (
        "Software updates to devices you own cannot secretly make them slower or "
        "less capable. If an update reduces performance, you must be told and "
        "given the option to keep the previous version."
    ),
    "CNSR-ELCS-0003": (
        "When you buy a software license, the company cannot unilaterally revoke "
        "it later. Software you paid for is yours to keep and use."
    ),

    # ── ELDR: Elder Financial Protection ─────────────────────────────────────
    "CNSR-ELDR-0001": (
        "Banks and financial institutions must report suspected elder financial "
        "abuse to authorities and are allowed to temporarily freeze an account "
        "to protect an elderly customer while an investigation happens."
    ),
    "CNSR-ELDR-0002": (
        "Telemarketing calls targeting older adults must include a mandatory "
        "waiting period before any purchase is final, and seniors must be given "
        "the right to cancel what they agreed to."
    ),
    "CNSR-ELDR-0003": (
        "Stealing from or financially exploiting an elderly person is a federal "
        "crime, with harsher penalties when the abuser held a position of trust "
        "(called a fiduciary relationship) — like a caregiver or financial adviser."
    ),
    "CNSR-ELDR-0004": (
        "Every nursing home or senior care facility that receives Medicare or "
        "Medicaid funding must provide residents with an independent advocate — "
        "someone who works for the resident, not the facility."
    ),

    # ── ENFL: Enforcement ────────────────────────────────────────────────────
    "CNSR-ENFL-0001": (
        "When a company violates consumer product ownership rules, they must restore "
        "the features they took away, pay back affected consumers, and pay civil "
        "penalties proportionate to the harm caused."
    ),
    "CNSR-ENFL-0002": (
        "If a company illegally restricts features of something you own, you "
        "have the right to take them to court. Consumers have a private right "
        "of action for unlawfully restricted product functionality."
    ),
    "CNSR-ENFL-0003": (
        "Government regulators can legally compel manufacturers to hand over "
        "repair manuals, diagnostic tools, and parts when they have been "
        "unlawfully withheld from consumers and independent shops."
    ),
    "CNSR-ENFL-0004": (
        "Breaking consumer product ownership rules can result in financial "
        "penalties, consumer lawsuits, and court orders to immediately stop "
        "the prohibited behavior."
    ),
    "CNSR-ENFL-0005": (
        "A manufacturer cannot block a repair by vaguely claiming it is unsafe. "
        "They must specifically and concretely demonstrate what the safety risk "
        "is. Vague safety claims are not a valid reason to deny repair access."
    ),
    "CNSR-ENFL-0006": (
        "The right to repair applies broadly: cars, phones and computers, farm "
        "equipment, and medical devices are all covered by repair rights standards."
    ),
    "CNSR-ENFL-0007": (
        "When the federal government buys products, it must give preference to "
        "products that are built to last and can be repaired. Government purchasing "
        "power should support a repair-friendly economy."
    ),

    # ── FASH: Fashion Industry Transparency ───────────────────────────────────
    "CNSR-FASH-0001": (
        "Apparel companies must tell consumers where their clothes were made "
        "and under what conditions, creating accountability for labor and "
        "environmental practices in global supply chains."
    ),
    "CNSR-FASH-0002": (
        "Fashion brands must disclose the environmental impact of their clothing "
        "production. Consumers deserve to know the true cost — in carbon, water, "
        "and waste — of what they wear."
    ),

    # ── FEES: Fee Transparency ────────────────────────────────────────────────
    "CNSR-FEES-0001": (
        "Companies cannot add surprise charges after you have started a purchase. "
        "Hidden fees, junk fees, and drip pricing — where the full cost is only "
        "revealed at the end — are banned."
    ),
    "CNSR-FEES-0002": (
        "The total amount you will pay — including all taxes, service fees, and "
        "mandatory charges — must be shown clearly before you complete a "
        "transaction. No surprise totals at checkout."
    ),
    "CNSR-FEES-0003": (
        "Companies cannot use confusing billing cycles or automatic renewals "
        "to trap customers who did not intend to keep paying. Renewals must be "
        "clearly disclosed and easy to cancel."
    ),
    "CNSR-FEES-0004": (
        "Subscriptions and automatic renewals must be easy to cancel through the "
        "same channel you used to sign up — not a phone call to a number buried "
        "on page eight of a website."
    ),
    "CNSR-FEES-0005": (
        "Every fee you are required to pay must be included in the price shown "
        "the first time you see it. Resort fees, service charges, and mandatory "
        "surcharges cannot be hidden until the end. Consumers can sue for triple "
        "the amount of any illegally hidden fee."
    ),

    # ── FOOD: Food Access ─────────────────────────────────────────────────────
    "CNSR-FOOD-0001": (
        "Dollar store chains must offer fresh fruits and vegetables at locations "
        "in areas the USDA has designated as food deserts — communities where "
        "residents have limited access to fresh food."
    ),
    "CNSR-FOOD-0002": (
        "Federal financing must be available to bring full-service grocery stores "
        "to underserved communities that lack access to fresh, affordable food."
    ),

    # ── FTRS: Feature Lock Prohibition ───────────────────────────────────────
    "CNSR-FTRS-0001": (
        "If hardware is already built to support a feature, manufacturers cannot "
        "artificially disable it and then charge a subscription fee to turn it "
        "back on. You should not pay a monthly fee for something the device can "
        "already do."
    ),
    "CNSR-FTRS-0002": (
        "Any restriction on software features must have a real, documented "
        "justification — not just a business model built on artificial limits. "
        "Feature restrictions require legitimate technical or safety reasons."
    ),

    # ── GENL: General Consumer Protection ────────────────────────────────────
    "CNSR-GENL-0001": (
        "Consumer protection law applies to any deceptive, coercive, or unfair "
        "practice — even when the company claims each individual act seems minor. "
        "Systemic unfairness is prohibited even without a single dramatic incident."
    ),
    "CNSR-GENL-0002": (
        "Companies cannot build a business model around confusing customers, "
        "hiding fees, or making it hard to cancel. Profiting from confusion, "
        "hidden costs, and friction is itself a prohibited practice."
    ),
    "CNSR-GENL-0003": (
        "Every consumer has clear, enforceable rights: to understand what they're "
        "paying, to cancel what they signed up for, to repair what they own, "
        "and to get their data back."
    ),
    "CNSR-GENL-0004": (
        "Take-it-or-leave-it contracts cannot legally strip you of your "
        "fundamental consumer rights, no matter what the fine print says. "
        "Some rights cannot be signed away."
    ),
    "CNSR-GENL-0005": (
        "Forcing consumers to give up their right to sue a company — buried "
        "in the fine print of a contract — should be banned or at minimum "
        "tightly controlled. Mandatory arbitration clauses undermine consumer "
        "access to justice."
    ),
    "CNSR-GENL-0006": (
        "A company that tricks you into something by burying it in legal "
        "boilerplate is still breaking the law. Disclosure must be real and "
        "informed consent must be genuine — fine print is not a substitute "
        "for fairness."
    ),

    # ── GMBL: Gambling Consumer Protection ───────────────────────────────────
    "CNSR-GMBL-0001": (
        "Slot-machine-style 'skill game' terminals cannot operate unlicensed "
        "in gas stations, bars, and convenience stores. States that allow them "
        "must set a minimum age, require problem gambling disclosures, and "
        "impose per-session loss limits."
    ),
    "CNSR-GMBL-0002": (
        "Gambling terminals cannot be placed in businesses where minors are "
        "the primary customers. Gambling ads cannot target people under 21, "
        "and loyalty programs cannot reward gambling activity."
    ),
    "CNSR-GMBL-0003": (
        "All legal online sports betting must offer deposit limits, cooling-off "
        "periods, and a national self-exclusion registry. Platforms that use "
        "algorithms to target known problem gamblers face civil and criminal "
        "liability."
    ),

    # ── INDX: Indexed / Miscellaneous Consumer Protections ───────────────────
    "CNSR-INDX-0001": (
        "Timeshare contracts must give buyers a real way out. You cannot be "
        "bound to a timeshare for life, and your heirs cannot be forced to "
        "inherit your financial obligations after you are gone."
    ),
    "CNSR-INDX-0002": (
        "For-profit hospice companies that bill Medicare must be closely "
        "supervised to prevent fraud and ensure they only enroll patients "
        "who are genuinely eligible for end-of-life care."
    ),
    "CNSR-INDX-0003": (
        "Trucking companies cannot require drivers to lease their trucks under "
        "terms that leave them earning below minimum wage or effectively trapped "
        "in a cycle of debt to their employer."
    ),

    # ── LIFE: Product Lifespan ────────────────────────────────────────────────
    "CNSR-LIFE-0001": (
        "Consumer products must meet basic durability standards for their "
        "category. A product shouldn't break down far sooner than a reasonable "
        "person would expect based on what it's sold as."
    ),
    "CNSR-LIFE-0002": (
        "After you buy a product, the manufacturer must continue to provide "
        "updates, parts, and service for a minimum period. Ending support "
        "immediately after sale is not acceptable."
    ),
    "CNSR-LIFE-0003": (
        "Companies cannot use software updates or end-of-life policies to "
        "deliberately shorten the usable life of a product you own. Artificial "
        "obsolescence through software is prohibited."
    ),
    "CNSR-LIFE-0004": (
        "When a manufacturer stops supporting the software for a product, that "
        "product must still be able to function normally. You should not lose "
        "a working device just because the company ended its software support."
    ),

    # ── OWNS: Product Ownership ───────────────────────────────────────────────
    "CNSR-OWNS-0001": (
        "When you purchase a physical product, you get full access to everything "
        "it can do. Features built into the hardware cannot be locked away behind "
        "a subscription fee after you've already bought the device."
    ),
    "CNSR-OWNS-0002": (
        "Companies cannot take what you've already bought and convert it into "
        "a monthly payment requirement. Software locks, paywalls, and post-sale "
        "restrictions that erode what you own are prohibited."
    ),
    "CNSR-OWNS-0003": (
        "If a product you bought relies on a company's online servers to work, "
        "those features must keep working even if the company shuts down its "
        "service or goes bankrupt."
    ),
    "CNSR-OWNS-0004": (
        "If a company can remotely disable or shut down a product they sold you, "
        "they must tell you that before you buy. Marketing something as yours "
        "to own while secretly keeping a remote kill switch is deceptive."
    ),

    # ── PDLS: Predatory Lending ───────────────────────────────────────────────
    "CNSR-PDLS-0001": (
        "Loans with interest rates above a set ceiling — including all fees — "
        "are prohibited or must be rate-capped. High-cost predatory loans that "
        "trap people in debt are banned."
    ),
    "CNSR-PDLS-0002": (
        "Lenders cannot keep rolling a loan over repeatedly, trapping you in a "
        "cycle where you can never pay down what you owe. Debt traps through "
        "repeated rollovers are prohibited."
    ),
    "CNSR-PDLS-0003": (
        "When financial companies target economically vulnerable communities with "
        "predatory products, they face increased enforcement scrutiny and must "
        "pay back the consumers they harmed."
    ),
    "CNSR-PDLS-0004": (
        "Consumer loans are capped at 36% annual interest, including all fees. "
        "Lenders cannot use bank partnership arrangements to dodge this cap, "
        "and states can set stricter limits."
    ),
    "CNSR-PDLS-0005": (
        "Companies that manage student loan repayment must follow legal standards "
        "to protect borrowers, including helping distressed borrowers enroll "
        "in income-driven repayment. Servicers who misroute payments or wrongly "
        "deny relief can be sued."
    ),
    "CNSR-PDLS-0006": (
        "Before taking out a reverse mortgage — a loan that draws on your home's "
        "value — you must receive independent counseling. Lenders cannot steer "
        "you toward their own products, and your heirs are protected from "
        "owing more than the home is worth."
    ),
    "CNSR-PDLS-0007": (
        "'Buy now, pay later' services are subject to the same consumer protection "
        "rules as credit cards — they must disclose the true cost in APR terms "
        "and cannot collect debt while a consumer dispute is pending."
    ),

    # ── PRDT: Predatory Lending Rate Caps ─────────────────────────────────────
    "CNSR-PRDT-0001": (
        "No loan to a consumer can charge more than 36% annual interest, "
        "including all fees and charges. This applies to every lender, "
        "with no exceptions or loopholes."
    ),
    "CNSR-PRDT-0002": (
        "Payday lenders, auto title lenders, and high-cost installment lenders "
        "must verify that a borrower can actually afford to repay before "
        "handing over the money. Lending to people who cannot repay is prohibited."
    ),
    "CNSR-PRDT-0003": (
        "Companies that buy and collect debt must prove they own it, prove the "
        "amount is accurate, and cannot attempt to collect on debts that are "
        "past the legal time limit. Old debt cannot be revived."
    ),
    "CNSR-PRDT-0004": (
        "Auto lenders cannot use 'spot delivery fraud' — driving off the lot "
        "before financing is final and then changing the terms — or use a GPS "
        "device to remotely disable your car as a collection tactic without "
        "strict legal safeguards."
    ),

    # ── PRED: Prediction Markets ──────────────────────────────────────────────
    "CNSR-PRED-0001": (
        "Placing financial bets on the outcomes of elections is absolutely "
        "prohibited on any federally regulated prediction market. Election "
        "integrity cannot be subjected to financial speculation."
    ),
    "CNSR-PRED-0002": (
        "Online platforms where you bet on real-world events — like who will "
        "win an election or how a company will perform — must be regulated as "
        "financial products, with full consumer protections."
    ),
    "CNSR-PRED-0003": (
        "Platforms that run prediction markets must tell users that the platform "
        "itself sets the odds, what fees are charged, and what financial risks "
        "they are taking. Transparency is required."
    ),

    # ── QLTS: Product Quality ─────────────────────────────────────────────────
    "CNSR-QLTS-0001": (
        "Products must meet basic durability and safety standards appropriate "
        "for how they are sold and what they are meant to do. A product that "
        "fails well below reasonable expectations fails this standard."
    ),
    "CNSR-QLTS-0002": (
        "If a product's marketing claims do not match its actual quality, "
        "that is a violation. Products must perform as reasonably promised."
    ),
    "CNSR-QLTS-0003": (
        "When a pattern of low-quality manufacturing harms consumers, "
        "regulators can review and challenge those practices — not just "
        "wait for individual complaints."
    ),
    "CNSR-QLTS-0004": (
        "Essential household goods — the things families rely on daily — must "
        "meet stronger baseline quality standards, so people are not repeatedly "
        "replacing goods that should last."
    ),

    # ── REHB: Addiction Treatment Consumer Protections ───────────────────────
    "CNSR-REHB-0001": (
        "Addiction treatment centers must offer treatment approaches proven by "
        "scientific research to work, such as medication-assisted treatment. "
        "Centers cannot offer only ineffective or unproven methods."
    ),
    "CNSR-REHB-0002": (
        "Paying or receiving payments to steer patients to a particular addiction "
        "treatment center — known as 'patient brokering' — is a federal crime. "
        "Profit cannot come before patient welfare."
    ),
    "CNSR-REHB-0003": (
        "Sober living homes must be registered and meet minimum state licensing "
        "standards. They cannot serve as pipelines to funnel residents to "
        "treatment centers in exchange for kickbacks."
    ),

    # ── RELI: Religious Organization Consumer Protections ────────────────────
    "CNSR-RELI-0001": (
        "The Federal Trade Commission has full authority to investigate and "
        "take action against religious organizations that use deceptive "
        "practices to solicit donations. Tax-exempt status does not exempt "
        "fraud."
    ),
    "CNSR-RELI-0002": (
        "Any religious organization that collects more than $10,000 in donations "
        "annually must tell donors how those funds are being used. Donors "
        "deserve transparency about where their money goes."
    ),
    "CNSR-RELI-0003": (
        "Religious organizations that specifically target elderly donors must "
        "follow enhanced consumer protection rules, recognizing the particular "
        "vulnerability of older adults to high-pressure solicitation."
    ),
    "CNSR-RELI-0004": (
        "Claiming that a donation will bring supernatural financial rewards "
        "is a form of wire fraud and mail fraud. These promises are not "
        "protected religious speech — they are illegal deception."
    ),
    "CNSR-RELI-0005": (
        "Manipulative, high-pressure donation tactics used in religious settings "
        "— like confining donors until they give or using emotional coercion — "
        "are prohibited consumer protection violations."
    ),

    # ── SUBS: Subscription Rights ─────────────────────────────────────────────
    "CNSR-SUBS-0001": (
        "Companies cannot convert products into subscriptions just to extract "
        "ongoing revenue when selling you full ownership would work just as well. "
        "Subscriptions must deliver genuine ongoing value, not just capture "
        "recurring payments."
    ),
    "CNSR-SUBS-0002": (
        "Before you pay, companies must clearly tell you whether you are buying "
        "something outright or subscribing to ongoing access. You have a right "
        "to know what kind of purchase you are making."
    ),
    "CNSR-SUBS-0003": (
        "A company cannot deliberately update your device to make it worse "
        "in order to pressure you into subscribing to a paid version. Degrading "
        "owned products to force a subscription conversion is prohibited."
    ),
    "CNSR-SUBS-0004": (
        "The basic functions of a device you own — the things that make it "
        "work as advertised — cannot be locked behind a monthly fee. Core "
        "functionality comes with the device you purchased."
    ),
    "CNSR-SUBS-0005": (
        "Subscription models are legitimate when they genuinely deliver an "
        "ongoing service that requires continuous resources — like cloud storage, "
        "live updates, or internet connectivity. The model must match the "
        "service."
    ),
    "CNSR-SUBS-0006": (
        "The difference between features you own permanently and features that "
        "require an ongoing subscription must be clearly disclosed when you "
        "buy the product. No surprises after purchase."
    ),
    "CNSR-SUBS-0007": (
        "If a free trial converts to a paid subscription, you must actively "
        "confirm you want to continue — after the trial ends. Charges made "
        "without that confirmation must be refunded within 5 business days."
    ),

    # ── SYSR: System-Level Right to Repair ────────────────────────────────────
    "CNSR-SYSR-0001": (
        "Owning a product means you have the right to repair it. Manufacturers "
        "cannot create unreasonable barriers — in hardware design or software — "
        "to fixing your own property."
    ),
    "CNSR-SYSR-0002": (
        "Repair manuals, diagnostic tools, and spare parts must be available "
        "to both consumers and independent repair shops at fair prices. Access "
        "to repair cannot be restricted to authorized dealers alone."
    ),
    "CNSR-SYSR-0003": (
        "Manufacturers cannot deliberately design products to be impossible to "
        "repair — for example, by gluing components together unnecessarily or "
        "using proprietary screws to block access."
    ),

    # ── TMSH: Timeshare ───────────────────────────────────────────────────────
    "CNSR-TMSH-0001": (
        "If you sign a timeshare contract, you have 15 days to cancel it "
        "for any reason — no penalties, no questions asked. This gives you "
        "time to review what you actually agreed to."
    ),
    "CNSR-TMSH-0002": (
        "After 10 years, timeshare owners must have a clear legal path to exit "
        "the contract. No one should be trapped in a timeshare indefinitely "
        "or stuck paying fees for decades."
    ),

    # ── TRAN: Transparency in Features ────────────────────────────────────────
    "CNSR-TRAN-0001": (
        "Companies must use clear, standardized labels showing which product "
        "features are fully included in the purchase price and which cost extra. "
        "You should know exactly what you are buying."
    ),
    "CNSR-TRAN-0002": (
        "A company cannot move features that were included when you bought "
        "a product behind a new paywall after the fact. Post-sale feature "
        "lock-outs require your consent and your right to cancel without penalty."
    ),

    # ── WARS: Warranty Rights ─────────────────────────────────────────────────
    "CNSR-WARS-0001": (
        "Warranties must be written in plain language, be fair, and actually "
        "be honored. Companies cannot use confusing terms or procedural traps "
        "to deny legitimate warranty claims."
    ),
    "CNSR-WARS-0002": (
        "When you buy a product, the manufacturer must tell you exactly how "
        "long they will provide support, updates, and replacement parts. "
        "Support timelines must be disclosed at the point of sale."
    ),
    "CNSR-WARS-0003": (
        "If a manufacturer stops supporting a product before their disclosed "
        "timeline, consumers are entitled to a remedy — such as a repair, "
        "replacement, or full refund."
    ),

    # ── ZDBT: Zombie Debt ─────────────────────────────────────────────────────
    "CNSR-ZDBT-0001": (
        "Congress must make it illegal to sue anyone for a debt that is past "
        "its legal time limit. Collectors cannot re-age old debts to make them "
        "look newer, and must disclose a debt's age before contacting you or "
        "filing a lawsuit."
    ),
}
# fmt: on


def update_database(updates: list[tuple[str, str]]) -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.executemany(
        "UPDATE positions SET plain_language = ?, updated_at = datetime('now') "
        "WHERE id = ?",
        updates,
    )
    conn.commit()
    affected = conn.total_changes
    conn.close()
    print(f"  DB: updated {affected} rows")


def update_html(updates: dict[str, str]) -> int:
    content = HTML_PATH.read_text(encoding="utf-8")
    insert_count = 0
    fill_count = 0

    for position_id, plain_text in updates.items():
        # Locate the card by its id attribute
        card_id_pattern = re.compile(
            r'id="' + re.escape(position_id) + r'"',
            re.DOTALL,
        )
        match = card_id_pattern.search(content)
        if not match:
            print(f"  HTML: WARNING — card {position_id} not found in HTML")
            continue

        card_start = match.start()

        # Find the end of this card's content block by locating the closing </div>
        # that corresponds to the opening <div ... id="CNSR-...">. We do a simple
        # forward scan to find the next closing </div> that isn't nested.
        # A simpler approach: find the next policy-card opening or section end.
        rest = content[card_start:]
        # Find all rule-plain within the next 2000 chars (well within one card)
        card_snippet = rest[:2000]

        # Case 1: already has non-empty rule-plain — skip entirely
        non_empty_plain = re.search(
            r'class="rule-plain"[^>]*>\s*[^\s<]', card_snippet
        )
        if non_empty_plain:
            continue

        # Case 2: empty <p class="rule-plain"></p> — fill it in
        empty_plain = re.search(
            r'(<p class="rule-plain">)(</p>)', card_snippet
        )
        if empty_plain:
            old = empty_plain.group(0)
            new = f'<p class="rule-plain">{plain_text}</p>'
            # Replace only the first occurrence after card_start
            pos_in_content = card_start + empty_plain.start()
            content = content[:pos_in_content] + new + content[pos_in_content + len(old):]
            fill_count += 1
            continue

        # Case 3: no rule-plain at all — insert after rule-title closing tag
        title_close = re.search(
            r'(class="rule-title"[^>]*>)(.*?)(</p>)',
            card_snippet,
            re.DOTALL,
        )
        if title_close:
            insertion_point = card_start + title_close.end()
            new_para = f'\n<p class="rule-plain">{plain_text}</p>'
            content = content[:insertion_point] + new_para + content[insertion_point:]
            insert_count += 1
            continue

        print(f"  HTML: WARNING — could not find insertion point for {position_id}")

    HTML_PATH.write_text(content, encoding="utf-8")
    print(f"  HTML: inserted {insert_count} new rule-plain paragraphs, "
          f"filled {fill_count} empty ones")
    return insert_count + fill_count


BATCH_SIZE = 50


def get_batch(batch_num: int) -> dict[str, str]:
    """Return the subset of PLAIN_LANGUAGE for the given 1-based batch number."""
    all_ids = list(PLAIN_LANGUAGE.keys())
    start = (batch_num - 1) * BATCH_SIZE
    end = start + BATCH_SIZE
    batch_ids = all_ids[start:end]
    return {pid: PLAIN_LANGUAGE[pid] for pid in batch_ids}


def total_batches() -> int:
    import math
    return math.ceil(len(PLAIN_LANGUAGE) / BATCH_SIZE)


def main() -> None:
    import sys

    batch_arg = None
    if len(sys.argv) > 1:
        try:
            batch_arg = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [batch_number]")
            sys.exit(1)

    if batch_arg is not None:
        subset = get_batch(batch_arg)
        print(
            f"Processing batch {batch_arg}/{total_batches()} "
            f"({len(subset)} entries: "
            f"{list(subset.keys())[0]} → {list(subset.keys())[-1]})"
        )
    else:
        subset = PLAIN_LANGUAGE
        print(f"Processing all {len(PLAIN_LANGUAGE)} CNSR plain language entries...")

    updates_for_db = [(text, pid) for pid, text in subset.items()]
    print("Updating database...")
    update_database(updates_for_db)

    print("Updating HTML...")
    update_html(subset)

    print("Done.")


if __name__ == "__main__":
    main()
