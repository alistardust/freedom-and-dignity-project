#!/usr/bin/env python3
"""
Complete all status-missing policy cards in:
  - docs/pillars/science-technology-space.html  (38 cards: add rule-plain + rule-notes)
  - docs/pillars/foreign-policy.html            (50 cards: add rule-notes only)

Also updates status class and badge text for all 88 cards.

Run from the repo root:
  python scripts/complete-policy-cards.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCI_TECH_FILE = REPO_ROOT / "docs/pillars/science-technology-space.html"
FPOL_FILE = REPO_ROOT / "docs/pillars/foreign-policy.html"


# ---------------------------------------------------------------------------
# Science & Technology card data — 38 cards
# Each card needs: rule-plain, rule-notes, status+badge update
# ---------------------------------------------------------------------------
SCI_TECH_CARDS = [
    {
        "card_id": "STS-FND-001",
        "rule_plain": (
            "The federal government must invest a minimum percentage of GDP in basic and applied research "
            "every year, written into law so that a single bad budget year cannot dismantle decades of "
            "scientific capacity. This floor is adjusted for inflation and cannot be cut through normal "
            "appropriations processes."
        ),
        "rule_notes": (
            "GDP-percentage floors can be gamed by reclassifying non-research spending as research; "
            "the rule must precisely define qualifying expenditures to prevent accounting manipulation. "
            "Economic downturns mechanically reduce the dollar floor even if the percentage holds, "
            "so a nominal minimum should accompany the GDP-ratio requirement to prevent sharp real "
            "cuts during recessions. Congressional appropriators could comply with the floor while "
            "redirecting funding toward politically favored topics; independent scientific "
            "priority-setting authority is needed to prevent this. The floor creates no quality "
            "control mechanism — agencies can spend the minimum on low-return programs and technically "
            "comply; linking a portion of funding to competitive peer-reviewed grants addresses this. "
            "Foreign state actors have sought to influence U.S. research priorities through academic "
            "partnerships; the rule should require disclosure of all foreign funding sources on "
            "federally supported research."
        ),
    },
    {
        "card_id": "STS-FND-002",
        "rule_plain": (
            "Federal research grants should last five years instead of one, so scientists can do "
            "long-term work without spending most of their time applying for the next round of funding. "
            "Five-year cycles with mid-term reviews preserve accountability while providing the "
            "stability that serious science requires."
        ),
        "rule_notes": (
            "Multi-year grants reduce administrative overhead but create a risk of funding lock-in — "
            "poorly performing programs could run for five years before accountability checkpoints; "
            "mid-cycle review authority for cause must be preserved. The 20% cap on short-cycle grants "
            "applies to agencies, not individual programs; a single large short-cycle program could "
            "consume the entire permitted 20%. Universities may use multi-year security to delay "
            "difficult personnel decisions; this is a known institutional behavior the rule should "
            "acknowledge. The transition from annual to five-year cycles creates a funding cliff for "
            "researchers whose annual grants end before new five-year cycles begin; phased "
            "implementation timelines are needed. Some fast-moving fields — AI, infectious disease — "
            "genuinely benefit from shorter cycles that allow redirection; the 20% carve-out may be "
            "insufficient for those fields."
        ),
    },
    {
        "card_id": "STS-FND-003",
        "rule_plain": (
            "When the federal government makes regulatory decisions — like whether a drug is safe or "
            "a chemical can be used in food — it cannot rely solely on studies funded by the industry "
            "being regulated without requiring independent scientists to verify the results first. "
            "Industry funding is not disqualifying, but it cannot be the only evidence."
        ),
        "rule_notes": (
            "The 'sole evidentiary basis' standard is narrow enough that industry studies can remain "
            "dominant in the record as long as a single independent study exists, even if that study "
            "is small or poorly designed; the rule should require independent studies to be comparable "
            "in scale and quality before they count as meaningful confirmation. The replication "
            "requirement could slow beneficial regulatory approvals if independent research capacity "
            "is inadequate; dedicated federal funding for replication infrastructure is a prerequisite. "
            "Disclosure requirements for industry funding already exist but are inconsistently "
            "enforced; the rule must include real consequences for non-disclosure rather than just "
            "reporting obligations. The prohibition applies to regulatory policy but not to litigation, "
            "insurance, or clinical practice where the same industry influence concern exists. "
            "Independent replication capacity is a bottleneck that could create a queue that delays "
            "regulation indefinitely; maximum replication timelines must be specified."
        ),
    },
    {
        "card_id": "STS-FND-004",
        "rule_plain": (
            "This position requires federal science agencies — the CDC, FDA, NASA, NIH, NSF, NIST, "
            "and EPA — to formally coordinate their research so that major cross-cutting problems get "
            "integrated scientific attention instead of siloed responses. PCAST must review and "
            "publicly report on coordination gaps annually."
        ),
        "rule_notes": (
            "PCAST has existed since 1990 but its recommendations are often ignored; annual review "
            "and public assessment requirements create accountability but not enforcement when agencies "
            "fail to implement recommendations. Cross-agency coordination can diffuse accountability — "
            "when multiple agencies share responsibility, none may act decisively; clear lead-agency "
            "designations for specific research areas are needed. Data-sharing across agencies "
            "creates interoperability and security challenges; standardized formats and security "
            "protocols must be preconditions for sharing, not afterthoughts. Interagency partnerships "
            "require coordinated budgets across separately appropriated agencies, which current "
            "appropriations law makes structurally difficult; a mechanism for joint funding pools "
            "is needed. The partnership structure names seven agencies but excludes research-relevant "
            "agencies like USDA, DOE, DHS, and NOAA; the framework must be explicitly extensible."
        ),
    },
    {
        "card_id": "STS-FND-005",
        "rule_plain": (
            "When a federal agency officially says it needs more research to make a good regulatory "
            "decision, this rule requires it to actually fund that research — or explain to Congress "
            "within 90 days why it cannot and ask for the money. It closes the loophole where "
            "agencies indefinitely delay action by claiming research is needed but never funding it."
        ),
        "rule_notes": (
            "'More research is needed' is a well-documented industry delay tactic used to postpone "
            "unfavorable regulatory decisions; this rule could be exploited if the delay itself "
            "extends review timelines indefinitely. The 90-day supplemental request requirement "
            "applies only when existing appropriations are insufficient — agencies could claim "
            "existing funds are adequate without actually reprogramming them. Congress may ignore "
            "supplemental requests; the rule creates a procedural obligation but no mechanism to "
            "compel appropriations. The rule applies to agencies but not to Congress, which can "
            "decline to fund research needs without consequence. Research determinations made in "
            "bad faith — to provide political cover for inaction — need an independent review "
            "mechanism to distinguish genuine scientific needs from manufactured uncertainty."
        ),
    },
    {
        "card_id": "STS-FND-006",
        "rule_plain": (
            "Any research paid for by federal tax dollars must be made freely available to the "
            "public the moment it is published — no waiting periods and no paywalls. If taxpayers "
            "funded the science, they should be able to read the results."
        ),
        "rule_notes": (
            "A zero-day embargo eliminates the Article Processing Charge revenue model that journals "
            "currently use to fund open-access publishing; the rule requires either a federal funding "
            "mechanism to cover these costs or a shift to diamond open-access models, or it "
            "effectively mandates per-article fees out of grant budgets. The rule applies to "
            "peer-reviewed articles but not to datasets or raw data, which are often more valuable "
            "for replication; data-sharing mandates need equal urgency. Publishers may shift to "
            "pre-publication fees rather than post-publication subscriptions, increasing upfront "
            "costs for researchers. Some research has national security implications that warrant "
            "restricted access; the rule needs a narrow, well-defined security exemption with "
            "independent oversight to prevent overuse. International reciprocity is not addressed — "
            "foreign researchers benefit from access to U.S.-funded research while comparable "
            "access to foreign-funded research may be unavailable; bilateral open-access agreements "
            "should be pursued."
        ),
    },
    {
        "card_id": "STS-PUB-001",
        "rule_plain": (
            "This position creates a single, publicly searchable national database where all "
            "federally funded research findings are published and kept up to date, so any American "
            "can find and read the science their tax dollars paid for — free of charge."
        ),
        "rule_notes": (
            "A centralized federal database is a high-value target for state-sponsored cyberattacks; "
            "the security architecture must be robust, with redundant backups and continuous threat "
            "monitoring. Real-time updating creates accuracy risks — early preprints presented "
            "alongside final peer-reviewed publications without clear differentiation could mislead "
            "users; quality metadata and status labeling are essential. Searchability depends on "
            "consistent metadata standards; agencies with incompatible data models will produce "
            "integration failures that make the database practically unusable. Long-term archival "
            "sustainability is not addressed — federal IT projects are frequently underfunded and "
            "abandoned; a dedicated governance structure and protected appropriation are needed. "
            "Database access does not by itself ensure research is read or acted upon; discovery "
            "is only one of several barriers to research translation."
        ),
    },
    {
        "card_id": "STS-PUB-002",
        "rule_plain": (
            "Before research goes to peer review, it should pass a basic quality check: Is the "
            "sample size large enough? Was the study designed to actually answer the question it "
            "claims to? Are the statistics sound? Catching obvious methodological problems early "
            "reduces the number of flawed studies that enter the scientific literature."
        ),
        "rule_notes": (
            "Pre-publication screening by federal agencies introduces a government review step "
            "before independent peer review, which could chill controversial but valid research — "
            "particularly research that challenges regulatory assumptions. Minimum sample size "
            "standards cannot be uniform across all research designs; a rare-disease trial "
            "legitimately has a small sample while a general-population survey does not; the rule "
            "must allow field-specific standards set by independent scientific bodies rather than "
            "NIH and NSF, which have their own funding interests. Researchers at well-resourced "
            "institutions have greater capacity to meet quality screening thresholds, which could "
            "systematically disadvantage HBCU-affiliated and smaller researchers; capacity-building "
            "support must accompany the requirement. Pre-publication screening could be exploited "
            "by future administrations to suppress inconvenient findings under a quality-control "
            "rationale; strong independence protections and judicial review of screening decisions "
            "are essential. The rule addresses sample size and statistical power but not other "
            "common methodological failures like p-hacking, selective outcome reporting, and "
            "inadequate blinding."
        ),
    },
    {
        "card_id": "STS-PUB-003",
        "rule_plain": (
            "Every research paper from federally funded science must include a short, plain-English "
            "summary that any member of the public can understand. When agencies use research to "
            "make regulatory decisions, those plain-language summaries must be publicly available "
            "alongside the agency's findings."
        ),
        "rule_notes": (
            "Quality of plain-language summaries varies enormously; without clear standards and "
            "independent review, summaries may be incomplete, misleading, or remain inaccessible "
            "to general audiences despite the requirement. Authors writing their own plain-language "
            "summaries have incentives to overstate findings; independent review or at minimum "
            "authorship disclosure would reduce hype. Plain-language summaries may be used by "
            "advocates, journalists, and politicians in ways that decontextualize findings; a "
            "correction and clarification mechanism should exist. The rule applies to federally "
            "funded research but not to privately funded research that agencies also rely on for "
            "regulatory purposes, creating an incomplete picture in regulatory records. "
            "Translation into languages other than English is not addressed; significant portions "
            "of the U.S. public are not primary English readers, and plain-language requirements "
            "should include translation obligations for communities heavily affected by regulated "
            "industries."
        ),
    },
    {
        "card_id": "STS-PUB-004",
        "rule_plain": (
            "Before a federally funded study begins collecting data, researchers must publicly "
            "register exactly what they plan to study, how they will measure it, and what they "
            "expect to find. This prevents researchers from changing their hypothesis after seeing "
            "the results — a practice that produces misleading findings."
        ),
        "rule_notes": (
            "Pre-registration is most effective for confirmatory hypothesis-testing research but "
            "is poorly suited to exploratory or discovery research, which is a large and legitimate "
            "part of basic science; the rule must distinguish between research types and not "
            "penalize exploratory work. Pre-registration does not prevent HARKing (Hypothesizing "
            "After Results are Known) if researchers update their registration after seeing data; "
            "the rule needs audit mechanisms for registration fidelity. Regulatory agencies giving "
            "'substantially greater weight' to pre-registered studies creates an incentive to "
            "pre-register even exploratory studies superficially to gain the weighting advantage. "
            "Pre-registration registries require long-term maintenance and preservation; a federal "
            "registry that is not maintained would defeat the purpose of the requirement. "
            "International harmonization is not addressed — if U.S. funders require pre-registration "
            "while international collaborators do not, joint studies will face structural "
            "inconsistencies that disadvantage U.S. researchers."
        ),
    },
    {
        "card_id": "STS-PUB-005",
        "rule_plain": (
            "For the most important research — studies that directly drive major regulatory or "
            "clinical decisions — independent scientists must replicate the findings before those "
            "studies can be the sole basis for policy. Studies funded by industry must be replicated "
            "by researchers with no financial ties to the outcome."
        ),
        "rule_notes": (
            "'High-impact studies' requires a definition; if the determination of impact rests with "
            "the regulated industry or its allies, the designation could be manipulated to avoid "
            "replication requirements. Independent replication is resource-intensive; without "
            "dedicated funding, the requirement creates a bottleneck that delays regulation without "
            "providing genuine quality assurance. Replication failures do not always indicate fraud "
            "or error — they may reflect contextual differences or population heterogeneity; the "
            "rule needs a standard for what constitutes a valid replication rather than treating "
            "all replication failures as disqualifying. The 'primary basis' standard does not "
            "prevent industry studies from remaining influential as supporting evidence; the full "
            "evidentiary record, not just the primary study, must be addressed. Mandatory replication "
            "requirements may deter researchers from conducting original high-impact studies if they "
            "know their work will face mandatory independent scrutiny before being acted on."
        ),
    },
    {
        "card_id": "STS-PUB-006",
        "rule_plain": (
            "Scientists who receive federal research funding must publish their results — even when "
            "the study found nothing, or when the drug did not work, or when the treatment made "
            "things worse. Hiding negative results distorts the scientific record and leads other "
            "researchers to waste time and money repeating experiments that have already been done."
        ),
        "rule_notes": (
            "The two-year publication requirement is a meaningful incentive but no standard is "
            "specified for what constitutes adequate publication; depositing a minimal dataset in "
            "an obscure repository should not satisfy the requirement. The ineligibility penalty "
            "for non-publication applies only to future federal funding — a researcher who received "
            "a large grant, failed to publish, and left academia faces no consequence. Pre-prints "
            "posted to public repositories may satisfy the letter of the rule without peer-reviewed "
            "publication; minimum quality standards for compliant publication must be specified. "
            "Some research yields null results because the study was terminated early for safety "
            "or futility; mandatory publication of such studies requires clear protocols for how "
            "incomplete datasets should be presented to avoid misleading readers. The rule does "
            "not address data archival — raw data from federally funded studies must be preserved, "
            "not only published articles and summaries."
        ),
    },
    {
        "card_id": "STS-EDU-001",
        "rule_plain": (
            "The federal government should invest in helping the public understand science — not "
            "just teaching it to children in school, but building adults' capacity to evaluate "
            "scientific claims, understand uncertainty, and make evidence-informed decisions as "
            "citizens and voters."
        ),
        "rule_notes": (
            "A federal science literacy 'strategy' without mandatory metrics or accountability "
            "mechanisms is easily reduced to a symbolic publication; specific, measurable literacy "
            "outcomes and independent assessment are required for the commitment to be real. "
            "Science literacy interventions that are not culturally adapted may disproportionately "
            "serve already-advantaged communities; equity requirements for underserved communities "
            "must be built in. Trust in science is a prerequisite for science literacy to matter; "
            "the rule does not address the institutional credibility crisis affecting major "
            "scientific agencies, which is a structural barrier to any literacy program. "
            "Measuring science literacy is methodologically contested — different instruments "
            "produce different results and there is no consensus on what constitutes adequate "
            "literacy; the rule should specify measurement standards. Science literacy funding "
            "could be captured by politically favored organizations; competitive, peer-reviewed "
            "grant processes with independence from executive political influence are essential."
        ),
    },
    {
        "card_id": "STS-EDU-002",
        "rule_plain": (
            "This rule asks federal science education policy to acknowledge that most Americans hold "
            "religious beliefs, and that science education is more effective when it does not treat "
            "faith as incompatible with scientific understanding. It requires approaches that engage "
            "rather than alienate religious communities without compromising scientific accuracy."
        ),
        "rule_notes": (
            "The coexistence framework risks being interpreted as requiring educators to soften or "
            "equivocate on well-established scientific consensus — evolution, the age of the "
            "universe, climate change — to avoid antagonizing religious communities; the rule must "
            "include a clear prohibition on compromising scientific accuracy. 'Broadening science "
            "support without compromising scientific standards' is a genuine tension that cannot "
            "always be resolved; the rule needs a clear hierarchy in which scientific accuracy is "
            "non-negotiable. Framing science and religion as compatible is accurate for many "
            "traditions but not universal — some traditions hold genuinely incompatible claims; "
            "the framework should be honest about this rather than asserting universal "
            "compatibility. Federal government involvement in characterizing the science-religion "
            "relationship raises Establishment Clause concerns; the rule must be carefully scoped "
            "to science communication rather than theological claims. Science communication "
            "strategies designed for one religious community may be ineffective or counterproductive "
            "for others; the framework must be adaptable and research-based."
        ),
    },
    {
        "card_id": "STS-EDU-003",
        "rule_plain": (
            "Evidence-based science education — including evolution, climate science, and vaccine "
            "science — must be protected from political interference at every level of government, "
            "including state legislatures, school boards, and any other authority that oversees "
            "public or charter school curricula."
        ),
        "rule_notes": (
            "Federal authority over K-12 curricula is constitutionally limited by the Tenth "
            "Amendment; this rule likely depends on conditions attached to federal education "
            "funding rather than direct mandates, which reduces compliance in states that decline "
            "federal education dollars. Charter school inclusion is appropriate but enforcement "
            "is structurally complex because charter authorizers vary widely in oversight capacity. "
            "The rule protects evidence-based content from removal but does not address "
            "supplementary materials — districts could technically comply while providing "
            "creationist or climate-denialist supplementary resources. Defining 'political "
            "interference' is contested — curriculum decisions are inherently political; the rule "
            "needs clear standards for what constitutes prohibited interference versus legitimate "
            "democratic input. Teacher training and professional support for evidence-based "
            "instruction are not addressed; curriculum protection without teacher capacity-building "
            "may produce formal compliance without substantive change."
        ),
    },
    {
        "card_id": "STS-EDU-004",
        "rule_plain": (
            "This position creates a federal fund specifically for producing and distributing "
            "high-quality, accurate science content for the general public — documentaries, "
            "podcasts, articles, and online content that explain science clearly to people "
            "who are not scientists."
        ),
        "rule_notes": (
            "A federal fund that favors particular content providers could create a de facto "
            "government-approved science communication industry; competitive grant processes with "
            "independent review are essential to prevent this. Science communication perceived as "
            "government-produced may be distrusted by the communities it most needs to reach; "
            "the fund should prioritize trusted community voices and independent producers over "
            "federal agencies as primary communicators. 'Accessible, accurate' content is subject "
            "to political pressure on accuracy — future administrations could use a federal fund "
            "to promote politically convenient science while suppressing inconvenient findings; "
            "strong independence protections are needed. The fund risks duplicating existing "
            "science communication infrastructure at NSF, NIH, NASA, and NOAA; coordination "
            "rather than duplication of these programs is needed. Without evaluation requirements, "
            "the fund could persist indefinitely without demonstrating impact on actual science "
            "literacy; evidence-based evaluation of funded programs must be required."
        ),
    },
    {
        "card_id": "STS-EDU-005",
        "rule_plain": (
            "Federal funding for science museums, planetariums, and public broadcasting science "
            "programs must be maintained and protected, and free or affordable access programs "
            "must be funded so that science education reaches everyone — not just people who can "
            "pay admission."
        ),
        "rule_notes": (
            "'Federally funded museums' is a subset of the science museum sector; many science "
            "museums receive no direct federal funding and serve major public audiences — the "
            "rule's scope is narrower than its stated goal. Free access programs at museums have "
            "real operational costs that must be accounted for in federal funding formulas; "
            "underfunded mandates could strain institutions rather than expand access. Public "
            "broadcasting science programming faces competition from ad-supported digital science "
            "content; the rule should address how federal investment interacts with the digital "
            "media ecosystem. Museum access programs may not reach the most science-literacy-"
            "deficient populations if physical proximity to urban science institutions is required; "
            "mobile programming and outreach investment are needed. The rule does not address "
            "content quality standards; federally funded science exhibits can become outdated "
            "without maintenance requirements."
        ),
    },
    {
        "card_id": "STS-SPC-001",
        "rule_plain": (
            "NASA must maintain its own crewed spacecraft program — one it controls directly — "
            "so that the United States can send astronauts to space without depending on private "
            "companies or foreign governments to provide the ride."
        ),
        "rule_notes": (
            "Maintaining an independent NASA crewed vehicle alongside commercial providers "
            "significantly increases costs; the rule must justify this expenditure against the "
            "actual risk that commercial providers become unreliable or unavailable. 'Sufficient "
            "cadence to sustain crew rotation' is an operational standard that requires definition — "
            "how many flights per year, to what destinations? Without specifics, NASA could argue "
            "minimal activity satisfies the requirement. The rule creates structural tension with "
            "the Commercial Crew Program, which Congress and successive administrations have "
            "supported; clarification of how the two programs interact is needed. Crew vehicle "
            "programs have long development timelines — if NASA's independent capability "
            "deteriorates, restoring it could take a decade or more; a minimum readiness standard, "
            "not just a nominal capability, is needed. Deep space exploration programs like Artemis "
            "already require NASA-operated vehicles; the rule should clarify whether existing "
            "programs satisfy the requirement or whether additional investment is needed."
        ),
    },
    {
        "card_id": "STS-SPC-002",
        "rule_plain": (
            "NASA should be able to fix and upgrade its own satellites and space telescopes while "
            "they are in orbit — the way astronauts repaired the Hubble Space Telescope — so that "
            "billion-dollar scientific instruments do not have to be abandoned when they break "
            "or become outdated."
        ),
        "rule_notes": (
            "Orbital servicing capability is expensive to develop and maintain; a cost-benefit "
            "analysis comparing servicing investment against replacement costs on a mission-by-mission "
            "basis should be required rather than a blanket design mandate. Robotic servicing "
            "technology is still maturing; mandating it as a design requirement before it is "
            "fully validated could impose constraints that reduce scientific capability. The rule "
            "applies to 'major space telescopes and orbital research platforms' but does not define "
            "'major,' allowing NASA to exclude significant assets from the requirement. Commercial "
            "orbital servicing providers are emerging; the rule should clarify whether commercial "
            "servicing contracts satisfy the requirement or whether NASA must operate the capability "
            "directly. Servicing requirements at design stage increase initial cost and complexity; "
            "the rule should distinguish between servicing-enabling design features (low marginal "
            "cost) and full servicing system development (high cost), requiring the former for all "
            "missions and the latter based on cost-benefit analysis."
        ),
    },
    {
        "card_id": "STS-SPC-003",
        "rule_plain": (
            "NASA needs budget certainty years in advance to plan space programs — you cannot build "
            "a rocket or a space telescope one year at a time. This rule requires Congress to commit "
            "to multi-year funding plans and requires an affirmative vote to cancel a major program, "
            "rather than just quietly cutting it from the budget."
        ),
        "rule_notes": (
            "Requiring affirmative Congressional votes to cancel programs reduces executive "
            "flexibility and could lock in programs that have become scientifically obsolete or "
            "technically infeasible; a sunset review mechanism is needed. Multi-year budget "
            "authority is constitutionally unusual; Congress appropriates annually, and advance "
            "commitments may not bind future Congresses absent specific legislative structure. "
            "'Long-range program planning authority' could be read narrowly to mean NASA can plan "
            "without Congress being obligated to fund those plans; the enforcement mechanism "
            "must be more specific. The rule addresses Congressional cancellations but not "
            "Presidential impoundment or administrative restructuring that achieves de facto "
            "cancellation without a Congressional vote. Large multi-year programs have historically "
            "suffered from cost overruns requiring budget adjustments; independent cost estimation "
            "requirements are needed to prevent commitments made on unrealistic projections."
        ),
    },
    {
        "card_id": "STS-SPC-004",
        "rule_plain": (
            "Federal investment in space exploration should explicitly be counted as an investment "
            "in science education — because watching astronauts and missions inspires young people "
            "to study science, engineering, and math. NASA's educational programs and internship "
            "pipeline must be treated as core parts of its mission, not extras that get cut."
        ),
        "rule_notes": (
            "Treating space exploration primarily as an inspiration and education tool risks "
            "subordinating scientific merit as the primary driver of program selection; popular "
            "but scientifically marginal missions could be justified as inspirational. NASA STEM "
            "education programs have faced evaluations showing mixed results on actual career "
            "pathways; evidence-based program design and independent evaluation must be required. "
            "HBCU and MSI partnership requirements are valuable but must include adequate funding "
            "and programmatic substance, not just nominal institutional relationships. The rule "
            "says education programs must be 'treated as core elements, not optional additions' "
            "but mandates no minimum funding percentage or staffing level; without quantitative "
            "floors, this is aspirational rather than binding. Space inspiration's benefits may "
            "accrue disproportionately to students who already have quality science education; "
            "targeted outreach to underserved communities must be explicitly required."
        ),
    },
    {
        "card_id": "STS-SPC-005",
        "rule_plain": (
            "The U.S. should negotiate formal international agreements for deep space exploration "
            "before major missions launch — not after — so that the benefits of international "
            "cooperation are designed into the mission from the start, as they were for the "
            "International Space Station."
        ),
        "rule_notes": (
            "Pre-launch treaty negotiation requirements could slow or block programs where partner "
            "negotiations are difficult; the rule needs a timeline for completing negotiations and "
            "a clear standard for what happens if negotiations fail by that deadline. International "
            "partnerships in deep space add mission complexity, introduce technology transfer and "
            "security concerns, and require shared governance that can delay decisions; these "
            "tradeoffs must be addressed explicitly. Deep space exploration has military and "
            "strategic dimensions that may complicate partnership frameworks; the rule should "
            "clarify what classified capabilities can remain outside partnership frameworks. "
            "Ratification of cooperation frameworks by partner nations is outside U.S. control; "
            "the rule cannot guarantee frameworks are in place before programs launch. Historical "
            "ISS partnership experience shows geopolitical crises can strand cooperation even in "
            "formally ratified frameworks; resilience planning for partnership disruptions is needed."
        ),
    },
    {
        "card_id": "STS-DEB-001",
        "rule_plain": (
            "The U.S. government should fund orbital debris tracking and active cleanup as national "
            "security priorities, because space debris threatens every satellite that modern society "
            "depends on — GPS, weather forecasting, communications, and banking all depend on "
            "satellites that can be destroyed by debris."
        ),
        "rule_notes": (
            "Active orbital cleanup is still largely theoretical at scale; funding it as a national "
            "security priority before cleanup technology is validated could waste significant "
            "resources on approaches that do not scale. Debris cleanup in orbit could physically "
            "interact with foreign satellites, creating international incidents and legal disputes "
            "over ownership and liability under the Outer Space Treaty. The national security "
            "framing could lead to militarization of cleanup capabilities that should be civilian "
            "and internationally coordinated; transparency and international coordination "
            "frameworks must be required. Debris tracking data is partially classified; the rule "
            "should address how classified tracking data intersects with civilian and commercial "
            "safety needs. The cost of active removal of legacy debris created by other nations "
            "is enormous and the legal framework for assigning liability is unclear; the "
            "international legal dimensions must be addressed."
        ),
    },
    {
        "card_id": "STS-DEB-002",
        "rule_plain": (
            "The companies and countries that put satellites in orbit are responsible for safely "
            "removing them at the end of their operational life. If your satellite becomes orbital "
            "junk, that is your problem to solve and your cost to bear — just as a factory owner "
            "is responsible for the pollution their factory produces."
        ),
        "rule_notes": (
            "Small satellite operators and academic institutions may lack the financial capacity "
            "to fund deorbit operations; strict financial responsibility requirements without a "
            "tiered system could push out non-commercial actors and concentrate the orbital "
            "commons among large corporations. End-of-life disposal plans submitted at licensing "
            "time may prove technically infeasible; disposal bonds or insurance requirements "
            "are needed to ensure financial coverage when plans fail. Satellites launched before "
            "the rule takes effect have no disposal obligation — the legacy debris problem is "
            "not addressed by prospective liability assignment alone. Operator liability for "
            "disposal creates an incentive for planned disposal but not for avoiding debris-"
            "generating events during operational life; in-orbit collision avoidance obligations "
            "are needed as a complement. International coordination is essential — if only U.S. "
            "operators bear disposal costs while foreign operators do not, U.S. commercial "
            "operators are competitively disadvantaged without global environmental benefit."
        ),
    },
    {
        "card_id": "STS-DEB-003",
        "rule_plain": (
            "Before approving a large satellite constellation — like SpaceX's Starlink, which has "
            "tens of thousands of satellites — the government must require an approved, credible "
            "plan for safely removing all those satellites when they stop working. "
            "No approved debris plan, no authorization."
        ),
        "rule_notes": (
            "'Without approved debris mitigation plans' requires a definition of what constitutes "
            "an approved plan; FCC and Space Force are not well-equipped to perform independent "
            "technical validation — a dedicated independent review body is needed. Constellation "
            "operators have strong incentives to submit superficially compliant plans that depend "
            "on best-case technical assumptions; the approval standard must require margin for "
            "propulsion failures and orbital perturbations. The rule caps new authorizations but "
            "does not address constellations already authorized; tens of thousands of existing "
            "satellite authorizations lack adequate debris mitigation plans. Constellation size "
            "caps create market structure effects — large operators who already have approved "
            "plans can operate at scale while new entrants face higher barriers; the rule should "
            "ensure non-discriminatory access. Some debris mitigation techniques create different "
            "risks than propulsion-based deorbit; techniques must be evaluated on actual deorbit "
            "reliability, not just the presence of a documented plan."
        ),
    },
    {
        "card_id": "STS-DEB-004",
        "rule_plain": (
            "An approved plan for safely removing a satellite from orbit at the end of its life "
            "should be a required condition of getting the radio spectrum and orbital slot license "
            "to operate the satellite in the first place. No credible deorbit plan, no license."
        ),
        "rule_notes": (
            "FCC spectrum licensing and orbital slot allocation are distinct from safety "
            "regulation; merging them could create conflicts between FCC's communication mandate "
            "and safety objectives that require careful statutory authority. Deorbit plan approval "
            "at licensing cannot account for the satellite's actual end-of-life condition; a "
            "satellite that runs out of fuel unexpectedly may be unable to execute an approved "
            "plan regardless of its quality. License conditions can be waived or modified; the "
            "rule must prohibit waivers of deorbit requirements without demonstrated technical "
            "necessity and compensating measures. International operators launching from foreign "
            "sites using foreign orbital slots are outside FCC jurisdiction, creating an "
            "enforcement gap that unilateral U.S. licensing requirements cannot close. Many "
            "commercial satellites involve multiple regulators across multiple jurisdictions; "
            "coordination with FAA and international frequency coordination bodies is required."
        ),
    },
    {
        "card_id": "STS-DEB-005",
        "rule_plain": (
            "The U.S. should lead the effort to create an international treaty framework for "
            "managing who can put things in orbit, where they can go, and who is responsible for "
            "cleaning up orbital debris — because orbital space is a shared global commons that "
            "no single country can govern alone."
        ),
        "rule_notes": (
            "Treaty negotiation timelines are measured in years to decades; this rule sets a goal "
            "but cannot compel international agreement, and setting an unrealistic timeline may "
            "produce nominal frameworks without genuine participation. Countries with growing "
            "space programs — China, Russia, India, the EU — have different interests in space "
            "traffic management; U.S.-led frameworks may be rejected by the countries most "
            "responsible for debris. Space traffic management authority with real enforcement "
            "would require ceding some sovereign control over orbital activities; domestic "
            "political constraints on international agreements that bind U.S. space activities "
            "must be addressed. Commercial operators have strong interests in minimal traffic "
            "management requirements and will lobby against meaningful treaty terms; independent "
            "public interest representation in treaty negotiations is needed. Parallel development "
            "of national space traffic management rules enforceable against U.S. operators is "
            "needed to address near-term risks while international negotiations proceed."
        ),
    },
    {
        "card_id": "STS-DEB-006",
        "rule_plain": (
            "Kessler syndrome — a chain reaction of collisions that fills an orbital region with "
            "so much debris it becomes permanently unusable — would destroy the global satellite "
            "infrastructure modern civilization depends on. The U.S. government should formally "
            "treat its prevention as a national security priority and treat deliberate "
            "debris-generating weapons tests as threats."
        ),
        "rule_notes": (
            "Designating Kessler syndrome prevention as a national security priority could "
            "militarize what should be a shared civilian and commercial problem, potentially "
            "hindering the international cooperation needed for effective prevention. National "
            "security designation could be used to classify debris-related information that "
            "should be transparent, undermining commercial operators' ability to perform "
            "collision avoidance. Treating foreign anti-satellite tests as national security "
            "threats is accurate but could trigger escalatory dynamics; the primary response "
            "should be specified as diplomatic and legal, with deterrence as secondary. The "
            "threshold for Kessler syndrome is scientifically contested — different orbital "
            "shells have different criticality levels; the rule should require scientific "
            "assessment of specific shells rather than a single undifferentiated threat "
            "designation. Prevention ultimately requires international cooperation; framing this "
            "primarily as a U.S. national security issue may undermine the diplomatic frame "
            "needed for a global response."
        ),
    },
    {
        "card_id": "STS-AGY-001",
        "rule_plain": (
            "The FDA's drug and medical device approval process should be faster without being "
            "less safe. This requires adequate staffing, modern technology systems, and clear "
            "scientific standards — not shortcuts that put patients at risk."
        ),
        "rule_notes": (
            "'Faster without reducing safety' is a legitimate goal but is also a political formula "
            "that can be used to justify inadequate review processes; specific time targets must "
            "be paired with outcome metrics measuring post-approval safety. Accelerated approval "
            "pathways already exist (Fast Track, Breakthrough Therapy, Accelerated Approval); "
            "the rule should specify what structural reforms are needed beyond existing pathways "
            "rather than implying the problem is solely one of investment. Industry pressure "
            "consistently favors faster approvals over more rigorous ones; an independent FDA "
            "advisory board with majority non-industry representation is needed to resist speed "
            "pressure. Emergency use authorizations during COVID-19 showed that speed can create "
            "public trust problems even when the science is sound; the rule must address how to "
            "maintain public confidence in accelerated processes. FDA staffing capacity depends "
            "significantly on appropriations; the rule must be paired with funding commitments "
            "to be actionable."
        ),
    },
    {
        "card_id": "STS-AGY-002",
        "rule_plain": (
            "The FDA gets a large portion of its budget from fees paid by the drug and device "
            "companies it regulates. This creates a conflict of interest — an agency that depends "
            "on industry fees to pay its staff has an institutional incentive to keep those "
            "customers happy. This rule requires reducing that dependence through public funding."
        ),
        "rule_notes": (
            "PDUFA user fees currently fund the majority of FDA's drug review operations; replacing "
            "this revenue requires substantial congressional appropriations that may not materialize, "
            "potentially reducing FDA's review capacity during the transition. 'Reduce structural "
            "dependence' without specifying a target percentage means industry fees could remain "
            "dominant while the rule is technically satisfied. Even if user fees are replaced by "
            "appropriations, congressional politics could produce politicized budget cuts as a "
            "substitute for industry capture, trading one form of influence for another. The rule "
            "does not address the revolving door between FDA staff and the pharmaceutical industry, "
            "which is as significant a source of captured decision-making as fee structure. "
            "International comparators — EMA, PMDA — use different funding models with varying "
            "independence outcomes; empirical evidence on which models best preserve regulatory "
            "independence should inform the design."
        ),
    },
    {
        "card_id": "STS-AGY-003",
        "rule_plain": (
            "The CDC must be protected from political interference in its scientific work and "
            "its public data reporting. When the CDC changes or suppresses findings for political "
            "reasons, it cannot do its job of protecting public health — and the damage to "
            "public trust takes years to rebuild."
        ),
        "rule_notes": (
            "'Political interference' requires a precise definition; not all executive branch "
            "oversight constitutes impermissible interference, but the line has been systematically "
            "exploited and must be specified in statute. The rule protects data reporting "
            "independence but not research priorities, which can be shaped by political influence "
            "without directly altering reported data. Whistleblower protections for CDC scientists "
            "who report interference are not addressed; without protection mechanisms, "
            "independence protections on paper may not function in practice. The rule does not "
            "address CDC leadership appointment and removal standards, which are the primary "
            "mechanism through which political interference is operationalized. Targeted budget "
            "cuts to specific CDC programs achieve de facto political suppression without formal "
            "interference with data reporting; targeted defunding must be addressed as a form "
            "of political interference."
        ),
    },
    {
        "card_id": "STS-AGY-004",
        "rule_plain": (
            "NIST — the National Institute of Standards and Technology — should be the neutral, "
            "authoritative federal body that sets technical standards for AI, quantum computing, "
            "and biotechnology, and should actively engage with international standards bodies "
            "so that American standards shape global norms rather than the reverse."
        ),
        "rule_notes": (
            "NIST already performs this function to a degree through the AI RMF and cybersecurity "
            "framework; the rule should specify what additional authority, resources, or statutory "
            "mandate is needed beyond current operations. NIST standards often reflect the "
            "interests of industry participants who dominate its standards development processes; "
            "independence from dominant commercial interests requires structural reform of "
            "stakeholder participation rules. Mandatory engagement with international standards "
            "bodies could require NIST to commit to positions before domestic consensus is "
            "reached, creating foreign policy implications for technical standards work. NIST's "
            "budget and staff have not kept pace with AI and quantum technology development; "
            "specific resource commitments must accompany the mandate. Standards for AI and "
            "biotechnology have significant civil liberties and safety implications; public "
            "participation requirements beyond industry stakeholders are needed in NIST's "
            "standards development processes."
        ),
    },
    {
        "card_id": "STS-AGY-005",
        "rule_plain": (
            "For major challenges that cut across multiple scientific domains — like the "
            "intersection of climate, health, and technology — there should be standing joint "
            "bodies across federal agencies that coordinate research and response rather than "
            "each agency working in isolation."
        ),
        "rule_notes": (
            "Permanent cross-agency councils can become coordination theater without enforcement "
            "authority; the rule needs to give councils decision-making power or at minimum the "
            "ability to require agencies to explain why they rejected council recommendations. "
            "'Jurisdictional boundaries must not prevent coordinated scientific response' is a "
            "principle without an enforcement mechanism; agencies with conflicting mandates will "
            "still prioritize their own authorities when coordination requires compromise. Council "
            "composition is not specified; without representation requirements, councils could "
            "be dominated by the largest agencies and exclude bodies with critical specialized "
            "expertise. Permanent structures are harder to reform when they become dysfunctional "
            "than ad hoc task forces; periodic review and restructuring authority should be "
            "included. Cross-agency councils for AI, biosafety, and pandemic preparedness "
            "already exist in various forms; the rule should audit and reform existing structures "
            "rather than create duplicative new bodies."
        ),
    },
    {
        "card_id": "STS-AGY-006",
        "rule_plain": (
            "Federal research partnerships and funding set-asides should specifically target "
            "land-grant universities, HBCUs, and other minority-serving institutions, so that "
            "federal science investment builds real research capacity at these institutions — "
            "not just symbolic grants that do not change the structural funding gap."
        ),
        "rule_notes": (
            "'Meaningful capacity-building' is the stated goal but without specific funding "
            "levels, participation targets, or independent assessment, set-asides may remain "
            "symbolic. HBCU-targeted research programs have historically been underfunded "
            "relative to stated goals; program structure alone is insufficient without genuine "
            "appropriations commitment. Concentration of federal research infrastructure at "
            "elite research universities creates systemic barriers for MSIs that must be "
            "addressed in the NSF and NIH proposal review process, not just through set-asides. "
            "Land-grant university inclusion is appropriate but many land-grant universities "
            "are large, well-resourced R1 institutions; the rule should focus MSI provisions "
            "on genuinely under-resourced institutions. The rule addresses research partnerships "
            "but not the pipeline of HBCU and MSI students and faculty into federal programs; "
            "institutional partnerships without career development investment may produce "
            "temporary activity without long-term capacity change."
        ),
    },
    {
        "card_id": "STS-INT-001",
        "rule_plain": (
            "The U.S. should remain an active, committed participant in international scientific "
            "agreements and research partnerships, because America's scientific community benefits "
            "enormously from access to global data, instruments, and collaboration networks — "
            "and this global standing is hard to rebuild once lost."
        ),
        "rule_notes": (
            "The rule states that withdrawal from scientific frameworks cannot be quickly reversed, "
            "but no protections against withdrawal are specified; some treaty commitments require "
            "Senate ratification and can be unilaterally withdrawn by the executive. 'Scientific "
            "credibility as a strategic asset' is a defensible but contestable claim; the rule "
            "would benefit from empirical evidence on the actual strategic returns of scientific "
            "leadership. Some international scientific cooperation involves dual-use technology "
            "with weapons proliferation implications; technology transfer risks must be addressed "
            "alongside cooperation commitments. The rule does not address U.S. funding obligations "
            "in international scientific institutions, which the U.S. has defaulted on "
            "historically; consistent payment of dues is a precondition for the leadership role "
            "described. Scientific partnerships with adversary states require careful management "
            "of IP and security concerns; the rule should address how cooperation proceeds in "
            "high-tension geopolitical contexts."
        ),
    },
    {
        "card_id": "STS-INT-002",
        "rule_plain": (
            "The U.S. should make international climate science cooperation permanent — including "
            "contributions to climate science infrastructure in developing countries, where the "
            "effects of climate change are most severe and the capacity to study and respond to "
            "those effects is most limited."
        ),
        "rule_notes": (
            "'Permanent commitment' is aspirational; U.S. climate science treaty commitments have "
            "been repeatedly withdrawn and restored along partisan lines, and a domestic legal "
            "structure that makes withdrawal procedurally difficult is needed to operationalize "
            "permanence. International climate science cooperation involves dual-use satellite "
            "and remote sensing technology; export control and technology transfer implications "
            "must be addressed. U.S. contributions to climate science infrastructure in "
            "developing nations require long-term institutional commitments vulnerable to aid "
            "budget cuts; a minimum funding level as a percentage of climate aid should be "
            "specified. Climate science cooperation can become entangled with climate adaptation "
            "and mitigation policy debates; the rule should clarify that scientific cooperation "
            "is not contingent on political resolution of mitigation policy. Some developing "
            "nations may lack the institutional capacity to absorb climate science infrastructure "
            "investment effectively; capacity-building requirements must accompany "
            "infrastructure provision."
        ),
    },
    {
        "card_id": "STS-INT-003",
        "rule_plain": (
            "Pandemic preparedness should be a permanent part of U.S. global health "
            "infrastructure — funded and maintained all the time, not assembled in a rush when "
            "a pandemic has already started. Protecting Americans requires a healthy world; "
            "this is domestic public health investment with a global supply chain."
        ),
        "rule_notes": (
            "'Permanent global research infrastructure' requires sustained appropriations that "
            "have historically not materialized outside crisis periods; a funding floor protected "
            "from post-pandemic drawdown is needed. Global pandemic preparedness involves "
            "sensitive pathogen research, biosafety protocols, and dual-use biological technology; "
            "biosafety standards and dual-use research oversight in international partnerships "
            "must be addressed. The U.S. funding role in WHO and international pandemic "
            "preparedness has been politically contested; the domestic legal framework for "
            "maintaining commitments across administrations must be addressed. Pandemic "
            "preparedness investment benefits countries that may be geopolitical adversaries; "
            "the rule should acknowledge this as an acceptable cost of genuinely global "
            "preparedness while addressing legitimate security concerns. The Global Health "
            "Security Agenda and other multilateral frameworks exist; the rule should build on "
            "them rather than create parallel U.S.-centered infrastructure that could fragment "
            "global coordination."
        ),
    },
    {
        "card_id": "STS-INT-004",
        "rule_plain": (
            "Scientific credibility and the ability to collaborate with scientists around the world "
            "is a strategic asset in American foreign policy — and the State Department should "
            "formally recognize this, invest in science diplomacy, and integrate scientific "
            "exchange and joint research into its relationships with strategic partners."
        ),
        "rule_notes": (
            "Framing science diplomacy as a 'foreign policy asset' risks instrumentalizing "
            "scientific cooperation for political purposes, which can undermine the trust that "
            "makes scientific collaboration valuable in the first place. Science attachés and "
            "diplomatic roles for scientists require specialized hiring paths that current State "
            "Department human capital systems do not easily accommodate; civil service reform "
            "is needed alongside the policy. Joint research programs with strategic partners "
            "involve technology transfer and IP issues; the rule should address how science "
            "diplomacy interfaces with export control law. Scientific exchange programs have "
            "faced national security scrutiny; the rule should address how to maintain openness "
            "in exchange programs while managing genuine counterintelligence risks. Framing "
            "science diplomacy as a 'strategic tool' may cause partner nations to view U.S. "
            "scientific engagement as instrumentally motivated; authentic scientific collaboration "
            "requires prioritizing scientific merit over diplomatic utility."
        ),
    },
]


# ---------------------------------------------------------------------------
# Foreign Policy card data — 50 cards
# Each card needs: rule-notes only (rule-plain already present in HTML)
# ---------------------------------------------------------------------------
FOREIGN_POLICY_CARDS = [
    {
        "card_id": "FPOL-HRTS-0001",
        "rule_notes": (
            "The UDHR is a declaration, not a binding treaty; reaffirming it as a foreign policy "
            "foundation does not create enforceable obligations unless backed by specific treaty "
            "ratifications and statutory requirements. 'Foundation of U.S. foreign policy' does "
            "not define a hierarchy of human rights commitments — the UDHR includes economic and "
            "social rights that are routinely subordinated to commercial and strategic interests; "
            "prioritization guidance is needed. U.S. domestic human rights practices are regularly "
            "cited in international forums as inconsistent with the UDHR; the rule should include "
            "a domestic compliance review component alongside foreign advocacy. Reaffirmation of "
            "the UDHR can be selective — U.S. administrations have invoked it for civil and "
            "political rights while resisting its economic and social rights provisions; consistent "
            "application across all categories must be required. Strategic alliances with "
            "UDHR-violating states have historically created de facto exceptions; the rule must "
            "address how UDHR commitments function when they conflict with treaty alliance "
            "obligations."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0002",
        "rule_notes": (
            "'Digital rights' is not a fully defined legal category; the rule should reference "
            "specific international human rights instruments (ICCPR Article 19, HRC Resolutions "
            "on internet freedom) to anchor the commitment in existing legal frameworks. Government "
            "use of mass digital surveillance is directly implicated — recognizing digital rights "
            "as human rights creates obligations regarding U.S. domestic surveillance programs "
            "that are not addressed in this rule. Technology export controls are the primary "
            "enforcement mechanism; the rule should specify the digital rights standard these "
            "controls must satisfy and who enforces it. The right to digital privacy is contested "
            "in U.S. domestic law; recognizing it as a universal human right creates tension with "
            "domestic surveillance architecture that would need to be resolved for the position "
            "to be credible. Foreign governments that restrict internet access — China, Russia, "
            "Iran, Saudi Arabia — are significant U.S. trade and diplomatic partners; the rule "
            "should specify what diplomatic and trade consequences follow from this recognition."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0003",
        "rule_notes": (
            "The UN General Assembly recognized the right to a clean, healthy, and sustainable "
            "environment as a universal human right in 2022; U.S. support has been inconsistent "
            "and must be formalized through treaty engagement, not only declaratory support. "
            "Recognition of environmental rights in foreign policy creates pressure for consistency "
            "with domestic environmental policy, where the U.S. has significant gaps; the rule "
            "must address how to manage this tension honestly rather than ignoring it. "
            "Environmental rights recognition could conflict with trade agreements that protect "
            "investor rights to operate polluting industries; the rule should address how "
            "environmental rights apply in investor-state disputes. Countries that recognize "
            "environmental rights face litigation risk from communities challenging development "
            "projects; the diplomatic implications for U.S. project finance abroad should be "
            "addressed. 'Core foreign policy commitment' language does not define consequences "
            "for violations; environmental rights recognition without enforcement mechanisms "
            "has limited practical impact."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0004",
        "rule_notes": (
            "'Non-derogable' is a specific human rights term meaning rights that cannot be "
            "suspended even in emergencies; applying it to LGBTQ+ rights is a principled position "
            "but puts the U.S. in direct tension with treaty allies and partners where LGBTQ+ "
            "criminalization is widespread. U.S. global advocacy for LGBTQ+ rights has been "
            "criticized as culturally imperialist by some governments and civil society groups; "
            "the rule should address how to advance rights while respecting the agency of affected "
            "communities to define their own advocacy strategies. 'In all foreign engagements' "
            "includes engagement with Saudi Arabia, Qatar, and Egypt where LGBTQ+ rights advocacy "
            "directly conflicts with strategic and economic interests; the rule must address what "
            "happens when principles and strategic interests collide. Consistency demands that "
            "this standard apply to U.S. allies as well as adversaries; past U.S. practice has "
            "been to prioritize rights advocacy toward adversaries while muting it toward allies. "
            "U.S. domestic LGBTQ+ rights protections have faced significant rollbacks in recent "
            "years; advocacy credibility abroad depends in part on consistency at home."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0005",
        "rule_notes": (
            "'Non-negotiable' language eliminates diplomatic flexibility; the rule should address "
            "how to advance women's rights in contexts where continued engagement rather than "
            "isolation produces better outcomes for women on the ground. U.S. military intervention "
            "in Afghanistan — nominally to advance women's rights — ended with the Taliban's return "
            "to power and the destruction of those rights; the rule should address the limits and "
            "risks of militarized approaches to women's rights advocacy. The U.S. has not ratified "
            "CEDAW; meaningful foreign policy commitment to women's rights requires at minimum "
            "Senate consideration of ratification, not only diplomatic rhetoric. Domestic "
            "inconsistency — particularly on reproductive rights following Dobbs — undermines "
            "U.S. credibility in advancing women's rights abroad; the rule should acknowledge "
            "this tension. U.S. conditions on gender equality can trigger domestic backlash in "
            "recipient countries that worsens women's conditions; evidence-based assessment of "
            "advocacy approaches is needed rather than assuming conditionality is always effective."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0006",
        "rule_notes": (
            "The United States is already bound by the UN Convention Against Torture, ratified "
            "in 1994; the persistent relevance of this rule reflects that statutory and treaty "
            "commitments have been violated and require more robust institutionalization. "
            "Post-9/11 extraordinary rendition involved transfer of detainees to countries known "
            "to practice torture; the prohibition must specifically address such transfers even "
            "when diplomatic assurances are provided, given that such assurances have proven "
            "demonstrably unreliable. CIA black sites, contractor-administered interrogations, "
            "and DoD programs have all been vectors for torture; the prohibition must apply to "
            "all U.S. agents, contractors, and facilities, not only uniformed military personnel. "
            "Classified interrogation programs make accountability nearly impossible; the rule "
            "should require declassification of all interrogation programs within a defined "
            "timeframe with independent oversight. Criminal accountability for torture committed "
            "by U.S. officials has not occurred; the rule must address accountability for past "
            "violations to create genuine deterrence, not only prohibit future acts."
        ),
    },
    {
        "card_id": "FPOL-HRTS-0007",
        "rule_notes": (
            "U.S. credibility in opposing these practices is compromised by its own record — "
            "Guantanamo represents indefinite detention without trial, the targeted drone "
            "program has produced extrajudicial killings, and the CIA's detention program "
            "involved disappeared detainees; the rule must address domestic compliance alongside "
            "foreign advocacy. 'Consistently oppose' means applying the standard to allies as "
            "well as adversaries; past U.S. practice has been vigorous condemnation of adversary "
            "states' practices while quiet acceptance of ally states' practices. The rule should "
            "specify diplomatic, economic, and legal consequences for states that systematically "
            "practice these abuses, not just verbal opposition through diplomatic channels. "
            "Extrajudicial killing through targeted drone strikes requires its own specific rule "
            "addressing legal standards, accountability, and oversight; this rule should "
            "cross-reference the covert action oversight family. Enforced disappearances are a "
            "crime under the International Convention for the Protection of All Persons from "
            "Enforced Disappearance; U.S. ratification of this convention is a prerequisite "
            "for credible advocacy."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0001",
        "rule_notes": (
            "'Committing war crimes' requires a legal determination that the U.S. has historically "
            "resisted making about partner states; the rule needs a specific standard for when a "
            "war crimes determination triggers the prohibition, including which body makes the "
            "determination and what evidence threshold applies. Political pressure from the arms "
            "industry and strategic partners has consistently produced exceptions to arms transfer "
            "restrictions; legal obligations that cannot be waived through executive discretion "
            "alone are needed. Ongoing U.S. arms transfers to Saudi Arabia during the Yemen war "
            "demonstrate the gap between principle and practice; the rule should address how "
            "existing transfers to ongoing conflict parties are reviewed. The rule prohibits "
            "transfers 'to governments' but U.S. arms often flow to non-state actors through "
            "intermediaries; all transfer mechanisms including FMF, DCS, EDA, and covert programs "
            "must be covered. Independent legal determination of war crimes status requires "
            "Congressional involvement; executive branch monopoly on these determinations allows "
            "indefinite deferral."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0002",
        "rule_notes": (
            "A 'generational extension' creates the possibility of decades-long restrictions on "
            "countries undergoing genuine democratic transitions; a structured review process with "
            "clear benchmarks for lifting embargoes is needed rather than open-ended duration "
            "based on time alone. Independent judicial review of war crimes findings that trigger "
            "embargoes is essential; if the executive branch makes the determination, triggers "
            "can be avoided through non-findings rather than genuine behavioral change. The "
            "'generational' framing refers to institutional accountability across leadership "
            "generations, which is sound in principle but embargo periods must be defined against "
            "objective behavioral benchmarks rather than calendar time. Arms embargoes have "
            "historically been evaded through third-country transshipment; enforcement mechanisms "
            "addressing evasion, including secondary sanctions on transshipping countries, are "
            "needed. Embargoes affect defense industry employment and allied diplomatic "
            "relationships; the rule must withstand substantial political pressure from both "
            "domestic arms manufacturers and partner governments."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0003",
        "rule_notes": (
            "The ATT was signed by the Obama administration in 2013 but has not been submitted "
            "to the Senate for ratification; Senate ratification requires 67 votes and faces "
            "strong opposition from senators aligned with the domestic arms industry. U.S. "
            "ratification without adequate implementation — including export licensing reform, "
            "end-use monitoring, and interagency coordination — would be symbolic; implementation "
            "capacity must accompany ratification. The ATT's humanitarian law provisions require "
            "states parties to assess whether arms could be used to commit atrocities; this is "
            "the mechanism through which the treaty operationalizes the transfer prohibition, "
            "but the assessment standard is subject to wide interpretation. Major arms exporters "
            "including Russia and China are not ATT parties; U.S. ratification strengthens the "
            "treaty's normative authority but does not bind non-parties, limiting practical "
            "effect without broader universalization efforts. ATT implementation creates reporting "
            "obligations requiring greater transparency in U.S. arms exports, which will face "
            "opposition from secrecy-preferring elements of the national security establishment."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0004",
        "rule_notes": (
            "The Leahy Law already exists in two statutes (FAA Section 620M and Title 10 Section "
            "362); the rule should specify what 'substantially strengthen' means — higher "
            "evidentiary thresholds for exemptions, expanded agency coverage, or faster vetting "
            "timelines. Leahy Law vetting has been chronically under-resourced at State; funding "
            "and staffing the vetting process adequately is a prerequisite for genuine enforcement, "
            "not merely a rhetorical upgrade. The law applies to military and police units "
            "receiving direct U.S. assistance; it does not apply to units receiving assistance "
            "from U.S.-funded but nominally independent entities — a significant loophole. "
            "Credible information standards for Leahy violations are inconsistently applied; "
            "standardized evidentiary requirements and independent review of vetting "
            "determinations are needed. Remediation provisions — the process by which a "
            "sanctioned unit can be reinstated — have been used to launder accountability; "
            "genuine accountability before reinstatement, not just pro forma assurances, "
            "must be required."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0005",
        "rule_notes": (
            "Arms Export Control Act procedures currently include a Congressional notification "
            "period with a joint resolution of disapproval option; shifting to affirmative "
            "approval is constitutionally defensible but requires significant statutory reform. "
            "Presidential emergency authorities under Section 36(c) of the AECA have been used "
            "repeatedly to circumvent Congressional notification; the rule must eliminate or "
            "substantially narrow these emergency authorities. 'Major arms sales' requires "
            "a definition — current law uses dollar thresholds that have not been updated for "
            "inflation; a combination of dollar thresholds and capability categories is needed. "
            "Affirmative approval processes are slow; defining Congressional action timelines "
            "is needed to avoid administrative paralysis while preserving meaningful oversight. "
            "Foreign governments have a strong interest in avoiding Congressional scrutiny of "
            "their human rights records; the rule creates diplomatic pressure that the executive "
            "branch will resist, requiring legislative codification to be durable."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0006",
        "rule_notes": (
            "End-use monitoring currently exists as the Blue Lantern program and Enhanced "
            "End-Use Monitoring; the rule should specify what is inadequate about current "
            "monitoring and what 'real legal consequences' means — automatic suspension, "
            "criminal penalties, or permanent blacklisting. Monitoring effectiveness is "
            "limited by the willingness of recipient governments to allow access; the rule "
            "needs to address what happens when access is denied rather than treating denial "
            "as an acceptable operational outcome. End-use violations discovered years later "
            "may be difficult to prosecute; a statute of limitations long enough to allow "
            "complex international investigations is needed. Consequences for violations should "
            "apply to both the recipient government and any U.S. officials who approved the "
            "transfer despite evidence of likely misuse; accountability must be bilateral. "
            "Third-country transshipment evades end-use monitoring; the rule must address the "
            "full transfer chain, not only the immediate recipient."
        ),
    },
    {
        "card_id": "FPOL-ARMS-0007",
        "rule_notes": (
            "Full transparency in arms transfers conflicts with classified military assistance "
            "programs; the rule must specify which categories can legitimately remain classified "
            "and require oversight of classified programs by cleared Congressional committees "
            "rather than no oversight. Export notification to Congress is currently required "
            "for major sales but not all transfers; expanding transparency to all transfers "
            "creates compliance burdens that may exceed agency capacity without additional "
            "resources. Public disclosure of transfer data enables foreign governments to track "
            "U.S. military relationships in ways with strategic implications; disclosure timing "
            "and format requirements must address this rather than defaulting to secrecy. "
            "Transparency data must be standardized and machine-readable to be useful for "
            "oversight; inconsistent reporting formats have historically allowed formal compliance "
            "without genuine transparency. Civil society organizations and investigative "
            "journalists are primary users of arms transparency data; the rule should protect "
            "their access and prohibit classification of data primarily to avoid accountability "
            "scrutiny."
        ),
    },
    {
        "card_id": "FPOL-MILS-0001",
        "rule_notes": (
            "Human rights impact assessments require specialized expertise not currently "
            "institutionalized in the export licensing process; hiring specialized assessors "
            "creates a bottleneck that could be used to slow legitimate export approvals. "
            "Assessment methodologies are contested — different frameworks produce different "
            "conclusions; a standardized methodology developed by an independent body, not by "
            "the arms-exporting agencies themselves, is essential. The rule applies to private "
            "export licenses (DCS) but not equivalently to government-to-government transfers "
            "(FMF, EDA, IMET); the assessment requirement should apply equally across all "
            "transfer mechanisms to prevent migration to less-scrutinized channels. Companies "
            "seeking licenses have strong incentives to understate human rights risks in "
            "self-reported information; independent assessment rather than reliance on "
            "applicant-provided data is essential. Impact assessments without accountability "
            "for incorrect assessments are ineffective; a post-transfer review mechanism for "
            "assessment accuracy is needed."
        ),
    },
    {
        "card_id": "FPOL-MILS-0002",
        "rule_notes": (
            "'Heightened export controls' requires specification — a new export control list, "
            "elevated licensing requirements, end-use monitoring, or some combination; without "
            "specificity, agencies can nominally comply while maintaining current practice. "
            "AI weapons capabilities are often embedded in broader dual-use systems; "
            "distinguishing controlled AI-weapons capabilities from permissible dual-use AI "
            "exports is technically complex and requires specialized export control expertise "
            "that does not currently exist at scale. Surveillance technology exported for "
            "'legitimate law enforcement' has been used for political repression; a standard "
            "for acceptable use that goes beyond the exporter's stated intent, including "
            "independent post-transfer monitoring, is needed. Export controls impose costs on "
            "U.S. technology companies in competitive international markets; the rule should "
            "address how to maintain U.S. competitive position while enforcing meaningful "
            "restrictions. Multilateral coordination on AI weapons export controls is more "
            "effective than unilateral U.S. controls; the U.S. should pursue harmonized "
            "standards through the Wassenaar Arrangement and other forums."
        ),
    },
    {
        "card_id": "FPOL-MILS-0003",
        "rule_notes": (
            "A 2-year cooling-off period is the current standard for some senior officials; "
            "the rule should specify what the extended period should be and for which categories "
            "of officials — general officers and SES members have different knowledge advantages "
            "that the cooling-off period must address. 'Revolving door' restrictions can be "
            "evaded through consulting arrangements, board memberships, and advisory roles that "
            "do not technically constitute employment; the rule must cover all forms of "
            "compensated engagement. The restriction creates a deterrent to public service for "
            "officials who expect post-retirement industry careers; adequate retirement "
            "compensation as a counterbalance should be addressed alongside the restriction. "
            "Enforcement of revolving door restrictions has historically been weak; real "
            "penalties — criminal liability, disgorgement of consulting fees, prohibition on "
            "future government service — that exceed current administrative sanctions are needed. "
            "The rule addresses the DoD-contractor revolving door but should also cover senior "
            "officials at intelligence agencies, State, and USTR, who have comparable conflicts."
        ),
    },
    {
        "card_id": "FPOL-MILS-0004",
        "rule_notes": (
            "Offensive cyber capabilities and spyware are inherently dual-use — network "
            "penetration tools used for defense can be used for offense; the rule needs a "
            "classification framework that distinguishes weapons-grade capabilities from "
            "permissible security research tools without stifling defensive security work. "
            "NSO Group's Pegasus spyware was sold to governments that used it against "
            "journalists, activists, and political opponents in multiple countries, demonstrating "
            "that stated end-use is insufficient without independent monitoring. International "
            "coordination is essential; unilateral U.S. controls will be undercut by Israeli, "
            "European, and other suppliers not subject to equivalent restrictions. The Wassenaar "
            "Arrangement's 2013 addition of 'intrusion software' created significant problems "
            "for legitimate security researchers; the rule must learn from that experience and "
            "target malicious state use without restricting defensive security practice. "
            "Classification of offensive cyber programs makes Congressional oversight difficult; "
            "cleared committees with genuine expertise must have meaningful access."
        ),
    },
    {
        "card_id": "FPOL-MILS-0005",
        "rule_notes": (
            "The DoD has failed every financial audit since audits were first required in 1990; "
            "framing audit passage as a precondition for budget increases is a plausible "
            "accountability mechanism but the DoD can maintain current spending levels "
            "indefinitely without passing an audit. The precondition creates a potential "
            "national security vulnerability — if budget increases are linked to audit passage, "
            "adversaries benefit from the predictability of constrained DoD resources during "
            "periods of audit failure. Financial audits measure accounting accuracy, not program "
            "effectiveness or strategic value; passing an audit would not demonstrate wise "
            "spending, only adequate accounting. Fixing DoD financial management systems "
            "requires upfront investment, not budget denial; the rule should require a credible "
            "audit roadmap with milestones rather than binary pass/fail consequences. The rule "
            "should specify what 'passing' an audit means — unqualified opinion, reduction in "
            "material weaknesses, or something else — to prevent gaming of the metric."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0001",
        "rule_notes": (
            "'Genuine last resort' is a Just War criterion that has been interpreted expansively "
            "to justify most modern U.S. military actions; the rule must specify what structural "
            "changes — Congressional authorization requirements, diplomatic timeline mandates — "
            "operationalize genuine last resort rather than leaving it as a rhetorical standard. "
            "The 2001 AUMF has been used to justify military operations in at least 19 countries "
            "over two decades without specific Congressional authorization; AUMF reform is a "
            "precondition for genuine diplomatic primacy. Diplomatic primacy requires investing "
            "in diplomatic capacity at a level proportionate to military spending; current "
            "resource allocation is heavily military-dominant, and the rule must address this "
            "imbalance. The Defense Department's increasing assumption of diplomatic and "
            "development functions through Combatant Commanders' theater engagement must be "
            "addressed; restoring diplomatic primacy requires clearer civilian-military role "
            "delineation. Humanitarian intervention scenarios create genuine tension between "
            "diplomatic primacy and civilian protection; the rule should address Responsibility "
            "to Protect doctrine and its relationship to force-as-last-resort standards."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0002",
        "rule_notes": (
            "U.S. arrears to the UN have been recurring — the U.S. has withheld assessed "
            "contributions multiple times for political reasons; the domestic legal mechanism "
            "for ensuring consistent payment, including limits on executive authority to withhold "
            "dues, must be addressed. 'Reform-supporting' membership requires a definition; "
            "the U.S. has used reform advocacy to advance structural changes that advantage "
            "wealthy member states while characterizing opposition as anti-reform. UN "
            "peacekeeping effectiveness is mixed; blanket support for UN operations without "
            "quality and accountability standards could enable poorly designed or poorly executed "
            "missions. The Security Council veto structure gives the U.S., China, and Russia "
            "effective vetoes over accountability for their own actions; constructive membership "
            "must include willingness to accept scrutiny of U.S. actions, not only to apply "
            "scrutiny to others. Congressional approval requirements for UN treaty commitments "
            "create structural tension with executive management of UN membership; consistent "
            "participation despite Congressional opposition must be addressed."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0003",
        "rule_notes": (
            "The U.S. is not an ICC member state and American citizens are expressly protected "
            "from ICC jurisdiction by the American Servicemembers Protection Act; constructive "
            "engagement requires either repealing ASPA and joining the Rome Statute or defining "
            "a form of cooperation that stops short of full membership. U.S. cooperation with "
            "ICC investigations involving adversary states has been selectively forthcoming; "
            "consistent engagement requires applying the same standard to U.S. allies and "
            "officials. U.S. sanctions against ICC officials imposed in 2020 damaged the ICC's "
            "credibility and the U.S.'s standing as a rule-of-law advocate; reversing these "
            "sanctions is a prerequisite for credible engagement. ICC jurisdiction over U.S. "
            "military operations abroad — even without U.S. membership — is contested; the rule "
            "should address how the U.S. manages this jurisdictional question in the context of "
            "engagement. Constructive engagement is more meaningful if the U.S. works toward "
            "eventual membership; the rule should include a timeline for Senate consideration "
            "of the Rome Statute."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0004",
        "rule_notes": (
            "'Shared global challenges' covers a vast range of issues; the rule should specify "
            "which categories trigger the multilateral default and what the exception standard "
            "is for unilateral action. Multilateral frameworks require consensus that may be "
            "impossible on urgent issues; the rule needs an exception for cases where multilateral "
            "action is blocked by veto-wielding powers acting in bad faith. U.S. unilateral "
            "sanctions have been a primary tool of foreign policy; the multilateral default "
            "creates tension with the extensive U.S. unilateral sanctions apparatus and must "
            "address whether existing sanctions regimes should be multilateralized. The UN "
            "Security Council's structure makes genuine multilateralism impossible when P5 "
            "members are directly implicated; alternative multilateral frameworks for issues "
            "where the Council is structurally blocked must be specified. Multilateral processes "
            "are slower than unilateral ones; the urgency threshold that permits bypassing "
            "multilateral frameworks must be defined to prevent eroding the default through "
            "claimed urgency."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0005",
        "rule_notes": (
            "'Scale proportionate to conflict response' requires a baseline estimate of current "
            "conflict response spending and a defined proportion for prevention; without specific "
            "numbers, the commitment is aspirational. Conflict prevention investments are often "
            "invisible when they succeed — there is no 'prevented war' to point to — which makes "
            "them politically difficult to fund and easy to cut during budget pressures. The "
            "political will problem for conflict prevention is structural: legislators who fund "
            "prevention do not receive political credit for wars that did not happen, while those "
            "who fund conflict response receive visible credit for military successes; the rule "
            "must address this incentive structure. Conflict prevention investment can inadvertently "
            "signal weakness if not paired with credible deterrence; the rule should address how "
            "prevention investment interacts with deterrence posture. Evidence on which conflict "
            "prevention interventions actually work is limited; rigorous evaluation of prevention "
            "programs rather than simply increasing spending on existing models must be required."
        ),
    },
    {
        "card_id": "FPOL-DPLS-0006",
        "rule_notes": (
            "The U.S. has participated in the Universal Periodic Review but has accepted "
            "relatively few recommendations and implemented fewer still; the rule must specify "
            "what 'respond substantively' means — acceptance rates, implementation timelines, "
            "reporting requirements. Some UPR recommendations touch on contested domestic "
            "policy areas — police violence, prison conditions, indigenous rights; accepting "
            "international review of these areas faces strong political resistance that must "
            "be addressed rather than ignored. International accountability mechanisms can be "
            "instrumentalized — adversary states routinely use them to make bad-faith submissions "
            "targeting U.S. domestic policy; the rule must distinguish genuine engagement from "
            "defensive participation. U.S. treaty body obligations under ICCPR, CAT, CERD, and "
            "CRPD include regular reporting requirements; the U.S. has been chronically late in "
            "submitting these reports, and compliance with existing obligations is a prerequisite "
            "for credible participation in new review processes. Domestic implementation of "
            "international human rights recommendations requires executive and Congressional "
            "action; the rule should specify what follow-through mechanisms make international "
            "review substantive rather than performative."
        ),
    },
    {
        "card_id": "FPOL-AIDS-0001",
        "rule_notes": (
            "Blanket conditionality can harm civilian populations who depend on assistance "
            "programs when their governments violate human rights; the rule must distinguish "
            "between military and security assistance (where conditionality is most appropriate) "
            "and humanitarian assistance (where population welfare must be protected). "
            "'Verifiable' compliance requires independent monitoring capacity that is not always "
            "available in recipient countries; the rule must address what happens when "
            "verification is impossible due to government restrictions on access. Human rights "
            "conditionality can be manipulated — conditions imposed selectively against adversary "
            "states while waived for allies — without consistent enforcement; an independent "
            "compliance assessment mechanism is needed. Conditionality has mixed evidence of "
            "effectiveness; it can trigger backlash, undermine reformers within governments, "
            "and produce cosmetic compliance; evidence-based assessment of conditionality "
            "approaches should be required. Emergency humanitarian assistance must be explicitly "
            "exempt from conditionality; the rule should specify that life-saving assistance "
            "flows regardless of government human rights status."
        ),
    },
    {
        "card_id": "FPOL-AIDS-0002",
        "rule_notes": (
            "'Strategic aid' is defined in contrast to development and humanitarian aid, but "
            "the line is often blurred — security assistance framed as counterterrorism or "
            "border security directly supports repressive security forces. Authoritarianism is "
            "not binary; there is a spectrum, and the rule needs a standard for what level of "
            "authoritarianism triggers the prohibition and who makes the determination. Ending "
            "strategic aid to authoritarian partners would directly affect Israel, Saudi Arabia, "
            "Egypt, and other major U.S. allies; these strategic implications must be addressed "
            "rather than ignored. Ending strategic aid may reduce U.S. leverage to influence "
            "reforms in recipient countries; the rule should address whether it applies regardless "
            "of reform potential or whether engagement-based alternatives are permitted. The "
            "effectiveness of this rule depends on whether alternatives — Russian or Chinese "
            "assistance — would fill the gap and produce worse outcomes; this empirical "
            "question must be addressed."
        ),
    },
    {
        "card_id": "FPOL-AIDS-0003",
        "rule_notes": (
            "USAID independence was significantly reduced by integrating it into the State "
            "Department's organizational structure; restoring genuine independence requires "
            "statutory changes beyond organizational charts. Development impact evaluation "
            "requires clear metrics that are contested among development economists; the rule "
            "should specify what evaluation standards will be used and whether evaluations "
            "are conducted by USAID itself or by genuinely independent assessors. Aid programs "
            "with proven development impact have sometimes been cut for political reasons while "
            "ineffective programs with political support are maintained; independence requires "
            "structural protection from political override of evidence-based decisions. U.S. "
            "aid frequently comes with procurement requirements (tied aid) that reduce "
            "development effectiveness; procurement reform must accompany independence "
            "restoration. USAID's historical role has included intelligence-linked programs "
            "and democracy promotion activities that compromise development credibility; "
            "independence requires clearly separating development assistance from intelligence "
            "and political operations."
        ),
    },
    {
        "card_id": "FPOL-AIDS-0004",
        "rule_notes": (
            "Elite capture of aid is a well-documented phenomenon in development economics; "
            "the rule states the goal but does not specify the mechanisms — direct service "
            "delivery, civil society support, cash transfers, conditional grants — that "
            "actually achieve it in different contexts. Aid that bypasses government systems "
            "can undermine state capacity and accountability, which are themselves development "
            "goods; the rule must balance bypassing corrupt governments with the goal of "
            "building government capacity. Beneficiary targeting creates administrative costs "
            "and eligibility disputes; simple universal programs can reach populations more "
            "efficiently than highly targeted ones in some contexts. Monitoring whether aid "
            "benefits populations rather than elites requires ground-level access that is often "
            "restricted by host governments; consequences for access denial must be specified. "
            "Accountability requirements must extend to U.S. implementing organizations and "
            "contractors, who are also capable of capturing aid program value, not only to "
            "foreign governments."
        ),
    },
    {
        "card_id": "FPOL-AIDS-0005",
        "rule_notes": (
            "PEPFAR and the Global Fund demonstrate that sustained global public health "
            "investment can achieve transformative outcomes; the rule should build on these "
            "models and their documented lessons rather than treating global health investment "
            "as a new concept. The 'core security obligation' framing can lead to securitization "
            "of global health, where security priorities override public health principles and "
            "compromise the trust-based partnerships essential to health program effectiveness. "
            "Global public health investment requires trust-based partnerships with local health "
            "systems that can be undermined by political conditionality or intelligence-gathering "
            "programs co-located with health programs; these must be strictly separated. "
            "The COVID-19 pandemic exposed specific gaps in global health infrastructure — "
            "genomic surveillance capacity, supply chain resilience, WHO funding; the rule "
            "should address these documented gaps rather than being general. Pandemics require "
            "rapid response that conflicts with standard foreign assistance timelines and "
            "approval processes; emergency authorities for global health responses must be "
            "addressed."
        ),
    },
    {
        "card_id": "FPOL-RSPS-0001",
        "rule_notes": (
            "Formal acknowledgment of U.S. responsibility for historical interventions has "
            "precedent — the Clinton administration acknowledged U.S. involvement in the "
            "Guatemalan coup — but has not been consistently followed by substantive policy "
            "change; the rule should specify what acknowledgment triggers, not just that it "
            "must occur. 'Legislative resolutions' are the weakest form of acknowledgment and "
            "can be passed without executive buy-in; executive branch acknowledgment through "
            "formal diplomatic communications and policy documents should be required. Countries "
            "and advocacy communities may use formal U.S. acknowledgment as the basis for "
            "reparations claims; the rule should address how acknowledgment relates to "
            "reparative obligations rather than leaving this undefined. Acknowledgment of "
            "responsibility for some interventions may be politically achievable while others "
            "remain highly contested; the rule should not treat all acknowledgments as "
            "equivalent in difficulty or political cost. The rule names specific countries but "
            "the historical record of U.S. intervention is much longer; principled acknowledgment "
            "should follow a defined process rather than a fixed list that could immunize "
            "unacknowledged interventions."
        ),
    },
    {
        "card_id": "FPOL-RSPS-0002",
        "rule_notes": (
            "U.S. reconstruction aid to Iraq post-2003 amounted to over $60 billion, much of "
            "it characterized by massive waste, fraud, and abuse documented by SIGIR; future "
            "commitments require far better oversight structures, not simply more funding. "
            "'Sustained, long-term' commitment is difficult to codify without specific dollar "
            "amounts and multi-year authorization; annual appropriations processes will "
            "recurrently undermine the commitment without structural protection. Iraq's political "
            "environment makes some forms of reconstruction assistance counterproductive — aid "
            "flowing through corrupt institutions can strengthen those institutions rather than "
            "rebuilding civil society; the delivery mechanism is as important as the commitment. "
            "Some reconstruction commitments could be used by political actors to justify ongoing "
            "U.S. military presence in Iraq; the rule must decouple reconstruction assistance "
            "from military presence. The Iraqi government and public opinion have been divided "
            "on the extent and form of U.S. involvement; the rule should require that Iraqi "
            "agency in defining reconstruction priorities is respected."
        ),
    },
    {
        "card_id": "FPOL-RSPS-0003",
        "rule_notes": (
            "The U.S. has partially acknowledged its role in the 1953 coup — the State "
            "Department published a history acknowledging CIA involvement in 2013; the rule "
            "should specify what additional formal acknowledgment is required beyond existing "
            "disclosures. Acknowledgment in a 'diplomatic framework' requires Iranian "
            "willingness to engage in that framework; the rule cannot compel Iranian "
            "participation and must address what U.S. credibility looks like when acknowledged "
            "history is not sufficient to produce diplomatic progress. The 1953 coup is one of "
            "several historical grievances in U.S.-Iran relations; addressing it without "
            "addressing others (sanctions history, support for Iraq in the Iran-Iraq war, "
            "the 1988 Vincennes incident) risks appearing selective rather than principled. "
            "Framing acknowledgment as a 'prerequisite for credible engagement' could give "
            "hardliners in both countries a veto over diplomacy by refusing to acknowledge "
            "or accept acknowledgments as sufficient. Domestic opposition to acknowledging "
            "historical U.S. wrongdoing from intelligence community veterans and political "
            "actors will be significant; the political path to formal acknowledgment must "
            "be addressed."
        ),
    },
    {
        "card_id": "FPOL-RSPS-0004",
        "rule_notes": (
            "Similar bodies — the Church Committee, the 9/11 Commission — have successfully "
            "reviewed historical programs, but their findings have been implemented inconsistently "
            "and sometimes suppressed; structural independence requires more than appointment "
            "independence. 'Structurally independent of the executive branch' but with access "
            "to classified records creates a fundamental tension; independent review bodies "
            "with classified access are ultimately dependent on executive cooperation for that "
            "access, and this dependence must be addressed through statute. The body's mandate "
            "to 'periodically examine' and report every five years means each report covers a "
            "narrow recent window; a one-time comprehensive historical examination should "
            "precede the periodic review structure. Recommending 'reparative actions and "
            "diplomatic acknowledgments to Congress and the President' creates obligations "
            "only if there is a mechanism for Congress and the President to respond; a "
            "response-and-record requirement is needed. The body's proposed composition "
            "excludes intelligence and military professionals who have domain expertise "
            "in the operations being reviewed; their inclusion in some advisory capacity "
            "is needed for analytical credibility."
        ),
    },
    {
        "card_id": "FPOL-RSPS-0005",
        "rule_notes": (
            "'Multi-year, insulated commitments not subject to annual appropriations volatility' "
            "is the right structure but is extremely difficult to achieve under U.S. constitutional "
            "law, which gives Congress annual appropriations authority; a mandatory spending "
            "classification or compact structure that achieves durability must be specified. "
            "Causal attribution of harm — isolating U.S. action from other contributing factors "
            "— is methodologically complex; a standard of causal contribution rather than strict "
            "but-for causation is needed to prevent complexity from defeating accountability. "
            "Reparative assistance must be designed to reach affected populations, not just "
            "governments; where U.S. actions also destabilized government institutions, "
            "channeling reparative aid through those institutions may be counterproductive. "
            "The rule cross-references the review mechanism as the determining body; if that "
            "mechanism is not established or fails to function, this rule is unenforceable and "
            "the relationship between the two rules must be addressed. Some eligible countries "
            "— Iran, Cuba, Vietnam — are under U.S. sanctions regimes that would technically "
            "prohibit the reparative assistance this rule requires; how reparative assistance "
            "interacts with existing sanctions must be specified."
        ),
    },
    {
        "card_id": "FPOL-TRDS-0001",
        "rule_notes": (
            "'Widespread forced labor' requires a definition and a designated determination body; "
            "the rule should specify whether ILO reporting, State Department TIP reports, or an "
            "independent body makes the determination, with what evidentiary standard. Countries "
            "with significant forced labor — China, Qatar, Uzbekistan — are at different points "
            "in U.S. trade relationships; the rule's application to existing agreements requires "
            "a transition mechanism that is not provided. Ending trade agreements with forced "
            "labor states could harm civilian workers who depend on export industries for income; "
            "the rule should address the economic welfare of affected workers rather than treating "
            "trade restriction as purely punitive. 'Government self-reporting' is correctly "
            "excluded from the monitoring standard, but independent monitoring requires access "
            "that host governments may deny; consequences for access denial must be specified. "
            "The rule applies to preferential trade agreements but not to most-favored-nation "
            "status under WTO membership; a country can be excluded from a preferential agreement "
            "while still enjoying normal trade relations, limiting the rule's practical impact."
        ),
    },
    {
        "card_id": "FPOL-TRDS-0002",
        "rule_notes": (
            "ILO core conventions are referenced but ILO monitoring has limited enforcement "
            "authority; making ILO standards 'binding' through trade agreements requires defining "
            "what happens when ILO monitors report violations and what the enforcement timeline "
            "is. 'Same dispute resolution mechanisms as commercial provisions' is the right "
            "standard — USMCA's rapid response mechanism for Mexican labor violations is a "
            "useful model — but fast-track dispute resolution for labor claims requires "
            "political commitment that has been absent from most trade agreements. Private "
            "right of action for affected workers is a significant departure from current "
            "practice and would require legal standing in U.S. courts for foreign workers; "
            "this faces strong opposition from both business groups and sovereignty-focused "
            "legislators. Labor provisions in trade agreements require monitoring capacity "
            "in countries that may have limited regulatory infrastructure; capacity-building "
            "must accompany compliance monitoring requirements. In some partner countries "
            "associational rights can only be exercised through state-controlled unions; the "
            "rule should address whether compliance with the letter of ILO standards while "
            "maintaining state union monopolies satisfies the requirement."
        ),
    },
    {
        "card_id": "FPOL-TRDS-0003",
        "rule_notes": (
            "The rebuttable presumption approach significantly increases the evidentiary burden "
            "on U.S. importers, who may lack practical ability to audit global supply chains; "
            "the rule should address what constitutes adequate importer due diligence to rebut "
            "the presumption without creating barriers that only large corporations can meet. "
            "CBP's capacity to enforce import restrictions is already strained; extending the "
            "UFLPA framework globally without additional CBP resources would create backlogs "
            "that importers could exploit. The UFLPA's Uyghur-specific focus was politically "
            "achievable in a way a global framework may not be; the rule should acknowledge "
            "the political constraints and propose a phased implementation strategy. Some "
            "supply chain audits are conducted by firms with conflicts of interest; auditor "
            "independence and certification standards must accompany any extension of the "
            "framework. Small and medium enterprises often lack the supply chain visibility "
            "of large corporations; the global framework must include proportionate compliance "
            "requirements that do not effectively prohibit SME participation in international "
            "trade."
        ),
    },
    {
        "card_id": "FPOL-TRDS-0004",
        "rule_notes": (
            "The three-year review cycle means a country can deteriorate significantly between "
            "reviews without trade consequences; an emergency mechanism for accelerated review "
            "when conditions sharply worsen is needed. 'Specific, measurable, and independently "
            "verified' benchmarks are essential but the track record of benchmark-setting in "
            "trade agreements is poor — benchmarks are routinely set at levels that existing "
            "conditions already satisfy; an independent body with real authority to set "
            "meaningful benchmarks is needed. Proportionality between violations and trade "
            "consequences requires a defined formula; without one, consequences will be "
            "calibrated to geopolitical interests rather than violation severity. The "
            "independent interagency review body must include civil society and labor experts "
            "with genuine independence; past interagency processes have been dominated by "
            "trade-expansion interests. The rule allows only withdrawal of preferential "
            "tariff treatment as a consequence; a menu of graduated responses from diplomatic "
            "censure to trade suspension would allow more proportionate and targeted "
            "enforcement."
        ),
    },
    {
        "card_id": "FPOL-TRDS-0005",
        "rule_notes": (
            "Wage floor provisions calibrated to local purchasing power parity are technically "
            "complex and subject to methodological disputes about PPP calculations; independent "
            "determination of PPP wage floors is needed to prevent manipulation by either "
            "governments or trading partners. Corporate profit-sharing requirements in trade "
            "agreements are unprecedented and would face strong opposition from business groups; "
            "the legal and political path to implementing such requirements in international "
            "trade law must be addressed. 'Investment rules that prohibit relocation to evade "
            "labor rights compliance' requires a standard for what constitutes evasion versus "
            "legitimate business relocation; every dispute will contest this line. Adjustment "
            "assistance for workers in both the U.S. and partner countries requires funding "
            "from both governments; the U.S. cannot unilaterally require another country's "
            "government to fund worker adjustment, and its own adjustment assistance programs "
            "have been chronically underfunded. Trade standards alone cannot produce broadly "
            "shared prosperity in partner countries; complementary policies supporting workers "
            "in transition must accompany trade-linked labor standards."
        ),
    },
    {
        "card_id": "FPOL-CLMS-0001",
        "rule_notes": (
            "Treating climate change as a 'core foreign policy and national security priority' "
            "without specifying what changes in decision-making it requires is aspirational "
            "rather than structural; the rule needs to specify how climate analysis is "
            "integrated into foreign policy decisions and who is accountable for that integration. "
            "National security framing of climate can concentrate climate policy in military "
            "and intelligence institutions rather than civilian agencies better equipped to "
            "address systemic causes; the rule should specify which institutions lead. Climate "
            "change as a national security framing has historically been used to justify "
            "militarized responses to climate-driven instability (migration, resource conflict) "
            "rather than addressing root causes; the rule must prioritize prevention over "
            "securitized response. The rule does not address domestic consistency — a foreign "
            "policy that treats climate as a national security priority while subsidizing "
            "domestic fossil fuel production lacks credibility and will face legitimate "
            "criticism from allies and partners. Climate foreign policy intersects with "
            "trade, aid, and technology export policy in ways that must be explicitly "
            "coordinated rather than siloed."
        ),
    },
    {
        "card_id": "FPOL-CLMS-0002",
        "rule_notes": (
            "The Paris Agreement allows parties to set their own NDC targets; 'honor, exceed, "
            "and permanently commit' requires a domestic legal mechanism making withdrawal "
            "procedurally difficult and NDC ambition escalation enforceable, which the "
            "Agreement's voluntary structure does not provide. U.S. withdrawal and re-entry "
            "under successive administrations has damaged the credibility of U.S. commitments; "
            "the rule must address the domestic legal and institutional mechanisms that "
            "prevent future withdrawal rather than just stating a commitment. 'Exceed' NDC "
            "commitments is aspirational but must be defined against a specific baseline and "
            "timeline to be meaningful. The Paris Agreement's 1.5°C pathway requires "
            "acceleration of U.S. decarbonization well beyond current NDC commitments; "
            "the rule should reference this scientific benchmark explicitly. International "
            "climate cooperation requires reciprocal commitments from major emitters; U.S. "
            "leadership is necessary but not sufficient, and the rule should address how "
            "U.S. commitments are linked to progress by China, India, and other major emitters."
        ),
    },
    {
        "card_id": "FPOL-CLMS-0003",
        "rule_notes": (
            "U.S. climate finance commitments through international mechanisms have historically "
            "been underfunded and inconsistently delivered; a domestic legal mechanism for "
            "funding climate finance obligations that protects against annual appropriations "
            "volatility is needed. 'Developing nations' covers a wide range of countries with "
            "very different climate finance needs and capacities; the rule should distinguish "
            "between adaptation finance for the most vulnerable countries and broader climate "
            "investment for middle-income emerging economies. Climate finance effectiveness "
            "requires that funds actually reach affected communities rather than flowing "
            "primarily to governments or multilateral institutions; direct access mechanisms "
            "for local and civil society organizations must be supported. U.S. climate finance "
            "has sometimes been delivered in the form of loans rather than grants, increasing "
            "debt burdens for already-stressed low-income countries; the rule should specify "
            "the appropriate mix of grants, concessional loans, and technical assistance. "
            "Private sector climate finance mobilization is essential to meet the overall "
            "climate finance gap; the rule should address how public climate finance is "
            "designed to leverage private capital."
        ),
    },
    {
        "card_id": "FPOL-CLMS-0004",
        "rule_notes": (
            "Climate displacement is not yet recognized under the 1951 Refugee Convention "
            "or its 1967 Protocol; supporting international climate refugee protections requires "
            "either treaty amendment — politically very difficult — or development of new "
            "international instruments, and the rule should specify the diplomatic strategy. "
            "The distinction between climate-driven displacement and conflict-driven or "
            "economic displacement is legally and practically difficult to establish; mixed "
            "causation cases, which will be the majority, require workable standards. "
            "Recognizing climate displacement without creating corresponding U.S. immigration "
            "pathways is inconsistent; the rule should cross-reference domestic immigration "
            "and asylum policy. Some climate-affected countries are reluctant to accept the "
            "framing of their populations as 'climate refugees' because of concerns about "
            "sovereignty and permanent displacement rather than adaptation; the rule should "
            "address these concerns. The scale of potential climate displacement — hundreds of "
            "millions of people by mid-century on current trajectories — would overwhelm "
            "existing international protection frameworks; the rule must address the adequacy "
            "of existing mechanisms for the scale of need."
        ),
    },
    {
        "card_id": "FPOL-CLMS-0005",
        "rule_notes": (
            "U.S. executive directors at international financial institutions already have "
            "authority to oppose fossil fuel financing; the rule formalizes and strengthens "
            "this direction, but enforcement depends on consistent instructions to executive "
            "directors and their willingness to act against majority votes. IFI financing "
            "decisions are often defended as supporting 'energy access' for the global poor; "
            "the rule should address how to ensure genuine energy access — including through "
            "renewable energy alternatives — rather than simply eliminating fossil fuel finance "
            "without providing alternatives. Some developing countries have significant fossil "
            "fuel reserves that are central to their development strategies; U.S. opposition "
            "to fossil fuel financing in IFIs affects these countries' development options "
            "and creates political tensions that must be addressed through alternative finance "
            "mechanisms. The rule applies to U.S. international financial institutions but "
            "not to U.S. bilateral export finance through ExIm Bank and DFC, which continue "
            "to finance some fossil fuel projects; consistency across all U.S. international "
            "finance channels is needed. Eliminating fossil fuel financing creates transition "
            "risks for workers and communities in fossil fuel-dependent developing economies; "
            "just transition support must accompany the financing restriction."
        ),
    },
    {
        "card_id": "FPOL-INTL-0001",
        "rule_notes": (
            "'Genuine congressional oversight and approval' requires specifying what procedures "
            "satisfy the requirement — which programs need prior approval, which need "
            "notification, and which can proceed under standing authorities — rather than leaving "
            "it to executive-congressional negotiation. The Gang of Eight briefing model that "
            "currently satisfies 'Congressional oversight' requirements allows only a handful of "
            "members to receive covert action notices and prohibits them from disclosing "
            "information to colleagues; this is not meaningful democratic oversight. Prior "
            "approval for covert action would constitute a significant structural change; the "
            "speed requirements of intelligence operations create legitimate tension with "
            "legislative approval timelines that must be addressed through emergency procedures. "
            "Oversight of ongoing covert programs — not just initial approval — is the larger "
            "gap in current law; persistent activities under standing authorities have operated "
            "for years without meaningful Congressional review. The rule must address how "
            "oversight applies to 'finding'-based authorities versus Title 50 covert action "
            "programs and the increasing use of Title 10 special operations authorities to "
            "conduct covert-like activities outside the covert action framework."
        ),
    },
    {
        "card_id": "FPOL-INTL-0002",
        "rule_notes": (
            "The U.S. targeted killing program has operated under classified legal memoranda "
            "that define 'active armed conflict' expansively enough to apply nearly anywhere; "
            "the rule's prohibition outside 'active armed conflict' is only meaningful if "
            "that term is defined by statute rather than executive interpretation. Civilian "
            "casualty accounting under the current framework has relied on defining all "
            "military-age males in a strike zone as combatants; this standard must be "
            "explicitly rejected in the rule. Prohibiting extrajudicial killings outside "
            "active armed conflict does not address the accountability gap for those that "
            "occurred during declared conflicts; the rule should address accountability for "
            "past violations. Drone strike operations may be conducted by CIA under covert "
            "action authorities rather than DoD authorities; the prohibition must apply "
            "equally to both agencies regardless of which authority is invoked. Partner "
            "forces conducting U.S.-enabled strikes face even less accountability than "
            "direct U.S. strikes; the rule must address U.S. legal responsibility for "
            "civilian casualties caused by U.S.-enabled partner operations."
        ),
    },
    {
        "card_id": "FPOL-INTL-0003",
        "rule_notes": (
            "The prohibition on intelligence support to rights-violating security forces "
            "mirrors the Leahy Law's structure; like the Leahy Law, it will only be effective "
            "if vetting processes are adequately funded and not subject to national security "
            "waivers. 'Human rights violations' as a threshold requires a defined standard and "
            "designation body; the executive branch's control over these determinations allows "
            "indefinite deferral as with Leahy Law violations. Intelligence sharing arrangements "
            "with foreign services are often classified and operate outside the oversight "
            "mechanisms that apply to military assistance; the rule must specifically address "
            "classified intelligence relationships. The rule prohibits intelligence 'support' "
            "but does not define whether training, equipment, analytical products, and joint "
            "operations all constitute prohibited support; each category may require different "
            "treatment. Ending intelligence support to rights-violating partners may create "
            "capability gaps that the U.S. addresses through other means; the rule must be "
            "robust to workarounds that achieve the same operational objectives."
        ),
    },
    {
        "card_id": "FPOL-INTL-0004",
        "rule_notes": (
            "Systematic declassification of historical covert operations is resisted by "
            "intelligence agencies on grounds that sources and methods remain sensitive "
            "decades later; the rule needs an independent declassification review mechanism "
            "that can make authoritative decisions over agency objections. The National "
            "Declassification Center exists but processes documents slowly and with "
            "inadequate resources; the rule must be paired with funding and staffing "
            "commitments. Historical accounting of covert operations may expose U.S. "
            "officials and their foreign partners to legal liability; a statutory framework "
            "addressing how accountability and historical transparency interact is needed. "
            "Some covert operations remain sensitive because they involved or implicate "
            "current allies; diplomatic management of these disclosures is needed alongside "
            "the declassification mandate. Declassification without accompanying analysis "
            "and accessible presentation produces document dumps rather than genuine public "
            "accounting; the rule should require contextualized public reporting, not only "
            "document release."
        ),
    },
    {
        "card_id": "FPOL-INTL-0005",
        "rule_notes": (
            "Mass surveillance of foreign populations by U.S. intelligence agencies operates "
            "under Executive Order 12333 rather than FISA, which provides far weaker legal "
            "standards; the rule should specify that foreign persons' privacy rights are "
            "protected under statutory standards comparable to U.S. persons' FISA protections. "
            "The Five Eyes and other intelligence-sharing arrangements enable U.S. surveillance "
            "of U.S. persons through foreign partner collection; the rule should address "
            "whether it covers surveillance conducted by partners at U.S. direction. "
            "Applying privacy standards 'proportionate to privacy rights' for foreign "
            "populations requires defining what those rights are and where the U.S. "
            "recognizes them as applying; this is currently contested in international law. "
            "Mass surveillance programs are classified and operate without meaningful "
            "public oversight; the rule must address what oversight mechanisms — "
            "Congressional, judicial, or independent — apply to foreign collection programs. "
            "Some foreign intelligence collection is genuinely essential to national security; "
            "the rule should distinguish between mass surveillance of civilian populations "
            "and targeted collection against security threats rather than prohibiting "
            "foreign intelligence collection categorically."
        ),
    },
]


# ---------------------------------------------------------------------------
# Transformation functions
# ---------------------------------------------------------------------------

def apply_status_update(content: str, card_id: str) -> str:
    """Replace status-missing with status-included, anchored to card ID."""
    old = f'status-missing" id="{card_id}"'
    new = f'status-included" id="{card_id}"'
    if old not in content:
        print(f"  WARNING: status pattern not found for {card_id}", file=sys.stderr)
        return content
    return content.replace(old, new, 1)


def apply_badge_update_sci_tech(content: str, card_id: str) -> str:
    """Replace Proposed badge, anchored to card ID (sci-tech uses <p> for rule-id)."""
    old = f'<p class="rule-id">{card_id}</p>\n<span class="rule-badge">Proposed</span>'
    new = f'<p class="rule-id">{card_id}</p>\n<span class="rule-badge">Included</span>'
    if old not in content:
        print(f"  WARNING: badge pattern not found for {card_id}", file=sys.stderr)
        return content
    return content.replace(old, new, 1)


def apply_badge_update_fpol(content: str, card_id: str) -> str:
    """Replace Proposed badge, anchored to card ID (fpol uses <code> for rule-id)."""
    old = f'<code class="rule-id">{card_id}</code>\n<span class="rule-badge">Proposed</span>'
    new = f'<code class="rule-id">{card_id}</code>\n<span class="rule-badge">Included</span>'
    if old not in content:
        print(f"  WARNING: badge pattern not found for {card_id}", file=sys.stderr)
        return content
    return content.replace(old, new, 1)


def insert_rule_plain(content: str, card_id: str, rule_plain: str) -> str:
    """Insert rule-plain before the rule-title, anchored to card ID."""
    card_start = content.find(f'id="{card_id}"')
    if card_start == -1:
        print(f"  WARNING: card not found for {card_id}", file=sys.stderr)
        return content
    header_close = content.find('</div>\n<p class="rule-title">', card_start)
    if header_close == -1:
        print(f"  WARNING: rule-title anchor not found for {card_id}", file=sys.stderr)
        return content
    insert_at = header_close + len('</div>\n')
    insertion = f'<p class="rule-plain">{rule_plain}</p>\n'
    return content[:insert_at] + insertion + content[insert_at:]


def insert_rule_notes(content: str, card_id: str, rule_notes: str) -> str:
    """Insert rule-notes after rule-stmt's </p>, before the card's closing </div>."""
    card_start = content.find(f'id="{card_id}"')
    if card_start == -1:
        print(f"  WARNING: card not found for {card_id}", file=sys.stderr)
        return content
    stmt_close = content.find('</p>\n</div>', card_start)
    if stmt_close == -1:
        print(f"  WARNING: stmt-close pattern not found for {card_id}", file=sys.stderr)
        return content
    insert_at = stmt_close + len('</p>')
    insertion = f'\n<p class="rule-notes">{rule_notes}</p>'
    return content[:insert_at] + insertion + content[insert_at:]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_file(filepath: Path, cards: list, is_sci_tech: bool) -> None:
    content = filepath.read_text(encoding="utf-8")
    original_content = content
    errors = 0

    for card in cards:
        card_id = card["card_id"]

        # 1. Status class
        before = content
        content = apply_status_update(content, card_id)
        if content == before:
            errors += 1

        # 2. Badge text
        before = content
        if is_sci_tech:
            content = apply_badge_update_sci_tech(content, card_id)
        else:
            content = apply_badge_update_fpol(content, card_id)
        if content == before:
            errors += 1

        # 3. Insert rule-plain (sci-tech only)
        if is_sci_tech and card.get("rule_plain"):
            before = content
            content = insert_rule_plain(content, card_id, card["rule_plain"])
            if content == before:
                errors += 1

        # 4. Insert rule-notes
        before = content
        content = insert_rule_notes(content, card_id, card["rule_notes"])
        if content == before:
            errors += 1

    if errors > 0:
        print(f"ERRORS: {errors} replacements failed in {filepath.name}.", file=sys.stderr)
        sys.exit(1)

    if content == original_content:
        print(f"No changes made to {filepath.name} (already up-to-date?).")
    else:
        filepath.write_text(content, encoding="utf-8")
        print(f"Updated {filepath.name}: {len(cards)} cards processed.")


def main() -> None:
    print("Processing science-technology-space.html ...")
    process_file(SCI_TECH_FILE, SCI_TECH_CARDS, is_sci_tech=True)

    print("Processing foreign-policy.html ...")
    process_file(FPOL_FILE, FOREIGN_POLICY_CARDS, is_sci_tech=False)

    print("Done.")


if __name__ == "__main__":
    main()
