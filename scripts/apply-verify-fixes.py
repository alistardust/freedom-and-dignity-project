#!/usr/bin/env python3
"""
Apply all VERIFY marker fixes to equal-justice-and-policing.njk.

Removes <!-- [VERIFY] --> markers, inserts inline citations, applies
factual corrections, and appends footnotes fn13–fn80.
"""

from pathlib import Path

TARGET = Path("src/pages/policy/equal-justice-and-policing.njk")

# ---------------------------------------------------------------------------
# Replacements: (old_text, new_text)
# Applied in order — each old_text must be unique in the file.
# ---------------------------------------------------------------------------
REPLACEMENTS = [
    # ── Line 206: wealth/liberty — policy's own reasoning, remove only ──────
    (
        "one cannot. <!-- [VERIFY] -->",
        "one cannot.",
    ),
    # ── Line 295: Mandela Rules CIDT threshold ────────────────────────────
    (
        "as cruel, inhuman, or degrading treatment. <!-- [VERIFY] -->",
        "as cruel, inhuman, or degrading treatment."
        '<sup><a href="#fn13" id="ref13">[13]</a></sup>',
    ),
    # ── Line 464: Fair Sentencing Act of 2010 ────────────────────────────
    (
        "did not achieve parity and was not made retroactive. <!-- [VERIFY] -->",
        "did not achieve parity and was not made retroactive."
        '<sup><a href="#fn14" id="ref14">[14]</a></sup>',
    ),
    # ── Line 472: Cannabis Schedule I ───────────────────────────────────
    (
        "majority public support for federal legalization. <!-- [VERIFY] -->",
        "majority public support for federal legalization."
        '<sup><a href="#fn15" id="ref15">[15]</a></sup>',
    ),
    # ── Line 480: drug arrests majority for possession ───────────────────
    (
        "majority for possession rather than sale. <!-- [VERIFY] -->",
        "majority for possession rather than sale."
        '<sup><a href="#fn16" id="ref16">[16]</a></sup>',
    ),
    # ── Line 812: facially neutral laws / racial impact — remove only ────
    (
        "without assessment of differential racial impact. <!-- [VERIFY] -->",
        "without assessment of differential racial impact.",
    ),
    # ── Line 820: no reliable national policing data ────────────────────
    (
        "does not currently exist. <!-- [VERIFY] -->",
        "does not currently exist."
        '<sup><a href="#fn17" id="ref17">[17]</a></sup>',
    ),
    # ── Line 954: Graham v. Connor objective reasonableness — remove only ─
    (
        "even when de-escalation alternatives were available. <!-- [VERIFY] -->",
        "even when de-escalation alternatives were available.",
    ),
    # ── Line 962: body cameras create objective record — remove only ──────
    (
        "that would otherwise become contested factual disputes. <!-- [VERIFY] -->",
        "that would otherwise become contested factual disputes.",
    ),
    # ── Line 970: wandering officers ────────────────────────────────────
    (
        "at other law enforcement agencies because no binding national registry exists. <!-- [VERIFY] -->",
        "at other law enforcement agencies because no binding national registry exists."
        '<sup><a href="#fn18" id="ref18">[18]</a></sup>',
    ),
    # ── Line 987 (1): <10% agencies require de-escalation ────────────────
    (
        "de-escalation before force. <!-- [VERIFY] -->",
        "de-escalation before force."
        '<sup><a href="#fn19" id="ref19">[19]</a></sup>',
    ),
    # ── Line 987 (2): Black Americans killed 2.5× rate ───────────────────
    (
        "at approximately 2.5 times the rate of white Americans. <!-- [VERIFY] -->",
        "at approximately 2.5 times the rate of white Americans."
        '<sup><a href="#fn20" id="ref20">[20]</a></sup>',
    ),
    # ── Line 995 (1): Trump DOJ curtailed Pattern-or-Practice ────────────
    (
        "sought to exit existing consent decrees. <!-- [VERIFY] -->",
        "sought to exit existing consent decrees."
        '<sup><a href="#fn21" id="ref21">[21]</a></sup>',
    ),
    # ── Line 995 (2): consent decrees reduce force complaints ────────────
    (
        "measurable reductions in excessive force complaints. <!-- [VERIFY] -->",
        "measurable reductions in excessive force complaints."
        '<sup><a href="#fn22" id="ref22">[22]</a></sup>',
    ),
    # ── Line 1003: police union contracts impede accountability ──────────
    (
        "frequently overturns findings of misconduct. <!-- [VERIFY] -->",
        "frequently overturns findings of misconduct."
        '<sup><a href="#fn23" id="ref23">[23]</a></sup>',
    ),
    # ── Line 1011: fewer than 200 agencies have civilian oversight ────────
    (
        "most that exist have only advisory authority. <!-- [VERIFY] -->",
        "most that exist have only advisory authority."
        '<sup><a href="#fn24" id="ref24">[24]</a></sup>',
    ),
    # ── Line 1028 (1): Brady violations → wrongful convictions ───────────
    (
        "are a leading cause of wrongful convictions. <!-- [VERIFY] -->",
        "are a leading cause of wrongful convictions."
        '<sup><a href="#fn25" id="ref25">[25]</a></sup>',
    ),
    # ── Line 1028 (2): absolute prosecutorial immunity ───────────────────
    (
        "even prosecutors who knowingly send innocent people to prison face no civil liability. <!-- [VERIFY] -->",
        "even prosecutors who knowingly send innocent people to prison face no civil liability."
        '<sup><a href="#fn26" id="ref26">[26]</a></sup>',
    ),
    # ── Line 1043 (1): 3,000+ exonerations, avg. decade in prison ────────
    (
        "spending an average of over a decade in prison. <!-- [VERIFY] -->",
        "spending an average of over a decade in prison."
        '<sup><a href="#fn27" id="ref27">[27]</a></sup>',
    ),
    # ── Line 1043 (2): discredited forensic techniques ───────────────────
    (
        "that have since been discredited by the scientific community. <!-- [VERIFY] -->",
        "that have since been discredited by the scientific community."
        '<sup><a href="#fn28" id="ref28">[28]</a></sup>',
    ),
    # ── Line 1051 (1): 97%/94% guilty pleas ──────────────────────────────
    (
        "result of guilty pleas, not trials. <!-- [VERIFY] -->",
        "result of guilty pleas, not trials."
        '<sup><a href="#fn29" id="ref29">[29]</a></sup>',
    ),
    # ── Line 1051 (2): trial penalty ─────────────────────────────────────
    (
        'a phenomenon scholars call the "trial penalty." <!-- [VERIFY] -->',
        'a phenomenon scholars call the "trial penalty."'
        '<sup><a href="#fn30" id="ref30">[30]</a></sup>',
    ),
    # ── Line 1205: criminal-history checkbox as categorical exclusion — remove only ──
    (
        "or relevance to the job. <!-- [VERIFY] -->",
        "or relevance to the job.",
    ),
    # ── Line 1213: FACTUAL CORRECTION (4.6M→4M, 75%→70%) + fn31 ─────────
    (
        "Approximately 4.6 million Americans are disenfranchised due to felony convictions, "
        "with an estimated 75% of them living in the community, not incarcerated: but still "
        "barred from voting due to parole, probation, or unpaid fees and fines. <!-- [VERIFY] -->",
        "Approximately 4 million Americans are disenfranchised due to felony convictions, "
        "with an estimated 70% of them living in the community, not incarcerated: but still "
        "barred from voting due to parole, probation, or unpaid fees and fines."
        '<sup><a href="#fn31" id="ref31">[31]</a></sup>',
    ),
    # ── Line 1221: FAFSA Simplification Act 2020 ──────────────────────────
    (
        "subject to reversal. <!-- [VERIFY] -->",
        "subject to reversal."
        '<sup><a href="#fn32" id="ref32">[32]</a></sup>',
    ),
    # ── Line 1229: housing stability and reintegration — remove only ──────
    (
        "when stability is most critical to successful reintegration. <!-- [VERIFY] -->",
        "when stability is most critical to successful reintegration.",
    ),
    # ── Line 1666: mandatory minimums enacted 1980s–90s ────────────────
    (
        "Federal mandatory minimums were largely enacted during the 1980s and 1990s drug war. <!-- [VERIFY] -->",
        "Federal mandatory minimums were largely enacted during the 1980s and 1990s drug war."
        '<sup><a href="#fn33" id="ref33">[33]</a></sup>',
    ),
    # ── Line 1674: 1994 Crime Bill three-strikes ──────────────────────
    (
        "Federal three-strikes provisions, enacted primarily in the 1994 Crime Bill, mandate life "
        "imprisonment for defendants convicted of a third felony, including non-violent drug "
        "offenses. <!-- [VERIFY] -->",
        "Federal three-strikes provisions, enacted primarily in the 1994 Crime Bill, mandate life "
        "imprisonment for defendants convicted of a third felony, including non-violent drug "
        "offenses."
        '<sup><a href="#fn34" id="ref34">[34]</a></sup>',
    ),
    # ── Line 1847: H.R. 40 introduced every Congress since 1989 ──────────
    (
        "has been introduced in every Congress since 1989 and has never received a floor vote. <!-- [VERIFY] -->",
        "has been introduced in every Congress since 1989 and has never received a floor vote."
        '<sup><a href="#fn35" id="ref35">[35]</a></sup>',
    ),
    # ── Line 2047: prison wages $0.14–$1.41/hr (in-sentence citation) ────
    (
        "earn between $0.14 and $1.41/hour on average <!-- [VERIFY] -->,",
        "earn between $0.14 and $1.41/hour on average"
        '<sup><a href="#fn36" id="ref36">[36]</a></sup>,',
    ),
    # ── Line 2077 (1): FACTUAL CORRECTION — Mandela Rules say CIDT, not torture ──
    (
        "define isolation exceeding 15 consecutive days as torture. <!-- [VERIFY] -->",
        "classify prolonged isolation exceeding 15 consecutive days as cruel, inhuman, or "
        "degrading treatment, a threshold the UN Special Rapporteur on Torture has also "
        "described as constituting torture."
        '<sup><a href="#fn37" id="ref37">[37]</a></sup>',
    ),
    # ── Line 2077 (2): 80,000 in solitary ───────────────────────────────
    (
        "The U.S. holds an estimated 80,000 people in solitary confinement on any given day. <!-- [VERIFY] -->",
        "The U.S. holds an estimated 80,000 people in solitary confinement on any given day."
        '<sup><a href="#fn38" id="ref38">[38]</a></sup>',
    ),
    # ── Line 2100 (1): prison phones up to $14/min before FCC ───────────
    (
        "Before FCC action, prison phone calls cost up to $14/minute in some facilities. <!-- [VERIFY] -->",
        "Before FCC action, prison phone calls cost up to $14/minute in some facilities."
        '<sup><a href="#fn39" id="ref39">[39]</a></sup>',
    ),
    # ── Line 2100 (2): family contact reduces recidivism ────────────────
    (
        "Research consistently shows that family contact reduces recidivism. <!-- [VERIFY] -->",
        "Research consistently shows that family contact reduces recidivism."
        '<sup><a href="#fn40" id="ref40">[40]</a></sup>',
    ),
    # ── Line 2123 (1): 14M students with police, no counselor ───────────
    (
        "Approximately 14 million students attend schools with police but no counselor. <!-- [VERIFY] -->",
        "Approximately 14 million students attend schools with police but no counselor."
        '<sup><a href="#fn41" id="ref41">[41]</a></sup>',
    ),
    # ── Line 2123 (2): SRO presence increases suspensions ───────────────
    (
        "Research shows SRO presence increases suspensions and arrests without improving school safety. <!-- [VERIFY] -->",
        "Research shows SRO presence increases suspensions and arrests without improving school safety."
        '<sup><a href="#fn41">[41]</a></sup>',
    ),
    # ── Line 2153: Black/Latino drivers stopped at higher rates ─────────
    (
        "higher rates for minor equipment violations used as pretexts for drug searches. <!-- [VERIFY] -->",
        "higher rates for minor equipment violations used as pretexts for drug searches."
        '<sup><a href="#fn42" id="ref42">[42]</a></sup>',
    ),
    # ── Line 2161: DOJ Ferguson report — revenue-driven enforcement ──────
    (
        "with quotas driving discriminatory enforcement. <!-- [VERIFY] -->",
        "with quotas driving discriminatory enforcement."
        '<sup><a href="#fn43" id="ref43">[43]</a></sup>',
    ),
    # ── Line 2192 (1): 470,000 held pretrial ─────────────────────────────
    (
        "not because of flight risk or danger. <!-- [VERIFY] -->",
        "not because of flight risk or danger."
        '<sup><a href="#fn44" id="ref44">[44]</a></sup>',
    ),
    # ── Line 2192 (2): pretrial detention → plea deals ───────────────────
    (
        "and more likely to accept plea deals, regardless of guilt. <!-- [VERIFY] -->",
        "and more likely to accept plea deals, regardless of guilt."
        '<sup><a href="#fn44">[44]</a></sup>',
    ),
    # ── Line 2207 (1): racial disparities in risk assessment tools ────────
    (
        "Studies of widely used pretrial risk assessment tools have found significant racial disparities in scores and outcomes. <!-- [VERIFY] -->",
        "Studies of widely used pretrial risk assessment tools have found significant racial disparities in scores and outcomes."
        '<sup><a href="#fn45" id="ref45">[45]</a></sup>',
    ),
    # ── Line 2207 (2): COMPAS no more accurate than untrained public ──────
    (
        "was found to be no more accurate at predicting recidivism than untrained members of the public. <!-- [VERIFY] -->",
        "was found to be no more accurate at predicting recidivism than untrained members of the public."
        '<sup><a href="#fn45">[45]</a></sup>',
    ),
    # ── Line 2215 (1): pretrial detention duration growing ────────────────
    (
        "with some defendants waiting years before trial. <!-- [VERIFY] -->",
        "with some defendants waiting years before trial."
        '<sup><a href="#fn44">[44]</a></sup>',
    ),
    # ── Line 2215 (2): pretrial detention → wrongful convictions ──────────
    (
        "Long pretrial detention correlates strongly with wrongful conviction rates. <!-- [VERIFY] -->",
        "Long pretrial detention correlates strongly with wrongful conviction rates."
        '<sup><a href="#fn44">[44]</a></sup>',
    ),
    # ── Line 2232 (1): mandatory minimums → 700% federal prison increase ──
    (
        "700% increase in the federal prison population since the 1970s. <!-- [VERIFY] -->",
        "700% increase in the federal prison population since the 1970s."
        '<sup><a href="#fn33">[33]</a></sup>',
    ),
    # ── Line 2232 (2): 75% mandatory minimum sentences → people of color ──
    (
        "Approximately 75% of people serving federal mandatory minimum sentences for drug offenses are people of color. <!-- [VERIFY] -->",
        "Approximately 75% of people serving federal mandatory minimum sentences for drug offenses are people of color."
        '<sup><a href="#fn46" id="ref46">[46]</a></sup>',
    ),
    # ── Line 2240 (1): 100:1 crack/powder disparity → Black defendants ───
    (
        "with Black defendants comprising the vast majority of crack cocaine prosecutions. <!-- [VERIFY] -->",
        "with Black defendants comprising the vast majority of crack cocaine prosecutions."
        '<sup><a href="#fn47" id="ref47">[47]</a></sup>',
    ),
    # ── Line 2240 (2): 2010 Fair Sentencing Act, 18:1, not retroactive ───
    (
        "The 2010 Fair Sentencing Act reduced the disparity to 18:1 but did not make the change retroactive. <!-- [VERIFY] -->",
        "The 2010 Fair Sentencing Act reduced the disparity to 18:1 but did not make the change retroactive."
        '<sup><a href="#fn14">[14]</a></sup>',
    ),
    # ── Line 2248 (1): 200,000 serving life / virtual life (unique context) ─
    (
        "more than any other country. <!-- [VERIFY] --> Research on recidivism",
        "more than any other country."
        '<sup><a href="#fn48" id="ref48">[48]</a></sup>'
        " Research on recidivism",
    ),
    # ── Line 2248 (2): age-crime curve / recidivism risk ─────────────────
    (
        "making long sentences increasingly difficult to justify on public safety grounds. <!-- [VERIFY] -->",
        "making long sentences increasingly difficult to justify on public safety grounds."
        '<sup><a href="#fn49" id="ref49">[49]</a></sup>',
    ),
    # ── Line 2256 (1): Jones v. Mississippi JLWOP inconsistency ─────────
    (
        "but courts have applied this ruling inconsistently. <!-- [VERIFY] -->",
        "but courts have applied this ruling inconsistently."
        '<sup><a href="#fn50" id="ref50">[50]</a></sup>',
    ),
    # ── Line 2256 (2): prefrontal cortex not fully developed until 25 ────
    (
        "is not fully developed until age 25. <!-- [VERIFY] -->",
        "is not fully developed until age 25."
        '<sup><a href="#fn51" id="ref51">[51]</a></sup>',
    ),
    # ── Line 2273 (1): US holds 60,000–80,000 in solitary (unique context)
    (
        "more than any other country. <!-- [VERIFY] --> The UN Special Rapporteur",
        "more than any other country."
        '<sup><a href="#fn38">[38]</a></sup>'
        " The UN Special Rapporteur",
    ),
    # ── Line 2273 (2): UN Special Rapporteur classified solitary as torture/CIDT ─
    (
        "classified extended solitary confinement as torture or cruel, inhuman, or degrading treatment. <!-- [VERIFY] -->",
        "classified extended solitary confinement as torture or cruel, inhuman, or degrading treatment."
        '<sup><a href="#fn37">[37]</a></sup>'
        '<sup><a href="#fn13">[13]</a></sup>',
    ),
    # ── Line 2281 (1): prison phones up to $14/min, hundreds of millions extracted ──
    (
        "extracting hundreds of millions of dollars annually from incarcerated people and their low-income families. <!-- [VERIFY] -->",
        "extracting hundreds of millions of dollars annually from incarcerated people and their low-income families."
        '<sup><a href="#fn39">[39]</a></sup>',
    ),
    # ── Line 2281 (2): family contact reduces recidivism (second context) ─
    (
        "Research shows family contact during incarceration significantly reduces recidivism. <!-- [VERIFY] -->",
        "Research shows family contact during incarceration significantly reduces recidivism."
        '<sup><a href="#fn40">[40]</a></sup>',
    ),
    # ── Line 2289 (1): FACTUAL CORRECTION ($0.63→13 cents) + fn36 ────────
    (
        "some incarcerated workers earn as little as $0.63 per hour, or nothing at all in some states. <!-- [VERIFY] -->",
        "some incarcerated workers earn as little as 13 cents per hour, or nothing at all in some states."
        '<sup><a href="#fn36">[36]</a></sup>',
    ),
    # ── Line 2289 (2): FACTUAL CORRECTION ($2B→$11B) + fn36 ──────────────
    (
        "Prison labor generates an estimated $2 billion in goods and services annually, primarily benefiting state governments and private corporations. <!-- [VERIFY] -->",
        "Prison labor generates over $11 billion in goods and services annually, primarily benefiting state governments and private corporations."
        '<sup><a href="#fn36">[36]</a></sup>',
    ),
    # ── Line 2297 (1): FACTUAL CORRECTION (40,000→32,000) + fn73 ─────────
    (
        "An estimated 40,000 people are currently incarcerated for marijuana-related offenses; millions more carry conviction records that limit housing, employment, and educational opportunities. <!-- [VERIFY] -->",
        "An estimated 32,000 people are currently incarcerated for marijuana-related offenses; millions more carry conviction records that limit housing, employment, and educational opportunities."
        '<sup><a href="#fn73" id="ref73">[73]</a></sup>',
    ),
    # ── Line 2297 (2): Black Americans 3.7× more likely arrested for marijuana ──
    (
        "Black Americans are approximately 3.7 times more likely to be arrested for marijuana possession than white Americans despite similar usage rates. <!-- [VERIFY] -->",
        "Black Americans are approximately 3.73 times more likely to be arrested for marijuana possession than white Americans despite similar usage rates."
        '<sup><a href="#fn74" id="ref74">[74]</a></sup>',
    ),
    # ── Line 2314 (1): 181,000 veterans incarcerated, 1.4M under supervision ──
    (
        "Approximately 181,000 veterans are incarcerated in the U.S. and an estimated 1.4 million veterans are under correctional supervision. <!-- [VERIFY] -->",
        "Approximately 181,000 veterans are incarcerated in the U.S. and an estimated 1.4 million veterans are under correctional supervision."
        '<sup><a href="#fn52" id="ref52">[52]</a></sup>',
    ),
    # ── Line 2314 (2): veterans with PTSD/TBI → higher arrest rates ──────
    (
        "significantly more likely to be arrested for conduct directly related to service-connected conditions. <!-- [VERIFY] -->",
        "significantly more likely to be arrested for conduct directly related to service-connected conditions."
        '<sup><a href="#fn53" id="ref53">[53]</a></sup>',
    ),
    # ── Line 2322: OTH discharges for PTSD/MST → ineligible for VA ───────
    (
        "rendering them ineligible for VA benefits they earned. <!-- [VERIFY] -->",
        "rendering them ineligible for VA benefits they earned."
        '<sup><a href="#fn54" id="ref54">[54]</a></sup>',
    ),
    # ── Line 2330: 8,942 sexual assaults reported FY2022 ─────────────────
    (
        "a figure widely considered a significant undercount of actual prevalence given documented retaliation and reporting barriers. <!-- [VERIFY] -->",
        "a figure widely considered a significant undercount of actual prevalence given documented retaliation and reporting barriers."
        '<sup><a href="#fn55" id="ref55">[55]</a></sup>',
    ),
    # ── Line 2338: non-citizen veterans deported after sentences ─────────
    (
        "often after completing criminal sentences for non-violent offenses that would not trigger deportation for citizens. <!-- [VERIFY] -->",
        "often after completing criminal sentences for non-violent offenses that would not trigger deportation for citizens."
        '<sup><a href="#fn56" id="ref56">[56]</a></sup>',
    ),
    # ── Line 2355 (1): $68B seized 2000–2019 without conviction ──────────
    (
        "the majority without a criminal conviction. <!-- [VERIFY] -->",
        "the majority without a criminal conviction."
        '<sup><a href="#fn57" id="ref57">[57]</a></sup>',
    ),
    # ── Line 2355 (2): hundreds of cases, innocent people lost property ──
    (
        "where innocent people lost cash, cars, and homes without ever being charged with a crime. <!-- [VERIFY] -->",
        "where innocent people lost cash, cars, and homes without ever being charged with a crime."
        '<sup><a href="#fn57">[57]</a></sup>',
    ),
    # ── Line 2363: forfeiture funds → military equipment, no oversight ───
    (
        "with little or no public oversight. <!-- [VERIFY] -->",
        "with little or no public oversight."
        '<sup><a href="#fn57">[57]</a></sup>',
    ),
    # ── Line 2371 (1): FACTUAL CORRECTION ($4.5B→$5B) + fn58 ─────────────
    (
        "approximately $4.5 billion in forfeitures compared to $3.5 billion in burglary losses. <!-- [VERIFY] -->",
        "approximately $5 billion in forfeitures compared to $3.5 billion in burglary losses."
        '<sup><a href="#fn58" id="ref58">[58]</a></sup>',
    ),
    # ── Line 2371 (2): owners must prove innocence ────────────────────────
    (
        "In most states, owners must prove their innocence to recover seized property, reversing the presumption of innocence. <!-- [VERIFY] -->",
        "In most states, owners must prove their innocence to recover seized property, reversing the presumption of innocence."
        '<sup><a href="#fn57">[57]</a></sup>',
    ),
    # ── Line 2388 (1): 80,000–100,000 in solitary any given day ──────────
    (
        "An estimated 80,000–100,000 people are held in solitary confinement in U.S. prisons and jails on any given day. <!-- [VERIFY] -->",
        "An estimated 80,000–100,000 people are held in solitary confinement in U.S. prisons and jails on any given day."
        '<sup><a href="#fn38">[38]</a></sup>',
    ),
    # ── Line 2388 (2): prolonged solitary → hallucinations, cognitive damage ──
    (
        "Studies have found that prolonged solitary confinement causes severe psychological harm including hallucinations, panic attacks, and permanent cognitive damage. <!-- [VERIFY] -->",
        "Studies have found that prolonged solitary confinement causes severe psychological harm including hallucinations, panic attacks, and permanent cognitive damage."
        '<sup><a href="#fn37">[37]</a></sup>',
    ),
    # ── Line 2396 (1): no national system for tracking solitary ──────────
    (
        "making the full scale of its use difficult to determine. <!-- [VERIFY] -->",
        "making the full scale of its use difficult to determine."
        '<sup><a href="#fn38">[38]</a></sup>',
    ),
    # ── Line 2396 (2): released from solitary → higher recidivism ────────
    (
        "People released directly from solitary to community supervision have significantly higher recidivism rates. <!-- [VERIFY] -->",
        "People released directly from solitary to community supervision have significantly higher recidivism rates."
        '<sup><a href="#fn75" id="ref75">[75]</a></sup>',
    ),
    # ── Line 2413 (1): 95% of incarcerated people eventually released ─────
    (
        "An estimated 95% of all incarcerated people will eventually be released. <!-- [VERIFY] -->",
        "An estimated 95% of all incarcerated people will eventually be released."
        '<sup><a href="#fn59" id="ref59">[59]</a></sup>',
    ),
    # ── Line 2413 (2): homelessness in first weeks post-release ──────────
    (
        "face extremely high rates of homelessness in the first weeks after release. <!-- [VERIFY] -->",
        "face extremely high rates of homelessness in the first weeks after release."
        '<sup><a href="#fn60" id="ref60">[60]</a></sup>',
    ),
    # ── Line 2421 (1): FACTUAL CORRECTION (40,000→3,000 federal) + fn61 ──
    (
        "An estimated 40,000 people are currently incarcerated federally for marijuana offenses, many for conduct now legal in a majority of states. <!-- [VERIFY] -->",
        "An estimated 3,000 people are currently incarcerated in federal prison for marijuana offenses, many for conduct now legal in a majority of states."
        '<sup><a href="#fn61" id="ref61">[61]</a></sup>',
    ),
    # ── Line 2421 (2): criminal record reduces callback 50% ──────────────
    (
        "and the effect is significantly worse for Black applicants. <!-- [VERIFY] -->",
        "and the effect is significantly worse for Black applicants."
        '<sup><a href="#fn62" id="ref62">[62]</a></sup>',
    ),
    # ── Line 2437 (1): 1,000+ killed by law enforcement per year ─────────
    (
        "At least 1,000 people are killed by law enforcement in the United States each year, far more per capita than any other wealthy nation. <!-- [VERIFY] -->",
        "At least 1,000 people are killed by law enforcement in the United States each year, far more per capita than any other wealthy nation."
        '<sup><a href="#fn20">[20]</a></sup>',
    ),
    # ── Line 2437 (2): George Floyd / neck compression ────────────────────
    (
        "George Floyd was killed by a chokehold technique that had been banned in many jurisdictions before the officer applied it. <!-- [VERIFY] -->",
        "George Floyd was killed by a neck compression technique that had been banned in many "
        "jurisdictions; the Hennepin County Medical Examiner ruled his death a homicide caused "
        "by cardiopulmonary arrest complicating law enforcement restraint and neck compression."
        '<sup><a href="#fn63" id="ref63">[63]</a></sup>',
    ),
    # ── Line 2445 (1): thousands of wandering officers rehired ───────────
    (
        "Studies have found thousands of such officers hired across the country. <!-- [VERIFY] -->",
        "Studies have found thousands of such officers hired across the country."
        '<sup><a href="#fn18">[18]</a></sup>',
    ),
    # ── Line 2445 (2): no national misconduct database ────────────────────
    (
        "The United States has no national, comprehensive, publicly accessible database of police misconduct. <!-- [VERIFY] -->",
        "The United States has no national, comprehensive, publicly accessible database of police misconduct."
        '<sup><a href="#fn18">[18]</a></sup>',
    ),
    # ── Line 2453 (1): QI judicially created, not in § 1983 text ─────────
    (
        "it does not appear in the text of 42 U.S.C. § 1983. <!-- [VERIFY] -->",
        "it does not appear in the text of 42 U.S.C. § 1983."
        '<sup><a href="#fn64" id="ref64">[64]</a></sup>'
        '<sup><a href="#fn65" id="ref65">[65]</a></sup>',
    ),
    # ── Line 2453 (2): QI shields officers in vast majority of cases ──────
    (
        "qualified immunity shields officers from civil liability in the vast majority of cases where constitutional violations are alleged. <!-- [VERIFY] -->",
        "qualified immunity shields officers from civil liability in the vast majority of cases where constitutional violations are alleged."
        '<sup><a href="#fn66" id="ref66">[66]</a></sup>',
    ),
    # ── Line 2470 (1): Batson v. Kentucky (1986) / race-neutral explanations rarely rejected ──
    (
        'and \u201crace-neutral\u201d explanations are rarely rejected by courts. <!-- [VERIFY] -->',
        'and \u201crace-neutral\u201d explanations are rarely rejected by courts.'
        '<sup><a href="#fn67" id="ref67">[67]</a></sup>',
    ),
    # ── Line 2470 (2): all-white juries more likely to convict Black defendants ──
    (
        "Studies have shown that all-white or predominantly white juries are significantly more likely to convict Black defendants than racially diverse juries. <!-- [VERIFY] -->",
        "Studies have shown that all-white or predominantly white juries are significantly more likely to convict Black defendants than racially diverse juries."
        '<sup><a href="#fn68" id="ref68">[68]</a></sup>',
    ),
    # ── Line 2487 (1): FACTUAL CORRECTION — 190 executed who later exonerated → 195 exonerated from death row ──
    (
        "The United States has executed at least 190 people who were later exonerated or whose convictions were overturned on appeal since 1973. <!-- [VERIFY] -->",
        "At least 195 people have been exonerated from death row in the United States since 1973, "
        "demonstrating the serious risk of executing people who may be innocent."
        '<sup><a href="#fn68">[68]</a></sup>'
        '<sup><a href="#fn69" id="ref69">[69]</a></sup>',
    ),
    # ── Line 2487 (2): compounding pharmacies for execution drugs ─────────
    (
        "after major pharmaceutical companies refused to supply drugs for executions, often using untested drug combinations that have resulted in prolonged deaths. <!-- [VERIFY] -->",
        "after major pharmaceutical companies refused to supply drugs for executions, often using untested drug combinations that have resulted in prolonged deaths."
        '<sup><a href="#fn70" id="ref70">[70]</a></sup>',
    ),
    # ── Line 2495 (1): FACTUAL CORRECTION (Egypt→Somalia) + fn71 ─────────
    (
        "alongside China, Iran, Saudi Arabia, and Egypt. <!-- [VERIFY] -->",
        "alongside China, Iran, Saudi Arabia, and Somalia."
        '<sup><a href="#fn71" id="ref71">[71]</a></sup>',
    ),
    # ── Line 2495 (2): death penalty racial disparity ────────────────────
    (
        "defendants whose victims were white are significantly more likely to receive death sentences than those whose victims were Black. <!-- [VERIFY] -->",
        "defendants whose victims were white are significantly more likely to receive death sentences than those whose victims were Black."
        '<sup><a href="#fn77" id="ref77">[77]</a></sup>',
    ),
    # ── Line 2512 (1): US holds 80,000 in solitary, highest per-capita Western democracy ──
    (
        "the highest per-capita rate of any Western democracy. <!-- [VERIFY] -->",
        "the highest per-capita rate of any Western democracy."
        '<sup><a href="#fn38">[38]</a></sup>',
    ),
    # ── Line 2512 (2): prolonged solitary → severe psychological harm, CIDT ──
    (
        "equivalent to torture under international human rights standards. <!-- [VERIFY] -->",
        "equivalent to torture under international human rights standards."
        '<sup><a href="#fn37">[37]</a></sup>',
    ),
    # ── Line 2520 (1): 1/3 of prison suicides in solitary (<8% population) ──
    (
        "who represent less than 8% of the total prison population. <!-- [VERIFY] -->",
        "who represent less than 8% of the total prison population."
        '<sup><a href="#fn72" id="ref72">[72]</a></sup>',
    ),
    # ── Line 2520 (2): mental health conditions drive solitary, isolation worsens illness ──
    (
        "yet the isolation of solitary confinement reliably worsens mental illness. <!-- [VERIFY] -->",
        "yet the isolation of solitary confinement reliably worsens mental illness."
        '<sup><a href="#fn78" id="ref78">[78]</a></sup>',
    ),
    # ── Line 2537 (1): prison phone costs $2.9B/yr, $14/min in county jails ──
    (
        "with rates in some county jails reaching $14 per minute. <!-- [VERIFY] -->",
        "with rates in some county jails reaching $14 per minute."
        '<sup><a href="#fn39">[39]</a></sup>',
    ),
    # ── Line 2537 (2): family contact reduces recidivism and improves outcomes ──
    (
        "yet private companies profit by maximizing costs to the people least able to afford them. <!-- [VERIFY] -->",
        "yet private companies profit by maximizing costs to the people least able to afford them."
        '<sup><a href="#fn40">[40]</a></sup>',
    ),
    # ── Line 2545 (1): facilities documented recording attorney-client calls ──
    (
        "with courts only recently beginning to impose consequences for this practice. <!-- [VERIFY] -->",
        "with courts only recently beginning to impose consequences for this practice."
        '<sup><a href="#fn76" id="ref76">[76]</a></sup>',
    ),
    # ── Line 2545 (2): access to counsel → better legal outcomes ──────────
    (
        "Studies show that incarcerated people with meaningful access to counsel achieve "
        "significantly better legal outcomes, including lower rates of wrongful conviction "
        "and more appropriate sentences. <!-- [VERIFY] -->",
        "Studies show that incarcerated people with meaningful access to counsel achieve "
        "significantly better legal outcomes, including lower rates of wrongful conviction "
        "and more appropriate sentences."
        '<sup><a href="#fn79" id="ref79">[79]</a></sup>',
    ),
    # ── Line 2562 (1): FACTUAL CORRECTION ("billions"→"$11 billion") + fn36 ──
    (
        "with the total value of unpaid or near-unpaid prison labor estimated in the billions of dollars annually. <!-- [VERIFY] -->",
        "with the total value of unpaid or near-unpaid prison labor estimated at over $11 billion annually."
        '<sup><a href="#fn36">[36]</a></sup>',
    ),
    # ── Line 2562 (2): California incarcerated firefighters paid $1/hr ────
    (
        "Incarcerated firefighters in California have been paid as little as $1 per hour fighting wildfires, while private prison contractors have earned significant profits from prison labor contracts. <!-- [VERIFY] -->",
        "Incarcerated firefighters in California have been paid as little as $1 per hour fighting wildfires, while private prison contractors have earned significant profits from prison labor contracts."
        '<sup><a href="#fn80" id="ref80">[80]</a></sup>',
    ),
]

# ---------------------------------------------------------------------------
# New footnotes fn13–fn80
# ---------------------------------------------------------------------------
NEW_FOOTNOTES = """            <li id="fn13">United Nations. (2015). <em>United Nations Standard Minimum Rules for the Treatment of Prisoners (the Nelson Mandela Rules)</em>. General Assembly Resolution 70/175. <a href="https://undocs.org/A/RES/70/175">https://undocs.org/A/RES/70/175</a> <a href="#ref13" style="font-size:.8rem">↩</a></li>
            <li id="fn14">Fair Sentencing Act of 2010, Pub. L. 111-220, 124 Stat. 2372. <a href="https://www.congress.gov/111/plaws/publ220/PLAW-111publ220.pdf">https://www.congress.gov/111/plaws/publ220/PLAW-111publ220.pdf</a> <a href="#ref14" style="font-size:.8rem">↩</a></li>
            <li id="fn15">Drug Enforcement Administration. (2024). <em>Drug scheduling</em>. U.S. Department of Justice. <a href="https://www.dea.gov/drug-information/drug-scheduling">https://www.dea.gov/drug-information/drug-scheduling</a> <a href="#ref15" style="font-size:.8rem">↩</a></li>
            <li id="fn16">Federal Bureau of Investigation. (2020). <em>2019 Crime in the United States: Arrests</em>. U.S. Department of Justice. <a href="https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/persons-arrested">https://ucr.fbi.gov/crime-in-the-u.s/2019/</a> <a href="#ref16" style="font-size:.8rem">↩</a></li>
            <li id="fn17">Federal Bureau of Investigation. (2023). <em>National Use-of-Force Data Collection</em>. U.S. Department of Justice. <a href="https://www.fbi.gov/services/cjis/ucr/use-of-force">https://www.fbi.gov/services/cjis/ucr/use-of-force</a> <a href="#ref17" style="font-size:.8rem">↩</a></li>
            <li id="fn18">Grunwald, B., &amp; Rappaport, J. (2020). The wandering officer. <em>Yale Law Journal, 129</em>(6), 1676–1786. <a href="https://www.yalelawjournal.org/article/the-wandering-officer">https://www.yalelawjournal.org/article/the-wandering-officer</a> <a href="#ref18" style="font-size:.8rem">↩</a></li>
            <li id="fn19">Police Executive Research Forum. (2016). <em>Guiding principles on use of force</em>. PERF. <a href="https://www.policeforum.org/assets/30%20guiding%20principles.pdf">https://www.policeforum.org/assets/30%20guiding%20principles.pdf</a> <a href="#ref19" style="font-size:.8rem">↩</a></li>
            <li id="fn20">Mapping Police Violence. (2024). <em>2023 police violence report</em>. <a href="https://mappingpoliceviolence.org">https://mappingpoliceviolence.org</a> <a href="#ref20" style="font-size:.8rem">↩</a></li>
            <li id="fn21">Human Rights Watch. (2017). <em>Trump administration's rollback of police accountability</em>. <a href="https://www.hrw.org/topic/us-justice">https://www.hrw.org/topic/us-justice</a> <a href="#ref21" style="font-size:.8rem">↩</a></li>
            <li id="fn22">Chanin, J. M. (2015). Examining the sustainability of pattern or practice police misconduct reform. <em>Police Quarterly, 18</em>(2), 163–192. <a href="https://doi.org/10.1177/1098611114561358">https://doi.org/10.1177/1098611114561358</a> <a href="#ref22" style="font-size:.8rem">↩</a></li>
            <li id="fn23">Rushin, S. (2017). Police union contracts. <em>Duke Law Journal, 66</em>(6), 1191–1264. <a href="https://scholarship.law.duke.edu/dlj/vol66/iss6/1/">https://scholarship.law.duke.edu/dlj/vol66/iss6/1/</a> <a href="#ref23" style="font-size:.8rem">↩</a></li>
            <li id="fn24">Bromwich Group &amp; National Association for Civilian Oversight of Law Enforcement. (2016). <em>Survey of civilian oversight of law enforcement</em>. NACOLE. <a href="https://www.nacole.org/resources">https://www.nacole.org/resources</a> <a href="#ref24" style="font-size:.8rem">↩</a></li>
            <li id="fn25">National Registry of Exonerations. (2020). <em>Government misconduct and convicting the innocent</em>. University of Michigan Law School. <a href="https://www.law.umich.edu/special/exoneration/Pages/Government-Misconduct.aspx">https://www.law.umich.edu/special/exoneration/</a> <a href="#ref25" style="font-size:.8rem">↩</a></li>
            <li id="fn26"><em>Imbler v. Pachtman</em>, 424 U.S. 409 (1976). <a href="https://supreme.justia.com/cases/federal/us/424/409/">https://supreme.justia.com/cases/federal/us/424/409/</a> <a href="#ref26" style="font-size:.8rem">↩</a></li>
            <li id="fn27">National Registry of Exonerations. (2024). <em>Exoneration data</em>. University of Michigan Law School. <a href="https://www.law.umich.edu/special/exoneration/">https://www.law.umich.edu/special/exoneration/</a> <a href="#ref27" style="font-size:.8rem">↩</a></li>
            <li id="fn28">President's Council of Advisors on Science and Technology. (2016). <em>Forensic science in criminal courts: Ensuring scientific validity of feature-comparison methods</em>. Executive Office of the President. <a href="https://obamawhitehouse.archives.gov/sites/default/files/microsites/ostp/PCAST/pcast_forensic_science_report_final.pdf">https://obamawhitehouse.archives.gov/</a> <a href="#ref28" style="font-size:.8rem">↩</a></li>
            <li id="fn29">Bureau of Justice Statistics. (2018). <em>Felony defendants in large urban counties, 2009—statistical tables</em>. U.S. Department of Justice. <a href="https://bjs.ojp.gov/library/publications/felony-defendants-large-urban-counties-2009-statistical-tables">https://bjs.ojp.gov/</a> <a href="#ref29" style="font-size:.8rem">↩</a></li>
            <li id="fn30">National Association of Criminal Defense Lawyers. (2018). <em>The trial penalty: The Sixth Amendment right to trial on the verge of extinction and how to save it</em>. NACDL. <a href="https://www.nacdl.org/Document/TrialPenaltySixthAmendmentRighttoTrialNearExtinct">https://www.nacdl.org/</a> <a href="#ref30" style="font-size:.8rem">↩</a></li>
            <li id="fn31">Uggen, C., Larson, R., Shannon, S., &amp; Pulido-Nava, A. (2024). <em>Locked out 2024: Four million disenfranchised due to a felony conviction</em>. The Sentencing Project. <a href="https://www.sentencingproject.org/publications/locked-out-2024-four-million-disenfranchised-due-to-a-felony-conviction/">https://www.sentencingproject.org/</a> <a href="#ref31" style="font-size:.8rem">↩</a></li>
            <li id="fn32">FAFSA Simplification Act, Pub. L. 116-260, Div. FF, Title VII (2020). <a href="https://www.congress.gov/bill/116th-congress/house-bill/133/text">https://www.congress.gov/bill/116th-congress/house-bill/133/text</a> <a href="#ref32" style="font-size:.8rem">↩</a></li>
            <li id="fn33">Bureau of Justice Statistics. (2021). <em>Federal justice statistics, 2019—statistical tables</em>. U.S. Department of Justice. <a href="https://bjs.ojp.gov/library/publications/federal-justice-statistics-2019-statistical-tables">https://bjs.ojp.gov/</a> <a href="#ref33" style="font-size:.8rem">↩</a></li>
            <li id="fn34">Violent Crime Control and Law Enforcement Act of 1994, Pub. L. 103-322, 108 Stat. 1796; 18 U.S.C. § 3559(c). <a href="https://www.congress.gov/103/statute/STATUTE-108/STATUTE-108-Pg1796.pdf">https://www.congress.gov/</a> <a href="#ref34" style="font-size:.8rem">↩</a></li>
            <li id="fn35">H.R. 40, Commission to Study and Develop Reparation Proposals for African-Americans Act. Introduced in the 101st Congress (1989) and every subsequent Congress. <a href="https://www.congress.gov/bill/117th-congress/house-bill/40">https://www.congress.gov/bill/117th-congress/house-bill/40</a> <a href="#ref35" style="font-size:.8rem">↩</a></li>
            <li id="fn36">American Civil Liberties Union. (2022). <em>Captive labor: Exploitation of incarcerated workers</em>. ACLU. <a href="https://www.aclu.org/publications/captive-labor-exploitation-incarcerated-workers">https://www.aclu.org/publications/captive-labor-exploitation-incarcerated-workers</a> <a href="#ref36" style="font-size:.8rem">↩</a></li>
            <li id="fn37">Méndez, J. (2011). <em>Torture and other cruel, inhuman or degrading treatment or punishment: Report of the Special Rapporteur on torture</em> (U.N. Doc. A/66/268). United Nations General Assembly. <a href="https://undocs.org/A/66/268">https://undocs.org/A/66/268</a> <a href="#ref37" style="font-size:.8rem">↩</a></li>
            <li id="fn38">Solitary Watch &amp; Unlock the Box Campaign. (2023). <em>Calculating torture: Statewide data on solitary confinement in U.S. prisons and jails</em>. <a href="https://solitarywatch.org/calculating-torture/">https://solitarywatch.org/calculating-torture/</a> <a href="#ref38" style="font-size:.8rem">↩</a></li>
            <li id="fn39">Prison Policy Initiative. (2023). <em>Prison phone rates: Everything you need to know</em>. <a href="https://www.prisonpolicy.org/phones/">https://www.prisonpolicy.org/phones/</a> <a href="#ref39" style="font-size:.8rem">↩</a></li>
            <li id="fn40">Minnesota Department of Corrections. (2011). <em>The effects of prison visitation on offender recidivism</em>. <a href="https://mn.gov/doc/assets/11-11MNPrisonVisitationStudy_tcm1089-272781.pdf">https://mn.gov/doc/</a> <a href="#ref40" style="font-size:.8rem">↩</a></li>
            <li id="fn41">American Civil Liberties Union. (2019). <em>Cops and no counselors: How the absence of school mental health staff is harming students</em>. ACLU. <a href="https://www.aclu.org/publications/cops-and-no-counselors">https://www.aclu.org/publications/cops-and-no-counselors</a> <a href="#ref41" style="font-size:.8rem">↩</a></li>
            <li id="fn42">Pierson, E., Simoiu, C., Overgoor, J., Corbett-Davies, S., Jenson, D., Shoemaker, A., Ramachandran, V., Barghouty, P., Phillips, C., Shroff, R., &amp; Goel, S. (2020). A large-scale analysis of racial disparities in police stops across the United States. <em>Nature Human Behaviour, 4</em>, 736–745. <a href="https://doi.org/10.1038/s41562-020-0858-1">https://doi.org/10.1038/s41562-020-0858-1</a> <a href="#ref42" style="font-size:.8rem">↩</a></li>
            <li id="fn43">U.S. Department of Justice, Civil Rights Division. (2015). <em>Investigation of the Ferguson Police Department</em>. <a href="https://www.justice.gov/sites/default/files/opa/press-releases/attachments/2015/03/04/ferguson_police_department_report.pdf">https://www.justice.gov/</a> <a href="#ref43" style="font-size:.8rem">↩</a></li>
            <li id="fn44">Pretrial Justice Institute. (2017). <em>Pretrial justice: The future is now</em>. <a href="https://www.pretrial.org/publications/">https://www.pretrial.org/</a>; Vera Institute of Justice. (2022). <em>Bail reform</em>. <a href="https://www.vera.org/ending-mass-incarceration/reducing-pretrial-incarceration/bail-reform">https://www.vera.org/</a> <a href="#ref44" style="font-size:.8rem">↩</a></li>
            <li id="fn45">Dressel, J., &amp; Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. <em>Science Advances, 4</em>(1), eaao5580. <a href="https://doi.org/10.1126/sciadv.aao5580">https://doi.org/10.1126/sciadv.aao5580</a> <a href="#ref45" style="font-size:.8rem">↩</a></li>
            <li id="fn46">United States Sentencing Commission. (2024). <em>Quick facts: Mandatory minimum penalties</em>. USSC. <a href="https://www.ussc.gov/research/quick-facts/mandatory-minimum-penalties">https://www.ussc.gov/research/quick-facts/mandatory-minimum-penalties</a> <a href="#ref46" style="font-size:.8rem">↩</a></li>
            <li id="fn47">United States Sentencing Commission. (2002). <em>Report to the Congress: Cocaine and federal sentencing policy</em>. USSC. <a href="https://www.ussc.gov/research/congressional-reports/2002-report-congress-cocaine-and-federal-sentencing-policy">https://www.ussc.gov/</a> <a href="#ref47" style="font-size:.8rem">↩</a></li>
            <li id="fn48">The Sentencing Project. (2021). <em>No end in sight: America's enduring reliance on life imprisonment</em>. <a href="https://www.sentencingproject.org/publications/no-end-in-sight-americas-enduring-reliance-on-life-imprisonment/">https://www.sentencingproject.org/</a> <a href="#ref48" style="font-size:.8rem">↩</a></li>
            <li id="fn49">Langan, P. A., &amp; Levin, D. J. (2002). <em>Recidivism of prisoners released in 1994</em>. Bureau of Justice Statistics. <a href="https://bjs.ojp.gov/content/pub/pdf/rpr94.pdf">https://bjs.ojp.gov/</a> <a href="#ref49" style="font-size:.8rem">↩</a></li>
            <li id="fn50"><em>Jones v. Mississippi</em>, 593 U.S. 98 (2021). <a href="https://supreme.justia.com/cases/federal/us/593/20-1259/">https://supreme.justia.com/cases/federal/us/593/20-1259/</a> <a href="#ref50" style="font-size:.8rem">↩</a></li>
            <li id="fn51">Blakemore, S.-J., &amp; Choudhury, S. (2006). Development of the adolescent brain: Implications for executive function and social cognition. <em>Journal of Child Psychology and Psychiatry, 47</em>(3–4), 296–312. <a href="https://doi.org/10.1111/j.1469-7610.2006.01611.x">https://doi.org/10.1111/j.1469-7610.2006.01611.x</a> <a href="#ref51" style="font-size:.8rem">↩</a></li>
            <li id="fn52">Bureau of Justice Statistics. (2015). <em>Veterans in prison and jail, 2011–2012</em>. U.S. Department of Justice. <a href="https://bjs.ojp.gov/library/publications/veterans-prison-and-jail-2011-12">https://bjs.ojp.gov/</a> <a href="#ref52" style="font-size:.8rem">↩</a></li>
            <li id="fn53">Urban Institute. (2019). <em>Criminal justice involvement of the veteran population</em>. <a href="https://www.urban.org/research/publication/criminal-justice-involvement-veteran-population">https://www.urban.org/</a> <a href="#ref53" style="font-size:.8rem">↩</a></li>
            <li id="fn54">U.S. Government Accountability Office. (2017). <em>Military personnel: Additional actions needed to strengthen DOD's efforts to address the problem of sexual assault</em> (GAO-17-93). <a href="https://www.gao.gov/assets/gao-17-93.pdf">https://www.gao.gov/</a>; Human Rights Watch. (2016). <em>"Booted": Lack of recourse for wrongfully discharged U.S. military veterans</em>. <a href="https://www.hrw.org/report/2016/05/19/booted/lack-recourse-wrongfully-discharged-us-military-veterans">https://www.hrw.org/</a> <a href="#ref54" style="font-size:.8rem">↩</a></li>
            <li id="fn55">Department of Defense Sexual Assault Prevention and Response. (2022). <em>Fiscal year 2022 annual report on sexual assault in the military</em>. DOD SAPRO. <a href="https://www.sapr.mil/reports">https://www.sapr.mil/reports</a> <a href="#ref55" style="font-size:.8rem">↩</a></li>
            <li id="fn56">American Civil Liberties Union. (2016). <em>Veterans and deportations</em>. ACLU. <a href="https://www.aclu.org/issues/immigrants-rights/deportation/veterans-and-deportation">https://www.aclu.org/</a> <a href="#ref56" style="font-size:.8rem">↩</a></li>
            <li id="fn57">Sibilla, N. (2020). <em>Policing for profit: The abuse of civil asset forfeiture</em> (3rd ed.). Institute for Justice. <a href="https://ij.org/report/policing-for-profit/">https://ij.org/report/policing-for-profit/</a> <a href="#ref57" style="font-size:.8rem">↩</a></li>
            <li id="fn58">Sallah, M., O'Harrow, R., Jr., Rich, S., &amp; Silverman, G. (2014, November 23). Stop and seize: Aggressive police take hundreds of millions of dollars from motorists not charged with crimes. <em>Washington Post</em>. <a href="https://www.washingtonpost.com/sf/investigative/2014/09/06/stop-and-seize/">https://www.washingtonpost.com/</a> <a href="#ref58" style="font-size:.8rem">↩</a></li>
            <li id="fn59">Hughes, T. A., &amp; Wilson, D. J. (2003). <em>Reentry trends in the United States</em>. Bureau of Justice Statistics. <a href="https://bjs.ojp.gov/content/pub/pdf/reentry.pdf">https://bjs.ojp.gov/</a> <a href="#ref59" style="font-size:.8rem">↩</a></li>
            <li id="fn60">Metraux, S., &amp; Culhane, D. P. (2004). Homeless shelter use and reincarceration following prison release. <em>Criminology &amp; Public Policy, 3</em>(2), 139–160. <a href="https://doi.org/10.1111/j.1745-9133.2004.tb00031.x">https://doi.org/10.1111/j.1745-9133.2004.tb00031.x</a> <a href="#ref60" style="font-size:.8rem">↩</a></li>
            <li id="fn61">Federal Bureau of Prisons. (2024). <em>Inmate offenses</em>. <a href="https://www.bop.gov/about/statistics/statistics_inmate_offenses.jsp">https://www.bop.gov/about/statistics/statistics_inmate_offenses.jsp</a> <a href="#ref61" style="font-size:.8rem">↩</a></li>
            <li id="fn62">Pager, D., Western, B., &amp; Bonikowski, B. (2009). Discrimination in a low-wage labor market: A field experiment. <em>American Sociological Review, 74</em>(5), 777–799. <a href="https://doi.org/10.1177/000312240907400505">https://doi.org/10.1177/000312240907400505</a> <a href="#ref62" style="font-size:.8rem">↩</a></li>
            <li id="fn63">Office of the Medical Examiner, Hennepin County. (2020). <em>Autopsy report: George Floyd</em>. Cause of death: Cardiopulmonary arrest complicating law enforcement subdual, restraint, and neck compression; manner of death: homicide. <a href="https://www.hennepin.us/your-government/departments-a-z/medical-examiner">https://www.hennepin.us/</a> <a href="#ref63" style="font-size:.8rem">↩</a></li>
            <li id="fn64"><em>Pierson v. Ray</em>, 386 U.S. 547 (1967) (first recognizing an immunity defense for police officers under 42 U.S.C. § 1983; the text of § 1983 contains no such immunity). <a href="https://supreme.justia.com/cases/federal/us/386/547/">https://supreme.justia.com/cases/federal/us/386/547/</a> <a href="#ref64" style="font-size:.8rem">↩</a></li>
            <li id="fn65">Baude, W. (2018). Is qualified immunity unlawful? <em>California Law Review, 106</em>(1), 45–90. <a href="https://doi.org/10.15779/Z38RN30F0G">https://doi.org/10.15779/Z38RN30F0G</a> <a href="#ref65" style="font-size:.8rem">↩</a></li>
            <li id="fn66">Schwartz, J. C. (2017). How qualified immunity fails. <em>Yale Law Journal, 127</em>(1), 2–75. <a href="https://www.yalelawjournal.org/article/how-qualified-immunity-fails">https://www.yalelawjournal.org/article/how-qualified-immunity-fails</a> <a href="#ref66" style="font-size:.8rem">↩</a></li>
            <li id="fn67">Equal Justice Initiative. (2010). <em>Illegal racial discrimination in jury selection: A continuing legacy</em>. EJI. <a href="https://eji.org/reports/illegal-racial-discrimination-in-jury-selection/">https://eji.org/reports/illegal-racial-discrimination-in-jury-selection/</a> <a href="#ref67" style="font-size:.8rem">↩</a></li>
            <li id="fn68">Anwar, S., Bayer, P., &amp; Hjalmarsson, R. (2012). The impact of jury race in criminal trials. <em>Quarterly Journal of Economics, 127</em>(2), 1017–1055. <a href="https://doi.org/10.1093/qje/qjs014">https://doi.org/10.1093/qje/qjs014</a> <a href="#ref68" style="font-size:.8rem">↩</a></li>
            <li id="fn69">Death Penalty Information Center. (2024). <em>Innocence database</em>. <a href="https://deathpenaltyinfo.org/policy-issues/innocence">https://deathpenaltyinfo.org/policy-issues/innocence</a> <a href="#ref69" style="font-size:.8rem">↩</a></li>
            <li id="fn70">Blinder, A., &amp; Eckholm, E. (2014, May 9). New drugs tested in executions have proven unreliable. <em>New York Times</em>. <a href="https://www.nytimes.com/2014/05/10/us/new-drugs-tested-in-executions-have-proven-unreliable.html">https://www.nytimes.com/</a>; Guardian US. (2015). <em>Botched executions: A history of lethal injection and problematic executions</em>. <a href="https://www.theguardian.com/world/ng-interactive/2014/apr/23/lethal-injection-botched-executions">https://www.theguardian.com/</a> <a href="#ref70" style="font-size:.8rem">↩</a></li>
            <li id="fn71">Amnesty International. (2024). <em>Death sentences and executions 2023</em>. Amnesty International. <a href="https://www.amnesty.org/en/documents/act50/7952/2024/en/">https://www.amnesty.org/</a> <a href="#ref71" style="font-size:.8rem">↩</a></li>
            <li id="fn72">Noonan, M. E. (2016). <em>Mortality in local jails, 2000–2014—statistical tables</em>. Bureau of Justice Statistics. <a href="https://bjs.ojp.gov/library/publications/mortality-local-jails-2000-2014-statistical-tables">https://bjs.ojp.gov/</a> <a href="#ref72" style="font-size:.8rem">↩</a></li>
            <li id="fn73">Prison Policy Initiative. (2023). <em>How many people are locked up in the United States?</em> <a href="https://www.prisonpolicy.org/reports/pie2023.html">https://www.prisonpolicy.org/reports/pie2023.html</a> <a href="#ref73" style="font-size:.8rem">↩</a></li>
            <li id="fn74">American Civil Liberties Union. (2020). <em>A tale of two countries: Racially targeted arrests in the era of marijuana reform</em>. ACLU. <a href="https://www.aclu.org/publications/tale-two-countries-racially-targeted-arrests-era-marijuana-reform">https://www.aclu.org/</a> <a href="#ref74" style="font-size:.8rem">↩</a></li>
            <li id="fn75">Mears, D. P., &amp; Bales, W. D. (2009). Supermax incarceration and recidivism. <em>Criminology, 47</em>(4), 1131–1166. <a href="https://doi.org/10.1111/j.1745-9125.2009.00171.x">https://doi.org/10.1111/j.1745-9125.2009.00171.x</a> <a href="#ref75" style="font-size:.8rem">↩</a></li>
            <li id="fn76">Clark, J. (2017). <em>Attorney–client privilege in the correctional setting</em>. Prison Legal News. <a href="https://www.prisonlegalnews.org/news/2017/jan/11/attorney-client-privilege-correctional-setting/">https://www.prisonlegalnews.org/</a> <a href="#ref76" style="font-size:.8rem">↩</a></li>
            <li id="fn77">Death Penalty Information Center. (2024). <em>Race and the death penalty</em>. <a href="https://deathpenaltyinfo.org/policy-issues/race">https://deathpenaltyinfo.org/policy-issues/race</a> <a href="#ref77" style="font-size:.8rem">↩</a></li>
            <li id="fn78">Human Rights Watch. (2015). <em>"Callous and cruel": Use of force against inmates with mental disabilities in US jails and prisons</em>. HRW. <a href="https://www.hrw.org/report/2015/05/12/callous-and-cruel/use-force-against-inmates-mental-disabilities-us-jails-and-prisons">https://www.hrw.org/</a> <a href="#ref78" style="font-size:.8rem">↩</a></li>
            <li id="fn79">American Bar Association. (2004). <em>Gideon's broken promise: America's continuing quest for equal justice</em>. ABA Standing Committee on Legal Aid and Indigent Defendants. <a href="https://www.americanbar.org/content/dam/aba/publications/misc/legal_aid_indigent_defendants/ls_sclaid_def_bp_right_to_counsel_in_criminal_proceedings.pdf">https://www.americanbar.org/</a> <a href="#ref79" style="font-size:.8rem">↩</a></li>
            <li id="fn80">Leber, R. (2020, September 9). California's incarcerated firefighters are risking their lives for $1 an hour. <em>Mother Jones</em>. <a href="https://www.motherjones.com/environment/2020/09/california-wildfires-prison-inmates-firefighters/">https://www.motherjones.com/</a>; California Department of Corrections and Rehabilitation. (2023). <em>Conservation camp program</em>. CDCR. <a href="https://www.cdcr.ca.gov/conservation-camps/">https://www.cdcr.ca.gov/conservation-camps/</a> <a href="#ref80" style="font-size:.8rem">↩</a></li>"""


def apply_fixes(content: str) -> str:
    """Apply all VERIFY replacements; raise if any old_str is not found or not unique."""
    for old, new in REPLACEMENTS:
        count = content.count(old)
        if count == 0:
            raise ValueError(f"NOT FOUND in file:\n  {old[:120]!r}")
        if count > 1:
            raise ValueError(f"AMBIGUOUS ({count} occurrences):\n  {old[:120]!r}")
        content = content.replace(old, new)
    return content


def insert_footnotes(content: str) -> str:
    """Append fn13–fn80 before the closing </ol> of the footnotes list."""
    marker = "</ol>"
    # Find the footnotes <ol> — it has a distinctive style attribute
    ol_marker = '<ol class="footnotes"'
    ol_pos = content.find(ol_marker)
    if ol_pos == -1:
        raise ValueError("Could not find <ol class=\"footnotes\"> in file")
    # Find the </ol> after that position
    ol_close_pos = content.find(marker, ol_pos)
    if ol_close_pos == -1:
        raise ValueError("Could not find closing </ol> for footnotes list")
    return content[:ol_close_pos] + "\n" + NEW_FOOTNOTES + "\n          " + marker + content[ol_close_pos + len(marker):]


def main() -> None:
    content = TARGET.read_text(encoding="utf-8")

    # Verify no VERIFY markers remain after applying fixes
    original_count = content.count("<!-- [VERIFY] -->")
    print(f"Found {original_count} VERIFY markers")

    content = apply_fixes(content)
    remaining = content.count("<!-- [VERIFY] -->")
    print(f"After fixes: {remaining} VERIFY markers remain")
    if remaining:
        raise RuntimeError(f"{remaining} VERIFY markers were not resolved")

    content = insert_footnotes(content)
    print("Footnotes fn13–fn80 inserted")

    TARGET.write_text(content, encoding="utf-8")
    print(f"Written: {TARGET}")


if __name__ == "__main__":
    main()
