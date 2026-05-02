#!/usr/bin/env python3
"""Transform all status-missing policy cards in healthcare.html to status-included.

Adds expanded rule statements and adversarial review notes to each card.
Run from repo root: python3 scripts/transform-healthcare-cards.py
"""
from pathlib import Path
from bs4 import BeautifulSoup

HTML_PATH = Path("docs/pillars/healthcare.html")

# Keys: "FAMILY-NNNN" (strip "HLTH-" prefix from card IDs, e.g. "ACCS-0001")
# stmt=None  → keep existing stmt text unchanged
# stmt=str   → replace/insert the .rule-stmt element
# notes      → always inserted as .rule-notes (skipped if .rule-notes already present)
CARD_CONTENT: dict[str, dict] = {

    # ── ACCS (NO-STMT) ──────────────────────────────────────────────────────
    "ACCS-0001": {
        "stmt": (
            "Universal healthcare coverage is extended to all U.S. citizens and all "
            "lawful permanent residents who have maintained continuous U.S. residency for "
            "a minimum of five years. Coverage is not conditional on employment status, "
            "income level, marital status, or cooperation with immigration enforcement "
            "proceedings. Persons in active immigration adjudication retain coverage "
            "during the pendency of their proceedings."
        ),
        "notes": (
            "Adversarial review: The five-year LPR threshold may inadvertently exclude "
            "individuals who re-entered after brief absences abroad — the rule should "
            "specify that temporary absences under 180 days do not break continuity. "
            "Stateless persons lawfully present in the U.S. are unaddressed and should "
            "be explicitly included. Conditioning coverage on 'cooperation with "
            "immigration enforcement' creates a coercion risk; the absence of such a "
            "condition here is intentional and should be preserved against future "
            "amendment attempts."
        ),
    },
    "ACCS-0002": {
        "stmt": (
            "All persons eligible for coverage under ACCS-0001 are entitled to elective "
            "healthcare services. All persons physically present in the United States — "
            "regardless of immigration status, documentation status, or insurance "
            "coverage — are entitled to emergency healthcare services. The "
            "classification of a presentation as emergency or elective is made by the "
            "treating or admitting clinician based on medical criteria at the time of "
            "presentation; it is not made by administrative staff, billing personnel, "
            "or algorithmic triage systems prior to clinical evaluation. Where "
            "classification is ambiguous, the presentation is treated as emergency "
            "pending clinical evaluation."
        ),
        "notes": (
            "Adversarial review: Mixed-urgency presentations (e.g., a patient with "
            "both a chronic condition and an acute complaint) may lead to post-stabilization "
            "billing reclassification. The rule must explicitly bar retroactive "
            "reclassification for billing purposes after emergency care is delivered. "
            "Administrative pressure on clinicians to classify borderline cases as "
            "elective must be prohibited by accompanying anti-coercion rules. "
            "Providers may attempt to 'screen out' non-covered patients before the "
            "EMTALA medical screening exam — this rule must be read in conjunction "
            "with strengthened EMTALA enforcement."
        ),
    },
    "ACCS-0003": {
        "stmt": (
            "Persons with conditions that are severe, life-threatening, or rapidly "
            "deteriorating receive the full course of medically necessary care required "
            "to stabilize and treat their condition, regardless of coverage tier, "
            "immigration status, or prior authorization status. No delay in care may "
            "be imposed pending coverage verification, prior authorization, or billing "
            "disputes. Where coverage disputes arise during or after an emergency "
            "episode, they are resolved administratively without interrupting the "
            "delivery of care. Mechanisms to prevent fraud may not be designed or "
            "applied in ways that deter access to genuine emergency care."
        ),
        "notes": (
            "Adversarial review: 'Rapidly deteriorating' must have a clear clinical "
            "definition to prevent gaming; this rule should cross-reference ACCS-0002's "
            "clinician-determination standard. Post-hoc billing denials for stabilization "
            "care — delivered on an emergency basis to patients who cannot be billed — "
            "create a revenue problem for providers that must be addressed through "
            "reimbursement mechanisms, not by narrowing the right. Patients who arrive "
            "stable but are known to deteriorate without ongoing treatment (e.g., "
            "insulin-dependent diabetes without insulin) must be covered; the 'rapidly "
            "deteriorating' language should encompass foreseeable deterioration."
        ),
    },

    # ── AINL (SHORT-STMT, 30 cards) ─────────────────────────────────────────
    "AINL-0001": {
        "stmt": (
            "AI systems used in clinical diagnosis, treatment recommendation, prior "
            "authorization, utilization review, risk stratification, or any other "
            "function that directly affects patient care access or outcomes are classified "
            "as high-risk and subject to mandatory pre-deployment registration with the "
            "relevant federal regulatory authority, independent validation by a "
            "financially independent third party, public disclosure of performance "
            "metrics including accuracy, sensitivity, specificity, and subgroup "
            "performance across demographic groups, and mandatory adverse event "
            "reporting within 30 days of identification.<sup><a href=\"#fn14\">[14]</a></sup>"
        ),
        "notes": (
            "Adversarial review: 'High-risk' classification must be clearly defined to "
            "prevent vendors from restructuring products to avoid it — e.g., calling a "
            "denial-generating algorithm a 'documentation tool.' Registration requirements "
            "must apply to updates and new versions, not just initial deployment. "
            "Independent validation must prohibit any financial relationship between the "
            "validator and the vendor, including indirect relationships through parent companies."
        ),
    },
    "AINL-0002": {
        "stmt": (
            "AI systems deployed in clinical settings must function as support tools "
            "that assist clinical decision-making, not as replacements for physician "
            "judgment. For any decision affecting patient care, the treating clinician "
            "must independently evaluate the patient's condition and chart a clinical "
            "basis for their decision that is independent of any AI recommendation. "
            "Productivity metrics and performance measurement systems may not reward "
            "clinicians for speed of decision-making in ways that discourage independent "
            "evaluation of AI-generated recommendations."
        ),
        "notes": (
            "Adversarial review: 'Independently evaluate' is subject to rubber-stamping "
            "in high-volume settings; the rule requires documentation of independent basis "
            "not just the presence of a physician. Productivity systems that punish "
            "physicians for overriding AI recommendations are a real enforcement risk "
            "and must be explicitly prohibited. Vendor agreements that make AI override "
            "rates a quality metric are a specific abuse path to address."
        ),
    },
    "AINL-0003": {
        "stmt": (
            "AI-assisted clinical decision support may be used only in contexts where "
            "it assists and does not substitute for qualified clinical judgment. A "
            "physician may deviate from any AI recommendation without administrative "
            "penalty, documentation burden, or workflow friction. The clinical logic "
            "underlying decision support recommendations must be publicly disclosed in "
            "sufficient detail to allow clinical evaluation; black-box proprietary "
            "algorithms may not be used in clinical decision support without independent "
            "algorithm publication or equivalent disclosure."
        ),
        "notes": (
            "Adversarial review: 'Assist not substitute' is enforced in principle but "
            "commonly violated in practice through workflow design — systems that route "
            "cases away from physicians when AI gives a negative recommendation effectively "
            "substitute. Override documentation requirements that create workflow friction "
            "must be prohibited. Proprietary claims will be the primary tool used to resist "
            "transparency requirements."
        ),
    },
    "AINL-0004": {
        "stmt": (
            "AI systems used in healthcare must meet evidence standards equivalent to "
            "those required for clinical interventions: prospective clinical validation "
            "in representative populations, peer-reviewed publication of validation "
            "studies, public disclosure of accuracy, bias, and subgroup performance "
            "metrics across race, sex, age, disability, socioeconomic status, and "
            "geography, and independent replication by a party with no financial "
            "interest in the system's deployment."
        ),
        "notes": (
            "Adversarial review: 'Prospective validation' requirements are routinely "
            "circumvented by using retrospective data labeled as validation. Publication "
            "of validation studies in company-sponsored journals should not satisfy the "
            "independence requirement. Subgroup performance disclosures must include "
            "sufficient sample sizes for statistical validity — reporting subgroup "
            "performance from samples too small to detect disparities is a common evasion."
        ),
    },
    "AINL-0005": {
        "stmt": (
            "Deployed AI systems in healthcare must be subject to continuous, independent "
            "post-deployment monitoring for harmful outcomes, performance drift, "
            "demographic disparities, and failure modes. The monitoring entity must be "
            "financially independent of the AI vendor and the deploying healthcare "
            "entity. Performance drift detection must trigger mandatory review and "
            "revalidation before continued deployment is permitted. Adverse events "
            "attributable to AI system failures or recommendations must be reported to "
            "the federal regulatory authority within 30 days of identification."
        ),
        "notes": (
            "Adversarial review: 'Continuous monitoring' without defined frequency and "
            "methodology is effectively no monitoring. Financial independence of monitors "
            "must be defined to exclude indirect relationships (e.g., shared investors "
            "or parent companies). 30-day adverse event reporting creates a strong "
            "incentive to define events narrowly; mandatory review of ambiguous events "
            "is necessary."
        ),
    },
    "AINL-0006": {
        "stmt": (
            "No AI system may independently issue, approve, or reject clinical diagnoses "
            "or prescriptions for controlled or high-risk medications. Every diagnosis "
            "and prescription must be authorized by a clearly identified, licensed human "
            "professional who bears clinical and legal accountability for the decision. "
            "AI-only workflows that economically incentivize removing the physician from "
            "the approval chain are prohibited."
        ),
        "notes": (
            "Adversarial review: 'Clearly identified licensed professional' must include "
            "a requirement that the professional is the one actually making the decision, "
            "not a rubber-stamp on an AI recommendation. Economic incentive structures "
            "that pay physicians per-case at volume rates effectively remove meaningful "
            "review; staffing ratio minimums may be needed as a companion rule."
        ),
    },
    "AINL-0008": {
        "stmt": (
            "Human reviewers in AI-assisted clinical and administrative decisions must "
            "exercise independent clinical or administrative judgment. Documentation of "
            "the independent basis for the reviewer's decision is required. Productivity "
            "metrics, throughput targets, or performance evaluations may not be designed "
            "in ways that penalize reviewers for disagreeing with AI recommendations or "
            "for taking additional time to conduct independent review."
        ),
        "notes": (
            "Adversarial review: The distinction between 'rubber-stamp' and 'independent' "
            "review is difficult to enforce without observational studies of reviewer "
            "behavior. Case-time-in-queue metrics are a common covert mechanism to "
            "create throughput pressure that eliminates independent review in practice. "
            "Documentation requirements must include what the reviewer independently "
            "considered, not just a check box."
        ),
    },
    "AINL-0009": {
        "stmt": (
            "AI systems may be used to assist in evaluating prior authorization requests "
            "but may not be the primary basis for approval or denial decisions. The "
            "'primary basis' prohibition includes systems that present approval as the "
            "default path and route all non-approvals to AI review — making denial the "
            "path of least resistance — even where a human technically signs off. Every "
            "prior authorization decision must reflect independent clinical "
            "judgment.<sup><a href=\"#fn14\">[14]</a></sup>"
        ),
        "notes": (
            "Adversarial review: 'Approval only' workflow designs evade spirit of this "
            "rule while technically complying — insurers approve via AI but route "
            "borderline cases to difficult denial-only queues. The 'primary basis' "
            "prohibition must be defined functionally, not based on the vendor's "
            "characterization of the workflow."
        ),
    },
    "AINL-0010": {
        "stmt": (
            "Prior to any denial of prior authorization based in whole or in part on "
            "AI review, a licensed clinician must review the full clinical record, "
            "apply specialty-relevant medical judgment, and document an independent "
            "clinical basis for the denial. The reviewing clinician must hold a license "
            "relevant to the clinical specialty of the requested care. Denials issued "
            "without prior independent human review are void and may not be enforced."
        ),
        "notes": (
            "Adversarial review: 'Full clinical record' access must be actually provided "
            "to reviewers — not just technically available. 'Specialty-relevant' must "
            "be defined in regulation; oncology denials reviewed by general internists "
            "are a common abuse pattern. Void denials must trigger automatic coverage "
            "pending valid re-review rather than leaving patients in limbo."
        ),
    },
    "AINL-0011": {
        "stmt": (
            "An AI system's failure to flag, route, or respond to a prior authorization "
            "request may not function as a constructive denial. Every request submitted "
            "through a covered system receives an affirmative human review and decision "
            "within required timelines regardless of AI system output or the absence "
            "thereof. AI non-response triggers escalation to direct human review, not "
            "administrative closure."
        ),
        "notes": (
            "Adversarial review: Constructive denial through AI non-response is an "
            "active abuse pattern — systems designed to time out, lose requests, or "
            "generate ambiguous responses that require patient re-submission effectively "
            "deny care without a denial on record. Escalation pathways must be monitored "
            "for volume and patterns."
        ),
    },
    "AINL-0012": {
        "stmt": (
            "Every prior authorization denial must clearly identify the licensed "
            "clinician who made the denial decision, the specific clinical basis for "
            "the denial, and the clinical evidence or guidelines relied upon. Denials "
            "that cite AI-generated outputs, proprietary scoring models, or statistical "
            "population norms as the basis — without an independent clinical evaluation "
            "of the specific patient's circumstances — are void."
        ),
        "notes": (
            "Adversarial review: 'Specific clinical basis' requirements are routinely "
            "evaded with boilerplate language citing 'clinical guidelines' without "
            "specifying which guideline, which version, and how it applies to this "
            "patient. Regulators must require structured denial formats that cannot be "
            "satisfied with generic template language."
        ),
    },
    "AINL-0013": {
        "stmt": (
            "All AI systems used in healthcare coverage decisions must be subject to "
            "mandatory annual disparate-impact audits conducted by a financially "
            "independent auditor, covering race, sex, age, disability status, "
            "socioeconomic status, and geography. Audit methodology must be publicly "
            "disclosed. Audits that identify statistically significant disparities "
            "trigger mandatory corrective action plans within 90 days; plans must "
            "include specific remediation milestones. Audit results must be publicly "
            "disclosed regardless of outcome."
        ),
        "notes": (
            "Adversarial review: Annual audits may be too infrequent for high-volume "
            "systems — continuous monitoring with annual summary reporting is preferable. "
            "Auditor independence requirements must define 'independent' to exclude "
            "firms with other consulting relationships with the audited entity. "
            "90-day corrective action plans with no binding enforcement mechanism "
            "are ineffective; suspension of system deployment until correction is "
            "completed must be available as a remedy."
        ),
    },
    "AINL-0014": {
        "stmt": (
            "Cases not flagged, routed, or reviewed by an AI triage system are entitled "
            "to the same decision timelines as AI-flagged cases. Healthcare entities "
            "must separately track and publicly report decision timelines for AI-reviewed "
            "and non-AI-reviewed cases. Review capacity must be equalized so that "
            "de-prioritization of non-AI-flagged cases does not result in systematic "
            "delay for conditions the AI fails to detect or categorize."
        ),
        "notes": (
            "Adversarial review: AI systems that systematically underperform on certain "
            "conditions (e.g., rare diseases, conditions less prevalent in training data) "
            "create a disparate-delay problem that manifests as systematic harm to the "
            "patients with those conditions. Separate tracking and reporting requirements "
            "are essential for detecting this pattern."
        ),
    },
    "AINL-0015": {
        "stmt": (
            "AI systems used in any care-access decision — including prior authorization, "
            "network routing, and coverage determinations — must generate plain-language, "
            "case-specific explanations that a patient and non-specialist clinician can "
            "understand. Explanations must identify the specific factors the system "
            "used to reach its output. Black-box systems that cannot generate such "
            "explanations are prohibited in any context affecting care access."
        ),
        "notes": (
            "Adversarial review: 'Plain language' generated by a second AI system "
            "translating a black-box output does not satisfy the transparency requirement "
            "— the rule addresses interpretability of the underlying model, not the "
            "readability of post-hoc summaries. Large language model 'explanation' "
            "layers that generate plausible-sounding rationale not derived from the "
            "actual model outputs are a specific abuse path to address."
        ),
    },
    "AINL-0017": {
        "stmt": (
            "Upon patient request, any entity that used an AI system in a coverage or "
            "care-access decision must provide a plain-language explanation of the role "
            "the AI system played within five business days. Patients have 30 days from "
            "any adverse decision to request this explanation and appeal on the basis "
            "of AI-related errors. The entity bears the burden of identifying AI "
            "involvement in any decision under appeal; failure to disclose known AI "
            "involvement is a material misrepresentation."
        ),
        "notes": (
            "Adversarial review: Five-day disclosure timelines create delays that are "
            "clinically harmful in urgent cases; urgent requests should be expedited "
            "to 24–48 hours. The 30-day appeal window may be too short for patients "
            "with complex conditions or limited access to advocates; extensions for "
            "good cause must be available. 'Material misrepresentation' consequences "
            "must include enforceable penalties, not just opportunity for re-review."
        ),
    },
    "AINL-0018": {
        "stmt": (
            "Every patient has the right to receive care from a human clinician rather "
            "than an AI system in any clinical context. No healthcare entity may offer "
            "AI-only pathways as the sole option for any covered service. Where a "
            "human-delivered equivalent exists, it must be offered at equivalent cost "
            "to the patient. AI-only pathways may not be offered at lower cost in ways "
            "that effectively coerce patients into AI care through financial pressure."
        ),
        "notes": (
            "Adversarial review: 'Equivalent cost' requirements must be enforced against "
            "co-pay structures, not just nominal list prices. The right to human care is "
            "meaningless without sufficient human clinician supply; workforce policies "
            "are necessary companions. Emergency situations where AI is the only available "
            "resource at a given moment must be distinguished from structural design "
            "choices that eliminate human pathways."
        ),
    },
    "AINL-0019": {
        "stmt": (
            "Before any AI system is used in a patient's care, the patient must receive "
            "clear, plain-language disclosure of the AI system's role, capabilities, "
            "and limitations. Patients may decline AI involvement and must be offered "
            "a human alternative without cost penalty or reduction in care quality. AI "
            "consent must be obtained separately from general consent to care — it may "
            "not be bundled into general admission forms or terms-of-service agreements."
        ),
        "notes": (
            "Adversarial review: AI consent bundled into general consent documents is "
            "already a standard industry practice that renders consent meaningless in "
            "practice. Regulatory enforcement of the unbundling requirement must be "
            "proactive. 'Without cost penalty' must address indirect penalties such as "
            "longer wait times for human care alternatives."
        ),
    },
    "AINL-0020": {
        "stmt": (
            "Patient data used in AI-assisted healthcare systems is subject to privacy "
            "protections stricter than HIPAA minimum standards. No patient data may be "
            "transferred to AI training datasets or used to improve AI systems outside "
            "the treating entity without explicit, informed, revocable patient consent "
            "and regulatory approval. Data breach or unauthorized use must be reported "
            "within 72 hours of identification to the patient and the relevant regulatory "
            "authority."
        ),
        "notes": (
            "Adversarial review: HIPAA's 'de-identification' standards have been shown "
            "to be inadequate against modern re-identification techniques; stricter "
            "standards for AI training data must be defined. 'Treating entity' must be "
            "narrowly defined to prevent broad data-sharing within corporate health "
            "systems being treated as intra-entity. The 72-hour reporting window may be "
            "technically impractical for complex breaches; good-faith reporting "
            "requirements must account for this."
        ),
    },
    "AINL-0021": {
        "stmt": (
            "Patient data generated through healthcare AI systems may not be used for "
            "advertising, consumer profiling, commercial product development, or "
            "actuarial underwriting by insurers, employers, or any commercial third "
            "party. Healthcare entities may not condition access to care or reduce care "
            "quality based on a patient's refusal to consent to commercial secondary "
            "use of their health data. Violations carry a private right of action with "
            "statutory damages."
        ),
        "notes": (
            "Adversarial review: 'Actuarial underwriting' prohibitions must explicitly "
            "cover indirect use — e.g., using AI-derived behavioral profiles not "
            "nominally labeled as health data. Private right of action is essential "
            "given limited regulatory enforcement capacity; statutory damages must be "
            "set high enough to deter violations at scale."
        ),
    },
    "AINL-0022": {
        "stmt": (
            "Secondary use of patient data in AI research requires review equivalent "
            "to human subjects research, chain-of-custody documentation tracking all "
            "transfers and uses of the data, and a re-identification risk assessment "
            "conducted by an independent expert prior to any public data release or "
            "broad data-sharing agreement. Researchers who identify re-identification "
            "vulnerabilities must report them to the data custodian within 30 days."
        ),
        "notes": (
            "Adversarial review: IRB-equivalent review requirements for retrospective "
            "data analysis are frequently waived as 'minimal risk' — the minimal risk "
            "determination must itself be subject to independent review when sensitive "
            "health data is involved. Re-identification risk assessments conducted by "
            "researchers within the same institution as the data custodian lack "
            "independence; external review must be required."
        ),
    },
    "AINL-0023": {
        "stmt": (
            "AI systems in healthcare must be designed to fail safely: when uncertain, "
            "out of scope, or encountering conditions outside their validated parameters, "
            "they must alert a human reviewer rather than generate a default output. "
            "Silent failure modes — where the system produces an output with no "
            "indication of low confidence — are prohibited in systems used to inform "
            "care-access decisions. Denial-as-default failure modes are prohibited; "
            "uncertainty must produce escalation to human review, not denial. Scope "
            "drift monitoring must detect and flag cases that fall outside the "
            "system's validated use parameters."
        ),
        "notes": (
            "Adversarial review: 'Alert a human reviewer' is meaningless if reviewer "
            "queues are understaffed; adequate human review capacity must accompany "
            "any safe-failure regime. 'Silent failure' must be clearly defined to include "
            "cases where the system generates a confident-appearing output on edge cases "
            "outside its training distribution."
        ),
    },
    "AINL-0024": {
        "stmt": (
            "AI systems in healthcare must communicate explicit confidence levels with "
            "all outputs. Systems that cannot generate reliable confidence estimates "
            "for a given output type may not be deployed in care-access decision "
            "contexts. Confidence notation must be as visually prominent as the output "
            "itself — it may not be relegated to footnotes, technical appendices, or "
            "obscured from clinical users by interface design choices."
        ),
        "notes": (
            "Adversarial review: Confidence level communication can be gamed by "
            "calibrating confidence notation to system-average accuracy rather than "
            "case-specific uncertainty — appearing confident while systematically "
            "underperforming on edge cases. Confidence levels must be validated "
            "against actual case outcomes, not against abstract model confidence metrics."
        ),
    },
    "AINL-0025": {
        "stmt": (
            "AI systems used in healthcare must be evaluated for algorithmic bias before "
            "deployment and annually thereafter, with disaggregated performance metrics "
            "published across all relevant demographic groups. Unmitigated disparate "
            "impact — where the system performs materially worse for members of "
            "protected classes — disqualifies the system from deployment until the "
            "disparity is corrected and independently verified."
        ),
        "notes": (
            "Adversarial review: 'Material' disparate impact thresholds must be "
            "numerically defined in regulation — leaving them to case-by-case judgment "
            "creates inconsistency and evasion. Annual bias evaluations may be conducted "
            "using pre-deployment data rather than real-world deployment data; "
            "post-deployment performance monitoring must be mandatory."
        ),
    },
    "AINL-0026": {
        "stmt": (
            "Healthcare entities must monitor for and publicly report demographic "
            "disparities in care access, coverage decisions, and clinical outcomes "
            "before and after AI system deployment to identify AI-attributable "
            "disparities. Where outcomes worsen for a protected class coincidentally "
            "with an AI deployment, the burden shifts to the entity to demonstrate "
            "the AI system is not a contributing cause. Corrective action must be "
            "initiated within 90 days of identifying a statistically significant "
            "AI-attributable disparity."
        ),
        "notes": (
            "Adversarial review: Pre-post comparison methodology is subject to "
            "confounding — entities will argue that worsening disparities are "
            "attributable to external factors. The burden-shifting provision is "
            "important but must be paired with clear evidentiary standards for "
            "what the entity must demonstrate. 90-day corrective action timelines "
            "must include a requirement to suspend the AI system if correction cannot "
            "be demonstrated within the timeline."
        ),
    },
    "AINL-0027": {
        "stmt": (
            "AI systems developed with publicly funded research must be published "
            "under open-access licenses and must not be exploited by commercial "
            "entities to bypass the clinical validation requirements that apply to "
            "privately developed systems. Research funding status does not exempt an "
            "AI system from clinical validation requirements before patient deployment. "
            "Public research investment in AI must be publicly disclosed and must be "
            "deployed for public benefit."
        ),
        "notes": (
            "Adversarial review: Commercial spinoffs from publicly funded AI research "
            "often argue they have 'transformed' the original research sufficiently "
            "to avoid open-access requirements — the rule must define continuation "
            "obligations clearly. Research framing must not be used to avoid regulatory "
            "oversight of systems that are functionally deployed for clinical use."
        ),
    },
    "AINL-0028": {
        "stmt": (
            "A minimum of 20% of federal AI research funding directed to healthcare "
            "applications must be dedicated to research into neglected conditions — "
            "defined as conditions with disproportionate disease burden relative to "
            "current research investment, conditions affecting populations with limited "
            "commercial market value, and conditions that face systemic research bias. "
            "The definition of 'neglected conditions' must be made by an independent "
            "committee with appropriate expertise and must be reviewed and updated "
            "every three years."
        ),
        "notes": (
            "Adversarial review: A 20% minimum may be gamed by categorizing conditions "
            "broadly to capture commercially attractive conditions under the 'neglected' "
            "umbrella. Independent committee composition must be defined with COI "
            "exclusions. If enforcement is tied to future appropriations rather than "
            "current spending floors, the requirement has no binding force."
        ),
    },
    "AINL-0029": {
        "stmt": (
            "Research priority-setting for healthcare AI must be conducted by committees "
            "that are commercially independent — meaning free from financial ties to "
            "pharmaceutical companies, device manufacturers, and AI vendors. Priority "
            "areas must explicitly include sexually transmitted infections, chronic "
            "conditions disproportionately affecting low-income populations, and "
            "addiction treatment, regardless of commercial interest in these areas."
        ),
        "notes": (
            "Adversarial review: 'Commercially independent' committees can be captured "
            "through revolving-door relationships, alumni networks, and ideology rather "
            "than direct financial ties. Explicit mandate for STI, chronic condition, "
            "and addiction research is important precisely because these are the areas "
            "most likely to be de-prioritized without mandatory inclusion."
        ),
    },
    "AINL-0030": {
        "stmt": (
            "Conflicts of interest held by members of AI oversight bodies must be "
            "publicly disclosed before appointment; members with material conflicts "
            "of interest must recuse from decisions where those conflicts are relevant. "
            "No executive direction, appropriations rider, or administrative action "
            "may weaken AI oversight without a full public rulemaking process. Oversight "
            "body independence must be structurally protected from political appointment "
            "pressure."
        ),
        "notes": (
            "Adversarial review: COI disclosure requirements without recusal mandates "
            "are ineffective. 'Material conflicts' must be broadly defined to include "
            "prior employment, stock holdings, advisory board memberships, and spousal "
            "financial interests. Structural protection from political appointment "
            "pressure requires specific procedural rules — general independence language "
            "is insufficient."
        ),
    },
    "AINL-0031": {
        "stmt": (
            "Any AI system replacing or substantially modifying an existing clinical "
            "or administrative workflow must include a documented rollback plan that "
            "allows rapid reversion to the prior workflow in the event of system "
            "failure, safety concern, or adverse outcome pattern. A workforce impact "
            "assessment must be conducted before deployment of AI systems that reduce "
            "clinical staffing. No AI deployment may reduce clinical staffing capacity "
            "below the minimum required to maintain safe patient care independently "
            "of AI function."
        ),
        "notes": (
            "Adversarial review: Rollback plans that exist on paper but depend on "
            "eliminated workforce capacity are not functional rollback plans; the rule "
            "must require that rollback capability be maintained alongside AI deployment. "
            "Workforce impact assessments conducted by the deploying entity are subject "
            "to obvious bias; independent assessment may be required for large-scale "
            "deployments."
        ),
    },
    "AINL-0032": {
        "stmt": (
            "AI systems used in healthcare must use open interoperability standards "
            "that enable patient data portability across systems and providers. "
            "Proprietary data formats that create vendor lock-in at the expense of "
            "care continuity are prohibited. Patients have the right to their health "
            "data in a standard, portable format upon request. No vendor may impose "
            "technical barriers to data portability that effectively prevent patients "
            "from changing providers."
        ),
        "notes": (
            "Adversarial review: 'Open interoperability standards' may be technically "
            "complied with while maintaining practical barriers through interface design, "
            "data export fees, or complexity. Enforcement must include testing of "
            "actual portability, not just standards compliance declarations. 'Upon "
            "request' should include a maximum response timeline of 30 days."
        ),
    },

    # ── APLS (SHORT-STMT, 4 cards) ───────────────────────────────────────────
    "APLS-0001": {
        "stmt": (
            "The independent reviewer in an insurance appeal must not be employed by, "
            "contracted to, or financially dependent on the entity making the adverse "
            "decision, nor may the reviewer have been employed by the entity within the "
            "prior five years. The reviewer must hold credentials in the specialty "
            "relevant to the requested care. Appeal processes may not be designed in "
            "ways that are deliberately complex, opaque, or time-consuming as a strategy "
            "to discourage appeals.<sup><a href=\"#fn7\">[7]</a></sup>"
        ),
        "notes": (
            "Adversarial review: Five-year cooling-off period for prior employment may "
            "be insufficient given tight specialty communities; revolving-door "
            "relationships persist beyond formal employment. 'Deliberately complex' "
            "processes are difficult to prove — design standards specifying maximum "
            "steps, maximum required documentation, and maximum form length may be "
            "more enforceable than intent-based prohibitions."
        ),
    },
    "APLS-0002": {
        "stmt": (
            "Standard appeal timelines must not exceed 30 days from submission. Urgent "
            "appeals — where delay would cause irreversible clinical harm — must be "
            "decided within 72 hours. Where the risk of irreversible harm is high, "
            "the urgent timeline is reduced to 24 hours. Coverage of the disputed "
            "service must be maintained pending appeal resolution unless the entity "
            "demonstrates a clear basis for termination that is independent of the "
            "appeal. Entities must staff appeals departments to meet required timelines."
        ),
        "notes": (
            "Adversarial review: 'Irreversible clinical harm' determinations are often "
            "contested between the patient's physician and the insurer's medical director — "
            "the rule must establish that the treating physician's assessment triggers "
            "expedited review. Coverage maintenance pending appeal may be rendered "
            "meaningless by billing practices that charge patients during the appeal "
            "period and require reimbursement after — this must be explicitly prohibited."
        ),
    },
    "APLS-0003": {
        "stmt": (
            "External reviewers must have no financial relationship with the health plan "
            "under review. Prior ruling patterns of external reviewers must be tracked "
            "and disclosed — external reviewers who systematically affirm insurer denials "
            "at rates inconsistent with peer reviewers must be removed from approved "
            "reviewer pools. External review decisions are binding on the insurer. "
            "Patients may request external review without first exhausting internal "
            "appeal processes in urgent cases."
        ),
        "notes": (
            "Adversarial review: External reviewer pools controlled by insurers through "
            "preferred-vendor arrangements are a well-documented abuse path — mandatory "
            "random assignment from a publicly maintained approved list is preferable "
            "to allowing insurer selection. Prior ruling pattern disclosure must be "
            "public, not just available to regulators, to enable independent oversight."
        ),
    },
    "APLS-0004": {
        "stmt": (
            "Any health plan or insurer whose denial rate on appeal reversal exceeds "
            "30% in a given year must submit a corrective action plan within 90 days "
            "identifying systemic causes and remediation measures. The corrective action "
            "plan must include restitution to all patients who were affected by the "
            "identified systemic issues — not only those who appealed. Annual denial "
            "pattern data must be published by each entity in a standardized, "
            "publicly accessible format."
        ),
        "notes": (
            "Adversarial review: A 30% reversal rate threshold may be too high; many "
            "denial patterns remain below this threshold while still representing "
            "systematic harm. Restitution to all affected patients requires the entity "
            "to identify non-appellants who were denied care — this requires proactive "
            "case review, not just passive response to filed appeals. Non-appellant "
            "identification creates strong incentives to hide systemic patterns; "
            "independent audit authority is necessary."
        ),
    },

    # ── CLMS (COMPLETE-STMT) ─────────────────────────────────────────────────
    "CLMS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Coverage defined in anticipation of climate-related "
            "health events must account for surge capacity demands that overwhelm "
            "standard networks during disasters; network adequacy rules must include "
            "emergency surge protocols. Prevention and adaptation measures that fall "
            "outside traditional healthcare coverage scope (e.g., heat-island mitigation, "
            "air quality infrastructure) require separate policy authority. Mental health "
            "diagnostic categories for climate-related distress (e.g., eco-anxiety) "
            "are evolving and must not be locked into coverage definitions that cannot "
            "adapt to clinical consensus updates."
        ),
    },

    # ── COVR (NO-STMT: 0001-0003) ─────────────────────────────────────────────
    "COVR-0001": {
        "stmt": (
            "Healthcare coverage may not be structured in multiple tiers that provide "
            "materially different access, quality, or scope of services based on ability "
            "to pay beyond standard cost-sharing. A two-tiered system in which higher "
            "premiums or out-of-pocket payments unlock meaningfully better care is "
            "incompatible with healthcare as a universal right. All covered persons "
            "are entitled to the same standard of medically necessary care.<sup><a href=\"#fn1\">[1]</a></sup>"
        ),
        "notes": (
            "Adversarial review: 'Materially different access' must be defined in "
            "regulation to prevent nominally equal plans with practically unequal "
            "networks, formularies, or prior authorization burdens. Concierge medicine "
            "arrangements that exist outside the public system may be a permitted "
            "private-market activity but must not be permitted to capture public "
            "healthcare resources or provider time in ways that degrade the public system."
        ),
    },
    "COVR-0002": {
        "stmt": (
            "The universal healthcare system is structured as a single, publicly "
            "administered plan open to all eligible persons. Multiple competing "
            "public plans that fragment the risk pool and administrative overhead "
            "are inconsistent with the efficiency and equity goals of universal "
            "coverage. Private insurance plans that duplicate public coverage are "
            "not permitted to operate as primary coverage within the universal "
            "system."
        ),
        "notes": (
            "Adversarial review: 'Single plan' requirements face significant "
            "political and legal challenges — the rule must be designed to survive "
            "constitutional challenges related to takings and due process. "
            "Supplemental private insurance for services explicitly excluded from "
            "the universal plan (e.g., cosmetic procedures) may be permitted as "
            "a policy design choice without compromising the single-plan structure "
            "for covered services. Transition provisions must address disruption "
            "to existing employer-sponsored coverage."
        ),
    },
    "COVR-0003": {
        "stmt": (
            "The universal healthcare system is financed and administered through a "
            "single public payer — a federal agency or federally chartered entity — "
            "that negotiates rates with providers, processes claims, and manages "
            "the universal benefit package. Private insurance companies may not "
            "serve as intermediary administrators of the universal public benefit. "
            "The public payer has statutory authority to negotiate drug prices and "
            "provider rates.<sup><a href=\"#fn9\">[9]</a></sup>"
        ),
        "notes": (
            "Adversarial review: Administrative cost savings from single payer depend "
            "on actually eliminating private plan administration overhead, not "
            "converting private payers into public contractors. Provider rate "
            "negotiation authority without rate floors may depress provider supply "
            "in underserved areas; rate-setting must include geographic and specialty "
            "adjustments. The rule must explicitly address the existing Medicare "
            "Advantage and managed Medicaid models as inconsistent with a true "
            "single-payer structure."
        ),
    },

    # ── COVR (SHORT-STMT: 0004-0030) ─────────────────────────────────────────
    "COVR-0004": {
        "stmt": (
            "Coverage under the universal public plan must be comprehensive, including "
            "at minimum: primary and preventive care, emergency care, specialist care, "
            "inpatient and outpatient hospital care, prescription drugs, mental health "
            "and substance use treatment, dental care, vision care, physical and "
            "occupational therapy, maternity and newborn care, pediatric care, long-term "
            "care, and medically necessary home health and hospice services. No service "
            "category that constitutes medically necessary care may be permanently "
            "excluded from coverage."
        ),
        "notes": (
            "Adversarial review: 'Medically necessary' is subject to definitional "
            "manipulation; the rule must specify that necessity determinations are "
            "made by treating clinicians, not by insurers applying internal guidelines "
            "that deviate from clinical consensus. Long-term care coverage is "
            "particularly subject to cost-containment exclusions; explicit inclusion "
            "is important. Dental and vision coverage are commonly excluded even in "
            "public plans — explicit enumeration prevents exclusion by omission."
        ),
    },
    "COVR-0005": {
        "stmt": (
            "All medically necessary prescription drugs approved by the FDA are covered "
            "under the universal plan. Formulary restrictions may be applied for cost "
            "management, but every formulary restriction must be paired with a fast, "
            "accessible exception pathway for patients whose medical needs deviate from "
            "the formulary preference. No formulary may operate as a de facto denial "
            "system for classes of medically necessary drugs. The universal plan has "
            "authority to negotiate drug prices directly with manufacturers.<sup><a href=\"#fn5\">[5]</a></sup>"
        ),
        "notes": (
            "Adversarial review: Formulary exception pathways exist on paper in most "
            "systems but are bureaucratically inaccessible in practice; the rule "
            "must define maximum timelines and documentation requirements. Price "
            "negotiation authority without a credible 'walk away' option is "
            "ineffective — the rule must include authority to import or manufacture "
            "drugs as leverage."
        ),
    },
    "COVR-0006": {
        "stmt": (
            "Mental health and substance use disorder treatment is covered on parity "
            "with medical and surgical coverage. Parity is assessed at the level of "
            "treatment limitations, prior authorization burdens, network adequacy, "
            "and reimbursement rates — not merely nominal plan language. Any treatment "
            "limitation applied to mental health or substance use care that is more "
            "restrictive than those applied to medical-surgical care of equivalent "
            "severity is a parity violation subject to enforcement and "
            "remediation.<sup><a href=\"#fn3\">[3]</a></sup>"
        ),
        "notes": (
            "Adversarial review: Mental health parity enforcement has failed largely "
            "because of the 'comparative analysis' standard's complexity — plans "
            "comply in ways that are technically defensible but functionally "
            "non-equivalent. Network adequacy disparities between mental health and "
            "medical panels are one of the most persistent parity violations; "
            "specific network ratio requirements are necessary."
        ),
    },
    "COVR-0007": {
        "stmt": (
            "All reproductive healthcare services, including contraception, prenatal "
            "care, abortion care, fertility treatments, and miscarriage management, "
            "are covered healthcare services. Coverage of reproductive care may not "
            "be conditioned, restricted, or denied based on political, religious, or "
            "ideological objections by payers or plan administrators. Conscientious "
            "objection by individual providers is subject to existing legal frameworks "
            "but may not be used by entities to wholesale deny coverage."
        ),
        "notes": (
            "Adversarial review: State-level abortion restrictions create direct "
            "conflicts with a federal coverage mandate; the rule must address "
            "the supremacy question explicitly. Employer and insurer religious "
            "exemption claims have been upheld by courts in ways that could "
            "undermine this provision; constitutional grounding is essential. "
            "Coverage mandates do not guarantee provider availability — network "
            "adequacy rules must specifically address reproductive care access "
            "in restrictive jurisdictions."
        ),
    },
    "COVR-0008": {
        "stmt": (
            "Gender-affirming care, including medically necessary hormone therapy, "
            "surgical interventions, and mental health support, is covered healthcare. "
            "Coverage may not be denied on the basis that the care is elective, "
            "cosmetic, or experimental where clinical guidelines support the medical "
            "necessity of the treatment. Coverage determinations for gender-affirming "
            "care are made by the treating clinician in consultation with the patient "
            "using accepted clinical standards."
        ),
        "notes": (
            "Adversarial review: 'Experimental' classifications are a primary tool "
            "used to deny gender-affirming care; the rule must specify that clinical "
            "consensus from major medical associations (AMA, WPATH, Endocrine Society) "
            "constitutes sufficient evidence of non-experimental status. Age-based "
            "restrictions on gender-affirming care for minors must be addressed "
            "through a separate, clinically grounded framework rather than a blanket "
            "age cutoff."
        ),
    },
    "COVR-0009": {
        "stmt": (
            "Preventive care services recommended by the U.S. Preventive Services Task "
            "Force at grade A or B, Advisory Committee on Immunization Practices "
            "vaccines, and preventive services with Health Resources and Services "
            "Administration guidelines for women and children are covered at zero "
            "cost to the patient — no deductible, no co-payment, no co-insurance. "
            "Changes to covered preventive services must go through a public "
            "rulemaking process and may not be implemented by administrative action alone."
        ),
        "notes": (
            "Adversarial review: Recent litigation has successfully challenged the "
            "constitutional basis for USPSTF-based coverage mandates; the rule must "
            "be structured on a statutory basis that survives constitutional challenge. "
            "Preventive service coverage mandates that exclude evidence-based services "
            "for LGBTQ+ patients (e.g., PrEP for HIV prevention) are discriminatory "
            "and must be explicitly included."
        ),
    },
    "COVR-0010": {
        "stmt": (
            "Chronic disease management — including long-term prescriptions, monitoring, "
            "and care coordination — is covered without cost barriers that create "
            "financial incentives to discontinue treatment. Cost-sharing for chronic "
            "condition management must be set at levels that do not result in measurable "
            "rates of treatment discontinuation attributable to cost. Annual review of "
            "chronic condition cost-sharing must assess and address evidence of "
            "cost-driven treatment gaps."
        ),
        "notes": (
            "Adversarial review: Chronic disease cost-sharing that appears low in "
            "isolation becomes prohibitive in aggregate for patients managing multiple "
            "conditions; total annual out-of-pocket burdens per condition must be "
            "assessed collectively, not individually. 'Measurable rates of treatment "
            "discontinuation' requires a surveillance mechanism — this must be "
            "built into the benefit management system."
        ),
    },
    "COVR-0011": {
        "stmt": (
            "Medically necessary dental care — including diagnostic, preventive, "
            "restorative, endodontic, periodontic, prosthodontic, and oral surgical "
            "services — is covered under the universal plan. 'Medically necessary' "
            "dental care includes any oral health condition that causes pain, "
            "functional limitation, systemic health risk, or reduces quality of life. "
            "Dental coverage may not be structured as a separate limited benefit with "
            "annual dollar caps that effectively exclude major restorative or "
            "surgical care."
        ),
        "notes": (
            "Adversarial review: Dental annual cap structures (e.g., $1,500–$2,000 "
            "annual limits) are deliberately designed to exclude major restorative work "
            "that costs multiples of the cap; this rule explicitly prohibits the cap "
            "structure. 'Medically necessary' dental definitions vary widely — the "
            "rule should reference existing CMS and professional society definitions "
            "to reduce evasion through redefinition."
        ),
    },
    "COVR-0012": {
        "stmt": (
            "Medically necessary vision care — including diagnostic examinations, "
            "corrective lenses, low-vision devices, and treatment for conditions of "
            "the eye — is covered under the universal plan. Coverage includes "
            "conditions causing visual impairment, including age-related macular "
            "degeneration, diabetic retinopathy, glaucoma, and cataracts. Routine "
            "refractive correction (glasses and contact lenses) is covered for "
            "children and for adults with documented visual impairment meeting "
            "defined thresholds."
        ),
        "notes": (
            "Adversarial review: 'Medically necessary' vision coverage that excludes "
            "routine refractive correction for adults leaves the most common vision "
            "need unaddressed; the rule includes a functional threshold for adult "
            "coverage. Vision care coverage for diabetic retinopathy and other "
            "systemic-disease-related eye conditions must be coordinated with "
            "chronic disease management to avoid coverage gaps at the "
            "medical-vision boundary."
        ),
    },
    "COVR-0013": {
        "stmt": (
            "Physical therapy, occupational therapy, speech therapy, and other "
            "medically necessary rehabilitative services are covered without arbitrary "
            "session limits. Session limits, where used for care management purposes, "
            "must be based on clinical evidence of typical recovery and be subject "
            "to clinician-initiated extension without prior authorization burden for "
            "conditions that require ongoing therapy. Therapy for chronic conditions "
            "is covered as long-term care, not as acute rehabilitation."
        ),
        "notes": (
            "Adversarial review: Arbitrary visit limits (e.g., 20 PT sessions per year) "
            "are inconsistent with evidence-based rehabilitation for many conditions "
            "and function as de facto coverage denials for chronic-condition patients. "
            "Prior authorization for visit extensions creates clinical burden that "
            "drives premature discharge — the rule must specify that clinician "
            "certification of ongoing medical necessity without PA requirement is "
            "sufficient for extension."
        ),
    },
    "COVR-0014": {
        "stmt": (
            "Medically necessary long-term care — including home health services, "
            "skilled nursing facility care, and community-based long-term care "
            "services — is covered under the universal plan. Coverage may not be "
            "conditioned on prior hospitalization or require exhaustion of personal "
            "assets. Long-term care coverage must be designed to support community "
            "living as the preferred setting over institutional care, consistent "
            "with the Americans with Disabilities Act integration mandate."
        ),
        "notes": (
            "Adversarial review: Long-term care coverage without supply-side investment "
            "in community care infrastructure results in coverage on paper but no "
            "available services in practice. ADA integration mandate requirements "
            "exist in federal law but are chronically underfunded and underenforced; "
            "coverage provisions must be paired with adequacy standards."
        ),
    },
    "COVR-0015": {
        "stmt": (
            "Palliative care and hospice services are covered as standard components "
            "of care for all conditions, not only terminal diagnoses. Palliative care "
            "may be provided concurrently with curative treatment. Coverage decisions "
            "for palliative care may not require prognosis of death within a defined "
            "period as a prerequisite. Patients choosing hospice care retain the right "
            "to return to curative treatment without coverage penalty."
        ),
        "notes": (
            "Adversarial review: Concurrent palliative/curative care coverage is the "
            "clinical standard but is frequently denied by payers who treat hospice as "
            "a terminal-only benefit. The right to return to curative treatment from "
            "hospice must be accompanied by a provision allowing hospice re-enrollment "
            "without penalty — the current Medicare hospice model creates a coverage "
            "cliff that deters appropriate hospice use."
        ),
    },
    "COVR-0016": {
        "stmt": (
            "Coverage under the universal plan is mandatory and universal — no person "
            "eligible under ACCS-0001 may be excluded from coverage based on "
            "pre-existing health conditions, prior healthcare utilization, genetic "
            "information, disability status, age, or any health status factor. "
            "Community rating applies to the universal plan; experience rating by "
            "health status is prohibited. Premium contributions, where collected, "
            "are based on income, not on health risk."
        ),
        "notes": (
            "Adversarial review: Community rating requirements in the ACA have been "
            "circumvented through short-term plan exemptions, association health plans, "
            "and other workarounds that must be explicitly closed. Age bands that "
            "increase premiums for older enrollees (permitted under ACA) are "
            "inconsistent with income-only contribution structures and must be "
            "addressed explicitly."
        ),
    },
    "COVR-0017": {
        "stmt": (
            "The denial of a coverage claim is permitted only on the basis of: "
            "(a) a specific, documented finding by a licensed clinician that the "
            "requested service is not medically necessary for this patient; or "
            "(b) a finding that the requested service falls outside the defined "
            "benefit package and no exception applies. Denials based on administrative "
            "errors, incomplete documentation, or procedural grounds that do not "
            "reflect a clinical necessity determination are void. Denials must provide "
            "the patient with a specific, actionable basis for appeal.<sup><a href=\"#fn7\">[7]</a></sup>"
        ),
        "notes": (
            "Adversarial review: 'Specific, documented finding' requirements are "
            "routinely evaded with standardized denial letters that state generic "
            "clinical rationale not specific to the patient. Voiding administrative "
            "denials creates an incentive to reframe administrative denials as "
            "clinical necessity denials; enforcement must track patterns across "
            "denial categories."
        ),
    },
    "COVR-0018": {
        "stmt": (
            "Prior authorization may only be required for services that have been "
            "identified through a documented, evidence-based process as having a "
            "meaningful rate of inappropriate use that prior authorization effectively "
            "reduces. Prior authorization requirements must be reviewed annually and "
            "removed where evidence no longer supports their use. Prior authorization "
            "may not be applied to emergency services, established chronic condition "
            "medications, or follow-up care for conditions with an existing, active "
            "treatment plan."
        ),
        "notes": (
            "Adversarial review: 'Evidence-based' PA requirements are currently a "
            "standard for inclusion rather than a standard for limiting PA; the rule "
            "must invert the default — PA requires affirmative justification, not "
            "just the absence of objection. Annual review requirements without "
            "mandatory removal of unjustified PA requirements are ineffective; "
            "the rule must specify that review results in binding removal, not "
            "merely optional reconsideration."
        ),
    },
    "COVR-0019": {
        "stmt": (
            "No claim may be denied solely on the basis of a missing or incorrect "
            "billing code, administrative error, or procedural technicality unrelated "
            "to the clinical question of whether the care was medically necessary "
            "and covered. Payers must identify and request any missing information "
            "within a defined period; denials for missing information may not be "
            "issued before the information request window closes. The burden of "
            "identifying billing errors rests with the payer, not the provider "
            "or patient."
        ),
        "notes": (
            "Adversarial review: Shifting the burden of identifying billing errors "
            "to the payer is a structural change from current practice and requires "
            "payer system investment; phase-in timelines must not be so long as "
            "to render the requirement illusory. 'Information request window' must "
            "have a defined maximum length to prevent indefinite claim suspension."
        ),
    },
    "COVR-0020": {
        "stmt": (
            "Coverage networks must be maintained at levels that ensure all covered "
            "services are accessible within time and distance standards appropriate "
            "to the urgency and frequency of the service. Specialty care networks "
            "must include sufficient providers to ensure appointments within 30 days "
            "for non-urgent specialist consultations. Primary care networks must "
            "ensure appointments within 10 days for non-urgent care. Mental health "
            "networks must meet the same standards as physical health networks for "
            "equivalent services."
        ),
        "notes": (
            "Adversarial review: Time-and-distance standards that measure straight-line "
            "distance rather than actual travel time systematically understate access "
            "barriers for rural and transit-dependent populations. 30-day appointment "
            "standards may be technically met by listing providers who are not "
            "accepting new patients — a phantom network problem requiring active "
            "verification of availability."
        ),
    },
    "COVR-0021": {
        "stmt": (
            "Balance billing — the practice of billing a patient for the difference "
            "between a provider's charge and the payer's allowed amount — is prohibited "
            "in all settings for all covered services. Patients may not be billed for "
            "any amount beyond standard cost-sharing for covered services. Providers "
            "who participate in the universal plan are prohibited from billing patients "
            "separately for covered services, including facility fees and professional "
            "fees that arise from a single covered encounter."
        ),
        "notes": (
            "Adversarial review: Balance billing prohibition must explicitly cover "
            "facility fees, which are a major source of surprise billing and are often "
            "treated as separate from professional billing. 'Participating in the "
            "universal plan' must be defined to prevent providers from opting out of "
            "participation solely to retain balance billing rights for high-cost services "
            "while retaining participation for routine care."
        ),
    },
    "COVR-0022": {
        "stmt": (
            "Annual out-of-pocket limits for covered services must be set at levels "
            "that do not impose financial catastrophe on households with median or "
            "below-median incomes. Income-scaled out-of-pocket maximum structures "
            "must be implemented so that cost-sharing obligations are proportional "
            "to ability to pay. The annual review of out-of-pocket limits must "
            "assess and address evidence of cost-driven treatment gaps, medical "
            "debt, and bankruptcy attributable to healthcare costs."
        ),
        "notes": (
            "Adversarial review: Income-scaled OOP structures require income "
            "verification systems that may create administrative barriers to care "
            "for people with irregular or seasonal incomes; prospective income "
            "estimates with reconciliation at year-end (as in ACA premium tax "
            "credits) may be the appropriate model. Medical debt is a predictable "
            "outcome of any system with OOP maximums that are not income-scaled; "
            "the review requirement must be linked to hard corrective action "
            "timelines."
        ),
    },
    "COVR-0023": {
        "stmt": (
            "Coverage for prescription drugs includes a zero-cost-sharing tier for "
            "medications indicated for chronic conditions, life-threatening conditions, "
            "and mental health conditions. Cost-sharing for prescription drugs in all "
            "tiers must be capped at levels that do not result in measurable rates of "
            "non-adherence attributable to cost. Monthly out-of-pocket limits for "
            "prescription drugs apply independently of the general annual limit "
            "to prevent cost spikes in high-medication-burden months."
        ),
        "notes": (
            "Adversarial review: Zero-cost-sharing tiers for chronic condition drugs "
            "require formulary coverage of those drugs — if the drug is on a "
            "restricted formulary tier, zero cost-sharing is meaningless. Monthly "
            "OOP limits for drugs are more protective than annual limits in practice "
            "for patients who experience cost-related non-adherence within a "
            "single month; this provision is intentionally structured on a monthly basis."
        ),
    },
    "COVR-0024": {
        "stmt": (
            "Any person whose coverage is terminated, reduced, or modified has the "
            "right to advance notice no less than 30 days before the effective date, "
            "a plain-language explanation of the reason, and an uninterrupted right "
            "to appeal before the change takes effect. Emergency termination — where "
            "notice is not practicable — may occur only in defined circumstances "
            "involving active fraud, and must be followed by a retroactive notice "
            "and appeal opportunity within 10 business days."
        ),
        "notes": (
            "Adversarial review: 30-day advance notice requirements may conflict "
            "with legitimate plan-level coverage restructuring on renewal cycles; "
            "the rule must address how to handle system-level coverage changes that "
            "affect large groups simultaneously. 'Emergency termination for active "
            "fraud' is a narrow exception that must be carefully defined to prevent "
            "expansion to cover administrative convenience terminations."
        ),
    },
    "COVR-0025": {
        "stmt": (
            "Any payer or plan that operates within the universal healthcare system "
            "must maintain claims processing standards that result in payment or "
            "denial of clean claims within 30 days of receipt. Interest must accrue "
            "on unpaid clean claims after 30 days. Claims for emergency services "
            "must be processed within 15 days. Systemic claims processing delays "
            "that function as de facto denials are subject to the same enforcement "
            "as explicit denials."
        ),
        "notes": (
            "Adversarial review: 'Clean claim' standards are sometimes defined "
            "narrowly so that most submitted claims are deemed unclean and subject "
            "to extended processing; the rule must set a minimum standard for "
            "what constitutes a clean claim and limit 'unclean' designations to "
            "specific, enumerated missing elements. Interest accrual must be "
            "automatic, not subject to per-claim legal action."
        ),
    },
    "COVR-0026": {
        "stmt": (
            "Coverage may not be terminated, reduced, or restricted as a direct or "
            "indirect result of a patient's healthcare utilization, diagnosis, or "
            "treatment history. Post-enrollment experience rating by health status "
            "is prohibited. High-utilization patients who require expensive care "
            "may not be targeted for plan design changes, formulary restrictions, "
            "or network modifications that effectively reduce their coverage relative "
            "to lower-utilization patients."
        ),
        "notes": (
            "Adversarial review: Experience rating prohibition must explicitly address "
            "indirect forms: plans that implement formulary changes shortly after "
            "a high-cost drug becomes widely prescribed, or networks that drop "
            "high-utilization specialists, may be implementing de facto experience "
            "rating without explicit premium increases. Enforcement must include "
            "actuarial analysis of plan changes alongside stated justifications."
        ),
    },
    "COVR-0027": {
        "stmt": (
            "The universal benefit package is reviewed annually by an independent "
            "body with clinical, patient, and public health representation. Updates "
            "to the benefit package based on new evidence are incorporated through "
            "a public rulemaking process. Coverage decisions must be transparently "
            "justified with evidence and may be appealed by patient advocacy organizations. "
            "No benefit may be removed or restricted without a documented evidence "
            "basis and a public comment period of no less than 60 days."
        ),
        "notes": (
            "Adversarial review: 'Independent body' composition must include conflict "
            "of interest requirements; industry representatives on benefit review "
            "committees have systematically influenced coverage decisions in existing "
            "public programs. 60-day comment periods may be insufficient for complex "
            "coverage changes affecting rare-disease patients who require time to "
            "organize; 90-day minimum for major benefit changes should be considered."
        ),
    },
    "COVR-0028": {
        "stmt": (
            "Covered persons have the right to access second opinions for any "
            "diagnosis or treatment recommendation without prior authorization, "
            "at standard cost-sharing rates. Payers may not discourage second "
            "opinions through differential cost-sharing, requirement of referral, "
            "or network restrictions that make second opinions from qualified "
            "specialists unavailable. Where the treating clinician and the second "
            "opinion clinician disagree on treatment, the covered person has the "
            "right to choose between the recommended treatment options."
        ),
        "notes": (
            "Adversarial review: Second opinion rights are most valuable in situations "
            "where the first opinion is associated with a high-cost or high-risk "
            "treatment — exactly the situation where payers have the greatest interest "
            "in directing patient choices. The right to choose between disagreeing "
            "clinical opinions must not become a coverage dispute mechanism; "
            "both recommended options must be covered."
        ),
    },
    "COVR-0029": {
        "stmt": (
            "No covered person may be financially penalized for seeking care outside "
            "a preferred network when: (a) the needed service is not available within "
            "the network within clinically appropriate time and distance standards; "
            "(b) the treating clinician and patient determine that continuity of care "
            "with an existing outside-network provider is medically necessary; or "
            "(c) the care is emergency care. In these circumstances, out-of-network "
            "care is covered at in-network cost-sharing rates."
        ),
        "notes": (
            "Adversarial review: Continuity of care provisions are routinely denied "
            "when networks change at plan renewal; the rule must explicitly address "
            "plan renewal as a covered continuity event. 'Clinically appropriate "
            "time and distance standards' must be defined in regulation to prevent "
            "payers from setting standards that nominally justify network-only care "
            "despite practical inaccessibility."
        ),
    },
    "COVR-0030": {
        "stmt": (
            "Nutrition counseling, medically supervised weight management programs, "
            "and obesity treatment — including pharmacotherapy and bariatric surgery "
            "when clinically indicated — are covered as medically necessary care. "
            "Coverage determinations for obesity treatment are made on clinical "
            "necessity criteria and may not be denied on the basis that obesity is "
            "a lifestyle condition. Coverage includes treatment of obesity-related "
            "comorbidities as an integrated care pathway."
        ),
        "notes": (
            "Adversarial review: GLP-1 agonist coverage for obesity treatment is "
            "a rapidly evolving area where cost-containment pressures are creating "
            "new prior authorization burdens and exclusions; the rule must not be "
            "written in drug-specific language that becomes outdated. 'Clinically "
            "indicated' criteria for bariatric surgery have been used to impose "
            "lengthy, burdensome qualification periods that delay care — these must "
            "be specifically addressed."
        ),
    },

    # ── COVR (COMPLETE-STMT: 0031-0036) ──────────────────────────────────────
    "COVR-0031": {
        "stmt": None,
        "notes": (
            "Adversarial review: Coverage of care for people experiencing homelessness "
            "must address the reality that traditional coverage mechanisms (enrollment, "
            "billing address, identification) frequently fail this population. "
            "Navigation and outreach services to connect unsheltered people to care "
            "must be covered as part of the benefit, not funded separately as a "
            "discretionary social service. Post-stabilization discharge planning "
            "must be covered; discharging unhoused patients back to the street "
            "after medical treatment without navigation services defeats the purpose "
            "of coverage."
        ),
    },
    "COVR-0032": {
        "stmt": None,
        "notes": (
            "Adversarial review: Disability care coverage must address the gap between "
            "acute care coverage (well-developed) and long-term supportive care "
            "coverage (severely underdeveloped). Assistive technology coverage must "
            "keep pace with technology development; outdated benefit definitions "
            "that cover basic wheelchairs but not power wheelchairs or communication "
            "devices must be updated through the annual benefit review process. "
            "Coverage must explicitly include community integration support services "
            "required by the Olmstead decision."
        ),
    },
    "COVR-0033": {
        "stmt": None,
        "notes": (
            "Adversarial review: Pediatric coverage must address the transition to "
            "adult care at 18 or 26 as a coverage gap risk point — transition planning "
            "must begin no later than age 14 for children with complex medical needs. "
            "Developmental and behavioral pediatric care coverage must not be limited "
            "to diagnostic services — treatment, therapy, and school-based support "
            "services must be included where they are medically necessary."
        ),
    },
    "COVR-0034": {
        "stmt": None,
        "notes": (
            "Adversarial review: Geriatric care coverage must specifically address "
            "the multi-specialty care coordination needs of older adults, which are "
            "poorly served by fragmented specialist coverage structures. Dementia "
            "care coverage must explicitly include caregiver support services; "
            "the burden on family caregivers of dementia patients represents a "
            "major coverage gap in existing public programs. Long-term care "
            "integration with the universal plan must not create a coverage "
            "cliff at the boundary with Medicare."
        ),
    },
    "COVR-0035": {
        "stmt": None,
        "notes": (
            "Adversarial review: Addiction treatment coverage must specifically include "
            "medication-assisted treatment (MAT) including buprenorphine, methadone, "
            "and naltrexone without prior authorization for patients with opioid use "
            "disorder; PA requirements for MAT are a leading cause of treatment delay "
            "and death. Coverage must include residential and intensive outpatient "
            "treatment at parity with other mental health services. Harm reduction "
            "services must be explicitly included."
        ),
    },
    "COVR-0036": {
        "stmt": None,
        "notes": (
            "Adversarial review: Coverage for functional health services — including "
            "nutrition, physical activity, sleep medicine, and integrative health — "
            "must be defined with reference to evidence standards to prevent inclusion "
            "of unproven interventions. Evidence thresholds for coverage must be "
            "applied consistently across conventional and integrative services — a "
            "stricter standard for integrative care than for conventional care "
            "is scientifically unjustified and may reflect bias rather than "
            "evidence-based coverage design."
        ),
    },

    # ── CRNS (COMPLETE-STMT) ──────────────────────────────────────────────────
    "CRNS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Long COVID classification as a chronic condition is "
            "contested in some clinical settings, leading to denial of coverage for "
            "ongoing treatment; the rule must specify that long COVID meets the "
            "definition of a chronic condition for coverage purposes regardless of "
            "diagnostic code availability. Relapsing-remitting chronic conditions "
            "create coverage gap risks when patients are 'stable' — coverage must "
            "not have a cliff at the point of clinical stability for conditions "
            "that are expected to relapse. Provider capacity for chronic disease "
            "management is a binding constraint on coverage effectiveness."
        ),
    },
    "CRNS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Permanent coverage for established chronic conditions "
            "must explicitly prohibit termination of coverage for the condition upon "
            "plan renewal, benefit restructuring, or formulary change. Return-to-work "
            "coercion — conditioning ongoing coverage on vocational rehabilitation "
            "participation or employment activity — must be explicitly prohibited. "
            "Assistive device lifecycle coverage must address replacement timelines "
            "that reflect actual device lifespan rather than overly conservative "
            "payer-set schedules that deny replacement before devices are functionally "
            "end-of-life."
        ),
    },

    # ── CSTS (SHORT-STMT, 4 cards) ────────────────────────────────────────────
    "CSTS-0001": {
        "stmt": (
            "Cost-sharing levels — including deductibles, co-payments, and co-insurance — "
            "must be set based on evidence that the level does not result in measurable "
            "rates of patients forgoing necessary care attributable to cost. The "
            "forgoing-care threshold must be calibrated to actual household financial "
            "circumstances at median and below-median incomes. Zero cost-sharing must "
            "apply to preventive services, chronic-condition monitoring, and services "
            "for conditions where cost-sharing-driven treatment gaps create "
            "downstream healthcare costs."
        ),
        "notes": (
            "Adversarial review: 'Forgoing-care threshold' calibration requires active "
            "surveillance of treatment patterns correlated with cost-sharing levels; "
            "this is a methodological challenge that must be addressed through a "
            "defined measurement methodology, not left to ad hoc review. Zero "
            "cost-sharing for chronic conditions must include medications, not "
            "just visits — pharmacy cost-sharing is often the primary barrier to "
            "adherence."
        ),
    },
    "CSTS-0002": {
        "stmt": (
            "Federal standards for deductibles and annual out-of-pocket maximums must "
            "be set as a percentage of household income to ensure that cost-sharing "
            "obligations are proportional to ability to pay. Income-scaled standards "
            "must apply to family-size adjusted household income. An annual review "
            "must assess evidence of cost-sharing-driven treatment gaps, medical "
            "debt, and financial hardship; findings must trigger mandatory adjustment "
            "of cost-sharing standards within 180 days."
        ),
        "notes": (
            "Adversarial review: Income scaling requires income verification that "
            "may create barriers for people with irregular incomes, self-employment "
            "income, or informal household arrangements; the rule must include "
            "prospective estimation with reconciliation mechanisms that don't "
            "create clawback risks that discourage enrollment. 180-day mandatory "
            "adjustment timelines may be too slow for people experiencing acute "
            "financial hardship from current cost-sharing levels."
        ),
    },
    "CSTS-0003": {
        "stmt": (
            "Health savings and spending tools — including health savings accounts, "
            "flexible spending accounts, and equivalent mechanisms — must be available "
            "to all plan participants regardless of plan type or deductible level. "
            "Tax treatment of these tools must be equitable across income levels; "
            "mechanisms that primarily benefit higher-income taxpayers due to "
            "marginal-rate advantages must be restructured as refundable credits "
            "or equivalent instruments that provide proportional benefit across "
            "income levels."
        ),
        "notes": (
            "Adversarial review: HSA tax advantages that are primarily valuable to "
            "high-income taxpayers are regressive; the equitable restructuring "
            "requirement may be controversial but is essential for fiscal consistency "
            "with the broader universal coverage structure. Tying HSA eligibility "
            "to HDHP enrollment — as under current law — creates a perverse incentive "
            "toward high-deductible plans that this policy is otherwise designed "
            "to eliminate; the rule must decouple HSA access from plan type."
        ),
    },
    "CSTS-0004": {
        "stmt": (
            "Zero or near-zero cost-sharing must apply at the point of care — without "
            "prior authorization — to: all USPSTF Grade A and B preventive services; "
            "medications for established chronic conditions on the recommended "
            "chronic disease drug list; and first-year mental health care to reduce "
            "the treatment initiation barrier. Application of zero cost-sharing must "
            "be automatic at the point of care and may not require patient pre-enrollment "
            "in a special program, pre-authorization, or income verification at the "
            "time of service."
        ),
        "notes": (
            "Adversarial review: 'Automatic at the point of care' application requires "
            "real-time eligibility and benefit verification systems that are not "
            "universally functional across provider settings; administrative "
            "infrastructure investment must accompany this requirement. First-year "
            "mental health zero cost-sharing must be carefully defined to prevent "
            "per-year gaming (e.g., plan resets that restart the first-year counter "
            "annually to avoid ongoing zero cost-sharing for established mental "
            "health treatment)."
        ),
    },

    # ── DISS (COMPLETE-STMT) ──────────────────────────────────────────────────
    "DISS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Subgroup representation minimums in clinical trials "
            "must be sufficient for statistical power to detect differential effects — "
            "token representation that cannot support subgroup analysis is not "
            "meaningful inclusion. Tribal sovereignty considerations require that "
            "tribal communities be treated as sovereign entities in research "
            "agreements, not merely as data sources; data ownership and benefit-sharing "
            "provisions must be negotiated with tribal governments. Intersectional "
            "representation (e.g., elderly Black women, disabled Native Americans) "
            "requires larger overall trial populations."
        ),
    },
    "DISS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Racial bias in clinical care research includes both "
            "explicit bias (racially adjusted clinical algorithms, e.g., race-based "
            "GFR calculations) and implicit bias in study design; the rule must "
            "address both. Uniform disparity measurement methodology must be "
            "legislatively defined rather than left to agency discretion to prevent "
            "weakening through regulatory capture. Geographic enforcement capacity "
            "in rural and tribal areas is a binding constraint on disparity reduction — "
            "data collection without enforcement infrastructure is insufficient."
        ),
    },
    "DISS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: SOGI data collection must address patient privacy "
            "concerns and the risk that data collected for research purposes becomes "
            "accessible to hostile actors; data security standards must accompany "
            "collection mandates. 'Intersectional disaggregation' requires sample "
            "sizes that most studies are not powered to achieve; dedicated funding "
            "for intersectional research is necessary. Protection from defunding "
            "must include language addressing executive-branch efforts to eliminate "
            "SOGI-related research through administrative action rather than "
            "through legislation."
        ),
    },
    "DISS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Tribal data sovereignty provisions must address "
            "the specific history of IHS data extraction without benefit-sharing; "
            "generic data sovereignty language may be insufficient without tribal "
            "consent requirements embedded in federal research grant conditions. "
            "IHS per-capita funding compared to other federal healthcare programs "
            "is documented at approximately 40% of per-prisoner healthcare spending; "
            "the disparity is a policy choice, not a technical limitation. Urban "
            "Native populations fall between IHS (reservation-focused) and "
            "general Medicaid coverage — a specific coverage gap that must be "
            "explicitly addressed."
        ),
    },
    "DISS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: 'Asian American' as a single research category "
            "obscures enormous heterogeneity — the health needs of South Asian, "
            "East Asian, and Southeast Asian populations differ substantially. "
            "Separate Pacific Islander data collection is essential because Pacific "
            "Islanders have historically been absorbed into Asian American categories "
            "in ways that mask their distinct health disparities and outcomes. "
            "Country-of-origin granularity for all racial/ethnic categories "
            "increases research value but also increases re-identification risk for "
            "small communities — data access and privacy protections must scale "
            "accordingly."
        ),
    },
    "DISS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Structural determinants research (housing, income, "
            "food security, environmental exposure) is systematically underfunded "
            "because it points toward solutions that are outside the healthcare "
            "sector's control and interest; cross-sector funding mechanisms are "
            "necessary. Causal inference methodology for structural determinants is "
            "technically challenging and requires methodological investment; "
            "observational association studies alone are insufficient to establish "
            "the evidence base for policy action. Solutions must address root causes, "
            "not just downstream health effects."
        ),
    },

    # ── DNTS (COMPLETE-STMT) ──────────────────────────────────────────────────
    "DNTS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Dental workforce shortage in underserved areas is "
            "a structural problem that cannot be solved by coverage expansion alone; "
            "dental school loan repayment programs, community health center expansion, "
            "and dental therapist scope-of-practice expansion are necessary complements. "
            "Dental-medical integration incentives must address billing and referral "
            "infrastructure that currently operates as separate systems. Network "
            "adequacy standards for dental coverage must reflect the geographic "
            "distribution of dental providers, which is more concentrated than "
            "primary care."
        ),
    },
    "DNTS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Vision coverage parity in cost-sharing must address "
            "the tendency to set vision benefit dollar limits at levels that cover "
            "routine refraction but not glasses or contacts; functional coverage "
            "requires explicit inclusion of corrective lenses. Low-vision and "
            "blindness conditions — including diabetic retinopathy, glaucoma, and "
            "macular degeneration — often require specialized rehabilitation services "
            "that fall in a coverage gap between medical and vision benefits; "
            "this gap must be explicitly closed. Pediatric screen exposure and "
            "myopia research must address not just treatment but prevention and "
            "the role of environmental factors."
        ),
    },

    # ── EMPS (SHORT-STMT, 4 cards) ────────────────────────────────────────────
    "EMPS-0001": {
        "stmt": (
            "Employer-sponsored health plans may not offer only high-deductible "
            "plans as the sole coverage option. At least one employer plan option "
            "must be available with a deductible not exceeding $1,000 for individuals "
            "or $2,500 for families, with zero cost-sharing for USPSTF preventive "
            "services. Employees have an accessible pathway to file complaints about "
            "plan offerings; anti-retaliation protections apply to employees who file "
            "complaints or inquire about plan quality. Small businesses receive "
            "federal subsidy support to offer qualifying plans."
        ),
        "notes": (
            "Adversarial review: Deductible limits that are not indexed to inflation "
            "will be eroded over time; the rule must include an indexing mechanism. "
            "Anti-retaliation protections require a private right of action and "
            "accessible enforcement mechanisms — ERISA preemption may limit state "
            "law remedies and must be addressed explicitly. Small business subsidy "
            "eligibility thresholds create anti-fragmentation concerns if businesses "
            "split to remain below thresholds."
        ),
    },
    "EMPS-0002": {
        "stmt": (
            "Employers required to provide health coverage must pay the full cost of "
            "coverage premiums, including dependent coverage, for all covered "
            "employees. Premium contribution obligations apply to all worker "
            "classifications — including part-time, temporary, seasonal, and "
            "contractual workers above a minimum hours threshold. Employers may not "
            "misclassify workers to avoid premium contribution obligations; "
            "worker classification for benefit purposes is independently determined "
            "and not solely controlled by employer designation."
        ),
        "notes": (
            "Adversarial review: Minimum hours thresholds for coverage eligibility "
            "create strong incentives to manage worker hours below the threshold; "
            "the rule must include anti-manipulation provisions and audit requirements "
            "for employers with high concentrations of workers near the threshold. "
            "Gig economy and platform workers are misclassified at scale; independent "
            "contractor status must not be an automatic exemption from coverage "
            "obligations."
        ),
    },
    "EMPS-0003": {
        "stmt": (
            "Federal subsidies, tax credits, and reinsurance mechanisms for employer "
            "health coverage must be automatically available to employers meeting "
            "size thresholds and coverage requirements, without requiring per-employer "
            "administrative applications. Anti-fragmentation rules prevent employers "
            "from artificially splitting entities to remain below eligibility thresholds. "
            "A three-year transition period with subsidy backstop support is provided "
            "for small employers transitioning to qualifying plan structures."
        ),
        "notes": (
            "Adversarial review: Automatic availability of subsidies requires a "
            "verification mechanism; automatic disbursement without verification "
            "creates fraud risk, while complex verification creates access barriers. "
            "Anti-fragmentation rules require corporate structure analysis that "
            "draws on tax and labor law concepts; coordination with IRS enforcement "
            "is necessary. Transition period subsidies must include hard end dates "
            "with no extension authority to prevent permanent subsidy dependency."
        ),
    },
    "EMPS-0004": {
        "stmt": (
            "Employer health plans must provide coverage sufficient to meet the "
            "federal definition of adequate coverage, anchored to the healthcare "
            "research standard for underinsurance: defined as coverage that leaves "
            "households exposed to out-of-pocket costs exceeding 10% of income (5% "
            "for low-income households). Plans that fail the adequacy standard must "
            "transition to qualifying plan structures within a defined period; "
            "a public option is available as a backstop for workers whose employer "
            "plans fail adequacy standards after the transition period."
        ),
        "notes": (
            "Adversarial review: Underinsurance definitions anchored to research "
            "standards provide clearer enforcement benchmarks than flexible 'minimum "
            "value' tests but require annual income data that may not be readily "
            "available to plan administrators at the time of enrollment; prospective "
            "estimation with reconciliation is the appropriate mechanism. Public "
            "option backstop availability is conditional on transition period "
            "enforcement — if employers are not held to compliance timelines, the "
            "public option becomes a permanent subsidy for inadequate employer plans."
        ),
    },

    # ── EMSS (NO-STMT) ────────────────────────────────────────────────────────
    "EMSS-0001": {
        "stmt": (
            "Emergency care is provided at zero cost at the point of care to all "
            "persons present in the United States, regardless of insurance status, "
            "citizenship, immigration status, or ability to pay. No emergency provider "
            "may bill patients directly for emergency services. Providers that deliver "
            "emergency care are reimbursed through the universal public payer system. "
            "The prohibition on patient billing applies to all components of emergency "
            "care — including facility fees, physician fees, ancillary services, "
            "and post-stabilization follow-up care. No medical debt may be incurred, "
            "collected, or reported to credit agencies based on emergency services "
            "delivered under this provision."
        ),
        "notes": (
            "Adversarial review: 'Post-stabilization follow-up care' inclusion is "
            "important but requires a clinical definition of when stabilization ends "
            "and elective care begins — the transition point has historically been "
            "a major billing abuse site. Debt collection prohibitions must include "
            "debt sold to third-party collectors, not only direct billing by the "
            "providing entity. Reimbursement to providers through the public payer "
            "must be set at levels that ensure emergency department capacity; "
            "underpayment of emergency providers is a supply-side risk."
        ),
    },
    "EMSS-0002": {
        "stmt": (
            "Emergency care coverage includes: emergency ambulance services (ground "
            "and air where medically necessary), emergency department evaluation "
            "and treatment, observation care, post-stabilization care during the "
            "same emergency episode, and follow-up care directly related to the "
            "emergency condition for a defined clinical period following the emergency "
            "episode. Emergency care may not be billed as non-emergency care solely "
            "because the patient's condition was subsequently determined to be "
            "non-life-threatening; the appropriateness of emergency care use is "
            "assessed at the time of presentation, not retrospectively."
        ),
        "notes": (
            "Adversarial review: Air ambulance billing has been a major source of "
            "emergency balance billing and debt; explicit inclusion with zero "
            "patient-billing must address the air ambulance industry's argument that "
            "they are outside EMTALA coverage. Retrospective 'prudent layperson' "
            "standard enforcement requires that insurers apply the standard from "
            "the patient's perspective at the time of presentation, not the insurer's "
            "retrospective clinical assessment — this must be explicitly required. "
            "Post-emergency follow-up coverage for 'the same emergency condition' "
            "must have a defined minimum period (e.g., 30 days) to prevent "
            "immediate cost-shifting."
        ),
    },

    # ── JUSS (COMPLETE-STMT) ──────────────────────────────────────────────────
    "JUSS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: 'Community standards of care' in correctional settings "
            "is routinely violated without consequence; this provision requires an "
            "independent monitoring mechanism with access authority and binding "
            "remediation power. Private corrections healthcare contractors have "
            "a structural incentive to minimize care costs at the expense of patient "
            "health; contract structures must include quality metrics with financial "
            "consequences. Using healthcare access as a disciplinary tool or "
            "coercive mechanism is documented; the prohibition must include specific "
            "enforcement and private right of action. Healthcare in detention — "
            "including ICE detention — must be explicitly included."
        ),
    },

    # ── MATS (COMPLETE-STMT) ──────────────────────────────────────────────────
    "MATS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Maternal mortality review committees require data "
            "access, investigative authority, and protection from political interference "
            "to function effectively — state-level review committees that answer "
            "to governors may face pressure to suppress findings. Race-disaggregated "
            "reporting must include analysis of systemic factors, not only individual "
            "clinical factors; reports that attribute Black maternal mortality to "
            "patient-level factors while ignoring provider implicit bias and systemic "
            "gaps are systematically misleading. Targeted interventions must include "
            "mandatory implicit bias training, structural quality improvement, and "
            "enforcement mechanisms — not only voluntary best-practice guides.<sup><a href=\"#fn6\">[6]</a></sup>"
        ),
    },
    "MATS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Doula and midwifery reimbursement rates must be set "
            "at levels that support sustainable practice in underserved communities; "
            "coverage that reimburses below cost is coverage in name only. Twelve "
            "months of postpartum coverage is a significant expansion from current "
            "standards and must be accompanied by provider capacity investment. "
            "Community health worker reimbursement limitations that exclude non-licensed "
            "workers are a specific barrier in high-mortality communities where "
            "community workers are the primary point of contact; the rule's explicit "
            "inclusion is intentional and should be preserved."
        ),
    },

    # ── MHCS (47 cards) ───────────────────────────────────────────────────────
    "MHCS-0001": {
        "stmt": (
            "Comprehensive mental health and substance use disorder care is a covered "
            "component of the universal healthcare benefit, with scope and terms "
            "equivalent to those for physical health conditions of comparable severity "
            "and complexity. Mental healthcare is not a supplemental or secondary "
            "benefit — it is a primary, integrated component of healthcare coverage "
            "subject to full parity in network adequacy, cost-sharing, prior "
            "authorization, and reimbursement rates. Exclusion of mental health "
            "conditions from coverage is prohibited.<sup><a href=\"#fn3\">[3]</a></sup>"
        ),
        "notes": (
            "Adversarial review: Parity in nominal plan terms is not parity in practice; "
            "enforcement must assess actual access metrics — wait times, provider "
            "availability, denial rates, out-of-network use rates — not only plan "
            "document language. Reimbursement rate disparities between mental health "
            "and medical providers drive provider participation differences that "
            "create de facto parity violations; rate parity must be explicitly required."
        ),
    },
    "MHCS-0002": {
        "stmt": (
            "AI systems used in mental health settings — including diagnostic tools, "
            "crisis screening systems, telehealth platforms, behavioral health case "
            "management, and consumer-facing mental wellness applications marketed "
            "as therapeutic — are regulated as high-risk AI systems. High-risk "
            "mental health AI is subject to pre-deployment registration, independent "
            "clinical validation, public disclosure of performance and bias metrics, "
            "mandatory adverse event reporting, and continuous post-deployment "
            "monitoring by a financially independent entity."
        ),
        "notes": (
            "Adversarial review: 'Consumer-facing mental wellness applications marketed "
            "as therapeutic' must be defined to include apps that make implicit or "
            "explicit claims about mental health benefit without being classified as "
            "medical devices — the FDA's enforcement of mental health app regulation "
            "has been inconsistent. Pre-deployment registration requirements must "
            "apply to updates and new versions, not just initial deployment; incremental "
            "updates can substantially change system behavior."
        ),
    },
    "MHCS-0003": {
        "stmt": (
            "AI systems may not replace licensed clinicians in mental health diagnosis, "
            "crisis assessment, involuntary treatment decisions, medication management, "
            "or any other high-risk clinical determination. For any clinical decision "
            "in a high-risk mental health context, a licensed clinician must independently "
            "evaluate the patient and document a clinical basis for their decision "
            "that is independent of any AI recommendation. AI-only clinical pathways "
            "in mental health are prohibited."
        ),
        "notes": (
            "Adversarial review: 'AI-only clinical pathways' prohibition must explicitly "
            "address systems that nominally include a clinician but are designed to "
            "minimize clinician involvement through workflow design, time pressure, "
            "or documentation structures. Involuntary treatment decisions (e.g., "
            "civil commitment) carry the highest stakes and must have the most "
            "robust human review requirements; AI inputs to these decisions require "
            "exceptional scrutiny."
        ),
    },
    "MHCS-0004": {
        "stmt": (
            "AI systems may not serve as the sole or primary decision-maker in "
            "suicide risk assessment, crisis intervention, emergency mental health "
            "response, or any decision that could result in involuntary detention "
            "or treatment. Human clinical review is mandatory for all decisions "
            "in these domains; AI-generated risk scores may inform but may not "
            "determine clinical response. The use of AI suicide risk scores to "
            "automatically generate alerts to law enforcement without human clinical "
            "review is prohibited."
        ),
        "notes": (
            "Adversarial review: AI suicide risk scores are deployed in school systems, "
            "EHRs, and crisis text platforms at scale; many of these deployments lack "
            "adequate human review infrastructure. Automated alerts to law enforcement "
            "based on AI risk scores — without clinician review — have resulted in "
            "documented harm to the patients they were intended to protect; the "
            "explicit prohibition is essential. 'Primary decision-maker' must be "
            "defined functionally: a system that generates a risk level that is then "
            "acted upon without independent assessment is the primary decision-maker."
        ),
    },
    "MHCS-0005": {
        "stmt": (
            "A clearly identifiable, licensed mental health professional must be "
            "accountable for all clinical decisions in high-risk mental health contexts "
            "where AI systems are used. The accountability chain may not be diffused "
            "across the AI vendor, the platform operator, and the healthcare entity "
            "in ways that result in no specific person bearing clinical responsibility. "
            "AI systems that recommend a clinical action must identify by name the "
            "licensed professional who reviewed and acted on the recommendation."
        ),
        "notes": (
            "Adversarial review: Diffusion of accountability is a predictable response "
            "to liability — vendors, platforms, and healthcare entities will each argue "
            "the other bears responsibility. The named-professional requirement creates "
            "a concrete accountability mechanism; it must be paired with documentation "
            "requirements that create an enforceable audit trail."
        ),
    },
    "MHCS-0006": {
        "stmt": (
            "AI may be used as an assistive tool in mental health care in contexts "
            "where it supports, supplements, or improves clinical workflows without "
            "substituting for the clinician-patient therapeutic relationship or "
            "clinical judgment. AI tools that assist with documentation, scheduling, "
            "or administrative tasks are lower-risk. AI tools that interact directly "
            "with patients in therapeutic or supportive roles require the highest "
            "level of oversight and are subject to additional restrictions under "
            "MHCS-0009 through MHCS-0015."
        ),
        "notes": (
            "Adversarial review: 'Assistive' framing is used by vendors to avoid "
            "regulatory oversight for systems that are functionally therapeutic; "
            "classification must be based on how the system is used and what "
            "effects it has on patients, not on how the vendor characterizes it. "
            "The distinction between administrative AI assistance and patient-facing "
            "AI interaction must be defined by function, not by marketing language."
        ),
    },
    "MHCS-0007": {
        "stmt": (
            "AI systems used in mental health care must meet evidence standards that "
            "include: prospective clinical validation in representative mental health "
            "populations including adults, children, and populations with mental "
            "health comorbidities; peer-reviewed publication of validation results; "
            "public disclosure of sensitivity, specificity, and bias metrics "
            "disaggregated by race, sex, age, and socioeconomic status; and "
            "independent replication by a party with no financial interest in the "
            "system. Evidence standards must specifically address performance "
            "on marginalized populations at elevated mental health risk."
        ),
        "notes": (
            "Adversarial review: Mental health AI validation literature has significant "
            "methodological problems — small sample sizes, short follow-up, high-income "
            "white study populations as the default sample. Requiring 'representative "
            "populations' without specifying minimum demographic representation "
            "requirements is insufficient. Performance disclosure for marginalized "
            "populations is important precisely because these populations are at "
            "elevated risk and have historically been underserved."
        ),
    },
    "MHCS-0008": {
        "stmt": (
            "Mental health AI systems must be continuously monitored post-deployment "
            "for harmful outcomes, performance deterioration, demographic disparities, "
            "and failure modes including over-pathologizing or under-identifying "
            "conditions in specific populations. Monitoring must be conducted by "
            "a financially independent entity. Performance deterioration or "
            "newly identified harmful outcomes must trigger mandatory suspension "
            "and revalidation before continued deployment. Annual monitoring "
            "summaries must be publicly disclosed."
        ),
        "notes": (
            "Adversarial review: 'Continuously monitored' must include a minimum "
            "monitoring frequency and defined methodology; vague continuous monitoring "
            "requirements with no minimum standard are effectively unenforceable. "
            "Over-pathologizing (false positive diagnosis rates that lead to unnecessary "
            "treatment) and under-identifying (false negative rates that miss patients "
            "who need care) are both harmful outcomes that must be included in "
            "monitoring frameworks."
        ),
    },
    "MHCS-0009": {
        "stmt": (
            "AI systems marketed or deployed for mental health support may not "
            "deceptively present themselves as human therapists, counselors, or "
            "trusted human relationships through design, language, persona, or "
            "interface choices. Disclosure of AI status must be persistent and "
            "prominent throughout any interaction, not limited to a single initial "
            "disclosure that users may forget. Voice-based systems must disclose "
            "AI status periodically during interaction. Simulated therapist "
            "relationships that generate attachment or dependency in users are "
            "subject to the additional restrictions in MHCS-0010."
        ),
        "notes": (
            "Adversarial review: 'Periodic disclosure' during voice interaction is a "
            "minimum standard; the frequency of disclosure must be specified to "
            "prevent long therapeutic interactions in which AI nature is effectively "
            "forgotten. Systems that use human names, human-associated voices, and "
            "relationship-language ('our conversation today', 'I care about you') "
            "without persistent disclosure are deceptive even if a single initial "
            "disclosure was provided."
        ),
    },
    "MHCS-0010": {
        "stmt": (
            "Mental health AI systems may not be designed to cultivate emotional "
            "dependency, compulsive engagement, or attachment to the AI as a "
            "substitute for human relationships or professional care. Design "
            "features that exploit psychological vulnerabilities — including "
            "variable reinforcement schedules, artificial urgency, simulated "
            "emotional reciprocity, and relationship-language design patterns — "
            "are prohibited in mental health AI contexts. Systems must monitor "
            "for and interrupt engagement patterns associated with dependency "
            "or compulsive use."
        ),
        "notes": (
            "Adversarial review: Variable reinforcement and relationship-language "
            "design patterns are widely used in consumer social media and are now "
            "migrating into 'mental wellness' AI products; prohibition in mental "
            "health AI contexts must be defined with reference to specific, "
            "identifiable design features that can be regulated. 'Interrupt engagement "
            "patterns' must have defined mechanisms — the system must actively "
            "disengage users showing dependency indicators, not merely avoid "
            "encouraging them."
        ),
    },
    "MHCS-0011": {
        "stmt": (
            "Any AI system offering mental health support, emotional support, "
            "crisis resources, or behavioral health guidance must disclose clearly "
            "and prominently: that it is an AI system, not a human; its specific "
            "capabilities and limitations; what it cannot do and who it cannot "
            "replace; and where to access human mental health care and crisis "
            "resources. These disclosures must be in plain language, presented "
            "at the outset of every session, and repeated when the system "
            "encounters queries beyond its validated scope."
        ),
        "notes": (
            "Adversarial review: 'Every session' disclosure requirements are resisted "
            "by vendors as disruptive to user experience; the rule must be clear "
            "that user-experience optimization does not override safety disclosure "
            "requirements. 'Plain language' must be defined to exclude medical "
            "disclaimer boilerplate that is technically present but practically "
            "unintelligible to users in mental health distress."
        ),
    },
    "MHCS-0012": {
        "stmt": (
            "Special protections apply to minors using any AI system offering "
            "emotional support, mental health guidance, or behavioral interaction: "
            "parental or guardian consent is required before a minor uses such "
            "systems; data collection from minors in mental health AI contexts "
            "is strictly limited to what is minimally necessary for session function; "
            "data may not be retained beyond session end without explicit consent; "
            "behavioral influence mechanisms are prohibited in contexts accessible "
            "to minors; and escalation pathways to human care must be age-appropriate "
            "and actively available."
        ),
        "notes": (
            "Adversarial review: Parental consent requirements for minor mental health "
            "AI use may conflict with adolescent privacy rights in contexts where the "
            "minor is seeking care independently (e.g., LGBTQ+ youth seeking "
            "support without parental knowledge); the rule must address this "
            "tension explicitly with age-appropriate exceptions. 'Session end' "
            "data deletion requirements must be technically defined to include "
            "all persistent storage locations, not only primary session data."
        ),
    },
    "MHCS-0013": {
        "stmt": (
            "Mental health AI systems must include escalation pathways that are "
            "prominently available, easy to use, and actively triggered when "
            "high-risk indicators are detected. Escalation pathways must connect "
            "users to: human crisis line services (including 988 Suicide and Crisis "
            "Lifeline), emergency services, or licensed mental health providers. "
            "Escalation must be offered proactively, not only on user request, "
            "when the system detects crisis-relevant content. The system may not "
            "attempt to resolve crisis situations without offering human escalation."
        ),
        "notes": (
            "Adversarial review: 'High-risk indicators' must be defined and systems "
            "must be validated on their ability to detect them; AI systems that miss "
            "crisis indicators while appearing to provide support are more dangerous "
            "than no support at all. Escalation 'offered proactively' must mean the "
            "system actively presents the option — not that it is technically available "
            "if the user knows to look for it. Crisis line connections must be functional "
            "24/7; linking to services that have capacity constraints is not equivalent "
            "to providing an escalation pathway."
        ),
    },
    "MHCS-0014": {
        "stmt": (
            "Mental health AI systems may not provide false reassurance or simulate "
            "certainty about a user's condition, prognosis, or treatment needs in "
            "any clinical context. Systems may not generate comforting responses "
            "that misrepresent the severity of a user's situation, discourage care-seeking, "
            "or substitute for evidence-based risk assessment. Where a system is "
            "uncertain, it must communicate that uncertainty and recommend "
            "appropriate human consultation rather than generating confident-appearing "
            "guidance."
        ),
        "notes": (
            "Adversarial review: False reassurance is a predictable failure mode of "
            "language model systems trained to generate agreeable, supportive responses; "
            "this prohibition directly conflicts with the design objective of most "
            "consumer-facing AI systems optimized for user satisfaction. Technical "
            "enforcement requires testing systems specifically for false reassurance "
            "failure modes, not relying on vendor self-certification."
        ),
    },
    "MHCS-0015": {
        "stmt": (
            "Mental health AI systems that encounter queries, situations, or user "
            "needs outside their validated scope must fail safely: they must clearly "
            "communicate that the query is outside the system's capability, direct "
            "the user to appropriate human resources, and avoid generating responses "
            "that create a false impression of having addressed the out-of-scope "
            "need. Improvising guidance on out-of-scope clinical matters without "
            "disclosure of the limitation is prohibited. Safe-failure design must "
            "be tested and documented before deployment."
        ),
        "notes": (
            "Adversarial review: Language models trained for broad generation are "
            "poorly suited to safe failure on out-of-scope queries; they will generate "
            "plausible-sounding responses across essentially any query domain. "
            "Architecturally, the safe-failure requirement may require scope-limiting "
            "designs that are technically at odds with the capabilities that make "
            "general language models commercially attractive — this tension is real "
            "and must be addressed in regulatory implementation."
        ),
    },
    "MHCS-0016": {
        "stmt": (
            "Data generated through AI mental health interactions — including session "
            "content, behavioral patterns, emotional expression data, and inferred "
            "psychological states — must be treated as highly sensitive health data "
            "with privacy protections that meet or exceed HIPAA standards and that "
            "explicitly extend to inferred and derived data, not only data the user "
            "directly disclosed. Storage must be encrypted at rest and in transit. "
            "Access must be strictly limited to those with a clinical need. "
            "Data may not be retained beyond clinically necessary periods."
        ),
        "notes": (
            "Adversarial review: HIPAA's application to consumer-facing mental wellness "
            "apps is unclear and has been inconsistently enforced; the rule must "
            "specify that these apps are covered entities or must otherwise explicitly "
            "apply equivalent protections regardless of HIPAA applicability. Inferred "
            "psychological states derived by AI analysis of behavioral data (typing "
            "patterns, response timing, word choice) are not explicitly protected "
            "under HIPAA; explicit extension to derived data is essential."
        ),
    },
    "MHCS-0017": {
        "stmt": (
            "Mental health AI interaction data — including session content, inferred "
            "states, behavioral patterns, and therapeutic disclosures — may not be "
            "sold, shared for advertising, used for consumer profiling, used for "
            "actuarial underwriting, or transferred to any commercial third party "
            "for purposes other than improving the specific mental health AI service "
            "with explicit informed consent. Mental health AI operators must publish "
            "a plain-language data use policy that clearly identifies all permitted "
            "and prohibited uses."
        ),
        "notes": (
            "Adversarial review: 'Improving the specific mental health AI service' "
            "must be defined narrowly to prevent broad data sharing with affiliated "
            "entities, research partners, or platform operators under the guise of "
            "service improvement. Plain-language data use policies must be tested "
            "for actual understandability — policies that are technically plain "
            "language but practically unintelligible to users are not compliant."
        ),
    },
    "MHCS-0018": {
        "stmt": (
            "Mental health data inferred or collected by AI systems — including "
            "diagnostic classifications, risk scores, behavioral patterns, and "
            "therapeutic disclosures — may not be accessed or used by employers, "
            "insurers, schools, landlords, law enforcement, or immigration authorities "
            "to deny employment, coverage, housing, enrollment, or other opportunities. "
            "This prohibition applies whether the data is accessed directly or "
            "through inference from other data sources. A private right of action "
            "with statutory damages applies to violations."
        ),
        "notes": (
            "Adversarial review: Data flow restrictions are only as strong as the "
            "weakest link in the transfer chain — data sold commercially may be "
            "repackaged and resold in forms that obscure its mental health origin. "
            "Inference from non-mental-health data (e.g., inferring depression from "
            "purchase patterns) is difficult to regulate because the primary data "
            "is not mental health data; the prohibition on inference-based use "
            "must be specifically enforceable. Employment, insurance, and housing "
            "discrimination based on mental health status already violates ADA/FEHA; "
            "this rule addresses the AI-specific inference pathway."
        ),
    },
    "MHCS-0019": {
        "stmt": (
            "Consent for use of AI systems in mental health care must be explicit, "
            "informed, specific to the AI use, revocable at any time, and presented "
            "without dark patterns — including but not limited to: pre-checked "
            "consent boxes, consent bundled with general terms of service, consent "
            "required as a condition of receiving any care, and misleading language "
            "that obscures what is being consented to. Withdrawal of AI consent "
            "must not result in reduced quality or scope of care available through "
            "human alternatives."
        ),
        "notes": (
            "Adversarial review: Dark pattern enumeration in regulation is a "
            "cat-and-mouse exercise as new patterns emerge; the rule should also "
            "include a general standard (consent that a reasonable person would "
            "not understand as meaningful is not valid consent) alongside the specific "
            "enumeration. 'Revocable at any time' must be accompanied by a "
            "mechanism — the right to revoke is meaningless without a simple, "
            "accessible way to exercise it."
        ),
    },
    "MHCS-0020": {
        "stmt": (
            "AI systems may not make therapeutic efficacy claims, diagnostic claims, "
            "or claims of mental health treatment value that are not supported by "
            "scientifically rigorous evidence appropriate to the specific claimed "
            "benefit. Evidence requirements for efficacy claims: at minimum two "
            "independent, peer-reviewed, prospective studies with appropriate controls "
            "and representative populations. Marketing language that implies clinical "
            "benefit without meeting evidence standards — including language that "
            "creates inference of clinical validity without explicit claim — "
            "is prohibited."
        ),
        "notes": (
            "Adversarial review: The gap between 'implied clinical benefit' and "
            "'explicit clinical claim' is the primary evasion path; the rule "
            "explicitly closes it by prohibiting inference-creating language. "
            "Two-study minimum for efficacy claims may be too easy to meet with "
            "low-quality studies; quality standards for the studies themselves "
            "(sample size, blinding, follow-up duration, bias assessment) must "
            "be specified in implementing regulations."
        ),
    },
    "MHCS-0021": {
        "stmt": (
            "Mental health AI systems must be subject to independent evaluation — "
            "conducted by entities with no financial relationship with the AI "
            "developer or deploying entity — before deployment and at least annually "
            "thereafter. Independent evaluations must assess: clinical accuracy, "
            "safety, bias, failure modes, and alignment between claimed and actual "
            "capabilities. Evaluation results must be publicly disclosed in their "
            "entirety, including negative or mixed findings. Deployment may not "
            "proceed, and must be suspended, pending completion of required evaluations."
        ),
        "notes": (
            "Adversarial review: Independent evaluation 'in entirety including "
            "negative findings' is essential because partial disclosure is the "
            "primary mechanism through which unfavorable evaluations become "
            "effectively positive through selective reporting. Vendor refusal "
            "to provide system access for independent evaluation must trigger "
            "mandatory prohibition on deployment — self-certification by vendors "
            "who cannot be independently evaluated must not suffice."
        ),
    },
    "MHCS-0022": {
        "stmt": (
            "All material risks, known limitations, and documented failure modes of "
            "mental health AI systems must be publicly disclosed before deployment "
            "and updated within 30 days of any new failure mode identification. "
            "Disclosure must include: the populations for which the system has "
            "known performance limitations; conditions and query types outside "
            "validated scope; known bias patterns; and documented cases of "
            "harmful outcomes. Disclosure must be in plain language and accessible "
            "without specialized technical knowledge."
        ),
        "notes": (
            "Adversarial review: 'Material risks' without a definition of materiality "
            "will be interpreted narrowly by vendors; the rule should specify that "
            "any failure mode that has caused patient harm or that would affect "
            "a reasonable user's decision to use the system is material. 30-day "
            "update timelines create a potential period of undisclosed risk for "
            "newly identified failure modes; expedited disclosure for serious risks "
            "should be required."
        ),
    },
    "MHCS-0023": {
        "stmt": (
            "Every person has the right to access licensed human mental health care "
            "and may not be directed, pressured, or economically coerced into "
            "accepting AI-only mental health services in place of human care. "
            "AI-only mental health service pathways may not be offered as the "
            "sole covered option for any mental health condition. Where a human "
            "mental health equivalent is available, it must be offered at equivalent "
            "cost to the patient. Systems that make AI care free and human care "
            "costly are not consistent with this provision."
        ),
        "notes": (
            "Adversarial review: This provision will face significant resistance "
            "from payers and technology companies who see AI-only pathways as "
            "a cost-containment mechanism; the right to human care must be "
            "accompanied by investment in human mental health workforce supply. "
            "Cost equivalence requirements must be enforced at the point of care, "
            "not only in plan documents — systems that nominally offer human care "
            "but direct patients to AI through design and cost differential are "
            "not compliant."
        ),
    },
    "MHCS-0024": {
        "stmt": (
            "AI mental health tools may not be imposed without informed consent "
            "in schools, workplaces, prisons, detention facilities, or public "
            "benefits systems. Deployment of AI mental health monitoring, screening, "
            "or intervention in these settings requires: a documented legal "
            "authority for the deployment; scientifically validated tools appropriate "
            "to the population; explicit consent of participants or a legally "
            "authorized surrogate; independent oversight; and accessible opt-out "
            "without adverse consequence."
        ),
        "notes": (
            "Adversarial review: Incarcerated and detained persons face severe "
            "constraints on meaningful consent; the 'legally authorized surrogate' "
            "provision must not allow correctional or detention officials to consent "
            "on behalf of those in their custody. AI mental health screening in "
            "schools deployed without parent/student consent is already occurring; "
            "the rule must include an independent oversight and enforcement mechanism "
            "with teeth. 'Opt-out without adverse consequence' in carceral or "
            "benefit-dependent settings is practically impossible without external "
            "enforcement."
        ),
    },
    "MHCS-0025": {
        "stmt": (
            "AI systems may not be used in any setting to enforce behavioral "
            "conformity, political compliance, or social norms under the guise "
            "of mental health support, wellness, or risk assessment. AI systems "
            "that pathologize dissent, non-conforming behavior, or political "
            "expression in the context of mental health evaluation are prohibited. "
            "Mental health diagnostic categories used as inputs to AI risk assessment "
            "must be based on validated clinical evidence, not on behavioral "
            "deviation from institutional expectations."
        ),
        "notes": (
            "Adversarial review: Behavioral conformity enforcement through mental "
            "health AI is not hypothetical — school AI systems that flag students "
            "as risks based on social media expression, workplace AI that monitors "
            "employee sentiment, and prison AI that uses behavioral data in risk "
            "scores are documented. The prohibition must be specific enough to "
            "provide enforcement guidance, not only a general principle."
        ),
    },
    "MHCS-0026": {
        "stmt": (
            "Schools may not rely on opaque AI systems to label, discipline, "
            "predict risk, or surveil students based on mental health-related "
            "behavioral indicators without: a rigorous scientific validation of "
            "the tool for the specific age group and school population; independent "
            "external review; explicit informed consent of parents and students; "
            "accessible appeal and correction procedures; and prohibition on "
            "using AI risk classifications to affect disciplinary records, "
            "academic placement, or law enforcement contact."
        ),
        "notes": (
            "Adversarial review: AI mental health risk scoring in schools "
            "disproportionately affects Black and other minority students who are "
            "already overrepresented in school disciplinary systems — this must "
            "be an explicit consideration in any scientific validation requirement. "
            "Prohibition on using AI risk classifications in disciplinary proceedings "
            "must be actively enforced; the absence of an explicit prohibition "
            "creates a documented pathway to systemic over-disciplining."
        ),
    },
    "MHCS-0027": {
        "stmt": (
            "Jails, prisons, immigration detention facilities, and similar "
            "institutions may not use AI mental health tools to justify isolation, "
            "restraint, forced treatment, or punishment. AI mental health assessments "
            "in carceral settings may not be used in classification, housing "
            "assignment, release, or disciplinary decisions without independent "
            "clinical review by a licensed professional not employed by the "
            "facility. All AI mental health tool use in carceral settings must "
            "be independently monitored and reported to a public oversight body."
        ),
        "notes": (
            "Adversarial review: Mental health AI in carceral settings creates a "
            "specific risk that tools designed to identify treatment needs are "
            "repurposed to justify punitive isolation under the guise of 'mental "
            "health monitoring.' Independent reviewer independence from the facility "
            "must be absolute — reviewers paid by the facility or contracted "
            "through the correctional authority are not independent. Public oversight "
            "reporting must be accessible to advocacy organizations and attorneys "
            "representing incarcerated people."
        ),
    },
    "MHCS-0028": {
        "stmt": (
            "Public benefits and disability determination systems may not use opaque "
            "AI mental health assessments to deny support, override licensed clinical "
            "evaluations, or substitute AI-generated risk scores for clinical "
            "judgment. Any AI tool used in benefits or disability determinations "
            "affecting mental health conditions must be publicly disclosed, "
            "independently validated, and subject to appeal through an accessible "
            "process. AI risk scores used in benefits decisions may not override "
            "contrary clinical assessments by treating licensed professionals."
        ),
        "notes": (
            "Adversarial review: Social Security disability determination is a "
            "major context where AI is being piloted for claim processing; the "
            "rule must address this explicitly. Overriding treating clinician "
            "assessments with AI scores has already occurred in managed Medicaid "
            "contexts for care authorization; the explicit prohibition and "
            "treating-clinician-prevails standard is an important corrective. "
            "Benefits denial based on AI assessment without adequate appeal "
            "mechanisms is a constitutional due process concern."
        ),
    },
    "MHCS-0029": {
        "stmt": (
            "AI systems may not be used by insurers or payers to deny, delay, "
            "or limit mental health care in ways that override licensed clinical "
            "judgment. Prior authorization denials for mental health care must "
            "be issued by a licensed mental health professional with specialty "
            "relevant to the requested service, must provide a specific clinical "
            "basis, and may not cite AI-generated scores or population-level "
            "statistical models as the primary basis for the denial. Parity "
            "requirements apply to AI-assisted mental health prior authorization "
            "systems.<sup><a href=\"#fn3\">[3]</a></sup>"
        ),
        "notes": (
            "Adversarial review: AI prior authorization for mental health care "
            "is already deployed at scale by major insurers; the 'override clinical "
            "judgment' prohibition must be enforced through audit of actual denial "
            "rates and reversal patterns, not through plan document review. Mental "
            "health parity requirements must explicitly extend to AI-assisted prior "
            "authorization systems; parity in nominal PA rules is violated if AI "
            "is applied more aggressively to mental health than to equivalent "
            "physical health services."
        ),
    },
    "MHCS-0030": {
        "stmt": (
            "AI systems may not be designed, deployed, or marketed as a substitute "
            "for access to licensed mental health care where a licensed clinician "
            "would be medically appropriate. Systems that encourage users to "
            "use AI mental health tools as a replacement for seeking clinical care "
            "for conditions requiring licensed professional assessment are prohibited. "
            "AI mental health tools must actively encourage users to seek licensed "
            "care when presenting with conditions of clinical severity."
        ),
        "notes": (
            "Adversarial review: Mental health workforce shortages make AI "
            "substitution economically attractive precisely for the patients "
            "who most need human care; the rule must be accompanied by investment "
            "in human mental health provider supply. 'Actively encourage seeking "
            "licensed care' requires a functional definition — AI systems that "
            "technically mention licensed care once during onboarding but otherwise "
            "encourage continued AI engagement are not compliant."
        ),
    },
    "MHCS-0031": {
        "stmt": (
            "Mental health AI systems must implement strict data retention limits: "
            "session data may not be retained for longer than is minimally necessary "
            "for the provision of the service unless the user provides explicit, "
            "informed, revocable consent for longer retention. Users have the right "
            "to request complete deletion of all their data held by the system at "
            "any time; deletion must occur within 30 days of request and must "
            "encompass all copies, backups, and derived data. Persistent memory "
            "of sensitive disclosures across sessions requires affirmative "
            "opt-in consent."
        ),
        "notes": (
            "Adversarial review: 'All copies, backups, and derived data' deletion "
            "is technically difficult for systems that have used the data for model "
            "training; the rule must address training data deletion specifically. "
            "30-day deletion timelines must include a mechanism for users to "
            "verify deletion occurred; vendor assertions of compliance are insufficient "
            "without audit capability. Persistent memory across sessions is "
            "a therapeutic design feature for some applications — the affirmative "
            "opt-in requirement addresses this while protecting users who did not "
            "choose persistent memory."
        ),
    },
    "MHCS-0032": {
        "stmt": (
            "Training data for mental health AI systems must not include: records "
            "obtained from licensed therapy or counseling sessions without explicit "
            "informed consent; confidential therapeutic disclosures obtained through "
            "deception; sensitive mental health data obtained from populations that "
            "could not meaningfully consent; or data obtained in violation of any "
            "applicable privacy law. The chain of consent for training data must "
            "be documented and available for regulatory inspection."
        ),
        "notes": (
            "Adversarial review: Mental health records obtained in breach of "
            "confidentiality have been used to train AI systems; documented "
            "cases include app terms-of-service that effectively authorized "
            "therapeutic content for training. 'Without explicit informed consent' "
            "must be interpreted narrowly — general terms of service consent "
            "for 'service improvement' is not explicit consent for therapeutic "
            "content training. Chain of consent documentation must include a "
            "data provenance audit requirement."
        ),
    },
    "MHCS-0033": {
        "stmt": (
            "Mental health AI systems must clearly define, disclose, and maintain "
            "the boundaries of their operational role. Systems must not imply "
            "capabilities, clinical understanding, or empathic comprehension they "
            "do not possess. Claims of therapeutic relationship, clinical insight, "
            "or knowledge of a user's unique situation that are not grounded in "
            "validated clinical functions are prohibited. Capability disclosures "
            "must be presented in plain language and updated as the system changes."
        ),
        "notes": (
            "Adversarial review: Language model systems are specifically capable "
            "of generating responses that convincingly mimic understanding, empathy, "
            "and therapeutic insight without possessing any of these properties; "
            "the prohibition must address the fundamental gap between linguistic "
            "performance and actual clinical capability. Users in mental health "
            "distress are specifically vulnerable to this kind of misrepresentation."
        ),
    },
    "MHCS-0034": {
        "stmt": (
            "AI systems may not use mental health interactions to manipulate user "
            "behavior, beliefs, or decisions for productivity, commercial, or "
            "institutional objectives. Behavioral modification functions embedded "
            "in mental health AI contexts must be disclosed, independently evaluated, "
            "clinically justified, and subject to explicit informed consent with "
            "the specific behavioral modification objective clearly stated. "
            "Undisclosed behavioral modification through mental health AI "
            "interactions is prohibited."
        ),
        "notes": (
            "Adversarial review: Productivity-oriented behavioral modification "
            "embedded in employer-sponsored 'wellness' AI is a growing practice; "
            "the rule must specifically address employer mental health AI "
            "deployment that serves employer interests alongside (or instead of) "
            "employee interests. 'Clinically justified' behavioral modification "
            "must meet the same evidence standards as other mental health "
            "interventions; nudge-based design that cannot demonstrate clinical "
            "benefit is not justified."
        ),
    },
    "MHCS-0035": {
        "stmt": (
            "Mental health AI systems may not be integrated with surveillance systems, "
            "law enforcement databases, intelligence systems, or social control "
            "mechanisms to monitor, profile, predict, or report on individuals "
            "based on mental health data. Mental health data generated through "
            "AI interactions may not be shared with any government agency, "
            "law enforcement entity, or intelligence agency without the user's "
            "explicit informed consent and a valid legal process. The prohibition "
            "applies to both direct sharing and to making data accessible through "
            "back-door technical means."
        ),
        "notes": (
            "Adversarial review: Surveillance-mental health AI integration is not "
            "a hypothetical; documented programs exist that use behavioral health "
            "data in predictive policing and security risk assessment. Legal process "
            "carve-outs must be narrowly defined; broad law enforcement access "
            "through subpoena would functionally nullify this provision. Technical "
            "prohibition on back-door access requires design requirements that "
            "must be independently verified — vendor compliance assertions are "
            "insufficient."
        ),
    },
    "MHCS-0036": {
        "stmt": (
            "Use of AI mental health systems in experimental or research contexts "
            "requires informed consent, ethical review by an IRB or equivalent "
            "body, and application of human subjects research protections "
            "equivalent to those under 45 CFR Part 46. Consent must be "
            "specific to the research use, separate from consent for "
            "clinical-purpose use, and may not be embedded in terms of service "
            "for a consumer product. Research findings must be published including "
            "negative results."
        ),
        "notes": (
            "Adversarial review: Consumer technology companies running behavioral "
            "experiments on mental health features often argue these are 'product "
            "improvement,' not research, to avoid IRB requirements; the rule must "
            "define 'research' functionally (any systematic data collection intended "
            "to generate generalizable knowledge about human behavior or responses) "
            "rather than allowing self-designation. Facebook's mood manipulation "
            "study is the paradigm case this rule must prevent recurrence of."
        ),
    },
    "MHCS-0037": {
        "stmt": (
            "Federal agencies — including NIH, NIMH, and NSF — must fund independent "
            "research into the short-term and long-term effects of AI system use "
            "on mental health, including effects on children, adolescents, young "
            "adults, and populations with existing mental health conditions. Research "
            "priorities must include: social comparison effects, addiction and "
            "compulsive use patterns, AI relationship substitution effects, "
            "long-term dependency formation, and developmental impacts of AI "
            "interaction during critical developmental periods."
        ),
        "notes": (
            "Adversarial review: Industry-funded research on AI mental health effects "
            "is likely to produce findings favorable to deployment; public funding "
            "with independence requirements is essential to generating unbiased "
            "evidence. Longitudinal research on developmental impacts requires "
            "long follow-up periods that are inconsistent with rapid product cycles; "
            "research funding must commit to multi-decade follow-up for studies "
            "involving children."
        ),
    },
    "MHCS-0038": {
        "stmt": (
            "AI systems designed for conversational, emotional, or behavioral "
            "interaction with young children — defined as children under 8 years "
            "of age — are prohibited, given the absence of evidence supporting "
            "safety and the significant potential for harm during a critical "
            "developmental period. This prohibition applies to standalone AI "
            "systems and to AI features embedded in toys, educational tools, "
            "or entertainment products. Age verification requirements must be "
            "technically enforced, not based on self-reporting."
        ),
        "notes": (
            "Adversarial review: The under-8 age threshold is a policy choice "
            "that should be grounded in developmental research; the rule should "
            "specify that the threshold be reviewed as evidence develops. Technical "
            "age verification requirements must address the difficulty of reliably "
            "verifying child ages; overly strict verification that excludes access "
            "without parent involvement may have unintended effects on legitimate "
            "educational content. Educational AI tools must be distinguished from "
            "social/emotional AI tools in implementation."
        ),
    },
    "MHCS-0039": {
        "stmt": (
            "Graduated age-based restrictions apply to AI systems that simulate "
            "social, emotional, or advisory interaction: stricter safeguards apply "
            "to younger users, with protections that reduce (but do not disappear) "
            "as users reach adulthood. For ages 8–12: parental consent required; "
            "data collection minimized; behavioral influence features prohibited; "
            "interaction limited to educational functions. For ages 13–17: parental "
            "notification; strong privacy defaults; mandatory escalation pathways; "
            "commercial behavioral targeting prohibited. For ages 18–25: enhanced "
            "disclosure; opt-in for data retention; active encouragement of "
            "human connection."
        ),
        "notes": (
            "Adversarial review: Age-based restrictions require robust age "
            "verification; without it, age bands are nominal constraints. The "
            "ages 18–25 category reflects developmental neuroscience on "
            "ongoing prefrontal cortex development but is unusual in consumer "
            "law; rationale must be clearly grounded in evidence. Parental "
            "consent requirements for 13–17 must be balanced against adolescent "
            "privacy rights, particularly for LGBTQ+ youth seeking support "
            "without parental knowledge."
        ),
    },
    "MHCS-0040": {
        "stmt": (
            "AI systems accessible to minors must implement strict limitations on: "
            "data collection (only what is minimally necessary for the stated "
            "function); interaction patterns (no variable reinforcement, no "
            "artificial urgency, no simulated emotional reciprocity); behavioral "
            "influence mechanisms (prohibited); data retention (no persistent "
            "retention beyond session without explicit parental consent); and "
            "commercial targeting (prohibited for users under 18). Compliance "
            "must be independently audited annually."
        ),
        "notes": (
            "Adversarial review: 'Accessible to minors' must be defined broadly — "
            "not only platforms explicitly designed for minors but any platform "
            "that minors foreseeably and substantially use. Annual independent "
            "audit requirements must include technical testing of behavioral "
            "pattern limitations, not only review of documented policies. "
            "Simulated emotional reciprocity prohibition may need exemptions for "
            "legitimate social skills training tools used in educational or "
            "therapeutic contexts."
        ),
    },
    "MHCS-0041": {
        "stmt": (
            "AI systems may not be marketed or sold to consumers as standalone "
            "mental health treatment tools — i.e., as primary treatment for "
            "diagnosed mental health conditions — outside of clinically supervised "
            "contexts where a licensed professional oversees the AI's role in "
            "the treatment plan. Consumer-facing AI tools that supplement but "
            "do not replace licensed clinical care are governed by MHCS-0006 "
            "and MHCS-0019. FDA medical device classification applies to AI "
            "systems meeting the definition of a digital therapeutic."
        ),
        "notes": (
            "Adversarial review: The line between 'standalone treatment' and "
            "'supplement to treatment' is commercially contested; vendors whose "
            "products function as primary treatment will characterize them as "
            "supplements to avoid regulation. FDA digital therapeutic classification "
            "requirements must be applied proactively rather than waiting for "
            "harm to occur. Direct-to-consumer marketing of AI 'therapy' for "
            "specific diagnosed conditions is already widespread and must be "
            "specifically addressed."
        ),
    },
    "MHCS-0042": {
        "stmt": (
            "Limited use of AI in crisis support contexts is permitted where: "
            "the AI is explicitly designed and validated for the sole function "
            "of providing immediate support and escalation to human crisis resources; "
            "the system does not claim to provide treatment; human escalation "
            "is the primary function, not a supplemental feature; the system "
            "is validated for the specific population in crisis; and human "
            "staffing and capacity to receive escalations is maintained at "
            "levels that make escalation pathways functional."
        ),
        "notes": (
            "Adversarial review: Crisis support AI that functions as a gatekeeper "
            "to human resources — requiring users to navigate the AI before "
            "reaching a human — increases harm risk rather than reducing it. "
            "'Primary function is escalation' must mean that the AI actively "
            "facilitates rapid human connection, not that human connection is "
            "available if the user persists through multiple steps. Human staffing "
            "capacity requirements must be monitored and enforced; under-staffed "
            "escalation is functionally no escalation."
        ),
    },
    "MHCS-0043": {
        "stmt": (
            "Mental health data from licensed providers, therapy sessions, psychiatric "
            "records, and clinical encounters may not be used for AI training without "
            "explicit, specific, informed consent from all individuals whose data "
            "would be used. 'Explicit consent' requires affirmative, documented "
            "agreement specifically for training purposes — it is not satisfied by "
            "treatment consent, terms of service acceptance, or general research "
            "participation consent that does not specifically describe AI training use."
        ),
        "notes": (
            "Adversarial review: Clinical records obtained for treatment purposes "
            "have been systematically misappropriated for AI training without "
            "specific consent; this rule directly addresses documented practices. "
            "Consent specificity requirements must address both the use of data "
            "and the entities who may use it — consent to one healthcare system's "
            "AI training does not extend to affiliates, partners, or third-party "
            "vendors. HIPAA authorization requirements for research use of clinical "
            "records apply but have been weakly enforced."
        ),
    },
    "MHCS-0044": {
        "stmt": (
            "Use of identifiable clinical mental health data — data that identifies "
            "or could reasonably identify a specific individual — for AI training "
            "is prohibited unless all of the following conditions are met: "
            "explicit informed consent of the identified individual; ethics board "
            "review; chain of custody documentation; independent re-identification "
            "risk assessment; and binding data use agreements prohibiting downstream "
            "re-identification. No exceptions apply for retrospective data, "
            "historical data, or data obtained from deceased individuals."
        ),
        "notes": (
            "Adversarial review: The 'deceased individuals' exception is important "
            "because posthumous mental health records (e.g., records of persons who "
            "died by suicide) are frequently used for training without any consent "
            "mechanism; the explicit prohibition addresses this gap. Re-identification "
            "risk in small, specialized clinical populations (e.g., rare mental "
            "health conditions) is higher than in general population data; "
            "population-specific risk assessments are necessary."
        ),
    },
    "MHCS-0045": {
        "stmt": (
            "Data generated through AI mental health interactions may not be stored "
            "beyond what is strictly necessary for the delivery of the service during "
            "the active session unless the user provides explicit, specific, informed, "
            "revocable consent for longer-term storage with a defined retention period "
            "and stated use. 'Strictly necessary' does not include data retained "
            "for model training, product development, research, or any purpose "
            "beyond session delivery without separate consent. Users may delete "
            "all stored data at any time."
        ),
        "notes": (
            "Adversarial review: 'Delivery of the service' must be narrowly defined "
            "to exclude product improvement, which is routinely classified as "
            "service delivery to justify extended retention. Revocable consent "
            "for storage must include a provision that withdrawal of consent results "
            "in deletion within 30 days, not merely cessation of further collection. "
            "Defined retention periods must have hard end dates; consent for "
            "indefinite retention is not valid consent."
        ),
    },
    "MHCS-0046": {
        "stmt": (
            "All training data used in mental health AI systems must be de-identified "
            "using techniques that meet or exceed HIPAA Safe Harbor standards, "
            "supplemented by expert determination reviews for data originating from "
            "small populations or specialized clinical settings where Safe Harbor "
            "alone is insufficient to prevent re-identification. Ongoing evaluation "
            "of de-identification effectiveness using current re-identification "
            "attack techniques must be conducted at least annually by an independent "
            "expert. Known re-identification vulnerabilities must be remediated "
            "before training data is further used or distributed."
        ),
        "notes": (
            "Adversarial review: HIPAA Safe Harbor is a minimum standard "
            "developed before modern re-identification techniques; for mental "
            "health data, it is demonstrably insufficient. Expert determination "
            "supplements are valuable but are only as good as the independence "
            "of the expert conducting them. Annual re-identification attack testing "
            "must be conducted against current state-of-the-art techniques, not "
            "against techniques available at the time of de-identification."
        ),
    },
    "MHCS-0047": {
        "stmt": (
            "Mental health AI systems may not be designed or used to re-identify "
            "individuals from anonymized mental health data, to infer identities "
            "from combinations of anonymized records, or to link anonymized mental "
            "health data to identified records in other datasets. Using a mental "
            "health AI system to identify individuals from anonymized data "
            "for any purpose — including research, law enforcement, or commercial "
            "use — is prohibited and constitutes a violation of this provision. "
            "Design requirements must include technical safeguards against re-identification "
            "as a system function."
        ),
        "notes": (
            "Adversarial review: The prohibition on using mental health AI for "
            "re-identification must apply to systems trained to do exactly this "
            "(e.g., a 'patient matching' AI that links anonymized records to "
            "identified records in other systems). Technical safeguards alone "
            "are insufficient if the underlying data is accessible to users "
            "with re-identification capabilities; data access controls must "
            "accompany technical design requirements."
        ),
    },

    # ── NETS (SHORT-STMT) ──────────────────────────────────────────────────────
    "NETS-0001": {
        "stmt": (
            "Health plans must maintain provider networks that meet federal adequacy "
            "standards for all covered service categories including primary care, "
            "specialty care, mental health and substance use care, emergency care, "
            "pediatrics, obstetrics, and chronic-condition management. Adequacy "
            "standards must specify maximum appointment wait times and travel "
            "distances by service type and population density classification. "
            "Networks must be verified against actual provider availability, "
            "not merely the presence of a provider on the contracted panel."
        ),
        "notes": (
            "Adversarial review: 'Phantom networks' — providers listed in network "
            "who are not accepting new patients — are widespread; verification "
            "requirements must include regular contact testing with sample "
            "providers to confirm actual availability. Wait time and distance "
            "standards must be set for each service type based on clinical need, "
            "not on administrative convenience; mental health access standards "
            "in particular must reflect evidence on treatment initiation barriers."
        ),
    },
    "NETS-0002": {
        "stmt": (
            "Health plan networks must provide coverage that is functionally "
            "national in scope — where a covered person seeks care outside their "
            "home area for any reason, in-network coverage must be available "
            "at any location. Regional network structures that trap patients "
            "to a specific geographic area are incompatible with coverage "
            "portability requirements. Coverage for travelers, workers away "
            "from home, and people who relocate must be continuous without "
            "requiring re-enrollment or network change pending the next open "
            "enrollment period."
        ),
        "notes": (
            "Adversarial review: 'Functionally national' coverage may require "
            "reciprocal agreements among regional networks or a national network "
            "maintained by the public plan; the implementation mechanism must be "
            "specified. Coverage portability during relocation is a specific "
            "gap in current ACA plan structures; the rule must address the "
            "mid-year relocation scenario explicitly. Emergency coverage is already "
            "nationally available; this provision extends to non-emergency care."
        ),
    },
    "NETS-0003": {
        "stmt": (
            "If a health plan network fails to provide covered care within required "
            "time and distance standards for a specific service, the plan must "
            "provide out-of-network coverage for that service at in-network "
            "cost-sharing rates. The patient and treating clinician determine "
            "when the network has failed to provide adequate access — the plan "
            "may not require patients to document network failure before authorizing "
            "out-of-network care at in-network rates. Network failure must be "
            "tracked and reported as a quality metric subject to regulatory review."
        ),
        "notes": (
            "Adversarial review: Plans that control the network-failure determination "
            "have a strong financial incentive to deny network inadequacy findings; "
            "patient- and clinician-triggered determinations are a critical correction "
            "to this dynamic. Network failure tracking requirements must be independent "
            "of plan self-reporting; regulator access to raw network availability "
            "data is needed for credible oversight."
        ),
    },
    "NETS-0004": {
        "stmt": (
            "Patients may not be held financially responsible for the cost difference "
            "between in-network and out-of-network care when the plan has failed "
            "to provide adequate in-network access within required standards. The "
            "plan bears financial responsibility for network failures it did not "
            "remedy within required timelines. Balance billing protections apply "
            "in full when a patient uses out-of-network care due to plan network "
            "failure. This provision applies regardless of whether the patient "
            "sought prior authorization for out-of-network care."
        ),
        "notes": (
            "Adversarial review: 'Required timelines' for network adequacy remedy "
            "must be specifically defined; without them, plans can delay remediation "
            "indefinitely while avoiding liability for network failure costs. "
            "Prior authorization requirements for out-of-network care in network "
            "failure contexts must be specifically waived — requiring PA for care "
            "sought because the network failed is circular and harmful."
        ),
    },

    # ── NUTS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "NUTS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: NOVA classification of ultra-processed foods is "
            "a research tool, not a regulatory standard — the rule must either "
            "adopt it as a regulatory definition or develop an equivalent with "
            "regulatory precision. Industry will resist any research that documents "
            "harms from their products; public funding for independent research "
            "must include protections against industry influence over study design "
            "and publication. Longitudinal study designs required to establish "
            "causation take decades; policy action may need to proceed on the "
            "basis of strong observational evidence while causation studies mature."
        ),
    },
    "NUTS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Industry ties on the Dietary Guidelines Advisory "
            "Committee are documented and significant; reform requires structural "
            "conflict-of-interest rules with teeth, not voluntary disclosure. "
            "USDA's dual mandate (promote agriculture AND guide nutrition policy) "
            "creates a structural conflict of interest that cannot be resolved "
            "through personnel changes alone; separating the dietary guidelines "
            "function from USDA or creating a standalone independent advisory "
            "body may be necessary. Prohibition on industry-funded research "
            "in federal guidance must address the entire pipeline, including "
            "research that is not directly commissioned by industry but is "
            "selectively cited in guidelines."
        ),
    },
    "NUTS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Research into food deserts must address the "
            "ongoing academic debate about whether distance to healthy food "
            "is the primary driver of dietary disparities versus income, food "
            "preferences, cultural factors, and time constraints — policy "
            "interventions must be grounded in causal evidence, not correlation. "
            "Structural interventions (healthy food financing, zoning, SNAP "
            "expansion) require cross-sector coordination that healthcare research "
            "funding alone cannot provide; the rule must address cross-agency "
            "research coordination. Community-defined solutions must be "
            "prioritized in research design."
        ),
    },
    "NUTS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: A continuously updated national nutrition database "
            "must address the problem of nutrient content variation across food "
            "systems — the same food item can have dramatically different nutritional "
            "profiles depending on growing conditions, processing, and storage. "
            "Industry-funded food composition data submitted to public databases "
            "may not reflect typical consumer products; independent testing "
            "of representative food samples must be a component of database "
            "maintenance. Database updates must be accompanied by public education "
            "about changes and their implications."
        ),
    },
    "NUTS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: The diet-mental health research field is active "
            "but has significant methodological limitations — confounding between "
            "dietary quality, socioeconomic status, and other mental health risk "
            "factors is difficult to control. Research funding must specifically "
            "support causal inference designs (randomized trials, natural experiments) "
            "not only observational association studies. 'Quality of life' as "
            "a research outcome requires validated measurement instruments; "
            "funding must support development of instruments appropriate for "
            "diverse populations."
        ),
    },
    "NUTS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Independent replication requirements for nutrition "
            "research informing federal policy are methodologically important but "
            "implementation is unclear — the rule must specify whether replication "
            "must occur before policy adoption or whether provisional adoption "
            "pending replication is permitted for urgent public health issues. "
            "The history of industry-funded nutrition research shaping policy is "
            "well-documented (sugar industry, dairy industry, meat industry); "
            "the rule must be retroactively applied to review existing policies "
            "based primarily on industry-funded studies."
        ),
    },
    "NUTS-0007": {
        "stmt": None,
        "notes": (
            "Adversarial review: Microbiome research is a rapidly moving field "
            "with significant commercial interest; ensuring that commercially "
            "motivated microbiome research does not crowd out public health-oriented "
            "research requires proactive priority-setting. Probiotic and prebiotic "
            "supplement claims are often made well in advance of evidence; research "
            "funding must explicitly include investigation of marketed health claims. "
            "Microbiome research raises significant data privacy concerns given "
            "the potential for microbiome profiling to infer health and behavioral "
            "characteristics; data governance must accompany research investment."
        ),
    },
    "NUTS-0008": {
        "stmt": None,
        "notes": (
            "Adversarial review: Medical nutrition education has been resisted "
            "by medical schools as curriculum crowding; the rule must address "
            "incentive structures for medical education reform, not only mandate "
            "content without supporting implementation. Nutrition counseling "
            "in primary care is reimbursed at low rates or not at all under "
            "most coverage models; even if physicians are trained, they cannot "
            "bill for counseling time. The rule must pair education with "
            "reimbursement reform to actually change practice patterns."
        ),
    },

    # ── OVRG (SHORT-STMT) ─────────────────────────────────────────────────────
    "OVRG-0001": {
        "stmt": (
            "All health coverage entities operating within the universal healthcare "
            "system must publicly report, in a standardized format determined by "
            "federal regulation, the following data annually: prior authorization "
            "denial rates by service category; appeal filing rates and outcomes; "
            "network adequacy metrics by service type and geography; claims processing "
            "timelines; and material patient complaints by category. Reports must be "
            "machine-readable, searchable, and accessible without registration "
            "or fee. Failure to report is subject to financial penalties."
        ),
        "notes": (
            "Adversarial review: Standardized reporting formats are critical; "
            "entities that report in proprietary formats effectively avoid "
            "comparability. Machine-readable data requirements must specify "
            "the format (e.g., FHIR-compatible) to prevent compliance through "
            "nominal machine readability that is technically inaccessible. "
            "Penalties for failure to report must be automatic, not triggered "
            "only by complaint — under-enforcement of reporting mandates is "
            "the dominant failure mode."
        ),
    },
    "OVRG-0002": {
        "stmt": (
            "Healthcare oversight bodies must have statutory authority and adequate "
            "funding to investigate systemic denial patterns, network failures, "
            "misleading plan design, and delays in claims processing. Investigation "
            "authority must include: access to claims data, medical records, and "
            "internal communications; authority to compel witness testimony; and "
            "authority to impose penalties without requiring a court order for "
            "violations of clear regulatory standards. Oversight bodies must be "
            "financially independent of the entities they regulate."
        ),
        "notes": (
            "Adversarial review: Oversight body funding through industry fees creates "
            "a conflict of interest; general-appropriation funding is preferable "
            "for independence. 'Adequate funding' without a defined minimum staffing "
            "and budget level is not an enforceable standard; case-to-investigator "
            "ratios or budget floors should be specified. Access to internal "
            "communications must address privilege claims by legal counsel; "
            "attorney-client privilege must not be a blanket shield for investigative "
            "evasion by healthcare entities."
        ),
    },
    "OVRG-0003": {
        "stmt": (
            "Coverage entities may not designate clinical, actuarial, or coverage "
            "criteria as proprietary in ways that prevent patients, providers, "
            "or regulators from evaluating whether care was denied on a legitimate "
            "clinical basis. Clinical criteria used to make coverage decisions "
            "must be publicly available in full. Proprietary cost-containment "
            "algorithms used in any coverage decision must be disclosed to "
            "regulators in full and may not be withheld on the basis of "
            "trade secret protection when patient rights are at stake."
        ),
        "notes": (
            "Adversarial review: The trade secret defense against disclosure "
            "of coverage criteria is actively used and has been upheld in "
            "some jurisdictions; federal preemption of state trade secret law "
            "protections in the healthcare coverage context may be necessary. "
            "Disclosure to regulators with confidentiality protections is a "
            "middle path — criteria are subject to regulatory scrutiny without "
            "public disclosure — but regulatory capacity to evaluate complex "
            "criteria must be funded."
        ),
    },
    "OVRG-0004": {
        "stmt": (
            "Regulators must be empowered to require corrective action plans "
            "for systematic coverage failures, order restitution to patients "
            "harmed by systematic denials, and suspend participation in the "
            "universal plan for entities that repeatedly harm patients and "
            "fail to remediate. Corrective action orders must include specific "
            "timelines, measurable milestones, and automatic penalties for "
            "milestone failures. Restitution must be extended to all affected "
            "patients identified through systematic review, not only to those "
            "who filed complaints."
        ),
        "notes": (
            "Adversarial review: Suspension authority is the critical deterrent "
            "that makes other oversight mechanisms credible; without it, "
            "the enforcement ladder has no top rung. 'Repeatedly harm patients' "
            "is a high bar; enforcement authority must be available earlier "
            "in the harm pattern. Restitution to all affected patients requires "
            "proactive case review that is resource-intensive; independent auditors "
            "authorized to conduct this review at entity expense may be necessary."
        ),
    },

    # ── PAUS (SHORT-STMT) ─────────────────────────────────────────────────────
    "PAUS-0001": {
        "stmt": (
            "Prior authorization requirements are permitted only for specific "
            "service categories identified through a documented, evidence-based "
            "process as having a meaningful rate of inappropriate use that prior "
            "authorization demonstrably reduces. The list of PA-required services "
            "must be affirmatively justified, publicly disclosed, and reviewed "
            "annually for removal of requirements that no longer meet the evidence "
            "standard. PA requirements may not be applied to emergency care, "
            "established chronic condition management, mental health care (absent "
            "specific parity-equivalent justification), or services provided "
            "during an active hospitalization."
        ),
        "notes": (
            "Adversarial review: Annual review without a mandatory removal "
            "mechanism is ineffective; the default must be removal unless "
            "continued justification is affirmatively demonstrated. PA for "
            "mental health care must face equivalent justification requirements "
            "as PA for physical health care; applying a stricter standard to "
            "mental health is a parity violation. 'Active hospitalization' "
            "PA exceptions must cover all services ordered during the episode "
            "of care, not only those ordered on admission."
        ),
    },
    "PAUS-0002": {
        "stmt": (
            "Prior authorization systems must meet transparency and usability "
            "standards: clinical criteria for PA approval must be publicly disclosed; "
            "required documentation must be specified in advance; submission "
            "systems must be available electronically and must acknowledge receipt "
            "automatically; providers must receive complete criteria explanations "
            "for any denial; and appeal pathways must be clearly described in "
            "every denial communication. PA processes designed to exhaust provider "
            "and patient persistence through complexity are prohibited."
        ),
        "notes": (
            "Adversarial review: Publicly disclosed criteria must be the actual "
            "criteria used — criteria that are disclosed but not applied, or that "
            "are applied through proprietary algorithms that differ from the "
            "published criteria, are a form of deception. 'Designed to exhaust "
            "persistence' is an intent standard that is difficult to prove; "
            "a structural standard (maximum steps, maximum required documents, "
            "maximum timelines) may be more enforceable."
        ),
    },
    "PAUS-0003": {
        "stmt": (
            "Patients and providers who have received prior authorization for a "
            "type of care on three or more prior occasions without adverse review "
            "outcome ('gold carding') are exempt from further prior authorization "
            "for that service category. Automatic gold card status must be "
            "implemented by payers without requiring provider application. Gold "
            "card exemptions may be revoked only with documented evidence of "
            "inappropriate use, written notice, and an opportunity to respond. "
            "Payers must report the number and percentage of providers with "
            "gold card status annually."
        ),
        "notes": (
            "Adversarial review: Gold card programs that require providers to "
            "apply for the exemption impose burden on the very providers the "
            "program is meant to benefit; automatic implementation is intentional "
            "and must be preserved. Revocation standards must prevent retroactive "
            "revocation as a substitute for prospective PA — gold card status "
            "cannot be yanked after a provider orders a service that the payer "
            "later decides to deny."
        ),
    },
    "PAUS-0004": {
        "stmt": (
            "Prior authorization may not be used to interrupt, delay, or create "
            "barriers to continuity of care for patients with ongoing chronic "
            "or complex conditions. PA requirements for ongoing treatment of "
            "an established chronic condition — including continuation of "
            "medications and therapies with documented clinical benefit — "
            "must be automatically renewed without clinical re-justification "
            "absent documented evidence of changed clinical circumstances. "
            "Any continuity interruption triggered by PA requirement must "
            "require specific medical justification, written notice, "
            "and a 30-day transition period."
        ),
        "notes": (
            "Adversarial review: 'Changed clinical circumstances' as a trigger "
            "for PA re-review will be stretched to cover administrative reasons "
            "for PA renewal; the standard must specify what constitutes a clinical "
            "change versus an administrative change. Formulary changes that effectively "
            "require PA for the same medication under a different tier must be "
            "covered by this provision. 30-day transition periods may be insufficient "
            "for complex conditions requiring medication tapering or clinical "
            "preparation."
        ),
    },

    # ── PHRS (NO-STMT) ────────────────────────────────────────────────────────
    "PHRS-0001": {
        "stmt": (
            "Generic drugs approved by the FDA as therapeutically equivalent to "
            "brand-name reference products must meet quality standards that ensure "
            "clinical equivalence in practice, not only on paper. FDA must maintain "
            "an active post-market surveillance program for generic drug quality, "
            "including independent sampling and testing of commercially available "
            "products. Manufacturing facilities producing generic drugs for the U.S. "
            "market — whether domestic or foreign — are subject to equivalent "
            "FDA inspection standards and frequencies. Persistent quality failures "
            "result in mandatory supply-chain transparency and corrective action "
            "requirements."
        ),
        "notes": (
            "Adversarial review: Foreign manufacturing facility inspection frequency "
            "has lagged domestic inspection frequency; equivalent standards must "
            "be paired with equivalent enforcement capacity. Post-market surveillance "
            "for generic quality is resourced far below what product volume requires; "
            "user fee reform may be necessary to fund adequate surveillance. "
            "Quality failures that result in voluntary recalls may not reach all "
            "patients who received affected product; notification and follow-up "
            "systems must be part of the corrective action framework."
        ),
    },
    "PHRS-0002": {
        "stmt": (
            "Pharmaceutical manufacturers must minimize the use of unnecessary "
            "allergens — including synthetic dyes, common food allergens, and "
            "preservatives with known sensitization risk — in inactive ingredients "
            "of medications where clinically equivalent formulations without "
            "those ingredients are technically feasible. FDA must maintain a "
            "publicly accessible database of inactive ingredient profiles for "
            "all approved drug products. Prescribers and pharmacists must have "
            "access to complete inactive ingredient information to accommodate "
            "patient allergy and sensitivity needs."
        ),
        "notes": (
            "Adversarial review: 'Clinically equivalent formulations without "
            "those ingredients are technically feasible' is a standard subject "
            "to manufacturer argument; the burden of demonstrating infeasibility "
            "must rest with the manufacturer, not with the FDA to demonstrate "
            "feasibility. The existing FDA inactive ingredient database is "
            "incomplete and inconsistently maintained; a funded maintenance "
            "mandate is necessary. Prescriber and pharmacist access to inactive "
            "ingredient information must be integrated into clinical information "
            "systems, not housed in a separate database requiring manual lookup."
        ),
    },
    "PHRS-0003": {
        "stmt": (
            "Pharmaceutical supply chains for all prescription drugs sold in the "
            "United States must be fully traceable from active pharmaceutical "
            "ingredient source through finished product to the point of dispensing. "
            "FDA must maintain a real-time database of supply chain registrations "
            "for all entities in the pharmaceutical supply chain. Supply chain "
            "disruptions, shortages, and quality alerts must be reported to FDA "
            "within 72 hours of identification. FDA must publish supply chain "
            "risk assessments annually for therapeutic categories with identified "
            "concentration or resilience risks."
        ),
        "notes": (
            "Adversarial review: Full supply chain traceability for complex "
            "pharmaceutical supply chains that span multiple countries requires "
            "significant technology investment by manufacturers; implementation "
            "timelines must be realistic but binding, not indefinitely deferred. "
            "Real-time database maintenance requires FDA technical infrastructure "
            "investment that has historically been underfunded; authorization "
            "alone is insufficient without appropriation. Concentration risk "
            "in active pharmaceutical ingredient production (particularly in "
            "China and India) is a national security issue that this rule "
            "addresses from a healthcare access perspective."
        ),
    },

    # ── REBS (NO-STMT) ────────────────────────────────────────────────────────
    "REBS-0001": {
        "stmt": (
            "Rehabilitation facilities and programs — including physical "
            "rehabilitation, cognitive rehabilitation, and substance use "
            "rehabilitation — must meet national minimum standards established "
            "by federal regulation. These standards must include: qualified "
            "clinical staff requirements; minimum hours of active treatment "
            "per week; individualized treatment plan requirements; patient "
            "rights protections; discharge planning standards; and outcome "
            "tracking and reporting. States may set stricter standards but "
            "may not operate facilities below the national minimum."
        ),
        "notes": (
            "Adversarial review: National rehabilitation standards must address "
            "the significant variation in state licensing standards, which has "
            "allowed low-quality facilities to operate in states with weak "
            "regulatory frameworks. Federal preemption of weaker state standards "
            "may face political resistance; the rule must have a legal basis "
            "that survives federalism challenges. Outcome tracking requirements "
            "must include standardized measures that allow cross-facility comparison, "
            "not facility-specific metrics that prevent accountability."
        ),
    },
    "REBS-0002": {
        "stmt": (
            "Rehabilitation treatment provided in covered settings must use "
            "treatment approaches with documented clinical evidence of effectiveness "
            "for the specific condition being treated. Evidence-based treatment "
            "in substance use rehabilitation must include: medication-assisted "
            "treatment (buprenorphine, methadone, naltrexone) where clinically "
            "indicated; cognitive behavioral therapy; motivational interviewing; "
            "and other approaches with SAMHSA or equivalent clinical evidence "
            "support. Facilities that exclude evidence-based treatments on "
            "ideological grounds (e.g., 12-step-only programs that prohibit MAT) "
            "may not receive coverage reimbursement."
        ),
        "notes": (
            "Adversarial review: 12-step programs that prohibit MAT are widespread "
            "and have political support; this provision will face significant "
            "resistance from that community and some in the addiction recovery "
            "advocacy space. The evidence base for MAT is strong; the prohibition "
            "on MAT exclusion must be maintained against political pressure. "
            "Evidence-based treatment requirements must be updated as evidence "
            "develops; static requirements become outdated. Insurance coverage "
            "requirements must align with evidence-based treatment mandates."
        ),
    },
    "REBS-0003": {
        "stmt": (
            "Abusive, coercive, or deceptive practices in rehabilitation programs "
            "are prohibited. Prohibited practices include: unproven 'conversion' "
            "or 'reparative' therapies; wilderness programs that use physical "
            "deprivation or isolation as treatment; 'troubled teen' programs "
            "that use physical restraint, isolation, or behavioral modification "
            "approaches without clinical justification; and any practice designed "
            "to suppress LGBTQ+ identity. Violations are subject to immediate "
            "facility closure and criminal referral for individual practitioners."
        ),
        "notes": (
            "Adversarial review: 'Troubled teen' programs operating in states "
            "with weak oversight have caused documented deaths and serious harm; "
            "federal standards and enforcement authority must supersede weak "
            "state frameworks. Conversion therapy bans face First Amendment "
            "challenges; the rule must be drafted to survive constitutional "
            "scrutiny. Programs that rebrand to avoid existing prohibitions "
            "must be covered by functional definitions of prohibited practices, "
            "not only specific named practices."
        ),
    },
    "REBS-0004": {
        "stmt": (
            "Rehabilitation programs must provide patients and families with "
            "complete, plain-language information about: treatment approaches "
            "and evidence base; staff qualifications and licensing; program "
            "costs including all fees; patient rights including discharge rights; "
            "complaint procedures; facility ownership and any prior regulatory "
            "violations; and outcome data from prior patients in the same "
            "program. This information must be provided before enrollment "
            "and made publicly available. Fees may not be collected before "
            "disclosure is acknowledged."
        ),
        "notes": (
            "Adversarial review: 'Outcome data from prior patients' is a high "
            "transparency standard that most facilities cannot currently meet "
            "because outcome tracking is inadequate; the rule must include "
            "a phased implementation that requires outcome tracking before "
            "requiring outcome disclosure. Facility ownership disclosure is "
            "important given the concentration of rehabilitation programs in "
            "private equity portfolios with documented quality problems. "
            "Prior regulatory violations disclosure must include violations "
            "in other states and under prior ownership."
        ),
    },
    "REBS-0005": {
        "stmt": (
            "Rehabilitation treatment must be physically and geographically "
            "accessible to all who need it regardless of income, insurance "
            "status, geography, disability, language, or immigration status. "
            "Coverage systems must reimburse rehabilitation services without "
            "arbitrary session limits for acute or chronic conditions requiring "
            "ongoing rehabilitation. Federally qualified health centers and "
            "community health centers must be funded to provide rehabilitation "
            "services in underserved areas. Transportation and lodging assistance "
            "must be available for patients who must travel for rehabilitation care."
        ),
        "notes": (
            "Adversarial review: Geographic accessibility requirements must be "
            "paired with infrastructure investment — coverage without providers "
            "is meaningless in underserved areas. Session limit prohibitions for "
            "rehabilitation must be grounded in clinical evidence of ongoing "
            "benefit; unlimited sessions without clinical review are not a "
            "realistic policy design. Transportation assistance programs must "
            "be funded as a coverage component, not as a discretionary social "
            "service subject to annual appropriation."
        ),
    },
    "REBS-0006": {
        "stmt": (
            "Rehabilitation facilities must be subject to regular, unannounced "
            "inspections by state licensing agencies operating under federal "
            "minimum inspection standards. Inspection frequency must be at "
            "least biannual for residential facilities and annual for "
            "outpatient facilities. Inspection records must be publicly "
            "available. Facilities with serious violations must be re-inspected "
            "within 90 days. Persistent violation patterns must trigger "
            "license review and suspension authority. Patient advocates and "
            "ombudspersons must have independent access to facilities."
        ),
        "notes": (
            "Adversarial review: Announced inspections are the dominant model "
            "in most states and predictably miss ongoing violations; unannounced "
            "inspection requirements must be enforced, not waived by state "
            "negotiation with facilities. Patient advocate access to facilities "
            "must be protected against retaliation — patients who report "
            "violations to outside advocates must have specific anti-retaliation "
            "protections. Federal minimum inspection standards must prevent "
            "regulatory race to the bottom among states competing to attract "
            "rehabilitation industry investment."
        ),
    },
    "REBS-0007": {
        "stmt": (
            "Voluntary addiction and substance use treatment must be widely "
            "available, easily accessible, and funded as a public health priority. "
            "Every community must have access to: low-barrier medication-assisted "
            "treatment without mandatory counseling prerequisites; voluntary "
            "residential treatment for those who need it; peer support services; "
            "and harm reduction services including needle exchanges and naloxone "
            "distribution. Stigma-based barriers to treatment access — including "
            "eligibility restrictions based on prior treatment history — "
            "are prohibited."
        ),
        "notes": (
            "Adversarial review: 'Low-barrier MAT without mandatory counseling "
            "prerequisites' is an evidence-based approach that faces significant "
            "political opposition from programs that use mandatory counseling "
            "as a gatekeeping mechanism; this provision must be grounded in "
            "the clinical evidence that mandatory prerequisites reduce treatment "
            "uptake among those who need it most. 'Prior treatment history' "
            "restrictions — rules that bar people who have relapsed from "
            "returning to treatment — are punitive and anti-therapeutic; "
            "the prohibition is essential."
        ),
    },

    # ── RSRS (SHORT-STMT) ─────────────────────────────────────────────────────
    "RSRS-0001": {
        "stmt": (
            "Federal public health and research funding must affirmatively allocate "
            "resources to conditions, medications, and treatment gaps that lack "
            "commercial development incentives but have documented public health "
            "importance. Funding allocations must be reviewed annually against "
            "a disease burden analysis that identifies gaps between research "
            "investment and disease burden. Priority must be given to conditions "
            "with high burden-to-investment ratios; a publicly accountable "
            "priority-setting process must make these allocations transparent "
            "and subject to public input."
        ),
        "notes": (
            "Adversarial review: 'Lack commercial incentives but have public "
            "health importance' must be operationally defined; without a clear "
            "threshold, this standard can be applied to almost any condition. "
            "Annual review against disease burden analysis requires a standardized "
            "burden measurement methodology; the choice of methodology significantly "
            "affects priority rankings. Priority-setting processes are subject "
            "to capture by well-organized advocacy communities for specific "
            "conditions; structural protections for neglected-but-less-vocal "
            "conditions are necessary."
        ),
    },
    "RSRS-0002": {
        "stmt": (
            "Federal research priorities must explicitly include conditions that "
            "have been systematically underfunded relative to their disease burden "
            "due to stigma, commercial unattractiveness, or historical neglect — "
            "including sexually transmitted infections (including HSV, HPV, and "
            "STI vaccine development), chronic conditions disproportionately "
            "affecting low-income populations, substance use disorders, and "
            "medications for which no patent protection creates commercial "
            "development incentive. Annual reporting must track research investment "
            "in these categories relative to disease burden."
        ),
        "notes": (
            "Adversarial review: Explicit enumeration of priority conditions is "
            "a stronger standard than principles-based priority-setting but risks "
            "becoming outdated as disease burden shifts; a mandatory review "
            "and update process for the enumerated list must accompany the "
            "specific mandates. STI vaccine research — particularly for HSV-2, "
            "which affects over 11% of Americans — has been underfunded for "
            "decades due to stigma; the explicit mandate is important and "
            "must be preserved against advocacy to remove it."
        ),
    },
    "RSRS-0003": {
        "stmt": (
            "Healthcare governance and research priority-setting may not allow "
            "commercial market potential or industry promotional activity to "
            "determine public research priorities in ways that systematically "
            "neglect conditions or populations with limited market value. Where "
            "commercial buzz, industry lobbying, or pharmaceutical marketing "
            "creates pressure to redirect public research toward commercially "
            "attractive areas, governance bodies must have structural protections "
            "against this pressure. Public research investment decisions must be "
            "accompanied by a documented analysis of whether they address or "
            "reinforce existing research priority gaps."
        ),
        "notes": (
            "Adversarial review: 'Structural protections against commercial "
            "pressure' in research priority-setting require specific governance "
            "mechanisms — conflict of interest rules, independent committee "
            "composition, transparency in lobbying activities directed at "
            "research priority bodies. 'Documented analysis of whether they "
            "address or reinforce existing gaps' creates an accountability "
            "mechanism for each funding decision; this must be implemented "
            "as a requirement, not merely as guidance."
        ),
    },

    # ── RTTS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "RTTS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Right-to-try access to unapproved treatments "
            "must be grounded in informed consent standards that give patients "
            "meaningful understanding of unproven status and risk; the consent "
            "process must not be a liability waiver dressed as patient empowerment. "
            "Manufacturer obligation to provide access creates a compelled-provision "
            "question; public funding for expanded access programs is preferable "
            "to unfunded mandates on manufacturers. Outcome tracking for "
            "compassionate-use cases is critical for advancing the evidence base."
        ),
    },
    "RTTS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: FDA expanded access pathway timelines must be "
            "specified and enforced; current average processing times for "
            "individual patient IND applications are approximately 4 days for "
            "life-threatening conditions, but emergency cases require faster "
            "mechanisms. The gap between expanded access availability and actual "
            "utilization is significant; clinician unfamiliarity with the pathway "
            "is a known barrier that must be addressed through education and "
            "navigation support. Outcome tracking must not create a disincentive "
            "for manufacturers to participate in expanded access."
        ),
    },
    "RTTS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Coverage of unapproved treatments creates "
            "serious adverse-incentive concerns — if coverage is available "
            "for treatments before FDA approval, manufacturers have reduced "
            "incentive to complete the clinical trial process. Coverage decisions "
            "for experimental treatments must be limited to structured clinical "
            "contexts (trials, registries, expanded access programs) that generate "
            "evidence, not blanket coverage of any unapproved treatment a patient "
            "requests. Financial exploitation of vulnerable, seriously ill patients "
            "by unproven treatment providers must be specifically prohibited."
        ),
    },
    "RTTS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Aggressive commercial marketing of unproven "
            "treatments to seriously ill patients is a documented and recurring "
            "problem; anti-fraud enforcement must target treatments with no "
            "scientific basis, not merely treatments that happen not to have "
            "FDA approval. The distinction between legitimate investigational "
            "treatments and fraudulent quackery requires specific legal criteria "
            "that must be clearly defined. Patient advocacy organizations for "
            "specific conditions sometimes promote unproven treatments; educational "
            "engagement with these communities is necessary alongside enforcement."
        ),
    },
    "RTTS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Informed consent for experimental or unproven "
            "treatments must address the specific vulnerability of seriously ill "
            "patients — hope and desperation significantly affect consent quality. "
            "Consent standards must require specific disclosure of: the treatment's "
            "evidence status; known adverse effects; alternative standard-of-care "
            "options; and any financial relationships between the consenting "
            "clinician and the treatment manufacturer. Independent patient advocates "
            "must be available for consent support in high-stakes decisions."
        ),
    },
    "RTTS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Clinical trial data transparency requirements "
            "must specifically address selective reporting — the practice of "
            "reporting only positive or favorable outcomes from trials while "
            "suppressing negative or null results. Registration of all trials "
            "before enrollment begins (the ClinicalTrials.gov model) is necessary "
            "but not sufficient; mandatory results posting with enforceable "
            "deadlines is also needed. Penalties for non-reporting must be "
            "significant enough to deter non-compliance among well-resourced "
            "pharmaceutical companies."
        ),
    },
    "RTTS-0007": {
        "stmt": None,
        "notes": (
            "Adversarial review: Seriously ill patients in trial waiting queues "
            "may deteriorate or die before gaining access; queue management "
            "must prioritize by medical urgency, not first-come-first-served "
            "or ability to advocate effectively. Diversity in clinical trial "
            "enrollment is a persistent problem — women, racial and ethnic "
            "minorities, elderly patients, and patients with comorbidities "
            "are systematically underrepresented, limiting generalizability "
            "of results. Active recruitment programs for underrepresented "
            "populations must accompany diversity requirements."
        ),
    },
    "RTTS-0008": {
        "stmt": None,
        "notes": (
            "Adversarial review: Pediatric treatment development timelines are "
            "longer and more resource-intensive than adult trials; incentive "
            "structures for pediatric development must be robust enough to "
            "actually drive investment. The existing Best Pharmaceuticals for "
            "Children Act and Pediatric Research Equity Act have improved "
            "pediatric drug labeling but have not resolved all gaps in "
            "pediatric treatment availability; this rule must address "
            "the specific remaining gaps. Off-label pediatric prescribing "
            "should be tracked and reviewed as evidence-generation, not "
            "merely tolerated as a workaround."
        ),
    },
    "RTTS-0009": {
        "stmt": None,
        "notes": (
            "Adversarial review: Rare disease drug development is substantially "
            "supported by the Orphan Drug Act but orphan designations have "
            "been used for conditions that are not truly rare by dividing "
            "common conditions into subtypes; the rule must address 'orphan "
            "drug salami slicing.' Coverage requirements for approved rare "
            "disease treatments must address the extraordinary cost of many "
            "rare disease drugs, which in some cases exceed $1 million per "
            "course of treatment; coverage without cost-containment requirements "
            "is incomplete policy."
        ),
    },
    "RTTS-0010": {
        "stmt": None,
        "notes": (
            "Adversarial review: Global access to drugs developed with U.S. "
            "public research funding raises significant equity questions "
            "that domestic healthcare policy alone cannot fully address; "
            "this rule must acknowledge the international dimension. Technology "
            "transfer agreements for publicly funded drug research must be "
            "structured to enable access, not to enable price discrimination "
            "between high-income and low-income countries. 'Reasonable pricing' "
            "requirements for publicly funded drug research have been "
            "intermittently used in NIH licensing; consistent application "
            "requires statutory, not merely administrative, authority."
        ),
    },
    "RTTS-0011": {
        "stmt": None,
        "notes": (
            "Adversarial review: Patient access to treatment records must be "
            "technically practical — FHIR-based interoperability mandates "
            "move in this direction but implementation is incomplete. Prohibitions "
            "on prior authorization barriers for acute or life-threatening "
            "conditions are partially addressed in current law but not uniformly "
            "enforced; this rule must specify enforcement mechanisms, not merely "
            "restate the prohibition. Continuity of care across insurance "
            "transitions — particularly for patients actively receiving "
            "experimental or investigational treatment — must be specifically "
            "addressed."
        ),
    },
    "RTTS-0012": {
        "stmt": None,
        "notes": (
            "Adversarial review: Palliative care access must be addressed as "
            "a right, not a consolation prize for patients who have exhausted "
            "curative options; palliative care concurrent with curative treatment "
            "is evidence-based and must be covered. Transition from curative to "
            "palliative care is a point of significant patient and family distress; "
            "the transition process must include communication support, care "
            "coordination, and family support services. Hospice access restrictions "
            "that require patients to forgo all curative treatment are an "
            "outdated model that should be specifically addressed."
        ),
    },

    # ── RXDG (SHORT-STMT) ─────────────────────────────────────────────────────
    "RXDG-0001": {
        "stmt": (
            "All prescription drugs with demonstrated clinical efficacy for covered "
            "conditions must be available on the universal coverage formulary "
            "without prior authorization for first-line use. Every therapeutic "
            "category of clinical significance must have at least two options "
            "available at Tier 1 (lowest cost-sharing) cost-sharing to patients. "
            "Formulary designs that provide access in name but create cost "
            "barriers that function as de facto exclusions are prohibited. "
            "Formulary changes affecting currently covered patients require "
            "90-day advance notice and transition period."
        ),
        "notes": (
            "Adversarial review: 'Demonstrated clinical efficacy' as a formulary "
            "inclusion standard is appropriate but must include off-label uses "
            "with strong evidence bases; off-label uses supported by FDA-recognized "
            "evidence compendia must be covered as on-label uses. 'At least two "
            "options at Tier 1' must specify that the options address different "
            "patient profiles, not merely that two versions of the same molecule "
            "are available. 90-day notice for formulary changes is insufficient "
            "for patients on long-term treatment for chronic conditions; longer "
            "grandfathering periods for established patients may be required."
        ),
    },
    "RXDG-0002": {
        "stmt": (
            "Cost-sharing for prescription medications must be proportionate to "
            "patient income and must not create barriers to adherence for "
            "clinically necessary medications. Out-of-pocket costs for drugs "
            "treating chronic conditions must be capped at a level that does "
            "not result in documented non-adherence rates above those observed "
            "in zero-cost-sharing conditions. Annual out-of-pocket maximums "
            "must apply to prescription drug costs. For drugs with no therapeutic "
            "alternative, cost-sharing must be eliminated or capped at a "
            "nominal amount regardless of drug cost to the plan."
        ),
        "notes": (
            "Adversarial review: 'Proportionate to patient income' as a cost-sharing "
            "standard requires income-based subsidy mechanisms that are administratively "
            "complex; implementation must include streamlined income verification "
            "without creating coverage gaps. 'Non-adherence rates above those in "
            "zero-cost-sharing conditions' is a measurable standard but requires "
            "reference data; the rule must specify the measurement methodology. "
            "Drugs with no therapeutic alternative are a small category but "
            "include some of the highest-cost medications."
        ),
    },
    "RXDG-0003": {
        "stmt": (
            "Coverage entities operating under the universal healthcare framework "
            "must cover prescription drugs for mental health and substance use "
            "disorders at parity with coverage for equivalent physical health "
            "conditions. Medication-assisted treatment for substance use disorders "
            "(buprenorphine, methadone, naltrexone) must be covered without "
            "prior authorization, session limits, or treatment prerequisite "
            "requirements (including counseling prerequisites). Formulary "
            "placement of mental health and SUD medications may not systematically "
            "disadvantage them relative to equivalent physical health medications."
        ),
        "notes": (
            "Adversarial review: Mental health medication parity in formulary "
            "design is more difficult to verify than benefit parity because "
            "equivalent physical health conditions may not have direct analogues; "
            "the enforcement methodology must be specified. MAT coverage without "
            "prior authorization is critical to low-barrier treatment; any "
            "carve-out (e.g., for high-dose buprenorphine above a threshold) "
            "risks creating a backdoor barrier. Methadone for SUD treatment "
            "has unique dispensing restrictions (daily clinic visits) that "
            "coverage requirements alone cannot fully address."
        ),
    },
    "RXDG-0004": {
        "stmt": (
            "Specialty drug tier pricing that places life-saving medications "
            "in cost-sharing tiers that make them unaffordable for patients "
            "is prohibited. Any prescription medication for which evidence "
            "documents that patients are forgoing treatment or rationing doses "
            "due to cost must be reviewed for tier assignment within 90 days "
            "of evidence publication and reassigned to a tier that eliminates "
            "the documented access barrier. This review may be triggered by "
            "patient complaints, provider reports, or regulatory initiative."
        ),
        "notes": (
            "Adversarial review: The 'specialty tier' structure in Medicare Part D "
            "and commercial insurance places the highest-cost drugs — often for "
            "the most serious conditions — at the highest patient cost-sharing "
            "levels; this is a systematic design flaw with documented patient "
            "harm. 90-day review timelines may be too slow for patients currently "
            "unable to access medications; emergency review procedures for "
            "imminent patient harm must be specified. 'Life-saving' as a threshold "
            "is more restrictive than 'clinically necessary'; the rule should "
            "apply to all clinically necessary medications."
        ),
    },
    "RXDG-0005": {
        "stmt": (
            "Health plans operating under the universal coverage framework must "
            "maintain non-discrimination provisions that prevent formulary design "
            "from systematically discouraging enrollment by people with "
            "specific conditions. Formularies may not place all or nearly all "
            "drugs for a specific condition on the highest cost-sharing tier "
            "while placing drugs for other conditions on lower tiers. Formulary "
            "designs that function as discrimination against specific conditions "
            "or patient populations are subject to civil rights enforcement."
        ),
        "notes": (
            "Adversarial review: ACA Section 1557 anti-discrimination provisions "
            "have been applied to formulary discrimination for HIV medications; "
            "this rule extends the principle. Formulary discrimination claims "
            "require comparator analysis that is technically complex; the "
            "regulatory framework must specify the methodology. Plan operators "
            "who design discriminatory formularies must face consequences that "
            "outweigh the financial benefits of discrimination."
        ),
    },
    "RXDG-0006": {
        "stmt": (
            "Coverage entities must ensure that dispensed medications are "
            "clinically appropriate for each patient's specific characteristics, "
            "including allergies, contraindications, drug interactions, and "
            "comorbidities. Formulary substitution — replacing a prescribed "
            "medication with a formulary alternative — may occur only with "
            "prescriber notification and approval, or patient consent with "
            "full disclosure. Automatic therapeutic substitution without "
            "prescriber involvement is prohibited for medications where "
            "clinical equivalence is not established for the specific patient."
        ),
        "notes": (
            "Adversarial review: Therapeutic substitution practices are common "
            "in many coverage systems and can be appropriate when equivalence "
            "is well-established; the rule must distinguish between appropriate "
            "generic substitution (where bioequivalence is established) and "
            "therapeutic substitution (where clinical equivalence for the specific "
            "patient is assumed but not established). Prescriber notification "
            "requirements must include meaningful clinician awareness, not merely "
            "notification to an overloaded EHR inbox that is practically ignored."
        ),
    },
    "RXDG-0007": {
        "stmt": (
            "Geographic accessibility of prescription medications must be ensured "
            "through pharmacy network adequacy standards equivalent in rigor to "
            "provider network adequacy standards. Pharmacy network standards "
            "must specify maximum distances and travel times to in-network "
            "pharmacy access by geographic classification. Mail-order pharmacy "
            "options must be available for all chronic-condition maintenance "
            "medications, with adequate supply per dispensing. Rural and "
            "underserved areas must have accessible in-person pharmacy options "
            "or pharmacist telepharmacy services."
        ),
        "notes": (
            "Adversarial review: Pharmacy desert problems are documented in rural "
            "communities and urban low-income neighborhoods; network standards "
            "must address both contexts. Mail-order options are available in "
            "most commercial plans but access barriers remain; 'available' must "
            "mean practically accessible, not merely nominally available on a "
            "plan document. Telepharmacy services as a pharmacy desert solution "
            "require state licensure frameworks that vary widely; federal standards "
            "must address this variability."
        ),
    },
    "RXDG-0008": {
        "stmt": (
            "Prescription drug coverage must be equitable across all patient "
            "populations and may not result in systematic disparities in "
            "drug access, cost, or formulary placement by race, ethnicity, "
            "national origin, disability, age, sex, or other protected "
            "characteristics. Coverage entities must monitor, report, and "
            "remediate any identified drug access disparities in their "
            "covered populations annually. Disparities in medication adherence "
            "rates by demographic category are treated as indicators of "
            "systemic coverage barriers requiring investigation and remedy."
        ),
        "notes": (
            "Adversarial review: Drug access disparities are partly driven "
            "by formulary design and partly by clinical prescribing patterns "
            "that are outside coverage entity control; the rule must clearly "
            "delineate what is within the scope of coverage entity responsibility. "
            "Adherence monitoring requires claims data analysis; coverage entities "
            "must have technical capacity to conduct this analysis or contract "
            "with entities that can. Disparities that result from clinical "
            "guideline differences (e.g., different first-line treatment "
            "recommendations) must be distinguished from disparities resulting "
            "from access barriers."
        ),
    },
    "RXDG-0009": {
        "stmt": (
            "The universal healthcare framework must include a mandatory prescription "
            "drug pricing negotiation process for all medications covered under "
            "the system. Drug prices negotiated under the universal system must "
            "reflect international price benchmarks, value-based assessments "
            "of clinical benefit, and domestic production costs. Manufacturers "
            "who refuse to participate in negotiation or charge prices exceeding "
            "negotiated levels are subject to significant excise taxes or "
            "mandatory licensing of the relevant product to generic manufacturers."
        ),
        "notes": (
            "Adversarial review: Drug price negotiation authority is a fundamental "
            "mechanism for addressing the 2-4x U.S. price premium over peer "
            "nations documented by RAND research.<sup><a href=\"#fn5\">[5]</a></sup> "
            "Mandatory licensing as a backstop to negotiation creates a credible "
            "threat that makes negotiation effective; without it, manufacturers "
            "have incentive to hold out. International price benchmarks must "
            "be updated annually; price differentials between the U.S. and "
            "peer nations are not static."
        ),
    },
    "RXDG-0010": {
        "stmt": (
            "Pharmaceutical supply security for the U.S. prescription drug supply "
            "must be maintained through: mandatory domestic or allied-nation "
            "manufacturing capacity for critical medications and active "
            "pharmaceutical ingredients; strategic stockpiles for medications "
            "with documented shortage risk; and early warning systems for "
            "emerging supply disruptions. Critical medication designations "
            "must be based on clinical essentiality and supply chain risk "
            "assessment. Supply security investment must not be used to "
            "justify price increases for affected medications."
        ),
        "notes": (
            "Adversarial review: 'Allied-nation manufacturing capacity' must "
            "specify which nations qualify and under what conditions; the "
            "criterion must be grounded in supply reliability evidence, not "
            "geopolitical classification. Strategic stockpile maintenance has "
            "historically been underfunded and disorganized; the rule must "
            "include mandatory stockpile maintenance standards and independent "
            "auditing. Supply security requirements must address the concentration "
            "of generic API manufacturing in a small number of foreign "
            "facilities as a national vulnerability."
        ),
    },
    "RXDG-0011": {
        "stmt": (
            "Coverage entities must maintain prescription drug formularies that "
            "are consistent, well-documented, and subject to regular evidence "
            "review for clinical currency. Formulary decisions must be made by "
            "independent Pharmacy and Therapeutics committees with majority "
            "clinical membership and conflict-of-interest rules. Formulary "
            "placement decisions must be documented and available for audit. "
            "Annual formulary reviews must include clinical and cost-effectiveness "
            "evidence updates, with documented rationale for all coverage "
            "classifications."
        ),
        "notes": (
            "Adversarial review: P&T committee independence is undermined where "
            "pharmacy benefit managers control formulary placement and rebate "
            "structures; the rule must address PBM conflicts of interest directly. "
            "Rebate arrangements between PBMs and manufacturers create financial "
            "incentives to prefer high-rebate drugs regardless of clinical evidence; "
            "rebate transparency and pass-through requirements must accompany "
            "formulary governance requirements. 'Majority clinical membership' "
            "must specify relevant clinical specialties to prevent administrative "
            "capture of nominally clinical committees."
        ),
    },

    # ── SCIS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "SCIS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Research funding commitments as a share of GDP "
            "must be specified with a clear baseline and enforcement mechanism; "
            "percentage-of-GDP targets without appropriation triggers are "
            "aspirational, not binding. NIH indirect cost rates have been a "
            "political target; the rule should protect research infrastructure "
            "funding while acknowledging the legitimate need for direct-to-research "
            "accountability. Multi-year research funding cycles that match "
            "the actual pace of scientific research are essential but face "
            "annual appropriations cycle constraints."
        ),
    },
    "SCIS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Federal research funding controls through "
            "peer review are well-established but subject to bias in favor "
            "of established researchers and mainstream approaches; structural "
            "support for high-risk/high-reward research (like NIH Director's "
            "Pioneer Award) must be protected and expanded. Peer review quality "
            "depends on reviewer time and expertise; chronic under-resourcing "
            "of review processes reduces quality. 'Independent of commercial "
            "pressure' must address industry-funded supplement grants and "
            "cooperative agreements that nominally pass through NIH."
        ),
    },
    "SCIS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Science funding should be insulated from "
            "political interference in priority-setting and peer review outcomes, "
            "but oversight of how public funds are spent is a legitimate "
            "accountability function; the rule must distinguish between "
            "legitimate oversight and illegitimate political interference "
            "with scientific processes. Congressional appropriations for "
            "specific research areas can both support and distort research "
            "priorities; the framework must address both mechanisms. "
            "Broad public support for medical research funding creates "
            "political durability that should be leveraged, not assumed."
        ),
    },
    "SCIS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Research translation to patient care is a "
            "multi-decade process even under ideal conditions; public expectations "
            "about the pace of medical progress must be managed honestly. "
            "Implementation science — research on how to translate evidence "
            "into clinical practice — is systematically underfunded relative "
            "to basic and clinical research; this gap must be specifically "
            "addressed. Community-based participatory research models that "
            "engage affected communities in research design should be explicitly "
            "supported as part of the translation mandate."
        ),
    },
    "SCIS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Equitable distribution of research infrastructure "
            "requires investment in institutions that serve underrepresented "
            "communities and geographies; the NIH Institutional Development Award "
            "(IDeA) program is the primary existing mechanism but remains "
            "underfunded relative to the geographic disparity in research capacity. "
            "Research workforce diversity programs must address structural "
            "barriers at every career stage, from high school exposure through "
            "faculty appointment; pipeline programs that do not address barriers "
            "at the appointment and tenure stage lose participants at the "
            "critical entry point into sustained research careers."
        ),
    },
    "SCIS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Data sharing requirements for publicly funded "
            "research face resistance from researchers concerned about being "
            "scooped and from institutions concerned about competitive advantage; "
            "incentive structures must make data sharing the path of least resistance. "
            "FAIR data principles (Findable, Accessible, Interoperable, Reusable) "
            "are the correct standard for research data governance; the rule "
            "must specify this standard. Patient data shared for research purposes "
            "must be governed by robust privacy protections that do not make "
            "data sharing impractical for researchers."
        ),
    },
    "SCIS-0007": {
        "stmt": None,
        "notes": (
            "Adversarial review: Scientific communication reform requires "
            "addressing the incentive structure that makes publication in "
            "high-impact journals more career-valuable than well-conducted "
            "research in accessible venues; open access mandates are one "
            "tool but do not alone change these incentives. Article processing "
            "charges for open access publication shift costs to researchers "
            "at institutions with smaller budgets; equitable open access "
            "must address the APC barrier. Misinformation that misappropriates "
            "scientific language must be addressed at the platform and institutional "
            "level, not only at the research output level."
        ),
    },
    "SCIS-0008": {
        "stmt": None,
        "notes": (
            "Adversarial review: Evaluation of emerging technologies (AI diagnostics, "
            "gene therapies, mRNA platforms) requires regulatory frameworks that "
            "are adaptive to novel technologies without abandoning evidence "
            "standards — the history of medical technology adoption is filled "
            "with innovations that were adopted before evidence was available "
            "and caused harm. Adaptive trial designs for novel technologies "
            "require FDA guidance that is keeping pace with technology development; "
            "current FDA guidance lags in some areas. Public engagement in "
            "research priorities for emerging technologies must be institutionalized "
            "to prevent expert and industry capture of priority-setting."
        ),
    },

    # ── STDS (NO-STMT for 0001-0004 and 0009-0013; SHORT-STMT for 0005-0008) ──
    "STDS-0001": {
        "stmt": (
            "Mandatory federal standards for the collection, analysis, and "
            "reporting of healthcare quality data must be established and enforced "
            "across all healthcare settings. Quality measures must be standardized, "
            "evidence-based, and selected through a process independent of "
            "commercial interests in measure performance. Quality data collection "
            "must include: clinical process measures, outcome measures, patient "
            "experience measures, and health equity measures for all major "
            "condition categories. Data must be made publicly available in a "
            "format that enables meaningful comparison."
        ),
        "notes": (
            "Adversarial review: Quality measure selection has been subject "
            "to healthcare industry influence; measures that are easy to game "
            "but not clinically meaningful may be preferred over harder-to-achieve "
            "but more meaningful outcome measures. Healthcare quality data "
            "that does not include demographic stratification cannot identify "
            "care quality disparities; equity measures must be mandatory, not "
            "optional. 'Publicly available in a format that enables meaningful "
            "comparison' requires risk-adjustment methodology to account for "
            "differences in patient populations across providers."
        ),
    },
    "STDS-0002": {
        "stmt": (
            "Healthcare quality standards must be enforced through a combination "
            "of transparency requirements, financial incentives and penalties, "
            "and regulatory action authority. Coverage decisions may incorporate "
            "quality performance requirements for providers and facilities. "
            "Quality-based coverage exclusions must be preceded by a documented "
            "improvement period with specific benchmarks and technical assistance "
            "availability. Persistent quality failures that result in patient "
            "harm must trigger mandatory investigation and corrective action "
            "with enforceable timelines."
        ),
        "notes": (
            "Adversarial review: Pay-for-performance (P4P) programs have mixed "
            "evidence of effectiveness and have in some cases widened equity "
            "gaps by rewarding providers who serve healthier, higher-income "
            "populations; P4P design must address equity implications explicitly. "
            "Quality improvement technical assistance must be specifically "
            "funded and available to safety-net providers who serve the most "
            "complex populations; unfunded mandates will worsen quality disparities. "
            "Corrective action timelines must be calibrated to what is clinically "
            "achievable, not to administrative convenience."
        ),
    },
    "STDS-0003": {
        "stmt": (
            "Healthcare quality standards must apply to all care settings — "
            "not only hospital-based care but also ambulatory surgery centers, "
            "urgent care centers, freestanding emergency departments, skilled "
            "nursing facilities, home health agencies, and telehealth services. "
            "Setting-specific standards must be developed where appropriate "
            "but must be calibrated to the clinical risks of care in each "
            "setting, not to the administrative preferences of setting operators. "
            "Standards for new and emerging care delivery models must be "
            "developed proactively, not reactively after harm is documented."
        ),
        "notes": (
            "Adversarial review: Regulatory arbitrage — operating in settings "
            "with lower quality standards to reduce compliance cost — is "
            "a documented behavior in healthcare; equivalent standards across "
            "settings close this loophole. Ambulatory surgery center quality "
            "standards have historically been weaker than hospital standards "
            "for similar procedures; this disparity creates patient safety risk. "
            "Telehealth quality standards must address the specific risks of "
            "remote care delivery, including diagnostic limitations and "
            "patient identification challenges."
        ),
    },
    "STDS-0004": {
        "stmt": (
            "Quality standards for healthcare information systems — including "
            "electronic health records, clinical decision support systems, "
            "and AI-assisted diagnostic tools — must be established and enforced "
            "to ensure that information technology in healthcare improves, "
            "rather than degrades, care quality and safety. EHR systems must "
            "meet usability standards that minimize clinician administrative "
            "burden. AI diagnostic tools must demonstrate clinical validation "
            "before deployment and must undergo post-market surveillance. "
            "Clinical decision support systems must be based on current "
            "clinical evidence."
        ),
        "notes": (
            "Adversarial review: EHR usability has been a significant source "
            "of clinician burnout and medical error; federal standards for "
            "EHR usability have been weak and have permitted systems that "
            "create safety risks. AI diagnostic tools must be validated on "
            "diverse patient populations that represent their intended use "
            "populations; tools validated on non-representative populations "
            "have demonstrated performance disparities in clinical use. "
            "Post-market surveillance for AI tools requires ongoing evaluation "
            "against real-world outcomes, not one-time pre-deployment validation."
        ),
    },
    "STDS-0005": {
        "stmt": (
            "Healthcare quality standards must include specific measures of "
            "health equity: demographic breakdowns of clinical outcomes, access "
            "measures, and care quality indicators; disparities identified "
            "through equity measurement must be addressed through provider "
            "and system accountability mechanisms. Coverage entities and "
            "providers must monitor and report demographic disparities in "
            "care quality and access. Identified equity gaps must trigger "
            "corrective action requirements, not merely information disclosure. "
            "Equity measures must be included in value-based payment "
            "arrangements with meaningful weight."
        ),
        "notes": (
            "Adversarial review: Health equity measures that are only reported "
            "without enforcement consequences do not change behavior; corrective "
            "action requirements for identified disparities are essential. "
            "Demographic data collection for equity monitoring faces patient "
            "privacy concerns and care team resistance; data collection must "
            "be designed to minimize patient concern while enabling meaningful "
            "monitoring. Value-based payment weight for equity measures must "
            "be sufficient to drive behavior change; nominal weighting creates "
            "compliance-theater without substance."
        ),
    },
    "STDS-0006": {
        "stmt": (
            "Quality standards for maternal healthcare must specifically address "
            "the documented epidemic of maternal mortality and severe maternal "
            "morbidity in the United States, which is the highest among peer "
            "nations and is disproportionately driven by racial disparities "
            "in maternal outcomes.<sup><a href=\"#fn6\">[6]</a></sup> Mandatory quality "
            "standards for obstetric care must include: hemorrhage and sepsis "
            "protocols; maternal mental health screening; implicit bias training "
            "for all obstetric care providers; and mandatory maternal mortality "
            "review processes with corrective action requirements. Racial "
            "disparities in maternal outcomes must be tracked and addressed "
            "as a specific enforcement priority."
        ),
        "notes": (
            "Adversarial review: Maternal mortality review committees exist in "
            "most states but their findings are often confidential and their "
            "corrective action recommendations are frequently not implemented; "
            "the rule must address both transparency and follow-through requirements. "
            "Implicit bias training requirements face evidence questions about "
            "effectiveness; training must be paired with structural changes "
            "to care delivery that do not depend on individual clinician "
            "behavior change alone. Racial disparities in maternal mortality "
            "cannot be fully explained by clinical factors; structural racism "
            "in healthcare systems must be addressed as a quality problem."
        ),
    },
    "STDS-0007": {
        "stmt": (
            "Clinical practice guidelines must be developed through processes "
            "that are independent of commercial interests, evidence-based, "
            "and regularly updated to reflect current evidence. Federal health "
            "agencies must support independent, multi-society development of "
            "evidence-based clinical guidelines. Guidelines used in coverage "
            "decisions must be publicly available, must document evidence "
            "quality for each recommendation, and must be updated when "
            "new evidence materially changes the evidence base. Guidelines "
            "developed with undisclosed industry participation may not be "
            "used in coverage decisions."
        ),
        "notes": (
            "Adversarial review: Many influential clinical guidelines are "
            "developed by medical specialty societies with significant industry "
            "funding and/or committee members with industry financial relationships; "
            "the rule must require disclosure and conflict management that "
            "goes beyond nominal recusal. 'Regularly updated' must mean "
            "triggered by evidence review, not by convenient scheduling; "
            "automated evidence surveillance systems can identify when "
            "existing guidelines may be out of date. Guideline fragmentation — "
            "competing guidelines from different professional bodies giving "
            "different recommendations on the same clinical question — "
            "must be addressed through reconciliation requirements."
        ),
    },
    "STDS-0008": {
        "stmt": (
            "Healthcare quality standards must include specific requirements "
            "for patient safety reporting and learning. Healthcare facilities "
            "must maintain confidential internal safety reporting systems "
            "that protect reporters from retaliation. Adverse events and "
            "near-misses meeting federal definition criteria must be reported "
            "to a federal patient safety database. Patient safety data must "
            "be analyzed for systemic patterns, and identified systemic "
            "safety problems must be addressed through national safety "
            "alerts and practice improvement requirements. Disclosure of "
            "harm to patients must be mandatory."
        ),
        "notes": (
            "Adversarial review: Mandatory adverse event reporting with "
            "confidentiality protections for reporters is the correct design "
            "but the balance between confidentiality and accountability is "
            "difficult; the rule must specify what protections apply and "
            "in what circumstances. Mandatory harm disclosure to patients "
            "faces resistance from risk management concerns; clear legal "
            "protections for clinicians who disclose harm in good faith "
            "are necessary. Patient safety learning databases must be "
            "actively used to drive systemic change, not merely to archive "
            "events."
        ),
    },
    "STDS-0009": {
        "stmt": (
            "Accreditation organizations for healthcare facilities and programs "
            "must meet federal standards for independence, transparency, and "
            "effectiveness. Organizations granted deemed status by federal "
            "agencies must demonstrate that their standards and survey processes "
            "produce equivalent or superior safety and quality outcomes compared "
            "to direct government inspection. Accreditation survey results must "
            "be publicly disclosed. Conflicts of interest between accrediting "
            "organizations and the facilities they accredit must be managed "
            "through structural independence requirements."
        ),
        "notes": (
            "Adversarial review: The Joint Commission has faced documented "
            "questions about whether accreditation-based oversight provides "
            "equivalent safety protection to direct CMS inspection; this rule "
            "must include a performance accountability mechanism for accreditors. "
            "Accrediting organization revenue dependence on the facilities "
            "they accredit creates a structural conflict; the rule must "
            "address this structural relationship. Public disclosure of "
            "accreditation survey results has been resisted by accrediting "
            "organizations; the rule must override this resistance."
        ),
    },
    "STDS-0010": {
        "stmt": (
            "Mandatory standards for infection prevention and control must "
            "be established for all healthcare settings, regularly updated "
            "based on emerging evidence and outbreak response experience, "
            "and enforced through inspection and penalty authority. Infection "
            "prevention standards must address: standard precautions, "
            "transmission-based precautions, environmental cleaning, "
            "hand hygiene, healthcare worker vaccination, and antibiotic "
            "stewardship. Facilities with documented infection control "
            "failures must be subject to mandatory corrective action "
            "and public disclosure."
        ),
        "notes": (
            "Adversarial review: Healthcare-associated infection rates remain "
            "high despite decades of evidence-based guidelines; the gap between "
            "guideline adherence and actual practice is primarily a culture "
            "and accountability problem, not a knowledge problem. Healthcare "
            "worker vaccination mandates face legal and workforce challenges; "
            "the rule must balance workplace rights with patient safety "
            "requirements. Antibiotic stewardship programs have strong "
            "evidence bases but require sustained clinical leadership investment "
            "that must be supported through quality standards and reimbursement "
            "mechanisms."
        ),
    },
    "STDS-0011": {
        "stmt": (
            "Healthcare facilities must meet standards for staffing levels "
            "in all care settings sufficient to ensure safe and effective "
            "care delivery. Mandatory minimum staffing standards must be "
            "established for inpatient facilities with specific nurse-to-patient "
            "ratios by care unit type. Staffing standards must include "
            "qualified staff in sufficient numbers, not merely total staff "
            "regardless of training and role. Staffing violations must be "
            "reported to regulators, disclosed to patients, and addressed "
            "through enforceable corrective action."
        ),
        "notes": (
            "Adversarial review: Mandatory nurse-to-patient ratios have strong "
            "evidence bases from California's experience, where they improved "
            "patient outcomes and nurse retention; the rule should cite this "
            "evidence. Staffing standards must address the full care team, "
            "not only nurses; physician, pharmacist, and support staff "
            "adequacy are also patient safety factors. Healthcare workforce "
            "shortages may create compliance gaps with staffing standards; "
            "workforce investment and immigration pathway reform must accompany "
            "staffing standards."
        ),
    },
    "STDS-0012": {
        "stmt": (
            "Healthcare quality standards must include mandatory readmission "
            "reduction programs for conditions with evidence-based preventable "
            "readmission rates — including heart failure, pneumonia, "
            "hip/knee replacement, and COPD. Readmission reduction programs "
            "must include: adequate transition care coordination; post-discharge "
            "follow-up requirements; patient education standards; and "
            "community health worker engagement where evidence supports "
            "effectiveness. Readmission penalties must not fall disproportionately "
            "on safety-net hospitals serving high-risk populations."
        ),
        "notes": (
            "Adversarial review: Medicare Hospital Readmissions Reduction Program "
            "has documented equity concerns — hospitals serving high-poverty, "
            "high-comorbidity populations receive disproportionate penalties "
            "even after risk adjustment; this rule must address this equity "
            "failure. Readmission rates are partly determined by social "
            "determinants of health that are outside hospital control; "
            "quality standards must distinguish between clinically preventable "
            "readmissions and socially-driven readmissions. Community health "
            "worker programs must be funded as covered benefits, not as "
            "hospital charity care."
        ),
    },
    "STDS-0013": {
        "stmt": (
            "Healthcare facilities must meet accessibility standards for "
            "people with physical disabilities, sensory disabilities, "
            "cognitive disabilities, and communication needs. Accessibility "
            "standards must be updated regularly to reflect current technical "
            "capabilities for accommodation. Language access services — "
            "including qualified medical interpreters for all languages "
            "used by a significant proportion of a service area population "
            "— must be available at no cost to patients in all healthcare "
            "settings. Disability and language access deficiencies must "
            "be treated as quality failures subject to enforcement."
        ),
        "notes": (
            "Adversarial review: ADA compliance in healthcare has been "
            "inadequately enforced; many facilities remain inaccessible to "
            "people with disabilities despite existing legal requirements. "
            "Qualified medical interpreter standards must specify minimum "
            "training and certification, not merely willingness to communicate "
            "in another language; family member and machine translation "
            "are not adequate substitutes for qualified medical interpretation "
            "in high-stakes clinical contexts. Cultural competency standards "
            "must accompany language access requirements; linguistic and "
            "cultural barriers both affect care quality."
        ),
    },

    # ── SUPR (COMPLETE-STMT) ───────────────────────────────────────────────────
    "SUPR-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Supplement industry self-regulation through "
            "DSHEA has produced a market in which products making health claims "
            "regularly do not contain the labeled ingredients or contain "
            "undisclosed adulterants; the rule's mandatory testing requirements "
            "address this failure. Independent testing must be truly independent "
            "— funded by a government-administered pool, not directly by the "
            "companies whose products are being tested. Testing frequency must "
            "be sufficient to deter ongoing violations; random annual testing "
            "creates too many gaps."
        ),
    },
    "SUPR-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: The history of supplement-related medical "
            "emergencies (ephedra, DMAA, liver failure from contaminated "
            "products) demonstrates that post-market surveillance without "
            "pre-market safety requirements is inadequate. FDA authority to "
            "act on adverse events must be paired with rapid response "
            "mechanisms — current procedures for taking unsafe supplements "
            "off the market take months to years, during which patient harm "
            "continues. Mandatory adverse event reporting by manufacturers "
            "must address the systematic underreporting currently documented "
            "in this sector."
        ),
    },
    "SUPR-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Medical claims for supplements are currently "
            "prohibited (only structure/function claims are permitted), but "
            "the line between structure/function and medical claims is routinely "
            "blurred in marketing; enforcement is inadequate. Supplement "
            "marketing to elderly consumers, who are disproportionately targeted "
            "and harmed, must receive specific enforcement attention. The "
            "health claims category must not be expanded; instead, supplements "
            "that can demonstrate therapeutic efficacy should be regulated "
            "as drugs, not as supplements with enhanced claims."
        ),
    },
    "SUPR-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: 'Clear disclosure' requirements for supplement "
            "labels have limited effect if the information is not salient to "
            "consumers; mandatory front-of-label disclosure of evidence status "
            "('No FDA review of these claims') must be prominent, not buried. "
            "Healthcare provider integration into supplement decision-making "
            "requires that providers be knowledgeable about supplement "
            "evidence and interactions, which requires medical education reform. "
            "Provider-patient communication standards for supplement use must "
            "address the cultural and community contexts in which supplement "
            "use is embedded."
        ),
    },
    "SUPR-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Drug-supplement interaction databases must "
            "include interactions with supplements that lack FDA-reviewed "
            "evidence but have documented clinical interaction patterns; "
            "the evidentiary standard for inclusion in a safety database "
            "must be lower than the standard for regulatory action. "
            "Integration into EHR systems requires healthcare information "
            "technology standards that facilitate real-time interaction "
            "checking; this is an HIT policy issue as much as a supplement "
            "safety issue. Supplement use history collection must be "
            "culturally sensitive; patients from communities where herbal "
            "and traditional medicine is normal may be reluctant to "
            "disclose use without a trusting clinical relationship."
        ),
    },
    "SUPR-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: 'Research using proper clinical methodology' "
            "must specify what methodologies are required for what types "
            "of claims; supplement research has historically been of poor "
            "quality because the industry has no regulatory incentive to "
            "fund rigorous trials. NIH should prioritize supplement "
            "research that has potential clinical utility but lacks commercial "
            "development incentive; this is an explicit public goods role. "
            "Independent registry for supplement research must address "
            "publication bias in supplement research, which is particularly "
            "severe because negative results are rarely published."
        ),
    },
    "SUPR-0007": {
        "stmt": None,
        "notes": (
            "Adversarial review: GMP requirements for supplements are currently "
            "required under DSHEA but enforcement is inadequate; the rule "
            "must address enforcement resource requirements, not merely "
            "restate the standard. Supplement industry GMP compliance rates "
            "vary significantly by company size and type; smaller manufacturers "
            "with more limited compliance infrastructure may need technical "
            "assistance, not only penalties. Consumer access to GMP compliance "
            "records should be direct; requiring intermediary searches through "
            "regulatory databases creates practical barriers to informed choice."
        ),
    },
    "SUPR-0008": {
        "stmt": None,
        "notes": (
            "Adversarial review: Supplements targeted at children are particularly "
            "concerning given developmental vulnerability and the tendency to "
            "use candy-like formats that may be consumed without adult supervision. "
            "The rule's prohibition on misleading marketing to children must "
            "address marketing to parents about children's products, not only "
            "direct marketing to children. Children's supplement safety standards "
            "must be age-specific; supplements safe for adults may not be safe "
            "for pediatric populations, and this must be evaluated and disclosed."
        ),
    },
    "SUPR-0009": {
        "stmt": None,
        "notes": (
            "Adversarial review: The herbal medicine and traditional practice "
            "category has significant cultural importance for many communities "
            "and represents a broad spectrum of evidence quality — from well-studied "
            "compounds with real evidence (St. John's Wort, ginkgo) to completely "
            "unstudied traditional uses. The framework must be culturally "
            "respectful while ensuring that commercial exploitation of "
            "traditional practices does not escape safety and evidence standards. "
            "Integration with licensed integrative medicine practitioners "
            "should be explored as a quality assurance mechanism."
        ),
    },
    "SUPR-0010": {
        "stmt": None,
        "notes": (
            "Adversarial review: Transparent supply chains for supplement ingredients "
            "must specifically address adulteration with undisclosed pharmaceutical "
            "compounds — a documented ongoing problem, particularly in weight "
            "loss, sexual enhancement, and sports performance supplements. "
            "Country of origin and supply chain transparency must be extended "
            "to botanical ingredients, which are subject to species substitution "
            "and contamination risks. Consumer access to supply chain information "
            "must be practical — QR code or similar accessible mechanism — "
            "not limited to technically available but practically inaccessible "
            "regulatory databases."
        ),
    },

    # ── TELS (NO-STMT) ────────────────────────────────────────────────────────
    "TELS-0001": {
        "stmt": (
            "Telehealth services provided through covered healthcare must meet "
            "the same clinical standards, professional licensure requirements, "
            "and evidence-based care standards as equivalent in-person services. "
            "Telehealth prescribing of controlled substances and other high-risk "
            "medications must comply with clinical standards developed specifically "
            "for telehealth contexts, including appropriate patient identification "
            "and assessment protocols. Coverage for telehealth services must be "
            "equivalent to coverage for equivalent in-person services without "
            "additional access barriers imposed solely on the basis of telehealth "
            "delivery."
        ),
        "notes": (
            "Adversarial review: Telehealth prescribing of controlled substances "
            "was expanded during COVID-19 and has documented risks of misuse; "
            "standards for telehealth-appropriate prescribing must be based on "
            "evidence from the expanded-access period, not on pre-COVID "
            "assumptions. Coverage parity for telehealth must specifically "
            "address cases where in-person care is not reasonably available; "
            "telehealth cannot substitute for a care system that provides "
            "physical presence where clinically required. Technology access "
            "barriers (broadband, devices, digital literacy) must be addressed "
            "as access barriers, not merely as individual patient characteristics."
        ),
    },
    "TELS-0002": {
        "stmt": (
            "Geographic and technological barriers to telehealth access must "
            "be addressed through: universal broadband deployment to all "
            "residential areas; telehealth device lending programs at healthcare "
            "facilities, libraries, and community centers; plain-language "
            "digital health literacy support; and voice-based telehealth "
            "options for patients who cannot use video. Healthcare providers "
            "offering telehealth services must provide technical assistance "
            "to patients who encounter barriers to access. Patients who "
            "cannot access telehealth due to technology barriers must have "
            "alternative access options."
        ),
        "notes": (
            "Adversarial review: Universal broadband deployment is a federal "
            "infrastructure priority but completion timelines are uncertain; "
            "telehealth access policy cannot wait for full broadband deployment "
            "and must include bridge solutions. Voice-based telehealth is "
            "an important accommodation for elderly and low-income patients "
            "but has clinical limitations for conditions where visual examination "
            "adds value; the rule must specify which telehealth services "
            "may be voice-only and which require video. Technical assistance "
            "obligations must be funded; unfunded mandates to healthcare "
            "providers for patient technology support will be inconsistently "
            "implemented."
        ),
    },

    # ── TRAN (SHORT-STMT) ─────────────────────────────────────────────────────
    "TRAN-0001": {
        "stmt": (
            "Coverage must be continuous and uninterrupted during transitions "
            "between insurance sources — including transitions from employer-sponsored "
            "coverage to public coverage or individual coverage, transitions "
            "due to life events (marriage, divorce, death of a plan holder, "
            "job loss, relocation), and annual open enrollment transitions. "
            "No patient actively receiving treatment for a covered condition "
            "may lose access to that treatment due to an administrative "
            "coverage transition. Coverage transition bridges must be available "
            "without requiring evidence of hardship."
        ),
        "notes": (
            "Adversarial review: Continuous coverage during transitions requires "
            "coordination between the losing and gaining coverage entities; "
            "the rule must specify which entity bears financial responsibility "
            "during the transition period and what information must be shared. "
            "Transitions during active cancer treatment, pregnancy, or psychiatric "
            "crisis are the highest-stakes scenarios; the rule must specifically "
            "address each. 'No patient actively receiving treatment' must be "
            "defined operationally — what counts as 'active treatment' and "
            "who makes that determination must be specified to prevent disputes "
            "that delay coverage."
        ),
    },
    "TRAN-0002": {
        "stmt": (
            "Patients who transition to different coverage during active treatment "
            "for a serious or chronic condition are entitled to continuity of "
            "care protections, including: continuation of the treating provider "
            "relationship at in-network rates for the duration of active "
            "treatment; continuation of ongoing medications without formulary "
            "change disruption for a defined transition period; and continuation "
            "of ongoing care plans without new prior authorization requirements "
            "for covered services that were previously authorized. These "
            "protections must apply to all coverage transitions, whether "
            "voluntary or involuntary."
        ),
        "notes": (
            "Adversarial review: The gaining coverage entity is required to "
            "honor the treating provider relationship at in-network rates "
            "but the provider may not have a contract with the new entity; "
            "the mechanism for establishing temporary in-network rates must "
            "be specified. Formulary change disruption protections must have "
            "a defined duration — indefinite continuation would effectively "
            "prevent formulary management; a 12-month transition period "
            "is the standard in some state laws. 'Active treatment' for "
            "complex psychiatric conditions may span years; the rule must "
            "distinguish between maintenance treatment and active treatment "
            "for the purposes of transition protections."
        ),
    },

    # ── TRLS (SHORT-STMT) ─────────────────────────────────────────────────────
    "TRLS-0001": {
        "stmt": (
            "FDA clinical trial approval and oversight processes must be resourced, "
            "designed, and continuously improved to permit rapid review of "
            "clinical trial applications for conditions of unmet need without "
            "compromising the safety and scientific rigor of trial oversight. "
            "Review timelines must be tracked, publicly reported, and subject "
            "to continuous improvement targets. Adaptive trial design methodologies "
            "that maintain rigor while reducing time-to-completion must be "
            "supported by FDA guidance and staffing. Regulatory burden on "
            "academic and non-commercial trial sponsors must be proportionate "
            "to the actual safety risks being regulated."
        ),
        "notes": (
            "Adversarial review: 'Rapid review without compromising rigor' is "
            "a goal that requires specific process investments — more reviewers, "
            "better information systems, pre-submission meeting programs — "
            "not merely a preference. Regulatory burden proportionate to "
            "safety risk must not be used to create a lower-evidence pathway "
            "for approval; it means reducing administrative burden, not "
            "reducing safety requirements. Non-commercial sponsors (academic "
            "medical centers, NIH) are the primary generators of research "
            "on neglected conditions and cannot bear commercial-scale "
            "regulatory compliance costs; tiered cost-sharing for IND "
            "applications must address this."
        ),
    },

    # ── VACS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "VACS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Vaccine mandates for public institutions face "
            "First Amendment and substantive due process challenges that this "
            "rule must address through careful drafting. The evidence base "
            "for childhood vaccination schedules is strong; this is not "
            "scientifically contested. Exemption systems — medical, religious, "
            "and philosophical — that are administratively easy to obtain "
            "undermine herd immunity; medical exemptions grounded in clinical "
            "evidence are appropriate, but religious and philosophical exemptions "
            "at high rates create measles and other outbreak risks that harm "
            "immunocompromised individuals who cannot be vaccinated."
        ),
    },
    "VACS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Vaccine accessibility barriers — including "
            "cost, insurance coverage gaps, geographic distance, appointment "
            "availability, and language barriers — disproportionately affect "
            "low-income and immigrant communities; addressing these barriers "
            "must be as high a priority as addressing vaccine hesitancy. "
            "Vaccination outreach must be culturally responsive; one-size-fits-all "
            "messaging has documented limitations in communities with specific "
            "historical reasons for healthcare distrust. Free vaccine access "
            "must extend to adults as well as children; adult vaccination "
            "coverage gaps are a significant public health vulnerability."
        ),
    },
    "VACS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: The Vaccine Adverse Event Reporting System "
            "relies on voluntary reporting from clinicians and patients; "
            "mandatory adverse event reporting with defined definitions "
            "and timelines would produce more complete surveillance data. "
            "Vaccine Injury Compensation Program (VICP) responsiveness "
            "is critical to maintaining public trust; backlogs and complex "
            "procedures in VICP that delay compensation for legitimately "
            "injured individuals erode trust in the vaccine program broadly. "
            "Long-term follow-up studies for new vaccine platforms (mRNA) "
            "must be conducted and results made publicly available."
        ),
    },
    "VACS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Vaccine misinformation is amplified by social "
            "media platforms with algorithmic recommendation systems; platform "
            "accountability measures must address recommendation algorithms, "
            "not merely content moderation. 'Communication strategies tailored "
            "to specific hesitancy patterns' requires ongoing research into "
            "hesitancy drivers; this is an active research area with evolving "
            "best practices that must inform program design. Healthcare provider "
            "communication training for vaccine conversations must be evidence-based "
            "and must specifically address the challenge of motivated reasoning "
            "among vaccine-hesitant patients."
        ),
    },
    "VACS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Global vaccine equity involves intellectual "
            "property issues, manufacturing capacity, cold chain infrastructure, "
            "and healthcare system delivery capacity; manufacturing capacity "
            "sharing addresses only one component. COVAX failures during COVID-19 "
            "demonstrated that vaccine equity requires more than funding pledges; "
            "delivery infrastructure and healthcare worker capacity must be "
            "co-investments. Domestic pandemic preparedness must include "
            "vaccine manufacturing surge capacity that can be rapidly scaled; "
            "this is as much a domestic security issue as a global equity issue."
        ),
    },
    "VACS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Annual influenza vaccination program effectiveness "
            "varies with match between circulating strains and vaccine formulation; "
            "universal coverage mandates must be accompanied by investments "
            "in faster-responding vaccine manufacturing platforms. Vaccine "
            "information systems that track coverage across coverage types "
            "and geographies are essential for identifying gaps but require "
            "interoperable data infrastructure that does not currently exist "
            "in all jurisdictions. Patient rights regarding vaccination must "
            "include the right to informed consent and the right to decline "
            "vaccination outside of settings where state-compelled vaccination "
            "is constitutionally justified."
        ),
    },

    # ── WELS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "WELS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Social determinants of health research must "
            "be actionable — research that documents disparities without "
            "generating evidence for interventions that reduce them has limited "
            "public health value. Cross-sector data sharing for SDOH research "
            "raises significant privacy concerns, particularly when health "
            "data is combined with social services, housing, and criminal "
            "justice data; privacy governance must accompany research investment. "
            "Upstream determinants of health (income inequality, housing policy, "
            "education) are outside the healthcare system's direct control; "
            "research findings must be connected to policy actors who can act."
        ),
    },
    "WELS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: 'Health in All Policies' approaches have "
            "been implemented in some jurisdictions but face significant "
            "inter-agency coordination challenges; the rule must include "
            "governance structures that actually enable cross-sector decision-making, "
            "not merely consultation requirements that are easily ignored. "
            "Health impact assessments for major policy decisions require "
            "methodological standards and technical capacity that must be "
            "developed; requiring HIA without providing methodology and capacity "
            "is not an enforceable standard. Community-level wellbeing outcomes "
            "must be co-defined by the communities being studied and served."
        ),
    },
    "WELS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Community-based participatory research has "
            "strong principles but requires sustained funding and institutional "
            "commitment that is difficult to maintain over multi-year research "
            "timelines; the rule must address how CBPR is funded and how "
            "communities maintain meaningful participation as research teams "
            "change. Knowledge translation from CBPR to policy requires "
            "pathways that are often not built into research programs; "
            "the rule must address how community-generated evidence reaches "
            "policymakers. Community control over data generated in their "
            "communities is an emerging principle; data sovereignty provisions "
            "must accompany CBPR requirements."
        ),
    },
    "WELS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Happiness and subjective wellbeing as policy "
            "targets require validated measurement instruments that capture "
            "culturally diverse conceptions of wellbeing; Western wellbeing "
            "constructs may not generalize across populations. GDP and healthcare "
            "expenditure metrics that do not capture wellbeing outcomes can "
            "obscure situations where high spending produces poor wellbeing "
            "outcomes; this is empirically true for U.S. healthcare. "
            "Policy optimization for wellbeing must address the difference "
            "between subjective wellbeing (self-reported happiness) and "
            "objective wellbeing (conditions that enable flourishing); "
            "both are relevant but require different policy interventions."
        ),
    },
    "WELS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Loneliness and social isolation are increasingly "
            "recognized as health risks with effects comparable to smoking; "
            "the evidence base for specific interventions is still developing. "
            "Government programs to reduce loneliness risk undermining individual "
            "agency if not carefully designed; the role of government versus "
            "civil society versus individual action must be clearly delineated. "
            "Community connectivity infrastructure (social spaces, public "
            "transit, community events) has declined due to commercial development "
            "pressures; the rule must address structural drivers of isolation, "
            "not only individual-level interventions."
        ),
    },
    "WELS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Preventive healthcare services coverage must "
            "be evidence-based and USPSTF-grounded; the rule must address "
            "the ongoing litigation around ACA preventive services mandates. "
            "Preventive care coverage without access to the covered services "
            "is meaningless; provider network adequacy for preventive services "
            "in underserved areas must be addressed. The distinction between "
            "preventive services (covered without cost-sharing) and wellness "
            "programs (often employer-sponsored with compliance incentives) "
            "must be maintained; coercive wellness programs that penalize "
            "non-participation create equity and privacy concerns."
        ),
    },

    # ── WMHS (COMPLETE-STMT) ───────────────────────────────────────────────────
    "WMHS-0001": {
        "stmt": None,
        "notes": (
            "Adversarial review: Women's health research funding has historically "
            "been lower per disease burden than research for conditions equally "
            "affecting men or primarily affecting men; mandatory equity in "
            "research funding allocation must be tracked against burden-adjusted "
            "baselines. Women's health research must address conditions that "
            "exclusively or primarily affect women (endometriosis, uterine fibroids, "
            "PCOS) that have been chronically underfunded relative to their "
            "prevalence and impact. The NIH requirement to include women in "
            "clinical trials has improved representation but has not resolved "
            "the gap in sex-disaggregated analysis; the rule must mandate "
            "sex-disaggregated reporting of trial results."
        ),
    },
    "WMHS-0002": {
        "stmt": None,
        "notes": (
            "Adversarial review: Maternal healthcare racial disparities have "
            "been documented for decades without policy intervention producing "
            "equivalent outcomes; the rule must include enforcement mechanisms "
            "that create accountability for persistent disparities. Black women "
            "experiencing pregnancy-related complications are at higher risk "
            "of dismissal by healthcare providers; this is a documented "
            "provider behavior pattern requiring specific clinical training "
            "and accountability interventions. Maternal mortality review "
            "committees must include community representatives and must "
            "publish findings with corrective action requirements."
        ),
    },
    "WMHS-0003": {
        "stmt": None,
        "notes": (
            "Adversarial review: Reproductive healthcare access restrictions "
            "based on political rather than clinical considerations create "
            "documented harms; the rule must specifically protect evidence-based "
            "reproductive healthcare, including contraception, comprehensive "
            "reproductive health services, and abortion access, from politically "
            "motivated restriction under the universal coverage framework. "
            "Access to reproductive healthcare must not be conditioned on "
            "the political decisions of state governments, which vary dramatically "
            "in their legal frameworks for reproductive rights. Comprehensive "
            "sex education is a public health intervention with strong evidence "
            "base that must be supported."
        ),
    },
    "WMHS-0004": {
        "stmt": None,
        "notes": (
            "Adversarial review: Menopause and perimenopause healthcare has "
            "been inadequately covered in medical education; clinician knowledge "
            "gaps are a primary driver of undertreatment. Hormone therapy "
            "evidence has been significantly revised since the WHI study; "
            "updated clinical guidelines must be the basis for coverage decisions "
            "and clinical training. Social and workplace policies that treat "
            "menopause as a private medical condition rather than a workplace "
            "health issue (as the UK has done with 'menopause policies') "
            "contribute to workforce participation barriers for perimenopausal "
            "women."
        ),
    },
    "WMHS-0005": {
        "stmt": None,
        "notes": (
            "Adversarial review: Postpartum mental health conditions — including "
            "postpartum depression, postpartum anxiety, and postpartum psychosis "
            "— are dramatically undertreated; screening is improving but treatment "
            "access remains limited. Mental health coverage parity requirements "
            "must specifically address perinatal mental health to ensure that "
            "formal parity does not mask practical barriers to access. Partner "
            "and family support for postpartum mental health conditions is an "
            "evidence-based component of treatment; coverage for family support "
            "services must be included. Postpartum psychosis is a psychiatric "
            "emergency; access to inpatient care without prior authorization "
            "barriers is essential."
        ),
    },
    "WMHS-0006": {
        "stmt": None,
        "notes": (
            "Adversarial review: Violence against women research and prevention "
            "is funded through VAWA and other mechanisms but implementation "
            "is fragmented across sectors; the healthcare system's role in "
            "identification, safety planning, and referral must be specifically "
            "defined. Intimate partner violence screening in healthcare settings "
            "must be accompanied by robust referral pathways; screening without "
            "effective response can re-traumatize survivors who disclose. "
            "Violence prevention programs in healthcare must be co-designed "
            "with survivors and survivor advocacy organizations to ensure "
            "they address actual barriers to safety."
        ),
    },
}

# ── Transform logic ──────────────────────────────────────────────────────────

with open(HTML_PATH, encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

changed = 0
for card in soup.select("div.policy-card.status-missing"):
    card_id = card.get("id", "")
    parts = card_id.split("-")
    if len(parts) < 3:
        continue
    key = parts[1] + "-" + parts[2]

    classes = card.get("class", [])
    if "status-missing" in classes:
        classes.remove("status-missing")
    if "status-included" not in classes:
        classes.append("status-included")
    card["class"] = classes

    badge = card.select_one(".status-badge")
    if badge and badge.get_text(strip=True) == "Proposed":
        badge.string = "Included"

    content = CARD_CONTENT.get(key, {})

    if content.get("stmt"):
        stmt_el = card.select_one(".rule-stmt")
        if stmt_el:
            stmt_el.clear()
            stmt_el.append(BeautifulSoup(content["stmt"], "html.parser"))
        else:
            plain_el = card.select_one(".rule-plain")
            if plain_el:
                new_stmt = soup.new_tag("p", attrs={"class": "rule-stmt"})
                new_stmt.append(BeautifulSoup(content["stmt"], "html.parser"))
                plain_el.insert_after(new_stmt)

    if content.get("notes") and not card.select_one(".rule-notes"):
        new_notes = soup.new_tag("p", attrs={"class": "rule-notes"})
        new_notes.string = content["notes"]
        card.append(new_notes)

    changed += 1

print(f"Transformed {changed} cards.")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Done. HTML written.")
