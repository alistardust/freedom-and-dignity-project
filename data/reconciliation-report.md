# Policy Catalog Reconciliation Report

> **READ-ONLY REPORT** — No HTML or DB changes were made.
> Phase 2 migration may begin only after Ali signs off on this report.

---

## Summary

| Item | Count |
|------|-------|
| HTML policy cards (total) | 2,958 |
| HTML cards with valid ID | 2,887 |
| HTML cards with NO ID | 0 |
| HTML cards: div id ≠ code element id | 0 |
| HTML cards: invalid ID format | 71 |
| DB policy_items (total) | 2,783 |
| **Confirmed match** (in both HTML & DB) | **2,782** |
| Text divergence (same ID, different text) | 993 |
| **HTML-only** (on site, not in DB) | **71** |
| **DB-only** (in DB, not on site) | **1** |
| Duplicate IDs in HTML | 103 |

---

## HTML-only cards (on site, not in DB)

These cards exist in the HTML but have no matching `rule_id` in `policy_items`.
Per Phase 2 conflict rules: **HTML wins — DB must be backfilled.**

**By scope:**
- `EDU`: 7
- `ENV`: 8
- `HLT`: 7
- `IMM`: 4
- `MED`: 7
- `STS`: 38

**Total: 71**

<details>
<summary>Full list</summary>

| ID | Title | File |
|----|-------|------|
| `EDU-EQF-001` |  | education.html |
| `EDU-EQF-002` |  | education.html |
| `EDU-EQF-003` |  | education.html |
| `EDU-IDEA-001` |  | education.html |
| `EDU-IDEA-002` |  | education.html |
| `EDU-SRC-001` |  | education.html |
| `EDU-SRC-002` |  | education.html |
| `ENV-FDS-001` |  | environment-and-agriculture.html |
| `ENV-FDS-002` |  | environment-and-agriculture.html |
| `ENV-NUC-001` |  | environment-and-agriculture.html |
| `ENV-NUC-002` |  | environment-and-agriculture.html |
| `ENV-PFAS-001` |  | environment-and-agriculture.html |
| `ENV-PFAS-002` |  | environment-and-agriculture.html |
| `ENV-SUB-001` |  | environment-and-agriculture.html |
| `ENV-SUB-002` |  | environment-and-agriculture.html |
| `HLT-HRG-001` |  | healthcare.html |
| `HLT-HRG-002` |  | healthcare.html |
| `HLT-LCD-001` |  | healthcare.html |
| `HLT-LCD-002` |  | healthcare.html |
| `HLT-ORD-001` |  | healthcare.html |
| `HLT-ORD-002` |  | healthcare.html |
| `HLT-PAN-001` |  | healthcare.html |
| `IMM-DACA-001` |  | immigration.html |
| `IMM-DACA-002` |  | immigration.html |
| `IMM-SL-001` |  | immigration.html |
| `IMM-SL-002` |  | immigration.html |
| `MED-DIS-001` |  | information-and-media.html |
| `MED-DIS-002` |  | information-and-media.html |
| `MED-DIS-003` |  | information-and-media.html |
| `MED-LNJ-001` |  | information-and-media.html |
| `MED-LNJ-002` |  | information-and-media.html |
| `MED-S230-001` |  | information-and-media.html |
| `MED-S230-002` |  | information-and-media.html |
| `STS-AGY-001` | Reform FDA approval pathways to be faster without reducing safety or e | science-technology-space.html |
| `STS-AGY-002` | Reduce FDA's structural dependence on industry user fees as its primar | science-technology-space.html |
| `STS-AGY-003` | Protect CDC's operational independence and data reporting from politic | science-technology-space.html |
| `STS-AGY-004` | Establish NIST as the authoritative neutral standards body for AI, qua | science-technology-space.html |
| `STS-AGY-005` | Create permanent cross-agency science councils for integrated research | science-technology-space.html |
| `STS-AGY-006` | Expand federal research partnerships with land-grant universities, HBC | science-technology-space.html |
| `STS-DEB-001` | Fund Space Force and interagency debris tracking and active orbital cl | science-technology-space.html |
| `STS-DEB-002` | Assign financial responsibility for end-of-life satellite disposal to  | science-technology-space.html |
| `STS-DEB-003` | Cap large satellite constellation authorizations without approved debr | science-technology-space.html |
| `STS-DEB-004` | Make approved deorbit plans a mandatory condition of FCC spectrum and  | science-technology-space.html |
| `STS-DEB-005` | Lead the development of an international space traffic management trea | science-technology-space.html |
| `STS-DEB-006` | Designate Kessler syndrome prevention as a national security and econo | science-technology-space.html |
| `STS-EDU-001` | Establish a federal strategy and dedicated funding for public science  | science-technology-space.html |
| `STS-EDU-002` | Adopt a science-and-belief coexistence framework that broadens science | science-technology-space.html |
| `STS-EDU-003` | Protect evidence-based K-12 science curricula from political interfere | science-technology-space.html |
| `STS-EDU-004` | Create a National Science Communication Fund to support accessible, ac | science-technology-space.html |
| `STS-EDU-005` | Sustain federal investment in science museums, planetariums, and publi | science-technology-space.html |
| `STS-FND-001` | Establish a mandatory minimum federal investment in basic and applied  | science-technology-space.html |
| `STS-FND-002` | Replace annual grant cycles with five-year funding windows for all maj | science-technology-space.html |
| `STS-FND-003` | Prohibit industry-funded research from serving as the sole evidentiary | science-technology-space.html |
| `STS-FND-004` | Create formal cross-agency research partnerships across CDC, FDA, NASA | science-technology-space.html |
| `STS-FND-005` | Require a funding commitment whenever a federal agency determines that | science-technology-space.html |
| `STS-FND-006` | Require immediate, barrier-free public access to all federally funded  | science-technology-space.html |
| `STS-INT-001` | Maintain U.S. leadership in international scientific treaty frameworks | science-technology-space.html |
| `STS-INT-002` | Reinstate and expand international climate science cooperation as a pe | science-technology-space.html |
| `STS-INT-003` | Build pandemic preparedness as permanent global research infrastructur | science-technology-space.html |
| `STS-INT-004` | Treat U.S. scientific credibility as a foreign policy asset and scienc | science-technology-space.html |
| `STS-PUB-001` | Create a national open-access research database for all publicly funde | science-technology-space.html |
| `STS-PUB-002` | Require pre-publication quality screening for sample adequacy, researc | science-technology-space.html |
| `STS-PUB-003` | Require plain-language summaries alongside every published paper from  | science-technology-space.html |
| `STS-PUB-004` | Mandate pre-registration of study methodology before data collection f | science-technology-space.html |
| `STS-PUB-005` | Require independent replication before high-impact studies can serve a | science-technology-space.html |
| `STS-PUB-006` | Require publication of negative results to combat publication bias | science-technology-space.html |
| `STS-SPC-001` | Restore and maintain a NASA-operated crewed spacecraft capability inde | science-technology-space.html |
| `STS-SPC-002` | Restore NASA's capability to service, repair, and upgrade orbital infr | science-technology-space.html |
| `STS-SPC-003` | Provide NASA with multi-year budget stability and long-range program p | science-technology-space.html |
| `STS-SPC-004` | Recognize space exploration as a source of national inspiration and a  | science-technology-space.html |
| `STS-SPC-005` | Extend the ISS cooperation model to deep space exploration through per | science-technology-space.html |

</details>

---

## DB-only items (in DB, not on site)

These items are in `policy_items` but have no matching ID on the site.
Per Phase 2 conflict rules: **Add as proposal card to HTML.**

> ⚠️ NOTE: DB `status = 'MISSING'` does NOT reliably indicate the item is absent
> from the site. Many HTML cards were added after the DB was built from source logs.
> This list reflects IDs genuinely absent from HTML, not the DB status field.

**By scope:**
- `TAXN`: 1

**Total: 1**

<details>
<summary>Full list</summary>

| ID | Statement | DB Status |
|----|-----------|-----------|
| `TAXN-GENL-0001` | Tax systems must be progressive overall and may not shift disproportio | CANONICAL |

</details>

---

## Text divergences (same ID, different text)

These items are in both HTML and DB, but the text appears to differ.
**These require human review — do not auto-resolve.**

**Total: 993**

| ID | HTML title | DB statement | File |
|----|-----------|--------------|------|
| `ADMN-ADJS-0001` | adjudication systems must provide clear notice, records | Agency adjudication systems must provide clear notice,  | administrative-state.html |
| `ADMN-CAPS-0001` | must be structurally insulated from regulated-industry  | Agencies must be structurally insulated from regulated- | administrative-state.html |
| `ADMN-CIVL-0001` | Career civil servants may not be reclassified as at-wil | Career federal employees in competitive service positio | administrative-state.html |
| `ADMN-COOS-0001` | with overlapping jurisdiction must coordinate enforceme | Agencies with overlapping jurisdiction must coordinate  | administrative-state.html |
| `ADMN-ENFL-0001` | must have sufficient investigatory powers, subpoena aut | Agencies must have sufficient investigatory powers, sub | administrative-state.html |
| `ADMN-FNDS-0001` | charged with protecting rights, public safety, markets, | Agencies charged with protecting rights, public safety, | administrative-state.html |
| `ADMN-INDS-0001` | must be protected from arbitrary defunding, bad-faith u | Agencies must be protected from arbitrary defunding, ba | administrative-state.html |
| `ADMN-MAJS-0001` | Congress must explicitly confirm agency authority for m | Congress must affirmatively exercise its authority to c | administrative-state.html |
| `ADMN-PUBL-0001` | rulemaking and oversight processes must include meaning | Agency rulemaking and oversight processes must include  | administrative-state.html |
| `ADMN-RGTS-0001` | authority may not be exercised through arbitrary, discr | Agency authority may not be exercised through arbitrary | administrative-state.html |
| `ADMN-RULS-0001` | must have authority to issue, revise, and clarify | Agencies must have authority to issue, revise, and clar | administrative-state.html |
| `ADMN-SCIS-0001` | relying on scientific, medical, technical, or economic  | Agencies relying on scientific, medical, technical, or  | administrative-state.html |
| `ADMN-SYSR-0001` | agencies are legitimate constitutional instruments of d | Administrative agencies are legitimate constitutional i | administrative-state.html |
| `ADMN-TRAN-0001` | must publish clear public information about mission, ru | Agencies must publish clear public information about mi | administrative-state.html |
| `ADMN-WBLS-0001` | Federal employees must be protected from retaliation fo | Federal employees who report illegal orders, scientific | administrative-state.html |
| `ANTR-PHRM-0003` | Pharmacy Benefit Managers must be banned from pharmacy  | PBM consolidation and vertical self-dealing must be bro | antitrust-and-corporate-power.html |
| `CHKS-AINL-0001` | Prohibition on Asymmetrical AI Processes | AI-assisted decision systems must not create asymmetric | checks-and-balances.html |
| `CHKS-AINL-0002` | Independent Human Judgment Required for Material Harm | Any decision that materially harms restricts or denies  | checks-and-balances.html |
| `CHKS-AINL-0004` | Equal and Timely Consideration Regardless of AI Score | All individuals must receive equal and timely considera | checks-and-balances.html |
| `CHKS-AINL-0005` | AI Bias Detection and Mitigation | AI systems used in decision-making processes must inclu | checks-and-balances.html |
| `CHKS-AINL-0006` | Continuous Auditing for Bias and Disparate Impact | Decision-making systems using AI must be continuously a | checks-and-balances.html |
| `CHKS-AINL-0007` | Domain-Specific AI Rules | Each policy domain or pillar must define its own AI sys | checks-and-balances.html |
| `CHKS-BRNS-0001` | Independent Oversight Boards for Each Branch | Each branch of government and major constitutional body | checks-and-balances.html |
| `CHKS-BRNS-0002` | Oversight Board Independence | Oversight boards must be independent from the bodies th | checks-and-balances.html |
| `CHKS-FEDS-0001` | Federal Independent Oversight Body | Establish a federal independent oversight and investiga | checks-and-balances.html |
| `CHKS-FEDS-0002` | Authority Over Federally Elected Officials | Federal oversight body has authority to investigate any | checks-and-balances.html |
| `CHKS-FEDS-0003` | Oversight Body Composition and Elected Component | Federal oversight body includes one elected member and  | checks-and-balances.html |
| `CHKS-FEDS-0004` | Subpoena and Deposition Powers | Federal oversight body has subpoena and deposition powe | checks-and-balances.html |
| `CHKS-FEDS-0005` | High-Risk Systems Not Fully Centralized | High-risk systems must not be fully centralized | checks-and-balances.html |
| `CHKS-FEDS-0007` | Federal Standards for Elections | Federal sets standards but not direct control of electi | checks-and-balances.html |
| `CHKS-FNDS-0001` | Guaranteed Adequate Funding | Funding for oversight and investigation bodies must be  | checks-and-balances.html |
| `CHKS-FNDS-0002` | Automatic Extension if Funding Not Passed | If funding is not passed oversight bodies automatically | checks-and-balances.html |
| `CHKS-FNDS-0003` | Automatic Extension Includes 10% Increase | Automatic funding extension includes a 10 percent incre | checks-and-balances.html |
| `CHKS-FNDS-0004` | Funding Separate from Overseen Departments | Oversight funding must be separate from the departments | checks-and-balances.html |
| `CHKS-FNDS-0005` | Protection from Political and External Influence | Oversight funding must be protected from political and  | checks-and-balances.html |
| `CHKS-FNDS-0006` | Platform as Policy and Strategy | Platform is both a policy framework and long-term strat | checks-and-balances.html |
| `CHKS-FNDS-0013` | Movement Not Left vs Right | Movement is not left vs right | checks-and-balances.html |
| `CHKS-FNDS-0023` | Core Values: Truth, Equality, Freedom, Dignity | Core values include truth equality freedom dignity | checks-and-balances.html |
| `CHKS-GEOS-0004` | Cross-State Access Guaranteed | Cross-state access must be guaranteed | checks-and-balances.html |
| `CHKS-GEOS-0005` | Travel Support When Local Care Unavailable | Travel support required when local care unavailable | checks-and-balances.html |
| `CHKS-JURS-0001` | Jurisdiction Over State Officials | Federal oversight body may investigate governors and hi | checks-and-balances.html |
| `CHKS-JURS-0002` | Jurisdiction Over Failed State Oversight | Federal oversight body may investigate state oversight  | checks-and-balances.html |
| `CHKS-STAS-0001` | State Oversight Boards Required | Each state must establish its own independent oversight | checks-and-balances.html |
| `CHKS-STAS-0002` | Directly Elected Members | State oversight boards include directly elected members | checks-and-balances.html |
| `CHKS-STAS-0003` | Appointed Members Balance | State oversight boards include members appointed by leg | checks-and-balances.html |
| `CNSR-ALGO-0001` | Algorithmic pricing and offers may not discriminate bas | Pricing algorithms, personalized offer systems, and con | consumer-rights.html |
| `CNSR-CNSS-0001` | No required proprietary consumables where alternatives  | Products may not require proprietary consumables or sub | consumer-rights.html |
| `CNSR-CRDS-0001` | Credit reports must be accurate and disputes must be me | Credit reporting agencies must maintain accurate consum | consumer-rights.html |
| `CNSR-DBRS-0001` | Data brokers must register, disclose their sources, and | Commercial data brokers that compile, sell, or share co | consumer-rights.html |
| `CNSR-DRKS-0001` | Deceptive interface design that manipulates consumer ch | Interface designs that deliberately manipulate consumer | consumer-rights.html |
| `CNSR-ENFL-0001` | Violations require restoration, restitution, and penalt | Violations of ownership-based functionality rules must  | consumer-rights.html |
| `CNSR-ENFL-0002` | Private right of action for unlawful post-purchase rest | Consumers must have a private right of action where pro | consumer-rights.html |
| `CNSR-FEES-0001` | Prohibit hidden fees, drip pricing, and junk fees | Hidden fees, junk fees, drip pricing, and post-selectio | consumer-rights.html |
| `CNSR-FTRS-0001` | May not artificially disable available hardware feature | Manufacturers may not artificially disable or withhold  | consumer-rights.html |
| `CNSR-GENL-0001` | Prohibit deceptive and exploitative business practices | Consumer protection law must prohibit deceptive, coerci | consumer-rights.html |
| `CNSR-OWNS-0001` | Purchase conveys full access to core functionality | Purchase of a physical product conveys full access to i | consumer-rights.html |
| `CNSR-OWNS-0002` | Ownership may not be converted to subscription dependen | Ownership of a product may not be converted into a subs | consumer-rights.html |
| `CNSR-QLTS-0001` | Products must meet minimum durability and quality stand | Consumer products must meet minimum durability, safety, | consumer-rights.html |
| `CNSR-SUBS-0001` | Subscriptions may not replace feasible ownership | Subscription models may not be structured to replace ow | consumer-rights.html |
| `CNSR-TRAN-0002` | Post-sale paywalling of previously included features pr | Post-sale changes that move previously included feature | consumer-rights.html |
| `CNSR-WARS-0001` | Warranties must be understandable, fair, and enforceabl | Warranty systems must be understandable, fair, and enfo | consumer-rights.html |
| `CORT-LGOS-0001` | Congressional supermajority override of SCOTUS decision | Congress may reinstate a federal statute invalidated by | courts-and-judicial-system.html |
| `CORT-NOMS-0001` | Senate must act on judicial nominees within 90 days | The Senate must hold confirmation hearings and vote on  | courts-and-judicial-system.html |
| `CORT-SHDS-0001` | Shadow docket orders require supermajority and written  | Emergency or shadow docket orders issued without full b | courts-and-judicial-system.html |
| `CORT-SIZS-0001` | Supreme Court size set by constitutional amendment or s | Supreme Court size must be set by constitutional amendm | courts-and-judicial-system.html |
| `CRPT-ASFS-0001` | Prohibit civil asset forfeiture without criminal convic | The federal government and any state or local law enfor | anti-corruption.html |
| `CRPT-EMOS-0001` | Establish a statutory enforcement mechanism for the emo | Congress must enact a statute establishing a clear caus | anti-corruption.html |
| `CRPT-FARS-0001` | Strengthen FARA enforcement with mandatory registration | The Foreign Agents Registration Act (22 U | anti-corruption.html |
| `CRPT-INTL-0001` | Full U.S. implementation of UNCAC obligations — asset r | The United States must fully implement all obligations  | anti-corruption.html |
| `CRPT-OWNS-0001` | Full public beneficial ownership registry — strengthen  | The beneficial ownership reporting framework establishe | anti-corruption.html |
| `EDUC-BNDS-0001` | Guarantee broadband access and devices for all K–12 stu | Every K–12 student must have reliable broadband interne | education.html |
| `EDUC-DISS-0001` | Replace zero-tolerance discipline with restorative just | Schools must transition away from zero-tolerance, punit | education.html |
| `EDUC-FINC-0001` | EDU|FIN|Student loan debt forgiveness or large-scale re | Student loan debt forgiveness or large-scale restructur | education.html |
| `EDUC-LIBS-0001` | Protect K–12 teachers from retaliation for teaching evi | K–12 teachers must be protected from disciplinary actio | education.html |
| `EDUC-STDS-0001` | EDU|STD|Education standards must include protections ag | Education standards must include protections against po | education.html |
| `ELEC-IDAS-0001` | Mandatory free voter ID assistance | Free voter ID assistance | elections-and-representation.html |
| `ELEC-IDAS-0002` | Legal representation and case management | Legal and case support for ID access | elections-and-representation.html |
| `ELEC-IDAS-0003` | Free transportation to ID-issuing offices | If a state requires voter ID, it must provide free tran | elections-and-representation.html |
| `ELEC-IDAS-0004` | Proactive outreach — state finds the voter | States requiring voter ID must proactively identify and | elections-and-representation.html |
| `ELEC-IDAS-0005` | Mobility must not be a barrier to voter ID | Physical mobility must not be a barrier to obtaining vo | elections-and-representation.html |
| `ENVR-CLIS-0001` | Require federal climate adaptation plans for all major  | All major federal infrastructure programs and agencies  | environment-and-agriculture.html |
| `ENVR-CPXS-0001` | Establish a carbon price that reflects the full social  | The United States must implement a carbon pricing mecha | environment-and-agriculture.html |
| `ENVR-JUSS-0001` | Prohibit siting of polluting facilities that creates di | Environmental permitting processes must include a cumul | environment-and-agriculture.html |
| `ENVR-REGS-0002` | Environmental Protection Agency must be constitutionall | The Environmental Protection Agency must be constitutio | environment-and-agriculture.html |
| `ENVR-WTRS-0001` | Establish a federal right to clean water for all reside | Access to safe, affordable drinking water is a fundamen | environment-and-agriculture.html |
| `GUNS-ACQS-0001` | Universal background checks for all acquisitions | Require background checks for all firearm acquisitions | gun-policy.html |
| `GUNS-ACQS-0002` | Background checks cover all transfers including private | Background check requirement applies to all transfers i | gun-policy.html |
| `GUNS-ACQS-0003` | Comprehensive and interoperable background check databa | Background check databases must be comprehensive, inter | gun-policy.html |
| `GUNS-BANS-0001` | Ban weapons of war from civilian ownership | Ban private ownership of weapons of war including autom | gun-policy.html |
| `GUNS-BANS-0002` | Evasion-resistant definition of weapons of war | Definition of weapons of war must be evasion-resistant  | gun-policy.html |
| `GUNS-MHES-0001` | Dangerousness-based mental health evaluation | Mental health evaluations for gun ownership must be nar | gun-policy.html |
| `GUNS-MHES-0002` | No blanket exclusion based on diagnosis alone | Prohibit blanket exclusion from firearm ownership based | gun-policy.html |
| `GUNS-MILS-0003` | Militia transparency and accountability requirements | Require militias to maintain membership records, financ | gun-policy.html |
| `GUNS-MILS-0004` | Government oversight of militia training | Federal and state governments must have oversight autho | gun-policy.html |
| `GUNS-MILS-0005` | Regulated militias integrated into disaster relief | Provide mechanisms for regulated militias to train for  | gun-policy.html |
| `GUNS-REGS-0001` | Constitutional authority to regulate firearms | Amend the Constitution to explicitly affirm government  | gun-policy.html |
| `GUNS-RFLS-0001` | Federal minimum standards for red flag laws | Establish federal minimum standards for red flag / extr | gun-policy.html |
| `GUNS-TRAN-0001` | Mandatory safety training for firearm ownership | Require safety training as a condition of firearm owner | gun-policy.html |
| `GUNS-TRAN-0002` | Mandatory de-escalation training for ownership | Require de-escalation training as a condition of firear | gun-policy.html |
| `GUNS-TRAN-0003` | Safe storage requirement | Require secure storage of firearms; safe storage law as | gun-policy.html |
| `HLTH-AINL-0001` | High-risk AI classification | AI systems in healthcare must be treated as high-risk s | healthcare.html |
| `HLTH-AINL-0002` | AI as support, not replacement | AI systems may support but not replace licensed medical | healthcare.html |
| `HLTH-AINL-0003` | Clinical decision support limits | AI systems may be used for clinical decision support on | healthcare.html |
| `HLTH-AINL-0004` | Evidence standards before deployment | AI systems must meet strong evidence standards for safe | healthcare.html |
| `HLTH-AINL-0005` | Continuous monitoring requirement | Deployed healthcare AI systems must be continuously mon | healthcare.html |
| `HLTH-AINL-0006` | No independent diagnosis or prescription | AI systems may not independently diagnose or prescribe  | healthcare.html |
| `HLTH-AINL-0007` | AI may not deny care | AI systems may not be used to deny restrict or limit me | healthcare.html |
| `HLTH-AINL-0008` | Independent clinical judgment required | Human reviewers must exercise independent clinical judg | healthcare.html |
| `HLTH-AINL-0009` | AI for approval only, not denial | AI systems may be used to assist or expedite approval o | healthcare.html |
| `HLTH-AINL-0010` | Prior human review for denials | Human review must occur prior to any denial decision an | healthcare.html |
| `HLTH-AINL-0012` | Independent evaluation required for denials | All denial decisions must be based on independent clini | healthcare.html |
| `HLTH-AINL-0013` | No systemic bias from AI prioritization | AI systems used to assist approvals must not create sys | healthcare.html |
| `HLTH-AINL-0014` | Equal human consideration for non-AI-flagged cases | Case review systems must ensure that requests not prior | healthcare.html |
| `HLTH-AINL-0015` | No opaque triage decisions | AI systems may not make opaque triage or prioritization | healthcare.html |
| `HLTH-AINL-0016` | AI may not prioritize cost over outcomes | Coverage decision-making entities must not use AI syste | healthcare.html |
| `HLTH-AINL-0017` | Access to explanations and appeals | Patients and providers must have access to explanations | healthcare.html |
| `HLTH-AINL-0018` | Right to human care | Patients have the right to receive care from qualified  | healthcare.html |
| `HLTH-AINL-0019` | Informed consent and opt-out | Patients must be informed when AI systems are used in t | healthcare.html |
| `HLTH-AINL-0020` | Strict data protections | Healthcare data used by AI systems must be treated as h | healthcare.html |
| `HLTH-AINL-0021` | No commercial data exploitation | Healthcare data may not be used for advertising profili | healthcare.html |
| `HLTH-AINL-0022` | Training data ethical standards | Training data for healthcare AI must meet strict ethica | healthcare.html |
| `HLTH-AINL-0023` | Fail-safe design | Healthcare AI systems must fail safely and defer to hum | healthcare.html |
| `HLTH-AINL-0024` | No unwarranted certainty | AI systems may not present outputs with unwarranted cer | healthcare.html |
| `HLTH-AINL-0025` | Bias evaluation and mitigation | Healthcare AI systems must be evaluated and mitigated f | healthcare.html |
| `HLTH-AINL-0026` | No disparity worsening | AI deployment must not worsen disparities in healthcare | healthcare.html |
| `HLTH-AINL-0027` | AI for research acceleration | AI may be used to accelerate medical research and drug  | healthcare.html |
| `HLTH-AINL-0028` | Research funding for neglected conditions | Increase funding for research into under-studied condit | healthcare.html |
| `HLTH-AINL-0029` | Priority for underfunded diseases | Public funding priorities must include diseases and con | healthcare.html |
| `HLTH-AINL-0030` | Science-based AI policy | Healthcare AI policy and approvals must be grounded in  | healthcare.html |
| `HLTH-AINL-0031` | Safe AI integration | AI systems must be integrated into healthcare systems i | healthcare.html |
| `HLTH-AINL-0032` | Interoperability with privacy protections | Healthcare AI systems should support interoperability a | healthcare.html |
| `HLTH-APLS-0001` | Fast, meaningful, independent appeals | Patients and providers must have access to fast meaning | healthcare.html |
| `HLTH-APLS-0002` | Urgent appeal timelines | Appeals involving urgent medically necessary treatment  | healthcare.html |
| `HLTH-APLS-0004` | Pattern review and penalties | Successful appeals should trigger review of the underly | healthcare.html |
| `HLTH-CLMS-0001` | Establish coverage and preparedness standards for clima | Coverage systems must include treatment for climate-rel | healthcare.html |
| `HLTH-COVR-0004` | Tighter denial limits | Establish tighter overall rules limiting denial of heal | healthcare.html |
| `HLTH-COVR-0005` | Overhaul insurance to reduce denials | Until universal healthcare is implemented overhaul heal | healthcare.html |
| `HLTH-COVR-0006` | Faster coverage decision timelines | Require faster timelines for healthcare coverage decisi | healthcare.html |
| `HLTH-COVR-0007` | Expedited appeal processes | Require expedited appeal processes for denials of healt | healthcare.html |
| `HLTH-COVR-0009` | Protect pre-existing condition bans | Protect and strengthen bans on denial of coverage based | healthcare.html |
| `HLTH-COVR-0010` | Expand coverage for under-covered conditions | Expand required coverage for conditions that are often  | healthcare.html |
| `HLTH-COVR-0011` | Require mental healthcare coverage | Require coverage of mental healthcare including talk th | healthcare.html |
| `HLTH-COVR-0012` | Psychedelic therapy coverage | Require coverage of psychedelic therapy where medically | healthcare.html |
| `HLTH-COVR-0013` | Nationwide in-network care | Require health plans to provide nationwide in-network c | healthcare.html |
| `HLTH-COVR-0014` | Expand HSA-style tools | Expand HSA-style health spending cards or equivalent he | healthcare.html |
| `HLTH-COVR-0015` | Ban high-deductible-only plans | Ban employers from offering only high-deductible health | healthcare.html |
| `HLTH-COVR-0016` | Employers pay all premiums | Require employers to pay all health insurance premiums  | healthcare.html |
| `HLTH-COVR-0017` | Fair coverage processes | Healthcare coverage or service may not be denied restri | healthcare.html |
| `HLTH-COVR-0018` | Clear standards for denials | Any adverse coverage decision must be based on clear me | healthcare.html |
| `HLTH-COVR-0019` | Public reporting of denial rates | Denial rates delay patterns and reversal rates must be  | healthcare.html |
| `HLTH-COVR-0020` | Penalties for repeated unjustified denials | Repeated unjustified denial or delay of medically neces | healthcare.html |
| `HLTH-COVR-0021` | Mandatory care floor | Coverage systems must include a broad mandatory floor o | healthcare.html |
| `HLTH-COVR-0022` | No vague exclusions | Coverage exclusions may not be written so broadly or va | healthcare.html |
| `HLTH-COVR-0023` | Clear language and pro-access interpretation | Coverage rules must be written in clear language and in | healthcare.html |
| `HLTH-COVR-0024` | Evidence-based coverage inclusion | Coverage systems must include medicines procedures ther | healthcare.html |
| `HLTH-COVR-0025` | Permanent pre-existing condition protections | Protections against denial or exclusion based on pre-ex | healthcare.html |
| `HLTH-COVR-0026` | No indirect pre-existing condition exclusion | Coverage systems must not use pre-existing-condition lo | healthcare.html |
| `HLTH-COVR-0027` | Expand historically under-covered conditions | Coverage requirements must be expanded for conditions t | healthcare.html |
| `HLTH-COVR-0028` | Mental health parity | Coverage systems must include mental healthcare on pari | healthcare.html |
| `HLTH-COVR-0029` | No mental health access discrimination | Coverage systems may not impose narrower networks harsh | healthcare.html |
| `HLTH-COVR-0030` | Emerging evidence-based therapies | Where evidence and law support it coverage systems shou | healthcare.html |
| `HLTH-CRNS-0001` | Require coverage of post-acute sequelae of infectious d | Coverage systems must classify post-acute sequelae of i | healthcare.html |
| `HLTH-CSTS-0001` | Cost-sharing must not block access | Deductibles copays and out-of-pocket cost structures mu | healthcare.html |
| `HLTH-CSTS-0002` | Regulate cost-sharing for patient protection | Healthcare cost-sharing rules must be regulated to prot | healthcare.html |
| `HLTH-CSTS-0003` | Broad health spending tool access | Health spending cards or equivalent patient-directed to | healthcare.html |
| `HLTH-CSTS-0004` | No cost barriers for chronic/preventive care | Cost-sharing design may not be used to discourage care  | healthcare.html |
| `HLTH-DNTS-0001` | Include dental care in the mandatory coverage floor | Coverage systems must include comprehensive dental care | healthcare.html |
| `HLTH-EMPS-0001` | No high-deductible-only employer plans | Employers may not satisfy healthcare obligations by off | healthcare.html |
| `HLTH-EMPS-0002` | Employers pay full premiums | Employers should be required to pay the full premium co | healthcare.html |
| `HLTH-EMPS-0003` | Small business supports | Small businesses should receive subsidies public suppor | healthcare.html |
| `HLTH-EMPS-0004` | Prevent underinsurance disguised as coverage | Employer-based health coverage rules during the transit | healthcare.html |
| `HLTH-JUSS-0001` | Guarantee healthcare for incarcerated individuals equiv | Every person in state or federal custody has a constitu | healthcare.html |
| `HLTH-MATS-0001` | Mandate maternal mortality review and racial equity rep | Every state must maintain a maternal mortality review c | healthcare.html |
| `HLTH-MHCS-0002` | Mental health AI as high-risk | AI systems in mental health must be regulated as high-r | healthcare.html |
| `HLTH-MHCS-0003` | AI may not replace clinicians in high-risk determinatio | AI systems may not replace licensed clinicians in diagn | healthcare.html |
| `HLTH-MHCS-0004` | No AI-only suicide/crisis decisions | AI systems may not serve as the sole decision-maker in  | healthcare.html |
| `HLTH-MHCS-0005` | Human accountability required | A clearly identifiable licensed human professional must | healthcare.html |
| `HLTH-MHCS-0006` | AI as assistive tool only | AI may be used as an assistive tool in mental healthcar | healthcare.html |
| `HLTH-MHCS-0007` | Evidence standards for mental health AI | AI systems used in mental health care must meet strong  | healthcare.html |
| `HLTH-MHCS-0008` | Continuous monitoring for mental health AI | Mental health AI systems must be continuously monitored | healthcare.html |
| `HLTH-MHCS-0009` | No deceptive AI therapist presentation | AI systems marketed for mental health support may not d | healthcare.html |
| `HLTH-MHCS-0010` | No emotional dependency cultivation | AI systems may not be designed to cultivate emotional d | healthcare.html |
| `HLTH-MHCS-0011` | Clear AI disclosure | Any AI system offering mental health support must clear | healthcare.html |
| `HLTH-MHCS-0013` | Escalation pathways to human care | Mental health AI systems must include clear escalation  | healthcare.html |
| `HLTH-MHCS-0014` | No false reassurance | Mental health AI systems may not provide false reassura | healthcare.html |
| `HLTH-MHCS-0015` | Fail safely to human care | Where mental health AI systems are uncertain or out of  | healthcare.html |
| `HLTH-MHCS-0016` | Enhanced mental health data privacy | Data generated through AI mental health interactions mu | healthcare.html |
| `HLTH-MHCS-0017` | No commercial mental health data exploitation | Mental health AI data may not be sold shared for advert | healthcare.html |
| `HLTH-MHCS-0018` | No discriminatory use of mental health data | Mental health data inferred or collected by AI systems  | healthcare.html |
| `HLTH-MHCS-0019` | Explicit informed consent | Consent for use of mental health AI systems and their d | healthcare.html |
| `HLTH-MHCS-0020` | Evidence required for efficacy claims | AI systems may not claim mental health efficacy diagnos | healthcare.html |
| `HLTH-MHCS-0021` | Independent evaluation required | Mental health AI systems must be subject to independent | healthcare.html |
| `HLTH-MHCS-0022` | Disclose risks and failure modes | Material risks limitations and known failure modes of m | healthcare.html |
| `HLTH-MHCS-0023` | Right to human mental healthcare | People must retain a right to access human mental healt | healthcare.html |
| `HLTH-MHCS-0024` | Coercive AI deployment safeguards | AI mental health tools may not be imposed coercively in | healthcare.html |
| `HLTH-MHCS-0025` | No behavioral conformity enforcement | AI systems may not be used to enforce behavioral confor | healthcare.html |
| `HLTH-MHCS-0026` | School AI risk-scoring restrictions | Schools may not rely on opaque AI mental health or risk | healthcare.html |
| `HLTH-MHCS-0027` | Prison/detention AI restrictions | Jails prisons detention facilities and similar institut | healthcare.html |
| `HLTH-MHCS-0028` | Public benefits AI assessment limits | Public benefits or disability systems may not use opaqu | healthcare.html |
| `HLTH-MHCS-0029` | Insurers may not use AI to deny mental health care | AI systems may not be used by insurers or payers to den | healthcare.html |
| `HLTH-MHCS-0030` | AI not substitute for licensed care | AI systems may not be used as a substitute for access t | healthcare.html |
| `HLTH-MHCS-0031` | Data retention limits and user control | Mental health AI systems must implement strict limits o | healthcare.html |
| `HLTH-MHCS-0032` | Training data consent standards | Training data for mental health AI systems must not inc | healthcare.html |
| `HLTH-MHCS-0033` | Clear capability limits | Mental health AI systems must clearly define their role | healthcare.html |
| `HLTH-MHCS-0034` | No manipulative behavior modification | AI systems may not use mental health interactions to ma | healthcare.html |
| `HLTH-MHCS-0035` | No surveillance integration | Mental health AI systems may not be integrated with sur | healthcare.html |
| `HLTH-MHCS-0036` | Research ethical review standards | Use of AI mental health systems in experimental or rese | healthcare.html |
| `HLTH-MHCS-0037` | Fund independent AI mental health research | Fund independent research into the short-term and long- | healthcare.html |
| `HLTH-MHCS-0038` | Ban conversational AI for young children | Ban use of AI systems designed for conversational emoti | healthcare.html |
| `HLTH-MHCS-0039` | Graduated age-based AI restrictions | Establish graduated age-based restrictions for AI syste | healthcare.html |
| `HLTH-MHCS-0040` | Minor-accessible AI data limits | AI systems accessible to minors must include strict lim | healthcare.html |
| `HLTH-MHCS-0041` | No direct-to-consumer mental health AI treatment | AI systems may not be marketed or deployed as standalon | healthcare.html |
| `HLTH-MHCS-0042` | Limited crisis support AI | Limited use of AI systems for crisis support may be per | healthcare.html |
| `HLTH-MHCS-0043` | Clinical data consent for training | Mental health data from licensed providers therapy sess | healthcare.html |
| `HLTH-MHCS-0044` | Identifiable clinical data training prohibition | Use of identifiable clinical mental health data for AI  | healthcare.html |
| `HLTH-MHCS-0045` | Mental health interaction data storage limits | Mental health data generated through AI interactions ma | healthcare.html |
| `HLTH-MHCS-0046` | Robust de-identification for training data | All training data used in mental health AI systems must | healthcare.html |
| `HLTH-MHCS-0047` | No re-identification of anonymized data | AI systems must not be designed or used to re-identify  | healthcare.html |
| `HLTH-NETS-0001` | Adequate networks for all services | Health plans must maintain adequate networks for all co | healthcare.html |
| `HLTH-NETS-0002` | National networks required | Health plan networks must function nationally rather th | healthcare.html |
| `HLTH-NETS-0003` | Out-of-network coverage when network inadequate | If adequate in-network care is not available within rea | healthcare.html |
| `HLTH-NETS-0004` | No patient penalty for network failures | Patients may not be penalized for obtaining necessary c | healthcare.html |
| `HLTH-OVRG-0001` | Public reporting of coverage metrics | Coverage entities must publicly report denial rates app | healthcare.html |
| `HLTH-OVRG-0002` | Oversight authority and enforcement | Healthcare oversight bodies must have authority to inve | healthcare.html |
| `HLTH-OVRG-0003` | No hiding behind proprietary claims | Coverage entities may not hide harmful practices behind | healthcare.html |
| `HLTH-OVRG-0004` | Corrective action and suspension authority | Regulators must be empowered to require corrective acti | healthcare.html |
| `HLTH-PAUS-0001` | Strict limits on prior authorization | Prior authorization requirements must be strictly limit | healthcare.html |
| `HLTH-PAUS-0002` | Transparent prior authorization systems | Prior authorization systems must be transparent clinica | healthcare.html |
| `HLTH-PAUS-0003` | Reduce repeated prior authorization burden | Repeated approval of the same type of medically necessa | healthcare.html |
| `HLTH-PAUS-0004` | No prior authorization disruption of continuity | Prior authorization may not be used to disrupt continui | healthcare.html |
| `HLTH-RSRS-0001` | Increase funding for neglected conditions | Public healthcare and research policy must increase fun | healthcare.html |
| `HLTH-RSRS-0002` | Priority for stigmatized conditions | Research priorities should include stigmatized or less  | healthcare.html |
| `HLTH-RSRS-0003` | Resist commercial research bias | Healthcare governance should not allow commercial buzz  | healthcare.html |
| `HLTH-RXDG-0001` | Broad prescription access required | Drug coverage systems must include broad access to medi | healthcare.html |
| `HLTH-RXDG-0002` | Fast formulary exception pathways | Patients must have fast and meaningful exception pathwa | healthcare.html |
| `HLTH-RXDG-0003` | No harmful step-therapy loops | Coverage systems may not force repeated medication fail | healthcare.html |
| `HLTH-RXDG-0004` | Coverage for neglected condition medications | Coverage for medications should include neglected or un | healthcare.html |
| `HLTH-RXDG-0005` | Controlled substance quotas ensure access | Production quotas and regulatory limits on controlled m | healthcare.html |
| `HLTH-RXDG-0006` | No artificial medication shortages | Regulatory systems may not restrict supply of approved  | healthcare.html |
| `HLTH-RXDG-0007` | Quotas based on real-world demand | Controlled substance quotas must be based on real-world | healthcare.html |
| `HLTH-RXDG-0008` | Rapid response to medication shortages | When shortages of controlled medications occur regulato | healthcare.html |
| `HLTH-RXDG-0009` | No geographic medication access restrictions | Patients must be able to access prescribed controlled m | healthcare.html |
| `HLTH-RXDG-0010` | Balanced access expansion with safeguards | Expansion of access to controlled medications must be p | healthcare.html |
| `HLTH-RXDG-0011` | No patient-uncontrolled treatment disruption | Patients receiving ongoing treatment with controlled me | healthcare.html |
| `HLTH-STDS-0005` | Strict maximum response timelines | Healthcare coverage decisions and prior authorization d | healthcare.html |
| `HLTH-STDS-0006` | Accelerated urgent decision timelines | Urgent and emergency-related coverage determinations mu | healthcare.html |
| `HLTH-STDS-0007` | Presumptive approval if timelines missed | If a coverage decision is not made within required time | healthcare.html |
| `HLTH-STDS-0008` | No delay as denial strategy | Administrative delay may not be used as a strategy to a | healthcare.html |
| `HLTH-SUPR-0001` | Fund comprehensive supplement research through NCCIH | Supplement research funding | healthcare.html |
| `HLTH-SUPR-0002` | Reform supplement labeling to reflect actual evidence | Supplement labeling standards | healthcare.html |
| `HLTH-SUPR-0003` | Require independent laboratory testing and quality cert | Supplement lab transparency | healthcare.html |
| `HLTH-SUPR-0004` | Establish minimum quality standards for supplement manu | Minimum supplement quality standards | healthcare.html |
| `HLTH-TRAN-0001` | Regulate transition-state coverage systems | Until universal single-payer healthcare is implemented  | healthcare.html |
| `HLTH-TRAN-0002` | Immediate improvement without delay | Transition-state healthcare reform must be designed to  | healthcare.html |
| `HLTH-TRLS-0001` | Streamlined new treatment approvals | Approvals and trials for new treatments funded and stre | healthcare.html |
| `HOUS-CLTS-0001` | Community land trusts must be recognized and supported  | Government must recognize community land trusts and sha | housing.html |
| `HOUS-IZNS-0001` | Large residential developments must include affordable  | Residential developments above a defined unit threshold | housing.html |
| `HOUS-MHOS-0001` | Mobile home park residents must have protections agains | Residents of mobile home parks and manufactured housing | housing.html |
| `HOUS-PUBL-0001` | Government-owned or publicly administered housing must  | Public and social housing must be maintained as a perma | housing.html |
| `HOUS-SOIS-0001` | Landlords may not refuse housing based on lawful source | Landlords, property managers, and rental listing platfo | housing.html |
| `HOUS-TENS-0001` | Tenants must have enforceable rights to habitability, r | Tenants must have meaningful protection from retaliator | housing.html |
| `IMMG-ACCS-0001` | Access to Services | Immigration status may affect specific program eligibil | immigration.html |
| `IMMG-ACCS-0002` | Access to Services | Children within United States jurisdiction must have me | immigration.html |
| `IMMG-ACCS-0003` | Access to Services | Local access to healthcare schooling identification sup | immigration.html |
| `IMMG-ACCS-0004` | Access to Services | Public-service systems should provide clear multilingua | immigration.html |
| `IMMG-ACCS-0005` | Access to Services | Basic access to reporting crime seeking emergency help  | immigration.html |
| `IMMG-ACCS-0006` | Access to Services | State and local institutions may not use ordinary publi | immigration.html |
| `IMMG-ADML-0001` | Administration & Process | Immigration systems must be funded and staffed to reduc | immigration.html |
| `IMMG-ADML-0002` | Administration & Process | Administrative simplification should reduce complexity  | immigration.html |
| `IMMG-ADML-0003` | Administration & Process | People must have accessible status updates document acc | immigration.html |
| `IMMG-ADML-0004` | Administration & Process | Immigration forms notices deadlines and legal standards | immigration.html |
| `IMMG-ADML-0005` | Administration & Process | Backlog reduction efforts may not sacrifice accuracy du | immigration.html |
| `IMMG-ADML-0006` | Administration & Process | Immigration applicants must have clear access to case s | immigration.html |
| `IMMG-ADML-0007` | Administration & Process | Immigration agencies may not use contradictory document | immigration.html |
| `IMMG-ADML-0008` | Administration & Process | Where agency error delay or lost records materially har | immigration.html |
| `IMMG-ASYS-0001` | Asylum & Humanitarian Protection | People seeking asylum or humanitarian protection must h | immigration.html |
| `IMMG-ASYS-0002` | Asylum & Humanitarian Protection | Asylum systems may not rely on impossible deadlines ina | immigration.html |
| `IMMG-ASYS-0003` | Asylum & Humanitarian Protection | Credibility determinations in asylum and humanitarian c | immigration.html |
| `IMMG-ASYS-0004` | Asylum & Humanitarian Protection | People with credible fear or other serious protection c | immigration.html |
| `IMMG-ASYS-0005` | Asylum & Humanitarian Protection | Humanitarian protection systems must be designed to acc | immigration.html |
| `IMMG-ASYS-0006` | Asylum & Humanitarian Protection | Asylum and refugee procedures must include clear timely | immigration.html |
| `IMMG-ASYS-0007` | Asylum & Humanitarian Protection | Credible-fear and related threshold screenings must be  | immigration.html |
| `IMMG-ASYS-0008` | Asylum & Humanitarian Protection | People seeking asylum or refugee protection must have s | immigration.html |
| `IMMG-ASYS-0009` | Asylum & Humanitarian Protection | Asylum adjudication must account for trauma memory disr | immigration.html |
| `IMMG-ASYS-0010` | Asylum & Humanitarian Protection | Children survivors of trafficking survivors of gender-b | immigration.html |
| `IMMG-ASYS-0011` | Asylum & Humanitarian Protection | Detention may not be used to pressure abandonment of as | immigration.html |
| `IMMG-ASYS-0012` | Asylum & Humanitarian Protection | Asylum and refugee decisions must be explained clearly  | immigration.html |
| `IMMG-ASYS-0013` | Asylum & Humanitarian Protection | Return or removal decisions in protection cases must in | immigration.html |
| `IMMG-BRDS-0002` | Border Governance | Border enforcement powers must be clearly limited by co | immigration.html |
| `IMMG-BRDS-0003` | Border Governance | Use of force in border contexts must be strictly constr | immigration.html |
| `IMMG-BRDS-0004` | Border Governance | Border processing systems must be designed for order an | immigration.html |
| `IMMG-BRDS-0005` | Border Governance | Border enforcement may not be militarized in ways that  | immigration.html |
| `IMMG-BRDS-0006` | Border Governance | Border officials and agencies must be subject to strong | immigration.html |
| `IMMG-BRDS-0007` | Border Governance | Independent review mechanisms must investigate deaths a | immigration.html |
| `IMMG-BRDS-0008` | Border Governance | Border enforcement may not use deprivation of food wate | immigration.html |
| `IMMG-BRDS-0009` | Border Governance | Border processing facilities must meet humane standards | immigration.html |
| `IMMG-BRDS-0010` | Border Governance | Emergency border powers may not be used as permanent su | immigration.html |
| `IMMG-CITS-0001` | Citizenship & Naturalization | Pathways to citizenship should be clear affordable and  | immigration.html |
| `IMMG-CITS-0002` | Citizenship & Naturalization | Citizenship systems should not be structured to preserv | immigration.html |
| `IMMG-CITS-0003` | Citizenship & Naturalization | Birthright citizenship must remain explicit and protect | immigration.html |
| `IMMG-CITS-0004` | Citizenship & Naturalization | Long-term lawful residents should have fair and stable  | immigration.html |
| `IMMG-CITS-0005` | Citizenship & Naturalization | Naturalization systems should be clear affordable timel | immigration.html |
| `IMMG-CITS-0006` | Citizenship & Naturalization | Citizenship eligibility processes should not be distort | immigration.html |
| `IMMG-CITS-0007` | Citizenship & Naturalization | Long-term lawful residents should not remain in extende | immigration.html |
| `IMMG-CITS-0008` | Citizenship & Naturalization | Naturalization procedures should include accessible lan | immigration.html |
| `IMMG-CITS-0009` | Citizenship & Naturalization | The citizenship process may include lawful standards fo | immigration.html |
| `IMMG-CITS-0010` | Citizenship & Naturalization | Fees and procedural burdens in citizenship processes sh | immigration.html |
| `IMMG-CLMS-0001` | Create a climate displacement visa category for people  | The United States must establish a humanitarian visa ca | immigration.html |
| `IMMG-CONS-0001` | Contractor Accountability | Private contractors involved in immigration processing  | immigration.html |
| `IMMG-CONS-0002` | Contractor Accountability | Immigration contractors may not claim secrecy proprieta | immigration.html |
| `IMMG-CONS-0003` | Contractor Accountability | Contractors performing immigration-related functions mu | immigration.html |
| `IMMG-CONS-0004` | Contractor Accountability | No contractor compensation structure may reward detenti | immigration.html |
| `IMMG-CONS-0005` | Contractor Accountability | Immigration-service contracts must prioritize rights pr | immigration.html |
| `IMMG-CONS-0006` | Contractor Accountability | Government may not fragment immigration functions acros | immigration.html |
| `IMMG-CONS-0007` | Contractor Accountability | People harmed by immigration contractors must have full | immigration.html |
| `IMMG-CONS-0008` | Contractor Accountability | Independent oversight bodies must have full access to c | immigration.html |
| `IMMG-CONS-0009` | Contractor Accountability | Immigration enforcement detention adjudication and core | immigration.html |
| `IMMG-CONS-0010` | Contractor Accountability | Core immigration functions include detention custody tr | immigration.html |
| `IMMG-CONS-0011` | Contractor Accountability | Limited use of contractors may be permitted for non-cor | immigration.html |
| `IMMG-CONS-0012` | Contractor Accountability | Contractors may not exercise authority over individuals | immigration.html |
| `IMMG-CONS-0013` | Contractor Accountability | No compensation structure may reward detention volume e | immigration.html |
| `IMMG-CONS-0014` | Contractor Accountability | Government entities may not indirectly outsource core i | immigration.html |
| `IMMG-CONS-0015` | Contractor Accountability | All permitted contractors must be subject to full publi | immigration.html |
| `IMMG-CONS-0016` | Contractor Accountability | Individuals harmed by contractor actions must have full | immigration.html |
| `IMMG-CRTS-0001` | Courts & Adjudication | Immigration adjudication systems must be structured for | immigration.html |
| `IMMG-CRTS-0002` | Courts & Adjudication | Immigration courts or equivalent adjudicative bodies sh | immigration.html |
| `IMMG-CRTS-0003` | Courts & Adjudication | People in immigration proceedings must have clear acces | immigration.html |
| `IMMG-CRTS-0004` | Courts & Adjudication | Adjudicators in immigration systems must receive trauma | immigration.html |
| `IMMG-DATA-0001` | Data Privacy & Surveillance | Immigration systems may not use broad data surveillance | immigration.html |
| `IMMG-DATA-0002` | Data Privacy & Surveillance | Data-sharing between immigration systems and other gove | immigration.html |
| `IMMG-DATA-0003` | Data Privacy & Surveillance | Immigration data must be treated as highly sensitive an | immigration.html |
| `IMMG-DATA-0004` | Data Privacy & Surveillance | Record systems must include correction mechanisms so pe | immigration.html |
| `IMMG-DETS-0001` | Detention & Custody | Immigration detention must be strictly limited and may  | immigration.html |
| `IMMG-DETS-0002` | Detention & Custody | Indefinite immigration detention is prohibited | immigration.html |
| `IMMG-DETS-0003` | Detention & Custody | Detention conditions must meet strong standards for hea | immigration.html |
| `IMMG-DETS-0004` | Detention & Custody | Alternatives to detention should be preferred where app | immigration.html |
| `IMMG-DETS-0005` | Detention & Custody | Immigration detention must be subject to prompt individ | immigration.html |
| `IMMG-DETS-0006` | Detention & Custody | Use of offshore or legally exceptional detention struct | immigration.html |
| `IMMG-DETS-0007` | Detention & Custody | Private immigration detention facilities are prohibited | immigration.html |
| `IMMG-DETS-0008` | Detention & Custody | Detention custody transportation or confinement of immi | immigration.html |
| `IMMG-DETS-0009` | Detention & Custody | Government may not use private contractors to evade acc | immigration.html |
| `IMMG-DETS-0010` | Detention & Custody | Any non-private immigration detention or custody settin | immigration.html |
| `IMMG-DETS-0011` | Detention & Custody | Deaths injuries medical neglect sexual abuse and seriou | immigration.html |
| `IMMG-DETS-0012` | Detention & Custody | Contractor or agency employees involved in immigration  | immigration.html |
| `IMMG-DOCS-0001` | Documentation & Identity | Immigration and travel document systems must respect up | immigration.html |
| `IMMG-DOCS-0002` | Documentation & Identity | Removal of sex and gender markers from passports and id | immigration.html |
| `IMMG-DUES-0001` | Due Process & Rights | People in immigration proceedings must have meaningful  | immigration.html |
| `IMMG-DUES-0002` | Due Process & Rights | People must have timely access to counsel or accredited | immigration.html |
| `IMMG-DUES-0003` | Due Process & Rights | Immigration proceedings may not rely on rushed scheduli | immigration.html |
| `IMMG-DUES-0004` | Due Process & Rights | Immigration decisions must be reviewable and may not be | immigration.html |
| `IMMG-DUES-0005` | Due Process & Rights | Interpretation and translation services must be availab | immigration.html |
| `IMMG-DUES-0006` | Due Process & Rights | All persons within the United States or under the custo | immigration.html |
| `IMMG-DUES-0007` | Due Process & Rights | Immigration status may not be used to deny or diminish  | immigration.html |
| `IMMG-DUES-0008` | Due Process & Rights | Individuals in immigration detention or proceedings mus | immigration.html |
| `IMMG-DUES-0009` | Due Process & Rights | Habeas corpus protections apply fully to all individual | immigration.html |
| `IMMG-DUES-0010` | Due Process & Rights | Immigration detention and removal decisions must remain | immigration.html |
| `IMMG-DUES-0011` | Due Process & Rights | No category of person within United States jurisdiction | immigration.html |
| `IMMG-ENFL-0001` | Enforcement Structure | Immigration and Customs Enforcement in its current form | immigration.html |
| `IMMG-ENFL-0002` | Enforcement Structure | Any replacement immigration-enforcement structure must  | immigration.html |
| `IMMG-ENFL-0003` | Enforcement Structure | Immigration enforcement agencies may not use broad disc | immigration.html |
| `IMMG-ENFL-0004` | Enforcement Structure | Immigration enforcement functions must be structurally  | immigration.html |
| `IMMG-ENFL-0005` | Enforcement Structure | Replacement structures must include strong anti-abuse s | immigration.html |
| `IMMG-FAMS-0001` | Family Unity & Protection | Family separation in immigration enforcement is prohibi | immigration.html |
| `IMMG-FAMS-0002` | Family Unity & Protection | Immigration systems must prioritize family unity and pr | immigration.html |
| `IMMG-FAMS-0003` | Family Unity & Protection | Children in immigration systems must receive heightened | immigration.html |
| `IMMG-FAMS-0004` | Family Unity & Protection | Families may not be coerced into waiver or removal deci | immigration.html |
| `IMMG-INTL-0001` | Integration & Support | Immigration policy should support stable local integrat | immigration.html |
| `IMMG-INTL-0002` | Integration & Support | People with pending lawful-status or protection claims  | immigration.html |
| `IMMG-INTL-0003` | Integration & Support | Administrative limbo should not be treated as an accept | immigration.html |
| `IMMG-INTL-0004` | Integration & Support | Immigration-system design should reduce fear-driven avo | immigration.html |
| `IMMG-LABS-0001` | Labor Protections | Immigration status may not be used by employers to supp | immigration.html |
| `IMMG-LABS-0002` | Labor Protections | All workers regardless of immigration status must be pr | immigration.html |
| `IMMG-LABS-0003` | Labor Protections | Reporting labor abuse wage theft trafficking or unsafe  | immigration.html |
| `IMMG-LABS-0004` | Labor Protections | Visa and work authorization systems must be designed to | immigration.html |
| `IMMG-LABS-0005` | Labor Protections | Pathways tied to labor participation should not functio | immigration.html |
| `IMMG-LABS-0006` | Labor Protections | Visa and work authorization systems may not be structur | immigration.html |
| `IMMG-LABS-0007` | Labor Protections | Workers on employer-tied visas must have meaningful por | immigration.html |
| `IMMG-LABS-0008` | Labor Protections | Immigration-dependent labor systems must include safegu | immigration.html |
| `IMMG-LABS-0009` | Labor Protections | Workers pursuing labor claims safety claims or traffick | immigration.html |
| `IMMG-LABS-0010` | Labor Protections | Immigration pathways connected to labor should prioriti | immigration.html |
| `IMMG-OVRG-0001` | Oversight & Transparency | Immigration agencies and detention systems must be subj | immigration.html |
| `IMMG-OVRG-0002` | Oversight & Transparency | Immigration systems must publish standardized data on d | immigration.html |
| `IMMG-OVRG-0003` | Oversight & Transparency | Patterns of abuse rights violations discriminatory enfo | immigration.html |
| `IMMG-OVRG-0004` | Oversight & Transparency | Immigration officials and agencies may not evade accoun | immigration.html |
| `IMMG-REFS-0001` | Refugee Resettlement | The United States should maintain a robust refugee rese | immigration.html |
| `IMMG-REFS-0002` | Refugee Resettlement | Refugee admissions and resettlement may not be arbitrar | immigration.html |
| `IMMG-REFS-0003` | Refugee Resettlement | Refugee systems must include predictable processing cap | immigration.html |
| `IMMG-REFS-0005` | Refugee Resettlement | Refugee eligibility and processing standards must be cl | immigration.html |
| `IMMG-REFS-0007` | Refugee Resettlement | Refugee systems should coordinate with state and local  | immigration.html |
| `IMMG-REFS-0008` | Refugee Resettlement | Refugees should have clear pathways from initial admiss | immigration.html |
| `IMMG-REFS-0010` | Refugee Resettlement | Refugee systems must be subject to strong public oversi | immigration.html |
| `IMMG-REMS-0001` | Removal & Deportation | People may not be deported to countries that are not th | immigration.html |
| `IMMG-REMS-0002` | Removal & Deportation | Removal may not be carried out to any country where the | immigration.html |
| `IMMG-REMS-0003` | Removal & Deportation | Third-country removals require strict legal standards m | immigration.html |
| `IMMG-REMS-0004` | Removal & Deportation | Removal proceedings must include meaningful notice acce | immigration.html |
| `IMMG-REMS-0005` | Removal & Deportation | No person may be deported while a timely appeal motion  | immigration.html |
| `IMMG-REMS-0006` | Removal & Deportation | Removal orders must be based on individualized review a | immigration.html |
| `IMMG-REMS-0007` | Removal & Deportation | People facing removal must have access to the full fact | immigration.html |
| `IMMG-REMS-0008` | Removal & Deportation | Immigration systems must include strong safeguards agai | immigration.html |
| `IMMG-REMS-0009` | Removal & Deportation | Where credible evidence suggests a removal may be unlaw | immigration.html |
| `IMMG-REMS-0010` | Removal & Deportation | Wrongful removal must trigger mandatory review accounta | immigration.html |
| `IMMG-REMS-0011` | Removal & Deportation | Removal decisions must account for family unity caregiv | immigration.html |
| `IMMG-REMS-0012` | Removal & Deportation | People may not be removed in ways that knowingly cut of | immigration.html |
| `IMMG-REMS-0013` | Removal & Deportation | Removal procedures involving children families disabled | immigration.html |
| `IMMG-REMS-0014` | Removal & Deportation | Government agencies must publicly report standardized d | immigration.html |
| `IMMG-REMS-0015` | Removal & Deportation | Expedited or summary removal procedures must be strictl | immigration.html |
| `IMMG-REMS-0016` | Removal & Deportation | Removal transport and handoff procedures must be docume | immigration.html |
| `IMMG-RGTS-0001` | Core Rights Principles | Immigration policy must respect human rights due proces | immigration.html |
| `IMMG-RGTS-0002` | Core Rights Principles | Immigration systems may not rely on cruelty degradation | immigration.html |
| `IMMG-RGTS-0003` | Core Rights Principles | Immigration law and administration must be clear consis | immigration.html |
| `IMMG-RGTS-0004` | Core Rights Principles | Geography language wealth or access to counsel must not | immigration.html |
| `IMMG-RGTS-0005` | Core Rights Principles | Immigration policy enforcement and adjudication may not | immigration.html |
| `IMMG-RGTS-0006` | Core Rights Principles | Immigration rules criteria and processes must be writte | immigration.html |
| `IMMG-RGTS-0007` | Core Rights Principles | Selective enforcement targeting based on protected char | immigration.html |
| `IMMG-RGTS-0008` | Core Rights Principles | The United States may not create parallel systems of ju | immigration.html |
| `IMMG-RGTS-0009` | Core Rights Principles | Differences in immigration status may affect specific l | immigration.html |
| `IMMG-SRVS-0001` | Services & Sanctuary | People within United States jurisdiction must have acce | immigration.html |
| `IMMG-SRVS-0002` | Services & Sanctuary | Seeking emergency care basic healthcare or medically ne | immigration.html |
| `IMMG-SRVS-0003` | Services & Sanctuary | Immigration status may not be used to deny medically ne | immigration.html |
| `IMMG-SRVS-0004` | Services & Sanctuary | Children within United States jurisdiction must have me | immigration.html |
| `IMMG-SRVS-0005` | Services & Sanctuary | Schools and educational institutions may not be convert | immigration.html |
| `IMMG-SRVS-0006` | Services & Sanctuary | Immigration-related fear must not be allowed to undermi | immigration.html |
| `IMMG-SRVS-0007` | Services & Sanctuary | Essential public-service systems should include firewal | immigration.html |
| `IMMG-SRVS-0008` | Services & Sanctuary | Routine use of healthcare schools shelters labor agenci | immigration.html |
| `IMMG-SRVS-0009` | Services & Sanctuary | Public institutions must provide clear multilingual gui | immigration.html |
| `IMMG-SRVS-0010` | Services & Sanctuary | Where immigration status affects eligibility for specif | immigration.html |
| `IMMG-SRVS-0011` | Services & Sanctuary | Benefit systems must not use confusing status rules con | immigration.html |
| `IMMG-SRVS-0012` | Services & Sanctuary | Children mixed-status families and other vulnerable hou | immigration.html |
| `IMMG-STSS-0001` | Status & Pathways | Immigration policy should provide realistic lawful path | immigration.html |
| `IMMG-STSS-0002` | Status & Pathways | Status-adjustment systems should be clear affordable an | immigration.html |
| `IMMG-STSS-0003` | Status & Pathways | People brought to the country as children or raised sub | immigration.html |
| `IMMG-STSS-0004` | Status & Pathways | Immigration law should reduce long-term undocumented li | immigration.html |
| `IMMG-STSS-0005` | Status & Pathways | Status eligibility should account for family unity labo | immigration.html |
| `IMMG-STSS-0006` | Status & Pathways | The overall system for obtaining visas green cards perm | immigration.html |
| `IMMG-STSS-0007` | Status & Pathways | Visa and permanent-residence systems should be simplifi | immigration.html |
| `IMMG-STSS-0008` | Status & Pathways | Application fees and procedural burdens for visas green | immigration.html |
| `IMMG-STSS-0009` | Status & Pathways | Backlogs in family-based employment-based and humanitar | immigration.html |
| `IMMG-STSS-0010` | Status & Pathways | Lawful-status systems must include clearer timelines st | immigration.html |
| `IMMG-STSS-0011` | Status & Pathways | Status pathways must be designed to reduce dependency o | immigration.html |
| `IMMG-STSS-0012` | Status & Pathways | Long-term temporary-status limbo should be reduced by c | immigration.html |
| `IMMG-SYSR-0001` | System Design | Lawful immigration pathways should be designed to reduc | immigration.html |
| `IMMG-SYSR-0002` | System Design | Immigration policy should be designed to reduce limbo f | immigration.html |
| `IMMG-SYSR-0003` | System Design | Immigration systems must be evaluated not only for enfo | immigration.html |
| `IMMG-SYSR-0004` | System Design | Any future immigration reforms must be tested against a | immigration.html |
| `IMMG-TRFS-0001` | Trafficking Protections | Immigration systems must include strong protections for | immigration.html |
| `IMMG-TRFS-0002` | Trafficking Protections | People reporting trafficking forced labor or coercive e | immigration.html |
| `IMMG-TRFS-0003` | Trafficking Protections | Trafficking-related immigration protections must be acc | immigration.html |
| `IMMG-TRFS-0004` | Trafficking Protections | Immigration and labor systems should coordinate to iden | immigration.html |
| `IMMG-TRFS-0005` | Trafficking Protections | Survivors of trafficking and severe exploitation should | immigration.html |
| `IMMG-VISS-0001` | Visas & Legal Immigration | Visa categories and lawful-entry pathways should be mod | immigration.html |
| `IMMG-VISS-0002` | Visas & Legal Immigration | Immigration pathways should be structured to reduce ext | immigration.html |
| `IMMG-VISS-0003` | Visas & Legal Immigration | Green-card and permanent-residence systems should have  | immigration.html |
| `IMMG-VISS-0004` | Visas & Legal Immigration | Applicants for visas green cards and permanent residenc | immigration.html |
| `IMMG-VISS-0005` | Visas & Legal Immigration | Application requirements should be simplified and stand | immigration.html |
| `IMMG-VISS-0006` | Visas & Legal Immigration | Fees for visas green cards and permanent residence shou | immigration.html |
| `IMMG-VISS-0007` | Visas & Legal Immigration | Family-based and humanitarian pathways should not be st | immigration.html |
| `IMMG-VISS-0008` | Visas & Legal Immigration | Long-term residents with stable ties should have realis | immigration.html |
| `IMMG-VISS-0009` | Visas & Legal Immigration | Immigration pathways should be resilient against admini | immigration.html |
| `IMMG-VISS-0010` | Visas & Legal Immigration | The visa system must be comprehensively modernized to r | immigration.html |
| `IMMG-VISS-0011` | Visas & Legal Immigration | Visa categories should be simplified clarified and reor | immigration.html |
| `IMMG-VISS-0012` | Visas & Legal Immigration | Overlapping or contradictory visa rules should be reduc | immigration.html |
| `IMMG-VISS-0013` | Visas & Legal Immigration | Visa pathways should be designed to reflect real family | immigration.html |
| `IMMG-VISS-0014` | Visas & Legal Immigration | Visa adjudications must operate under transparent targe | immigration.html |
| `IMMG-VISS-0015` | Visas & Legal Immigration | Applicants must have meaningful access to real-time cas | immigration.html |
| `IMMG-VISS-0016` | Visas & Legal Immigration | Administrative delay may not be used as a de facto deni | immigration.html |
| `IMMG-VISS-0017` | Visas & Legal Immigration | Visa adjudication standards must be clear consistent an | immigration.html |
| `IMMG-VISS-0018` | Visas & Legal Immigration | Requests for documentation or proof in visa cases must  | immigration.html |
| `IMMG-VISS-0019` | Visas & Legal Immigration | Applicants must have meaningful opportunities to correc | immigration.html |
| `IMMG-VISS-0020` | Visas & Legal Immigration | Employment-based visa systems must reduce dependency on | immigration.html |
| `IMMG-VISS-0021` | Visas & Legal Immigration | Student and trainee visa systems must protect against e | immigration.html |
| `IMMG-VISS-0022` | Visas & Legal Immigration | Temporary visa systems should not be designed to keep p | immigration.html |
| `IMMG-VISS-0023` | Visas & Legal Immigration | Family-based visa systems should prioritize reunificati | immigration.html |
| `IMMG-VISS-0024` | Visas & Legal Immigration | Family-based applicants should not face excessive docum | immigration.html |
| `IMMG-VISS-0025` | Visas & Legal Immigration | Visa fees must be regulated so they cover legitimate ad | immigration.html |
| `IMMG-VISS-0026` | Visas & Legal Immigration | Fee waivers reductions or public support should be avai | immigration.html |
| `IMMG-VISS-0027` | Visas & Legal Immigration | Visa systems should include clear mechanisms for transi | immigration.html |
| `IMMG-VISS-0028` | Visas & Legal Immigration | People should not be forced into repeated cycles of tem | immigration.html |
| `IMMG-VISS-0029` | Visas & Legal Immigration | Applicants already in lawful immigration processes shou | immigration.html |
| `IMMG-VISS-0030` | Visas & Legal Immigration | Major changes to visa systems should include transition | immigration.html |
| `INFR-AFDS-0001` | Internet, electricity, and water must be affordable to  | Federal law must establish affordability standards and  | infrastructure-and-public-goods.html |
| `INFR-BLDS-0002` | Carbon-Neutral Infrastructure | Require infrastructure systems and buildouts to be carb | information-and-media.html |
| `INFR-ENRS-0004` | End Fossil Fuel Subsidies | End oil and coal subsidies | information-and-media.html |
| `INFR-ENRS-0005` | Guarantee Fossil Fuel Phaseout | Guarantee phaseout of oil and coal for energy productio | information-and-media.html |
| `INFR-EQJS-0001` | Infrastructure siting decisions must not disproportiona | Major infrastructure siting decisions — including highw | infrastructure-and-public-goods.html |
| `INFR-GRDS-0003` | Carbon-Neutral Power Grid | Require a carbon-neutral or carbon-negative power grid | information-and-media.html |
| `INFR-LBRS-0001` | All federally funded infrastructure projects must pay p | All infrastructure projects receiving federal funding,  | infrastructure-and-public-goods.html |
| `INFR-RAIL-0001` | Modernize Rail System | Modernize the U | information-and-media.html |
| `INFR-TRAN-0002` | Prioritize Accessible Public Transit | Prioritize reliable affordable and accessible public tr | information-and-media.html |
| `INFR-TRAN-0004` | Require Hybrid Capability in Transition | Require at minimum plug-in hybrid capability during tra | information-and-media.html |
| `INFR-TRAN-0005` | Strict Fuel Efficiency Standards | Establish extremely strict fuel-efficiency standards du | information-and-media.html |
| `JUST-AINL-0001` | Ban AI sentencing determinations | AI systems may not be used to determine or recommend cr | equal-justice-and-policing.html |
| `JUST-AINL-0002` | Ban AI recidivism predictions in sentencing | AI risk assessment tools predicting recidivism dangerou | equal-justice-and-policing.html |
| `JUST-AINL-0003` | AI for wrongful conviction identification | AI may be used to assist in identifying wrongful convic | equal-justice-and-policing.html |
| `JUST-AINL-0004` | AI for bias identification under oversight | AI systems should be used to identify and mitigate bias | equal-justice-and-policing.html |
| `JUST-AINL-0005` | AI evidence transparency requirements | AI-generated evidence or analysis may not be used in co | equal-justice-and-policing.html |
| `JUST-AINL-0006` | Right to examine AI systems | Defendants must have the right to examine challenge and | equal-justice-and-policing.html |
| `JUST-AINL-0007` | Ban AI juror profiling | AI systems may not be used to profile rank or exclude j | equal-justice-and-policing.html |
| `JUST-AINL-0008` | Ban AI prosecutorial automation | AI systems may not be used to recommend or automate pro | equal-justice-and-policing.html |
| `JUST-AINL-0009` | Mandatory AI disclosure | All use of AI in legal proceedings must be disclosed to | equal-justice-and-policing.html |
| `JUST-AINL-0010` | AI evidence validity standards | AI evidence must meet strict reliability and scientific | equal-justice-and-policing.html |
| `JUST-BALS-0001` | End cash bail systems | End or sharply limit cash bail systems that criminalize | equal-justice-and-policing.html |
| `JUST-BALS-0002` | Limit pretrial detention | Pretrial detention must be limited to cases with clear  | equal-justice-and-policing.html |
| `JUST-BALS-0003` | Ban AI bail risk scores | AI systems may not be used to assign bail or pretrial r | equal-justice-and-policing.html |
| `JUST-BALS-0004` | Least restrictive pretrial conditions | Pretrial release decisions must favor the least restric | equal-justice-and-policing.html |
| `JUST-CIVL-0001` | Meaningful civil court access | People must have meaningful access to civil courts for  | equal-justice-and-policing.html |
| `JUST-CIVL-0002` | Ban or limit forced arbitration | Forced arbitration clauses that strip people of meaning | equal-justice-and-policing.html |
| `JUST-CIVL-0003` | Preserve class actions | Class actions and collective remedies must remain avail | equal-justice-and-policing.html |
| `JUST-CIVL-0004` | Eliminate fee barriers to justice | Court fees filing costs and procedural burdens must not | equal-justice-and-policing.html |
| `JUST-CONS-0001` | Retain human rights in custody | People in custody retain human rights including access  | equal-justice-and-policing.html |
| `JUST-CONS-0002` | Ban or limit solitary confinement | Solitary confinement must be banned or strictly limited | equal-justice-and-policing.html |
| `JUST-CONS-0003` | Mental health treatment in custody | Mental health needs in custody must be treated medicall | equal-justice-and-policing.html |
| `JUST-CONS-0004` | Disability access in detention | Disability access and accommodation must be guaranteed  | equal-justice-and-policing.html |
| `JUST-CONS-0005` | Independent facility inspections | Independent inspections and public reporting are requir | equal-justice-and-policing.html |
| `JUST-CRTS-0001` | Design for intelligibility | Justice systems must be designed for intelligibility an | equal-justice-and-policing.html |
| `JUST-CRTS-0002` | Accessible court participation | Courts must provide accessible notice scheduling and pa | equal-justice-and-policing.html |
| `JUST-CRTS-0003` | Remote tools preserve due process | Remote participation tools may improve access but may n | equal-justice-and-policing.html |
| `JUST-CRTS-0004` | Reduce procedural traps | Justice institutions must identify and reduce procedura | equal-justice-and-policing.html |
| `JUST-DEFS-0001` | Right to competent counsel | Every person facing serious criminal charges must have  | equal-justice-and-policing.html |
| `JUST-DEFS-0002` | Public defense funding parity | Public defense systems must be funded at levels suffici | equal-justice-and-policing.html |
| `JUST-DEFS-0003` | Timely access to evidence | Defendants must have timely access to discovery evidenc | equal-justice-and-policing.html |
| `JUST-DEFS-0004` | Prevent procedural delay undermining defense | Courts must not permit procedural delay or administrati | equal-justice-and-policing.html |
| `JUST-DEFS-0005` | Right to challenge evidence validity | Defendants must have the right to challenge the scienti | equal-justice-and-policing.html |
| `JUST-DEFS-0006` | Broad timely disclosure | Disclosure obligations must be broad continuing and tim | equal-justice-and-policing.html |
| `JUST-DEFS-0007` | Preserve exculpatory evidence | Prosecutors and law enforcement must preserve potential | equal-justice-and-policing.html |
| `JUST-DEFS-0008` | Enforce disclosure failures | Failure to disclose material evidence should carry enfo | equal-justice-and-policing.html |
| `JUST-DEFS-0009` | Expert assistance access | Defendants must have meaningful access to expert assist | equal-justice-and-policing.html |
| `JUST-DEFS-0010` | Prevent resource imbalance advantage | Procedural rules must not be structured in ways that re | equal-justice-and-policing.html |
| `JUST-DRGS-0003` | Redirect to treatment | Redirect funding to treatment | equal-justice-and-policing.html |
| `JUST-DRGS-0005` | No overdose assistance penalty | No penalty for overdose assistance | equal-justice-and-policing.html |
| `JUST-EVDS-0001` | Forensic scientific validity | Forensic methods used in court must meet strict scienti | equal-justice-and-policing.html |
| `JUST-EVDS-0002` | Exclude junk science | Junk science and unsupported forensic techniques must b | equal-justice-and-policing.html |
| `JUST-EVDS-0003` | Chain-of-custody standards | Digital and physical evidence must maintain transparent | equal-justice-and-policing.html |
| `JUST-EVDS-0004` | Identify synthetic evidence | Synthetic or AI-generated evidence must be clearly iden | equal-justice-and-policing.html |
| `JUST-EVDS-0005` | Review when science discredited | When foundational science behind a conviction is later  | equal-justice-and-policing.html |
| `JUST-FFFS-0001` | Ban revenue-extraction justice | Justice systems must not use fines fees and monetary pe | equal-justice-and-policing.html |
| `JUST-FFFS-0002` | Assess ability to pay | Ability to pay must be assessed before imposing or enfo | equal-justice-and-policing.html |
| `JUST-FFFS-0003` | Ban incarceration for inability to pay | People may not be incarcerated detained or otherwise de | equal-justice-and-policing.html |
| `JUST-FFFS-0004` | Limit compounding penalties | Late fees interest penalties and compounding charges in | equal-justice-and-policing.html |
| `JUST-FFFS-0005` | Accessible payment alternatives | Courts and agencies must provide accessible alternative | equal-justice-and-policing.html |
| `JUST-FFFS-0006` | Ban justice revenue dependency | Justice institutions may not depend on fines fees or ci | equal-justice-and-policing.html |
| `JUST-IMMS-0001` | Due process limits on immigration detention | Immigration detention must be subject to strict due pro | equal-justice-and-policing.html |
| `JUST-IMMS-0002` | Immigration counsel access | People in immigration proceedings must have meaningful  | equal-justice-and-policing.html |
| `JUST-IMMS-0003` | Ban coercive family separation | Family separation and coercive detention practices must | equal-justice-and-policing.html |
| `JUST-JUVS-0001` | Prioritize rehabilitation for youth | Juvenile justice systems must prioritize rehabilitation | equal-justice-and-policing.html |
| `JUST-JUVS-0002` | Limit adult sentencing for children | Children may not be subjected to adult sentencing stand | equal-justice-and-policing.html |
| `JUST-JUVS-0003` | Automatic juvenile record sealing | Juvenile records should be sealed or expunged automatic | equal-justice-and-policing.html |
| `JUST-JUVS-0004` | Youth custody services | Youth in custody must retain access to education mental | equal-justice-and-policing.html |
| `JUST-LAWS-0001` | Abolish qualified immunity | Qualified immunity is abolished and may not be used to  | equal-justice-and-policing.html |
| `JUST-LAWS-0002` | Government official accountability | Government officials including law enforcement must be  | equal-justice-and-policing.html |
| `JUST-LAWS-0003` | Remove prior-case-law requirement | Legal standards for accountability must not require vic | equal-justice-and-policing.html |
| `JUST-LAWS-0004` | Indemnification limits | Governments may provide indemnification for officials a | equal-justice-and-policing.html |
| `JUST-LNGS-0001` | Interpretation at every stage | People involved in justice proceedings must have meanin | equal-justice-and-policing.html |
| `JUST-LNGS-0002` | Free language access | Interpreter and translation access must be provided wit | equal-justice-and-policing.html |
| `JUST-LNGS-0003` | Language failures not harmless | Language access failures may not be treated as harmless | equal-justice-and-policing.html |
| `JUST-LNGS-0004` | Limit automated translation | Critical justice proceedings may not rely solely on aut | equal-justice-and-policing.html |
| `JUST-LNGS-0005` | Proactive language-access identification | Justice institutions must proactively identify language | equal-justice-and-policing.html |
| `JUST-OVRG-0001` | Publish standardized justice data | Justice institutions must publish standardized data on  | equal-justice-and-policing.html |
| `JUST-OVRG-0002` | Disaggregate disparity data | Justice data must be disaggregated to identify racial g | equal-justice-and-policing.html |
| `JUST-OVRG-0004` | Require action on audit findings | Justice agencies must be required to act on audit findi | equal-justice-and-policing.html |
| `JUST-POLC-0013` | Preserve and disclose misconduct records | Law enforcement misconduct records relevant to credibil | equal-justice-and-policing.html |
| `JUST-POLC-0014` | Disclose Brady and Giglio material | Prosecutors must disclose credibility-related misconduc | equal-justice-and-policing.html |
| `JUST-POLC-0015` | Consequences for officer dishonesty | Police officers with substantiated records of dishonest | equal-justice-and-policing.html |
| `JUST-POLC-0016` | Ban misconduct concealment | Law enforcement agencies may not use internal secrecy c | equal-justice-and-policing.html |
| `JUST-POLC-0017` | Track misconduct across jurisdictions | Independent systems should track officer misconduct pat | equal-justice-and-policing.html |
| `JUST-PROS-0001` | Ban coercive charging | Prosecutors may not use charging decisions to coerce pl | equal-justice-and-policing.html |
| `JUST-PROS-0002` | Automatic exculpatory disclosure | Prosecutors must disclose exculpatory evidence fully pr | equal-justice-and-policing.html |
| `JUST-PROS-0003` | Ban retaliatory prosecution | Retaliatory or politically motivated prosecution is pro | equal-justice-and-policing.html |
| `JUST-PROS-0004` | Prosecutorial transparency and audit | Prosecutorial offices must be subject to transparency a | equal-justice-and-policing.html |
| `JUST-PROS-0005` | Ban AI prosecutorial automation | AI systems may not independently recommend charges plea | equal-justice-and-policing.html |
| `JUST-PRPS-0001` | Ban or limit civil forfeiture | Civil forfeiture should be banned or strictly limited a | equal-justice-and-policing.html |
| `JUST-PRPS-0003` | Ban forfeiture as revenue | Justice agencies may not rely on forfeiture or seized a | equal-justice-and-policing.html |
| `JUST-PRPS-0004` | Ban civil forfeiture without conviction | Civil asset forfeiture is prohibited and property may n | equal-justice-and-policing.html |
| `JUST-PRPS-0005` | Strict limits on temporary seizure | Temporary seizure of property prior to conviction must  | equal-justice-and-policing.html |
| `JUST-PRPS-0006` | Accessible seizure contest processes | Property owners must have meaningful accessible and tim | equal-justice-and-policing.html |
| `JUST-RECS-0001` | Broad expungement access | People should have broad access to sealing expungement  | equal-justice-and-policing.html |
| `JUST-RECS-0002` | Automatic expungement | Expungement and sealing should be automatic in many cat | equal-justice-and-policing.html |
| `JUST-RECS-0003` | Automatic juvenile sealing | Juvenile records should be sealed or expunged automatic | equal-justice-and-policing.html |
| `JUST-RECS-0004` | Seal dismissed and acquitted charges | Dismissed charges acquittals and invalidated conviction | equal-justice-and-policing.html |
| `JUST-RECS-0005` | Honor expungement in systems | Background-check systems and public records systems mus | equal-justice-and-policing.html |
| `JUST-RECS-0006` | Accessible record correction | People must have accessible processes to correct errors | equal-justice-and-policing.html |
| `JUST-REIS-0001` | Reduce collateral consequences | People completing sentences should not face unnecessary | equal-justice-and-policing.html |
| `JUST-REIS-0002` | Limit collateral consequences | Collateral consequences must be reviewed limited and ti | equal-justice-and-policing.html |
| `JUST-REIS-0003` | Reentry support services | Reentry support should include access to identification | equal-justice-and-policing.html |
| `JUST-REIS-0004` | Prioritize reintegration | Justice policy should prioritize reintegration and stab | equal-justice-and-policing.html |
| `JUST-REVS-0001` | Expand post-conviction review | Post-conviction review processes must be expanded and a | equal-justice-and-policing.html |
| `JUST-REVS-0003` | Wrongful conviction triggers review | Wrongful-conviction indicators must trigger mandatory r | equal-justice-and-policing.html |
| `JUST-REVS-0004` | AI for wrongful conviction patterns | AI may be used to identify patterns of wrongful convict | equal-justice-and-policing.html |
| `JUST-REVS-0005` | No artificial deadlines for relief | Post-conviction review should not be restricted by arti | equal-justice-and-policing.html |
| `JUST-REVS-0006` | Access to post-conviction resources | People seeking post-conviction relief must have meaning | equal-justice-and-policing.html |
| `JUST-REVS-0007` | Presumptive systemic review | Justice systems should create presumptive review pathwa | equal-justice-and-policing.html |
| `JUST-RSTS-0001` | Restorative justice pathways | Justice systems should include restorative justice path | equal-justice-and-policing.html |
| `JUST-RSTS-0002` | Expand diversion programs | Diversion programs should be expanded to reduce unneces | equal-justice-and-policing.html |
| `JUST-RSTS-0003` | Preserve due process in diversion | Restorative and diversion programs must not be coercive | equal-justice-and-policing.html |
| `JUST-RSTS-0004` | Equitable diversion access | Access to restorative justice and diversion should not  | equal-justice-and-policing.html |
| `JUST-SUPR-0001` | Support reintegration not reincarceration | Probation and parole systems must be designed to suppor | equal-justice-and-policing.html |
| `JUST-SUPR-0002` | Narrow tailored supervision conditions | Conditions of probation and parole must be narrowly tai | equal-justice-and-policing.html |
| `JUST-SUPR-0003` | Limit technical violation incarceration | Technical violations that do not involve new serious cr | equal-justice-and-policing.html |
| `JUST-SUPR-0004` | Due process for revocation | Revocation of probation or parole must require meaningf | equal-justice-and-policing.html |
| `JUST-SUPR-0005` | Prevent impossible conditions | Probation and parole systems must not impose impossible | equal-justice-and-policing.html |
| `JUST-SUPR-0006` | Periodic supervision review | Supervision terms should be periodically reviewed and s | equal-justice-and-policing.html |
| `JUST-VICS-0001` | Victim protection and participation | Victims of crime must have access to protection informa | equal-justice-and-policing.html |
| `JUST-VICS-0002` | Trauma-informed victim services | Victim-support systems should include trauma-informed s | equal-justice-and-policing.html |
| `JUST-VICS-0003` | Preserve evidentiary standards | Victims’ rights frameworks may not be used to erode evi | equal-justice-and-policing.html |
| `JUST-VICS-0004` | Justice not retribution alone | Victim participation must be structured to support just | equal-justice-and-policing.html |
| `JUST-VICS-0005` | Equitable victim support access | Access to victim-support services must be equitable and | equal-justice-and-policing.html |
| `JUST-WITS-0001` | Protect witnesses from retaliation | Witnesses must be protected from intimidation retaliati | equal-justice-and-policing.html |
| `JUST-WITS-0002` | Proportionate witness protection | Witness-protection measures must be proportionate revie | equal-justice-and-policing.html |
| `JUST-WITS-0003` | Disclose witness inducements | Courts and prosecutors must disclose material inducemen | equal-justice-and-policing.html |
| `JUST-WITS-0004` | Penalize witness intimidation | Witness intimidation by officials law enforcement litig | equal-justice-and-policing.html |
| `LABR-CLMS-0001` | All workers have the right to safe temperatures and hea | All workers have an enforceable right to protection fro | labor-and-workers-rights.html |
| `LABR-DOMS-0001` | Domestic workers must be covered by full labor law prot | Domestic workers&#x2014;including nannies, housekeepers | labor-and-workers-rights.html |
| `LABR-PAYS-0002` | Wage systems must be transparent, predictable, and free | The federal minimum wage must be set at a level suffici | labor-and-workers-rights.html |
| `LABR-PBNS-0001` | Benefits must travel with workers across employment rel | Social insurance systems and workplace benefits&#x2014; | labor-and-workers-rights.html |
| `LABR-PRLS-0001` | Prison labor may not be compelled without fair compensa | Incarcerated workers performing labor may not be compel | labor-and-workers-rights.html |
| `LABR-SCHS-0001` | Workers in covered industries must receive advance noti | Workers in retail, food service, hospitality, and other | labor-and-workers-rights.html |
| `LABR-SFTS-0001` | Employers must provide safe working conditions and may | All workers have the right to a safe workplace and empl | labor-and-workers-rights.html |
| `LEGL-DMJS-0001` | Structural minority rule over national policy is prohib | Legislative systems must prevent structural minority ru | legislative-reform.html |
| `LEGL-DRFS-0001` | Binding drafting standards required for all new federal | A constitutional amendment or equivalent binding rule s | legislative-reform.html |
| `LEGL-DRFS-0002` | Each new law requires plain-language statement of purpo | Every new law must include a plain-language statement o | legislative-reform.html |
| `LEGL-PROS-0001` | Filibuster and indefinite minority obstruction must end | Legislative procedure may not allow indefinite minority | legislative-reform.html |
| `LEGL-RPLS-0001` | Repeal Alien Enemies Act and related emergency abuse fr | Repeal the Alien Enemies Act framework and related emer | legislative-reform.html |
| `LEGL-SENS-0003` | Senate may serve as review body rather than co-equal ve | The Senate may serve as a review, delay, and revision b | legislative-reform.html |
| `MDIA-NETS-0001` | Restore and permanently codify net neutrality in federa | Internet service providers must treat all legal interne | information-and-media.html |
| `MDIA-OWNS-0001` | Establish and enforce media ownership limits to prevent | No single entity may own more than one daily newspaper, | information-and-media.html |
| `MDIA-PLTS-0001` | Require transparency in platform content moderation pol | Digital platforms with significant user reach must publ | information-and-media.html |
| `MDIA-PUBL-0001` | Guarantee and expand public media funding insulated fro | Federal funding for public media — including the Corpor | information-and-media.html |
| `TAXN-AUTS-0001` | Automation Tax on Labor Displacement | Companies that replace or materially displace human lab | taxation-and-wealth.html |
| `TAXN-AUTS-0002` | Automation Tax Revenue for Public Benefit | Revenue from AI or automated-labor taxation should be u | taxation-and-wealth.html |
| `TAXN-AUTS-0003` | Structure Tax to Discourage Irresponsible Displacement | AI or automated-labor taxation should be structured to  | taxation-and-wealth.html |
| `TAXN-CDRS-0001` | Candidates for federal office must publicly disclose ta | Candidates for President, Vice President, and federal e | taxation-and-wealth.html |
| `TAXN-CORS-0001` | Corporations must pay meaningful taxes on real economic | Corporate tax rates must be sufficient to prevent profi | taxation-and-wealth.html |
| `TAXN-ENFL-0001` | Tax enforcement agencies must be well funded, technical | The IRS must be funded and staffed to enforce tax law e | taxation-and-wealth.html |
| `TAXN-EQTS-0001` | Equal Pay and Economic Opportunity | Guarantee equal pay and equal economic opportunity rega | taxation-and-wealth.html |
| `TAXN-FTTS-0001` | Securities and derivatives transactions may be subject  | Financial transactions in stocks, bonds, and derivative | taxation-and-wealth.html |
| `TAXN-INDS-0001` | National Industrial Strategy | Establish national manufacturing and industrial policy  | taxation-and-wealth.html |
| `TAXN-INSS-0001` | AI Cannot Deny Insurance Without Human Review | AI systems may not be used to deny restrict or reduce i | taxation-and-wealth.html |
| `TAXN-INSS-0002` | Independent Human Judgment Required | Human reviewers in insurance decisions must exercise in | taxation-and-wealth.html |
| `TAXN-INTL-0001` | United States should pursue international agreements an | The United States should pursue international agreement | taxation-and-wealth.html |
| `TAXN-LVTS-0001` | Land value taxation may capture publicly created land v | Tax policy may employ land value taxation to capture th | taxation-and-wealth.html |
| `TAXN-SMBS-0001` | Small Business Healthcare Coverage Support | Provide subsidies carveouts or public support to help s | taxation-and-wealth.html |
| `TECH-AGES-0002` | No centralized databases | Age verification systems must not create centralized da | technology-and-ai.html |
| `TECH-AGES-0003` | Allow privacy-preserving alternatives | Allow age assurance mechanisms that preserve privacy su | technology-and-ai.html |
| `TECH-AGES-0004` | Data minimization and deletion | Any permitted age verification system must minimize dat | technology-and-ai.html |
| `TECH-AGES-0005` | Narrow scope requirements | Age verification requirements must be narrowly scoped t | technology-and-ai.html |
| `TECH-AGES-0006` | Ban surveillance proxy use | Governments and private entities may not use age verifi | technology-and-ai.html |
| `TECH-AINL-0001` | High-risk AI requires review | High-risk AI systems must be subject to heightened gove | technology-and-ai.html |
| `TECH-AINL-0002` | No automation without accountability | AI systems that affect rights liberty healthcare educat | technology-and-ai.html |
| `TECH-AINL-0003` | Rights to notice and review | No fully automated decisions in critical domains withou | technology-and-ai.html |
| `TECH-AINL-0004` | Transparency and auditability | AI systems used in public-sector decision-making must b | technology-and-ai.html |
| `TECH-AINL-0006` | Testing for bias and safety | AI systems must be tested for bias safety reliability a | technology-and-ai.html |
| `TECH-AINL-0007` | Documentation disclosure | Covered AI systems must maintain model cards documentat | technology-and-ai.html |
| `TECH-AINL-0008` | No secret law | Secret law or undisclosed AI decision systems must not  | technology-and-ai.html |
| `TECH-ALGO-0001` | Disclosure of algorithmic influence | People must be told when AI or algorithmic systems mate | technology-and-ai.html |
| `TECH-ALGO-0002` | Right to contest decisions | People must have the right to contest materially harmfu | technology-and-ai.html |
| `TECH-ALGO-0003` | Non-algorithmic alternatives | Users must have access to non-algorithmic or less perso | technology-and-ai.html |
| `TECH-ALGO-0004` | Ban manipulative optimization | Ban manipulative algorithmic optimization that targets  | technology-and-ai.html |
| `TECH-ALGO-0005` | Disclose ranking objectives | Platforms must disclose core ranking and recommendation | technology-and-ai.html |
| `TECH-ALGO-0006` | Protected researcher access | Independent researchers must have protected access to p | technology-and-ai.html |
| `TECH-AUDT-0001` | Independent auditing requirement | Covered AI systems must support independent auditing fo | technology-and-ai.html |
| `TECH-AUDT-0002` | Meaningful redress for harms | Affected individuals must have access to meaningful exp | technology-and-ai.html |
| `TECH-AUDT-0003` | Forensic logging | Organizations deploying high-risk AI must keep logs suf | technology-and-ai.html |
| `TECH-AUDT-0004` | Public AI registry | Government use of AI must be cataloged in a public regi | technology-and-ai.html |
| `TECH-AUDT-0005` | Oversight of classified systems | Classified or sensitive AI systems must still be subjec | technology-and-ai.html |
| `TECH-AUTS-0001` | Strict safeguards for high-risk systems | High-risk autonomous systems must not be deployed where | technology-and-ai.html |
| `TECH-AUTS-0002` | No replacement of accountable humans | AI systems used in healthcare education benefits housin | technology-and-ai.html |
| `TECH-AUTS-0003` | Prohibit automated denial systems | Automated denial systems for benefits care housing or l | technology-and-ai.html |
| `TECH-AUTS-0004` | Human override authority | Government agencies must maintain human override author | technology-and-ai.html |
| `TECH-BIOS-0002` | Ban real-time crowd tracking | Ban real-time biometric tracking of crowds or demonstra | technology-and-ai.html |
| `TECH-BIOS-0003` | No general identity infrastructure | Biometric systems may not be used as general identity i | technology-and-ai.html |
| `TECH-BIOS-0004` | Strict safeguards where permitted | Where biometrics are permitted they must require strict | technology-and-ai.html |
| `TECH-BIOS-0005` | Heightened data protection | Biometric data must be treated as highly sensitive prot | technology-and-ai.html |
| `TECH-DATA-0001` | Prohibit unauthorized cross-agency surveillance fusion | Ban or strictly limit cross-agency fusion of surveillan | technology-and-ai.html |
| `TECH-DATA-0002` | Ban secret dossiers | Ban creation of secret AI-generated behavioral dossiers | technology-and-ai.html |
| `TECH-DATA-0003` | Ban government use of commercial data | Ban use of commercially acquired bulk location biometri | technology-and-ai.html |
| `TECH-EDUS-0001` | AI must enhance not replace learning | AI systems in education must enhance learning without r | technology-and-ai.html |
| `TECH-EDUS-0002` | No replacement of human educators | AI systems may not replace human educators in primary s | technology-and-ai.html |
| `TECH-EDUS-0003` | Support not substitute | AI systems may be used to support educators and student | technology-and-ai.html |
| `TECH-EDUS-0004` | No sole-basis grading | AI systems may not be the sole basis for grading or eva | technology-and-ai.html |
| `TECH-EDUS-0005` | Right to human review | Students have the right to human review of AI-influence | technology-and-ai.html |
| `TECH-EDUS-0006` | Clear policies on AI use | Educational institutions must establish clear policies  | technology-and-ai.html |
| `TECH-EDUS-0007` | Evaluate for bias | AI systems used in education must be evaluated for bias | technology-and-ai.html |
| `TECH-EDUS-0008` | Accessibility and equity | AI tools used in education must be accessible to all st | technology-and-ai.html |
| `TECH-EDUS-0009` | Data minimization | Student data collected by AI systems must be limited to | technology-and-ai.html |
| `TECH-EDUS-0010` | No commercial use of student data | Student data may not be sold shared or used for adverti | technology-and-ai.html |
| `TECH-EDUS-0011` | Enhanced protections for minors | Enhanced privacy protections are required for minors us | technology-and-ai.html |
| `TECH-EDUS-0012` | Ban invasive surveillance | Ban use of AI systems for invasive surveillance of stud | technology-and-ai.html |
| `TECH-EDUS-0013` | No emotion inference | AI systems may not be used to infer student emotions at | technology-and-ai.html |
| `TECH-EDUS-0014` | No behavioral scoring | Educational institutions may not use AI systems to assi | technology-and-ai.html |
| `TECH-EDUS-0015` | Disclose AI-generated content | AI-generated educational content must be clearly identi | technology-and-ai.html |
| `TECH-EDUS-0016` | No ideological manipulation | AI systems may not be used to impose ideological viewpo | technology-and-ai.html |
| `TECH-EDUS-0017` | Support critical thinking | Educational use of AI must support development of criti | technology-and-ai.html |
| `TECH-EDUS-0018` | Accessibility for disabilities | AI may be used to improve accessibility for students wi | technology-and-ai.html |
| `TECH-EDUS-0019` | Multilingual support | AI systems should support multilingual education and re | technology-and-ai.html |
| `TECH-EDUS-0020` | Disclosure requirement | Educational institutions must disclose use of AI system | technology-and-ai.html |
| `TECH-EDUS-0021` | Regular independent audits | AI systems used in education must be subject to regular | technology-and-ai.html |
| `TECH-EDUS-0022` | No proprietary opacity | Vendors providing AI systems to educational institution | technology-and-ai.html |
| `TECH-EDUS-0023` | Demonstrate educational benefit | AI systems must demonstrate educational benefit through | technology-and-ai.html |
| `TECH-EDUS-0024` | Informed consent for testing | Students may not be used as unwitting test subjects for | technology-and-ai.html |
| `TECH-ENVS-0001` | Sustainable operations required | AI systems and infrastructure must not externalize envi | technology-and-ai.html |
| `TECH-ENVS-0002` | Carbon neutrality requirement | Large-scale AI systems and data centers must meet stric | technology-and-ai.html |
| `TECH-ENVS-0003` | Energy disclosure | Operators of large AI systems must publicly disclose en | technology-and-ai.html |
| `TECH-ENVS-0004` | Renewable energy supply | High-consumption AI infrastructure must supply or offse | technology-and-ai.html |
| `TECH-ENVS-0005` | Water usage disclosure | AI infrastructure operators must disclose water usage i | technology-and-ai.html |
| `TECH-ENVS-0006` | Water resource protection | AI systems must not disproportionately strain local wat | technology-and-ai.html |
| `TECH-ENVS-0007` | Materials sourcing standards | Materials used in AI hardware including rare earth elem | technology-and-ai.html |
| `TECH-ENVS-0008` | Lifecycle responsibility | AI hardware producers must be responsible for full life | technology-and-ai.html |
| `TECH-ENVS-0009` | Durability and repairability | AI-related hardware must meet durability repairability  | technology-and-ai.html |
| `TECH-ENVS-0010` | Recycling programs | Operators must implement responsible recycling and disp | technology-and-ai.html |
| `TECH-ENVS-0011` | Internalize environmental costs | Companies developing or deploying AI systems must inter | technology-and-ai.html |
| `TECH-ENVS-0012` | Environmental impact assessments | Large-scale AI deployments must undergo environmental i | technology-and-ai.html |
| `TECH-ENVS-0013` | Support climate efforts | AI should be used to support climate modeling environme | technology-and-ai.html |
| `TECH-ENVS-0014` | Resource optimization | AI may be used to optimize energy water and resource us | technology-and-ai.html |
| `TECH-ENVS-0015` | Grid modernization support | AI systems may support modernization of electrical grid | technology-and-ai.html |
| `TECH-ENVS-0016` | No misrepresentation | AI companies may not misrepresent environmental impact  | technology-and-ai.html |
| `TECH-ENVS-0017` | Standardized reporting | Environmental reporting for AI systems must follow stan | technology-and-ai.html |
| `TECH-ENVS-0018` | Environmental justice protection | AI infrastructure may not disproportionately locate env | technology-and-ai.html |
| `TECH-ENVS-0019` | No global offloading | Environmental costs of AI supply chains must not be off | technology-and-ai.html |
| `TECH-ENVS-0020` | Integration with national policy | AI infrastructure policy must integrate with national e | technology-and-ai.html |
| `TECH-ENVS-0021` | Noise pollution standards | Establish standards for noise pollution from AI data ce | technology-and-ai.html |
| `TECH-FINC-0001` | Fairness and transparency in finance | AI systems in finance credit and insurance must not und | technology-and-ai.html |
| `TECH-FINC-0002` | No automated denial of credit | AI systems may not independently deny credit loans mort | technology-and-ai.html |
| `TECH-FINC-0003` | Human review before denial | Any decision that would deny restrict or materially wor | technology-and-ai.html |
| `TECH-FINC-0004` | No opaque criteria | AI systems used in underwriting or creditworthiness ass | technology-and-ai.html |
| `TECH-FINC-0005` | Anti-discrimination requirement | AI systems in finance and insurance must not discrimina | technology-and-ai.html |
| `TECH-FINC-0006` | Regular audits for bias | AI systems used in lending underwriting pricing or clai | technology-and-ai.html |
| `TECH-FINC-0007` | No automated insurance denial | AI systems may not independently deny restrict reduce o | technology-and-ai.html |
| `TECH-FINC-0008` | Independent human judgment required | Human reviewers in insurance decisions may not rely sol | technology-and-ai.html |
| `TECH-FINC-0009` | AI for approval not denial | AI systems may be used to assist or expedite approval o | technology-and-ai.html |
| `TECH-FINC-0010` | No negative inference from AI | Absence of AI approval or recommendation may not be use | technology-and-ai.html |
| `TECH-FINC-0011` | No behavioral surveillance scoring | AI systems may not use generalized behavioral surveilla | technology-and-ai.html |
| `TECH-FINC-0012` | Transparent risk scoring | Risk scoring in finance and insurance must be based on  | technology-and-ai.html |
| `TECH-FINC-0013` | No vulnerability profiling | AI systems may not use individualized vulnerability pro | technology-and-ai.html |
| `TECH-FINC-0014` | Fair housing access | AI systems used in mortgage housing finance or rental s | technology-and-ai.html |
| `TECH-FINC-0015` | Tenant screening limits | Tenant screening and housing-related AI systems may not | technology-and-ai.html |
| `TECH-FINC-0016` | Right to explanation | People have the right to a meaningful explanation of AI | technology-and-ai.html |
| `TECH-FINC-0017` | Right to appeal | People must have access to a timely human appeal proces | technology-and-ai.html |
| `TECH-FINC-0018` | Disclosure requirement | Entities using AI in consequential financial or insuran | technology-and-ai.html |
| `TECH-FINC-0019` | Data minimization | AI systems in finance and insurance may collect only da | technology-and-ai.html |
| `TECH-FINC-0020` | No data sales or repurposing | Financial and insurance data used by AI systems may not | technology-and-ai.html |
| `TECH-FINC-0021` | No secret profile enrichment | Entities may not secretly enrich financial or insurance | technology-and-ai.html |
| `TECH-FINC-0022` | No cross-system denial loops | AI systems may not be used to create cross-system denia | technology-and-ai.html |
| `TECH-FINC-0024` | No proprietary opacity | Trade secrecy or proprietary claims may not be used to  | technology-and-ai.html |
| `TECH-FINC-0025` | Documentation requirement | Entities deploying consequential AI systems in finance  | technology-and-ai.html |
| `TECH-FINC-0026` | No exploitation of vulnerability | AI systems may not be used to identify and exploit fina | technology-and-ai.html |
| `TECH-FINC-0027` | No impersonation | AI systems in finance and insurance may not impersonate | technology-and-ai.html |
| `TECH-FINC-0028` | Public-interest standards for essential systems | Where finance credit or insurance systems function as e | technology-and-ai.html |
| `TECH-FINC-0029` | No automatic exclusion from essential systems | AI systems must not be allowed to automatically exclude | technology-and-ai.html |
| `TECH-GOVN-0001` | Preserve due process and rights | AI systems used by government or public-service entitie | technology-and-ai.html |
| `TECH-GOVN-0002` | No automated denial of benefits | AI systems may not independently deny terminate reduce  | technology-and-ai.html |
| `TECH-GOVN-0003` | Human decision-maker before harm | Any decision that would deny reduce terminate or delay  | technology-and-ai.html |
| `TECH-GOVN-0004` | Independent human judgment required | Human reviewers may not rely solely on AI-generated rec | technology-and-ai.html |
| `TECH-GOVN-0005` | AI for approval not denial | AI systems may be used to help identify likely eligibil | technology-and-ai.html |
| `TECH-GOVN-0006` | Right to explanation | Individuals have the right to a meaningful explanation  | technology-and-ai.html |
| `TECH-GOVN-0007` | Right to appeal | Individuals must have a timely accessible appeal proces | technology-and-ai.html |
| `TECH-GOVN-0008` | Disclosure requirement | Government agencies must clearly disclose when AI syste | technology-and-ai.html |
| `TECH-GOVN-0009` | No behavioral scoring | Government may not use AI systems to assign generalized | technology-and-ai.html |
| `TECH-GOVN-0010` | No discriminatory profiling | Government AI systems may not use protected characteris | technology-and-ai.html |
| `TECH-GOVN-0011` | No social conformity scoring | Government may not use AI systems to monitor or score b | technology-and-ai.html |
| `TECH-GOVN-0012` | Access to human representatives | People must retain access to human government represent | technology-and-ai.html |
| `TECH-GOVN-0013` | No forced AI-only channels | Government may not force individuals into AI-only servi | technology-and-ai.html |
| `TECH-GOVN-0014` | Accessibility for vulnerable populations | AI-enabled public services must be accessible to disabl | technology-and-ai.html |
| `TECH-GOVN-0015` | No automated disability denials | AI systems may not be used to deny disability benefits  | technology-and-ai.html |
| `TECH-GOVN-0016` | No mass fraud sweeps | Government may not use AI systems to conduct mass fraud | technology-and-ai.html |
| `TECH-GOVN-0017` | No automated termination of essential benefits | AI systems may not automatically terminate housing food | technology-and-ai.html |
| `TECH-GOVN-0018` | No automated immigration decisions | AI systems may not independently determine immigration  | technology-and-ai.html |
| `TECH-GOVN-0019` | No credibility inference in immigration | Government may not use AI systems to infer truthfulness | technology-and-ai.html |
| `TECH-GOVN-0020` | Human review for immigration decisions | Any AI-influenced immigration or detention decision mus | technology-and-ai.html |
| `TECH-GOVN-0021` | Vendor accountability | Private vendors and contractors supplying AI systems to | technology-and-ai.html |
| `TECH-GOVN-0022` | No proprietary opacity | Trade secrecy or proprietary claims may not be used to  | technology-and-ai.html |
| `TECH-GOVN-0023` | Procurement disclosure | Government procurement of AI systems must include publi | technology-and-ai.html |
| `TECH-GOVN-0024` | Regular independent audits | Government AI systems must undergo regular independent  | technology-and-ai.html |
| `TECH-GOVN-0025` | Public AI registry | All materially consequential government AI systems must | technology-and-ai.html |
| `TECH-GOVN-0026` | Sunset and reauthorization | Government AI systems affecting rights benefits or lega | technology-and-ai.html |
| `TECH-GOVN-0027` | Explicit legal authority required | Government agencies may not deploy consequential AI sys | technology-and-ai.html |
| `TECH-GOVN-0028` | No unwitting test subjects | Government may not use the public as unwitting test sub | technology-and-ai.html |
| `TECH-GOVN-0029` | Right to challenge system legality | Individuals must be able to challenge not only a govern | technology-and-ai.html |
| `TECH-HARS-0001` | Platforms must implement effective systems to prevent a | Digital platforms with significant user bases must impl | technology-and-ai.html |
| `TECH-IMMS-0001` | Ban opaque immigration AI | Ban use of opaque or unreviewable AI systems in immigra | technology-and-ai.html |
| `TECH-IMMS-0002` | Ban risk scoring for detention | Ban AI risk scoring systems used to justify immigration | technology-and-ai.html |
| `TECH-INTL-0004` | Common carrier treatment | Internet service providers and core digital network inf | technology-and-ai.html |
| `TECH-INTL-0005` | Non-discrimination requirement | Common carrier obligations must prohibit discrimination | technology-and-ai.html |
| `TECH-INTL-0006` | No blocking or throttling | Network operators may not prioritize degrade or block t | technology-and-ai.html |
| `TECH-INTL-0007` | Narrow technical exceptions | Net neutrality frameworks must allow narrowly scoped ex | technology-and-ai.html |
| `TECH-INTL-0008` | Transparent exceptions | All exceptions to neutrality must be transparent audita | technology-and-ai.html |
| `TECH-INTL-0009` | Protection from rollback | Core neutrality and access protections must be insulate | technology-and-ai.html |
| `TECH-JUDS-0001` | No AI sentencing | AI systems may not be used to determine sentencing bail | technology-and-ai.html |
| `TECH-JUDS-0002` | No risk scoring | AI systems may not assign risk scores for recidivism da | technology-and-ai.html |
| `TECH-JUDS-0003` | No jury profiling | AI systems may not be used to profile influence or sele | technology-and-ai.html |
| `TECH-JUDS-0004` | Strict admissibility standards | AI-generated or AI-analyzed evidence must meet strict s | technology-and-ai.html |
| `TECH-JUDS-0005` | Right to examine AI evidence | Defendants and parties must have the right to examine c | technology-and-ai.html |
| `TECH-JUDS-0006` | AI for wrongful conviction review | AI may be used to assist in identifying wrongful convic | technology-and-ai.html |
| `TECH-JUDS-0007` | Identify systemic bias | AI should be used to identify systemic bias in sentenci | technology-and-ai.html |
| `TECH-JUDS-0008` | No AI final determinations | Judges and court staff may not rely on AI systems to ma | technology-and-ai.html |
| `TECH-JUDS-0009` | Clerical use only with disclosure | AI may be used to assist with clerical summarization re | technology-and-ai.html |
| `TECH-JUDS-0010` | Disclose material AI use | Courts must disclose material use of AI in opinion draf | technology-and-ai.html |
| `TECH-JUDS-0011` | No unfair docket prioritization | AI systems may not be used to prioritize dockets motion | technology-and-ai.html |
| `TECH-JUDS-0012` | Preserve accountable reasoning | Any AI-assisted judicial workflow must preserve a human | technology-and-ai.html |
| `TECH-JUDS-0013` | Evidence authentication | AI-generated or AI-enhanced evidence must be authentica | technology-and-ai.html |
| `TECH-JUDS-0014` | Technical disclosure for challenge | Parties must receive sufficient technical disclosure to | technology-and-ai.html |
| `TECH-JUDS-0015` | Scientific validation required | Courts may not admit AI outputs as expert-like evidence | technology-and-ai.html |
| `TECH-JUDS-0016` | Synthetic media high-risk | Synthetic media evidence must be presumptively treated  | technology-and-ai.html |
| `TECH-JUDS-0017` | Preserve analysis logs | If AI is used to analyze evidence all material logs mod | technology-and-ai.html |
| `TECH-JUDS-0018` | Defense access to AI disclosures | If prosecutors or the state use AI systems in investiga | technology-and-ai.html |
| `TECH-JUDS-0019` | Defense funding for AI parity | Public defenders and defense counsel must be provided f | technology-and-ai.html |
| `TECH-JUDS-0020` | No AI-driven plea pressure | AI systems may not be used to pressure plea deals throu | technology-and-ai.html |
| `TECH-JUDS-0021` | Guard against prosecutorial AI advantage | Courts must guard against prosecutorial advantage creat | technology-and-ai.html |
| `TECH-JUDS-0022` | No juror profiling | AI systems may not be used to profile rank influence or | technology-and-ai.html |
| `TECH-JUDS-0023` | AI reconstructions must be disclosed | AI-generated reconstructions simulations or visualizati | technology-and-ai.html |
| `TECH-JUDS-0024` | No AI summaries to juries | Courts may not provide juries with AI-generated summari | technology-and-ai.html |
| `TECH-JUDS-0025` | No distortion of evidentiary record | Jury-facing use of AI must not distort the evidentiary  | technology-and-ai.html |
| `TECH-JUDS-0026` | Default to prohibition | AI use in courts and legal proceedings must default to  | technology-and-ai.html |
| `TECH-JUDS-0027` | Ban AI-generated evidence | AI-generated or AI-fabricated evidence including images | technology-and-ai.html |
| `TECH-JUDS-0028` | Ban AI-enhanced evidence | AI-enhanced evidence that alters interpretation content | technology-and-ai.html |
| `TECH-JUDS-0029` | Analytical use only | AI may be used only for analytical purposes on existing | technology-and-ai.html |
| `TECH-JUDS-0030` | No generative AI for evidence | Generative AI systems including large language models m | technology-and-ai.html |
| `TECH-JUDS-0031` | Verifiable methods only | Permitted analytical systems must use verifiable reprod | technology-and-ai.html |
| `TECH-JUDS-0032` | Disclose analytical AI use | Any use of AI in evidence analysis must be explicitly d | technology-and-ai.html |
| `TECH-JUDS-0033` | No black-box systems | Black-box AI systems that cannot be meaningfully explai | technology-and-ai.html |
| `TECH-JUDS-0034` | AI not expert witnesses | AI systems may not be presented as expert witnesses or  | technology-and-ai.html |
| `TECH-JUDS-0035` | Human experts accountable | All expert testimony must be provided by qualified huma | technology-and-ai.html |
| `TECH-JUDS-0036` | Disclose AI-assisted expert analysis | Human experts using AI-assisted analysis must disclose  | technology-and-ai.html |
| `TECH-JUDS-0037` | No AI-drafted opinions | Judges and justices may not use generative AI systems t | technology-and-ai.html |
| `TECH-JUDS-0038` | No AI legal reasoning | AI systems may not substitute for judicial reasoning le | technology-and-ai.html |
| `TECH-JUDS-0039` | Limited clerical use | AI may be used for limited clerical tasks such as docum | technology-and-ai.html |
| `TECH-JUDS-0040` | No AI reconstructions to juries | AI-generated reconstructions simulations or demonstrati | technology-and-ai.html |
| `TECH-JUDS-0041` | No AI summaries of evidence to juries | AI systems may not be used to summarize interpret or pr | technology-and-ai.html |
| `TECH-JUDS-0042` | No AI influence on jurors | AI systems may not be used to influence juror perceptio | technology-and-ai.html |
| `TECH-JUDS-0043` | Recognize AI risks | Courts must recognize that AI systems can amplify confi | technology-and-ai.html |
| `TECH-JUDS-0044` | Elevated scrutiny standards | Any permitted AI-assisted analysis must meet elevated s | technology-and-ai.html |
| `TECH-JUDS-0045` | Right to challenge AI analysis | All parties must have full rights to challenge any AI-a | technology-and-ai.html |
| `TECH-JUDS-0046` | Reproducibility requirement | AI-assisted analysis must be reproducible by opposing p | technology-and-ai.html |
| `TECH-JUDS-0047` | Preserve analysis logs | All AI-assisted evidentiary analysis must include prese | technology-and-ai.html |
| `TECH-JUDS-0048` | Audit access requirement | Courts and opposing parties must have access to all mat | technology-and-ai.html |
| `TECH-JUDS-0049` | No AI family court determinations | AI systems may not be used to determine custody visitat | technology-and-ai.html |
| `TECH-JUDS-0050` | No parental fitness inference | AI systems may not infer parental fitness abuse risk cr | technology-and-ai.html |
| `TECH-JUDS-0051` | No AI in family court recommendations | Family courts may not rely on AI-generated summaries re | technology-and-ai.html |
| `TECH-JUDS-0052` | Disclose family court AI use | Any AI-assisted tool used in family court administratio | technology-and-ai.html |
| `TECH-JUDS-0053` | No automated evictions | AI systems may not be used to automate or materially dr | technology-and-ai.html |
| `TECH-JUDS-0054` | No tenant risk scoring | Courts may not rely on AI-generated tenant risk scores  | technology-and-ai.html |
| `TECH-JUDS-0055` | Disclose housing AI use | Landlords and housing litigants using AI-assisted evide | technology-and-ai.html |
| `TECH-JUDS-0056` | No eviction acceleration through AI | Housing courts must not use AI systems to accelerate ca | technology-and-ai.html |
| `TECH-JUDS-0057` | No AI in administrative adjudication | AI systems may not independently determine outcomes in  | technology-and-ai.html |
| `TECH-JUDS-0058` | No opaque scoring in administrative hearings | Administrative adjudication may not rely on opaque AI s | technology-and-ai.html |
| `TECH-JUDS-0059` | Disclose AI in administrative proceedings | Parties in administrative proceedings have the right to | technology-and-ai.html |
| `TECH-JUDS-0060` | Administrative appeal rights | Administrative agencies must provide meaningful human r | technology-and-ai.html |
| `TECH-JUDS-0061` | No AI probation/parole decisions | AI systems may not be used to determine probation parol | technology-and-ai.html |
| `TECH-JUDS-0062` | No proxy-based supervision scoring | AI systems may not assign supervision risk scores based | technology-and-ai.html |
| `TECH-JUDS-0063` | Individualized human review required | Probation and parole decisions must be based on individ | technology-and-ai.html |
| `TECH-JUDS-0064` | AI to identify bias in probation | AI may be used to identify patterns of bias inconsisten | technology-and-ai.html |
| `TECH-JUDS-0065` | No AI fines and fees escalation | AI systems may not be used to escalate fines fees colle | technology-and-ai.html |
| `TECH-JUDS-0066` | No payment coercion through AI | Courts and governments may not use AI to pressure payme | technology-and-ai.html |
| `TECH-JUDS-0067` | No AI debt-to-punishment escalation | AI systems may not be used to convert administrative de | technology-and-ai.html |
| `TECH-JUDS-0068` | AI to identify predatory fine patterns | AI may be used to identify unlawful disparities or pred | technology-and-ai.html |
| `TECH-JUDS-0069` | AI for legal aid access | AI may be used to assist legal aid intake document navi | technology-and-ai.html |
| `TECH-JUDS-0070` | Disclose legal-aid AI limits | AI tools used in legal-aid contexts must clearly disclo | technology-and-ai.html |
| `TECH-JUDS-0071` | Public legal-aid tools must be fair | Public legal-aid AI tools must be designed for accessib | technology-and-ai.html |
| `TECH-JUDS-0072` | Fund public legal access tools | Governments and courts should fund public-interest lega | technology-and-ai.html |
| `TECH-JUDS-0073` | AI records systems must be auditable | AI systems used to classify search summarize or priorit | technology-and-ai.html |
| `TECH-JUDS-0074` | No unequal filing access | Court administrative AI systems may not create unequal  | technology-and-ai.html |
| `TECH-JUDS-0075` | Preserve record accuracy | Public court records systems using AI must preserve acc | technology-and-ai.html |
| `TECH-JUDS-0076` | Human override for court admin AI | Courts must maintain human override and review mechanis | technology-and-ai.html |
| `TECH-JUDS-0077` | AI limited to assistive functions | Where AI is permitted in judicial contexts it must be l | technology-and-ai.html |
| `TECH-JUDS-0078` | No credibility assessment | AI systems may not be used to assess credibility truthf | technology-and-ai.html |
| `TECH-JUDS-0079` | No behavioral inference in court | Behavioral biometric or speech-analysis AI tools may no | technology-and-ai.html |
| `TECH-JUDS-0080` | No AI alteration of police footage | AI systems may not be used to reinterpret enhance or se | technology-and-ai.html |
| `TECH-JUDS-0081` | Preserve full context in evidence | AI-assisted analysis of law-enforcement evidence must p | technology-and-ai.html |
| `TECH-JUDS-0082` | No sole-basis AI translation | AI translation or interpretation systems may not be use | technology-and-ai.html |
| `TECH-JUDS-0083` | Human interpreters required | Human-certified interpreters are required for critical  | technology-and-ai.html |
| `TECH-JUDS-0084` | Forensic AI validation required | AI systems used in forensic laboratories must meet stri | technology-and-ai.html |
| `TECH-JUDS-0085` | Test forensic AI systems | Forensic AI systems must be independently tested for ac | technology-and-ai.html |
| `TECH-JUDS-0086` | No AI reconstruction of sealed records | AI systems may not reconstruct infer or surface sealed  | technology-and-ai.html |
| `TECH-JUDS-0087` | Enforce record protections | Use of AI to bypass legal protections on records privac | technology-and-ai.html |
| `TECH-JUDS-0088` | No AI influence campaigns on juries | AI-generated content may not be used to influence juror | technology-and-ai.html |
| `TECH-JUDS-0089` | Mitigate public AI influence on trials | Courts must recognize and mitigate risks of AI-driven p | technology-and-ai.html |
| `TECH-JUDS-0090` | AI version control required | AI systems used in any permitted judicial context must  | technology-and-ai.html |
| `TECH-JUDS-0091` | Revalidate AI changes | Material changes to AI systems used in legal contexts m | technology-and-ai.html |
| `TECH-JUDS-0092` | No shift of burden or standards | Use of AI systems may not shift burden of proof evident | technology-and-ai.html |
| `TECH-JUDS-0093` | Transparent AI procurement | Courts and judicial systems must use transparent procur | technology-and-ai.html |
| `TECH-JUDS-0094` | Independent validation before deployment | AI systems may not be deployed in judicial contexts wit | technology-and-ai.html |
| `TECH-JUDS-0095` | Authority to suspend AI systems | Courts must maintain the authority to suspend or prohib | technology-and-ai.html |
| `TECH-JUDS-0096` | Party right to request suspension | Parties must have the right to request suspension of AI | technology-and-ai.html |
| `TECH-LABS-0001` | Protect worker rights and dignity | AI systems in employment must not undermine worker righ | technology-and-ai.html |
| `TECH-LABS-0002` | No automated employment decisions | AI systems may not make fully automated hiring firing p | technology-and-ai.html |
| `TECH-LABS-0003` | No opaque candidate filtering | AI systems may not be used to filter or rank job candid | technology-and-ai.html |
| `TECH-LABS-0004` | Evaluate for bias | AI systems used in employment must be evaluated and mit | technology-and-ai.html |
| `TECH-LABS-0005` | Right to explanation | Applicants and employees have the right to receive mean | technology-and-ai.html |
| `TECH-LABS-0006` | Ban intrusive monitoring | Ban use of AI systems for continuous intrusive monitori | technology-and-ai.html |
| `TECH-LABS-0007` | No emotion inference | Ban use of AI systems to infer or monitor worker emotio | technology-and-ai.html |
| `TECH-LABS-0008` | No outside-hours monitoring | Employers may not use AI systems to monitor or infer wo | technology-and-ai.html |
| `TECH-LABS-0009` | No sole-basis discipline or termination | AI systems may not be used as the sole basis for discip | technology-and-ai.html |
| `TECH-LABS-0010` | Transparent productivity scoring | AI-generated productivity or performance scores must be | technology-and-ai.html |
| `TECH-LABS-0011` | No coercive productivity targets | AI systems may not be used to coerce workers into unsaf | technology-and-ai.html |
| `TECH-LABS-0012` | Right to refuse harmful AI | Workers must have the right to refuse use of AI systems | technology-and-ai.html |
| `TECH-LABS-0013` | Access to human managers | Workers must have access to human managers or decision- | technology-and-ai.html |
| `TECH-LABS-0014` | Data minimization | AI systems may only collect worker data that is strictl | technology-and-ai.html |
| `TECH-LABS-0015` | No data sales or repurposing | Worker data collected through AI systems may not be sol | technology-and-ai.html |
| `TECH-LABS-0016` | Right to access and correct data | Workers have the right to access review and correct dat | technology-and-ai.html |
| `TECH-LABS-0017` | Disclosure requirement | Employers must disclose use of AI systems in hiring mon | technology-and-ai.html |
| `TECH-LABS-0018` | Regular independent audits | AI systems used in employment must be subject to regula | technology-and-ai.html |
| `TECH-LABS-0019` | Documentation requirement | Employers must maintain documentation of AI system desi | technology-and-ai.html |
| `TECH-LABS-0020` | Ban behavior prediction scoring | Ban AI systems that assign risk scores predicting emplo | technology-and-ai.html |
| `TECH-LABS-0021` | Ban anti-union AI | Ban use of AI systems to identify monitor or suppress u | technology-and-ai.html |
| `TECH-LABS-0022` | Validate personality assessments | Ban use of AI systems that infer personality traits or  | technology-and-ai.html |
| `TECH-LABS-0023` | Worker role in AI deployment | Workers or their representatives must have a role in re | technology-and-ai.html |
| `TECH-LABS-0024` | Collective bargaining over AI | Use of AI systems affecting working conditions must be  | technology-and-ai.html |
| `TECH-MHCS-0001` | AI assists not replaces clinicians | AI mental-health tools may assist but must not replace  | technology-and-ai.html |
| `TECH-MHCS-0002` | Prohibit manipulative AI systems | AI systems designed for emotional dependency manipulati | technology-and-ai.html |
| `TECH-MHCS-0003` | Evaluate for mental health harms | Platforms and AI systems must be evaluated for mental-h | technology-and-ai.html |
| `TECH-MHCS-0004` | Stronger protections for minors | Children and adolescents require stronger protections a | technology-and-ai.html |
| `TECH-MHCS-0005` | Disclosure in sensitive contexts | Users must be clearly informed when they are interactin | technology-and-ai.html |
| `TECH-MILS-0001` | Meaningful human control required | Use of AI in military and intelligence contexts must pr | technology-and-ai.html |
| `TECH-MILS-0002` | Ban autonomous lethal targeting | Ban AI systems that can independently select and engage | technology-and-ai.html |
| `TECH-MILS-0003` | Ban AI force initiation | Ban deployment of AI systems that can initiate or escal | technology-and-ai.html |
| `TECH-MILS-0004` | Ban nuclear AI | Ban use of AI systems in nuclear command control target | technology-and-ai.html |
| `TECH-MILS-0005` | Ban AI target generation | Ban AI systems from generating, recommending, or priori | technology-and-ai.html |
| `TECH-MILS-0006` | No target filtering or ranking | AI systems may not be used to narrow, filter, or rank p | technology-and-ai.html |
| `TECH-MILS-0007` | Identified human decision-maker | All use of lethal force involving AI systems must inclu | technology-and-ai.html |
| `TECH-MILS-0008` | Logging and auditability | All AI-assisted military decisions must be logged and a | technology-and-ai.html |
| `TECH-MILS-0009` | Transparency for human oversight | AI systems used in military decision-making must provid | technology-and-ai.html |
| `TECH-MILS-0010` | Testing and reliability | AI systems used in military contexts must meet strict r | technology-and-ai.html |
| `TECH-MILS-0011` | Ban mass intelligence fusion | Ban large-scale AI-driven intelligence surveillance sys | technology-and-ai.html |
| `TECH-MILS-0012` | No profiling for targeting | Ban use of AI to profile individuals or populations for | technology-and-ai.html |
| `TECH-MILS-0013` | Compliance with laws of armed conflict | All AI military systems must comply with principles of  | technology-and-ai.html |
| `TECH-MILS-0014` | Clear attribution of responsibility | Responsibility for actions taken using AI systems must  | technology-and-ai.html |
| `TECH-MILS-0015` | No evasion of accountability | Use of AI systems must not be used to obscure responsib | technology-and-ai.html |
| `TECH-MILS-0016` | Congressional authorization required | Deployment of new classes of AI-enabled military capabi | technology-and-ai.html |
| `TECH-MILS-0017` | Limits on executive authority | Executive authority may not unilaterally expand the use | technology-and-ai.html |
| `TECH-MILS-0019` | Controlled testing required | AI systems intended for military use must undergo contr | technology-and-ai.html |
| `TECH-MILS-0020` | No real-world testing | Ban use of real-world military operations as primary te | technology-and-ai.html |
| `TECH-MILS-0022` | Contractor accountability | Private contractors developing AI for military use are  | technology-and-ai.html |
| `TECH-MILS-0023` | No outsourcing of authority | Government may not outsource decision-making authority  | technology-and-ai.html |
| `TECH-MILS-0024` | Export controls | Establish controls on export of high-risk military AI s | technology-and-ai.html |
| `TECH-MILS-0025` | Defensive AI permitted | AI systems may be used in defensive or non-person-targe | technology-and-ai.html |
| `TECH-MILS-0026` | No repurposing defensive AI | Defensive AI systems must not be repurposed or extended | technology-and-ai.html |
| `TECH-MILS-0027` | AI for analysis not targeting | AI may be used for analysis classification and situatio | technology-and-ai.html |
| `TECH-MILS-0028` | Ban offensive lethal AI | Ban use of AI systems in the execution of offensive let | technology-and-ai.html |
| `TECH-MILS-0029` | Limited guidance use | AI systems may be used in limited weapon guidance roles | technology-and-ai.html |
| `TECH-MILS-0030` | Guidance parameters strictly defined | Guidance systems must not alter expand reinterpret or s | technology-and-ai.html |
| `TECH-MILS-0031` | No new target selection by guidance | Guidance systems must be incapable of selecting new tar | technology-and-ai.html |
| `TECH-MILS-0032` | Human responsibility for guidance outcomes | Human operators remain fully responsible for all outcom | technology-and-ai.html |
| `TECH-MILS-0033` | Defensive systems against non-human threats | AI may be used in defensive systems including missile i | technology-and-ai.html |
| `TECH-MILS-0034` | Support international treaties | Promote and pursue international treaties to limit and  | technology-and-ai.html |
| `TECH-MILS-0035` | Treaty goal: ban autonomous weapons | International agreements should seek to prohibit fully  | technology-and-ai.html |
| `TECH-MILS-0036` | Treaty goal: ban targeting AI | International treaties should establish bans on AI syst | technology-and-ai.html |
| `TECH-MILS-0037` | Treaty goal: ban nuclear AI | International treaties should restrict AI use in nuclea | technology-and-ai.html |
| `TECH-MILS-0038` | Treaty mechanisms | Treaties should include transparency reporting requirem | technology-and-ai.html |
| `TECH-MILS-0039` | Prevent AI arms races | International efforts should aim to prevent destabilizi | technology-and-ai.html |
| `TECH-MILS-0040` | Export controls in treaties | Support international controls on export and proliferat | technology-and-ai.html |
| `TECH-MILS-0041` | Strong sanctions for violations | Violations of international military-AI treaty obligati | technology-and-ai.html |
| `TECH-MILS-0042` | Sanctions for prohibited systems | Sanctions for deployment or export of prohibited milita | technology-and-ai.html |
| `TECH-MILS-0043` | Narrow reciprocal exceptions | If an adversary deploys prohibited military AI systems, | technology-and-ai.html |
| `TECH-MILS-0044` | Temporary reciprocal measures | Any reciprocal exception to military AI prohibitions mu | technology-and-ai.html |
| `TECH-MILS-0045` | Core prohibitions remain | Core prohibitions on nuclear AI control, fully autonomo | technology-and-ai.html |
| `TECH-MILS-0046` | Autonomous targeting as war crime | Use of AI systems to autonomously select or engage huma | technology-and-ai.html |
| `TECH-MILS-0047` | Target generation as unlawful | Deployment of AI systems that generate or recommend hum | technology-and-ai.html |
| `TECH-MILS-0048` | Violations of armed conflict principles | Use of AI systems in ways that violate principles of di | technology-and-ai.html |
| `TECH-MILS-0049` | Precision guidance exception | Use of AI solely for precision guidance to reduce colla | technology-and-ai.html |
| `TECH-MILS-0050` | Commanders remain liable | Individuals and commanders remain legally responsible f | technology-and-ai.html |
| `TECH-MILS-0051` | Dedicated cyber branch | Establish a dedicated and fully developed cyber branch  | technology-and-ai.html |
| `TECH-MILS-0052` | Cyber defense mission | The cyber branch shall be responsible for defense of cr | technology-and-ai.html |
| `TECH-MILS-0053` | Offensive cyber limits | Offensive cyber operations must be strictly limited aut | technology-and-ai.html |
| `TECH-MILS-0054` | Minimize civilian cyber impact | Cyber operations must minimize impact on civilian infra | technology-and-ai.html |
| `TECH-MILS-0055` | Cyber branch oversight | All cyber military operations are subject to oversight  | technology-and-ai.html |
| `TECH-MILS-0056` | No domestic cyber surveillance | The cyber military branch may not be used for domestic  | technology-and-ai.html |
| `TECH-MILS-0057` | Coordination with civilian agencies | The cyber branch must coordinate with civilian agencies | technology-and-ai.html |
| `TECH-MILS-0058` | International cyber norms | The cyber branch should operate in alignment with inter | technology-and-ai.html |
| `TECH-MKTS-0001` | Shared algorithmic systems used to coordinate prices ac | The use of shared algorithmic systems, common pricing s | technology-and-ai.html |
| `TECH-OVRG-0001` | Public AI surveillance registry | Require public registration and disclosure of all gover | technology-and-ai.html |
| `TECH-OVRG-0002` | Regular independent audits | Require regular independent audits of all authorized go | technology-and-ai.html |
| `TECH-OVRG-0003` | Sunset and reauthorization | All government AI surveillance authorities and systems  | technology-and-ai.html |
| `TECH-PRIV-0001` | Right to access without identification | Individuals have the right to access lawful online cont | technology-and-ai.html |
| `TECH-PRIV-0002` | Protect anonymous use | Anonymous and pseudonymous use of the internet must be  | technology-and-ai.html |
| `TECH-SURS-0002` | Ban AI mass public surveillance | Ban AI-powered mass surveillance of public spaces excep | technology-and-ai.html |
| `TECH-SURS-0004` | Ban government data purchases | Government may not purchase commercially collected surv | technology-and-ai.html |
| `TECH-SURS-0005` | Strict warrant requirements | Require strict warrants minimization procedures and aud | technology-and-ai.html |
| `TECH-SURS-0008` | Automatic expiration | Surveillance authorities must expire automatically unle | technology-and-ai.html |
| `TECH-SURS-0009` | Ban network mapping | Ban AI systems that map political social religious or a | technology-and-ai.html |
| `TECH-SURS-0010` | Protect journalists and attorneys | Ban AI-enabled surveillance of journalists sources atto | technology-and-ai.html |
| `TECH-SYNS-0001` | Ban deceptive synthetic media | Synthetic media must not be used to deceive the public  | technology-and-ai.html |
| `TECH-SYNS-0002` | Ban synthetic impersonation | Ban the use of AI-generated media to impersonate a real | technology-and-ai.html |
| `TECH-SYNS-0003` | Ban identity verification bypass | Ban use of synthetic media to bypass identity verificat | technology-and-ai.html |
| `TECH-SYNS-0004` | Ban non-consensual sexual content | Ban creation and distribution of non-consensual synthet | technology-and-ai.html |
| `TECH-SYNS-0005` | Ban false harmful depiction | Ban synthetic media that falsely depicts a real person  | technology-and-ai.html |
| `TECH-SYNS-0006` | Ban political manipulation | Ban use of synthetic media in political advertising or  | technology-and-ai.html |
| `TECH-SYNS-0007` | Ban misleading about officials | Ban synthetic media used to materially mislead the publ | technology-and-ai.html |
| `TECH-SYNS-0008` | Ban coordinated deception | Ban coordinated use of synthetic media to mislead the p | technology-and-ai.html |
| `TECH-SYNS-0009` | Disclosure requirement | Require clear disclosure when media is substantially AI | technology-and-ai.html |
| `TECH-SYNS-0010` | Provenance markers required | Require AI-generated video and audio to include persist | technology-and-ai.html |
| `TECH-SYNS-0011` | Open-source detection | Provenance markers must be detectable using publicly av | technology-and-ai.html |
| `TECH-SYNS-0012` | Safeguards against removal | Developers of generative media systems must implement r | technology-and-ai.html |
| `TECH-SYNS-0013` | Allow parody and satire | Allow synthetic media for parody, satire, or artistic e | technology-and-ai.html |
| `TECH-SYNS-0014` | Allow disclosed journalism use | Allow use of synthetic media in journalism or documenta | technology-and-ai.html |
| `TECH-SYNS-0015` | Allow consensual use | Allow use of synthetic media depicting real individuals | technology-and-ai.html |

---

## ID mismatches (div `id` attribute ≠ `<code class="rule-id">` element)

The `<code class="rule-id">` is the authoritative policy ID.
The `id=` attribute on the div is the HTML fragment anchor and should match.
These are data integrity issues to fix before Phase 2.

✅ No ID mismatches detected.

---

## Cards with no ID

✅ All cards have IDs.

---

## Duplicate IDs in HTML

**103 IDs appear on more than one card.**

| ID | Files |
|----|-------|
| `ADMN-VTLS-0001` | rights-and-civil-liberties.html, administrative-state.html |
| `ADMN-VTLS-0002` | rights-and-civil-liberties.html, administrative-state.html |
| `ADMN-VTLS-0003` | rights-and-civil-liberties.html, administrative-state.html |
| `ADMN-VTLS-0004` | rights-and-civil-liberties.html, administrative-state.html |
| `ADMN-VTLS-0005` | rights-and-civil-liberties.html, administrative-state.html |
| `ANTR-AGFS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-ALGO-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-ANTS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-CAPS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-CONS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-ENFL-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-MKTS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-MPYS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-NMDS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-PEQS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-PISS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `ANTR-TRAN-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CHKS-ACCS-0001` | executive-power.html, checks-and-balances.html |
| `CHKS-BRNS-0001` | checks-and-balances.html, foreign-policy.html |
| `CHKS-BRNS-0002` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FEDS-0001` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FEDS-0002` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FEDS-0003` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FEDS-0004` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FNDS-0001` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FNDS-0002` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FNDS-0003` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FNDS-0004` | checks-and-balances.html, foreign-policy.html |
| `CHKS-FNDS-0005` | checks-and-balances.html, foreign-policy.html |
| `CHKS-JURS-0001` | checks-and-balances.html, foreign-policy.html |
| `CHKS-JURS-0002` | checks-and-balances.html, foreign-policy.html |
| `CHKS-SHDS-0001` | executive-power.html, checks-and-balances.html |
| `CHKS-SHDS-0002` | executive-power.html, checks-and-balances.html |
| `CHKS-STAS-0001` | checks-and-balances.html, foreign-policy.html |
| `CHKS-STAS-0002` | checks-and-balances.html, foreign-policy.html |
| `CHKS-STAS-0003` | checks-and-balances.html, foreign-policy.html |
| `CHKS-WARS-0001` | executive-power.html, checks-and-balances.html |
| `CRPT-AUDT-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CRPT-FINC-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CRPT-FINC-0002` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CRPT-FINC-0003` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CRPT-FINC-0004` | anti-corruption.html, antitrust-and-corporate-power.html |
| `CRPT-LAWS-0001` | anti-corruption.html, antitrust-and-corporate-power.html |
| `EDUC-ECES-0031` | education.html |
| `EDUC-FINC-0001` | education.html, environment-and-agriculture.html |
| `EDUC-STDS-0001` | education.html, environment-and-agriculture.html |
| `ENVR-BIOS-0003` | environment-and-agriculture.html |
| `EXEC-AMND-0001` | executive-power.html |
| `EXEC-AMND-0002` | executive-power.html |
| `EXEC-AMND-0003` | executive-power.html |
| `EXEC-AMND-0004` | executive-power.html |
| `EXEC-CABS-0001` | executive-power.html |
| `EXEC-CABS-0002` | executive-power.html |
| `EXEC-CABS-0003` | executive-power.html |
| `EXEC-CABS-0004` | executive-power.html |
| `EXEC-CABS-0005` | executive-power.html |
| `EXEC-GRDS-0001` | executive-power.html |
| `EXEC-HOGS-0001` | executive-power.html |
| `EXEC-HOGS-0002` | executive-power.html |
| `EXEC-HOGS-0003` | executive-power.html |
| `EXEC-HOGS-0004` | executive-power.html |
| `EXEC-HOGS-0013` | executive-power.html |
| `EXEC-HOGS-0014` | executive-power.html |
| `EXEC-VPOF-0001` | executive-power.html |
| `EXEC-VPOF-0002` | executive-power.html |
| `EXEC-VPOF-0003` | executive-power.html |
| `EXEC-VPOF-0004` | executive-power.html |
| `EXEC-VPOF-0005` | executive-power.html |
| `EXEC-VPOF-0006` | executive-power.html |
| `HOUS-PUBL-0001` | housing.html |
| `HOUS-TENS-0001` | housing.html |
| `INFR-BLDS-0002` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-ENRS-0004` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-ENRS-0005` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-GRDS-0003` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-RAIL-0001` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-RAIL-0002` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-TRAN-0001` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-TRAN-0002` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-TRAN-0003` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-TRAN-0004` | information-and-media.html, infrastructure-and-public-goods.html |
| `INFR-TRAN-0005` | information-and-media.html, infrastructure-and-public-goods.html |
| `JUST-POLC-0006` | equal-justice-and-policing.html, gun-policy.html |
| `JUST-POLC-0007` | equal-justice-and-policing.html, gun-policy.html |
| `LABR-LABS-0001` | labor-and-workers-rights.html, taxation-and-wealth.html |
| `LABR-WRKS-0001` | labor-and-workers-rights.html, environment-and-agriculture.html |
| `LABR-WRKS-0002` | labor-and-workers-rights.html, environment-and-agriculture.html |
| `LABR-WRKS-0003` | labor-and-workers-rights.html, environment-and-agriculture.html |
| `LEGL-RPLS-0001` | legislative-reform.html |
| `MDIA-PRSS-0001` | information-and-media.html |
| `MDIA-PRSS-0002` | information-and-media.html |
| `TAXN-CORS-0001` | taxation-and-wealth.html |
| `TAXN-ENFL-0001` | taxation-and-wealth.html |
| `TAXN-INDS-0001` | taxation-and-wealth.html |
| `TECH-CHDS-0001` | technology-and-ai.html |
| `TECH-DEMS-0001` | technology-and-ai.html |
| `TECH-INFS-0001` | technology-and-ai.html |
| `TECH-INTL-0007` | technology-and-ai.html |
| `TECH-INTL-0008` | technology-and-ai.html |
| `TECH-INTL-0009` | technology-and-ai.html |
| `TECH-MEDA-0001` | technology-and-ai.html |
| `TECH-MILS-0006` | technology-and-ai.html |
| `TECH-SCIS-0001` | technology-and-ai.html |

---

## Markdown cross-reference

Policy IDs mentioned in `pillars/` markdown sources.

No policy IDs found in `pillars/` markdown files.

---

## Required actions before Phase 2

1. **Fix ID mismatches**: Update all div `id` attributes to match their `<code class="rule-id">` value
   (0 mismatches across all pillar files)
2. **Assign IDs to untagged cards**: {len(results['no_id_cards'])} cards have no ID — run `scripts/tag-policy-cards.py`
3. **Review divergences**: {len(results['diverge'])} items have mismatched text between HTML and DB — human decision required
4. **Backfill HTML-only items**: {len(results['html_only'])} HTML cards must be added to DB before DB becomes canonical
5. **Add DB-only items to HTML**: {len(results['db_only'])} DB items must appear as proposal cards in the correct pillar pages

Ali must sign off on this report before Phase 2 migration begins.
