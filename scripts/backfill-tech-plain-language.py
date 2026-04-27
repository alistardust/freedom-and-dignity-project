#!/usr/bin/env python3
"""Backfill plain_language for all 499 TECH domain positions in DB and HTML."""

import re
import sqlite3
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
HTML_PATH = REPO_ROOT / "docs" / "pillars" / "technology-and-ai.html"

# fmt: off
PLAIN_LANGUAGE: dict[str, str] = {
    # AGES — Age Verification
    "TECH-AGES-0001": "Age verification systems that require government ID, biometrics, or persistent tracking to access legal online content are prohibited. People have the right to read and access information without being identified or tracked.",
    "TECH-AGES-0002": "Companies cannot build centralized databases of people's identities or browsing history just to verify age. Any age-check system must work without storing or sharing personal information.",
    "TECH-AGES-0003": "Privacy-preserving age checks — like on-device verification or anonymous credential systems — are permitted alternatives. These methods can confirm a user is old enough without revealing who they are.",
    "TECH-AGES-0004": "Any permitted age verification system must collect the least information possible and delete it immediately after the check. Holding on to identity data longer than necessary is prohibited.",
    "TECH-AGES-0005": "Age verification requirements can only apply to specific, high-risk types of content — not to the internet in general. This prevents age checks from becoming a tool for broad access control.",
    "TECH-AGES-0006": "Neither governments nor private companies may use age verification systems as cover for tracking, censoring, or monitoring people's online behavior.",

    # AINL — AI Accountability
    "TECH-AINL-0001": "AI systems with significant potential to affect people's lives or rights must go through a formal safety and accountability review before they can be used publicly.",
    "TECH-AINL-0002": "AI tools used in critical areas like healthcare, housing, employment, or policing must always have a human who is responsible for their decisions. No AI system can operate in these areas without human accountability.",
    "TECH-AINL-0003": "When an automated system makes an important decision about you, you have the right to know about it, get an explanation, appeal it, and have a human review it.",
    "TECH-AINL-0004": "When government agencies use AI to make decisions, those systems must be publicly documented, understandable, and open to independent inspection.",
    "TECH-AINL-0005": "The companies and people who build and deploy AI systems are legally responsible for harms those systems cause. They cannot avoid liability just because the decision was made by a machine.",
    "TECH-AINL-0006": "AI systems must be tested for problems like bias, safety failures, and potential misuse — both before they launch and after they are in use.",
    "TECH-AINL-0007": "Companies operating covered AI systems must publish documentation about those systems — what they do, how they were trained, and what risks they carry — appropriate to how dangerous they are.",
    "TECH-AINL-0008": "Governments and agencies cannot use secret AI decision systems to determine your rights, obligations, or access to services. The rules that govern decisions about you must be knowable.",

    # AISA — AI Safety
    "TECH-AISA-0001": "AI systems used in high-stakes areas — like healthcare, policing, or employment — must pass a federally certified safety review before they can be deployed. This protects people from harm caused by untested systems.",
    "TECH-AISA-0003": "AI tools used in the criminal justice system must be able to explain their decisions in plain terms. Predictive policing systems — which try to predict who might commit a crime — are banned.",

    # ALGO — Algorithmic Accountability
    "TECH-ALGO-0001": "When an AI or algorithm meaningfully affects what you see, whether you qualify for something, or what actions are taken on your account, you must be told that an algorithm is involved.",
    "TECH-ALGO-0002": "If an algorithm makes a decision that seriously harms you, you have the right to challenge it and ask for a review.",
    "TECH-ALGO-0003": "Where feasible, platforms must offer users a version of their service that is less personalized or not driven by algorithmic recommendations.",
    "TECH-ALGO-0004": "Algorithms designed to manipulate users by targeting psychological weaknesses — like fear, outrage, or addiction — for profit or political influence are banned.",
    "TECH-ALGO-0005": "Platforms must explain in plain terms what their recommendation and ranking systems are trying to optimize for — for example, engagement, recency, or relevance.",
    "TECH-ALGO-0006": "Independent researchers must be able to access platform data to study how algorithms affect people, subject to privacy protections.",

    # ANTS — Antitrust
    "TECH-ANTS-0001": "Patent rights cannot be used to block innovation or justify anti-competitive behavior in technology markets. Patents protect genuine invention, not market control.",
    "TECH-ANTS-0002": "Using patents as a tool to shut out competitors or prevent innovation is prohibited. Patent enforcement must be tied to legitimate protection of inventions, not business strategy.",

    # AUDT — Auditing
    "TECH-AUDT-0001": "AI systems that have significant potential to affect people must allow independent auditors to inspect them for safety, fairness, reliability, and potential for misuse.",
    "TECH-AUDT-0002": "If an AI-assisted decision harms you, you have the right to a meaningful explanation of how that decision was made and a path to seek redress.",
    "TECH-AUDT-0003": "Organizations using high-risk AI systems must keep detailed records of decisions so those decisions can be reviewed, investigated, or appealed later.",
    "TECH-AUDT-0004": "The government must maintain a public list of all AI systems it uses, with exceptions only for narrowly classified programs — and even those must be overseen by independent reviewers.",
    "TECH-AUDT-0005": "Even AI systems used in classified government settings must be independently reviewed by authorized oversight bodies. Being classified is not an excuse for avoiding accountability.",
    "TECH-AUDT-0006": "Before an AI system is deployed in a high-stakes area like healthcare, criminal justice, or housing, it must pass an independent audit to ensure it is fair and accurate.",
    "TECH-AUDT-0007": "If an AI system produces decisions that disproportionately harm a particular group, the people harmed have the right to sue in civil court.",

    # AUTS — Autonomous Systems
    "TECH-AUTS-0001": "Automated systems with a high risk of serious harm — such as restricting liberty or denying rights — must not be deployed unless strict protections are in place to prevent and address failures.",
    "TECH-AUTS-0002": "AI cannot replace the accountable human decision-maker in areas like healthcare, education, housing benefits, or employment. A human must always be responsible.",
    "TECH-AUTS-0003": "Fully automated systems that deny people benefits, care, housing, or legal status are prohibited unless human review and the right to appeal are guaranteed before any harm can occur.",
    "TECH-AUTS-0004": "Government agencies must always retain the ability for a human to override or escalate any automated decision. There must be clear procedures for when and how humans step in.",

    # BIOM — Biometric Privacy
    "TECH-BIOM-0001": "Federal law must establish Americans' right to control their own biometric data — such as fingerprints or face scans — including the right to consent before collection and to demand deletion afterward.",
    "TECH-BIOM-0002": "No company may collect, store, or use your biometric data — including your face, voice, fingerprint, iris, or the way you walk — without your explicit written consent. Selling or sharing biometric data is prohibited under any circumstances.",

    # BIOS — Biometric Surveillance
    "TECH-BIOS-0001": "Police and government agencies cannot use facial recognition technology to scan crowds or public spaces for general law enforcement purposes. This prevents widespread surveillance of people who have done nothing wrong.",
    "TECH-BIOS-0002": "Real-time scanning of crowds or protesters using facial recognition or other biometric technology is banned. People have the right to gather and protest without being identified by the government.",
    "TECH-BIOS-0003": "Biometric systems — like facial recognition or fingerprint scans — cannot be used as the standard way to verify identity when accessing legal content or participating in public life.",
    "TECH-BIOS-0004": "When biometric technology is permitted for a specific purpose, it must be strictly necessary, proportionate to the goal, open to independent review, and governed by clear rules about when data must be deleted.",
    "TECH-BIOS-0005": "Biometric data — like your face scan, fingerprints, or voice — is among the most sensitive kinds of personal information. It requires stronger consent requirements and stricter limits on how long it can be kept than regular personal data.",
    "TECH-BIOS-0006": "If police want to use facial recognition to investigate a specific suspect, they need an individual court-issued warrant and must have an independent expert review the results.",
    "TECH-BIOS-0007": "Genetic data is the most sensitive type of protected data. It cannot be sold to insurers, employers, or law enforcement without a court warrant.",

    # BRDS — Broadband
    "TECH-BRDS-0001": "Broadband internet is treated as a basic right. Government programs making it affordable must be permanent, and internet service cannot be cut off without a 30-day notice and help finding alternatives.",
    "TECH-BRDS-0002": "Every K–12 school must have high-speed internet, and students who lack devices or home internet access must receive them as a condition of federal education funding.",

    # CHDS — Child Digital Safety
    "TECH-CHDS-0001": "AI systems designed for children or likely to be used by them must meet higher standards for safety, privacy, and protection against manipulation or developmental harm.",
    "TECH-CHDS-0002": "AI companion apps and chatbots cannot be designed to create dependency or emotional reliance in children. These systems must not exploit children's emotional needs for commercial gain.",
    "TECH-CHDS-0003": "AI systems cannot pretend to be a child's friend, romantic partner, or parent figure. Simulated emotional relationships with children through AI are prohibited.",
    "TECH-CHDS-0004": "Apps and systems built for children cannot use manipulative design features — like streaks, rewards, or pressure tactics — engineered to keep kids engaged at the expense of their wellbeing.",
    "TECH-CHDS-0005": "AI systems used by children must collect as little data about them as possible. Unnecessary data collection from minors is prohibited.",
    "TECH-CHDS-0006": "Generative AI features with significant risks for minors — including anything sexually explicit — must be blocked for underage users. Platform age-gating for high-risk content is required.",
    "TECH-CHDS-0007": "AI systems used by children must include strong built-in safety controls. Developers cannot leave child safety as an optional feature to be added later.",
    "TECH-CHDS-0008": "Creating deepfake content involving minors or depicting school communities without consent is banned. This includes AI-generated images and videos that could be used for harassment or abuse.",
    "TECH-CHDS-0009": "Schools and parents must have clear, usable controls over how AI systems interact with children. Transparent tools for oversight and opt-out are required.",
    "TECH-CHDS-0010": "AI systems cannot replace qualified human support staff — like school counselors, mental health workers, or teachers — when children need real human support.",
    "TECH-CHDS-0011": "Platforms that offer child-facing AI systems must actively maintain strong content moderation and safety protections. Leaving children's safety to chance is not acceptable.",
    "TECH-CHDS-0012": "Researchers studying how AI affects children — including developmental and psychological impacts — must be supported and given access to data needed to protect children from harm.",

    # CYBS — Cybersecurity
    "TECH-CYBS-0001": "Companies that operate essential services like power grids, hospitals, or water systems must meet basic cybersecurity standards and report breaches within 24 hours. Minimum security practices protect everyone who depends on these systems.",
    "TECH-CYBS-0002": "Software companies whose products are used in critical infrastructure must fix known security flaws — and are legally liable if they don't. Patches and updates must be provided for at least five years.",
    "TECH-CYBS-0003": "Paying ransomware attackers connected to sanctioned countries or groups is illegal. All significant ransomware incidents must be reported to the FBI, helping authorities track and stop attacks.",

    # DATA — Data Systems
    "TECH-DATA-0001": "Government agencies cannot combine surveillance datasets from different sources into a unified system unless it is specifically authorized by law, subject to a judge's oversight, and disclosed publicly in general terms.",
    "TECH-DATA-0002": "Government and private actors cannot use AI to secretly build detailed behavioral profiles on individuals. Building such a profile requires specific legal cause and judicial approval.",
    "TECH-DATA-0003": "Government surveillance systems cannot be fed with bulk location data, biometric data, or behavioral data bought from commercial brokers. This closes a loophole that bypasses constitutional warrant requirements.",

    # DEEP — Deepfakes
    "TECH-DEEP-0001": "Creating or distributing fake explicit images of a real person without their consent — using AI or other tools — is a federal crime. This protects people from a devastating form of digital abuse.",
    "TECH-DEEP-0002": "Deepfake videos or audio recordings designed to deceive voters — for example, a fake video of a candidate saying something they never said — are illegal during elections.",

    # DEMS — Democracy Safeguards
    "TECH-DEMS-0001": "AI cannot be used to generate or spread fake election content designed to mislead voters about candidates, how to vote, polling locations, or election results.",
    "TECH-DEMS-0002": "Deepfake images, videos, or audio impersonating candidates or election officials in a way intended to deceive voters are prohibited.",
    "TECH-DEMS-0003": "AI-generated political ads must clearly show who made them, who paid for them, and that they were created with AI. Undisclosed AI content in political advertising is prohibited.",
    "TECH-DEMS-0004": "Platforms must have fast, effective systems to find and remove AI-generated fake election content before it spreads. The harm from election disinformation can be irreversible.",
    "TECH-DEMS-0005": "AI systems cannot be used to target individual voters with tailored messaging based on their psychology or personal data to manipulate their political views or voting behavior.",
    "TECH-DEMS-0006": "Political campaigns, parties, and major advocacy organizations must disclose when and how they use AI tools for targeting, messaging, or voter outreach.",
    "TECH-DEMS-0007": "AI cannot be used to impersonate voters, generate fake constituent messages, or simulate grassroots political support that does not actually exist.",
    "TECH-DEMS-0008": "Election administration agencies cannot rely on opaque AI tools to make decisions about voter rolls, ballot validity, or election processes without transparency and accountability.",
    "TECH-DEMS-0009": "AI tools used in running elections must be independently tested and documented, and their results must be auditable by human reviewers and election monitors.",
    "TECH-DEMS-0010": "AI systems cannot be used to suppress voter turnout — for example, through targeted misinformation about voting rules, locations, or eligibility.",
    "TECH-DEMS-0011": "Platforms and political advertisers cannot use generative AI to create personalized disinformation at scale. Mass production of AI-generated political propaganda is prohibited.",
    "TECH-DEMS-0012": "AI-generated content that affects elections must be preserved — not deleted — so that researchers and investigators can review what happened and hold bad actors accountable.",
    "TECH-DEMS-0013": "A publicly accessible database of identified AI-generated election disinformation must be maintained so researchers, journalists, and the public can study and track these threats.",
    "TECH-DEMS-0014": "Journalists, academic researchers, and election monitors must have the legal right to access data and tools needed to investigate AI-driven election interference.",
    "TECH-DEMS-0015": "AI content moderation systems used during elections must be carefully designed to avoid political bias or unfair censorship. Election-related moderation requires additional safeguards.",
    "TECH-DEMS-0016": "Emergency actions taken by platforms or government to address election-related AI content must be publicly justified and transparent, even when urgent. Crisis measures cannot be used as cover for censorship.",
    "TECH-DEMS-0017": "AI cannot be used to fabricate official documents, voting records, government announcements, or other materials that create false impressions about the conduct of an election.",

    # DTBR — Data Brokers
    "TECH-DTBR-0001": "Data brokers — companies that buy and sell people's personal data — must register with the federal government. They cannot sell your personal data without your explicit consent first. Health, location, and financial data can never be sold.",
    "TECH-DTBR-0002": "Advertisers cannot target you based on your health, political views, religion, sexual orientation, gender identity, immigration status, or financial troubles. Targeted advertising of any kind is permanently banned for anyone under 18.",
    "TECH-DTBR-0003": "Federal law must give all Americans clear rights over their own data — including the right to know what is collected, limit how it is used, and demand transparency from algorithms. An independent federal agency must enforce these rights.",

    # EDUS — Education
    "TECH-EDUS-0001": "AI tools in schools must help students learn — not replace teachers, undermine critical thinking, or create unfair advantages. Students' access to quality education must not depend on technology.",
    "TECH-EDUS-0002": "AI cannot take over the job of human teachers in K–12 or higher education. Direct teaching and mentorship require a human educator who can be held accountable.",
    "TECH-EDUS-0003": "AI systems may assist teachers and students, but they cannot substitute for qualified instruction or mentoring. Support tools are allowed; replacement is not.",
    "TECH-EDUS-0004": "Grades or evaluation outcomes that affect a student's future — like advancing to the next grade, earning a diploma, or disciplinary action — cannot be based solely on AI decisions. A human must be involved.",
    "TECH-EDUS-0005": "If an AI system affects your grade or academic evaluation, you have the right to request a human review of that decision.",
    "TECH-EDUS-0006": "Schools must have clear policies on how AI may and may not be used in learning. These policies must support genuine learning and cannot rely on AI detection tools that are known to be unreliable.",
    "TECH-EDUS-0007": "AI tools used in education must be tested to ensure they treat all students fairly. Tools that disadvantage students based on race, gender, disability, income, or language background are prohibited.",
    "TECH-EDUS-0008": "Every student must be able to use AI tools in the classroom, regardless of their background or resources. AI cannot make educational inequality worse.",
    "TECH-EDUS-0009": "When AI systems collect data about students, they may only collect what is actually needed for educational purposes. Gathering extra data about minors is not allowed.",
    "TECH-EDUS-0010": "Data collected from students through AI tools cannot be sold, shared with advertisers, or used to build profiles for non-educational purposes.",
    "TECH-EDUS-0011": "Children using AI in schools have stronger privacy protections than adults. Stricter rules apply to how student data is collected, stored, and used.",
    "TECH-EDUS-0012": "Schools cannot use AI to continuously monitor students, track their behavior, or analyze their bodies through biometric surveillance without a strong specific justification and protective safeguards.",
    "TECH-EDUS-0013": "AI systems cannot be used to infer how students are feeling, how attentive they are, or their psychological state as part of grading or discipline decisions.",
    "TECH-EDUS-0014": "Schools cannot use AI to assign behavioral compliance scores to students. Students are not subjects to be ranked by their conformity to automated expectations.",
    "TECH-EDUS-0015": "When educational content is AI-generated, students must be told. The limitations of AI-generated material must also be disclosed so students can evaluate it critically.",
    "TECH-EDUS-0016": "AI systems in education cannot impose a particular political or ideological viewpoint. Any attempt to use AI to shape students' beliefs without transparency or oversight is prohibited.",
    "TECH-EDUS-0017": "Education technology should strengthen students' ability to think critically and form their own judgments — not encourage passive acceptance of AI-generated answers.",
    "TECH-EDUS-0018": "AI tools that help students with disabilities — like transcription, translation, or adaptive learning — are encouraged. Accessibility benefits are a legitimate and important use of AI in education.",
    "TECH-EDUS-0019": "AI tools that help students learn in multiple languages are encouraged. Reducing language barriers improves equity — as long as the tools are accurate and fair across languages.",
    "TECH-EDUS-0020": "Schools must tell students, families, and the public when AI is being used in teaching, grading, or administrative decisions.",
    "TECH-EDUS-0021": "AI tools used in education must be regularly inspected by independent reviewers for accuracy, fairness, and whether they are actually helping students learn.",
    "TECH-EDUS-0022": "Technology companies that sell AI tools to schools cannot use business secrets as an excuse to avoid accountability or oversight of how their products work.",
    "TECH-EDUS-0023": "Before AI tools are rolled out to classrooms at scale, schools must have evidence that they actually improve learning outcomes. Unproven tools should not be experimented on students without safeguards.",
    "TECH-EDUS-0024": "Students cannot be used as unwitting test subjects for AI products. If a school wants to use students to test a new AI tool, families must be informed and given the opportunity to consent.",

    # ENVS — Environmental Standards
    "TECH-ENVS-0001": "AI companies must not pass their environmental costs — like power consumption, water use, or pollution — onto the public or the environment. They must operate within sustainable limits.",
    "TECH-ENVS-0002": "Large AI systems and data centers must be carbon neutral or carbon negative over their full life cycle. This means accounting for all emissions from building and running these systems, not just electricity use.",
    "TECH-ENVS-0003": "AI companies must publicly disclose how much energy their systems use, where it comes from, and how much pollution they produce. Transparency is required, not optional.",
    "TECH-ENVS-0004": "Large AI data centers must generate or procure their own clean energy, rather than drawing more from the shared electric grid and driving up costs and emissions for everyone else.",
    "TECH-ENVS-0005": "AI infrastructure operators must publicly disclose how much water their facilities use — including for cooling — and what impact that has on local water supplies.",
    "TECH-ENVS-0006": "AI data centers cannot be built or expanded in ways that strain local water supplies, especially in regions already facing drought or water scarcity.",
    "TECH-ENVS-0007": "The rare earth metals and other materials used to build AI hardware must be sourced responsibly, with strong environmental and labor protections throughout the supply chain.",
    "TECH-ENVS-0008": "AI hardware makers are responsible for the environmental impact of their products from production through disposal — not just during the use phase.",
    "TECH-ENVS-0009": "AI hardware must be designed to last, be repairable, and be reusable. Planned obsolescence that generates unnecessary electronic waste is prohibited.",
    "TECH-ENVS-0010": "Companies must provide responsible recycling and safe disposal programs for AI hardware and infrastructure components when those items reach end of life.",
    "TECH-ENVS-0011": "AI companies must pay for their own environmental impacts rather than shifting those costs to local communities, future generations, or ecosystems.",
    "TECH-ENVS-0012": "Large new AI data centers and infrastructure expansions must undergo formal environmental impact reviews before they can be approved and built.",
    "TECH-ENVS-0013": "AI can and should be used to help address climate change — for example, through climate modeling, environmental monitoring, and optimizing clean energy systems — but these uses must be transparent and accountable.",
    "TECH-ENVS-0014": "AI tools can be used to reduce energy and water waste in operations — but only if those optimizations don't create hidden environmental harms or unfairly shift burdens onto other communities.",
    "TECH-ENVS-0015": "AI systems may help upgrade and modernize the electrical grid and expand renewable energy — but these tools must operate transparently and serve the public interest, not just corporate efficiency goals.",
    "TECH-ENVS-0016": "AI companies cannot misrepresent their environmental performance by cherry-picking data, using unverifiable carbon offsets, or making sustainability claims that don't hold up to scrutiny.",
    "TECH-ENVS-0017": "Environmental reporting by AI companies must follow standardized, verifiable measurements. Inconsistent or self-selected metrics can hide real impacts.",
    "TECH-ENVS-0018": "AI data centers and infrastructure cannot be systematically placed in lower-income or marginalized communities to avoid scrutiny or accountability for their environmental harms.",
    "TECH-ENVS-0019": "The environmental costs of building AI hardware — like mining and manufacturing — cannot be pushed onto lower-income countries or regions that lack equivalent environmental protections.",
    "TECH-ENVS-0020": "Planning for AI infrastructure must be integrated with national strategies for grid modernization and renewable energy investment. AI's energy needs cannot be treated as separate from public energy policy.",
    "TECH-ENVS-0021": "Data centers must meet noise pollution standards that protect nearby communities. Local residents must have access to monitoring data and the ability to demand mitigation.",
    "TECH-ENVS-0022": "AI data centers that exceed defined water consumption limits must reduce usage, compensate affected communities, or face regulatory penalties.",
    "TECH-ENVS-0023": "AI data centers cannot be built or expanded in water-stressed regions without a rigorous review of the impact on local water availability and community needs.",
    "TECH-ENVS-0024": "AI data centers must not endanger local groundwater or underground water reserves. Protection of underground water sources is required.",
    "TECH-ENVS-0025": "AI data centers must use water recycling and reclamation systems where technically feasible. Wasting water that could be recovered is not acceptable.",
    "TECH-ENVS-0026": "AI data centers must have drought contingency plans that specify how they will reduce water consumption during water shortages without shifting burdens onto local communities.",
    "TECH-ENVS-0027": "Before a large AI data center is built or expanded, the local community must have a formal review process to assess the impact on water supply and other shared resources.",

    # FACE — Facial Recognition
    "TECH-FACE-0001": "Government agencies cannot use facial recognition to surveil people in public spaces. The government cannot track where you go or who you are based on your face in a crowd.",
    "TECH-FACE-0002": "Private companies cannot use facial recognition technology to identify or track people without first obtaining their clear, informed, and voluntary consent.",
    "TECH-FACE-0003": "All federal agencies are prohibited from using facial recognition until Congress passes a law setting standards for accuracy, transparency, and civil rights protections. Mass surveillance, immigration enforcement without a warrant, and monitoring of protests are permanently banned uses.",

    # FINC — Finance and Credit
    "TECH-FINC-0001": "AI tools used in finance, credit, and insurance must be fair, transparent, and non-discriminatory. Access to essential financial services cannot be undermined by opaque automated systems.",
    "TECH-FINC-0002": "AI cannot independently deny you a loan, mortgage, or other financial service. A qualified human must review and be accountable for any denial before it takes effect.",
    "TECH-FINC-0003": "Any decision to deny, restrict, or worsen your access to credit must be made directly by a human reviewer — not delegated to an AI. The human must make an independent judgment.",
    "TECH-FINC-0004": "AI systems that assess your creditworthiness must be able to explain how they reach their conclusions. Opaque or unexplainable criteria that affect financial decisions are not permitted.",
    "TECH-FINC-0005": "AI systems in lending and insurance cannot discriminate based on your race, gender, religion, or other protected characteristics — or based on zip code, language, or other stand-ins for those characteristics.",
    "TECH-FINC-0006": "AI systems used in lending, underwriting, and insurance must be regularly audited to check for discriminatory outcomes — including patterns that disproportionately harm particular groups.",
    "TECH-FINC-0007": "AI cannot independently deny, restrict, or cancel your insurance coverage. A human must review and be directly accountable for any adverse coverage or claims decision.",
    "TECH-FINC-0008": "Human reviewers making insurance decisions cannot simply rubber-stamp what an AI recommends. They must apply their own independent judgment.",
    "TECH-FINC-0009": "AI tools can be used to help approve insurance claims or coverage more efficiently — but they cannot be the primary reason a claim is denied, reduced, or restricted.",
    "TECH-FINC-0010": "The fact that an AI did not approve a claim cannot be used — even implicitly — as a reason to deny insurance or delay coverage. AI non-approval is not a valid justification for denial.",
    "TECH-FINC-0011": "AI systems in finance and insurance cannot use broad behavioral surveillance or assign social scores to determine your eligibility, pricing, or access. Your digital behavior cannot be used against you without specific legal authority.",
    "TECH-FINC-0012": "Risk scoring in finance and insurance must use transparent, lawful, and relevant factors. Systems that rely on opaque behavioral inference to score people are prohibited.",
    "TECH-FINC-0013": "AI systems cannot use detailed profiles of your personal vulnerabilities to charge you higher prices, fees, or unfavorable terms. Exploiting individual circumstances for profit is prohibited.",
    "TECH-FINC-0014": "AI tools used in mortgage lending and housing finance cannot reproduce patterns of historical discrimination. Fair access to housing-related financial services must be preserved.",
    "TECH-FINC-0015": "Tenant screening and other housing-related AI systems cannot rely on opaque scoring systems or unverifiable data. People's housing access cannot be blocked by black-box algorithms.",
    "TECH-FINC-0016": "When an AI system meaningfully influences a financial, credit, or insurance decision affecting you, you have the right to a plain-language explanation of how that decision was made.",
    "TECH-FINC-0017": "When an AI-influenced decision negatively affects your financial, credit, or insurance situation, you have the right to a timely appeal heard by a human reviewer.",
    "TECH-FINC-0018": "Companies using AI in consequential financial or insurance decisions must tell you when those systems played a meaningful role.",
    "TECH-FINC-0019": "AI systems in finance and insurance can only collect data about you that is actually necessary for a lawful and relevant decision. Collecting more than needed is prohibited.",
    "TECH-FINC-0020": "Financial and insurance data collected by AI systems cannot be sold, shared with advertisers, or repurposed for behavioral profiling unrelated to the original decision.",
    "TECH-FINC-0021": "Companies cannot secretly enrich your financial or insurance profile by adding data from third-party brokers, social media, or surveillance sources without explicit disclosure and legal authority.",
    "TECH-FINC-0022": "AI systems cannot trap people in self-reinforcing denial loops where a bad credit score blocks insurance, which blocks housing, which blocks benefits — all without independent human review and due process at each step.",
    "TECH-FINC-0023": "AI systems in finance and insurance must be regularly, independently audited for bias, fairness, legal compliance, and harm to consumers.",
    "TECH-FINC-0024": "Companies cannot use business secrets or proprietary claims to prevent regulators, courts, or affected people from understanding, challenging, or appealing AI-influenced financial decisions.",
    "TECH-FINC-0025": "Companies deploying consequential AI in finance and insurance must maintain detailed records sufficient to allow independent review, auditing, and accountability.",
    "TECH-FINC-0026": "AI systems cannot be used to identify and exploit people who are financially vulnerable — targeting them with predatory loans, fees, or insurance terms.",
    "TECH-FINC-0027": "AI systems in finance and insurance cannot pretend to be human advisors or misrepresent what authority they have or what obligations they carry. You have the right to know you are dealing with an automated system.",
    "TECH-FINC-0028": "When financial or insurance systems function as essential gateways to housing, healthcare, or basic economic participation, they must be governed by the highest public-interest standards — not just market incentives.",
    "TECH-FINC-0029": "AI systems cannot automatically exclude people from financial systems that are necessary for basic participation in society. Access to essential economic infrastructure must be protected.",

    # FMDS — Foundation Models
    "TECH-FMDS-0001": "Companies that build the most powerful AI models must register with a federal oversight body, disclose where their training data came from, and publish the results of safety tests before releasing the model.",
    "TECH-FMDS-0002": "AI developers must disclose whether their models were trained on copyrighted material, personal data, or data taken without consent. People have the right to request that their data be removed.",
    "TECH-FMDS-0003": "The most capable AI models must be adversarially tested — meaning experts try to find dangerous or harmful behaviors — before they can be released, and the results must be disclosed to federal oversight and independent reviewers.",
    "TECH-FMDS-0004": "Companies that deploy powerful AI models in high-risk applications must assess the specific risks of their application and report safety incidents to regulators.",
    "TECH-FMDS-0005": "AI models above a defined computational scale must register with NIST — the National Institute of Standards and Technology. Training data sources, known flaws, and adversarial safety test results must be publicly disclosed.",

    # GOVN — Government AI
    "TECH-GOVN-0001": "Government and public-service AI systems must uphold due process, equal protection, and transparency. AI cannot be used to undermine people's legal rights or access to services.",
    "TECH-GOVN-0002": "Government AI cannot independently cut off, reduce, or deny your access to public benefits, services, or legal status. Only a human official can make that call.",
    "TECH-GOVN-0003": "Any decision by the government to deny, reduce, or delay benefits or services must be made by a qualified human decision-maker — not delegated entirely to an automated system.",
    "TECH-GOVN-0004": "When humans review government AI decisions, they cannot simply repeat what the AI recommended. They must think independently and exercise real judgment.",
    "TECH-GOVN-0005": "Government can use AI to help identify who might be eligible for benefits or to process approvals more quickly — but AI cannot be the primary driver of denials or terminations.",
    "TECH-GOVN-0006": "If a government AI system affects your benefits, services, legal status, or rights, you have the right to a clear explanation of how that decision was made.",
    "TECH-GOVN-0007": "When a government AI system makes an adverse decision affecting you, you must have a realistic and timely way to appeal that decision to a human decision-maker.",
    "TECH-GOVN-0008": "Government agencies must openly disclose when AI systems materially shape decisions that affect the public. Hidden use of AI in government decision-making is prohibited.",
    "TECH-GOVN-0009": "The government cannot use AI to assign you a generalized risk score or trustworthiness rating to decide your access to public services or rights. Individual scoring for compliance or suspicion is prohibited.",
    "TECH-GOVN-0010": "Government AI systems cannot use your race, religion, gender, or other protected characteristics — or proxies for them — to infer whether you are eligible, suspicious, or dangerous.",
    "TECH-GOVN-0011": "The government cannot use AI to score or monitor your behavior, ideological views, or social conformity as a condition of receiving public services or benefits. Social scoring by government is prohibited.",
    "TECH-GOVN-0012": "Everyone must be able to speak with a human government representative for matters involving benefits, legal status, healthcare, housing, education, or other essential services. AI-only channels are not sufficient.",
    "TECH-GOVN-0013": "The government cannot force you into an AI-only service channel where the absence of a human would make it harder to be treated fairly, understand decisions, or contest them.",
    "TECH-GOVN-0014": "AI-powered public services must work for people with disabilities, low-income users, elderly people, and those with limited English proficiency. AI cannot create new barriers to accessing services.",
    "TECH-GOVN-0015": "AI systems cannot deny you disability benefits or override medical evidence from a licensed provider without transparent human review and the opportunity to challenge the decision.",
    "TECH-GOVN-0016": "The government cannot use AI to conduct mass sweeps looking for fraud or suspicion-based enforcement against people receiving benefits. These actions require individualized legal standards and human review.",
    "TECH-GOVN-0017": "AI systems cannot automatically terminate housing assistance, food assistance, healthcare coverage, disability support, or income benefits based on a statistical anomaly or behavioral prediction alone.",
    "TECH-GOVN-0018": "AI cannot independently decide someone's immigration status, order detention or deportation, rule on asylum claims, or determine family reunification. These decisions require a human official.",
    "TECH-GOVN-0019": "The government cannot use AI to infer whether someone applying for immigration or asylum status is telling the truth, presenting a danger, or has hidden intentions. These judgments require human review.",
    "TECH-GOVN-0020": "Any government decision about someone's immigration status or detention that was influenced by AI must be reviewed and finalized by a human official subject to due process and judicial oversight.",
    "TECH-GOVN-0021": "Private companies that supply AI systems to government must follow the same legal, constitutional, and ethical rules as the government itself. Government cannot outsource its obligations to private vendors.",
    "TECH-GOVN-0022": "A company's claim that its AI is a proprietary trade secret cannot be used to block oversight, prevent explanation of decisions, or prevent appeals in public-sector AI systems.",
    "TECH-GOVN-0023": "When government buys AI systems, the procurement process must be public, disclosing what the system does, its limitations, who built it, and how it will be overseen.",
    "TECH-GOVN-0024": "All major government AI systems must be regularly and independently audited for legal compliance, accuracy, bias, and impact on people's rights.",
    "TECH-GOVN-0025": "All government AI systems that affect rights, benefits, or legal status must be listed in a publicly accessible registry that describes what each system does and how it is overseen.",
    "TECH-GOVN-0026": "Government AI systems that affect rights or services must have expiration dates and must be periodically reauthorized through a public process. Indefinite authorization is not acceptable.",
    "TECH-GOVN-0027": "Government agencies cannot deploy AI in ways that affect the public without specific legal authority to do so and clear limits on how the system can be used.",
    "TECH-GOVN-0028": "Government cannot use the general public as uninformed test subjects for consequential AI experiments. Any testing must be lawful, transparent, and subject to ethical oversight.",
    "TECH-GOVN-0029": "People have the right not only to challenge a specific AI decision made against them, but also to challenge whether the AI system itself was legally authorized and valid.",

    # HARS — Harassment
    "TECH-HARS-0001": "Large social media platforms must actively detect and stop coordinated harassment campaigns, non-consensual intimate images, and other targeted abuse. Effective, consistent enforcement is required.",
    "TECH-HARS-0002": "Platform algorithms cannot amplify or recommend harassing or hate-based content. Recommendation systems that spread abuse at scale are prohibited.",
    "TECH-HARS-0003": "People who are targets of coordinated online harassment have enforceable rights — they can require platforms to respond and conduct an escalated review of their situation.",

    # IMMS — Immigration AI
    "TECH-IMMS-0001": "AI systems used to make immigration, detention, or deportation decisions must not operate as opaque black boxes. These decisions are too serious to be made by systems that cannot be reviewed or challenged.",
    "TECH-IMMS-0002": "AI-generated risk scores used to justify holding someone in immigration detention, denying their release, or separating families are banned.",

    # INFS — Infrastructure
    "TECH-INFS-0001": "AI systems used in critical infrastructure — like power grids, water systems, and transportation networks — must meet the highest standards for safety, security, resilience, and human control.",
    "TECH-INFS-0002": "AI systems cannot be deployed in critical infrastructure without passing rigorous safety and security reviews. The stakes are too high to allow untested systems near essential public services.",
    "TECH-INFS-0003": "Human operators must always have the ability to override or shut down AI systems managing critical infrastructure in real time. Removing that ability is prohibited.",
    "TECH-INFS-0004": "AI systems used in critical infrastructure must be comprehensively tested — including for failure modes and cybersecurity vulnerabilities — before being put into service.",
    "TECH-INFS-0005": "Critical infrastructure operators must maintain backup, non-AI operating modes that can keep systems running safely if AI systems fail or are compromised.",
    "TECH-INFS-0006": "AI-powered security tools can help detect and respond to cyberattacks on critical infrastructure — but humans must remain in control of the response.",
    "TECH-INFS-0007": "AI systems cannot be used to optimize critical infrastructure in ways that introduce new security vulnerabilities or reduce system resilience.",
    "TECH-INFS-0008": "When government or utilities buy AI systems for critical infrastructure, the contracts must require transparency, auditability, and accountability from the vendor.",
    "TECH-INFS-0009": "When an AI system in critical infrastructure fails or causes a safety incident, operators must report it to relevant authorities promptly so that lessons can be learned and shared.",
    "TECH-INFS-0010": "Operators of critical infrastructure cannot accept vendor claims that AI systems are too complex to explain or audit. Accountability for these systems cannot be waived.",
    "TECH-INFS-0011": "Essential public infrastructure using AI must maintain records of system decisions and operations sufficient for review, investigation, and accountability.",
    "TECH-INFS-0012": "Control of AI-enabled critical systems cannot be concentrated in a small number of hands. Monopolistic control over essential infrastructure creates dangerous single points of failure.",

    # INTL — Interoperability and Net Neutrality
    "TECH-INTL-0001": "Patent rights cannot be used to block interoperability, data portability, or the ability of competing systems to work together. Patents are not a tool for locking people in.",
    "TECH-INTL-0002": "Bypassing technical protections — like digital rights management — for the purpose of enabling competition, accessibility, or research is allowed and protected from liability.",
    "TECH-INTL-0003": "Patent law cannot be used to prevent people from using, accessing, or building compatible systems or products. Interoperability is a protected right.",
    "TECH-INTL-0004": "Internet service providers and the core infrastructure of the internet must be treated as neutral carriers — like telephone or postal services. They must carry all traffic equally.",
    "TECH-INTL-0005": "Network neutrality rules mean ISPs cannot favor or block traffic based on what the content is, who created it, where it is going, or for competitive or political reasons.",
    "TECH-INTL-0006": "Internet providers cannot slow down, block, or prioritize traffic to gain a competitive advantage, earn more money from certain content providers, or advance political goals.",
    "TECH-INTL-0007": "Network neutrality rules can have narrow exceptions for technical operations like managing network congestion, maintaining security, and ensuring reliability.",
    "TECH-INTL-0008": "Any exceptions to network neutrality must be publicly disclosed, independently auditable, and must not give any company or political actor an unfair advantage.",
    "TECH-INTL-0009": "Network neutrality protections must be written into law, not just regulatory rules. Regulations alone can be rolled back by a new administration; legal protections are more durable.",

    # JUDS — Judicial AI
    "TECH-JUDS-0001": "AI cannot be used to determine how long someone goes to prison, whether they get bail, or what punishment they receive in a criminal case.",
    "TECH-JUDS-0002": "AI systems cannot assign someone a score predicting how likely they are to commit another crime, how dangerous they are, or how likely they are to show up for court. These scores cannot be used in judicial decisions.",
    "TECH-JUDS-0003": "AI systems cannot be used to identify or profile potential jurors based on their behavior, psychology, or demographic background.",
    "TECH-JUDS-0004": "AI-generated or AI-analyzed evidence must meet strict standards for reliability and transparency, and defendants must have a full opportunity to challenge it before it is used in court.",
    "TECH-JUDS-0005": "Defendants and parties in legal proceedings have the right to examine and challenge any AI system used to generate or analyze evidence in their case — including how it works and what data it used.",
    "TECH-JUDS-0006": "AI may be used to help find wrongful convictions, identify errors, and speed up the appeals process for people who may have been unjustly imprisoned.",
    "TECH-JUDS-0007": "AI can be used to identify patterns of systemic bias in sentencing, policing, and prosecution — as a tool for reform and corrective action, not for making decisions about individuals.",
    "TECH-JUDS-0008": "Judges and court staff cannot use AI to make final decisions about facts, the law, credibility of witnesses, or how cases should come out. These decisions must remain human.",
    "TECH-JUDS-0009": "AI may be used for clerical tasks in courts — like organizing documents and summarizing routine records — but only with clear disclosure and no effect on legal outcomes.",
    "TECH-JUDS-0010": "Courts must disclose any meaningful use of AI in drafting opinions, legal analysis, or summarizing records. Undisclosed AI assistance in judicial work is prohibited.",
    "TECH-JUDS-0011": "AI systems cannot be used to prioritize which cases, motions, or hearings get scheduled or heard in ways that create unfairness or unequal access to justice.",
    "TECH-JUDS-0012": "Any AI-assisted judicial workflow must produce a human-authored, accountable, and reviewable chain of reasoning for every consequential decision.",
    "TECH-JUDS-0013": "AI-generated or AI-enhanced evidence must come with documented proof of where it came from, how it was created, and how it was handled.",
    "TECH-JUDS-0014": "Parties in a legal case must receive enough technical information about AI-generated evidence to effectively challenge its reliability and limitations.",
    "TECH-JUDS-0015": "Courts cannot allow AI outputs to be treated as expert-like evidence unless the AI's methods are scientifically valid, independently tested, and subject to challenge.",
    "TECH-JUDS-0016": "Deepfakes and synthetic media presented as evidence must be treated as high-risk and must meet enhanced authentication requirements before they can be used in court.",
    "TECH-JUDS-0017": "If AI is used to analyze evidence in a case, all of the data fed into the AI, the assumptions it made, and every step it took to reach its output must be preserved and available for review.",
    "TECH-JUDS-0018": "If prosecutors or the government use AI in their investigation, charging decisions, or trial preparation, defendants must have access to the same capabilities and data to ensure a fair proceeding.",
    "TECH-JUDS-0019": "Public defenders must be funded adequately to keep up with AI tools used by prosecutors. An AI advantage for one side but not the other is fundamentally unfair.",
    "TECH-JUDS-0020": "AI cannot be used to pressure people into accepting plea deals by showing them opaque conviction probability scores or predicted punishments. Plea decisions must be made without AI-driven intimidation.",
    "TECH-JUDS-0021": "Courts must prevent situations where prosecutors have access to powerful AI tools that defense lawyers cannot afford or access. Technological disparity in the courtroom undermines equal justice.",
    "TECH-JUDS-0022": "AI systems cannot be used to profile potential jurors based on their behavior, psychological traits, or demographic characteristics for the purpose of strategic selection.",
    "TECH-JUDS-0023": "AI-generated reconstructions, simulations, or visualizations shown to a jury must be clearly identified as computer-generated demonstrations — not factual recordings of what actually happened.",
    "TECH-JUDS-0024": "Courts cannot provide juries with AI-generated summaries, interpretations, or credibility assessments of testimony or evidence. Juries must evaluate evidence themselves.",
    "TECH-JUDS-0025": "AI in the courtroom must not distort the actual evidence, create false impressions of certainty, or present outputs as more precise or neutral than they actually are.",
    "TECH-JUDS-0026": "The default rule in courts and legal proceedings is that AI use is prohibited except where it is specifically and narrowly permitted with full transparency and audit requirements.",
    "TECH-JUDS-0027": "AI-generated evidence — including images, video, audio, text, or reconstructions — cannot be used in legal proceedings.",
    "TECH-JUDS-0028": "AI-enhanced evidence that changes the interpretation or meaning of the underlying evidence is not admissible in court.",
    "TECH-JUDS-0029": "AI may only be used for analysis on evidence that already exists — not to generate new content — and only where it does not change or reinterpret that evidence.",
    "TECH-JUDS-0030": "Generative AI systems, including large language models, cannot be used to analyze evidence in legal proceedings.",
    "TECH-JUDS-0031": "Analytical AI tools that are permitted in court must use verifiable, reproducible methods — such as established statistical techniques — not opaque generative processes.",
    "TECH-JUDS-0032": "Any use of AI in evidence analysis must be explicitly disclosed — including the methods used, what data was inputted, what the limitations are, and what the error rate is.",
    "TECH-JUDS-0033": "AI systems that cannot be meaningfully explained, tested, or challenged — so-called black boxes — are not admissible for use in evidentiary contexts in court.",
    "TECH-JUDS-0034": "AI systems cannot be brought into court as expert witnesses or treated as authoritative sources on factual or legal matters.",
    "TECH-JUDS-0035": "All expert testimony must come from qualified human experts who are personally accountable for their opinions and can be cross-examined.",
    "TECH-JUDS-0036": "A human expert who uses AI tools in their analysis must disclose that fact and remains fully responsible for every conclusion they reach, regardless of what the AI suggested.",
    "TECH-JUDS-0037": "Judges and justices cannot use generative AI to write, draft, or materially shape judicial opinions or rulings. Courts must speak in a human voice, with a human responsible.",
    "TECH-JUDS-0038": "AI systems cannot substitute for a judge's own reasoning, legal analysis, or interpretation of the law. Judicial thinking must remain a human function.",
    "TECH-JUDS-0039": "AI may only be used for limited clerical tasks in judicial settings — like document organization or formatting — that have no effect on legal content or outcomes.",
    "TECH-JUDS-0040": "AI-generated reconstructions, simulations, or demonstrative materials cannot be shown to juries. Juries must see and hear actual evidence, not AI-produced dramatizations.",
    "TECH-JUDS-0041": "AI cannot summarize, interpret, or present evidence or witness testimony to a jury. The jury evaluates evidence directly — AI is not an intermediary.",
    "TECH-JUDS-0042": "AI cannot directly or indirectly influence how jurors perceive, behave, or make decisions. Jury deliberations must be free from AI manipulation.",
    "TECH-JUDS-0043": "Courts must recognize that AI systems can cause confirmation bias, produce false information, and create false certainty — and must treat all AI outputs with appropriate skepticism.",
    "TECH-JUDS-0044": "Any AI-assisted analysis permitted in court must be held to a higher standard of reliability and scrutiny than ordinary evidence — including rigorous adversarial testing.",
    "TECH-JUDS-0045": "All parties must have full rights to challenge any AI-assisted analysis used in their case, including the ability to question the methods, assumptions, and outputs of the AI.",
    "TECH-JUDS-0046": "AI-assisted analysis used in court must be reproducible — the opposing party must be able to run the same inputs through the same system and get the same results.",
    "TECH-JUDS-0047": "All AI-assisted evidentiary analysis must include a complete preserved log of what data was put in, what came out, and every step the system took to get there.",
    "TECH-JUDS-0048": "Courts and opposing parties must have access to all materials needed to fully audit AI-assisted evidentiary analysis used against them.",
    "TECH-JUDS-0049": "AI cannot be used to make decisions about child custody, visitation rights, parental fitness, or where a child should be placed — without direct human review and a genuine opportunity to contest the outcome.",
    "TECH-JUDS-0050": "AI systems cannot draw inferences about a parent's fitness, the risk of abuse, or a witness's credibility from behavioral proxies, psychological profiling, or demographic data.",
    "TECH-JUDS-0051": "Family courts cannot rely on AI-generated summaries, recommendations, or credibility assessments in cases involving custody or the welfare of children.",
    "TECH-JUDS-0052": "Any AI-assisted tool used in family court administration must be fully disclosed and must not have a material effect on outcomes unless a human reviews and is accountable for that effect.",
    "TECH-JUDS-0053": "AI cannot automate or drive eviction outcomes without direct human judicial review and a real opportunity to challenge the decision.",
    "TECH-JUDS-0054": "Courts handling eviction cases cannot rely on AI-generated tenant risk scores, rental behavior predictions, or opaque housing analytics to decide cases.",
    "TECH-JUDS-0055": "Landlords who use AI-assisted evidence or analytics in court must disclose this to the other party and provide enough information for the tenant to meaningfully challenge it.",
    "TECH-JUDS-0056": "Housing courts cannot use AI to speed up case processing in ways that reduce meaningful notice, access to hearings, or the ability to be heard by a judge.",
    "TECH-JUDS-0057": "AI cannot independently decide the outcome of administrative hearings involving government benefits, licensing, immigration, or other official determinations. A human must make the decision.",
    "TECH-JUDS-0058": "Administrative proceedings — like hearings for benefits or licenses — cannot rely on opaque AI scoring or recommendation systems to assess credibility, eligibility, or fitness.",
    "TECH-JUDS-0059": "When AI materially influences an administrative recommendation, record summary, or decision, the people affected have the right to know about it.",
    "TECH-JUDS-0060": "Government agencies must provide a genuine human review and meaningful appeal process for any adverse decision that was influenced by AI.",
    "TECH-JUDS-0061": "AI cannot determine conditions of probation or parole, decide whether supervision should be intensified, or recommend revocation — through automated behavioral predictions or scoring.",
    "TECH-JUDS-0062": "AI systems used in probation and parole cannot assign risk scores based on proxies for race, class, disability, geography, or protected activities. These proxies are well-documented pathways to discriminatory outcomes.",
    "TECH-JUDS-0063": "Probation and parole decisions must be based on individualized human review — not automated through behavioral analytics or scoring systems.",
    "TECH-JUDS-0064": "AI can be used to identify patterns of bias, inconsistency, or unlawful disparity in probation and parole systems — as a tool for reform and accountability, not for making decisions about individuals.",
    "TECH-JUDS-0065": "AI cannot be used to escalate fines, fees, collection actions, or penalties based on predictions about whether someone will pay. Punishing people for predicted behavior rather than actual conduct is prohibited.",
    "TECH-JUDS-0066": "Courts and governments cannot use AI to pressure people into paying through automated threat scoring or penalty escalation. Legal consequences must follow actual due process.",
    "TECH-JUDS-0067": "AI cannot convert an administrative debt or missed payment into a harsher legal consequence — like a warrant or license suspension — without direct human judicial review.",
    "TECH-JUDS-0068": "AI can be used to identify patterns of unjust or predatory fine-and-fee practices for review and correction — as a reform tool, under public oversight.",
    "TECH-JUDS-0069": "AI tools can help people navigate legal aid, understand documents, and access legal information — as long as they do not replace licensed attorneys or give legal advice beyond their capability.",
    "TECH-JUDS-0070": "AI tools used in legal aid contexts must be upfront about what they can and cannot do, and cannot present themselves as human lawyers.",
    "TECH-JUDS-0071": "AI tools for legal aid must be designed to be accessible, easy to understand, and fair — and must not steer people away from asserting their legal rights.",
    "TECH-JUDS-0072": "Government and courts should invest in public-interest AI tools that help people navigate the legal system — provided these tools improve access without automating critical decisions.",
    "TECH-JUDS-0073": "AI systems used to search, classify, or summarize court records must be auditable and cannot distort which cases are visible or how they are understood.",
    "TECH-JUDS-0074": "Court administrative AI systems cannot create unequal access to filing, scheduling, or records based on hidden preferences, priorities, or biases.",
    "TECH-JUDS-0075": "Court records systems that use AI must ensure accuracy, transparency, and a quick way for people to correct errors in their records.",
    "TECH-JUDS-0076": "Courts must maintain human oversight and override capability for all AI-assisted administrative systems that affect people who are parties to cases.",
    "TECH-JUDS-0077": "Where AI is permitted in judicial settings, it must be limited to transparent, non-generative, assistive functions. It cannot author or materially shape legal reasoning or outcomes.",
    "TECH-JUDS-0078": "AI systems cannot be used to assess whether a witness, defendant, or party is telling the truth, deceiving the court, or has particular intentions. Credibility determination is a human function.",
    "TECH-JUDS-0079": "Behavioral analytics, biometric analysis, and speech-pattern AI tools cannot be used to infer a person's emotional state, honesty, or reliability in legal proceedings.",
    "TECH-JUDS-0080": "AI cannot be used to selectively reanalyze, enhance, or reinterpret police body camera or surveillance footage in ways that distort its meaning or context.",
    "TECH-JUDS-0081": "When AI is used to analyze law enforcement evidence, it must preserve the full context and may not highlight some parts while suppressing others in ways that mislead.",
    "TECH-JUDS-0082": "AI translation tools cannot be the sole basis for understanding what was said in a legal proceeding. Automated translation alone is not sufficient for legal accuracy.",
    "TECH-JUDS-0083": "Human-certified interpreters are required for critical legal proceedings. AI translation may only be used as a supplementary tool, not as the primary interpreter.",
    "TECH-JUDS-0084": "AI systems used in forensic laboratories — for things like DNA analysis or ballistics — must meet strict scientific validation standards. They cannot operate as unexplainable black boxes.",
    "TECH-JUDS-0085": "Forensic AI systems must be independently tested for accuracy, bias, and reproducibility before they can be used in any case that might go to court.",
    "TECH-JUDS-0086": "AI cannot be used to reconstruct, infer, or surface records that have been legally sealed, expunged, or otherwise protected from disclosure — even indirectly through data aggregation.",
    "TECH-JUDS-0087": "Using AI to get around legal protections on sealed or expunged records is prohibited and subject to enforcement.",
    "TECH-JUDS-0088": "AI-generated content cannot be used to try to influence jurors, witnesses, or court proceedings outside the courtroom — for example, through targeted social media campaigns during a trial.",
    "TECH-JUDS-0089": "Courts must be aware of and work to counter the risk of AI-driven public influence campaigns that could compromise the impartiality of juries or the fairness of proceedings.",
    "TECH-JUDS-0090": "AI systems used in court proceedings must have version control — meaning they must not change their behavior during an active case.",
    "TECH-JUDS-0091": "If an AI system used in a legal context changes significantly, it must be revalidated before continued use, and those changes may not retroactively affect prior analyses or decisions.",
    "TECH-JUDS-0092": "Using AI tools in a legal proceeding cannot shift the burden of proof, lower evidentiary standards, or reduce any party's procedural rights.",
    "TECH-JUDS-0093": "Courts must use transparent, publicly disclosed procurement processes when acquiring AI systems — including disclosing what was purchased, from whom, and at what cost.",
    "TECH-JUDS-0094": "AI systems cannot be put into use in judicial settings without independent validation that they are fair, reliable, and legally compliant.",
    "TECH-JUDS-0095": "Courts must be able to suspend or prohibit the use of any AI system that proves to be biased, unreliable, or legally inappropriate.",
    "TECH-JUDS-0096": "Parties to a legal case must have the right to request that an AI system being used in their proceeding be suspended if they have credible grounds for questioning its fairness or reliability.",

    # LABS — Labor
    "TECH-LABS-0001": "AI tools in employment must not undermine workers' rights, dignity, privacy, or fair access to economic opportunity.",
    "TECH-LABS-0002": "AI systems cannot make fully automated hiring, firing, promotion, or pay decisions without meaningful human review and accountability.",
    "TECH-LABS-0003": "AI systems cannot filter or rank job candidates using opaque or unexplainable criteria that materially affect who gets a job or an interview.",
    "TECH-LABS-0004": "AI systems used in hiring and employment must be tested for bias and cannot result in discrimination based on protected characteristics — or stand-ins for those characteristics.",
    "TECH-LABS-0005": "Job applicants and employees have the right to receive meaningful explanations of AI-influenced employment decisions that affect them.",
    "TECH-LABS-0006": "Continuous, invasive AI monitoring of workers — including biometric tracking, keystroke logging, and real-time behavioral surveillance — is banned except where strictly necessary and proportionate.",
    "TECH-LABS-0007": "AI systems cannot be used to infer or monitor workers' emotions, mood, engagement, or psychological state for purposes of employment decisions.",
    "TECH-LABS-0008": "Employers cannot use AI to monitor or draw inferences about worker behavior outside of working hours.",
    "TECH-LABS-0009": "AI systems cannot be the sole basis for disciplinary action, termination, or changes to pay. A human must be responsible for these decisions.",
    "TECH-LABS-0010": "AI-generated productivity or performance scores must be transparent and auditable, and they cannot be used to affect employment without human review.",
    "TECH-LABS-0011": "AI systems cannot be used to coerce workers into unsafe, unreasonable, or exploitative productivity targets.",
    "TECH-LABS-0012": "Workers must be able to refuse the use of AI systems that materially harm their dignity, privacy, or safety without fear of retaliation.",
    "TECH-LABS-0013": "Workers must have access to human managers or decision-makers for any matter affecting their employment status, discipline, or working conditions.",
    "TECH-LABS-0014": "AI systems used at work may only collect worker data that is strictly necessary for legitimate business purposes.",
    "TECH-LABS-0015": "Worker data collected through AI systems cannot be sold, shared with third parties, or used for purposes unrelated to the employment relationship.",
    "TECH-LABS-0016": "Workers have the right to access, review, and correct data collected about them by AI systems used by their employer.",
    "TECH-LABS-0017": "Employers must disclose when AI systems are used in hiring, monitoring, evaluation, and employment decision-making processes.",
    "TECH-LABS-0018": "AI systems used in employment must be subject to regular independent audits for bias, fairness, and legal compliance.",
    "TECH-LABS-0019": "Employers must maintain documentation of AI systems' purpose, data sources, and decision logic sufficient to allow oversight and accountability.",
    "TECH-LABS-0020": "AI systems that assign risk scores predicting employee behavior — like likelihood of quitting, unionizing, or engaging in protected activity — are banned.",
    "TECH-LABS-0021": "Using AI systems to identify, monitor, or suppress union activity, collective bargaining, or labor organizing is banned.",
    "TECH-LABS-0022": "Using AI to infer personality traits or psychological characteristics in hiring decisions is banned unless there is strong scientific evidence and proper safeguards in place.",
    "TECH-LABS-0023": "Workers or their representatives must have a meaningful role in reviewing and approving the deployment of high-impact AI systems in their workplace.",
    "TECH-LABS-0024": "When AI systems affect working conditions, their use must be subject to collective bargaining where applicable.",

    # LIAS — Liability
    "TECH-LIAS-0001": "Companies and developers that deploy high-risk AI systems are legally responsible for physical, financial, and other harms those systems cause — regardless of whether negligence can be proven. This is called strict liability.",
    "TECH-LIAS-0002": "When an AI system's secrecy makes it hard for a harmed person to prove it was at fault, courts will presume the AI caused the harm if the person shows the AI was involved and the harm matches known failure patterns. This shifts the burden of proof toward the company.",
    "TECH-LIAS-0003": "Companies deploying AI in high-risk areas must keep records of how the system made decisions, and must report aggregate harm data to federal oversight bodies every year.",

    # LICS — Compulsory Licensing
    "TECH-LICS-0001": "When a patent is used to block access to something essential — like a medicine, a software standard, or critical infrastructure — the government must be able to require a compulsory license, allowing others to use the invention in exchange for fair compensation.",
    "TECH-LICS-0002": "In vital sectors like healthcare, agriculture, and critical infrastructure, patent rights cannot be used to prevent access to essential tools, knowledge, or technology. Public need takes precedence.",

    # MEDA — Media and Platforms
    "TECH-MEDA-0001": "AI-powered recommendation systems on large platforms cannot be primarily optimized for outrage, compulsive use, political polarization, or the spread of false information when those outcomes predictably harm public discourse.",
    "TECH-MEDA-0002": "Large platforms must independently audit their recommendation systems to identify patterns of amplification that spread harmful content, misinformation, or targeted harassment.",
    "TECH-MEDA-0003": "Users must have real, meaningful control over what recommendation systems show them — including the ability to adjust preferences or opt out of personalized recommendations.",
    "TECH-MEDA-0004": "Platforms must disclose what their ranking and recommendation systems are primarily optimizing for in plain, understandable language.",
    "TECH-MEDA-0005": "AI-generated summaries of news, civic information, or public affairs must be clearly labeled as AI-generated and must meet standards for accuracy and fairness.",
    "TECH-MEDA-0006": "Dominant platforms cannot use AI tools to disadvantage competitors, suppress independent publishers, or manipulate the information environment for their own benefit.",
    "TECH-MEDA-0007": "Large platforms must publish quarterly reports disclosing how their content moderation systems work — including error rates, appeal outcomes, and whether their systems affect some groups differently than others.",

    # MHCS — Mental Health
    "TECH-MHCS-0001": "AI mental health tools can assist therapists and counselors, but they cannot replace licensed clinicians in diagnosing conditions, evaluating crises, or making high-risk treatment decisions.",
    "TECH-MHCS-0002": "AI systems designed to create emotional dependency — or to manipulate users through simulated companionship — must be restricted or prohibited. These systems can exploit human needs for connection.",
    "TECH-MHCS-0003": "Platforms and AI products must be evaluated for whether they contribute to addiction, compulsive use, social isolation, or self-harm. Mental health harms from technology must be taken seriously.",
    "TECH-MHCS-0004": "Children and teenagers need stronger protections against AI systems that are engineered to maximize engagement at the expense of their mental health.",
    "TECH-MHCS-0005": "When you are sharing something sensitive or emotional, you must be clearly informed if you are talking to an AI, not a human. Deceptive AI personas in emotionally sensitive contexts are prohibited.",

    # MKTS — Markets
    "TECH-MKTS-0001": "Using shared AI tools, pricing algorithms, or common software to coordinate prices or suppress wages among competing companies is illegal — even if no explicit agreement was made. Algorithmic price-fixing harms consumers and workers.",
    "TECH-MKTS-0002": "AI tools used to set prices or wages in markets that affect housing, employment, or essential goods must be reviewed for anti-competitive effects. Market fairness requires oversight of automated pricing.",

    # MILS — Military AI
    "TECH-MILS-0001": "When the military or intelligence agencies use AI, meaningful human control must be maintained, and the people giving orders must remain legally and ethically accountable for what the systems do.",
    "TECH-MILS-0002": "AI systems that can independently identify and kill people — with no human making the actual decision to use lethal force — are banned.",
    "TECH-MILS-0003": "AI systems that can start or escalate the use of military force on their own, without a human authorizing each action in real time, are banned.",
    "TECH-MILS-0004": "AI cannot be placed in control of nuclear weapons, command-and-control systems, targeting decisions, or launch processes. Nuclear force must remain under strict human control.",
    "TECH-MILS-0005": "AI cannot generate, recommend, or rank human targets for lethal military action. All targeting decisions must be made by human military personnel.",
    "TECH-MILS-0006": "AI cannot be used to narrow down, filter, or prioritize lists of human targets in a way that effectively drives the targeting decision — even if a human nominally approves the final choice.",
    "TECH-MILS-0007": "When lethal force is used with AI systems involved, there must be a specific, named human decision-maker responsible for that decision. Anonymous AI accountability is not acceptable.",
    "TECH-MILS-0008": "All AI-assisted military decisions must be logged and auditable — including what data the AI was given, what it recommended, and what the human decided.",
    "TECH-MILS-0009": "AI systems used in military decision-making must be transparent enough for the human operator to genuinely understand and evaluate what the system is recommending before acting on it.",
    "TECH-MILS-0010": "Military AI systems must meet strict reliability and testing thresholds before they are deployed. Unproven AI systems cannot be sent into operational environments.",
    "TECH-MILS-0011": "AI-driven intelligence surveillance systems that collect or analyze data about civilians on a mass scale without legal authority are banned.",
    "TECH-MILS-0012": "AI cannot be used to profile individuals or populations as potential military targets based solely on statistical inference, behavioral patterns, or algorithmic prediction.",
    "TECH-MILS-0013": "All military AI systems must comply with the laws of war — including the principles of distinguishing combatants from civilians, proportionality, and military necessity.",
    "TECH-MILS-0014": "When a military AI system takes an action, the legal and moral responsibility for that action must be clearly attributable to specific human beings within a defined command chain.",
    "TECH-MILS-0015": "Military AI systems cannot be used to obscure who is responsible for a military action or to help individuals or governments avoid legal accountability for what they did.",
    "TECH-MILS-0016": "Deploying a fundamentally new type of AI-enabled military capability must require explicit authorization from Congress — not just executive decision.",
    "TECH-MILS-0017": "The President and executive branch cannot unilaterally expand the use of AI in warfare beyond what Congress has explicitly authorized.",
    "TECH-MILS-0018": "All AI-enabled military programs must report regularly to Congress and independent oversight bodies on what they are doing and how they are performing.",
    "TECH-MILS-0019": "Military AI systems must be tested in controlled conditions before being used operationally. No new system goes live without prior evaluation.",
    "TECH-MILS-0020": "Using real military operations — with real people and real consequences — as the primary way to test an unproven AI system is banned.",
    "TECH-MILS-0021": "Military AI systems must be adversarially tested — meaning experts must try to find and expose every way the system can fail, be misused, or cause unintended harm.",
    "TECH-MILS-0022": "Private contractors who develop AI for military use must follow the same legal and ethical rules as the government itself. The military cannot outsource its obligations to private companies.",
    "TECH-MILS-0023": "The government cannot hand off responsibility for decisions about the use of force to private contractors or to AI systems. These decisions must remain with accountable government officials.",
    "TECH-MILS-0024": "Strong export controls must exist on high-risk military AI systems to prevent hostile nations or governments with poor human rights records from obtaining and using these technologies.",
    "TECH-MILS-0025": "AI systems can be used in defensive roles — like missile defense, threat detection, or intelligence gathering — where they do not make decisions about targeting or killing specific people.",
    "TECH-MILS-0026": "Defensive AI systems must not be modified or repurposed to identify, select, or target individual people. A tool approved for defense cannot be converted into an offensive targeting tool.",
    "TECH-MILS-0027": "AI may be used for analyzing battlefield information, classifying threats, and maintaining situational awareness — as long as it does not generate or recommend specific targets for lethal action.",
    "TECH-MILS-0028": "AI systems cannot be used to execute offensive lethal force — including selecting targets, making engagement decisions, or triggering weapons.",
    "TECH-MILS-0029": "AI may be used in weapon guidance systems solely to improve accuracy and reduce civilian casualties — but only after a human has already made the legal decision to engage a specific target.",
    "TECH-MILS-0030": "AI guidance systems must follow the specific target chosen by a human and must not change, reinterpret, expand, or substitute for that target in any way.",
    "TECH-MILS-0031": "AI guidance systems must be incapable of selecting new targets on their own, reprioritizing targets, or initiating additional attacks beyond the specific engagement the human authorized.",
    "TECH-MILS-0032": "Human operators remain fully responsible for all outcomes when AI-assisted weapon guidance is used — including any unintended harm, collateral damage, or errors.",
    "TECH-MILS-0033": "AI can be used in purely defensive systems — like intercepting incoming missiles or detecting attacks — where the purpose is protection rather than targeting people.",
    "TECH-MILS-0034": "The United States should pursue international agreements to limit and regulate the use of AI in military and intelligence operations, establishing shared global norms.",
    "TECH-MILS-0035": "International agreements should seek to ban fully autonomous lethal weapons — systems that can kill without a human making the decision — and ensure meaningful human control is maintained.",
    "TECH-MILS-0036": "International treaties should work to ban AI systems that can independently select and engage human targets without a human decision.",
    "TECH-MILS-0037": "International treaties should restrict the use of AI in nuclear weapons systems, including command-and-control systems and strategic weapons.",
    "TECH-MILS-0038": "International agreements should include transparency requirements and verification mechanisms to confirm that countries are actually complying with military AI restrictions.",
    "TECH-MILS-0039": "International efforts should work to prevent a global AI arms race — where countries compete to build the most powerful autonomous weapons — which increases the risk of rapid, accidental escalation.",
    "TECH-MILS-0040": "The United States should support international controls on the export of high-risk military AI technologies to prevent these tools from spreading to regimes that would misuse them.",
    "TECH-MILS-0041": "Countries that violate international agreements on military AI should face strong coordinated sanctions and other consequences from the international community.",
    "TECH-MILS-0042": "Sanctions for deploying or exporting banned military AI systems should be severe and, where possible, coordinated with allied nations for maximum effect.",
    "TECH-MILS-0043": "If an adversary deploys prohibited military AI systems, limited temporary exceptions to our own restrictions may be considered — but only through proper legal processes and with full public reporting.",
    "TECH-MILS-0044": "Any exception to military AI prohibitions made in response to an adversary's actions must be temporary, reported to Congress to the fullest extent compatible with national security, and subject to legal review.",
    "TECH-MILS-0045": "The core prohibitions — on AI in nuclear weapons, on fully autonomous lethal targeting, and on unaccountable use of force — must remain in place even if adversaries violate international norms. These are non-negotiable floors.",
    "TECH-MILS-0046": "Using AI to autonomously select or attack human targets, or to meaningfully remove human accountability from decisions about lethal force, is prohibited regardless of what other countries do.",
    "TECH-MILS-0047": "Using AI to generate or recommend human targets for lethal action — or to substitute AI judgment for human judgment on matters of life and death — is prohibited with no exceptions based on reciprocity.",
    "TECH-MILS-0048": "Using AI in ways that violate the laws of war — including failing to distinguish between combatants and civilians, or acting disproportionately — is prohibited and constitutes a war crime.",
    "TECH-MILS-0049": "Using AI solely to guide a weapon more precisely toward a target that a human already lawfully selected — in order to reduce civilian casualties — does not constitute a prohibited autonomous weapons system.",
    "TECH-MILS-0050": "Individual soldiers and commanders remain personally legally responsible for illegal outcomes that result from using AI systems. Being told to follow an AI recommendation is not a defense.",
    "TECH-MILS-0051": "A dedicated, fully developed military cyber branch must be established and maintained to conduct defensive operations, protect national security, and develop strategic cyber capabilities.",
    "TECH-MILS-0052": "The military cyber branch is responsible for defending critical infrastructure, military systems, and national cyber assets from attack.",
    "TECH-MILS-0053": "Offensive cyber operations — attacking another country's or actor's systems — must be strictly limited, authorized at the highest levels of government, and subject to the same legal and oversight requirements as other military operations.",
    "TECH-MILS-0054": "Cyber operations must be designed to minimize harm to civilian infrastructure — including hospitals, utilities, financial systems, and communications — even when targeting adversary systems.",
    "TECH-MILS-0055": "All military cyber operations must be subject to oversight, audit, and accountability mechanisms equivalent to those applied to other military activities.",
    "TECH-MILS-0056": "The military cyber branch cannot be used for domestic surveillance, law enforcement, or monitoring of American civilians, except under the most narrowly defined legal circumstances with judicial oversight.",
    "TECH-MILS-0057": "The military cyber branch must coordinate with civilian agencies and private infrastructure operators to protect national security while maintaining clear boundaries between military and civilian roles.",
    "TECH-MILS-0058": "The military cyber branch should operate in alignment with international efforts to establish norms, agreements, and treaties governing responsible behavior in cyberspace.",

    # NEUS — Neural Data
    "TECH-NEUS-0001": "Data collected from your brain activity — directly or indirectly — is the most sensitive kind of personal information. It cannot be collected, processed, or shared without your clear, specific, and revocable consent.",
    "TECH-NEUS-0002": "Your neural data — information derived from your brain — cannot be used by employers, law enforcement, insurers, or political campaigns. Using brain data to make decisions about people is prohibited.",
    "TECH-NEUS-0003": "Brain-computer interface devices must pass safety and consent reviews before going to market. Companies cannot change what data a device collects or add new features without your express re-consent.",

    # OVRG — Oversight
    "TECH-OVRG-0001": "All government AI surveillance systems must be publicly registered, disclosing what they are used for, what legal authority they have, where their data comes from, and how they are overseen.",
    "TECH-OVRG-0002": "Every authorized government AI surveillance system must be regularly audited by independent reviewers for legal compliance, accuracy, bias, and civil liberties impacts.",
    "TECH-OVRG-0003": "All government AI surveillance programs must have expiration dates and must be reauthorized through a public process. Indefinite surveillance authority is not acceptable.",

    # PLAT — Platform Liability
    "TECH-PLAT-0001": "Congress must change the law that currently shields social media platforms from responsibility for content their algorithms actively promote. Platforms should still be protected for good-faith moderation decisions on user content — but not for harms caused by their own recommendation systems.",

    # PRIV — Privacy Rights
    "TECH-PRIV-0001": "People have the right to access legal websites and online services without being required to show government ID or prove their identity. Anonymous internet access is a protected right.",
    "TECH-PRIV-0002": "Using the internet anonymously or under a pseudonym (a made-up name) is a protected right. Free expression and privacy require the ability to communicate without being identified.",
    "TECH-PRIV-0003": "Federal privacy law must establish a minimum floor of rights for all Americans — including the right to know what data is collected about you, how it is used, and how to delete it. States can create stronger protections, but not weaker ones.",
    "TECH-PRIV-0004": "Sensitive personal data about Americans — including health, financial, and biometric data — cannot be stored or processed on servers located in countries considered adversaries of the United States.",

    # PRTS — Portability
    "TECH-PRTS-0001": "You have the right to download all your personal data from any digital platform in a usable format, at any time, so you can take it with you when you switch services.",
    "TECH-PRTS-0002": "Large platforms must support standardized technical systems that allow users to stay connected to people on other platforms and move between services without losing their contacts or content.",
    "TECH-PRTS-0003": "Platforms cannot put up technical, legal, or contractual barriers that prevent you from leaving for a competitor, or that degrade the experience of competing services trying to access your data on your behalf.",

    # PUBL — Public AI Infrastructure
    "TECH-PUBL-0001": "The federal government should build and maintain publicly accessible AI tools and computing resources so that the benefits of AI are available to everyone — not just large corporations.",
    "TECH-PUBL-0002": "When government agencies use AI systems in core public services, those systems should be auditable and not locked up in proprietary corporate tools wherever that is feasible.",
    "TECH-PUBL-0003": "When AI is deployed in a publicly funded service, the productivity gains it generates must be shared with the workers and the public — not captured entirely as corporate profit.",

    # RPRS — Right to Repair
    "TECH-RPRS-0001": "The right to repair your own legally owned products — including electronics, software-enabled devices, and machinery — must be protected. Manufacturers cannot use technical or legal barriers to prevent independent repair.",
    "TECH-RPRS-0002": "Replacement parts, repair manuals, diagnostic tools, and repair processes for products you own must be available at a reasonable cost. Manufacturers cannot monopolize the repair market.",

    # SCIS — Scientific Integrity
    "TECH-SCIS-0001": "AI cannot be used to fabricate scientific data, fake images, invent citations, or create false peer-review identities. Using AI to commit scientific fraud is prohibited.",
    "TECH-SCIS-0002": "Researchers who use AI tools in their work — for writing, data analysis, or coding — must disclose that use. Hiding AI assistance in scientific research is a form of misconduct.",
    "TECH-SCIS-0003": "Scientific journals must prohibit the submission of manuscripts that were AI-generated without disclosure. Passing AI writing off as original human research is prohibited.",
    "TECH-SCIS-0004": "Research institutions must have clear policies requiring that the origin and use of AI tools in research is documented and disclosed throughout the research process.",
    "TECH-SCIS-0005": "AI may assist scientists with analysis, but it cannot substitute for human expertise, verification, and accountability. Scientists remain responsible for the validity of their conclusions.",
    "TECH-SCIS-0006": "Funding agencies and scientific journals should require that AI-assisted research be reproducible — meaning others can independently verify the results using the same methods.",
    "TECH-SCIS-0007": "Scientific databases and search engines must protect against AI-generated fake papers and citations polluting the scientific record and misleading researchers.",
    "TECH-SCIS-0008": "Research funded by the public and conducted using AI should prioritize openness — sharing data, methods, and findings so others can build on and verify the work.",
    "TECH-SCIS-0009": "Research institutions must have specific procedures for investigating and addressing scientific misconduct that was enabled or committed using AI tools.",
    "TECH-SCIS-0010": "AI systems cannot be used to generate fake peer reviewers, fabricate reviews, or manipulate the scientific peer-review process in any way.",

    # SCPS — Patent Scope
    "TECH-SCPS-0001": "The length and scope of patent protection must be set to encourage real innovation and serve the public interest — not to maximize corporate profits or create indefinite monopolies.",
    "TECH-SCPS-0002": "Strategies for artificially extending patent protection — like making minor modifications to renew patents or \"evergreening\" — that do not represent genuine innovation are prohibited.",

    # SFTS — Software Patents
    "TECH-SFTS-0001": "General ideas, abstract mathematical concepts, and basic computational methods cannot be patented. Patent protection applies to specific, concrete implementations — not to the underlying concepts.",
    "TECH-SFTS-0002": "Software patents must be narrowly written and technically specific. Overly broad patents that cover wide categories of software functions are prohibited.",
    "TECH-SFTS-0003": "Patent claims that would prevent independent developers from implementing a standard technical function are invalid. Monopolizing common technical approaches harms innovation.",

    # SURS — Surveillance
    "TECH-SURS-0001": "Mass surveillance of the public without warrants or individualized legal cause is banned. Collecting communications, movements, or activities of people who are not suspected of wrongdoing is prohibited.",
    "TECH-SURS-0002": "AI-powered surveillance systems that scan public spaces or monitor large numbers of people simultaneously are banned, except in extremely narrow, high-threshold emergency conditions.",
    "TECH-SURS-0003": "The government cannot use AI to track your location persistently or stitch together your identity across different platforms and data sources without a court order based on individualized suspicion.",
    "TECH-SURS-0004": "Government agencies cannot get around constitutional warrant requirements by buying surveillance data from commercial data brokers. Purchasing what you cannot legally collect yourself is prohibited.",
    "TECH-SURS-0005": "Accessing communications or surveillance data requires strict court-approved warrants, minimization procedures limiting what can be collected, and detailed audit logs. These safeguards are mandatory.",
    "TECH-SURS-0006": "AI-based predictive policing — using algorithms to guess who might commit a crime — is banned when it relies on opaque scoring systems or data tainted by historical enforcement bias.",
    "TECH-SURS-0007": "Government agencies cannot deploy AI tools that assign suspicion or risk scores to members of the public as they go about their daily lives.",
    "TECH-SURS-0008": "Surveillance authority must automatically expire unless renewed through a transparent public process. Authorities cannot accumulate indefinite surveillance powers through inaction.",
    "TECH-SURS-0009": "AI cannot be used to map out a person's political affiliations, social relationships, religious community, or associations without individualized probable cause approved by a judge.",
    "TECH-SURS-0010": "AI-enabled surveillance of journalists, their sources, lawyers, or protected communications requires the highest level of judicial review under the narrowest possible circumstances.",

    # SURV — Surveillance Reform
    "TECH-SURV-0001": "Intelligence agencies cannot search through Americans' private communications — collected under the broad foreign intelligence authority known as Section 702 — without first obtaining a warrant.",
    "TECH-SURV-0002": "Government agencies cannot buy commercially available surveillance data to get around the legal requirement for a warrant. The Constitution's protections cannot be bypassed through private market purchases.",
    "TECH-SURV-0003": "The FBI must obtain an individual warrant with probable cause before searching databases of Americans' communications collected under Section 702 of FISA — a foreign intelligence law. The current practice of warrantless backdoor searches of Americans' private communications must end.",
    "TECH-SURV-0004": "Bulk collection of Americans' phone records, internet metadata, and location data — without suspicion of any wrongdoing — must be permanently prohibited. Surveillance of Americans must be based on individualized judicial orders.",

    # SYNS — Synthetic Media
    "TECH-SYNS-0001": "AI-generated media — also called synthetic media — cannot be used to deceive the public about real people or events in ways that cause harm, manipulate elections, or violate individual rights.",
    "TECH-SYNS-0002": "Using AI-generated images, audio, or video to impersonate a real person for fraud, financial gain, or unauthorized access to systems is banned.",
    "TECH-SYNS-0003": "AI-generated fake identities or media cannot be used to bypass identity verification systems — for example, to fraudulently pass a facial recognition check.",
    "TECH-SYNS-0004": "Creating or distributing AI-generated sexually explicit content depicting a real person without their consent is banned. This is a serious harm to personal dignity and safety.",
    "TECH-SYNS-0005": "Creating AI-generated content that convincingly portrays a real person doing or saying something false — in a way that could damage their reputation or put them in danger — is banned.",
    "TECH-SYNS-0006": "Using AI-generated content in political advertising that puts fabricated words, actions, or statements in a real person's mouth is banned.",
    "TECH-SYNS-0007": "Using AI-generated content to spread false information about a public official's health, actions, or status in order to mislead the public is banned.",
    "TECH-SYNS-0008": "Using coordinated AI-generated media to deceive the public about real events, elections, or public safety situations is banned.",
    "TECH-SYNS-0009": "When media is substantially AI-generated or has been significantly altered to depict realistic human activity, it must be clearly labeled as such.",
    "TECH-SYNS-0010": "AI-generated video and audio must include built-in, tamper-resistant markers that identify the content as AI-generated. These provenance markers must persist through sharing and distribution.",
    "TECH-SYNS-0011": "The tools needed to detect AI-generated content provenance markers must be freely available to the public, using open-source methods. Verification cannot require expensive or proprietary software.",
    "TECH-SYNS-0012": "Developers of AI content generation tools must implement reasonable safeguards to prevent users from stripping provenance markers off AI-generated content.",
    "TECH-SYNS-0013": "AI-generated parody, satire, and artistic expression are allowed — as long as the content is clearly labeled or would not reasonably be mistaken for a genuine factual account.",
    "TECH-SYNS-0014": "Journalists and documentary filmmakers may use AI-generated content for legitimate reporting or storytelling — but only if they clearly disclose it and do not use it to mislead about real events.",
    "TECH-SYNS-0015": "AI-generated content depicting a real, identifiable person is allowed when that person has given explicit, informed consent to being depicted in that way.",

    # SYSR — System Reform
    "TECH-SYSR-0001": "The patent system must be structured to promote genuine innovation that benefits the public — not to reward patent accumulation, block competition, or extract royalties without adding value.",

    # THKS — Patent Thickets
    "TECH-THKS-0001": "Accumulating large numbers of patents primarily to create licensing revenue or block competitors — rather than to protect actual innovations — is prohibited.",
    "TECH-THKS-0002": "When overlapping patents create unreasonable barriers to entering a market or building new products, those patent thickets must be addressed through regulatory action.",
    "TECH-THKS-0003": "Regulatory bodies must have the authority to limit, unwind, or prevent the formation of patent thickets that stifle innovation, block competition, or harm the public interest.",

    # TRAN — Patent Transparency
    "TECH-TRAN-0001": "Who owns a patent, who is licensed to use it, and who is enforcing it must be publicly disclosed. Hidden patent ownership structures undermine accountability.",
    "TECH-TRAN-0002": "Using shell companies or obscure ownership structures to hide who actually controls a patent is prohibited. Transparency in patent ownership is required.",

    # TRDE — Patent Trolls
    "TECH-TRDE-0001": "Patent enforcement cannot be used as a weapon against companies that are simply trying to build or sell products. Frivolous or bad-faith patent claims are prohibited.",
    "TECH-TRDE-0002": "Entities that do not make or sell products themselves — sometimes called patent trolls — cannot use patents as a tool to extract payments from businesses through the threat of litigation.",
    "TECH-TRDE-0003": "Courts must have the authority to require the losing party in frivolous patent cases to pay the winner's legal fees, and to impose sanctions on patent abuse.",
    "TECH-TRDE-0004": "Patent assertion companies cannot use shell structures to hide who controls a patent in order to make it harder for defendants to identify who they are really dealing with.",
}
# fmt: on

BATCH_SIZE = 50


def update_db(entries: list[tuple[str, str]]) -> None:
    """Update plain_language in the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executemany(
        "UPDATE positions SET plain_language=?, updated_at=datetime('now') WHERE id=?",
        entries,
    )
    conn.commit()
    conn.close()


def update_html(entries: list[tuple[str, str]]) -> None:
    """Insert <p class='rule-plain'> after <p class='rule-title'> in the HTML file."""
    html = HTML_PATH.read_text(encoding="utf-8")
    for pos_id, plain_text in entries:
        # Skip if already has rule-plain (idempotent)
        already = re.search(
            rf'id="{re.escape(pos_id)}".*?class="rule-plain"',
            html,
            re.DOTALL,
        )
        if already:
            continue

        # Match the card block and insert rule-plain after rule-title closing </p>
        # Pattern: id="TECH-XXXX-NNNN" ... <p class="rule-title">...</p> followed by <p class="rule-stmt">
        escaped_id = re.escape(pos_id)
        pattern = (
            rf'(id="{escaped_id}"[^>]*>(?:(?!</div>).)*?'
            rf'<p class="rule-title">.*?</p>)'
            rf'(\s*<p class="rule-stmt">)'
        )
        escaped_plain = plain_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        replacement = rf'\1<p class="rule-plain">{escaped_plain}</p>\2'
        new_html, n = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
        if n == 0:
            print(f"  WARNING: could not find insertion point for {pos_id}")
        else:
            html = new_html

    HTML_PATH.write_text(html, encoding="utf-8")


def git_commit(batch_num: int, total_batches: int, ids: list[str]) -> None:
    """Commit the current batch to git."""
    msg = (
        f"feat(plain-lang): backfill TECH plain language batch {batch_num}/{total_batches}\n\n"
        f"Add rule-plain text for {len(ids)} TECH positions:\n"
        + "\n".join(f"  {i}" for i in ids[:10])
        + (f"\n  ... and {len(ids) - 10} more" if len(ids) > 10 else "")
        + "\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
    )
    subprocess.run(
        ["git", "add", str(DB_PATH), str(HTML_PATH)],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=REPO_ROOT,
        check=True,
    )


def main() -> None:
    all_ids = list(PLAIN_LANGUAGE.keys())
    total = len(all_ids)
    batches = [all_ids[i : i + BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
    total_batches = len(batches)

    print(f"Processing {total} positions in {total_batches} batches of {BATCH_SIZE}")

    for batch_num, batch_ids in enumerate(batches, start=1):
        entries = [(PLAIN_LANGUAGE[pid], pid) for pid in batch_ids]
        print(f"\nBatch {batch_num}/{total_batches}: {len(entries)} positions")

        print("  Updating database...")
        update_db(entries)

        print("  Updating HTML...")
        update_html(entries)

        print(f"  Committing batch {batch_num}...")
        git_commit(batch_num, total_batches, batch_ids)
        print(f"  ✓ Batch {batch_num} committed")

    print(f"\n✓ All {total} positions processed.")


if __name__ == "__main__":
    main()
