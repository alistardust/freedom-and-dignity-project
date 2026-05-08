# Data Rights and Privacy Pillar Design Spec

**Date:** 2026-05-08
**Status:** Design approved -- ready for spec review
**Author:** Sam (GitHub Copilot) / Ali
**Research sources:**
- `policy/research/surveillance-capitalism/surveillance_capitalism_overview.md`
- `policy/research/surveillance-capitalism/surveillance_capitalism_academic_supplement.md`
- `policy/research/surveillance-pricing/surveillance_pricing_overview.md`

---

## Problem Statement

The platform currently has no dedicated pillar addressing the surveillance capitalism system --
the infrastructure through which behavioral data is extracted from virtually every American,
processed into prediction products, and used to price, target, manipulate, and discriminate
against individuals without meaningful notice or consent. Existing coverage is fragmented:
the Consumer Rights pillar's ALGO family covers algorithmic discrimination in consumer decisions,
but the data broker ecosystem that supplies those algorithms, the ad-tech infrastructure that
monetizes behavioral profiles, the behavioral modification systems that exploit them, and the
pricing mechanisms that extract from them are all unaddressed.

The research documents a $200-$260B industry touching every domain of life -- insurance pricing,
credit scoring, employment screening, political advertising, consumer pricing, and behavioral
manipulation -- with no comprehensive federal regulatory framework. Notice-and-choice frameworks
have been shown empirically and mathematically to provide no meaningful protection (McDonald and
Cranor 2008: reading every privacy policy you encounter would take 76 work days per year). The
academic evidence supports moving to data minimization and categorical prohibition, not disclosure.

This spec designs the Data Rights and Privacy pillar: a new pillar in the Real Freedom foundation
covering six policy families and 34 positions.

---

## Scope

**In scope:**
- New pillar: Data Rights and Privacy
- Domain code: `PRIV`
- Foundation: Real Freedom (primary), cross-referenced to Equal Justice
- Six policy families: 34 positions total
- New DB entries: `PRIV` domain, six `PRIV-XXXX` subdomains, 34 positions (status: PROPOSED)
- New pillar HTML page: `docs/pillars/data-rights-and-privacy.html`

**Out of scope:**
- Changes to existing CNSR-ALGO family (cross-referenced, not replaced)
- Surveillance pricing in Consumer Rights (SVPR is Family 4 of this pillar only)
- Platform-level AI governance (covered by Tech/AI pillar)
- Criminal justice surveillance (covered by Courts/Criminal Justice pillar)
- Immigration surveillance (cross-reference only)
- Children's Online Privacy Protection Act reform (cross-reference via PRIV-ADTC-0003)

---

## Baseline Architecture

All six families operate within a single baseline architecture established at the pillar level:

**Data minimization:** Data collection is limited to what is necessary for the stated purpose at
the time of collection. Collecting data for one purpose and repurposing it for another requires
a new independent lawful basis.

**Categorical prohibition:** Certain data categories cannot be collected, held, sold, or used
for any purpose regardless of consent. Consent mechanisms -- including ToS acceptance,
click-through consent, or contract -- cannot override categorical prohibitions. Affected
categories: location history beyond current session, inferred or self-disclosed health conditions,
reproductive health data, behavioral vulnerability scores, financial distress indicators,
immigration status, biometric identifiers, and inferred political, religious, or sexual
orientation.

**Consent fiction rejection:** Notice-and-choice frameworks do not satisfy the platform's
consent standard where the data practice would not survive meaningful informed consent. Burying
consent in privacy policies or terms of service does not constitute consent for purposes of
any family in this pillar.

**PolicyOS baseline:** All six families inherit KERN (universal), PRIV (privacy and surveillance
overlay), ECON (economic domination overlay), ENFA (enforcement overlay), and AIGV (AI governance
overlay where algorithmic systems are used). REGD applies to regulatory design.

---

## Family Map

| Code | Family name | Cards | PolicyOS primary |
|------|-------------|-------|-----------------|
| PRIV-DBKR | Data Broker Regulation | 6 | KERN-0008, PRIV-0001, PRIV-0002 |
| PRIV-ADTC | Ad-Tech and RTB Reform | 5 | PRIV-0001, PRIV-0002, KERN-0015 |
| PRIV-BMOD | Behavioral Modification | 5 | KERN-0016, KERN-0017, PRIV-0002 |
| PRIV-SVPR | Surveillance Pricing | 7 | ECON-0002, KERN-0008, KERN-0017 |
| PRIV-ALGO | Algorithmic Discrimination | 5 | KERN-0007, KERN-0012, KERN-0013 |
| PRIV-ENFA | Enforcement Architecture | 6 | ENFA-0001 through 0005, KERN-0027 |

**Total: 34 positions**

---

## Cross-Pillar References

| This pillar | References | Why |
|-------------|------------|-----|
| PRIV-DBKR | CNSR-ALGO (algorithmic consumer decisions) | Data broker products supply the ALGO systems |
| PRIV-ALGO | CNSR-ALGO | PRIV-ALGO extends FCRA; CNSR-ALGO covers specific consumer decision harms |
| PRIV-SVPR | CNSR-CFPS-0001, CFPS-0004 | CFPB independence required for enforcement |
| PRIV-ADTC | Tech/AI pillar | Algorithmic targeting systems overlap |
| PRIV-BMOD | Tech/AI pillar | Platform design accountability overlaps |
| PRIV-ALGO | Civil Rights / Equal Justice pillar | Disparate impact enforcement overlaps |

---

## Card Specifications

---

### Family 1: PRIV-DBKR -- Data Broker Regulation

---

#### PRIV-DBKR-0001 -- Definition and Scope of Data Broker Activity

**Rule-plain:**
A data broker is any company whose business is collecting and selling personal information about
people who are not their direct customers. This rule defines what counts as a data broker and
who must follow the rules in this family.

**Rule-stmt:**
A "data broker" is any commercial entity that collects, aggregates, processes, or sells personal
data about individuals who are not in a direct commercial relationship with that entity at the
time of collection. This definition includes: companies whose primary business is acquiring and
reselling personal data; companies that collect personal data as a secondary business and
monetize it through licensing, sale, or exchange; data analytics firms whose outputs incorporate
or are derived from third-party personal data; identity resolution and data enrichment services;
and credit reporting agencies not otherwise regulated under the Fair Credit Reporting Act with
respect to their non-FCRA data practices. Entities acting solely as data processors on behalf of
a data controller do not qualify as data brokers under this definition with respect to that
processing relationship. Entities that are otherwise covered by this definition are not exempt
due to partial FCRA coverage; FCRA-covered practices remain subject to FCRA, and non-FCRA
practices are subject to this family. A natural person's data about themselves does not
constitute data broker activity.

**Rule-notes:**
The definition follows the functional approach of the FTC's 2014 data broker report, which
identified hundreds of companies operating in this space. The Christl and Spiekermann (2016)
academic mapping identifies 10 data broker business models, most of which would be covered by
this definition. The FCRA carve-out is intentional: FCRA-regulated credit bureaus are also
data brokers in their non-FCRA operations, and this gap has historically allowed Experian,
TransUnion, and Equifax to sell marketing data without FCRA constraints. Cross-reference:
PRIV-DBKR-0002 (registration requirement).

---

#### PRIV-DBKR-0002 -- Federal Data Broker Registration

**Rule-plain:**
Every data broker doing business in the United States must register with the federal government.
This creates a public list so consumers and regulators know who these companies are and what
data they collect.

**Rule-stmt:**
Every data broker operating in the United States must register annually with the Federal Trade
Commission. Registration must include: the entity's legal name, principal business address, and
all trade names under which it operates; a description of each data category held (including
sensitive categories defined in PRIV-DBKR-0004); the primary sources through which data is
acquired; the primary commercial applications and buyer categories for which data is sold or
licensed; the retention period for each data category; and a designated privacy contact. The FTC
must maintain a publicly accessible registry. Registration fees must be sufficient to fund
administration of the registry and the centralized deletion mechanism established in PRIV-DBKR-0003.
Failure to register is a per-day violation enforceable by the FTC. Operating as an unregistered
data broker constitutes an unfair or deceptive act or practice under 15 U.S.C. § 45.

**Rule-notes:**
Modeled on Vermont's H.764 (2018), the first state data broker registration law, and California's
DELETE Act (SB 362, 2023). Vermont found 121 brokers registered in the first year; estimates
suggest 4,000+ operate in the U.S. (Privacy Rights Clearinghouse 2023). Registration without
a centralized deletion mechanism provides limited consumer benefit; see PRIV-DBKR-0003.
Cross-reference: PRIV-ENFA-0004 (proactive audit mandate).

---

#### PRIV-DBKR-0003 -- Centralized Consumer Deletion Mechanism

**Rule-plain:**
You should be able to tell all data brokers to delete your information with a single request,
not by tracking down 4,000 separate companies. This rule requires a one-stop deletion system
that every registered data broker must honor.

**Rule-stmt:**
The FTC must establish and maintain a centralized consumer data deletion and opt-out mechanism
accessible online and by written request at no cost to the consumer. A consumer's verified
request through this mechanism constitutes a binding deletion request directed simultaneously
to every registered data broker. Upon receipt of a centralized deletion request, each registered
data broker must: (1) delete all personal data pertaining to the requesting consumer within 30
days; (2) suppress reacquisition of that consumer's data from third-party sources for a period
of no less than 12 months; (3) notify all downstream recipients of the deleted data that the
data is subject to deletion. The mechanism must be accessible without creating an account with
any data broker or third-party service. Data brokers must honor centralized deletion requests
regardless of any contractual language purporting to permit continued retention. Noncompliance
with a deletion request is a per-consumer, per-day violation.

**Rule-notes:**
Modeled on California's DELETE Act (SB 362, 2023), which created California's first centralized
deletion mechanism effective January 2026. The federal model extends this approach nationally.
The 30-day deletion window and 12-month re-acquisition suppression follow the California model.
The "no account creation required" provision closes a loophole in which brokers required
consumers to create accounts (and thereby provide more data) to exercise deletion rights.
Acquisti, Brandimarte, and Loewenstein (2015) document the behavioral economics basis for why
individual broker-by-broker opt-out frameworks fail consumers. Cross-reference: PRIV-DBKR-0002
(registration as prerequisite), PRIV-ENFA-0002 (state AG enforcement).

---

#### PRIV-DBKR-0004 -- Categorical Prohibition on Sensitive Data

**Rule-plain:**
Some types of personal information are too sensitive to be collected and sold, period -- no
matter what you signed. Data brokers may not buy, sell, or trade in these categories.

**Rule-stmt:**
No data broker may collect, hold, sell, license, exchange, or otherwise transfer the following
categories of personal data ("prohibited categories"), regardless of any claimed consent, contract,
or terms-of-service provision:

(a) Precise location history: records of an individual's location at more than two distinct
points in time, or any continuous location tracking, excluding current-session navigation
services where data is not retained;

(b) Inferred or disclosed health and medical information: including diagnoses, medications,
mental health status, disability status, or information inferred from location visits to
healthcare facilities;

(c) Reproductive health and pregnancy data: including data inferred from purchases, app use,
location, or search behavior;

(d) Behavioral vulnerability and financial distress scores: predictive models of psychological
vulnerability, addiction likelihood, impulsivity, financial stress, or debt distress, derived
from behavioral signals;

(e) Immigration status: including citizenship status, visa type, country of birth, or any
proxy for immigration status;

(f) Biometric identifiers: including facial geometry, fingerprints, voiceprints, gait patterns,
and retinal scans;

(g) Inferred political affiliation, religious belief, or sexual orientation: including any
score, segment, or categorization derived from behavioral signals that predicts or indicates
these attributes.

The foregoing list is a floor. The FTC may add categories by rulemaking without requiring
legislative authorization. Consent-based exceptions are not available for prohibited categories;
the prohibition is absolute regardless of any claimed waiver.

**Rule-notes:**
The categorical approach follows GDPR Article 9 (special categories of personal data) but goes
further: the GDPR permits processing special categories with explicit consent; this rule does not.
The consent exception was deliberately excluded based on the academic evidence (Solove 2013,
Acquisti et al. 2015) that consent in data contexts is structurally fictional, and on the
PolicyOS data minimization baseline (PRIV-0001: collection minimized to stated purpose). The
reproductive health category was added in response to documented post-Dobbs risks of law
enforcement procurement of location and purchase data to identify patients seeking abortion
services. Cross-reference: PRIV-PRIV-0004 (government procurement ban), PRIV-DBKR-0001
(definition scope).

---

#### PRIV-DBKR-0005 -- Data Minimization and Purpose Limitation

**Rule-plain:**
Companies may only collect personal information for a specific, stated reason -- and once
collected, they can only use it for that reason. If they want to use it for something else,
that requires separate permission.

**Rule-stmt:**
Every data broker must identify, at the time of data collection or acquisition, the specific
commercial purpose for which each data category is being collected. Data may not be used for
any purpose that is incompatible with the purpose stated at collection ("purpose limitation").
A downstream application is incompatible if a reasonable person would not have expected,
at the time of collection, that their data would be used in that way. Incompatible secondary
use includes: using data collected for targeted advertising to build insurance underwriting
models; using data collected for identity verification to build behavioral marketing profiles;
and using data collected for product personalization to build willingness-to-pay pricing models.
Data brokers must document and retain purpose specifications for the period of data retention
plus three years. Secondary use for a new purpose requires either: (a) a new affirmative
consent that specifically identifies the new purpose; or (b) a finding that the secondary use
is strictly compatible with the original purpose under FTC rulemaking standards.

**Rule-notes:**
Purpose limitation is the core architectural feature of GDPR that, if enforced, would prohibit
most data broker activity (Schwartz 2019). The U.S. FIPPs framework nominally includes
"use limitation" but has never been meaningfully enforced in the commercial data context
(Cate 2010). The "reasonable person expectation" standard for incompatibility is drawn from
EU GDPR Recital 50 and Schwartz's comparative analysis. The advertising-to-insurance pipeline
(where behavioral data collected for ad targeting is repurposed for insurance underwriting) is
the most documented and commercially significant incompatible secondary use. Cross-reference:
PRIV-ALGO-0001 (FCRA extension to all consequential uses).

---

#### PRIV-DBKR-0006 -- Prohibition on Government Procurement of Commercial Surveillance Data

**Rule-plain:**
The government may not buy from data brokers what it could not collect itself under the
Constitution. This closes the loophole where agencies use data broker purchases to avoid the
warrant requirement.

**Rule-stmt:**
No federal, state, or local government agency, law enforcement entity, intelligence agency,
immigration enforcement agency, or contractor acting on their behalf may purchase, license,
access, or otherwise acquire from any data broker any data in the prohibited categories defined
in PRIV-DBKR-0004, or any data whose acquisition would otherwise require a warrant, court order,
or other legal process if sought directly. This prohibition applies regardless of whether the
government entity was the original collector of the data. Government acquisition of non-prohibited
commercial data for legitimate administrative purposes (such as address verification for benefit
delivery) remains permissible subject to stated purpose limitation and data minimization
requirements. Violations are actionable under 42 U.S.C. § 1983 where applicable.

**Rule-notes:**
PLOS-PRIV-0004 (system principles) directly addresses this: "Commercial surveillance data may
not be purchased or used by government actors to circumvent constitutional limitations on direct
government surveillance." This rule operationalizes that principle. The Fourth Amendment's
third-party doctrine (Smith v. Maryland, 1979; Carpenter v. United States, 2018) creates an
ongoing loophole: data voluntarily shared with a service provider may be obtainable without
a warrant. Government purchases of data broker databases have been documented by the Wall Street
Journal (2020), the Office of the Director of National Intelligence (2024 ODNI report), and
ACLU litigation. The ODNI report acknowledged agencies were acquiring commercially available
data that would require legal process if sought directly from individuals.

---

### Family 2: PRIV-ADTC -- Ad-Tech and Real-Time Bidding Reform

---

#### PRIV-ADTC-0001 -- RTB Bid Request Data Minimization

**Rule-plain:**
When websites sell ad space in real-time auctions, they currently broadcast your personal
profile to hundreds of companies who didn't win the auction and have no right to your data.
This rule limits what information can be shared in those auctions.

**Rule-stmt:**
No party participating in a real-time bidding (RTB) auction, programmatic advertising exchange,
header bidding operation, or equivalent automated ad auction mechanism may include in any bid
request or equivalent auction signal: precise or approximate location (beyond country or
designated market area); device fingerprint data; behavioral profile data or audience segment
identifiers derived from cross-site tracking; data in any prohibited category under
PRIV-DBKR-0004; or any persistent identifier that enables cross-context tracking of an
individual. Bid requests may include: page-level contextual signals (URL category, page topic,
content rating); session-level non-persistent identifiers; and geographic context at the
designated market area (DMA) level. The FTC, in consultation with the FCC, must establish
technical standards for compliant bid request formats within 18 months of enactment.

**Rule-notes:**
The Irish Council for Civil Liberties (ICCL 2022) documented that the average American's
digital signature is broadcast to RTB auction participants hundreds of times per day. Critically,
all auction participants receive the bid request -- and with it the user's behavioral profile --
regardless of whether they win. This "observe without winning" mechanism allows data collection
at no cost and creates the primary surveillance externality of the RTB system. The FTC has
documented RTB-based data leakage (FTC 2014, 2021). Technical standards are necessary because
RTB protocols (OpenRTB) are industry specifications, not regulatory standards, and participants
can include prohibited data without detection absent standardized format requirements.
Cross-reference: PRIV-DBKR-0004 (prohibited categories).

---

#### PRIV-ADTC-0002 -- Ban on Behavioral Targeting Using Sensitive Data

**Rule-plain:**
Advertisers may not target people using sensitive personal information -- like their health
conditions, political views, financial struggles, or location history. These categories are too
dangerous to be used to target people with ads.

**Rule-stmt:**
No advertiser, publisher, demand-side platform (DSP), supply-side platform (SSP), data
management platform (DMP), or other participant in a digital advertising transaction may
target, segment, or select advertising audiences on the basis of any data in the prohibited
categories defined in PRIV-DBKR-0004, or on the basis of any behavioral inferences derived
from those categories. This prohibition applies regardless of whether the targeting data was
obtained directly or from a third-party data broker, and regardless of whether the category
data is labeled as such. Modeling or lookalike audience creation based on prohibited-category
seed audiences is prohibited. Contextual advertising -- targeting based on the content of
the page or app context in which an advertisement is displayed, without reference to individual
user profiles -- is fully permitted. Topic-based interest targeting that does not use individual
behavioral profiles and does not incorporate prohibited categories is permitted.

**Rule-notes:**
Goldfarb and Tucker (2011) found that privacy regulation reducing behavioral targeting reduced
advertising effectiveness by 65% for behavioral versus contextual comparison -- the industry's
primary economic counter-argument. However, this finding predates current AI-enhanced contextual
advertising systems (which have significantly narrowed the performance gap), and the welfare
analysis does not account for the consumer surplus transferred to advertisers through behavioral
extraction. Johnson (2013) finds that the market for consumer data is characterized by market
failure (Bergemann and Bonatti 2015 provide the theoretical basis): firms systematically
undersupply privacy. Contextual advertising has existed for decades and supports viable ad
markets without user profiling. Cross-reference: PRIV-ADTC-0001 (RTB data minimization),
PRIV-DBKR-0004 (prohibited categories).

---

#### PRIV-ADTC-0003 -- Prohibition on Behavioral Targeting of Minors

**Rule-plain:**
Advertisers may not use personal data to target ads at anyone under 18. This is an absolute
rule -- no behavioral advertising to children or teenagers, regardless of what any app or
website says in its terms of service.

**Rule-stmt:**
No advertiser, publisher, advertising platform, or data broker may target advertising to any
individual known or reasonably inferable to be under the age of 18 on the basis of any
behavioral, demographic, psychographic, or location profile data. For purposes of this rule,
a minor is "reasonably inferable" when: the platform, service, or application is primarily
directed at minors; the individual has disclosed their age as under 18 to the platform; the
behavioral signals of the individual are consistent with a minor as established by FTC guidance;
or the data was collected through a service that obtained parental consent under COPPA. Platforms
primarily directed at minors may serve only contextual advertising. This rule does not affect
age-verification requirements or parental consent obligations under COPPA; it establishes a
prohibition additional to and independent of COPPA.

**Rule-notes:**
This rule is grounded in consent capacity and developmental autonomy, not contested mental
health causation claims. Minors cannot provide legally binding consent to behavioral profiling
under existing contract law, and the behavioral economics evidence (Acquisti et al. 2015)
showing that adults cannot provide informed consent to data practices applies with greater force
to minors. The contested social media mental health evidence (Twenge et al. 2018 vs. Orben and
Przybylski 2019) is deliberately not invoked here. COPPA (1998) provides a foundation for
minors' online privacy protection but covers only directed-at-children services for under-13
and has significant enforcement gaps. This rule extends categorical protection to all minors
and applies to all behavioral targeting regardless of platform designation. Cross-reference:
PRIV-BMOD-0004 (minors -- engagement prohibition).

---

#### PRIV-ADTC-0004 -- Political Advertising Transparency Repository

**Rule-plain:**
Every political ad shown online must be logged in a public database so voters can see who
paid for it, who it was targeting, and how much was spent. Hidden political targeting is a
threat to democracy.

**Rule-stmt:**
Every platform with more than 1 million U.S. monthly active users that serves political
advertising -- defined as any paid content concerning candidates, ballot measures, political
parties, or policies before a legislative or regulatory body -- must maintain and provide
public access to a real-time advertising transparency repository. The repository must contain,
for each political advertisement served: the full content of the advertisement; the name and
address of the paying advertiser; the total amount paid; the targeting parameters used (at the
category level, not individual level); the total number of impressions served; and the platforms
and formats on which it was served. The repository must be publicly searchable by advertiser,
date, and keyword. Data must be retained for a minimum of five years. Failure to maintain or
provide access to the repository is a per-day violation.

**Rule-notes:**
Modeled on the EU Digital Services Act Article 39 (political advertising transparency
repository) and the FEC's existing disclosure requirements for broadcast political advertising.
The research documents psychographic micro-targeting in the Cambridge Analytica operation
(Zuboff 2019; Cadwalladr and Graham-Harrison 2018). The repository does not require disclosure
of individual targeting -- which would itself create privacy risks -- but requires category-level
targeting disclosure sufficient for independent researchers and journalists to assess targeting
patterns. Cross-reference: Democracy/Elections pillar (political campaign finance and advertising).

---

#### PRIV-ADTC-0005 -- Contextual Advertising Safe Harbor

**Rule-plain:**
Advertising based on the content of the page you are reading -- not on your personal profile --
is fully permitted. This rule makes clear that targeting based on what you are reading right now
is different from surveillance-based targeting and is not restricted.

**Rule-stmt:**
Nothing in this family restricts advertising served on the basis of contextual signals alone.
Contextual advertising means advertising selected and served based on: the content, topic, or
category of the webpage, application screen, or media in which the advertisement is displayed;
the time of day; the geographic location at the DMA level or broader; the language of the
content; or the device type and screen size. Contextual advertising is not subject to the
restrictions in PRIV-ADTC-0001 or PRIV-ADTC-0002, provided that: no individual behavioral
profile is used in selecting the advertisement; no cross-context tracking identifier is
associated with the served impression; and the contextual signals used are not themselves
derived from prohibited-category data. This safe harbor does not permit contextual targeting
that functions as a proxy for prohibited-category targeting (e.g., targeting users of
reproductive-health-content pages with financial exploitation advertising).

**Rule-notes:**
The contextual safe harbor is necessary to prevent this family from being interpreted as a
general prohibition on digital advertising, which is neither the intent nor the appropriate
policy outcome. Contextual advertising has supported viable online publishing for decades
and does not require individual surveillance. The proxy-exploitation carve-out closes the
obvious evasion path: using "contextual" labels to target vulnerable populations (people reading
about addiction, mental health, debt, or pregnancy) with exploitative products.

---

### Family 3: PRIV-BMOD -- Behavioral Modification and Manipulation

---

#### PRIV-BMOD-0001 -- Dark Patterns Prohibition

**Rule-plain:**
Companies may not use design tricks to make you do things you did not intend to do -- like
signing up for a subscription without realizing it, or making it easy to say yes and hard to
say no. These are called dark patterns, and they are prohibited.

**Rule-stmt:**
No commercial entity operating a digital interface -- including websites, applications, and
connected device interfaces -- may deploy interface design that: (a) makes it materially easier
to complete a data-sharing, subscription, or consent action than to decline it ("asymmetric
friction"); (b) uses false urgency, artificial scarcity, or countdown timers to pressure
decisions about data sharing, subscription, or consent; (c) employs visual design that
obscures, minimizes, or de-emphasizes privacy-protective choices relative to data-sharing
choices; (d) requires multiple steps to withdraw consent where a single step was required to
give it ("roach motel"); (e) uses confirmshaming -- labeling the opt-out option as a negative
self-assessment ("No, I don't want savings"); or (f) inserts product additions, service upgrades,
or subscriptions into purchase flows without explicit separate confirmation ("sneak into basket").
The taxonomy of prohibited dark patterns is not exhaustive; the FTC must issue and periodically
update guidance on prohibited dark patterns. Third-party services that provide dark pattern
implementations as a commercial product are jointly liable with deploying entities.

**Rule-notes:**
Mathur et al. (2019) found 1,818 dark pattern instances across 11,000 shopping websites and
identified 22 third-party companies offering dark pattern tools as commercial services --
establishing that dark patterns are industrialized, not idiosyncratic. The joint liability
provision targets those third-party service providers directly. Gray et al. (2018) established
that dark patterns require professional design expertise and shared practitioner vocabulary,
meaning they are the product of deliberate design choices. The legal basis for prohibition
under FTC Section 5 is clear (FTC v. Nudge LLC et al., 2022; FTC dark pattern enforcement
actions 2022-2024). This rule codifies and extends that authority. Cross-reference:
PRIV-BMOD-0004 (minors -- categorical prohibition), PRIV-ADTC-0003 (targeting of minors).

---

#### PRIV-BMOD-0002 -- Engagement Optimization Prohibition

**Rule-plain:**
Platforms may not deliberately design features to keep you scrolling or using their service
longer than you intended, using psychological techniques that override your own judgment. Making
a product genuinely useful is fine; exploiting your attention is not.

**Rule-stmt:**
No platform with more than 1 million U.S. monthly active users may deploy engagement
optimization systems that are designed to maximize time spent, session length, or interaction
frequency through mechanisms that exploit psychological vulnerabilities rather than deliver
genuine utility. Prohibited mechanisms include: variable-ratio reinforcement notification
schedules designed to produce compulsive checking behavior; infinite scroll implementations
that remove natural stopping points from content feeds without an active user request to
continue; autoplay of content or media in sequences designed to prevent session termination;
and personalized emotional-state targeting that uses inferred emotional vulnerability, boredom,
loneliness, or distress signals to increase engagement. Platforms must provide users with
accessible controls to set daily usage limits, disable autoplay and infinite scroll, and manage
notification frequency and timing. These controls must be available at no charge and accessible
within two user interactions from any page of the platform.

**Rule-notes:**
Meshi, Tamir, and Heekeren (2015) document the reward circuitry (ventral striatum activation)
engaged by social media notifications and likes -- establishing the neurological basis for
variable reinforcement schedule effects. The rule is grounded in PLOS-KERN-0016 ("No system
may rely on deprivation, coercion, fear, or chronic precarity as a primary mechanism of
compliance or control") and PLOS-KERN-0017 ("Incentive structures may not reward denial,
extraction, concealment, or deprivation of rights or essential services"). The social media
mental health causation evidence is actively contested (Twenge et al. 2018 vs. Orben and
Przybylski 2019) and is deliberately not cited as the basis for this rule. The basis is
behavioral autonomy and the consumer protection principle that design may not exploit
psychological architecture to override user intent. Cross-reference: PRIV-BMOD-0004
(minors -- all engagement features prohibited categorically).

---

#### PRIV-BMOD-0003 -- Psychographic Profiling for Persuasion Purposes

**Rule-plain:**
Companies may not build psychological profiles of individuals and use those profiles to
personalize persuasion -- including advertising and political messaging -- in ways designed
to exploit their specific emotional vulnerabilities. Knowing that a person is anxious,
lonely, or grieving and targeting them with that in mind is manipulation, not marketing.

**Rule-stmt:**
No commercial entity may construct or use psychographic profiles -- predictive models of
individual psychological traits, emotional states, vulnerabilities, personality dimensions,
or behavioral tendencies derived from behavioral data -- for purposes of personalized
persuasion in commercial or political contexts. Prohibited uses include: personalized
advertising that selects or adjusts message content, tone, framing, or imagery based on
inferred psychological traits or emotional states; political messaging personalized to
exploit inferred psychological vulnerabilities; and A/B testing systems that optimize
for persuasion effectiveness by identifying psychological levers specific to individual users
rather than by improving the substantive quality of content. General content relevance
targeting -- selecting advertisements based on expressed interests or stated preferences --
is not psychographic profiling under this rule. The FTC must issue guidance within 12 months
of enactment distinguishing permissible interest-based targeting from prohibited psychographic
persuasion.

**Rule-notes:**
The Cambridge Analytica operation is the documented large-scale deployment of psychographic
profiling for political persuasion: profiles built from Facebook data for approximately 87
million users, used to personalize political advertising in the 2016 election (Cadwalladr and
Graham-Harrison 2018). Zuboff (2019) describes behavioral modification as the third and most
advanced stage of surveillance capitalism -- beyond prediction to guaranteed behavior through
psychological manipulation. Richards and Hartzog's (2019) duty-of-loyalty framework would
categorically prohibit psychographic profiling as incompatible with a fiduciary obligation to
users. The commercial/political targeting of psychological vulnerability implicates PLOS-KERN-0016
and Platform Value 3 (Real Liberty): manipulation that targets psychological vulnerabilities is
a form of non-coercive coercion that hollows out meaningful agency.

---

#### PRIV-BMOD-0004 -- Minors: Categorical Engagement Prohibition

**Rule-plain:**
For users under 18, all engagement optimization features are prohibited entirely -- not just
regulated. No infinite scroll, no variable reinforcement notifications, no autoplay, no
psychographic profiling.

**Rule-stmt:**
With respect to any user known or reasonably inferable to be under the age of 18, the
prohibitions in PRIV-BMOD-0001 through PRIV-BMOD-0003 apply as categorical prohibitions
without exception. In addition, the following practices are prohibited with respect to minors
regardless of whether they would otherwise be permitted under PRIV-BMOD-0002: personalized
content ranking that optimizes for engagement metrics rather than stated user preferences or
chronological order; social comparison features that display follower counts, like counts,
or equivalent social validation metrics in feeds or profile contexts; streak mechanics or
activity reward systems that create daily engagement obligations; and push notifications of
any type between the hours of 11:00 PM and 7:00 AM local time. These prohibitions apply
regardless of platform terms of service, parental consent provisions, or stated user age.
A platform that collects age data and fails to apply these protections to identified minors is
in violation even if the user misrepresented their age.

**Rule-notes:**
This rule is grounded entirely in consent capacity and developmental autonomy under Platform
Value 3 (Real Liberty) and Value 2 (Equal Standing). Minors lack the legal capacity to consent
to behavioral profiling and lack the fully developed prefrontal cortex structures associated
with resistance to variable-ratio reinforcement effects (Meshi et al. 2015). The social
comparison and social validation features are grounded in Twenge et al. (2018) -- while the
overall causal claim for mental health harm is contested, the specific mechanism of social
comparison through like counts and follower displays has more robust empirical support than
aggregate screen time measures. The push notification curfew follows the UK's Children's Code
(Age Appropriate Design Code, 2020). Cross-reference: PRIV-ADTC-0003 (no behavioral targeting
of minors).

---

#### PRIV-BMOD-0005 -- Third-Party Behavioral Modification Service Liability

**Rule-plain:**
Companies that sell the tools used to manipulate people are as responsible as the companies
that use those tools. If you build a product designed to help others exploit users, you are
liable when that happens.

**Rule-stmt:**
Any third-party service provider that markets, licenses, or otherwise provides behavioral
modification tools, dark pattern implementations, psychographic targeting systems, or engagement
optimization systems as commercial products bears joint and several liability with any client
entity that deploys those tools in violation of PRIV-BMOD-0001 through PRIV-BMOD-0004. A
third-party service provider is liable under this rule if it: knew or reasonably should have
known that its product was designed or primarily used for a prohibited purpose; marketed its
product using language indicating prohibited uses; or failed to establish and enforce
contractual use restrictions prohibiting use in violation of this family. Service providers
that demonstrate affirmative steps to prevent prohibited use, including binding contractual
prohibitions, contract termination procedures for violations, and reasonable monitoring, may
petition the FTC for a compliance safe harbor. This rule applies to providers of recommendation
algorithm services, notification optimization services, engagement analytics platforms, and
A/B testing platforms whose optimization targets include engagement metrics.

**Rule-notes:**
Mathur et al. (2019) identified 22 third-party companies offering dark pattern implementations
as commercial services. Without third-party liability, prohibitions on dark patterns and
engagement optimization can be evaded by outsourcing to specialized providers who can claim
ignorance of end-use. The joint and several liability model follows FCRA furnisher liability
(15 U.S.C. § 1681s-2) and COPPA service provider liability, both of which establish downstream
liability for third-party data service providers. The affirmative compliance safe harbor prevents
over-deterrence of general-purpose analytics tools that have incidental prohibited uses.

---

### Family 4: PRIV-SVPR -- Surveillance Pricing

*Note: This family was previously designed as a standalone Consumer Rights family. The
7-card structure is reproduced here as Family 4 of the Data Rights and Privacy pillar,
with position IDs updated to PRIV-SVPR.*

---

#### PRIV-SVPR-0001 -- Definitions and Scope

**Rule-plain:**
Surveillance pricing is when a company uses your personal data to figure out the most you
would pay for something -- and then charges you exactly that. This rule defines what counts
as surveillance pricing and what doesn't.

**Rule-stmt:**
"Surveillance pricing" means the use of any personal data profile -- whether assembled by
data brokers, platform behavioral tracking, purchase history, location data, device fingerprints,
credit data, inferred psychological attributes, or any combination -- to set, adjust, confirm,
or personalize a price for a specific individual above the price that individual would have been
charged without the profiling. The definition is technology-neutral and applies to any mechanism
by which individual-level behavioral or demographic data is used to identify and extract a
price closer to that individual's maximum willingness to pay. The following are not surveillance
pricing under this rule: (a) uniform time-based dynamic pricing applied identically to all
consumers, such as peak and off-peak pricing or event-based surge pricing; (b) loyalty and
rewards programs that reduce price below the standard rate for eligible participants; (c)
negotiated bulk or volume pricing; (d) geographic pricing variations based on publicly known
cost factors such as distribution cost, local tax, or regulatory compliance cost; and (e)
categorical promotional pricing applied uniformly to a group defined by an explicit, disclosed
criterion such as student status or military affiliation.

**Rule-notes:**
The FTC's January 2025 Surveillance Pricing Study (subsequently removed from the FTC website
following the administration change) studied eight companies and found use of browsing history,
GPS location, device fingerprints, social media data, and credit data for individual
willingness-to-pay extraction. Shiller (2020) empirically demonstrates that comprehensive
behavioral tracking enables near-perfect consumer surplus extraction: 12.2% profit increase
vs. 0.8% for demographic-only discrimination. The technology-neutral definition is required by
PLOS-KERN-0022 (systems must adapt to technological change without crisis overhaul). Cross-
reference: PRIV-DBKR-0004 (categorical prohibition on behavioral vulnerability scores);
PRIV-SVPR-0003 (data broker pipeline ban).

---

#### PRIV-SVPR-0002 -- Core Prohibition

**Rule-plain:**
No company may use a personal profile to charge you more than they would charge someone
without that profile. It does not matter whether the data came from the company itself or
from a data broker.

**Rule-stmt:**
No person, retailer, platform, service provider, financial institution, insurer, healthcare
provider, or pricing intermediary may use any personal data profile to set a price for a
specific consumer that exceeds the price an unprofiled consumer of equivalent transaction
characteristics would pay for the same product, service, or access. This prohibition applies
regardless of: whether the profile was assembled by the selling entity or obtained from a
third-party data broker; whether the consumer has a preexisting relationship with the seller;
whether the consumer provided data knowingly or unknowingly; and whether the profiling is
accomplished through first-party behavioral data, third-party data acquisition, or inference
from either. "Equivalent transaction characteristics" means the same product or service,
purchased at the same time, in the same geographic market, through the same channel. The
existence of a loyalty discount for other consumers does not satisfy this rule; the baseline
for the unprofiled price is the standard price available to consumers who have not provided
profiling data.

**Rule-notes:**
PLOS-ECON-0002 is dispositive: "where a sector exhibits market concentration sufficient to
deny workers, tenants, borrowers, or consumers the practical ability to refuse, negotiate, or
exit, rule design must include structural remedies. Disclosure and transparency requirements
alone are not structural remedies." The surveillance pricing ecosystem is invisible to consumers;
they cannot refuse what they cannot detect. Bergemann, Brooks, and Morris (2015) establish
that perfect first-degree price discrimination captures all consumer surplus for the seller.
Varian (1985) -- the industry's economic counter-argument -- applies to third-degree market
segment discrimination, not to first-degree individual-level extraction; and in any case
assumes lower prices reach lower-income consumers, which surveillance pricing evidence
contradicts. Cross-reference: PRIV-SVPR-0001 (definitions), PRIV-SVPR-0003 (data broker
pipeline).

---

#### PRIV-SVPR-0003 -- Data Broker Pipeline Prohibition

**Rule-plain:**
Data brokers and data companies may not create or sell profiles designed to predict how much
a person is willing to pay. Selling tools for extraction is part of the extraction.

**Rule-stmt:**
No data broker, data analytics company, financial data provider, or pricing intermediary may
compile, sell, license, or otherwise provide: consumer willingness-to-pay profiles; price
sensitivity scores; behavioral vulnerability scores used in pricing; or predictive models of
individual maximum acceptable price -- for use in any consumer-facing pricing system. Violations
are joint and several with any retail or service entity that purchases and deploys such profiles
in violation of PRIV-SVPR-0002. A data broker claiming it did not know its product would be
used for prohibited surveillance pricing bears the burden of demonstrating the affirmative steps
it took to prevent such use, including contractual prohibitions, use monitoring, and contract
termination upon violation discovery.

**Rule-notes:**
The FTC's 2025 Surveillance Pricing Study identified Mastercard's Dynamic Yield subsidiary,
Revionics/Aptos, McKinsey, JPMorgan Chase, Pros Holdings, Bloomreach, and Task Systems as
participants in the surveillance pricing intermediary market. The joint-and-several liability
provision follows the BMOD third-party liability model (PRIV-BMOD-0005). Closing the
data-broker-supply-chain loophole is essential: a retail prohibition without a pipeline
prohibition creates an enforcement gap where brokers continue supplying profiles and retailers
claim the profiles were "general market analytics" rather than willingness-to-pay extraction.
Cross-reference: PRIV-DBKR-0004 (categorical prohibition on behavioral vulnerability scores
independently of this family).

---

#### PRIV-SVPR-0004 -- Permitted Pricing Practices

**Rule-plain:**
Prices can still go up and down based on supply and demand, timing, and where you are. You can
still get discounts for being a student or a member. This rule describes what is clearly allowed
so there is no confusion.

**Rule-stmt:**
Nothing in PRIV-SVPR-0001 through PRIV-SVPR-0003 restricts the following pricing practices:
(a) dynamic pricing based on supply and demand applied uniformly to all purchasers at the time
of transaction, where the pricing mechanism does not use individual behavioral profiles;
(b) loyalty discounts, rewards programs, and membership pricing that reduce a consumer's price
below the standard price, provided the discount is available on uniform disclosed terms;
(c) negotiated pricing in commercial and business-to-business transactions;
(d) geographic pricing variations based on publicly known and documented cost differentials;
(e) categorical promotional pricing available to all members of a disclosed class;
(f) insurance rating factors that are actuarially justified, independently reviewed, and
applied to groups rather than individuals on the basis of a categorical risk factor, not on the
basis of behavioral surveillance data about the specific individual;
(g) auction-based pricing mechanisms where all participants bid under equivalent information
conditions.

**Rule-notes:**
Surge pricing and yield management (airline pricing) are not covered because the mechanism --
adjusting price based on demand at a point in time, applied uniformly -- does not extract
individual willingness to pay through behavioral profiling. The FTC has previously distinguished
"personalized pricing" from "dynamic pricing" on this basis. The insurance actuarial carve-out
is narrow: it covers group-level risk categories, not individual behavioral surveillance. The
growing practice of using behavioral data in insurance underwriting is separately addressed
in PRIV-ALGO (algorithmic discrimination prohibition). Cross-reference: PRIV-ALGO-0001
(FCRA extension to consequential decisions including insurance).

---

#### PRIV-SVPR-0005 -- Transparency and Disclosure

**Rule-plain:**
If your price was individually set using personal data, you have the right to know that. And
when regulators ask to review the pricing system, companies cannot hide behind trade secrets.

**Rule-stmt:**
Any commercial entity that uses personal data profiles in any pricing system must: (a) disclose
to consumers upon request whether their specific transaction price was determined using a
personal data profile or behavioral model, and if so, the general categories of data used;
(b) disclose to the FTC and CFPB upon request the full methodology, data categories, models,
and vendor relationships used in its pricing systems; (c) notify the FTC within 60 days of
deploying any new pricing system that incorporates personal behavioral data. Trade secret
claims do not override regulatory disclosure obligations under (b). Proprietary model
specifications may be shared with regulators under appropriate confidentiality agreements;
trade secret claims may not prevent regulatory inspection of the category of data used, the
general methodology applied, or the demographic distribution of pricing outcomes.

**Rule-notes:**
PLOS-KERN-0008 prohibits "hidden rules, inaccessible information, trade-secret shields, or
black-box procedures to determine consequential outcomes." Consumer transaction prices are
consequential outcomes. Trade-secret exceptions are available for regulatory disclosure under
narrowly defined conditions: the methodology may remain confidential from competitors and the
public, but not from regulators with enforcement authority. The PLOS-AIGV-0008 provision --
"affected individuals, regulators, and courts must be able to review rights-impacting AI systems
without trade-secret claims swallowing accountability" -- directly applies to AI-driven pricing
systems. Cross-reference: PRIV-SVPR-0006 (enforcement authority with audit power).

---

#### PRIV-SVPR-0006 -- Enforcement Authority

**Rule-plain:**
The FTC is the main regulator for most companies. The CFPB covers banks, insurance companies,
and lenders. Both regulators must actively look for violations -- they cannot wait for consumers
to complain about pricing systems they cannot see.

**Rule-stmt:**
The Federal Trade Commission has primary enforcement jurisdiction over PRIV-SVPR with respect
to retail, e-commerce, platform, and non-financial service entities. The Consumer Financial
Protection Bureau has primary enforcement jurisdiction with respect to financial institutions,
insurance entities, mortgage lenders, and credit product providers. Both agencies have
concurrent enforcement authority where entities operate in multiple sectors. Both agencies
must conduct proactive surveillance pricing audits -- enforcement is not limited to
consumer complaint response. Proactive audit authority includes: the right to demand pricing
system documentation from any entity suspected of prohibited surveillance pricing; the right
to conduct anonymous test purchases to identify personalized pricing; and the right to compel
disclosure of pricing algorithm parameters under regulatory confidentiality. Civil penalties
may be imposed per transaction, per consumer, or per violation period at the enforcing agency's
discretion subject to proportionality standards established by rulemaking.

**Rule-notes:**
Complaint-driven enforcement is structurally inadequate for surveillance pricing because
consumers cannot detect whether their price was individually set through behavioral profiling.
This is the enforcement design failure identified in PolicyOS PAOS-ENFC (enforcement
architecture must include proactive monitoring, not just complaint response). The FTC/CFPB
lane assignment follows the model established for financial regulation generally: CFPB
covers financial entities regulated under Dodd-Frank Title X; FTC covers the rest.
The anonymous test purchase authority -- sending test buyers to compare prices -- is the
most direct enforcement mechanism and has been used in housing and credit discrimination
investigations. Cross-reference: PRIV-ENFA-0001 (enforcement architecture), CNSR-CFPS-0001
(CFPB independence and funding baseline).

---

#### PRIV-SVPR-0007 -- Private Right of Action

**Rule-plain:**
If you were charged more because of a hidden personal profile, you can sue the company even
if you cannot prove exactly how much more you paid. The law sets minimum damages so that
individual cases are worth bringing.

**Rule-stmt:**
Any consumer subjected to prohibited surveillance pricing in violation of PRIV-SVPR-0002 may
bring a civil action in any court of competent jurisdiction. Statutory damages: not less than
$500 nor more than $5,000 per transaction, with the specific amount determined by the court
based on the willfulness, duration, and scale of the violation. Actual damages are available
where the consumer can demonstrate damages exceeding the statutory minimum. Class actions are
available. Prevailing plaintiffs are entitled to reasonable attorney's fees and costs. A
defendant may avoid per-transaction damages for a specific transaction by demonstrating by
clear and convincing evidence that the transaction price was not determined by a prohibited
personal data profile. Willful violations -- including continued use of a prohibited pricing
system after receiving a regulatory notice of probable violation -- are subject to treble
statutory damages.

**Rule-notes:**
Statutory damages following the FCRA model (15 U.S.C. § 1681n: $100-$1,000 per violation
plus attorney's fees) and the Illinois BIPA model ($1,000 per negligent, $5,000 per intentional
violation) provide the closest precedents. The burden-shifting provision -- placing on the
defendant the obligation to prove the price was not profiling-driven -- addresses the fundamental
information asymmetry: consumers cannot access the pricing algorithm, so the standard
preponderance of evidence rule would systematically bar recovery. Citron and Solove (2022)
provide the doctrinal framework for recognizing privacy-related harms as legally cognizable
injuries sufficient to support standing. Cross-reference: PRIV-ENFA-0003 (private right of action
for data broker violations generally).

---

### Family 5: PRIV-ALGO -- Algorithmic Discrimination Prohibition

---

#### PRIV-ALGO-0001 -- FCRA Extension to All Consequential Algorithmic Decisions

**Rule-plain:**
The 1970 Fair Credit Reporting Act covers credit reports but was never updated for the data
broker era. This rule extends its protections to all data broker products used in decisions
that affect your life -- insurance, employment, housing, benefits, and more.

**Rule-stmt:**
The Fair Credit Reporting Act (15 U.S.C. § 1681 et seq.) is extended to apply to all data
broker products -- including behavioral profiles, predictive scores, algorithmic assessments,
and any other data broker output -- used in any of the following contexts ("covered uses"):
credit and lending decisions; insurance underwriting and pricing; employment hiring, promotion,
or termination decisions; housing rental, mortgage, or lease decisions; public benefits
eligibility determinations; educational admissions and financial aid decisions; and any other
decision that materially affects an individual's life chances as defined by FTC rulemaking.
For purposes of this rule, an entity using any data broker product in a covered use is a
"consumer reporting agency" with respect to that use regardless of whether it is otherwise
subject to FCRA. Affected consumers have all FCRA rights with respect to covered-use data,
including the right to access the data used, to dispute its accuracy, and to receive adverse
action notices. The cost of extending these rights to covered-use data falls on the entity
making the covered-use decision.

**Rule-notes:**
FCRA's 1970 definition of "consumer reporting agency" covers entities that "regularly" assemble
or evaluate consumer information for defined purposes. Most data brokers are not consumer
reporting agencies because they sell to buyers who make their own decisions, not for the
enumerated FCRA purposes. This functional gap allows data broker products to influence credit,
insurance, employment, and housing decisions without FCRA accountability. Pasquale's "black box
society" (2015) documents this accountability gap. Chouldechova (2017) and Hardt et al. (2016)
establish that algorithmic fairness criteria are mathematically incompatible -- a finding that
makes rulemaking on which criterion to apply necessary, not optional. Cross-reference:
CNSR-ALGO (existing algorithmic consumer decision positions); PRIV-DBKR-0004 (categorical
prohibition on data used as inputs).

---

#### PRIV-ALGO-0002 -- Mandatory Algorithmic Impact Assessments

**Rule-plain:**
Before deploying a computer system that makes or recommends decisions affecting people's lives,
companies and agencies must evaluate whether it discriminates or causes other harms. That
evaluation must be done by someone independent of the team that built the system.

**Rule-stmt:**
Prior to deploying any automated decision system in a covered use as defined in PRIV-ALGO-0001,
the deploying entity must complete and retain an algorithmic impact assessment (AIA) conducted
or reviewed by a qualified independent party not employed by the deploying entity. The AIA must
include: a description of the system's purpose, inputs, and decision outputs; an analysis of
the accuracy and error rates of the system on the population to which it will be applied;
a disparate impact analysis assessing whether the system produces materially different outcomes
for persons in protected classes under applicable civil rights law; an assessment of the data
sources used and any known limitations, biases, or gaps in those sources; and a statement of
the standards the deploying entity will use to evaluate ongoing system performance. AIAs must
be updated whenever the system is materially modified and must be provided to the FTC or CFPB
upon request. AIAs are not required to be publicly disclosed but must be retained for the life
of the system plus five years.

**Rule-notes:**
PLOS-AIGV-0004 requires pre-deployment assessment and ongoing monitoring for high-impact AI
systems. PLOS-AIGV-0005 requires third-party auditability. Selbst et al. (2019) identifies
"portability traps" -- the problem that a system fair in one context may be unfair when deployed
in another, making one-time fairness certification insufficient. The AIA requirement does not
resolve the mathematical fairness criterion problem identified by Chouldechova and Hardt --
it requires that entities choose and document a standard, creating accountability for that
choice rather than mandating a specific criterion. The independent review requirement follows
PLOS-KERN-0007 (risk level assessed by actor independent of system's proponent or operator).

---

#### PRIV-ALGO-0003 -- Adverse Action Notice and Explanation Rights

**Rule-plain:**
If a computer system recommended against you -- denied you insurance, a job, housing, or a
loan -- you have the right to know that a computer was involved, what data it used, and why
it reached that conclusion. You also have the right to challenge it.

**Rule-stmt:**
Any entity making an adverse decision in a covered use through or with material assistance of
an automated decision system must provide the affected individual with: (a) notice that an
automated system was a contributing factor in the adverse decision; (b) the specific data
categories and data sources used by the system in reaching its output; (c) the principal factors
in the system's output in plain language sufficient to allow the affected person to understand
the basis for the decision; and (d) information about how to dispute the accuracy of the data
used. Notice must be provided within 5 business days of the adverse decision. The FTC, in
consultation with the CFPB, must establish plain-language standards for adverse action notices.
An entity may not claim trade secret protection to avoid providing the category-level information
required under (b) and (c). The affected individual's right to dispute data accuracy extends
to all covered-use data as provided in PRIV-ALGO-0001.

**Rule-notes:**
The CFPB has extended adverse action notice requirements to algorithmic credit decisions under
existing FCRA authority (2022 CFPB circular). This rule codifies and extends that authority
across all covered uses. PLOS-KERN-0013 requires challenge, appeal, correction, pause, and
independent review mechanisms for every consequential decision system. PLOS-KERN-0010 requires
meaningful review: "adequate time to evaluate the decision and the full information the system
used; access to that information; and actual authority to override, modify, or reject the
automated recommendation." Trade secret carve-out for category-level data follows the same
logic as PRIV-SVPR-0005: the methodology may be confidential but the data categories and
principal factors cannot be. Cross-reference: PRIV-ENFA-0003 (private right of action).

---

#### PRIV-ALGO-0004 -- Prohibition on Protected Class Proxies

**Rule-plain:**
Companies may not use data that effectively predicts your race, gender, religion, or other
protected characteristic and then use that prediction to make decisions about you. Using a
stand-in for a protected class is the same as using the protected class itself.

**Rule-stmt:**
No entity using an automated decision system in a covered use may use any data input or model
feature that functions as a proxy for membership in a class protected under Title VII of the
Civil Rights Act, the Fair Housing Act, the Equal Credit Opportunity Act, the Americans with
Disabilities Act, or any other applicable federal anti-discrimination statute. A data feature
is a prohibited proxy if: (a) it is strongly correlated with protected class membership in the
population to which the system is applied, and (b) there is no independent non-discriminatory
justification for its use that is proportionate to its discriminatory effect. Zip code is not
categorically prohibited as a risk factor but requires affirmative justification where it
functions as a racial or ethnic proxy. Third-party behavioral scores or data broker products
whose predictive value is primarily derived from protected class membership are prohibited
inputs regardless of how they are labeled. Disparate impact claims arising from proxy use are
cognizable under the statutes enumerated above; proof that the system produces disparate
outcomes is sufficient to shift the burden of justification to the entity.

**Rule-notes:**
Angwin et al. (ProPublica 2016) and Dressel and Farid (2018) document that commercial risk
assessment tools (COMPAS) produce racially disparate outcomes consistent with proxy use.
The Obermeyer et al. (2019) study in Science demonstrated that a widely deployed healthcare
algorithm was calibrated to a cost proxy that embedded racial bias, demonstrating proxy
discrimination even in non-explicitly-protected domains. The Vanguard decision (9th Cir.) and
HUD disparate impact rule establish the disparate impact framework for housing and lending;
this rule codifies burden-shifting for algorithmic systems across all covered uses.
Cross-reference: PRIV-ALGO-0002 (AIA must include disparate impact analysis).

---

#### PRIV-ALGO-0005 -- Algorithmic Discrimination Private Right of Action

**Rule-plain:**
If a company's algorithm discriminated against you in a decision about your insurance, job,
housing, or loan -- and used data it shouldn't have or failed to tell you what it used -- you
can sue.

**Rule-stmt:**
Any individual who suffers an adverse decision in a covered use as defined in PRIV-ALGO-0001,
and who can establish that the decision was made using a system in violation of PRIV-ALGO-0001
through PRIV-ALGO-0004, may bring a civil action for: actual damages; statutory damages of not
less than $1,000 per violation where actual damages are not provable; equitable relief including
correction of adverse records, reconsideration of the adverse decision, and injunctive relief
against continued use of the noncompliant system; and attorney's fees and costs. Class actions
are available where common questions of law or fact apply to a class of persons subjected to
the same noncompliant system. This private right of action supplements and does not replace
enforcement rights under FCRA, ECOA, the Fair Housing Act, Title VII, or any other applicable
statute. State civil rights statutes providing greater protections are not preempted.

**Rule-notes:**
FCRA's existing private right of action (15 U.S.C. § 1681n, § 1681o) provides the model:
actual damages or statutory damages of $100-$1,000 per violation for negligent violations;
up to $1,000 for willful violations plus punitive damages. The extension of PRIV-ALGO's private
right of action to all covered uses, not just FCRA-covered uses, is necessary to prevent
the coverage gap identified in PRIV-ALGO-0001. Citron and Solove (2022) provide the doctrinal
framework for establishing algorithmic discrimination as a cognizable legal harm. The
non-preemption provision follows the pattern of Title VII (which does not preempt state
civil rights statutes providing greater protections).

---

### Family 6: PRIV-ENFA -- Enforcement Architecture

---

#### PRIV-ENFA-0001 -- FTC and CFPB Jurisdiction and Lane Assignments

**Rule-plain:**
The FTC is the main regulator for most companies under this pillar. The CFPB handles banks,
lenders, and insurance companies. Both agencies have clear authority to write rules and issue
fines -- not just negotiate settlements.

**Rule-stmt:**
The Federal Trade Commission has primary enforcement jurisdiction over all provisions of this
pillar with respect to entities that are not financial institutions, depository institutions,
credit unions, insurance companies, or mortgage servicers. The Consumer Financial Protection
Bureau has primary enforcement jurisdiction over the foregoing financial entities. Both agencies
have concurrent jurisdiction where an entity operates in both sectors. Both agencies are
explicitly authorized to promulgate binding rules implementing each family of this pillar
without requiring additional legislative authorization. Civil money penalties under this pillar
apply for first-time violations; neither agency is limited to injunctive relief for first
offenses. Civil penalties are to be calculated per violation, per consumer affected, or per
day of ongoing violation at the enforcing agency's discretion, subject to proportionality
standards established by agency rulemaking within 12 months of enactment.

**Rule-notes:**
The FTC Restoration Act (proposed, not enacted as of this writing) would have restored the
FTC's Section 13(b) restitution authority following AMG Capital Management, LLC v. FTC (2021).
This pillar's civil money penalty authority does not depend on Section 13(b) restoration --
it establishes independent statutory penalty authority. The "first offense civil penalty"
provision corrects the structural weakness in current FTC authority where injunctive-relief-only
first offenses create low-cost compliance failure incentives. Cross-reference: CNSR-CFPS-0001,
CNSR-CFPS-0004 (CFPB independence and funding baseline required for effective enforcement).

---

#### PRIV-ENFA-0002 -- State Attorney General Concurrent Authority

**Rule-plain:**
State attorneys general can also enforce these rules. Federal protection is the floor; states
can go further. This ensures enforcement does not depend entirely on a federal agency that
may be underfunded or politically pressured.

**Rule-stmt:**
The attorney general of any state may bring a civil action in federal or state court to enforce
any provision of this pillar on behalf of the residents of that state. State enforcement
authority is concurrent with and does not require authorization from the FTC or CFPB. Where
a state brings an enforcement action on a matter that is the subject of a pending federal
action, the agencies must coordinate to avoid duplicative remedies but state enforcement is not
stayed. States may enact and enforce privacy, data broker regulation, or algorithmic
accountability laws that provide greater protections than this pillar; this pillar establishes
a federal floor, not a ceiling. States may not enact laws that provide lesser protections on
the grounds that federal minimum standards have been established.

**Rule-notes:**
State AG concurrent enforcement has been effective in data security enforcement (the multi-state
data breach coalitions), consumer protection enforcement, and FCRA enforcement. The non-preemption
"floor not ceiling" provision is the most contested element in federal privacy legislation --
industry has consistently sought federal preemption of state privacy laws (including CCPA/CPRA)
as part of any federal privacy framework. This rule rejects that approach. CCPA/CPRA represents
the most comprehensive currently operative state framework; federal preemption of CCPA would
reduce, not increase, consumer protection in California. Schwartz (2019) identifies preemption
as one of the most significant risks in any federal privacy bill.

---

#### PRIV-ENFA-0003 -- Private Right of Action with Statutory Damages

**Rule-plain:**
You can take a data broker or surveillance company to court if they violate your data rights,
even without proving exactly how much money you lost. Minimum damages are set so it is worth
bringing a case.

**Rule-stmt:**
Any individual whose rights under any provision of this pillar have been violated may bring
a civil action against the violating entity. Statutory damages: not less than $100 nor more
than $1,000 per violation for negligent or unintentional violations; not less than $1,000 nor
more than $5,000 per violation for knowing or reckless violations; actual damages where greater
than statutory minimums. Punitive damages are available for willful violations. Class actions
are available where common questions of law or fact apply to a class of affected individuals.
Prevailing plaintiffs are entitled to reasonable attorney's fees and costs. Prevailing defendants
are not entitled to attorney's fees absent a finding that the action was frivolous. This private
right of action supplements pillar-specific private rights of action in PRIV-SVPR-0007 and
PRIV-ALGO-0005; the most specific applicable provision governs where specific damages schedules
differ.

**Rule-notes:**
Modeled on the FCRA private right of action (15 U.S.C. § 1681n, 1681o) and Illinois BIPA
(740 ILCS 14/20). The BIPA model has proven the most effective private enforcement mechanism
in U.S. privacy law: BIPA's $1,000-$5,000 per-scan statutory damages have generated billions
in settlements for biometric data violations, demonstrating that statutory damages produce
compliance incentives that actual-harm requirements cannot. The asymmetric attorney's fee
provision (plaintiff fees available; defendant fees only for frivolous cases) follows the
civil rights fee-shifting model and prevents fee deterrence of meritorious privacy actions.
Citron and Solove (2022) establish the doctrinal framework for privacy harms as legally
cognizable injuries satisfying standing requirements after TransUnion v. Ramirez (2021).

---

#### PRIV-ENFA-0004 -- Proactive Audit Mandate

**Rule-plain:**
Regulators must actively look for violations -- they cannot only respond to consumer complaints.
Because most violations of this pillar are invisible to consumers, waiting for complaints
means waiting for harms that will never be reported.

**Rule-stmt:**
The FTC and CFPB must each conduct not fewer than 25 proactive compliance audits per year of
entities covered by this pillar. Proactive audits may include: documentary demands for pricing
system, behavioral data use, and algorithmic decision system records; anonymous and pseudonymous
test transactions to detect personalized pricing or discriminatory automated decisions; review
of advertising transparency repository data for PRIV-ADTC-0004 compliance; and examination of
data broker registrations against market intelligence on operating entities. The FTC must
publish an annual public report describing the number of audits conducted, the categories of
violations identified, enforcement actions taken, and systemic patterns observed. Audit findings
must be shared with state attorneys general with concurrent enforcement authority. Entities
selected for audit must cooperate and may not withhold requested records on trade secret grounds
where the FTC has issued a Civil Investigative Demand.

**Rule-notes:**
PAOS-ENFC requirements specify that enforcement must include proactive monitoring, not just
complaint-driven response. The invisibility problem is structural: consumers cannot detect
personalized pricing, cannot read behavioral profiles compiled about them, and cannot observe
engagement optimization mechanisms operating in real time. Complaint-driven enforcement is
therefore structurally inadequate. The 25-audit-per-year floor is a minimum; FTC rulemaking
must establish an audit cadence proportionate to the market. PLOS-ENFA-0003 requires monitoring
"for fraud, concealment, recurring violations, and systemic abuse patterns rather than relying
only on complaint-driven detection." Cross-reference: PRIV-DBKR-0002 (registry data available
for audit targeting).

---

#### PRIV-ENFA-0005 -- Escalating Sanctions and Structural Remedies

**Rule-plain:**
Companies that keep violating these rules face escalating consequences -- not just fines that
they can write off as a cost of doing business. Serious or repeated violations can result in
being required to delete data assets or be barred from certain data practices.

**Rule-stmt:**
For first violations, the FTC or CFPB may impose civil money penalties under PRIV-ENFA-0001
and issue compliance orders specifying required corrective actions. For second violations within
a 5-year period, penalties are trebled and a structural remedy assessment is mandatory.
Structural remedies available to the enforcing agency include: mandatory deletion of specified
data assets and prohibition on reacquisition; prohibition on specific data collection, sale,
or use practices; divestiture of data broker subsidiaries or data management platforms where
the violation is integral to the subsidiary's operations; and operational restrictions on new
data product lines pending compliance certification. For patterns of violation affecting more
than 100,000 consumers, or for deliberate concealment of violations, the enforcing agency may
seek dissolution of the violating data broker entity as a last resort. Individual officers
and directors bear personal liability for violations committed with their knowledge or approval.

**Rule-notes:**
PLOS-ENFA-0004 requires "escalating intervention" including "structural remedies, suspension,
or removal of authority where proportionate." PLOS-ENFA-0005 extends liability to responsible
individuals "where deliberate misconduct, gross negligence, fraud, or failure of oversight is
established." The data-asset deletion remedy is the data sector equivalent of disgorgement of
ill-gotten profits in securities enforcement: it removes the economic benefit of the violation
(the data itself). The FTC has used data deletion as a remedy in a small number of cases
(Cambridge Analytica settlement, Everalbum settlement) establishing precedent; this rule codifies
and extends that authority. Cross-reference: PRIV-DBKR-0003 (centralized deletion mechanism
provides the infrastructure for remedial deletion orders).

---

#### PRIV-ENFA-0006 -- Whistleblower Protections

**Rule-plain:**
Employees and contractors who report violations of these rules are protected from being fired
or punished for reporting. This is how the public finds out about violations that are hidden
inside companies.

**Rule-stmt:**
No data broker, advertising platform, behavioral technology company, or other entity covered
by this pillar may retaliate against any employee, contractor, former employee, or agent who:
(a) reports a potential violation of any provision of this pillar to the FTC, CFPB, a state
attorney general, or any other law enforcement entity; (b) provides information or assistance
in any investigation or proceeding related to such a potential violation; or (c) refuses to
participate in activity they reasonably believe to be a violation of this pillar. Prohibited
retaliation includes termination, demotion, harassment, exclusion from business opportunities,
and breach of confidentiality claims asserted to prevent good-faith reporting. Whistleblowers
who provide original information leading to a successful enforcement action resulting in
penalties exceeding $1,000,000 are entitled to between 10% and 30% of the penalties collected.
Non-disclosure agreements and confidentiality provisions in employment contracts may not be
used to prevent reporting to regulatory authorities.

**Rule-notes:**
PLOS-KERN-0027 requires whistleblower protections "available regardless of employment status
and may not be waived by contract." The whistleblower bounty provision follows the SEC
whistleblower program (Dodd-Frank Section 922), which has been the most effective U.S. financial
enforcement mechanism: the SEC collected $6.5 billion in enforcement actions involving
whistleblower information between 2012 and 2023. Data broker operations are opaque to external
regulators; insider information is the most reliable source of evidence for systemic violations.
The NDA carve-out is necessary because data companies routinely require employees to sign broad
confidentiality agreements that purport to cover disclosure of company practices to regulators --
a practice that, if enforceable, would eliminate the practical effect of whistleblower protections.

---

## PolicyOS Compliance Summary

### Values implicated
| Value | How addressed |
|-------|---------------|
| Value 1 (Human Dignity) | Categorical prohibition treats persons as rights-holders, not data points |
| Value 2 (Equal Standing) | Algorithmic discrimination family; distributional harm named in SVPR; proxy prohibition |
| Value 3 (Real Liberty) | Behavioral modification prohibition; consent fiction rejection; surveillance pricing ban |
| Value 5 (Accountable Power) | Enforcement architecture; proactive audits; individual officer liability |
| Value 6 (Transparency) | Adverse action notice; pricing transparency; RTB data minimization |
| Value 10 (Enforceable Fairness) | FCRA extension; disparate impact burden-shifting; private right of action |
| Value 11 (Durability against capture) | State AG concurrent authority; floor not ceiling; FTC capture prevention |

### KERN rules applied
KERN-0008 (no hidden rules/trade secret shields), KERN-0012 (anti-bias), KERN-0013 (challenge
and appeal), KERN-0015 (prevent foreseeable abuse), KERN-0016 (no deprivation/coercion as
compliance mechanism), KERN-0017 (no extraction incentives), KERN-0022 (adapt to technological
change), KERN-0027 (whistleblower protections).

### Overlays applied
PRIV, ECON, ENFA, AIGV (for algorithmic systems), REGD (for regulatory design).

### Value tensions documented (PAOS-NORM-0008)
1. **Industry's Varian (1985) counter-argument on price discrimination welfare:** Addressed in
   PRIV-SVPR-0004 (permitted practices) and rule-notes throughout. Position: the theoretical
   welfare ambiguity applies to third-degree market segmentation; first-degree behavioral
   extraction is categorically different and the empirical evidence (Shiller 2020) supports the
   ban.
2. **Social media mental health causation contested:** Addressed in PRIV-BMOD-0002 and 0004
   rule-notes. Position: the behavioral autonomy and developmental consent grounds are
   independently sufficient; contested mental health evidence is not cited.
3. **RTB reform vs. advertising market welfare (Goldfarb and Tucker 2011):** Addressed in
   PRIV-ADTC-0002 rule-notes. Position: contextual advertising safe harbor preserves viable
   advertising markets; only behavioral targeting of prohibited categories is restricted.
4. **Consent architecture vs. individual autonomy (Solove consent dilemma):** Addressed in
   baseline architecture. Position: data minimization and categorical prohibition resolve the
   consent dilemma by removing the categories most likely to produce harm from the consent
   framework entirely.

---

## Adversarial Review (PAOS-TEST-0008)

### Gaps
- PRIV-DBKR-0004 list of prohibited categories will require updating as new data types emerge
  (AI-inferred emotion, biometric from video, continuous biometric monitoring). The FTC
  rulemaking authority in 0004 addresses this without requiring legislative revision.
- The pillar does not address offline data collection (paper records, in-store tracking without
  digital component). This is a deliberate scope limitation, not a gap -- offline data broker
  activity is substantially smaller and different enough in mechanism to warrant separate treatment.

### Loopholes
- **First-party exemption for SVPR:** Closed in PRIV-SVPR-0002 by applying the prohibition to
  first-party profile use. A retailer cannot escape the prohibition by building its own
  willingness-to-pay model rather than buying one.
- **Data broker reclassification:** Entities may claim to be "analytics firms" or "marketing
  partners" rather than data brokers. Addressed in PRIV-DBKR-0001 with a functional definition.
- **Consent workaround via ToS:** Explicitly closed in the baseline architecture and
  PRIV-DBKR-0004.
- **Contextual advertising as cover for behavioral targeting:** Addressed in PRIV-ADTC-0005
  (contextual safe harbor does not cover proxy-for-prohibited-category targeting).

### Abuse paths
- **Industry capture of the FTC rulemaking process:** Addressed via PRIV-ENFA-0002 (state AG
  concurrent authority not dependent on federal regulatory posture) and PRIV-ENFA-0003
  (private right of action independent of agency action).
- **Federal preemption of state law:** Explicitly rejected in PRIV-ENFA-0002.
- **Trade secret shields over pricing and algorithmic systems:** Directly foreclosed in
  PRIV-SVPR-0005 and PRIV-ALGO-0003.

### Unintended consequences
- **Advertising market disruption:** Contextual advertising safe harbor (PRIV-ADTC-0005) and
  narrow scope of behavioral targeting prohibition (sensitive categories and minors only, not
  all behavioral advertising) limit market disruption.
- **Small data broker compliance burden:** Registration and deletion mechanism requirements
  may have disproportionate compliance costs for small brokers. The FTC must account for this
  in fee-setting and rulemaking.

---

## Implementation Notes

**New pillar page:** `docs/pillars/data-rights-and-privacy.html`
**Suggested pillar color:** `#2a4a6b` (deep navy, consistent with civil liberties/rights palette)
**Foundation assignment:** Freedom to be confirmed in `docs/assets/js/data.js`
**DB entries required:**
- New domain: `PRIV` (Data Rights and Privacy)
- New subdomains: DBKR, ADTC, BMOD, SVPR, ALGO, ENFA
- 34 new positions: PRIV-DBKR-0001 through 0006, PRIV-ADTC-0001 through 0005,
  PRIV-BMOD-0001 through 0005, PRIV-SVPR-0001 through 0007, PRIV-ALGO-0001 through 0005,
  PRIV-ENFA-0001 through 0006 (all status: PROPOSED)

**Cross-references to add:**
- CNSR-ALGO family: add reference to PRIV-ALGO (extension of FCRA)
- CNSR-CFPS-0001, CFPS-0004: referenced as enforcement infrastructure dependency
- Tech/AI pillar: PRIV-ADTC and PRIV-BMOD cross-reference for algorithmic targeting
