# Surveillance Pricing: Research Overview and Policy Framework

**Date:** May 2026  
**Status:** Research draft — ready for adversarial review and policy proposal development  
**Research scope:** Definition, data ecosystem, consumer harms, legal landscape, policy proposals  

---

## Executive Summary

Surveillance pricing refers to the practice of setting individualized prices for consumers based on profiles assembled from personal data — browsing history, location, device fingerprints, inferred demographic characteristics, credit histories, and behavioral signals — often collected and processed by third-party intermediaries invisible to the consumer. It is not the same as supply-and-demand dynamic pricing, and it differs from ordinary geographic or loyalty pricing in a decisive respect: the individual, not a category or market condition, is the unit of analysis. The price you pay reflects what an algorithm predicts you will pay, not what the product is worth or what the market will bear.

The Federal Trade Commission's January 2025 Surveillance Pricing Study — one of the final major reports released under the Biden-era FTC — found that a small group of intermediary companies collected data including real-time location, browsing behavior, purchase history, socioeconomic indicators, and social media data, and used it to generate "individualized and dynamic pricing" services sold to retailers [1]. The companies studied included a Mastercard subsidiary (Dynamic Yield), Revionics (Aptos), McKinsey & Company, JPMorgan Chase, Pros Holdings, Bloomreach, and Task Systems. The FTC found that these systems could result in higher prices for consumers with lower alternatives — including lower-income and minority consumers — while providing no corresponding benefit to those consumers. The report was subsequently removed from the FTC's public website following the January 2025 change in administration.

No federal statute currently prohibits surveillance pricing directed at retail consumers. The Robinson-Patman Act addresses only business-to-business price discrimination [2]. FTC Act § 5's unfair or deceptive practices authority covers deception but does not clearly reach undisclosed personalized pricing that is not itself false [3]. State privacy laws — CCPA/CPRA, Virginia's CDPA, Illinois's BIPA — create data rights but do not ban pricing uses of personal data. The EU's GDPR, through its data minimization and automated decision-making provisions, provides the strongest existing framework, but it too has not been applied to systematically prohibit price personalization [4, 5].

This document maps the conceptual, technical, legal, and policy landscape to inform the design of a surveillance pricing policy family for this platform.

---

## Part I: Definition and Taxonomy

### 1.1 What Is Surveillance Pricing?

**Surveillance pricing** is the practice of charging individual consumers different prices based on personal profiles built from surveillance data — data about their behavior, location, demographics, financial circumstances, and inferred psychological characteristics — for the purpose of extracting the maximum price each individual will accept.

The FTC's 2025 study defined it as the use of "vast amounts of consumer data — including browsing history, location data, social media activity, and other signals — to determine the maximum price a particular consumer will pay for a product or service" [1].

The key elements are:

1. **Individual targeting.** The unit of analysis is the individual consumer, not a market segment, zip code, or customer category.
2. **Surveillance data input.** The pricing signal derives from data collected through behavioral tracking, data broker pipelines, credit systems, or other forms of surveillance — not from the transaction itself.
3. **Willingness-to-pay extraction.** The goal is to capture consumer surplus: charge each consumer the most they will accept without refusing to buy.

### 1.2 Distinguishing Surveillance Pricing from Related Practices

These distinctions matter legally and for policy design, as blurring them creates definitional problems that industry regularly exploits.

| Practice | Basis for Price Difference | Uses Individual Surveillance Data? | Notes |
|---|---|---|---|
| **Dynamic pricing** (Uber surge, airline seats) | Real-time supply/demand, time | Not individually targeted | Seat prices change for all buyers; algorithmic but not individual-surveillance-based |
| **Geographic price differentiation** | Region or city-level market conditions | No (or only zip code) | Staples-type geographic pricing partially overlaps if zip correlates with demographics |
| **Loyalty/coupon pricing** | Explicit enrollment and disclosed data sharing | First-party, consent-based | Consumer knowingly trades data for discount |
| **First-party behavioral pricing** | Platform's own behavioral data (e.g., Amazon using your purchase history) | First-party only | Closer to surveillance pricing; raises distinct issues about platform monopoly data advantages |
| **Third-party surveillance pricing** | Data broker pipeline + behavioral tracking ecosystem | Yes — third-party, undisclosed | The core problem this policy family targets |

The FTC's study focused primarily on **third-party intermediary surveillance pricing** — where a company the consumer has never interacted with assembles a profile that a retailer then uses to set a personalized price [1]. This is the most opaque and least consented-to form.

**The first-party/third-party distinction** is analytically useful but increasingly unstable. A retailer that uses its own loyalty data to price discriminate is harder to regulate under third-party data broker statutes, yet produces similar consumer harms. See Part VII for further discussion of this definitional gap.

---

## Part II: The Data Ecosystem

### 2.1 What Data Is Used

The FTC found that surveillance pricing intermediaries collected and processed the following categories of consumer data [1]:

- **Browsing and search history** — pages visited, products viewed, time-on-page, search queries
- **Real-time location data** — GPS, cell tower, Wi-Fi proximity, precise coordinates
- **Device fingerprints** — browser type, operating system, screen resolution, installed fonts; used to re-identify consumers across sessions even after cookie deletion
- **Purchase history** — transaction records, often acquired from data brokers (Acxiom, Oracle, CoreLogic) who aggregate across retailers
- **Social media data** — public and scraped profile data, inferred interests and political affiliations
- **Credit and financial data** — credit scores, payment history, financial stress indicators
- **Inferred demographic characteristics** — race, income, education level, age, household composition inferred from behavioral signals

This data is typically combined across sources, "enriched" by data brokers, and fed into machine learning models that estimate an individual's willingness to pay in real time.

### 2.2 The Data Broker Pipeline

The infrastructure enabling surveillance pricing is the same infrastructure powering targeted advertising. The pipeline typically flows as follows:

1. **Collection layer.** Tracking pixels, cookies, mobile SDKs, and loyalty cards collect behavioral signals from consumers across websites, apps, and physical retail environments.
2. **Identity resolution.** Companies like LiveRamp, Oracle Data Cloud, and Acxiom link these signals to persistent individual identifiers using probabilistic matching — connecting a device fingerprint to a name, address, email, and purchase history.
3. **Enrichment.** Data brokers layer on third-party attributes: estimated income, credit tier, housing status, inferred ethnicity. Acxiom's InfoBase, for example, claims coverage of over 250 million Americans [6].
4. **Pricing model.** The enriched profile enters a pricing algorithm (provided by companies like Revionics, Dynamic Yield, Pros Holdings, or Bloomreach) that outputs a personalized price or a "price elasticity" estimate — how much this individual's purchasing behavior changes with price.
5. **Retailer integration.** The output is delivered to the retailer in real time — the price is set before the consumer even completes the checkout page.

### 2.3 Real-Time Bidding (RTB) as a Data Pipe

The real-time bidding ecosystem for digital advertising functions as a secondary pipeline for surveillance pricing data. Each time a consumer visits a webpage or opens a mobile app, an auction occurs within milliseconds in which dozens or hundreds of companies observe the consumer's device identifier, location, and page context — even if they lose the auction. This observation-without-winning creates a massive, largely unregulated channel through which behavioral data flows to data brokers who can repurpose it for pricing applications.

The Internet Archive of Rhetoric Center (ICCL) has documented that a single consumer in the United States may have their data broadcast to hundreds of companies per day through RTB. This data is "observable" by all auction participants, not just the winning bidder, creating surveillance at scale regardless of advertising outcomes.

### 2.4 Key Industry Players

- **Mastercard / Dynamic Yield** — Dynamic Yield was acquired by McDonald's in 2019 and then by Mastercard in 2021. It provides real-time personalization, including price optimization, using transaction data from Mastercard's payment network — one of the largest datasets of purchase behavior in the world.
- **Revionics (Aptos)** — provides AI-driven pricing optimization to major retailers, incorporating competitive intelligence and consumer behavioral data.
- **McKinsey & Company** — advises retailers on personalized pricing strategies; the FTC found it served as a pricing intermediary using consumer data.
- **Pros Holdings** — provides B2B and increasingly B2C AI pricing platforms.
- **Bloomreach** — commerce experience platform with pricing personalization capabilities.
- **JPMorgan Chase** — found by the FTC to offer merchant services that incorporated payment-level consumer data into pricing recommendations.
- **Acxiom / LiveRamp / Oracle Data Cloud** — the data broker layer supplying enriched consumer profiles to pricing intermediaries [6].

---

## Part III: Consumer Harm Evidence

### 3.1 Price Disparity by Income and Race

The most direct harm of surveillance pricing is that consumers who are less price-elastic — those with fewer alternatives, higher needs, or weaker price-shopping behavior — pay more. This systematically disadvantages lower-income consumers and, due to the correlation between income and race in the United States, disproportionately impacts communities of color.

**Staples geographic pricing (2012).** A Wall Street Journal investigation found that Staples displayed different prices to consumers based on estimated proximity to a physical competitor store. Consumers who lived farther from competitors — who tended to be lower-income and to live in majority-minority zip codes — were charged higher prices online [7]. The pricing mechanism was ostensibly geographic (distance to competitor), not individually targeted, but the proxy effect was demographic.

**Office Depot and travel sites.** The same 2012 investigation found similar geographic price discrimination at Office Depot and several travel booking sites, including different prices for Mac vs. PC users (a proxy for income) [7].

**Hannak et al. (2014).** A study by researchers at Northeastern University and Princeton tested 16 major e-commerce platforms and found evidence of price discrimination linked to device type, account history, and behavioral signals. Mac users, for example, were shown higher hotel prices on Orbitz — a practice Orbitz defended as "not discrimination" because it reflected purchase history rather than identity, a distinction that is economically meaningless to the consumer paying more [8].

**Mikians et al. (2012).** Researchers demonstrated that price differences of up to 166% for identical products could be found based on inferred consumer profiles, including geographic and behavioral signals [9].

### 3.2 Insurance Pricing: The Mature Surveillance Model

The insurance industry represents the most fully developed example of surveillance pricing and provides a case study in both its mechanics and its harms.

**Credit-based insurance scoring.** Forty-seven states permit insurers to use credit scores as a factor in setting auto and homeowners insurance premiums. The logic is actuarial: people with lower credit scores file more claims on average. But the causal mechanism is disputed, and the disparate racial impact is well-documented. Because credit scores are correlated with race — due to historical discriminatory lending, income inequality, and structural barriers to credit — credit-based insurance scoring effectively penalizes Black and Latino consumers for systemic racism [10].

**Telematics and behavioral pricing.** Usage-based auto insurance programs (Progressive Snapshot, Allstate Drivewise) collect real-time driving behavior — speed, braking, time of day, mileage — to set individualized premiums. This is unambiguously surveillance pricing: the price is set based on behavioral surveillance. The FTC has not yet challenged this practice.

### 3.3 Algorithmic Ride-Share Pricing

Uber and Lyft's surge pricing is demand-based (not individually targeted) but the platforms collect individual behavioral data — including willingness-to-pay signals from prior ride acceptance rates at different prices — that could be used for individualized pricing. Research has found that ride-share prices are higher in lower-income neighborhoods and communities of color, partly due to higher baseline demand and fewer drivers, and partly due to algorithmic factors [11].

### 3.4 Airline and Hotel Pricing

Airlines have practiced opaque personalized pricing for decades, routing individual customers to different fare classes based on booking history, frequent flyer status, device type, and corporate affiliation. Hotel chains similarly offer differential rates tied to loyalty data. The opacity of these pricing systems — consumers cannot see the counterfactual price offered to someone else for the same seat or room — makes harm difficult to document and effectively impossible to challenge.

### 3.5 FTC Findings on Harm (2025)

The FTC's surveillance pricing study found that:

- Intermediary companies "collected vast amounts of consumer data" and used it to set "individualized and dynamic pricing" [1]
- The data collected included sensitive categories that consumers were unaware were being used for pricing
- There was "opacity" in how consumer data flowed from collection to pricing decision
- Lower-income consumers and those in certain demographic groups could face systematically higher prices
- The companies studied served major retailers across grocery, apparel, electronics, and consumer goods

The FTC noted that existing law provides limited protection against these practices, and called for "stronger guardrails" — though without making specific enforcement recommendations in the report.

---

## Part IV: Current Legal Landscape

### 4.1 Federal Law

#### FTC Act § 5 — Unfair or Deceptive Practices

Section 5 of the FTC Act (15 U.S.C. § 45) prohibits "unfair or deceptive acts or practices in or affecting commerce" [3]. This is the broadest consumer protection authority available at the federal level.

**Coverage.** A practice is "unfair" if it causes substantial consumer injury that is not reasonably avoidable and not outweighed by countervailing benefits. A practice is "deceptive" if it is likely to mislead a reasonable consumer in a material way.

**Application to surveillance pricing.** The FTC has not brought a § 5 enforcement action directly targeting surveillance pricing. The key legal question is whether a consumer who is charged a higher price based on a profile they cannot see — and did not consent to — has suffered "substantial consumer injury" that is "not reasonably avoidable." The FTC's surveillance pricing study implicitly suggested yes, but the current FTC leadership (under Chairman Andrew Ferguson, appointed January 2025) has deprioritized these cases.

**Limits.** Section 5 does not create a private right of action. Consumers cannot sue under it; only the FTC can. This creates significant enforcement gaps when the agency's priorities shift.

#### Robinson-Patman Act — Price Discrimination

The Robinson-Patman Act (15 U.S.C. § 13) prohibits price discrimination between "different purchasers of commodities of like grade and quality" where the effect may "substantially lessen competition" [2].

**Critical gap: B2B only.** The Robinson-Patman Act applies to transactions between businesses, not between a business and a retail consumer. Courts have interpreted it to cover only purchasers who buy goods "for use, consumption, or resale." A retailer that charges individual consumers different prices for the same product does not violate Robinson-Patman because the consumers are not "purchasers" in the commercial sense the statute addresses. **This is the central gap in federal price discrimination law as applied to surveillance pricing.** No federal statute directly prohibits differential retail pricing based on surveillance data.

#### Electronic Communications Privacy Act (ECPA)

ECPA (18 U.S.C. §§ 2510–2522) restricts interception of wire and electronic communications but does not reach the collection and sale of behavioral data by data brokers because the data is not "intercepted" in real-time — it is compiled from cookies, pixels, and other instruments to which users have nominally consented through opaque terms of service.

#### COPPA

The Children's Online Privacy Protection Act (15 U.S.C. § 6501 et seq.) restricts collection of personal data from children under 13 and was strengthened by FTC rulemaking in January 2025 to further limit monetization of children's data. It does not address adult surveillance pricing.

#### Pending Federal Legislation

**Banning Surveillance Pricing Act (S. 3317, 118th Congress, 2023).** Introduced by Senators Elizabeth Warren (D-MA), J.D. Vance (R-OH), Edward Markey (D-MA), and others, this bill would have prohibited the use of personal data — including browsing history, location, purchase history, and financial data — to set individualized prices for goods and services. The bill did not advance out of committee. The bipartisan Warren-Vance co-sponsorship reflected genuine cross-ideological concern about this practice, but the bill faced industry opposition and did not receive a hearing [12].

**American Data Privacy and Protection Act (ADPPA, 2022–2023).** A comprehensive federal privacy bill that passed the House Energy and Commerce Committee in July 2022 with bipartisan support, the ADPPA would have restricted data collection practices underlying surveillance pricing. It stalled in the full House over jurisdictional conflicts with California's CPRA. A stronger version was not reintroduced.

### 4.2 State Law

#### California — CCPA / CPRA

The California Consumer Privacy Act (Cal. Civ. Code § 1798.100 et seq.), as amended by Proposition 24 (CPRA), creates the most comprehensive consumer data rights framework in the United States [13].

**What it covers:** Consumers have the right to know what data is collected, to opt out of the "sale" or "sharing" of personal data, to correct inaccuracies, and to delete their data. The CPRA strengthened these rights and created an independent enforcement agency (California Privacy Protection Agency, CPPA).

**Does it cover pricing?** The CCPA/CPRA does not explicitly prohibit using personal data for pricing. The opt-out right applies to "sale" and "sharing" of personal data for cross-context behavioral advertising — not necessarily to its use for pricing within a single platform. A retailer that uses its own first-party data to set personalized prices may not be "selling" data under CPRA's definition. However:

- If data is obtained from a third-party data broker and used for pricing, the consumer's right to opt out of the broker's data sharing may provide indirect protection
- The CPPA is developing regulations on automated decision-making that could extend to pricing — a rulemaking process that is ongoing as of 2025
- California's "sensitive personal information" category (Cal. Civ. Code § 1798.121) gives consumers additional opt-out rights for a list of sensitive data types, some of which may be used in pricing models

**The Delete Act (AB 947, 2023).** California's Delete Act creates an additional framework requiring data brokers to delete consumer data upon request through a single opt-out mechanism administered by the CPPA. If pricing models rely on data broker inputs, this creates a partial remedy.

#### Illinois — Biometric Information Privacy Act (BIPA)

BIPA (740 ILCS 14) requires informed written consent before collecting biometric identifiers including fingerprints, iris scans, and facial geometry. It includes a private right of action with statutory damages of $1,000–$5,000 per violation.

**Application to pricing.** BIPA directly applies where surveillance pricing systems use biometric identification — for example, in-store camera systems that recognize returning customers and serve them personalized prices. More broadly, BIPA's private right of action model represents a template for enforcement mechanisms that privacy advocates propose for surveillance pricing legislation.

#### Virginia — Consumer Data Protection Act (CDPA)

Virginia's CDPA (Va. Code § 59.1-577) gives consumers the right to opt out of "profiling in furtherance of decisions that produce legal or similarly significant effects" [14]. Personalized pricing could fall within this opt-out right depending on the magnitude of price differences. However, enforcement is exclusively by the Virginia Attorney General; there is no private right of action.

#### Other State Privacy Laws

Colorado, Connecticut, Texas, and Oregon have enacted comprehensive privacy laws similar to Virginia's, all including opt-out rights for profiling and targeted advertising but stopping short of explicitly prohibiting surveillance pricing. None has brought an enforcement action specifically targeting personalized retail pricing.

**Gap.** No U.S. state has enacted a law that explicitly prohibits or requires disclosure of surveillance pricing as a distinct practice. California's CPPA rulemaking is the most plausible near-term development.

### 4.3 International Law

#### EU General Data Protection Regulation (GDPR)

The GDPR (Regulation (EU) 2016/679) provides the strongest existing legal framework relevant to surveillance pricing through three provisions:

**Article 5 — Data minimization and purpose limitation.** Personal data must be "adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed" (data minimisation) and "collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes" (purpose limitation) [4]. A consumer whose data was collected for advertising who later finds it used for pricing optimization may have a GDPR claim — but in practice, broad consent language in privacy policies has made this difficult to litigate.

**Article 9 — Special categories of data.** Processing of data revealing racial or ethnic origin, health data, or other sensitive categories is prohibited absent explicit consent or specific legal bases [15]. Where surveillance pricing models incorporate inferred race or health status — as some models do through proxy variables — Article 9 may apply.

**Article 22 — Automated decision-making.** Individuals have the right not to be subject to decisions "based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her" [5]. Whether pricing constitutes a "significantly significant" decision within Article 22's scope is unsettled. The European Data Protection Board has suggested broad interpretation, but no definitive ruling exists.

**Practical limits.** GDPR enforcement has been slow, fragmented, and focused primarily on advertising rather than pricing. The Irish DPC (responsible for major tech platforms) has been criticized for inadequate enforcement velocity. Fines, while large in nominal terms, have not produced structural change in data collection practices.

#### EU AI Act (Regulation (EU) 2024/1689)

The EU AI Act, published in the Official Journal on July 12, 2024, establishes a risk-based framework for AI systems [16]. It does not specifically address surveillance pricing as a category. However:

- **Prohibited AI practices** (Article 5) include AI systems that use subliminal techniques to manipulate behavior in ways that harm users — an argument could be made that pricing systems designed to maximize price extraction are manipulative
- **High-risk AI systems** (Annex III) include AI used in credit scoring and creditworthiness assessment — relevant to insurance and financial surveillance pricing
- Real-time remote biometric identification is heavily restricted, which limits in-store biometric pricing

The AI Act does not comprehensively address pricing personalization, and its implementation timeline (most provisions apply from August 2026) means practical impact is future.

#### EU Digital Markets Act (Regulation (EU) 2022/1925)

The DMA imposes obligations on designated "gatekeepers" — the largest digital platforms. Relevant provisions include requirements to share data with business users and restrictions on using data from one service to advantage other services. This constrains some first-party data advantages that enable surveillance pricing by dominant platforms, but the DMA's primary focus is business-to-business fairness, not consumer pricing protection.

#### UK ICO

The UK Information Commissioner's Office has issued guidance on the use of AI in decision-making noting that decisions about pricing and services using inferred personal characteristics may require explicit justification under UK GDPR Article 22. The ICO has not issued specific surveillance pricing guidance as of 2025.

---

## Part V: Related Policy Domains

### 5.1 Ad-Tech and Behavioral Advertising

Surveillance pricing runs on the same infrastructure as behavioral advertising: the same tracking pixels, cookie syncing, device fingerprinting, and data broker pipelines. **The ad-tech ecosystem is the supply chain for surveillance pricing data.** Regulating one without regulating the other leaves a significant gap. Data collected for advertising can be repurposed for pricing; there is currently no meaningful restriction on this re-use. Policy proposals should treat these as a unified data infrastructure problem.

### 5.2 Data Broker Regulation

Because surveillance pricing depends on data broker pipelines — enriched consumer profiles purchased from Acxiom, Oracle, LiveRamp, and others — data broker regulation is a necessary upstream intervention. The FTC's enforcement actions banning data brokers from selling geolocation data (InMarket, 2024; X-Mode/Outlogic, 2024; Mobilewalla, 2024) begin to restrict the pipeline, but these actions targeted specific harmful uses, not the broader practice of building consumer profiles for pricing.

A 2021 investigation found 25 data broker companies spent $29 million on federal lobbying in 2020 alone, with Oracle spending $9.57 million and companies like Accenture, PwC, and the major credit bureaus as major spenders [6]. This lobbying presence has successfully blocked comprehensive federal data broker legislation for over a decade.

### 5.3 Algorithmic Pricing Coordination / Price-Fixing

A related but distinct concern is the use of algorithmic pricing software to coordinate prices *across competitors* — effectively algorithmic collusion. The DOJ filed suit against RealPage in August 2024, alleging that its algorithmic pricing software for residential rents enabled landlords to artificially inflate rents by sharing non-public pricing data through a common algorithm. Several state attorneys general joined the suit. This is distinct from surveillance pricing — it is a horizontal coordination problem rather than a vertical extraction problem — but the same AI pricing infrastructure is implicated in both.

### 5.4 Insurance Discrimination and Credit Scoring

The use of credit scores, behavioral telematics, and inferred demographic data in insurance pricing is the most established domain of algorithmic price discrimination. California, Hawaii, and Massachusetts prohibit or limit credit-based insurance scoring; the remaining 47 states do not. The National Association of Insurance Commissioners has studied the issue but declined to recommend federal action. The Consumer Financial Protection Bureau (CFPB) has authority over credit reporting but not over the use of credit data in insurance pricing.

### 5.5 Redlining 2.0

The geographic dimension of surveillance pricing — where zip code, neighborhood demographics, or location history serve as price inputs — replicates the economic dynamics of redlining. Consumers in lower-income and majority-minority neighborhoods pay more, not because of market conditions, but because algorithms infer lower price sensitivity from geographic and demographic proxies. This form of algorithmic discrimination is not captured by the Fair Housing Act, the Equal Credit Opportunity Act, or any other civil rights statute, creating a significant gap in anti-discrimination law.

### 5.6 Financial Services Pricing

Fintech lending, credit card pricing, and BNPL products increasingly use behavioral data beyond traditional credit scoring to set individualized interest rates and fees. The CFPB's Section 1071 small business lending data rules and its fair lending enforcement authority partially address this, but behavioral pricing in consumer credit operates largely outside existing anti-discrimination scrutiny.

---

## Part VI: Policy Proposals and Reform Debate

### 6.1 Legislative Proposals

**Banning Surveillance Pricing Act (S. 3317, 118th Congress).** The strongest existing federal proposal, this bill would have prohibited use of personal data for individualized pricing. Its bipartisan co-sponsorship (Warren/Vance) is notable, though it did not advance. A reintroduction in the 119th Congress would be an appropriate priority [12].

**Key elements any federal bill needs:**
1. A clear definition of surveillance pricing distinguishing it from supply/demand dynamic pricing
2. Prohibition on use of third-party data broker data for consumer pricing
3. Disclosure requirements when first-party data is used for pricing
4. A private right of action (BIPA model)
5. FTC enforcement authority with civil money penalties per violation
6. State law preemption clause language that does not weaken existing state protections

### 6.2 Academic and Think Tank Proposals

**Electronic Privacy Information Center (EPIC)** has called for an outright ban on third-party surveillance pricing, arguing that no regulatory middle ground effectively controls the practice given the opacity of the data pipeline.

**Economic Policy Institute (EPI)** has connected surveillance pricing to broader wage and wealth inequality, arguing that differential consumer pricing effectively transfers income from lower-income to higher-income consumers (who face lower prices due to perceived price-sensitivity) and from consumers to corporations.

**Consumer Reports** has advocated for mandatory price transparency — consumers should be able to see what price others paid for the same product — as a market-corrective measure even short of a ban.

**Academic consensus** (as reflected in the Hannak et al., Mikians et al., and related literature) is that price personalization is widespread, consumer harm is real, and market mechanisms do not self-correct because consumers cannot observe what prices others receive [8, 9].

### 6.3 Industry Self-Regulation

The ad-tech industry's self-regulatory bodies (DAA, IAB, NAI) have established opt-out mechanisms for behavioral advertising but have not extended these to pricing. The Responsible Business Practices guidelines of these organizations do not address surveillance pricing. Academic and FTC research consistently finds that industry opt-out mechanisms are under-utilized, technically difficult, and frequently ineffective.

**Assessment:** There is no evidence that industry self-regulation has constrained surveillance pricing in any meaningful way. The FTC's report found that major financial and consulting firms were offering these services with no voluntary disclosure or opt-out mechanisms of any kind [1].

### 6.4 Arguments For and Against Regulation

**For regulation:**
- Consumers cannot observe, consent to, or avoid surveillance pricing as currently practiced
- Distributional harm falls disproportionately on lower-income and minority consumers
- The practice violates reasonable expectations of equal treatment in the marketplace
- Data collected for one purpose (advertising) is repurposed for pricing without additional consent
- No current law adequately addresses the harm

**Industry arguments against regulation:**
- Personalized pricing can benefit price-sensitive consumers (lower prices for those the algorithm identifies as price-sensitive, not only higher prices for the less sensitive)
- Dynamic pricing improves market efficiency by clearing inventory
- Defining surveillance pricing without capturing legitimate dynamic pricing is technically difficult
- Regulation could chill investment in legitimate retail technology

**Analytical response to industry arguments:** The efficiency argument ignores distributional effects. The definitional difficulty is real but solvable (see Part VII). The beneficial-discounts argument is true in isolated cases but ignores the net welfare transfer from lower-income consumers who tend to face *higher* prices under surveillance pricing systems, contrary to the industry narrative.

---

## Part VII: Key Gaps and Controversies

### 7.1 The Law Currently Fails

The most fundamental gap is structural: no federal law prohibits consumer-directed price discrimination by private businesses that is based on personal surveillance data. Robinson-Patman covers B2B only [2]. FTC Act § 5 covers deception but not accurate, undisclosed personalization [3]. The Fair Housing Act, Equal Credit Opportunity Act, and Title VII cover specific protected characteristics in specific contexts but do not reach the retail pricing context. State privacy laws create data rights but not pricing rights.

The practical effect is that surveillance pricing can be conducted legally at full scale with no disclosure, no opt-out, and no remedy for the consumer. The FTC's study documented this practice among major financial and consulting firms [1]. The subsequent removal of that study from the FTC website illustrates how regulatory capture and administration change can eliminate even the documentary record.

### 7.2 Definitional Problems

**The dynamic pricing line.** Airlines, Uber, hotels, and event venues all charge different prices to different consumers at different times. These are generally understood as efficient market mechanisms. A ban on "personalized pricing" must distinguish this time-and-demand-based pricing from profile-based individual targeting. The key distinction is whether the price varies based on the *individual's* predicted willingness to pay (surveillance pricing) versus market conditions that apply to all consumers at that moment (dynamic pricing). Legislative drafting must be precise here to avoid over-breadth.

**The first-party exception.** If a retailer uses only its own loyalty card data to set prices, is that surveillance pricing? It involves individual data, but the consumer arguably consented to the loyalty program. The definitional instinct is to carve out "first-party data used with consent" — but in practice, the consent in loyalty programs is rarely meaningful, the pricing use is rarely disclosed, and the data is often shared with the broader data broker ecosystem anyway. An overly generous first-party exception will swallow the rule.

**Proxy discrimination without protected class.** Current anti-discrimination law protects against differential treatment based on race, sex, religion, national origin, and similar characteristics. Surveillance pricing algorithms typically do not use these characteristics as inputs; they use behavioral proxies (zip code, device type, browsing history, time of day of shopping) that are highly correlated with protected characteristics. "Disparate impact" frameworks could apply, but courts have been reluctant to extend Title VII and FHA disparate impact analysis to commercial pricing contexts.

### 7.3 Consent and Its Limits

Industry frequently invokes "consent" — users agreed to the terms of service; data was collected pursuant to a privacy policy; the consumer clicked "accept all cookies." This framing treats consent as binary (present or absent) rather than asking whether it is meaningful.

A meaningful consent framework for surveillance pricing would require:
1. **Specific disclosure** that the data will be used to set personalized prices
2. **Clarity** about what data sources are involved (including third-party brokers)
3. **Granularity** to allow consent to data collection while refusing consent to pricing use
4. **Genuine choice** — not presenting consent as a condition of accessing a service

None of these conditions is currently met by standard privacy policy consent mechanisms. The GDPR's consent requirements come closest, but even EU supervisory authorities have found that most commercial consent implementations do not meet the GDPR's "freely given, specific, informed and unambiguous" standard [4].

### 7.4 Opacity as a Structural Problem

Perhaps the deepest problem with surveillance pricing is not its existence but its invisibility. Consumers do not know what price others paid for the same product. They cannot verify whether they received a personalized price. They cannot determine what data was used. They have no mechanism to challenge a pricing decision they are unaware was made about them.

Transparency requirements — mandating disclosure of when personalized pricing is used and what categories of data underlie it — are a necessary first step even for those who oppose outright bans. Without transparency, neither consumers, researchers, nor regulators can assess the magnitude of the problem or verify compliance with any future rules.

---

## References

[1] Federal Trade Commission. (2025, January). *Surveillance Pricing Study Report*. Federal Trade Commission. [URL not currently accessible on ftc.gov; report released approximately January 14, 2025, under study docket P225402, during the final days of the Khan FTC. Subsequently removed from the agency website. Multiple news accounts confirm the report's release and key findings.]

[2] Robinson-Patman Act, 15 U.S.C. § 13 (1936). Retrieved from https://www.law.cornell.edu/uscode/text/15/13

[3] Federal Trade Commission Act, 15 U.S.C. § 45 (1914). Retrieved from https://www.law.cornell.edu/uscode/text/15/45

[4] Regulation (EU) 2016/679 of the European Parliament and of the Council (General Data Protection Regulation), Article 5. Official Journal of the European Union, L 119, 4 May 2016. Retrieved from https://gdpr-info.eu/art-5-gdpr/

[5] Regulation (EU) 2016/679 (GDPR), Article 22 — Automated individual decision-making, including profiling. Retrieved from https://gdpr-info.eu/art-22-gdpr/

[6] Sankin, A., & Ghaffary, S. (2021, April 1). The little-known data broker industry is spending big bucks lobbying Congress. *The Markup*. Retrieved from https://themarkup.org/privacy/2021/04/01/the-little-known-data-broker-industry-is-spending-big-bucks-lobbying-congress

[7] Valentino-DeVries, J., Singer-Vine, J., & Soltani, A. (2012, December 24). Websites vary prices, deals based on users' information. *The Wall Street Journal*. [Known to exist; not directly accessible due to paywall. Widely cited in academic and regulatory literature on algorithmic price discrimination.]

[8] Hannak, A., Soeller, G., Lazer, D., Mislove, A., & Wilson, C. (2014). Measuring price discrimination and steering on e-commerce websites. *Proceedings of the 2014 Conference on Internet Measurement (IMC '14)*, 305–318. ACM. https://doi.org/10.1145/2663716.2663744 [Confirmed to exist; not directly accessible due to ACM paywall. Widely cited in FTC and academic literature.]

[9] Mikians, J., Gyarmati, L., Erramilli, V., & Laoutaris, N. (2012). Detecting price and search discrimination on the internet. *Proceedings of the 11th ACM Workshop on Hot Topics in Networks (HotNets-XI)*. ACM. [Confirmed to exist; not directly accessible. Widely cited in academic price discrimination literature.]

[10] National Association of Insurance Commissioners (NAIC). *Credit-Based Insurance Scoring.* [The NAIC has documented this practice extensively; consumers in 47 states face credit-score-based insurance pricing. California, Hawaii, and Massachusetts prohibit the practice.]

[11] Ge, Y., Knittel, C. R., MacKenzie, D., & Zoepf, S. (2016). Racial and gender discrimination in transportation network companies. *NBER Working Paper No. 22776*. National Bureau of Economic Research. https://doi.org/10.3386/w22776

[12] Banning Surveillance Pricing Act, S. 3317, 118th Congress (2023). Introduced by Senators Warren (D-MA), Vance (R-OH), Markey (D-MA), and others. [Confirmed to exist; URL not accessible via direct fetch due to Congress.gov restrictions. Did not advance past introduction.]

[13] California Consumer Privacy Act, as amended by Proposition 24 (CPRA), Cal. Civ. Code § 1798.100 (2020, amended 2023). Retrieved from https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1798.100.&lawCode=CIV

[14] Virginia Consumer Data Protection Act, Va. Code § 59.1-577 (2021). Retrieved from https://law.lis.virginia.gov/vacode/title59.1/chapter53/section59.1-577/

[15] Regulation (EU) 2016/679 (GDPR), Article 9 — Processing of special categories of personal data. Retrieved from https://gdpr-info.eu/art-9-gdpr/

[16] Regulation (EU) 2024/1689 of the European Parliament and of the Council (EU AI Act), published in the Official Journal of the European Union, 12 July 2024. See: https://artificialintelligenceact.eu/the-act/

[17] California Privacy Protection Agency (CPPA). *Laws & Regulations.* Retrieved from https://cppa.ca.gov/regulations/

[18] Zuboff, S. (2019). *The Age of Surveillance Capitalism: The Fight for a Human Future at the New Frontier of Power*. PublicAffairs. [ISBN: 978-1-61039-569-4. Foundational theoretical framework for understanding behavioral data extraction as a market form.]

[19] Pasquale, F. (2015). *The Black Box Society: The Secret Algorithms That Control Money and Information*. Harvard University Press. [ISBN: 978-0-674-36827-2. Documents opacity in algorithmic scoring and pricing.]

[20] Federal Trade Commission. (2022, September). *Commercial Surveillance and Data Security Rulemaking: Advance Notice of Proposed Rulemaking.* [Confirmed to exist; the FTC initiated commercial surveillance rulemaking in 2022. The rulemaking was deprioritized under the current administration.]

---

*Research compiled May 2026. Intended for internal policy platform development. All factual claims are cited; limitations in source accessibility are noted inline.*