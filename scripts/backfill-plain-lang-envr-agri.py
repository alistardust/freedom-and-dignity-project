#!/usr/bin/env python3
"""Backfill plain_language for ENVR and AGRI policy positions.

Usage:
    python3 scripts/backfill-plain-lang-envr-agri.py --batch 1
    python3 scripts/backfill-plain-lang-envr-agri.py --batch 2
    python3 scripts/backfill-plain-lang-envr-agri.py --batch 3
    python3 scripts/backfill-plain-lang-envr-agri.py --batch 4

Each batch updates ~49 positions in both the SQLite DB and the HTML file.
Cards that already have class="rule-plain" in the HTML are skipped for HTML
edits but still receive the DB update.
"""

import argparse
import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
HTML_PATH = REPO_ROOT / "docs" / "policy" / "environment-and-agriculture.html"

# fmt: off
# All 196 (id, plain_language) pairs organized into 4 batches of ~49.
BATCH_1 = [
    ("AGRI-FARM-0001",
     "Poultry companies rank contract farmers against each other to determine their pay — a rigged "
     "system that keeps farmers in debt regardless of how well they perform. This policy bans that "
     '"tournament" pay system and requires enforcement of existing federal protections for contract '
     "farmers who raise chickens and livestock for large companies."),
    ("AGRI-FARM-0002",
     "Farmworkers grow the food we eat, but many lack the basic rights most workers take for granted "
     "— like the ability to form a union, work in safe conditions, or challenge exploitation under "
     "farm worker visa programs. This policy guarantees agricultural workers the same full labor "
     "protections that apply to workers in every other sector."),
    ("AGRI-FARM-0003",
     "Federal farm subsidies currently pay more to farmers who grow more corn and other commodity "
     "crops — rewarding volume over everything else, including soil health. This policy redirects "
     "those payments toward farmers who build healthy soil, diversify their crops, and farm in ways "
     "that hold up against drought, flooding, and other climate pressures."),
    ("AGRI-FOOD-0001",
     'Millions of Americans — especially in rural areas and low-income neighborhoods — live in "food '
     'deserts" where there is no nearby store selling fresh, healthy food. The federal government '
     "must act to ensure every person has access to nutritious food within a reasonable distance of "
     "their home."),
    ("ENVR-ADPT-0001",
     "Some neighborhoods face repeated, catastrophic flooding that no amount of rebuilding can fix, "
     "and climate change is making it worse. The federal government must fund voluntary buyout "
     "programs so families in the highest-risk flood and climate hazard zones can relocate to "
     "safer ground before the next disaster."),
    ("ENVR-ADPT-0002",
     "After floods, FEMA often funds rebuilding the same structures in the same flood-prone spots, "
     "guaranteeing future losses. This policy redirects disaster recovery funds toward stronger, "
     "climate-resilient construction rather than repeating the same cycle of damage and "
     "reconstruction."),
    ("ENVR-ADPT-0003",
     "Wildfires, hurricanes, rising seas, and extreme heat are forcing people from their homes — "
     "sometimes permanently. The federal government must provide real support — housing assistance, "
     "job training, and relocation help — for Americans displaced by climate conditions, whether "
     "from a single disaster or the slow creep of chronic climate stress."),
    ("ENVR-ADPT-0004",
     "Bridges, roads, water systems, and other infrastructure built with federal dollars must be "
     "designed to last in a changing climate. All federally funded projects must meet resilience "
     "standards that account for future flooding, extreme heat, and storms — not just the weather "
     "conditions of the past."),
    ("ENVR-AINL-0001",
     "When artificial intelligence (AI) is used to manage power grids, water systems, or "
     "transportation networks, safety and environmental protection must come first — not just "
     "efficiency or corporate profit. This policy requires AI systems in critical infrastructure "
     "to meet binding public-safety and environmental-protection obligations, regardless of who "
     "built them."),
    ("ENVR-AUDT-0001",
     "Large corporations must file detailed, standardized reports on their environmental impact "
     "four times a year so regulators and the public can hold them accountable. Quarterly reporting "
     "catches problems faster than annual disclosures and prevents companies from hiding their true "
     "environmental footprint."),
    ("ENVR-AUDT-0002",
     "Environmental audits must cover the full picture of a company's impact — water use, air "
     "emissions, pollutants released, and waste generated. Partial or selective disclosures do not "
     "give communities and regulators the information they need to protect public health."),
    ("ENVR-AUDT-0003",
     "To catch false reporting, audits must include both a company's own internal data and "
     "verification from multiple independent outside sources. Self-reported data alone is too easy "
     "to manipulate — independent verification is the only check that works."),
    ("ENVR-AUDT-0004",
     "Individuals who sign fraudulent environmental audits — not just their employers — can face "
     "personal criminal liability. Knowing you personally face prison time for certifying a false "
     "report makes honest auditing far more likely than fines that corporations can write off."),
    ("ENVR-AUDT-0005",
     "When companies coordinate to file false or misleading environmental reports together, the "
     "penalties are much steeper than for individual fraud. Organized cover-ups of environmental "
     "harm are treated as the serious crimes they are."),
    ("ENVR-BIOS-0001",
     "Animals that migrate seasonally — elk, salmon, monarch butterflies — need connected habitats "
     "to survive, but roads, fences, and development fragment their routes. This policy requires "
     "land managers and transportation planners to protect migration corridors so wildlife can move "
     "safely between habitats as seasons and climate conditions change."),
    ("ENVR-BIOS-0002",
     "Highways and railways cut across migration routes animals have used for thousands of years, "
     "killing millions of animals every year and isolating populations. Where roads and rail lines "
     "block key migration paths, wildlife crossings — bridges and tunnels built specifically for "
     "animals — must be constructed."),
    ("ENVR-BIOS-0003",
     "National parks and wildlife habitats belong to all Americans and must be protected from oil "
     "drilling, mining, logging, and commercial development. This policy requires adequate "
     "enforcement funding and legal mandates to restore habitats that have been damaged — not just "
     "stop new damage."),
    ("ENVR-BIOS-0004",
     "Parks, trees, and green spaces in cities reduce heat, improve air quality, support mental "
     "health, and give people outdoor places to gather. New urban development must include "
     "publicly accessible green space proportional to the number of people who live and work "
     "nearby."),
    ("ENVR-CHEM-0001",
     'PFAS are synthetic "forever chemicals" — found in thousands of products — that accumulate in '
     "human bodies and have been linked to cancer, thyroid disease, and immune system damage. This "
     "policy sets the strictest safe limits for PFAS, phases them out of non-essential uses, and "
     "requires the companies that profited from them to fund the cleanup."),
    ("ENVR-CHEM-0002",
     "Natural gas is primarily methane — a greenhouse gas far more potent than carbon dioxide "
     "over the short term. No new facilities to export liquefied natural gas (LNG) may be built, "
     "and methane leaking from gas operations must be regulated and sharply reduced under the "
     "Clean Air Act."),
    ("ENVR-CHEM-0003",
     "Some communities are surrounded by factories, refineries, and other industrial facilities "
     "and already bear far more pollution than the rest of the country. No new industrial permits "
     "may be issued in these overburdened communities, and all permitting must weigh the cumulative "
     "(total, combined) pollution burden — not just one new facility in isolation."),
    ("ENVR-CHKN-0001",
     "Contract poultry farmers are currently ranked against their neighbors to determine pay — a "
     "system that makes income unpredictable and gives companies leverage to cut costs at farmers' "
     "expense. This policy bans that tournament pay system and requires companies to compensate "
     "farmers based on objective, transparent performance standards."),
    ("ENVR-CHKN-0002",
     "Contract farmers who raise poultry under agreements with large corporations often have little "
     "power to negotiate fair terms or challenge unfair treatment. This policy establishes minimum "
     "contract rights — including clear payment terms, fair dispute resolution, and protection "
     "from retaliation — for all contract poultry growers."),
    ("ENVR-CLIS-0001",
     "The agencies that build our roads, power the grid, and supply our water need plans that "
     "account for hotter summers, rising seas, and more severe storms. Every major federal "
     "infrastructure agency must maintain a current climate adaptation plan and use it to guide "
     "where and how federal dollars are invested."),
    ("ENVR-CLIS-0002",
     "Some communities face unavoidable climate risks — from chronic flooding to sea level rise "
     "— where staying put is no longer safe. A federal program must fund planned, voluntary "
     "relocation for these communities, covering costs and helping residents transition to safer "
     "locations with dignity."),
    ("ENVR-CLLS-0001",
     "Fossil fuel companies spent decades funding disinformation campaigns about climate science "
     "while their own scientists confirmed the harm. This policy creates a federal legal cause of "
     "action so that victims of climate disasters can sue companies that deliberately misled the "
     "public while knowing their products were causing harm."),
    ("ENVR-CLLS-0002",
     "The U.S. made voluntary emissions pledges under the Paris Agreement that any future "
     "administration can ignore or reverse. This policy writes those climate commitments into "
     "binding domestic law and includes an automatic escalation mechanism if projected emissions "
     "fall behind the required pace."),
    ("ENVR-CLLS-0003",
     "Solving climate change at the scale the science requires demands federal investment "
     "comparable to a major national mobilization — at least $1 trillion per decade. This policy "
     "directs that investment, reserves 40% for frontline communities hit hardest by pollution "
     "and climate change, and guarantees jobs for fossil fuel workers displaced by the transition."),
    ("ENVR-CLLS-0004",
     "Investors and the public deserve to know how much greenhouse gas pollution large companies "
     "produce and what financial risks they face from climate change. Every publicly traded company "
     "must disclose its full emissions — including from its supply chain — and climate risks in "
     "annual SEC filings, verified by an independent auditor."),
    ("ENVR-CLNS-0001",
     "Preventing new pollution is only half the job — the contamination already in our soil, "
     "water, and air must be actively cleaned up. Environmental policy must include funded "
     "remediation of existing contamination, not just rules about what companies can't do "
     "going forward."),
    ("ENVR-CLNS-0002",
     "When a company dumps toxic waste or pollutes a community's water, the people who caused "
     "the harm — not the taxpayers or the affected residents — must pay for the cleanup. "
     "Polluters pay; communities should not subsidize the damage done to them."),
    ("ENVR-CLNS-0003",
     "Strong legal liability for pollution cleanup makes it cheaper to manage waste responsibly "
     "than to cut corners and face massive cleanup bills later. Weak liability rules let polluters "
     "profit while communities pay the price in contaminated water and poisoned soil."),
    ("ENVR-CLNS-0004",
     "When the company responsible for pollution has gone bankrupt, disappeared, or refused to "
     "act, government must have the legal authority and dedicated funding to step in and get the "
     "cleanup done. Communities should not wait decades for remediation because a polluter "
     "won't pay."),
    ("ENVR-CLNS-0005",
     "Paying for environmental cleanups requires reliable funding — through dedicated public funds, "
     "required corporate financial reserves, and mandatory bonds (deposits held in trust) that "
     "high-risk industries must post before they begin polluting activities. The money for cleanup "
     "must exist before it is needed, not after."),
    ("ENVR-CLNS-0006",
     "Pollution does not respect jurisdictional boundaries — federal, state, and local governments "
     "must coordinate their cleanup programs so contaminated sites do not fall through the gaps "
     "between agencies. Shared responsibility with clear accountability is the only way to address "
     "the full backlog of contaminated land and water."),
    ("ENVR-CLNS-0007",
     "Not all contaminated sites are equally urgent. Cleanup programs must prioritize the sites "
     "where pollution poses the greatest immediate risk to human health — especially where "
     "vulnerable people live near contamination — and to the ecosystems that cannot wait for "
     "bureaucratic scheduling."),
    ("ENVR-CLNS-0008",
     "New chemicals are introduced faster than science can study their long-term effects. "
     "Government agencies must fund ongoing research, monitoring, and proactive response to "
     "emerging contaminants before harm to people or nature becomes irreversible."),
    ("ENVR-CLNS-0009",
     'PFAS ("forever chemicals") and microplastics are virtually indestructible synthetic materials '
     "that have spread across the environment and accumulate in human bodies. Cleanup and "
     "remediation standards must specifically address how to remove and contain these persistent "
     "pollutants — not just conventional hazardous wastes."),
    ("ENVR-CLNS-0010",
     "Old factories, mine sites, and waste dumps — often located in or near residential "
     "communities — leave behind contaminated soil and groundwater that can harm health for "
     "generations. These contaminated industrial sites must be assessed, cleaned up, and restored "
     "to safe conditions."),
    ("ENVR-CLNS-0011",
     "Cleaning up contaminated industrial sites is an opportunity as well as an obligation. "
     "Community members must have meaningful input into what happens next, and redevelopment "
     "should benefit the neighborhood that lived with the contamination — not just "
     "outside investors."),
    ("ENVR-CLNS-0012",
     "Pollution does not only harm people — it poisons rivers, wetlands, forests, and the "
     "wildlife that depends on them. Full cleanup means restoring damaged ecosystems to health, "
     "not just reducing contamination to a minimum legal threshold."),
    ("ENVR-CLNS-0013",
     "When restoring a damaged ecosystem, the standard of success must be a functioning, "
     "resilient natural environment — with healthy water, diverse wildlife, and living soil — "
     "not just checking a compliance box. Biodiversity and long-term ecological health are the "
     "real measures of a genuine restoration."),
    ("ENVR-CLNS-0014",
     "People who have lived near contaminated sites have often already suffered real health "
     "consequences — cancer, birth defects, chronic illness. They must have access to health "
     "monitoring, affordable medical care, and legal tools to seek compensation for the harm "
     "done to them."),
    ("ENVR-CLNS-0015",
     "Communities have a right to know about contamination near their homes and whether cleanup "
     "is actually working. Cleanup progress, contamination data, and remediation outcomes must "
     "be publicly reported in formats that residents can actually understand and use."),
    ("ENVR-CLNS-0016",
     "Polluters must not be allowed to run out the clock through endless legal challenges while "
     "contamination continues to harm communities. Cleanup obligations cannot be delayed "
     "indefinitely — there must be enforceable deadlines and real consequences for inaction."),
    ("ENVR-CLNS-0017",
     "Companies that repeatedly ignore known contamination — despite warnings, penalties, and "
     "court orders — must face escalating consequences, up to and including direct federal "
     "intervention and takeover of the cleanup. There must be a backstop when the regulatory "
     "process repeatedly fails."),
    ("ENVR-CLNS-0018",
     "The U.S. must set and enforce hard, declining limits on total greenhouse gas emissions — "
     'a "carbon budget" — aligned with limiting global warming to 1.5°C (2.7°F), as scientists '
     "say is necessary to avoid the worst climate outcomes. Without enforceable caps, voluntary "
     "pledges will not deliver what the science requires."),
    ("ENVR-CLNS-0019",
     "Every electric utility must generate 100% of its power from clean, zero-emission sources "
     "by 2035. Clean electricity — from wind, solar, hydropower, and other renewables — is the "
     "foundation of a decarbonized economy, and this mandate sets binding interim milestones "
     "backed by federal investment and enforcement."),
    ("ENVR-CLNS-0020",
     "Methane — the main component of natural gas — traps heat in the atmosphere far more "
     "powerfully than carbon dioxide over the short term. All oil and gas operations must "
     "monitor and sharply limit methane leaks, and deliberately burning off gas (flaring) in "
     "violation of regulations must carry criminal penalties."),
]

BATCH_2 = [
    ("ENVR-COAL-0001",
     "Coal is the dirtiest source of electricity and a leading cause of air pollution, lung "
     "disease, and climate change. All coal-fired power plants must shut down by January 1, 2030 "
     "— giving utilities time to plan an orderly transition while ensuring the phase-out "
     "actually happens."),
    ("ENVR-COAL-0002",
     "Thousands of abandoned coal mines sit contaminated and unrestored across Appalachia and "
     "the West, polluting streams and endangering communities for decades. The coal industry — "
     "not taxpayers — must fund the full cleanup of every mine it abandoned."),
    ("ENVR-COAL-0003",
     "Mountaintop removal blasts apart mountains to reach coal seams beneath, permanently "
     "destroying Appalachian ecosystems and burying hundreds of miles of streams under waste. "
     "This destructive practice is prohibited with no exceptions."),
    ("ENVR-COFF-0001",
     "Carbon credits from forests — also called carbon offsets — are sold on voluntary markets "
     "where fraud and weak oversight have undermined their value and credibility. The CFTC "
     "(the federal commodity markets regulator) must set and enforce integrity standards so "
     "that a carbon credit represents real, permanent, independently verified emissions "
     "reductions."),
    ("ENVR-COFF-0002",
     "When forests sold as permanent carbon stores burn down or are cut, the emissions "
     "reductions those credits claimed no longer exist. This policy requires a permanence bond "
     "(a financial reserve held in trust) and a clear protocol for replacing reversed forest "
     "carbon credits with verified new ones."),
    ("ENVR-CORN-0001",
     "Federal law currently requires that a large share of the gasoline supply be blended with "
     "corn ethanol — a mandate that drives up corn prices, strains water resources, and provides "
     "minimal climate benefit compared to other clean energy investments. This policy repeals "
     "that mandate."),
    ("ENVR-CORN-0002",
     "The federal government spends tens of billions of dollars subsidizing corn and other "
     "commodity crops, while fruits, vegetables, and practices that build healthy soil receive "
     "a fraction of that support. Farm subsidies must be rebalanced toward the foods Americans "
     "need and the farming practices that sustain the land long-term."),
    ("ENVR-CORS-0001",
     'Companies increasingly claim to be "sustainable," "carbon neutral," or "eco-friendly" '
     "without reliable evidence behind those claims, misleading consumers. This policy "
     "establishes enforceable federal standards against greenwashing — companies must back up "
     "environmental marketing claims with verified data or face legal consequences."),
    ("ENVR-CORS-0002",
     "Anti-greenwashing rules only work if standardized, verifiable reporting backs them up. "
     "Companies must use consistent, transparent reporting formats that regulators can actually "
     "audit, so that environmental marketing claims can be measured against an objective "
     "standard."),
    ("ENVR-CORS-0003",
     'PFAS — a class of thousands of synthetic "forever chemicals" — must be classified as '
     "hazardous substances under the federal Superfund law (CERCLA), making manufacturers "
     "strictly liable for cleanup costs regardless of negligence. This removes major legal "
     "barriers to forcing polluters to pay."),
    ("ENVR-CORS-0004",
     "People who live at the fence line of factories, refineries, and chemical plants are "
     "exposed to pollution that distant regulators may not even be tracking. Mandatory real-time, "
     "publicly accessible air and water quality monitoring at these locations gives communities "
     "the information they need to protect themselves."),
    ("ENVR-CPXS-0001",
     "Making companies pay for the greenhouse gas pollution they emit — through a carbon fee or "
     "a cap-and-trade system — is one of the most effective tools for driving the clean energy "
     "transition. This policy requires major emitters to put a real price on their pollution so "
     "that clean alternatives become economically competitive."),
    ("ENVR-CPXS-0002",
     "A carbon price could raise costs for working families if the revenue simply disappears "
     "into general government funds. This policy returns all carbon revenue as a direct, "
     "equal per-person dividend to every American, so low- and middle-income households "
     "come out ahead."),
    ("ENVR-CPXS-0003",
     "The federal government currently provides over $20 billion a year in tax breaks and other "
     "subsidies to oil, gas, and coal companies — money that should be driving the clean energy "
     "transition instead. All fossil fuel subsidies must end, and the savings redirected to "
     "clean energy development and worker transition support."),
    ("ENVR-CWAS-0001",
     "The Supreme Court's 2023 Sackett ruling gutted the Clean Water Act by removing federal "
     "protection from millions of acres of wetlands and seasonal streams. This policy restores "
     "that protection by writing a clear, broad definition of protected waters into federal law "
     "— one that Congress controls, not the courts."),
    ("ENVR-CWAS-0002",
     "Millions of Americans drink tap water with unsafe levels of nitrates, arsenic, or lead — "
     "but weak federal rules and lax testing make it hard to know until harm is already done. "
     "This policy requires the EPA to set enforceable safe limits for these contaminants and "
     "mandates annual testing and public reporting by all large water systems."),
    ("ENVR-CWAS-0003",
     "States in the American West share rivers through old legal agreements (compacts) written "
     "before climate-driven water scarcity. A federal minimum ecological flow for western rivers "
     "must protect the water needed for healthy rivers and downstream communities — no state "
     "may drain a river below that minimum, even under existing water rights."),
    ("ENVR-DESS-0001",
     "Products and packaging that cannot be recycled, reused, or safely broken down are a "
     "major source of waste and pollution. New products must be designed from the start so "
     "materials can be recovered and reused — not just used once and thrown away."),
    ("ENVR-DESS-0002",
     "Products made from multiple materials bonded or glued together — foil laminated to "
     "plastic, metal fused to fabric — almost never get recycled. Using these mixed-material "
     "constructions must be phased out unless there is a strong functional reason with "
     "no viable alternative."),
    ("ENVR-DESS-0003",
     "Appliances, electronics, and other products that break easily and cannot be repaired "
     "waste both money and resources. Products must be built to last, with parts that can be "
     "replaced when they wear out rather than requiring disposal of the whole device."),
    ("ENVR-DESS-0004",
     "Sealed-in batteries, glued displays, and non-replaceable components in devices that fail "
     "most often force consumers to throw away otherwise functional products. Manufacturers must "
     "stop sealing in the parts most likely to fail first and instead design them to be "
     "user-replaceable."),
    ("ENVR-DESS-0005",
     "Federal public land belongs to all Americans, not oil and mining companies. No new "
     "permits for fossil fuel extraction on public lands may be issued, and existing permits "
     "must be phased out on a responsible timeline that protects both the environment and "
     "affected workers."),
    ("ENVR-ENFL-0001",
     "When a company's waste tanks leak, pipelines rupture, or improper disposal contaminates "
     "groundwater, that company must pay to clean it up — not the public or the affected "
     "community. Strict liability means there is no escaping responsibility by arguing the "
     "contamination was accidental."),
    ("ENVR-ENFL-0002",
     "Repeated or catastrophic violations of waste containment rules — not one-time accidents "
     "— must trigger mandatory cleanup orders and elevated criminal penalties. The law must "
     "treat systematic negligence as the deliberate choice to externalize costs onto communities "
     "that it is."),
    ("ENVR-ENFL-0003",
     "The EPA enforces the laws protecting our air, water, and land — but political pressure "
     "has repeatedly led to enforcement delays and weakened rules. The EPA must be fully funded "
     "and legally protected from political interference so enforcement decisions are made on "
     "science and law, not industry relationships."),
    ("ENVR-ENFL-0004",
     "Knowingly dumping toxic waste or falsifying environmental records are often treated as "
     "minor civil violations with modest fines — not the serious crimes they are. Major "
     "environmental violations must be upgraded to felonies, and executives who authorize "
     "them must face personal criminal liability, not just corporate fines."),
    ("ENVR-ENFL-0005",
     'The "revolving door" — where EPA officials leave to lobby for the industries they once '
     "regulated, or industry executives move into regulatory roles — undermines enforcement "
     "and public trust. A five-year waiting period before regulators can work for regulated "
     "industries, and vice versa, reduces conflicts of interest."),
    ("ENVR-ENFL-0006",
     "Environmental laws often allow ordinary citizens to sue polluters directly when the "
     "government fails to act — a critical backup enforcement tool. Those citizen suit "
     "provisions must be restored and expanded across all major environmental laws so "
     "communities can hold polluters accountable even when agencies don't."),
    ("ENVR-EPRS-0001",
     "When a company makes a product, it is responsible for what happens to that product at "
     "the end of its life — not just the consumer or the local trash service. Producers must "
     "fund and participate in systems to collect, sort, and recycle the products they sell."),
    ("ENVR-EPRS-0002",
     "Companies that design products knowing they will be difficult to recycle should pay for "
     "that difficulty — not pass the cost onto local governments and taxpayers. Producer-funded "
     "collection and recycling programs make the true cost of a product's disposal visible "
     "before it's sold."),
    ("ENVR-EPRS-0003",
     "Single-use, hard-to-recycle, or hazardous products cost far more to manage than their "
     "price tags suggest — those costs are simply paid by communities and the environment rather "
     "than the company that made them. Fees and restrictions on these products ensure their "
     "true environmental cost is built into what companies and consumers actually pay."),
    ("ENVR-EPRS-0004",
     "All plastic packaging sold in the U.S. must either be actually recycled, recovered, or "
     "composted — not just labeled recyclable without any system to do so. Extended producer "
     "responsibility (EPR) — requiring manufacturers to fund and operate take-back and recycling "
     "programs — is how that happens."),
    ("ENVR-ESCS-0001",
     "Plastics, chemicals, and other waste must be contained at every step — from factory to "
     "consumer to disposal — so they cannot escape into rivers, oceans, and wild places. "
     "Leakage into the natural environment is a system failure, and those systems must be "
     "designed to prevent it."),
    ("ENVR-ESCS-0002",
     "Every company that makes, ships, or disposes of waste products is responsible for keeping "
     "those materials contained throughout the full chain — not just while the product is in "
     "their own hands. Responsibility does not end when goods leave the factory."),
    ("ENVR-ESCS-0003",
     'Tiny plastic particles ("microplastics") and synthetic chemicals are now found in the '
     "most remote places on Earth and in human blood, lungs, and breast milk. Releasing "
     "plastics, microplastics, or persistent synthetic materials into the environment must be "
     "prohibited, and existing contamination must be remediated."),
    ("ENVR-FDSS-0001",
     "Federal food distribution programs must be structured to deliver nutritious food "
     "efficiently, equitably, and without waste. Strong food system standards reduce hunger "
     "and ensure public food dollars reach the people who need them most."),
    ("ENVR-FDSS-0002",
     "Food system regulation must address the full supply chain — from farm to table — to "
     "ensure safety, reduce food waste, and protect both producers and consumers. Gaps in "
     "oversight leave communities vulnerable to supply disruptions and food safety failures."),
    ("ENVR-FFEX-0001",
     'Hydraulic fracturing ("fracking") — high-pressure injection of water and chemicals into '
     "rock to release oil and gas — must be immediately banned on federal public lands, with a "
     "complete national phase-out within 10 years. Fracking pollutes groundwater, releases "
     "methane, and locks in decades of additional fossil fuel dependence."),
    ("ENVR-FFEX-0002",
     "Coal is the most polluting energy source and must be fully phased out — no coal-fired "
     "power by 2030, no coal mining by 2035. Workers and communities that have depended on coal "
     "must receive federally funded support to build new livelihoods."),
    ("ENVR-FFEX-0003",
     "A permanent ban on all new offshore oil and gas drilling must be enacted, existing "
     "offshore operations phased out, and over $20 billion in annual federal fossil fuel "
     "subsidies eliminated within four years. Public waters and public money must not continue "
     "funding an industry the world must move beyond."),
    ("ENVR-FRCK-0001",
     'Public lands and tribal lands belong to all Americans — they must not be used for '
     'hydraulic fracturing ("fracking"), which risks groundwater contamination and significant '
     "methane leakage. No new fracking permits may be issued on public or tribal land."),
    ("ENVR-FRCK-0002",
     "Fracking companies use hundreds of chemicals under trade secret protections, leaving "
     "communities and regulators unable to know what is being injected into the ground near "
     "their water supplies. All fracking chemical formulas must be disclosed to the public."),
    ("ENVR-FRCK-0003",
     "Research consistently shows elevated health risks for people living within a half-mile "
     "to a mile of active fracking operations — from air pollution, noise, and chemical "
     "exposure. Fracking sites must be set back at least one mile from homes, schools, and "
     "water sources."),
    ("ENVR-FRCK-0004",
     "When fracking companies go bankrupt or walk away, taxpayers often get stuck paying to "
     "plug wells and clean up the land. Before any fracking operation begins, operators must "
     "post a full financial bond covering the complete cost of well plugging and land "
     "reclamation."),
    ("ENVR-FSIL-0001",
     "The federal government currently gives over $20 billion per year in tax breaks and "
     "royalty relief to oil, gas, and coal companies — money that should be driving the clean "
     "energy transition. All fossil fuel subsidies must end immediately, and the savings must "
     "be redirected to clean energy and worker support."),
    ("ENVR-FSIL-0002",
     'Hydraulic fracturing ("fracking") on federal lands must end now, and a national phase-out '
     "of fracking must proceed under binding environmental justice standards that protect "
     "communities — often low-income and communities of color — most burdened by its "
     "health and environmental impacts."),
    ("ENVR-FSIL-0003",
     "All coal-fired power plants must close by 2030, and every affected worker and community "
     "must receive federally funded support — including income replacement, retraining, and "
     "community economic development funding. The coal phase-out must be planned and supported, "
     "not abrupt and abandoned."),
    ("ENVR-FSIL-0004",
     "No new oil and gas drilling leases may be issued on federal lands or in offshore waters, "
     "and all existing federal leases must be retired by 2035. Public land must not be "
     "committed to decades of additional fossil fuel extraction when the world urgently needs "
     "to decarbonize."),
    ("ENVR-GNDS-0001",
     "By 2035, every electric utility in the country must generate 100% of its power from "
     "clean, zero-emission sources — wind, solar, hydropower, and others. Clean electricity "
     "is the foundation for decarbonizing the entire economy, and this mandate sets binding "
     "interim milestones backed by federal investment and enforcement."),
]

BATCH_3 = [
    ("ENVR-GNDS-0002",
     "$500 billion in federal investment over 10 years must build zero-emission public transit, "
     "retrofit existing buildings for energy efficiency, and expand urban tree canopy — with at "
     "least 40% directed to frontline communities that have historically borne the worst "
     "pollution while benefiting least from public investment."),
    ("ENVR-GNDS-0003",
     "Natural gas — mostly methane, a potent greenhouse gas — must be phased out of homes and "
     "utilities. A federal methane tax on gas operations, a mandate for gas utilities to "
     "transition customers to electric alternatives by 2040, and a ban on new gas pipeline "
     "construction within two years are all required to make this happen."),
    ("ENVR-INDS-0001",
     "Factories and industrial operations must minimize the waste they generate and prevent any "
     "waste from leaking into surrounding communities and ecosystems. Contained waste cannot "
     "contaminate the air, soil, or water that neighbors depend on."),
    ("ENVR-INDS-0002",
     "If cleaner, more effective waste-reduction technology exists, industries must adopt it "
     "— not run outdated, polluting processes indefinitely just because they already own the "
     "old equipment. Best-available-technology requirements drive continuous improvement rather "
     "than locking in the worst practices of the past."),
    ("ENVR-INDS-0003",
     "Facilities that generate industrial waste must monitor what they are releasing and "
     "report it publicly. Routine monitoring and transparent reporting allow regulators, "
     "researchers, and nearby communities to identify problems before they become crises."),
    ("ENVR-INDS-0004",
     "When an industrial facility sits next to homes, a school, or a drinking water source, "
     "the margin for error is much smaller than at a remote industrial site. Facilities near "
     "sensitive communities must meet stricter environmental standards that reflect what is "
     "at stake."),
    ("ENVR-INFS-0001",
     "The systems that move and process waste — landfills, pipes, trucks, transfer stations "
     "— must be designed and operated so nothing escapes into the environment. Infrastructure "
     "failures that allow leachate, runoff, or toxic emissions are preventable and must "
     "be prevented."),
    ("ENVR-INFS-0002",
     "Landfills, waste treatment plants, and waste transport vehicles must meet current "
     "environmental standards — not the outdated requirements in place when they were built "
     "decades ago. Upgrading aging waste infrastructure protects water, air, and soil."),
    ("ENVR-INFS-0003",
     "Waste facilities — landfills, incinerators, hazardous waste sites — have historically "
     "been placed in low-income communities and communities of color at far higher rates, "
     "compounding existing health burdens. New waste facility siting must not add more burden "
     "to already overburdened neighborhoods."),
    ("ENVR-JUSS-0001",
     "When a company applies to build an industrial facility, regulators must consider the "
     "total pollution burden that community already carries — not just what one new facility "
     "would add in isolation. In communities already overloaded with pollution, no new "
     "permits may be issued."),
    ("ENVR-JUSS-0002",
     "Federal environmental enforcement must track whether its protections are applied equally "
     "— regardless of income or race — and actively correct cases where enforcement has "
     "consistently failed certain communities. Unequal pollution enforcement is both an "
     "environmental and a civil rights failure."),
    ("ENVR-JUSS-0003",
     "The communities most exposed to pollution historically have the least resources to "
     "address its consequences. Federal investment must flow to these communities for cleanup, "
     "health monitoring, medical care, and economic development — not just new rules about "
     "future projects."),
    # ENVR-LBLS-0001 already has rule-plain in HTML; use existing text for DB
    ("ENVR-LBLS-0001",
     "This position requires food labels to clearly state where meat, fish, and produce come "
     "from, requires plain-language disclosure when food contains GMO ingredients, and prohibits "
     "products from using the word \u2018natural\u2019 on their label unless they are certified to "
     "meet that standard. Consumers have the right to know what is in their food and where it "
     "was grown or raised \u2014 current labeling gaps keep that information hidden."),
    ("ENVR-LIFS-0001",
     "The environmental impact of a product doesn't end when you buy it — it continues through "
     "every year of use and into how it's eventually discarded. Manufacturers are responsible "
     "for that full lifecycle, from product design through to end-of-life management."),
    ("ENVR-LIFS-0002",
     "Products designed to be thrown away after one use or one failure waste enormous amounts "
     "of materials and energy. Every product should be repairable, upgradeable, or recyclable "
     "so that useful materials stay in circulation as long as possible."),
    ("ENVR-LIFS-0003",
     "Manufacturers must provide ways to take back their products at end of life, support "
     "repair networks, and fund recycling programs. Making producers responsible for what "
     "happens after the sale is the most effective incentive to design products that don't "
     "end up in landfills."),
    ("ENVR-MINE-0001",
     "The General Mining Act of 1872 — older than the lightbulb — allows mining companies to "
     "extract gold, silver, and other hardrock minerals from federal public land without paying "
     "royalties to the American people and often without posting adequate cleanup bonds. Mining "
     "companies must pay fair market-rate royalties and deposit full reclamation bonds before "
     "any permit is granted."),
    ("ENVR-NGAS-0001",
     "Building new natural gas pipelines, compressor stations, or distribution infrastructure "
     "after 2026 locks in decades of additional fossil fuel use and methane leakage. No new "
     "gas infrastructure may be built after that date — investment must shift to clean "
     "alternatives instead."),
    ("ENVR-NGAS-0002",
     "The pipes delivering gas to homes and apartments across the country leak methane — a "
     "potent greenhouse gas — and expose residents to indoor air pollution. All residential "
     "gas distribution lines must be replaced or shut down by 2040 as homes transition to "
     "electric heating and appliances."),
    ("ENVR-NGAS-0003",
     "Starting in 2027, all newly constructed buildings must be designed without natural gas "
     "connections. Building gas-free from the start is far cheaper and less disruptive than "
     "retrofitting later, and it sets a clear path toward eliminating fossil fuel combustion "
     "from the built environment."),
    ("ENVR-NGAS-0004",
     "New buildings starting in 2027 must use all-electric systems for heating, cooking, and "
     "hot water. Electric appliances powered by a clean grid produce zero in-home air pollution "
     "— gas appliances cannot match that, no matter how efficient they become."),
    ("ENVR-NGAS-0005",
     "Gas utilities must publish clear, public timelines for transitioning their customers to "
     "electric alternatives — not keep extending gas service indefinitely. Transparency about "
     "the transition lets households and landlords plan ahead."),
    ("ENVR-NGAS-0006",
     "No household may have its gas service shut off before an affordable, functioning electric "
     "alternative is available and accessible to that household. Protecting people from losing "
     "heat and cooking access during the transition is a basic obligation of the policy."),
    # ENVR-NUCS-0001 already has rule-plain in HTML; write new DB text for stub
    ("ENVR-NUCS-0001",
     "Nuclear power produces zero direct greenhouse gas emissions, but generates radioactive "
     "waste that remains dangerous for thousands of years. Federal policy must set clear, "
     "science-based standards for the safe operation, waste storage, and eventual "
     "decommissioning of nuclear facilities."),
    # ENVR-NUCS-0002 already has rule-plain in HTML; write new DB text for stub
    ("ENVR-NUCS-0002",
     "Radioactive waste from nuclear plants is currently stored at dozens of sites across "
     "the country without a permanent disposal solution, posing long-term risks to communities "
     "and groundwater. Federal policy must fund and implement a permanent waste disposal "
     "program and ensure existing storage sites are safely maintained."),
    ("ENVR-OCNS-0001",
     "Marine reserves — ocean areas where fishing and other extraction are prohibited — "
     "allow fish populations and ocean ecosystems to recover and become more resilient. "
     "Designating 30% of U.S. ocean waters as no-take reserves by 2030, managed by an "
     "independent science board, gives ocean life the space and time to rebuild."),
    ("ENVR-OCNS-0002",
     "Deep-sea mining would destroy some of the least-understood and most fragile ecosystems "
     "on Earth to extract minerals for batteries and electronics. It must be prohibited in "
     "all U.S. waters and actively opposed in international negotiations."),
    ("ENVR-OILG-0001",
     "U.S. offshore waters belong to all Americans, not the oil industry. No new offshore "
     "oil and gas drilling leases may be issued — ending the expansion of a system that risks "
     "oil spills, harms marine ecosystems, and deepens long-term fossil fuel dependence."),
    ("ENVR-OILG-0002",
     "When offshore oil rigs and pipelines reach the end of their useful lives, operators "
     "often delay or avoid decommissioning (dismantling and cleanup) indefinitely, leaving "
     "aging infrastructure to rust and eventually fail. All offshore infrastructure must be "
     "fully removed at the operator's expense within five years of the end of production."),
    ("ENVR-OILG-0003",
     "When offshore oil spills happen, the current legal caps on how much the responsible "
     "company must pay are far too low to cover the true environmental and economic damage. "
     "Oil spill liability limits must be doubled and operators must post full environmental "
     "restoration bonds before any new drilling begins."),
    ("ENVR-OILG-0004",
     "Coastal communities, beaches, fisheries, and marine ecosystems within 50 miles of shore "
     "are most vulnerable to offshore drilling accidents. Drilling must be prohibited within "
     "that distance from any U.S. coastline."),
    # ENVR-ORGS-0001 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-ORGS-0001",
     "This position creates a federal program that supports farmers converting their land to "
     "organic production by providing five years of income payments, technical assistance, and "
     "coverage of certification fees during the difficult transition period. The income gap "
     "that farmers face while transitioning to organic \u2014 before their land qualifies for "
     "premium prices \u2014 is a major barrier that this program removes."),
    # ENVR-ORGS-0002 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-ORGS-0002",
     "This position requires that federal commodity support and crop insurance programs be "
     "restructured to eliminate the financial advantage that conventional industrial farming "
     "currently has over organic and diversified farming. Federal subsidies currently tilt the "
     "playing field heavily toward monoculture; rebalancing them gives farmers a real choice "
     "to adopt more sustainable practices."),
    # ENVR-PFAS-0001 already has rule-plain in HTML (stub); write new DB text
    ("ENVR-PFAS-0001",
     'PFAS are a class of thousands of synthetic "forever chemicals" — found in everything '
     "from nonstick cookware to firefighting foam — that persist in the environment and in "
     "human bodies indefinitely. A comprehensive federal framework must cover all PFAS "
     "compounds — not just a handful — with strict limits, phase-outs, and cleanup "
     "requirements."),
    # ENVR-PFAS-0002 already has rule-plain in HTML (stub); write new DB text
    ("ENVR-PFAS-0002",
     "Meaningful PFAS regulation requires coordinated action across multiple agencies — EPA, "
     "FDA, USDA, and DoD — covering drinking water, food, consumer products, and industrial "
     "uses. A coherent national PFAS policy must close the gaps between agencies that allow "
     "ongoing exposure to continue."),
    # ENVR-PFAS-0003 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-PFAS-0003",
     "This position requires the EPA to set binding drinking water limits for all PFAS "
     "compounds at the lowest detectable level, and requires Congress to ban all non-essential "
     "uses of PFAS in consumer products within five years. PFAS \u2014 known as "
     "\u201cforever chemicals\u201d \u2014 accumulate in human bodies and have been linked to "
     "cancer, thyroid disease, and immune system damage."),
    # ENVR-PFAS-0004 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-PFAS-0004",
     "This position holds PFAS manufacturers fully and directly liable for all remediation "
     "costs and victims\u2019 medical expenses when they knowingly concealed the health risks "
     "of their products \u2014 with no \u201csophisticated purchaser\u201d defense allowed for "
     "consumer-facing products. Companies that hid what they knew about PFAS toxicity for "
     "decades must pay to clean up the contamination they caused and provide healthcare to "
     "those they harmed."),
    # ENVR-PFAS-0005 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-PFAS-0005",
     "This position requires the Department of Defense to complete full PFAS remediation at "
     "all contaminated military bases within 10 years, provide free lifetime healthcare to all "
     "veterans and family members with PFAS exposure, and compensate affected communities for "
     "contaminated water and property. Military firefighting foam is a major source of PFAS "
     "contamination near bases, and those who served their country should not bear the health "
     "costs of that pollution."),
    ("ENVR-PKGS-0001",
     "Layers of unnecessary packaging — multi-layer plastic pouches, mixed-material wrapping, "
     "decorative boxes inside boxes — generate enormous waste that largely cannot be recycled. "
     "Regulations must set limits on excessive packaging and require that what remains is "
     "actually designed to be recovered and reused."),
    ("ENVR-PKGS-0002",
     "Packaging made from materials that cannot be separated — foil bonded to plastic, "
     "mixed-material laminates — goes directly to the landfill even when consumers try to "
     "recycle it. These non-separable packaging types must be phased out."),
    ("ENVR-PKSS-0001",
     "National parks, wilderness areas, and wildlife habitats are shared public assets that "
     "must be protected from being sold off, drilled, mined, or logged. Strong enforcement "
     "funding and legal mandates to restore damaged areas ensure that protection is real, "
     "not just a promise on paper."),
    ("ENVR-PLSS-0001",
     "Single-use plastics — straws, bags, utensils, coffee cups — are used for minutes and "
     "persist in the environment for centuries. Production and use of these items must be "
     "reduced through fees, restrictions, and phase-outs, with genuinely sustainable "
     "alternatives developed to replace them."),
    ("ENVR-PLSS-0002",
     'Products labeled "biodegradable" or "compostable" often break down only under specific '
     "industrial conditions that most communities cannot provide, misleading consumers into "
     "thinking they are making a green choice. Any alternative to plastic must meet verified "
     "environmental standards and actually decompose in realistic conditions."),
    ("ENVR-PLSS-0003",
     "Single-use plastics in food service — cups, lids, containers, cutlery — are among the "
     "largest sources of plastic waste entering waterways and oceans. Fees, restrictions, and "
     "redesign requirements must drive a real shift away from throwaway plastic in food and "
     "beverage service."),
    ("ENVR-PLSS-0004",
     "Microbeads — tiny plastic particles used as exfoliants in cosmetics and as abrasives "
     "in cleaning products — wash directly into waterways and are too small to filter out in "
     "wastewater treatment. Intentionally added microplastics in consumer products must be "
     "completely banned."),
    ("ENVR-PLSS-0005",
     "The federal government must lead by example: all federal agencies and facilities must "
     "stop purchasing single-use plastics by 2028. Removing single-use plastics from federal "
     "procurement removes billions of dollars in demand for disposable plastic and sends a "
     "clear market signal."),
    ("ENVR-PLST-0001",
     "Plastic producers currently sell packaging without funding the systems needed to collect "
     "and recycle it — those costs fall on local governments and taxpayers. Plastic packaging "
     "producers must directly fund real recycling infrastructure, not lobby for voluntary "
     "pledges that never get built."),
    ("ENVR-PLST-0002",
     "Electronics, batteries, and hazardous consumer products contain materials that are toxic "
     "in landfills and valuable if recovered — but most people have no practical way to dispose "
     "of them responsibly. Extended producer responsibility (EPR) — manufacturers funding and "
     "operating take-back programs — must apply to all these product categories."),
    ("ENVR-PLTR-0001",
     "The tournament system pays poultry contract farmers by comparing their flock performance "
     "against neighbors — a ranking that companies can manipulate through unequal input "
     "supplies. This system must be abolished and replaced with pay based on objective, "
     "transparent, independently verifiable performance criteria."),
]

BATCH_4 = [
    ("ENVR-POLC-0001",
     "Noise pollution — from traffic, airports, construction, and industrial equipment "
     "— damages hearing, raises stress, and disrupts sleep for tens of millions of Americans. "
     "The federal government must set stronger standards for monitoring and reducing noise "
     "pollution across industries and transportation systems."),
    ("ENVR-POLC-0002",
     "Artificial light at night disrupts human sleep patterns, interferes with nocturnal "
     "wildlife, and has made the night sky invisible to most Americans. Stronger national "
     "standards for light pollution will protect both human health and the natural environment "
     "that depends on darkness."),
    ("ENVR-POLC-0003",
     "Wireless networks are expanding rapidly, and exposure to electromagnetic radiation from "
     "towers and infrastructure is a growing concern for communities where infrastructure is "
     "concentrated. The federal government must set and enforce standards for monitoring "
     "electromagnetic exposure and protecting public safety as networks proliferate."),
    ("ENVR-POLC-0004",
     'Microplastics and PFAS ("forever chemicals") have spread throughout the environment and '
     "are now detected in human blood, rainwater, and the most remote ecosystems. National "
     "pollution standards must specifically address monitoring and reducing these chemical "
     "pollutants alongside conventional air and water pollution."),
    ("ENVR-POLC-0005",
     "Current EPA air quality standards for fine particulate matter (PM2.5 — tiny particles "
     "that penetrate deep into lungs), ozone, and other pollutants may not fully protect "
     "public health based on the latest science. National standards must be updated and "
     "expanded to address emerging industrial pollutants that current rules do not yet cover."),
    ("ENVR-PSTS-0001",
     "Many pesticides were approved for use decades ago under weaker scientific standards "
     "than we have today and have never been fully reassessed. The EPA must complete a thorough "
     "re-evaluation of all pre-1996 pesticide registrations within five years, using current "
     "toxicology and environmental science."),
    ("ENVR-PSTS-0002",
     "Most farms rely heavily on chemical pesticides, but biological alternatives — beneficial "
     "insects, crop rotation, targeted treatments — can achieve similar results with far less "
     "environmental harm. A federal cost-share program helps farmers adopt Integrated Pest "
     "Management (using multiple strategies to reduce pesticide dependence) without bearing "
     "the full cost of the transition alone."),
    ("ENVR-RECS-0001",
     "The current patchwork of local recycling programs — each with different rules for what "
     "can be recycled and how — confuses consumers and produces low-quality material that often "
     "ends up in landfills anyway. Recycling infrastructure must be expanded, standardized, "
     "and modernized to handle the volume and variety of materials we actually produce."),
    ("ENVR-RECS-0002",
     "A recycling bin and a truck that collects it are only the beginning — the materials must "
     "actually be sorted and processed into usable raw material. Local recycling programs must "
     "be fully funded to do the complete job, not just collect materials that quietly end up "
     "in the landfill."),
    ("ENVR-RECS-0003",
     "Recycling labels vary wildly across communities — the same symbol can mean recyclable "
     "here and not recyclable anywhere in the same metropolitan area. Standardized, accurate "
     "recycling labels help people sort correctly and prevent contamination of recycling "
     "streams."),
    ("ENVR-REGS-0001",
     "Regenerative agriculture — farming practices that build soil organic matter, reduce "
     "erosion, and restore the land's capacity to hold water — improves long-term farm "
     "productivity while capturing carbon from the atmosphere. Federal policy must promote "
     "and financially support these practices."),
    ("ENVR-REGS-0002",
     "Crop rotation, cover crops, and reduced tillage (less plowing) build healthier soil, "
     "reduce fertilizer runoff, and help the land absorb and store carbon. Farmers who adopt "
     "these practices must be incentivized and supported through federal conservation programs."),
    ("ENVR-REGS-0003",
     "Heavy reliance on synthetic pesticides and fertilizers degrades soil, pollutes "
     "waterways, and creates health risks for farm workers and nearby communities. Federal "
     "programs must support and fund farmers who transition to organic and low-input methods "
     "that reduce these harms."),
    ("ENVR-REGS-0004",
     "Precision agriculture technologies — GPS-guided planting, soil sensors, drone monitoring "
     "— can dramatically reduce fertilizer, pesticide, and water use while maintaining yields. "
     "Federal investment must support development and adoption of these tools, especially for "
     "smaller farms that can't afford them alone."),
    ("ENVR-REGS-0005",
     "Healthy soil is a long-term national resource, but it is rarely measured or tracked. "
     "Farms participating in USDA conservation programs must measure and report their soil "
     "health over time so that public money actually funds practices that improve the land."),
    ("ENVR-REGS-0006",
     "Fertilizer and pesticide runoff from farms is one of the leading causes of water "
     "pollution in the U.S., creating dead zones in the Gulf of Mexico and contaminating "
     "drinking water sources. Farms receiving federal subsidy payments must have — and "
     "follow — plans to manage their runoff."),
    ("ENVR-REGS-0007",
     "Large-scale livestock operations often confine animals in conditions that cause severe, "
     "chronic suffering. Federal standards must establish minimum humane confinement conditions "
     "— covering space, movement, and basic behavioral needs — for animals raised in large-scale "
     "industrial operations."),
    ("ENVR-RFNY-0001",
     "Building new oil refineries or expanding existing ones only makes sense if you plan to "
     "keep burning oil for decades — the opposite of what the climate requires. No new "
     "refinery construction or capacity expansion permits may be issued after 2025."),
    ("ENVR-RFNY-0002",
     "Oil refineries are a major source of air pollution, including toxic compounds linked "
     "to cancer and respiratory disease in nearby communities. All operating refineries must "
     "meet current EPA air quality standards within five years — not just new facilities."),
    ("ENVR-RFNY-0003",
     "Refineries that eventually shut down must be fully cleaned up, but cleanup costs are "
     "often abandoned to the public when companies fail or walk away. Before expanding "
     "capacity, refinery operators must post full decommissioning bonds — deposits held in "
     "trust to fund cleanup when the time comes."),
    # ENVR-RTFS-0001 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-RTFS-0001",
     "This position prohibits the federal government from overriding state and local laws "
     "that set stricter environmental, food safety, pesticide, or animal welfare standards "
     "than federal minimums in agriculture and food production. Federal law is a floor, not "
     "a ceiling \u2014 states and localities that want stronger protections for their residents "
     "and environment should not be blocked from providing them."),
    ("ENVR-SPCS-0001",
     "Thousands of decommissioned satellites and rocket stages in orbit — space debris, "
     "also called space junk — create growing collision risks for active satellites, space "
     "stations, and future missions. Federal rules must require companies to actively remove "
     "or mitigate their spent hardware."),
    ("ENVR-SPCS-0002",
     "Rapid deployment of large private satellite constellations creates radio frequency "
     "interference and light pollution that affects scientific research and astronomy. "
     "Stronger regulation of private satellite deployment is needed before the orbital "
     "environment becomes too congested for science and safety."),
    ("ENVR-SPCS-0003",
     "Private companies launching satellite networks must meet environmental, scientific, "
     "and orbital safety standards before they are approved to deploy — not after thousands "
     "of satellites are already in orbit. Regulatory approval must come before launch, "
     "not be negotiated after the fact."),
    # ENVR-SUBS-0001 already has rule-plain in HTML (stub); write new DB text
    ("ENVR-SUBS-0001",
     "Federal farm subsidies are heavily skewed toward large industrial commodity operations "
     "and away from small, diversified, and beginning farmers. Subsidy reform must rebalance "
     "this support toward farms that serve communities, build long-term soil health, and "
     "contribute to local food systems."),
    # ENVR-SUBS-0002 already has rule-plain in HTML (stub); write new DB text
    ("ENVR-SUBS-0002",
     "Agricultural subsidies should be tied to practices that deliver real public benefits "
     "— clean water, healthy soil, reduced chemical use, climate resilience — not simply to "
     "how much commodity a farm produces. Tying payments to environmental outcomes shifts "
     "public spending toward lasting value."),
    ("ENVR-SUPR-0001",
     "Companies must not be allowed to permanently disable (brick) a working physical device "
     "simply by ending software support or shutting down online services. Hardware that is "
     "physically functional must remain functional regardless of the manufacturer's "
     "business decisions."),
    ("ENVR-SUPR-0002",
     "When a manufacturer ends support for a product's software, they must release that "
     "software as open source or provide a functional way to keep the product running. "
     "This prevents hardware built with real materials and energy from becoming landfill "
     "just because a company stopped issuing updates."),
    ("ENVR-SYSR-0001",
     "Waste reduction, recyclability, repairability, and durability are not separate issues "
     "— they must be integrated into a unified regulatory framework across environmental, "
     "consumer protection, and product safety rules. Fragmented rules let manufacturers "
     "evade accountability for the waste their products generate."),
    ("ENVR-SYSR-0002",
     "When waste-generating practices can dodge accountability by falling between agencies "
     "— not an EPA issue, not a consumer protection issue — those jurisdictional gaps must "
     "be closed by design, not left for communities to fight over case by case."),
    ("ENVR-SYSR-0003",
     'Federal waste policy must be built around a circular economy model — keeping materials '
     "in use as long as possible, minimizing what gets extracted from nature, and closing "
     "the loop so waste from one process becomes input for another. Linear "
     "\u201ctake-make-throw\u201d systems waste finite resources and externalize harm onto "
     "communities and ecosystems."),
    ("ENVR-SYSR-0004",
     "Waste rules must cover a product's full journey — how it is extracted, manufactured, "
     "used, and eventually discarded — not just what happens at the final disposal stage. "
     "Problems designed into a product at the beginning cannot be fixed by better trash "
     "management at the end."),
    ("ENVR-SYSR-0005",
     "Waste issues routinely cut across the responsibilities of multiple agencies — EPA, "
     "FDA, FTC, CPSC, USDA. Those agencies must coordinate rather than each treating waste "
     "as someone else's problem. Cross-agency coordination is required, not optional."),
    ("ENVR-SYSR-0006",
     "The science of materials, environmental impact, and waste management evolves rapidly "
     "— regulatory standards must be updated regularly to keep pace with that science, not "
     "left static for decades while the problems around them change."),
    ("ENVR-TRAN-0001",
     "How much waste is the U.S. actually generating? What percentage is being recycled, "
     "and what is leaking into the environment? Government must track and publish this data "
     "so policymakers and the public can know whether current policies are working and where "
     "attention is most needed."),
    ("ENVR-TRAN-0002",
     "National averages can hide serious local problems — a neighborhood where recycling "
     "rates are zero or where pollution is leaking into a local creek. Environmental data "
     "must be collected at high enough resolution to detect local disparities and emerging "
     "issues before they become crises."),
    ("ENVR-TRAN-0003",
     "Environmental data is only useful if people can actually access and work with it. "
     "Data on waste, recycling, pollution, and material flows must be published in formats "
     "that communities, researchers, and policymakers can use — not archived in inaccessible "
     "government databases."),
    ("ENVR-TRAN-0004",
     "When every industry and every state uses different definitions and formats for "
     "environmental reporting, comparisons are impossible and patterns are invisible. "
     "Standardized reporting requirements across industries and jurisdictions make "
     "accountability possible."),
    ("ENVR-TRAN-0005",
     "Transparency in environmental reporting is about more than publishing numbers — it "
     "is about whether communities, regulators, and advocates can actually use that data "
     "to hold polluters accountable. Open, accessible reporting builds the public trust "
     "and enforcement capacity that environmental protection requires."),
    # ENVR-TRNS-0001 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-TRNS-0001",
     "This position guarantees that every worker in coal mining, oil and gas extraction, "
     "petroleum refining, or coal power whose job is eliminated by the clean energy transition "
     "receives five years of full wage replacement, lifetime healthcare, and full pension "
     "vesting \u2014 regardless of how close to retirement they are. These workers kept "
     "America\u2019s energy system running; they deserve real economic security, not just "
     "retraining brochures."),
    # ENVR-TRNS-0002 already has good rule-plain in HTML; use existing text for DB
    ("ENVR-TRNS-0002",
     "This position requires clean energy developers receiving federal incentives to "
     "prioritize hiring from fossil fuel communities and contribute to community reinvestment "
     "funds. It also requires fossil fuel companies to fully remediate all abandoned wells, "
     "mines, and contaminated sites before they can receive any new permits \u2014 making "
     "them clean up their past before profiting from the future."),
    ("ENVR-URBS-0001",
     "Parks, community gardens, tree canopy, and other green spaces reduce heat, improve "
     "air quality, support mental health, and give people outdoor places to gather. Cities "
     "must plan and maintain publicly accessible green space proportional to the number of "
     "people who live there — not just where property values make it convenient."),
    ("ENVR-WSTS-0001",
     "Reducing waste at the source — making less of it in the first place — is far more "
     "effective than managing it after it has been created. All waste policy must start "
     "with minimizing generation and preventing materials from escaping into the environment, "
     "not just finding better ways to dispose of them."),
    ("ENVR-WSTS-0002",
     "The right order of waste management — reduce first, then reuse, then recycle, then "
     "safely dispose — reflects a basic truth: the further down the chain you go, the more "
     "value and resources are already lost. All waste policy must follow this hierarchy."),
    ("ENVR-WSTS-0003",
     "When a new material's long-term environmental impact is unknown, the default must be "
     "caution — not wait-and-see. The precautionary principle, acting to prevent harm before "
     "it is proven rather than waiting for evidence of damage, must guide how novel materials "
     "are regulated."),
    ("ENVR-WSTS-0004",
     "New categories of materials — nanomaterials (particles measured in billionths of a "
     "meter), synthetic biology products, advanced composites — are entering the waste stream "
     "faster than current regulations can address them. Waste policy must be regularly updated "
     "to govern these emerging categories before they cause irreversible harm."),
    ("ENVR-WTRS-0001",
     "Safe drinking water is a fundamental right, not a luxury — but millions of Americans, "
     "especially in low-income communities and communities of color, live with contaminated "
     "or unaffordable water. Federal law must set enforceable minimum water quality standards, "
     "prioritize cleanup of contaminated systems, and ensure no household loses access to "
     "safe water because they cannot pay."),
    ("ENVR-WTRS-0002",
     "Water scarcity and contamination affect entire regions — from aquifers depleted by "
     "farming to rivers poisoned by industry to recharge zones paved over by development. "
     "Federal and state water law must address all of these threats, update interstate "
     "water-sharing agreements for a drier climate, and guarantee downstream communities "
     "always have adequate water access."),
    ("ENVR-WTRS-0003",
     'PFAS ("forever chemicals"), nitrates from fertilizer runoff, lead from old pipes, and '
     "arsenic from natural deposits are among the most dangerous drinking water contaminants "
     "— but federal limits on several of them lag far behind the science. All drinking water "
     "contaminant limits must be based on the best available health science and updated "
     "regularly as knowledge improves."),
]
# fmt: on

ALL_BATCHES = {
    1: BATCH_1,
    2: BATCH_2,
    3: BATCH_3,
    4: BATCH_4,
}

# IDs that already have rule-plain in the HTML — skip HTML insertion for these.
HTML_ALREADY_FILLED = {
    "ENVR-FDSS-0001",
    "ENVR-FDSS-0002",
    "ENVR-LBLS-0001",
    "ENVR-NUCS-0001",
    "ENVR-NUCS-0002",
    "ENVR-ORGS-0001",
    "ENVR-ORGS-0002",
    "ENVR-PFAS-0001",
    "ENVR-PFAS-0002",
    "ENVR-PFAS-0003",
    "ENVR-PFAS-0004",
    "ENVR-PFAS-0005",
    "ENVR-RTFS-0001",
    "ENVR-SUBS-0001",
    "ENVR-SUBS-0002",
    "ENVR-TRNS-0001",
    "ENVR-TRNS-0002",
}


def update_db(updates: list[tuple[str, str]]) -> None:
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.executemany(
            "UPDATE positions SET plain_language = ? WHERE id = ?",
            [(text, pid) for pid, text in updates],
        )
        conn.commit()
        print(f"  DB: updated {conn.total_changes} rows")
    finally:
        conn.close()


def insert_plain_language_html(html: str, card_id: str, plain_text: str) -> str:
    """Insert <p class="rule-plain"> after <p class="rule-title"> in the card."""
    # Check if rule-plain already exists in this card's section
    card_pattern = re.compile(
        r'id="' + re.escape(card_id) + r'"(.*?)</div>',
        re.DOTALL,
    )
    m = card_pattern.search(html)
    if not m:
        print(f"  WARNING: card {card_id} not found in HTML")
        return html
    if "rule-plain" in m.group(1):
        print(f"  HTML: {card_id} already has rule-plain — skipping")
        return html

    # Find rule-title closing tag within this card and insert after it
    title_pattern = re.compile(
        r'(id="' + re.escape(card_id) + r'".*?<p[^>]*class="rule-title"[^>]*>.*?</p>)',
        re.DOTALL,
    )
    tm = title_pattern.search(html)
    if not tm:
        print(f"  WARNING: rule-title not found for {card_id}")
        return html

    new_para = f'<p class="rule-plain">{plain_text}</p>'
    insert_pos = tm.end()
    return html[:insert_pos] + new_para + html[insert_pos:]


def process_batch(batch_num: int) -> None:
    updates = ALL_BATCHES[batch_num]
    print(f"\nProcessing batch {batch_num} ({len(updates)} positions)…")

    # 1. Update DB
    print("Updating database…")
    update_db(updates)

    # 2. Update HTML
    print("Updating HTML…")
    html = HTML_PATH.read_text(encoding="utf-8")
    html_updates = 0
    html_skips = 0

    for card_id, plain_text in updates:
        if card_id in HTML_ALREADY_FILLED:
            html_skips += 1
            continue
        new_html = insert_plain_language_html(html, card_id, plain_text)
        if new_html != html:
            html_updates += 1
        html = new_html

    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"  HTML: inserted {html_updates} rule-plain paragraphs, skipped {html_skips}")
    print(f"Batch {batch_num} complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill ENVR/AGRI plain language")
    parser.add_argument(
        "--batch",
        type=int,
        choices=[1, 2, 3, 4],
        required=True,
        help="Which batch to process (1–4)",
    )
    args = parser.parse_args()
    process_batch(args.batch)


if __name__ == "__main__":
    main()
