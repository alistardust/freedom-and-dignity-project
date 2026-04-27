#!/usr/bin/env python3
"""Backfill plain_language for all 323 HLTH positions in DB and HTML."""

import re
import sqlite3
import subprocess
from pathlib import Path

REPO = Path(__file__).parent.parent
HTML_FILE = REPO / "docs/pillars/healthcare.html"
DB_FILE = REPO / "policy/catalog/policy_catalog_v2.sqlite"

# fmt: off
PLAIN_LANGUAGE: dict[str, str] = {
    # ACCS – Healthcare access eligibility
    "HLTH-ACCS-0001": "Health coverage would be guaranteed to all U.S. citizens and people who have lived here long-term. Residency status alone would not be grounds for denying care.",
    "HLTH-ACCS-0002": "Planned, non-urgent procedures would be available only to people who live in the country. Emergency care would remain available to everyone regardless of where they live.",
    "HLTH-ACCS-0003": "People with severe or life-threatening conditions would receive full coverage for necessary care even if they do not meet ordinary residency requirements.",

    # ADTX – Addiction treatment
    "HLTH-ADTX-0001": "All addiction treatment centers that accept insurance or federal money would need to meet federal safety and quality standards, and prove they use evidence-based treatments. Paying someone to steer a vulnerable patient to a high-profit center would become a serious federal crime.",
    "HLTH-ADTX-0002": "Doctors could prescribe proven addiction medications like buprenorphine without navigating extra regulatory hurdles, and all insurance plans would have to cover FDA-approved addiction treatments without requiring prior approval first. This removes the biggest barriers keeping people with opioid addiction from getting the most effective help available.",
    "HLTH-ADTX-0003": "A permanent federal fund of at least $10 billion a year would support addiction treatment services, with priority given to rural areas and communities hit hardest by overdose deaths. States would be required to show the money is actually reaching people who need it.",

    # AINL – AI in healthcare
    "HLTH-AINL-0001": "AI tools used in healthcare would be treated as high-risk technology, meaning they would have to meet strict safety and accountability standards before being used with patients.",
    "HLTH-AINL-0002": "AI can help doctors, but it cannot replace them. Licensed medical professionals must remain in charge of diagnosing patients and deciding on treatment.",
    "HLTH-AINL-0003": "AI can help a doctor think through options, but cannot make the final call. Any AI used in clinical settings must support—not replace—a physician's own judgment.",
    "HLTH-AINL-0004": "Before an AI tool can be used with real patients, it must have solid proof that it is safe, works as claimed, and does not treat some patient groups less fairly than others.",
    "HLTH-AINL-0005": "Once deployed, AI systems in healthcare must be continuously watched for errors, bias, and harmful outcomes—not just tested once before launch.",
    "HLTH-AINL-0006": "AI cannot independently diagnose a patient or prescribe treatment on its own. A qualified human must always be in the loop and accountable for those decisions.",
    "HLTH-AINL-0007": "An insurer's AI system cannot be used to deny, restrict, or cut off medically necessary care. Any denial must be made by an independent human reviewer, not an algorithm.",
    "HLTH-AINL-0008": "When a human reviewer is required to check an AI decision, they must genuinely think it through themselves—they cannot simply rubber-stamp whatever the AI recommended.",
    "HLTH-AINL-0009": "AI can be used to speed up approvals for care, but it cannot be the primary reason care is denied. Denials still require independent human clinical review.",
    "HLTH-AINL-0010": "A human reviewer must look at a case before any care is denied—decisions cannot be delegated to an appeal process after the fact.",
    "HLTH-AINL-0011": "Insurers cannot use the fact that an AI system did not flag or recommend a treatment as a basis for denying it.",
    "HLTH-AINL-0012": "Every denial of care must be based on an independent clinical evaluation, not just the absence of AI support or an algorithm's output.",
    "HLTH-AINL-0013": "AI systems that help process care requests must be monitored to ensure they are not systematically making it harder for certain groups of patients to get approved.",
    "HLTH-AINL-0014": "Care requests that an AI did not highlight must still receive timely human review—patients should not be deprioritized just because an algorithm did not flag their case.",
    "HLTH-AINL-0015": "AI systems that sort and prioritize care requests must be explainable and subject to oversight—black-box triage that affects patient care is not allowed.",
    "HLTH-AINL-0016": "Insurers cannot use AI systems to cut costs by overriding what patients' doctors say they need. Saving money cannot take priority over patient health outcomes.",
    "HLTH-AINL-0017": "When an AI system influences a coverage decision, patients and their doctors have the right to a clear explanation of how that decision was made and the ability to appeal it.",
    "HLTH-AINL-0018": "Patients have the right to receive care from a qualified human provider and cannot be forced to use AI-only care pathways as their only option.",
    "HLTH-AINL-0019": "Patients must be told when AI is being used in their care and must be able to opt out where that is feasible.",
    "HLTH-AINL-0020": "Healthcare data used by AI systems must be treated as highly sensitive and protected with strict safeguards against misuse, sharing, or unauthorized access.",
    "HLTH-AINL-0021": "A patient's healthcare data cannot be used by AI systems for advertising, commercial profiling, or any purpose unrelated to their care.",
    "HLTH-AINL-0022": "The data used to train AI healthcare tools must have been collected legally, ethically, and with proper consent from patients.",
    "HLTH-AINL-0023": "If an AI healthcare system is uncertain or encounters a situation outside its training, it must fail safely and hand off to a qualified human provider rather than improvising.",
    "HLTH-AINL-0024": "AI tools used in clinical settings must not present their outputs as more certain than they actually are, since false confidence can lead to serious medical errors.",
    "HLTH-AINL-0025": "AI systems used in healthcare must be regularly tested to ensure they do not perform worse for patients based on race, gender, income, or other characteristics.",
    "HLTH-AINL-0026": "Healthcare AI cannot be deployed in ways that make existing gaps in access or quality worse for underserved communities.",
    "HLTH-AINL-0027": "AI can be used to accelerate medical research and drug development, as long as it meets the same safety, transparency, and ethics standards applied to traditional research.",
    "HLTH-AINL-0028": "Federal research funding would be directed toward conditions and treatments that have been historically overlooked or underfunded relative to how many people they affect.",
    "HLTH-AINL-0029": "Government research priorities must include common but underfunded diseases—not just conditions that attract the most commercial investment.",
    "HLTH-AINL-0030": "Rules about which AI tools are allowed in healthcare must be based on transparent, evidence-based science, free from commercial or political pressure.",
    "HLTH-AINL-0031": "AI must be brought into healthcare systems in ways that maintain safety, clear accountability, and continuity of care for patients.",
    "HLTH-AINL-0032": "Healthcare AI systems should be designed to share data across systems in ways that are useful for patients, while fully protecting privacy and security.",

    # APLS – Appeals
    "HLTH-APLS-0001": "When a patient's coverage is denied or a service is refused, they and their doctor must have access to a fast, meaningful, and genuinely independent appeal process.",
    "HLTH-APLS-0002": "If a delay in coverage could harm or worsen a patient's condition, the appeal must be resolved fast enough to prevent that harm—urgency must be factored into the timeline.",
    "HLTH-APLS-0003": "An independent reviewer—not someone connected to the insurer that issued the denial—must be available to review disputed coverage decisions.",
    "HLTH-APLS-0004": "When an appeal is won, the insurer must examine the pattern of similar denials, and face penalties if the same unjustified denial is happening repeatedly.",

    # CLMS – Climate and health
    "HLTH-CLMS-0001": "Health coverage systems would be required to cover conditions caused or worsened by climate change, including heat-related illness, respiratory disease from air pollution, and diseases spread by insects moving into new regions as temperatures rise.",

    # COVR – Coverage rules
    "HLTH-COVR-0001": "There would be one standard of healthcare coverage for everyone—no tiered system where wealthier people get access to better care.",
    "HLTH-COVR-0002": "Everyone would be enrolled in the same health plan, eliminating the complexity of multiple competing insurance options with different levels of coverage.",
    "HLTH-COVR-0003": "The government would take over health insurance through a single national plan, ending the private insurance system for covered services.",
    "HLTH-COVR-0004": "Stricter rules would cap how often and why insurers can say no to coverage or services, making it harder for insurance companies to deny necessary care.",
    "HLTH-COVR-0005": "While the country moves toward universal healthcare, the insurance system would be overhauled to reduce the frequency of denials, delays, and gaps that leave people without covered care.",
    "HLTH-COVR-0006": "Insurers would be required to make coverage and prior authorization decisions within set time limits, so patients are not left waiting indefinitely for decisions.",
    "HLTH-COVR-0007": "When coverage is denied, the appeals process would be fast enough to prevent patients from going without care while waiting for a decision.",
    "HLTH-COVR-0008": "Insurers would be required to cover more medicines, procedures, and treatments that are medically necessary, reducing the number of things patients must pay for out of pocket.",
    "HLTH-COVR-0009": "Insurance companies could not refuse to cover someone because of a health condition they already had—these protections would be permanent and harder to roll back.",
    "HLTH-COVR-0010": "Coverage requirements would expand to include conditions that have historically been ignored or underfunded by insurers, such as obesity and related care.",
    "HLTH-COVR-0011": "Health plans would be required to cover mental health treatment, including talk therapy, on equal terms with physical healthcare.",
    "HLTH-COVR-0012": "Where the evidence supports it and the law allows it, coverage would include psychedelic-assisted therapy administered under appropriate medical supervision.",
    "HLTH-COVR-0013": "Health plan networks would work everywhere in the country, not just in the region where someone enrolled—patients could see doctors in any state without penalty.",
    "HLTH-COVR-0014": "Health savings accounts (HSAs) and similar spending tools would be available to everyone, not just people enrolled in high-deductible insurance plans.",
    "HLTH-COVR-0015": "Employers could not meet their coverage obligations by offering only high-deductible health plans, which shift large costs onto employees before insurance kicks in.",
    "HLTH-COVR-0016": "Employers would be required to pay the full cost of employees' health insurance premiums, with defined exceptions and support for small businesses.",
    "HLTH-COVR-0017": "Coverage or services could not be denied, restricted, or delayed except through a fair, transparent process based on real medical evidence and individual circumstances.",
    "HLTH-COVR-0018": "Every denial of coverage must be based on clear medical standards applied to the individual patient's situation—blanket exclusions and automated denials would not be enough.",
    "HLTH-COVR-0019": "Insurers would be required to publicly report how often they deny claims, what those patterns look like, and how often denials are reversed on appeal.",
    "HLTH-COVR-0020": "Insurers that repeatedly deny medically necessary care without justification would face penalties, corrective action requirements, and potentially lose the ability to participate in public programs.",
    "HLTH-COVR-0021": "All coverage systems would be required to cover a broad floor of essential care—preventive, acute, chronic, reproductive, mental health, and disability-related services.",
    "HLTH-COVR-0022": "Coverage exclusions would have to be written precisely—vague language that effectively blocks necessary care would not be allowed.",
    "HLTH-COVR-0023": "Coverage rules would be written in clear language, and whenever the meaning is unclear, it would be interpreted in favor of the patient getting care.",
    "HLTH-COVR-0024": "Coverage systems would be required to include treatments, medications, and diagnostics that are supported by evidence and appropriate for a patient's individual situation.",
    "HLTH-COVR-0025": "Protections against being denied coverage for pre-existing conditions would be made permanent and explicitly resistant to being weakened or removed.",
    "HLTH-COVR-0026": "Insurance companies could not find workarounds to discriminate against people with pre-existing conditions through pricing, network design, or other indirect tactics.",
    "HLTH-COVR-0027": "Required coverage would expand to include conditions historically denied or stigmatized by insurers, such as obesity, chronic pain, and sexually transmitted infections.",
    "HLTH-COVR-0028": "Mental healthcare—including therapy, psychiatric care, crisis services, and longer-term treatment—would be covered on equal terms with physical healthcare.",
    "HLTH-COVR-0029": "Insurers could not make mental healthcare harder to access than physical healthcare through narrower networks, stricter utilization controls, or other tactics.",
    "HLTH-COVR-0030": "Where evidence and law support it, coverage would include therapies like psychedelic-assisted treatment under proper medical supervision.",
    "HLTH-COVR-0031": "All health plans would be required to cover preventive care at no cost to the patient—including annual physicals, cancer screenings, and mental health screenings.",
    "HLTH-COVR-0032": "Weight management services—including nutrition counseling, supervised programs, FDA-approved medications, and surgery when clinically indicated—would be covered as preventive care.",
    "HLTH-COVR-0033": "Coverage would include annual mental wellness visits with a licensed professional, separate from treatment visits, to support ongoing wellness and early identification of concerns.",
    "HLTH-COVR-0034": "When a licensed psychiatrist or psychologist documents that a physical condition causes severe mental or emotional distress that significantly impairs daily functioning, procedures addressing that condition would be covered.",
    "HLTH-COVR-0035": "Chronic pain lasting three or more months would be covered as a primary medical condition, not just managed with opioid prescriptions. Coverage would include pain specialists, physical therapy, and non-opioid treatments.",
    "HLTH-COVR-0036": "For people with chronic conditions, coverage would include care focused on improving daily function and quality of life—not just emergency and acute care.",
    "HLTH-COVR-0037": "Medicare for All would be established by law as a guaranteed benefit for every U.S. resident, with no premiums, copays, or deductibles.",

    # CRNS – Chronic conditions / Long COVID
    "HLTH-CRNS-0001": "Post-viral conditions like Long COVID would be classified as chronic conditions requiring ongoing medical care and coverage, not dismissed as temporary or unverifiable.",
    "HLTH-CRNS-0002": "People with chronic post-viral conditions would be covered for occupational therapy, assistive devices, workplace accommodations, and vocational rehabilitation to help them return to work and daily life.",
    "HLTH-CRNS-0003": "Medicaid would be required to cover home- and community-based services—like personal care and home health aides—as a guaranteed entitlement with no waiting lists.",
    "HLTH-CRNS-0004": "All direct care workers employed at Medicare- or Medicaid-funded facilities would receive a federal minimum wage floor, ensuring they are paid fairly for essential work.",
    "HLTH-CRNS-0005": "For-profit nursing homes and long-term care facilities receiving Medicare or Medicaid money could not pay out dividends or management fees to investors while using that public funding.",

    # CSTS – Cost-sharing
    "HLTH-CSTS-0001": "Deductibles and copays could not be set so high that they effectively block people from using their coverage—the point of insurance is to make care accessible.",
    "HLTH-CSTS-0002": "Rules about cost-sharing would be regulated to protect patients from financial shocks, care delays, and being priced out of treatments they technically have coverage for.",
    "HLTH-CSTS-0003": "Health savings tools would be widely available so more people can pay for care in a tax-advantaged way, without being required to be in a high-deductible plan.",
    "HLTH-CSTS-0004": "Cost-sharing structures could not be designed in ways that discourage people from getting care for chronic conditions, disabilities, or preventive treatments.",

    # DENT – Dental in Medicare
    "HLTH-DENT-0001": "Traditional Medicare would be required to cover dental care for the first time, including preventive cleanings, fillings, root canals, and dentures. Today, most seniors must pay entirely out of pocket for dental care.",

    # DISS – Health disparities
    "HLTH-DISS-0001": "All federally funded clinical trials would be required to include racial, ethnic, and gender minorities in numbers large enough to produce meaningful results for those communities.",
    "HLTH-DISS-0002": "Dedicated federal funding would go toward understanding and reducing the alarming gap in pregnancy-related death rates between Black women and white women.",
    "HLTH-DISS-0003": "Research into LGBTQ+ health disparities would be funded and expanded, and federal health data collection would be required to include sexual orientation and gender identity.",
    "HLTH-DISS-0004": "Federal funding would increase for research into Native American and Alaska Native health disparities, with genuine respect for tribal sovereignty in health policy decisions.",
    "HLTH-DISS-0005": "Asian Americans and Pacific Islanders would no longer be lumped together in health data—separate data collection would make health disparities across these diverse communities visible.",
    "HLTH-DISS-0006": "Federal research would increase into the structural factors—housing, income, education, neighborhood conditions—that drive health disparities more than individual behavior or genetics.",

    # DNTS – Dental and vision coverage
    "HLTH-DNTS-0001": "Dental care—including cleanings, fillings, gum disease treatment, and oral surgery—would be part of the required coverage floor, not an optional add-on.",
    "HLTH-DNTS-0002": "Vision care—including routine eye exams and corrective lenses—would be part of the required coverage floor, not a separate optional benefit.",

    # DRUG – Drug pricing
    "HLTH-DRUG-0001": "Medicare would be required to negotiate prices directly with pharmaceutical companies for all drugs it covers, not just a small list. This is how the VA already operates and it produces much lower prices.",
    "HLTH-DRUG-0002": "Insulin, epinephrine auto-injectors, naloxone, and other essential medicines could not be priced above what other wealthy countries pay for the same drugs.",
    "HLTH-DRUG-0003": "Pharmacy benefit managers (PBMs)—the middlemen who negotiate drug prices—would have to pass every dollar of manufacturer rebates directly to patients to reduce their out-of-pocket costs.",
    "HLTH-DRUG-0004": "Americans would be allowed to safely import prescription drugs from Canada and other comparable countries, where the same medications often cost a fraction of the U.S. price.",
    "HLTH-DRUG-0005": "Drug companies could not pay competitors to delay releasing generic versions of their drugs. These pay-for-delay deals would be treated as illegal antitrust violations.",
    "HLTH-DRUG-0006": "Drug manufacturers seeking FDA approval would be required to publicly disclose their full research, development, and marketing costs, so the public can assess whether prices are justified.",

    # EMPS – Employer-based coverage
    "HLTH-EMPS-0001": "Employers could not fulfill their healthcare obligation by offering only high-deductible plans that shift large costs to workers before any coverage kicks in.",
    "HLTH-EMPS-0002": "Employers would be required to pay the full cost of workers' health insurance premiums, with defined exceptions and support for small businesses.",
    "HLTH-EMPS-0003": "Small businesses would receive government subsidies or other supports to help them provide health coverage without threatening their financial stability.",
    "HLTH-EMPS-0004": "During any transition period, employer coverage rules would be written to prevent nominal plans that look like coverage but leave workers effectively uninsured.",

    # EMSS – Emergency care
    "HLTH-EMSS-0001": "Emergency medical care would be free for everyone at the point of service—no one would face a bill for going to the emergency room in a crisis.",
    "HLTH-EMSS-0002": "Emergency coverage would include ambulance transportation and necessary follow-up care after an emergency, not just the initial visit.",
    "HLTH-EMSS-0003": "Hospitals and providers could not bill patients more than their normal cost-sharing amount for emergency or surprise out-of-network care. The practice of 'balance billing'—sending large unexpected bills after emergency visits—would be banned nationwide.",

    # HOSP – Hospital market conduct
    "HLTH-HOSP-0001": "Hospitals and health systems could not include non-compete clauses in physician employment contracts. Doctors would be free to practice medicine anywhere after leaving a job without geographic restrictions.",
    "HLTH-HOSP-0002": "When hospitals seek to merge and would control more than 30% of a local market, they would face enhanced antitrust review and be required to maintain services and cap price increases as a condition of approval.",

    # HRGS – Hearing care coverage
    "HLTH-HRGS-0001": "Medicare and Medicaid would be required to cover prescription hearing aids and audiological services for beneficiaries with documented hearing loss—not just the over-the-counter aids now available for mild cases.",
    "HLTH-HRGS-0002": "Medicare and Medicaid would cover cochlear implants and other implantable hearing devices for all patients who meet audiological criteria, with prior authorization required to be resolved within five days.",

    # HSPC – Hospice care
    "HLTH-HSPC-0001": "Hospice providers could not discharge a patient simply because they were becoming expensive or nearing the Medicare spending cap. Discharge must be based on medical grounds, not financial ones.",
    "HLTH-HSPC-0002": "All Medicare-certified hospice providers would be required to maintain minimum staffing levels—including nursing and social work—to ensure patients receive consistent, quality end-of-life care.",
    "HLTH-HSPC-0003": "All Medicare-certified hospice providers would have to fully disclose their ownership structure, including private equity ownership chains, so the public can see who profits from hospice care.",
    "HLTH-HSPC-0004": "The physician certifying that a patient is terminal—which is required for hospice enrollment—must be independent and not financially connected to the hospice provider.",
    "HLTH-HSPC-0005": "Hospice providers would be required to be capable of providing around-the-clock nursing care during medical crises, and have access to inpatient hospice care when needed.",

    # JUSS – Justice and healthcare
    "HLTH-JUSS-0001": "People who are incarcerated have a constitutional right to healthcare that meets community standards of care. Jails and prisons must provide timely access to medical treatment, mental health care, and prescription medications.",

    # LCDS – Long COVID
    "HLTH-LCDS-0001": "Medicare and Medicaid would cover care at Long COVID multidisciplinary clinics, including care coordination, specialist visits, physical therapy, and cognitive rehabilitation. Long COVID would also be recognized as a qualifying disability under the ADA and Social Security.",
    "HLTH-LCDS-0002": "The NIH would be required to maintain a dedicated Long COVID research program funded at no less than $500 million annually, focused on finding biomarkers, understanding mechanisms, and identifying effective treatments.",

    # LTSS – Long-term services and supports
    "HLTH-LTSS-0001": "Federal law would set minimum nurse staffing ratios for all nursing homes that receive Medicare or Medicaid funding. Operators who repeatedly understaff would face criminal liability, not just fines.",
    "HLTH-LTSS-0002": "Medicaid would be required to cover home- and community-based services for all eligible people as a guaranteed entitlement—no waiting lists would be allowed.",
    "HLTH-LTSS-0003": "Home health aides and personal care workers paid through Medicaid would earn a minimum of $25 per hour with full benefits, equal to what equivalent workers earn in nursing facilities.",
    "HLTH-LTSS-0004": "Congress would address the elder care worker shortage through new immigration pathways for care workers, student loan forgiveness for direct care staff, and integration with paid family and medical leave policies.",

    # MATS – Maternal health
    "HLTH-MATS-0001": "Every state would be required to maintain a maternal mortality review committee that investigates all pregnancy-related deaths, with results reported publicly and broken down by race to make disparities visible.",
    "HLTH-MATS-0002": "Coverage would include doulas, certified midwives, and at least 12 months of postpartum care—expanding beyond the current standard of one visit six weeks after delivery.",

    # MHCS – Mental health and AI
    "HLTH-MHCS-0001": "Mental healthcare must be covered as a core part of any health plan, not treated as optional or secondary to physical care.",
    "HLTH-MHCS-0002": "AI systems used in mental health settings would be regulated as high-risk because mistakes can affect safety, privacy, and a person's access to essential care.",
    "HLTH-MHCS-0003": "AI cannot replace licensed mental health clinicians for high-stakes decisions like diagnosis, crisis assessment, or involuntary treatment. A real professional must always make those calls.",
    "HLTH-MHCS-0004": "AI cannot be the sole decision-maker in suicide risk assessment or mental health crisis response. A qualified human must always be in the loop.",
    "HLTH-MHCS-0005": "A clearly identified licensed professional must remain personally accountable for any high-risk mental health decision that involved an AI system.",
    "HLTH-MHCS-0006": "AI can be a helpful tool in mental healthcare, but only where it supports—rather than stands in for—qualified clinical judgment.",
    "HLTH-MHCS-0007": "AI tools used in mental health care must have strong, peer-reviewed evidence that they are safe, effective, and unbiased before they can be deployed.",
    "HLTH-MHCS-0008": "Mental health AI systems must be continuously monitored after launch for harmful outcomes, bias, and failure modes—not just approved once and left unchecked.",
    "HLTH-MHCS-0009": "Apps and AI tools marketed for mental health support could not pretend to be human therapists or build false impressions of a human relationship.",
    "HLTH-MHCS-0010": "AI tools marketed for mental health support could not be designed to create emotional dependency or compulsive usage in people seeking help.",
    "HLTH-MHCS-0011": "Any AI system offering mental health support must clearly state that it is not a human and explain its limitations in plain language.",
    "HLTH-MHCS-0012": "Children and teenagers using AI tools that offer emotional or behavioral support would have extra protections, given their vulnerability to influence and manipulation.",
    "HLTH-MHCS-0013": "Mental health AI systems must be able to connect users to human crisis resources or emergency services when the system detects serious risk—not try to handle crises on its own.",
    "HLTH-MHCS-0014": "AI in crisis support settings must not offer false reassurance or act more certain than it is—incorrect confidence in a mental health emergency can cost lives.",
    "HLTH-MHCS-0015": "If a mental health AI system encounters something beyond its capabilities, it must direct the user to a human rather than improvising an unsupported response.",
    "HLTH-MHCS-0016": "Information shared with AI mental health tools must be treated as highly sensitive health data, with strong privacy protections equivalent to clinical records.",
    "HLTH-MHCS-0017": "Mental health data collected by AI tools could not be sold, used for advertising, or used to build commercial profiles of users.",
    "HLTH-MHCS-0018": "Mental health data collected by AI could not be used by employers, insurers, schools, or landlords to deny someone a job, coverage, enrollment, or housing.",
    "HLTH-MHCS-0019": "Users of mental health AI tools must give explicit, informed, and revocable consent for data use—no hidden settings or deceptive consent flows.",
    "HLTH-MHCS-0020": "AI tools cannot claim mental health or therapeutic benefits without scientific evidence that actually supports those specific claims.",
    "HLTH-MHCS-0021": "Mental health AI systems must be evaluated by independent researchers, not just based on the company's own internal testing or marketing.",
    "HLTH-MHCS-0022": "The public must be able to see clear information about the known risks, limitations, and failure modes of AI mental health systems.",
    "HLTH-MHCS-0023": "People must always have the option to access human mental healthcare and cannot be directed to AI-only services because of cost or convenience decisions by payers.",
    "HLTH-MHCS-0024": "AI mental health tools cannot be imposed on people in schools, workplaces, prisons, or benefits systems without strong legal safeguards and voluntary consent.",
    "HLTH-MHCS-0025": "AI tools cannot be used to pressure people into certain behaviors or ideological conformity under the guise of providing mental health support.",
    "HLTH-MHCS-0026": "Schools cannot use opaque AI tools to label, track, or score students' mental health or risk levels without strict legal and scientific oversight.",
    "HLTH-MHCS-0027": "Jails and prisons cannot use AI mental health tools to justify isolating, restraining, or forcing treatment on incarcerated people without rigorous human review and legal protections.",
    "HLTH-MHCS-0028": "Public benefits and disability systems cannot use opaque AI mental health assessments to deny support or override the judgment of licensed clinical evaluators.",
    "HLTH-MHCS-0029": "Insurance companies cannot use AI to deny, delay, or cut back mental health care in ways that override a licensed clinician's judgment without transparent review and an appeal process.",
    "HLTH-MHCS-0030": "AI cannot be used as a substitute for access to licensed mental health care when that care is medically appropriate—it can supplement but not replace.",
    "HLTH-MHCS-0031": "Mental health AI systems must strictly limit how long they retain sensitive personal data and must give users meaningful control, including the ability to delete their information.",
    "HLTH-MHCS-0032": "Data used to train mental health AI systems cannot include sensitive personal disclosures or confidential therapy content that was not obtained with proper consent.",
    "HLTH-MHCS-0033": "Mental health AI systems must clearly define what they can and cannot do, and must not imply they understand patients the way a human clinician would.",
    "HLTH-MHCS-0034": "AI systems cannot use mental health interactions to shape a person's behavior for commercial or institutional goals without their explicit knowledge and consent.",
    "HLTH-MHCS-0035": "Mental health AI systems cannot be connected to surveillance, law enforcement, or intelligence systems to monitor or profile individuals.",
    "HLTH-MHCS-0036": "When AI mental health tools are used in research or experimental settings, they must meet full human subjects research standards, including informed consent and ethics review.",
    "HLTH-MHCS-0037": "Independent research into the effects of AI tools on mental health—especially for children, teenagers, and vulnerable adults—would receive dedicated federal funding.",
    "HLTH-MHCS-0038": "AI systems designed for conversation, emotional interaction, or behavioral guidance could not be marketed or deployed for children under a minimum age, such as eight years old.",
    "HLTH-MHCS-0039": "Age-based restrictions would apply to AI systems that simulate social, emotional, or advisory relationships, with stronger safeguards for younger users.",
    "HLTH-MHCS-0040": "AI tools accessible to minors would be required to limit data collection and restrict the behavioral influence techniques they can use.",
    "HLTH-MHCS-0041": "AI tools could not be sold directly to consumers as standalone mental health treatment—they would only be allowed in clinically supervised settings.",
    "HLTH-MHCS-0042": "In limited circumstances, AI tools could be used for crisis support, but only if they are designed solely to provide immediate help and escalate to human services.",
    "HLTH-MHCS-0043": "Mental health data from licensed therapy sessions or clinical records could not be used to train AI systems without explicit informed consent from the people whose data it is.",
    "HLTH-MHCS-0044": "Using identifiable mental health records to train AI is prohibited unless strict ethical, legal, and consent standards are met.",
    "HLTH-MHCS-0045": "Mental health data collected through AI interactions could not be stored beyond what is strictly necessary without the user's explicit ongoing consent.",
    "HLTH-MHCS-0046": "All training data for mental health AI must be thoroughly de-identified using robust methods, with ongoing safeguards to prevent re-identification.",
    "HLTH-MHCS-0047": "AI systems cannot be designed or used to identify individuals from anonymized mental health data sets.",
    "HLTH-MHCS-0048": "Anyone denied mental health or substance use coverage on worse terms than comparable physical healthcare coverage would have a direct right to sue in federal court, with attorney's fees available.",
    "HLTH-MHCS-0049": "Insurance plans could not require prior authorization, step therapy, or utilization review for emergency psychiatric care or acute crisis stabilization—people in mental health emergencies cannot be made to wait for approval.",

    # MNTL – Mental health system
    "HLTH-MNTL-0001": "Insurance plans could not impose stricter limits on mental health benefits than on physical health benefits. Mental health parity law would be actively enforced with real consequences for violations.",
    "HLTH-MNTL-0002": "The 988 Suicide and Crisis Lifeline would receive at least $1.5 billion annually to ensure every call is answered and that mobile crisis teams are available in every part of the country.",
    "HLTH-MNTL-0003": "Federal investment would fund enough community mental health centers and psychiatric beds to end the nationwide shortage that leaves people in crisis without access to inpatient care.",
    "HLTH-MNTL-0004": "No one could be involuntarily committed to a psychiatric facility for more than 72 hours without a hearing before an independent decision-maker—protecting people's rights while ensuring care.",
    "HLTH-MNTL-0005": "Full federal student loan forgiveness would be available to licensed mental health workers who commit to serving in underserved communities, addressing critical workforce shortages.",

    # NETS – Provider networks
    "HLTH-NETS-0001": "Health plans would be required to maintain adequate networks of providers for all covered services—including specialists and mental healthcare—so covered care is actually accessible.",
    "HLTH-NETS-0002": "Health plan networks would work across the whole country, not just the region where someone enrolled, so people are not stuck without in-network care when they travel or move.",
    "HLTH-NETS-0003": "If a health plan cannot provide adequate in-network care within a reasonable time and distance, the plan would be required to cover out-of-network care at in-network rates.",
    "HLTH-NETS-0004": "Patients cannot be penalized financially for going outside a narrow network when their plan failed to provide meaningful access to the care they needed.",

    # NUTS – Nutrition
    "HLTH-NUTS-0001": "The federal government would fund rigorous scientific research into how ultra-processed foods—industrial food products loaded with additives—contribute to chronic disease.",
    "HLTH-NUTS-0002": "The committee that writes the federal Dietary Guidelines would be required to operate independently of the food industry, whose funding has historically influenced nutrition policy in ways that serve commercial interests over public health.",
    "HLTH-NUTS-0003": "Federal research funding would go toward understanding how structural factors like food deserts, poverty, and geography drive poor nutrition outcomes that cannot be solved by individual behavior change alone.",
    "HLTH-NUTS-0004": "The national nutrition database would be continuously updated, expanded, and grounded in independent research—making it a genuinely useful resource for patients, clinicians, and policymakers.",
    "HLTH-NUTS-0005": "Long-term federal research would study how diet affects mental health, energy, cognitive function, and quality of life—areas currently underfunded relative to their importance.",
    "HLTH-NUTS-0006": "Before industry-funded nutrition research can inform federal dietary policy, it would be required to be independently replicated—preventing repeat historical examples of food industry science shaping public guidance.",
    "HLTH-NUTS-0007": "Federal funding would support rigorous research into the human microbiome and its role in health and disease—an emerging field with major implications for nutrition, immunity, and chronic disease.",
    "HLTH-NUTS-0008": "Nutrition education would be integrated into medical school and primary care practice, so physicians are equipped to counsel patients on diet—currently most receive fewer than 20 hours of nutrition training in medical school.",

    # ORDS – Orphan drugs
    "HLTH-ORDS-0001": "The Orphan Drug Act would be reformed to prevent pharmaceutical companies from abusing its special market protections by applying for rare-disease status for sub-groups of common diseases just to charge monopoly prices.",
    "HLTH-ORDS-0002": "Drugs for rare diseases that were developed with substantial federal research funding would be required to be priced at cost plus a capped markup, and could not use patent strategies to block generic competition after exclusivity expires.",

    # OVRG – Oversight
    "HLTH-OVRG-0001": "Insurers and other coverage entities would be required to publicly report how often they deny claims, how long delays typically last, and how often denied claims are reversed on appeal.",
    "HLTH-OVRG-0002": "Healthcare oversight bodies would have real enforcement authority to investigate patterns of denial, delay, and undercoverage—and to impose meaningful consequences when coverage systems fail patients.",
    "HLTH-OVRG-0003": "Clear penalties and remedies would apply when healthcare coverage systems systematically deny or delay care, so the consequences of harm to patients are real and enforceable.",
    "HLTH-OVRG-0004": "Patients would have the right to sue when coverage rules are violated in ways that delay or deny their care, giving them a direct legal remedy beyond the complaint process.",
    "HLTH-OVRG-0005": "All healthcare coverage entities—public and private—would be subject to consistent oversight and accountability standards, so there are no gaps where poor practices can hide.",

    # PANS – Pain management
    "HLTH-PANS-0001": "For patients with a confirmed chronic pain diagnosis, insurance could not use prior authorization to delay access to physical therapy, occupational therapy, or non-opioid pain treatments by more than 72 hours. Opioids could not be required as a first step before accessing alternatives.",

    # PAUS – Prior authorization
    "HLTH-PAUS-0001": "Prior authorization—the requirement to get insurer approval before receiving care—would be strictly limited to cases with clear evidence that it prevents overuse. It could not be applied routinely to standard care.",
    "HLTH-PAUS-0002": "When prior authorization is required, the process must be transparent, clinically grounded, and easy for patients and their doctors to navigate without unnecessary complexity.",
    "HLTH-PAUS-0003": "Once a type of care has been approved multiple times for the same patient, the burden of repeatedly seeking re-authorization would be reduced or eliminated.",
    "HLTH-PAUS-0004": "Prior authorization could not be used to disrupt ongoing care for a chronic condition without a clear medical reason—continuity of care would be protected.",

    # PBMS – Pharmacy benefit managers
    "HLTH-PBMS-0001": "Pharmacy benefit managers—the middlemen who manage drug benefits—could not charge plans more for a drug than they pay the pharmacy (spread pricing). All manufacturer rebates would have to go directly to patients or the plan, not be kept by the PBM.",
    "HLTH-PBMS-0002": "PBMs operating nationally would need to obtain a federal license and publicly disclose all contracts, rebate arrangements, and compensation structures, so the people paying for drug coverage can see what they are actually paying for.",
    "HLTH-PBMS-0003": "PBMs could not design drug benefit structures to steer patients toward pharmacies the PBM owns or makes money from, or make brand-name drugs cheaper than generics to push patients toward more expensive options.",

    # PHRS – Pharmacy and drug safety
    "HLTH-PHRS-0001": "Generic drugs would be required to meet strong quality and safety standards equivalent to brand-name drugs, so patients can trust that generics work as well as the originals.",
    "HLTH-PHRS-0002": "Pharmaceutical manufacturers could not include unnecessary allergens or harmful additives in drug formulations when safer alternatives are available.",
    "HLTH-PHRS-0003": "The pharmaceutical supply chain would be required to have full traceability—so when contamination or counterfeiting is discovered, affected products can be traced and removed quickly.",

    # REBS – Rehabilitation
    "HLTH-REBS-0001": "All rehabilitation facilities and programs would be required to meet nationally consistent standards for staffing, safety, and treatment quality.",
    "HLTH-REBS-0002": "Rehabilitation treatment must be grounded in approaches with proven effectiveness—not practices that lack evidence or have been shown to cause harm.",
    "HLTH-REBS-0003": "Abusive practices in rehabilitation settings—including coercion, humiliation, and physically unsafe methods—would be explicitly prohibited and subject to enforcement.",
    "HLTH-REBS-0004": "Rehabilitation facilities would be required to publicly report on their ownership, outcomes, and treatment approaches so patients can make informed choices.",
    "HLTH-REBS-0005": "Rehabilitation treatment must be made accessible to people regardless of income, location, or disability status—barriers that prevent people from accessing recovery would be addressed.",
    "HLTH-REBS-0006": "Regular independent audits and oversight of rehabilitation programs would ensure ongoing compliance with safety and quality standards.",
    "HLTH-REBS-0007": "Voluntary treatment options would be expanded so people seeking help can access rehabilitation without being required to enter coercive or institutional settings.",

    # REPR – Reproductive rights
    "HLTH-REPR-0001": "Congress would codify the right to abortion access in federal law, ensuring that right is protected regardless of what individual states decide, with clear medical exceptions and no gestational bans inconsistent with medical practice.",
    "HLTH-REPR-0002": "The U.S. would commit to cutting its maternal mortality rate in half within five years through mandatory state mortality review committees, obstetric emergency standards, and targeted funding to address racial disparities.",
    "HLTH-REPR-0003": "All FDA-approved contraceptive methods would be available without a prescription, covered by every health insurance plan at zero cost, and covered by Medicaid everywhere—backed by $500 million annually for comprehensive sex education.",
    "HLTH-REPR-0004": "A federal reparative justice program would compensate survivors of state-sanctioned sterilization. Coercive sterilization in prisons, immigration detention, and institutions would be permanently prohibited and subject to criminal penalties.",

    # RSRS – Research and science
    "HLTH-RSRS-0001": "Federal healthcare funding would be required to increase investment in neglected conditions, medications, and populations that have received less attention than their medical burden warrants.",
    "HLTH-RSRS-0002": "Research priorities would specifically include conditions that are stigmatized, commercially unattractive, or primarily affecting vulnerable populations—where market incentives alone will never drive adequate investment.",
    "HLTH-RSRS-0003": "Dedicated federal funding would support research into medications and treatments serving small patient populations or communities where there has historically been little commercial interest.",

    # RTTS – Right to try
    "HLTH-RTTS-0001": "Adult patients who have tried all approved treatments—or for whom no approved treatment exists—would have the right to access investigational treatments under a licensed physician's supervision.",
    "HLTH-RTTS-0002": "All access to investigational treatments under this framework would require a licensed physician to order, oversee, and monitor the treatment throughout the process.",
    "HLTH-RTTS-0003": "Before trying an investigational treatment, patients must receive full written informed consent in plain language, an independent medical evaluation, and a second physician opinion.",
    "HLTH-RTTS-0004": "To qualify for investigational treatment access, a patient must have a confirmed diagnosis from a licensed physician and have exhausted or be unable to use approved treatments.",
    "HLTH-RTTS-0005": "Every use of investigational treatment would contribute anonymized outcome data to a national research database, turning individual access into evidence that helps future patients.",
    "HLTH-RTTS-0006": "All data submitted to the national investigational treatment database would be de-identified and protected to the highest privacy standards before submission.",
    "HLTH-RTTS-0007": "A publicly searchable national database of anonymized outcomes from investigational treatments would be created, so researchers, patients, and doctors can learn from real-world results.",
    "HLTH-RTTS-0008": "Doctors who follow all required protocols when administering an investigational treatment would be protected from professional discipline and civil liability.",
    "HLTH-RTTS-0009": "This framework creates a medically supervised access path—it does not create a commercial market for unapproved drugs, and the government's authority to regulate drugs is fully preserved.",
    "HLTH-RTTS-0010": "The DEA and FDA would be required to conduct mandatory evidence-based reviews of drug scheduling classifications for substances with established safety profiles, keeping scheduling decisions grounded in science rather than politics.",
    "HLTH-RTTS-0011": "The FDA's expanded access program would be reformed to set a 30-day decision deadline, require written justification for denials, and streamline the application process so patients can access it without a lawyer.",
    "HLTH-RTTS-0012": "No manufacturer or clinic could charge patients more than actual cost recovery for investigational treatments. Requiring patients to waive their right to sue as a condition of access would be prohibited.",

    # RURL – Rural healthcare
    "HLTH-RURL-0001": "No rural hospital could close without federal review and approval. Critical access hospitals would receive guaranteed minimum operating support to remain viable.",
    "HLTH-RURL-0002": "The federal government would declare a rural maternal health emergency and fund comprehensive programs to address the gap in maternal care and death rates in rural communities, where OB services have largely disappeared.",
    "HLTH-RURL-0003": "Telehealth would be permanently available under Medicare and Medicaid at the same reimbursement rates as in-person care, including audio-only services for people without reliable internet access.",
    "HLTH-RURL-0004": "Every hospital would be required to meet federal minimum nurse-to-patient ratios, and nurses could not be required to work mandatory overtime—protecting both patient safety and the health of care workers.",

    # RXDG – Prescription drug access
    "HLTH-RXDG-0001": "Drug coverage systems must include broad access to the medications patients need—formularies (lists of covered drugs) cannot be used as hidden tools to effectively deny prescriptions.",
    "HLTH-RXDG-0002": "When a patient needs a drug not on the standard formulary, there must be a fast and meaningful exception process so individual medical need is not overridden by a blanket list.",
    "HLTH-RXDG-0003": "Coverage systems cannot require patients to try and fail on multiple drugs before accessing the treatment their doctor recommends, when doing so causes medical harm.",
    "HLTH-RXDG-0004": "Coverage for medications must include drugs for conditions that are underfunded or neglected by commercial markets, where evidence supports their medical necessity.",
    "HLTH-RXDG-0005": "Federal production quotas for controlled medications must be set at levels that ensure patients with valid prescriptions can actually get them—not create artificial shortages.",
    "HLTH-RXDG-0006": "Regulatory rules cannot restrict the supply of approved medications in ways that prevent patients from filling their prescriptions in a timely manner.",
    "HLTH-RXDG-0007": "Quotas for controlled substances must be based on actual real-world prescribing data and medical demand, not static limits set without regard to patient need.",
    "HLTH-RXDG-0008": "When shortages of controlled medications occur, regulators must act quickly to adjust supply chains and quotas to restore patient access.",
    "HLTH-RXDG-0009": "Patients must be able to fill prescriptions for controlled medications without encountering geographic or pharmacy access barriers that vary unfairly by region.",
    "HLTH-RXDG-0010": "Expanding access to controlled medications would be paired with evidence-based prescribing guidelines and monitoring for misuse—protecting both access and safety.",
    "HLTH-RXDG-0011": "Patients in ongoing treatment with controlled medications cannot have their care disrupted due to supply shortages, quota limits, or administrative barriers outside their control.",
    "HLTH-RXDG-0012": "The power to negotiate maximum fair prices for prescription drugs would apply across all payers and all Americans—not just Medicare beneficiaries.",
    "HLTH-RXDG-0013": "Drug prices in the U.S. would be capped at 120% of the median price paid for the same drug in comparable countries like Canada, the UK, Germany, France, Japan, and Australia.",
    "HLTH-RXDG-0014": "Agreements where a brand-name drug company pays a generic manufacturer to stay out of the market would be banned as illegal anti-competitive conduct, lowering drug prices by allowing generics to compete.",

    # SCIS – Science and research
    "HLTH-SCIS-0001": "Federal investment in public research—through NIH, NSF, CDC, and similar agencies—would be treated as a guaranteed baseline public good, protected from arbitrary cuts.",
    "HLTH-SCIS-0002": "Federally funded research must be free from commercial control. No company could hold exclusive rights over study design, data access, or publication of publicly funded work.",
    "HLTH-SCIS-0003": "All research funded with public dollars must be published openly and available to anyone at no cost, within twelve months of publication.",
    "HLTH-SCIS-0004": "Federal research priorities must actively counter market bias by directing funding toward neglected conditions, rare diseases, and populations that the commercial market underserves.",
    "HLTH-SCIS-0005": "Federal funding would include a dedicated allocation for replication studies—independently re-running key findings—to address the reproducibility crisis in science that has allowed bad results to influence public health policy.",
    "HLTH-SCIS-0006": "Federal scientific advisory committees—including FDA and CDC panels—must be composed of scientists selected on merit and expertise, free from political appointment pressure.",
    "HLTH-SCIS-0007": "A national research infrastructure with dedicated funding would support clinical investigation of promising under-studied therapies, including psychedelic-assisted treatments and other approaches that market forces have failed to fund.",
    "HLTH-SCIS-0008": "Researchers who report misconduct, data manipulation, or commercial interference in federally funded research would be protected as whistleblowers against retaliation.",

    # STDS – Coverage standards
    "HLTH-STDS-0001": "Coverage decisions must be grounded in evidence-based medicine—not cost-cutting practices dressed up as clinical criteria.",
    "HLTH-STDS-0002": "Medical coverage standards must be set by scientific and clinical evidence, free from political or ideological interference.",
    "HLTH-STDS-0003": "All health plans would be required to meet minimum levels of service and access, so people can actually use the coverage they have.",
    "HLTH-STDS-0004": "Health plans would be held to maximum wait time standards for appointments and services, so covered care is available within a reasonable time.",
    "HLTH-STDS-0005": "Coverage and prior authorization decisions must be made within legally required time limits, so patients are not left in limbo waiting for decisions.",
    "HLTH-STDS-0006": "When a coverage decision involves urgent care, it must be made fast enough to prevent harm—urgency must shorten the decision timeline.",
    "HLTH-STDS-0007": "If a coverage decision is not made within the required timeframe, the requested care would be automatically approved unless narrow, defined exceptions apply.",
    "HLTH-STDS-0008": "Intentional administrative delay—dragging out decisions to avoid paying for care or to frustrate patients—would be prohibited and subject to enforcement.",
    "HLTH-STDS-0009": "The evidence base used to make coverage decisions must be fully transparent and publicly accessible, so patients and providers can understand why coverage rules are what they are.",
    "HLTH-STDS-0010": "When there is genuine scientific disagreement about coverage criteria, dissenting expert opinions would be published and made part of the public record.",
    "HLTH-STDS-0011": "Independent audit systems would regularly review whether coverage decisions are actually being made according to the stated standards.",
    "HLTH-STDS-0012": "Addiction would be treated as a medical condition in coverage and clinical standards—not a moral failing—with treatment held to the same standards as any other chronic disease.",
    "HLTH-STDS-0013": "Harm reduction strategies—approaches that reduce the health risks of drug use without requiring abstinence—would be treated as valid evidence-based medical interventions.",

    # SUPR – Supplements
    "HLTH-SUPR-0001": "The NIH would fund rigorous, independent, placebo-controlled research on widely used dietary supplements to establish what they actually do and do not do.",
    "HLTH-SUPR-0002": "Supplement labels would have to accurately reflect what the science actually shows, not just what manufacturers are allowed to imply under the current weak labeling rules.",
    "HLTH-SUPR-0003": "Supplements sold in the U.S. would be required to undergo independent laboratory testing to confirm they actually contain what the label says, at the stated dose.",
    "HLTH-SUPR-0004": "Manufacturing standards for dietary supplements would be strengthened and consistently enforced, including for imported products that currently face minimal scrutiny.",
    "HLTH-SUPR-0005": "Reporting of adverse events—health problems caused by supplements—would be made mandatory for healthcare providers, not just strongly encouraged, so dangerous products can be identified faster.",
    "HLTH-SUPR-0006": "A publicly accessible federal database of all marketed supplements, including safety data and the actual evidence for each claimed benefit, would be created and maintained.",
    "HLTH-SUPR-0007": "A federally funded crowdsourced safety surveillance system would track patient-reported problems with supplements across a market too large for the FDA to monitor alone.",
    "HLTH-SUPR-0008": "Manufacturers introducing a genuinely new supplement ingredient would be required to notify the FDA and demonstrate it is safe before selling it—currently this notification requirement is poorly enforced.",
    "HLTH-SUPR-0009": "The federal government would invest in public education resources to help people evaluate supplement claims critically and understand the difference between marketing and evidence.",
    "HLTH-SUPR-0010": "Industry-funded supplement research would be required to be disclosed and independently replicated before it could be used to shape federal dietary guidance.",

    # TELS – Telehealth
    "HLTH-TELS-0001": "Telemedicine services would be available to patients everywhere in the country, without being limited by state lines or regional insurance restrictions.",
    "HLTH-TELS-0002": "Telehealth would be treated as an access tool for people in rural areas, those with disabilities, and others who face barriers to in-person care—not as a secondary or lesser form of treatment.",

    # TRAN – Transition to universal care
    "HLTH-TRAN-0001": "Until the U.S. fully implements universal healthcare, all existing coverage systems would be regulated to move closer to universal standards—no rollbacks allowed during the transition.",
    "HLTH-TRAN-0002": "Healthcare reforms during any transition period must improve care immediately rather than weakening existing protections while waiting for a future system to arrive.",

    # TRLS – Treatment trials
    "HLTH-TRLS-0001": "Approvals and clinical trials for new treatments would be streamlined and better funded to move promising treatments to patients faster.",

    # UNIV – Universal healthcare
    "HLTH-UNIV-0001": "The U.S. would transition to a universal, publicly administered single-payer healthcare system, covering every resident with no premiums or cost barriers to essential care.",
    "HLTH-UNIV-0002": "While the U.S. works toward universal coverage, a robust public option would be immediately available to every American, offering comprehensive coverage at low or no cost as a bridge to the full system.",
    "HLTH-UNIV-0003": "A plan would be developed to transition from the current multi-payer system to a universal system in a way that minimizes disruption to patients, workers, and providers.",
    "HLTH-UNIV-0004": "The universal healthcare system would cover all medically necessary services, including mental health, dental, vision, long-term care, and reproductive healthcare.",

    # VACS – Vaccines
    "HLTH-VACS-0001": "Federal funding would go toward developing vaccines for infectious diseases—like STIs, tuberculosis, and malaria—where commercial incentives alone have failed to produce vaccines despite massive need.",
    "HLTH-VACS-0002": "A real-time, publicly accessible national vaccine safety database would be created, moving beyond the current passive reporting system that under-counts adverse events and is difficult for the public to use.",
    "HLTH-VACS-0003": "The federal government would fund and publish the largest independent post-market vaccine safety studies ever conducted, providing solid evidence to support public confidence.",
    "HLTH-VACS-0004": "A permanent, publicly accessible Vaccine Evidence Portal would be established to communicate vaccine science clearly and honestly—answering real public questions with real evidence.",
    "HLTH-VACS-0005": "All vaccines recommended by the CDC's Advisory Committee on Immunization Practices would be covered without any cost-sharing under universal healthcare—making vaccination free and accessible for everyone.",
    "HLTH-VACS-0006": "Federal funding would support evidence-based research into why people hesitate to vaccinate and what communication approaches effectively and respectfully address those concerns.",

    # VBEN – Veterans benefits
    "HLTH-VBEN-0001": "The VA disability rating system would be reformed to eliminate the zero-percent non-compensable rating, ensure combined ratings reflect actual functional impairment, and guarantee annual cost-of-living adjustments tied to Social Security COLA.",
    "HLTH-VBEN-0002": "The VA would be legally required to process all disability claims within 125 days, with emergency adjudicators for terminal or crisis cases and a new veterans benefits court for the most urgent appeals.",
    "HLTH-VBEN-0003": "The VA's caregiver support program would be expanded to cover veterans of all eras, with monthly stipends reflecting real home health aide costs and federally provided health insurance for family caregivers.",
    "HLTH-VBEN-0004": "The requirement that surviving military spouses choose between their survivor benefit plan and their dependency and indemnity compensation would be fully repealed—surviving spouses would receive both benefits in full, plus lifetime TRICARE coverage.",

    # VETS – Veterans healthcare
    "HLTH-VETS-0001": "The VA would be held to legally binding wait time standards, and veterans would be guaranteed access to community care providers when VA capacity cannot meet those timelines.",
    "HLTH-VETS-0002": "The VA would provide comprehensive, evidence-based mental healthcare for all veterans—including PTSD treatment using proven therapies, fully funded crisis intervention, and peer support specialists.",
    "HLTH-VETS-0003": "The VA would be fully funded to process all toxic exposure claims under the PACT Act fairly and promptly—no veteran with a covered condition would be denied due to bureaucratic delays.",
    "HLTH-VETS-0004": "The VA would provide complete healthcare for women veterans, including military sexual trauma treatment, full reproductive healthcare, and gender-specific services that have historically been underfunded.",

    # WELS – Wellbeing and wellness
    "HLTH-WELS-0001": "Federal healthcare policy would adopt a broader definition of health—one that includes mental and social well-being, not just the absence of disease—shaping how coverage and research priorities are set.",
    "HLTH-WELS-0002": "Federal research funding would go toward understanding what actually improves energy, mood, and daily functioning beyond just treating disease—a massive research gap that affects millions of people.",
    "HLTH-WELS-0003": "All federally funded healthcare research would be required to include patient-reported outcomes—measuring what patients actually experience—not just clinical markers that may not reflect how people actually feel.",
    "HLTH-WELS-0004": "Federal investment would support research into healthy aging and extending the years people live in good health, not just extending total lifespan.",
    "HLTH-WELS-0005": "Research into what promotes positive mental health—not just what treats mental illness—would receive dedicated federal funding, addressing a major gap in the current research agenda.",
    "HLTH-WELS-0006": "Healthcare quality measurement would be redesigned to capture wellness and quality-of-life outcomes, not just whether a provider performed the right procedure or avoided complications.",

    # WMHS – Women's health
    "HLTH-WMHS-0001": "Federal research funding for conditions that disproportionately affect women—including endometriosis, PCOS, and autoimmune diseases—would be proportional to how much those conditions affect people's lives, not based on historical neglect.",
    "HLTH-WMHS-0002": "The 1993 law requiring women to be included in federally funded clinical trials would be actively enforced—not just on paper—so medical treatments are tested on women and not just extrapolated from male-only studies.",
    "HLTH-WMHS-0003": "Dedicated federal research programs would finally address endometriosis, PCOS, and other chronically underfunded women's health conditions that cause severe suffering and have been ignored for decades.",
    "HLTH-WMHS-0004": "A national research agenda for menopause and female aging would be established, filling a striking gap given that menopause affects every woman who lives to middle age.",
    "HLTH-WMHS-0005": "Perinatal mental health conditions—including postpartum depression and anxiety, which affect up to 1 in 5 new parents—would receive dedicated federal research funding and improved clinical recognition.",
    "HLTH-WMHS-0006": "Research and clinical guidelines for cardiovascular disease in women would be updated to reflect that women often present with different symptoms than men, correcting decades of under-diagnosis.",
}
# fmt: on


def get_all_hlth_positions() -> list[dict]:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """SELECT id, subdomain, seq FROM positions
           WHERE domain='HLTH' AND (plain_language IS NULL OR plain_language = '')
           ORDER BY subdomain, seq"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_db(updates: dict[str, str]) -> None:
    conn = sqlite3.connect(DB_FILE)
    for pos_id, text in updates.items():
        conn.execute(
            "UPDATE positions SET plain_language = ? WHERE id = ?", (text, pos_id)
        )
    conn.commit()
    conn.close()


def update_html(updates: dict[str, str]) -> None:
    html = HTML_FILE.read_text(encoding="utf-8")
    changed = 0
    for pos_id, plain_text in updates.items():
        # Pattern 1: card has <p class="rule-plain"></p> already (empty) - fill it
        empty_pattern = (
            rf'(id="{re.escape(pos_id)}"[^>]*>(?:.*?)'
            rf'<p class="rule-plain">)\s*(</p>)'
        )
        filled = re.sub(
            empty_pattern,
            lambda m: f'{m.group(1)}{plain_text}{m.group(2)}',
            html,
            count=1,
            flags=re.DOTALL,
        )
        if filled != html:
            html = filled
            changed += 1
            continue

        # Pattern 2: card has <p class="rule-title"> with no rule-plain before rule-stmt
        # Find the card by id, locate rule-title, insert rule-plain after it
        # Find card section
        card_pattern = re.compile(
            rf'(<div[^>]*id="{re.escape(pos_id)}"[^>]*>.*?)'
            rf'(<p class="rule-title">[^<]*(?:<[^/][^>]*>[^<]*</[^>]*>)*[^<]*</p>)',
            re.DOTALL
        )
        m = card_pattern.search(html)
        if m:
            old = m.group(0)
            new = old + f'<p class="rule-plain">{plain_text}</p>'
            html = html.replace(old, new, 1)
            changed += 1
            continue

        # Pattern 3: rule-title is a <div> (proposal cards with old structure)
        card_div_pattern = re.compile(
            rf'(<div[^>]*id="{re.escape(pos_id)}"[^>]*>.*?)'
            rf'(<div class="rule-title">[^<]*(?:<[^/][^>]*>[^<]*</[^>]*>)*[^<]*</div>)',
            re.DOTALL
        )
        m = card_div_pattern.search(html)
        if m:
            old = m.group(0)
            new = old + f'<p class="rule-plain">{plain_text}</p>'
            html = html.replace(old, new, 1)
            changed += 1

    HTML_FILE.write_text(html, encoding="utf-8")
    print(f"  HTML: updated {changed} cards")


def git_commit(message: str) -> None:
    subprocess.run(
        ["git", "add", "docs/pillars/healthcare.html", "policy/catalog/policy_catalog_v2.sqlite"],
        cwd=REPO,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", message, "--trailer",
         "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"],
        cwd=REPO,
        check=True,
    )


def main() -> None:
    positions = get_all_hlth_positions()
    print(f"Found {len(positions)} HLTH positions needing plain language")

    # Check coverage
    missing = [p["id"] for p in positions if p["id"] not in PLAIN_LANGUAGE]
    if missing:
        print(f"WARNING: No plain language written for {len(missing)} positions:")
        for m in missing:
            print(f"  {m}")

    # Batch in groups of ~50 for commits
    covered = [(p["id"], PLAIN_LANGUAGE[p["id"]]) for p in positions if p["id"] in PLAIN_LANGUAGE]
    print(f"Processing {len(covered)} positions in batches of 50")

    batch_size = 50
    batches = [covered[i:i+batch_size] for i in range(0, len(covered), batch_size)]

    for batch_num, batch in enumerate(batches, 1):
        batch_dict = dict(batch)
        print(f"\nBatch {batch_num}/{len(batches)}: {len(batch_dict)} positions")
        update_db(batch_dict)
        update_html(batch_dict)
        git_commit(
            f"feat(plain-lang): backfill HLTH plain language batch {batch_num}\n\n"
            f"Add plain_language field for {len(batch_dict)} HLTH policy positions "
            f"({batch[0][0]} through {batch[-1][0]})."
        )
        print(f"  Committed batch {batch_num}")


if __name__ == "__main__":
    main()
