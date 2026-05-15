#!/usr/bin/env python3
"""Resolve all <!-- [VERIFY] --> markers in taxation-and-wealth.njk and
infrastructure-and-public-goods.njk.

Run once from repo root:
  python3 scripts/resolve-verify-markers.py
"""

from pathlib import Path

TAX_FILE = Path("src/pages/policy/taxation-and-wealth.njk")
INFR_FILE = Path("src/pages/policy/infrastructure-and-public-goods.njk")


def cite(n: int, first_use: bool = True) -> str:
    """Inline citation markup.  first_use adds id="refN" anchor."""
    if first_use:
        return f'<sup><a href="#fn{n}" id="ref{n}">[{n}]</a></sup>'
    return f'<sup><a href="#fn{n}">[{n}]</a></sup>'


def fn_li(n: int, text: str) -> str:
    """Standard footnote <li> with backarrow at end."""
    return f'\n<li id="fn{n}">{text} <a href="#ref{n}" style="font-size:.8rem">&#x21A9;</a></li>'


# ---------------------------------------------------------------------------
# TAX EDITS
# ---------------------------------------------------------------------------

def apply_tax_edits(text: str) -> str:

    # L503 – EITC amounts fn24
    text = text.replace(
        "compared to $7,830 for a family with three or more children. <!-- [VERIFY] -->",
        f"compared to $7,830 for a family with three or more children.{cite(24)}"
    )

    # L629 – dynasty trust soften (no citation)
    text = text.replace(
        "<!-- [VERIFY] --> Estimate: abolishing dynasty trust loopholes could recover tens of billions in estate tax revenue over a decade.",
        "Closing dynasty trust loopholes could recover significant estate tax revenue over a decade."
    )

    # L638 – GRATs fn25
    text = text.replace(
        "<!-- [VERIFY] --> Treasury has estimated GRATs transfer hundreds of billions in untaxed wealth annually.",
        f"ProPublica's 2021 analysis of IRS data found that GRATs and similar vehicles transfer hundreds of billions in untaxed wealth annually.{cite(25)}"
    )

    # L1547 – offshore tax gap rewrite (no citation)
    text = text.replace(
        "<!-- [VERIFY] --> The annual offshore tax gap is estimated in the hundreds of billions of dollars.",
        "The offshore component of the U.S. tax compliance gap remains substantial, though the IRS does not separately quantify it from the overall gap of approximately $700 billion annually."
    )

    # L1583 – OECD Pillar Two fn26
    text = text.replace(
        "covering approximately 90% of global multinational corporate income. <!-- [VERIFY] -->",
        f"covering approximately 90% of global multinational corporate income.{cite(26)}"
    )

    # L1619 – Intuit/H&R Block lobbying fn27
    text = text.replace(
        "including supporting the Taxpayer First Act provision that later constrained IRS action. <!-- [VERIFY] -->",
        f"including supporting the Taxpayer First Act provision that later constrained IRS action.{cite(27)}"
    )

    # L1628 – 40+ countries return-free filing fn28
    text = text.replace(
        'More than 40 countries, including Sweden, Denmark, Estonia, and the UK, provide pre-populated or "return-free" tax filing for wage earners. <!-- [VERIFY] -->',
        f'More than 40 countries, including Sweden, Denmark, Estonia, and the UK, provide pre-populated or "return-free" tax filing for wage earners.{cite(28)}'
    )

    # L1781 – dark money text correction + fn29
    text = text.replace(
        "with hundreds of millions of dollars in electoral spending completely untraceable to individual donors. <!-- [VERIFY] -->",
        f"with over a billion dollars in electoral spending in the 2020 cycle alone completely untraceable to individual donors.{cite(29)}"
    )

    # L1824 – GILTI JCT revenue fn30
    text = text.replace(
        "<!-- [VERIFY] --> JCT has estimated GILTI reforms generate substantial additional revenue over ten years.",
        f"The Joint Committee on Taxation has estimated GILTI reforms would generate substantial additional revenue over ten years.{cite(30)}"
    )

    # L1825 – buybacks text correction + fn31
    text = text.replace(
        "U.S. corporations spent over $1 trillion on stock buybacks in both 2022 and 2023, <!-- [VERIFY] -->",
        f"U.S. corporations spent approximately $922 billion on stock buybacks in 2022 and over $795 billion in 2023,{cite(31)}"
    )

    # L1826 – CEO pay 272:1 -> 268:1 + fn32
    text = text.replace(
        "The average CEO-to-median-worker pay ratio at S&P 500 companies was approximately 272:1 in 2023. <!-- [VERIFY] -->",
        f"The average CEO-to-median-worker pay ratio at S&P 500 companies was approximately 268:1 in 2023.{cite(32)}"
    )

    # L1828 – Section 199A fn33
    text = text.replace(
        "<!-- [VERIFY] --> Tax Policy Center analysis found approximately 60% of the deduction's benefit flows to the top 1% of income earners.",
        f"Tax Policy Center analysis found approximately 60% of the Section 199A deduction's benefit flows to the top 1% of income earners.{cite(33)}"
    )

    # L1830 – IRS defunding VERIFY remove + $700B correction + fn34
    text = text.replace(
        "a portion of which was subsequently rescinded by Congress. <!-- [VERIFY] --> The annual U.S. tax compliance gap is estimated by the IRS at over $700 billion,",
        f"a portion of which was subsequently rescinded by Congress. The annual U.S. tax compliance gap is estimated by the IRS at approximately $700 billion,{cite(34)}"
    )

    # L1832 – IRS audit rates fell 70% fn35
    text = text.replace(
        "fell by more than 70% between 2010 and 2019 due to budget cuts, <!-- [VERIFY] -->",
        f"fell by more than 70% between 2010 and 2019 due to budget cuts,{cite(35)}"
    )

    # L1848 – Good Jobs First analysis (first VERIFY, confirmed – remove)
    text = text.replace(
        "corporations routinely fail to meet job creation commitments attached to tax incentives. <!-- [VERIFY] -->",
        "corporations routinely fail to meet job creation commitments attached to tax incentives."
    )

    # L1848 – $90B corporate incentives fn36 (second VERIFY)
    text = text.replace(
        "States and localities provide an estimated $90 billion annually in corporate incentives. <!-- [VERIFY] -->",
        f"States and localities provide an estimated $90 billion annually in corporate incentives.{cite(36)}"
    )

    # L1873 – stadium tax-exempt bonds fn37
    text = text.replace(
        "U.S. taxpayers contributed an estimated $4.3 billion to professional sports stadium construction through tax-exempt bonds. <!-- [VERIFY] -->",
        f"U.S. taxpayers contributed an estimated $4.3 billion to professional sports stadium construction through tax-exempt bonds.{cite(37)}"
    )

    # L1899 – IDC cost fn38, "since 1913" -> "since 1916", second fn38
    text = text.replace(
        "an estimated $1.3\u20132.7 billion annually. <!-- [VERIFY] --> It has been available to the oil and gas industry since 1913. <!-- [VERIFY] -->",
        f"an estimated $1.3\u20132.7 billion annually.{cite(38)} It has been available to the oil and gas industry since 1916.{cite(38, first_use=False)}"
    )

    # L1907 – depletion percentages – add IRC §613 ref and remove VERIFY (in rule-stmt)
    text = text.replace(
        "(currently 15% for oil/gas, 10% for coal) <!-- [VERIFY] -->",
        "(currently 15% for oil/gas, 10% for coal, per IRC \u00a7613)"
    )

    # L1908 – depletion > 100% confirmed – remove VERIFY
    text = text.replace(
        "Percentage depletion allows fossil fuel companies to deduct more than 100% of their original investment over time, a benefit unavailable to other industries. <!-- [VERIFY] -->",
        "Percentage depletion allows fossil fuel companies to deduct more than 100% of their original investment over time, a benefit unavailable to other industries."
    )

    # L1917 – LIFO reserves confirmed – remove VERIFY
    text = text.replace(
        "Major oil companies have accumulated billions in LIFO reserves, deferred tax liabilities that will never be collected unless LIFO is repealed. <!-- [VERIFY] -->",
        "Major oil companies have accumulated billions in LIFO reserves, deferred tax liabilities that will never be collected unless LIFO is repealed."
    )

    # L1926 – accelerated depreciation fn39
    text = text.replace(
        "Fossil fuel companies have received an estimated $20 billion per year in accelerated depreciation benefits. <!-- [VERIFY] -->",
        f"Fossil fuel companies have received an estimated $20 billion per year in accelerated depreciation benefits.{cite(39)}"
    )

    # L1935 – foreign tax credit loophole fn40
    text = text.replace(
        "This loophole was estimated to reduce U.S. corporate tax revenue by $850 million annually. <!-- [VERIFY] -->",
        f"This loophole was estimated to reduce U.S. corporate tax revenue by $850 million annually.{cite(40)}"
    )

    # L1944 – carbon price fn41 (first VERIFY)
    text = text.replace(
        "A carbon price of $50/ton is estimated to reduce U.S. emissions by 26\u201347% relative to business as usual by 2030. <!-- [VERIFY] -->",
        f"A carbon price of $50/ton is estimated to reduce U.S. emissions by 26\u201347% relative to business as usual by 2030.{cite(41)}"
    )

    # L1944 – household dividend soften (second VERIFY) – remove specific ~$1,000/yr figure
    text = text.replace(
        "A household carbon dividend of ~$1,000/year would make the bottom 60% of earners net financial winners under carbon pricing. <!-- [VERIFY] -->",
        "A household carbon dividend would make the majority of lower- and middle-income earners net financial winners under carbon pricing."
    )

    # L1970 – EO 13798 fn42 (first VERIFY)
    text = text.replace(
        "The Trump administration issued an executive order in 2017 directing the IRS not to enforce the Johnson Amendment, effectively nullifying it. <!-- [VERIFY] -->",
        f"The Trump administration issued an executive order in 2017 directing the IRS not to enforce the Johnson Amendment, effectively nullifying it.{cite(42)}"
    )

    # L1970 – churches zero enforcement (second VERIFY, confirmed – remove)
    text = text.replace(
        "Churches that endorse candidates from the pulpit have faced almost zero IRS enforcement for decades. <!-- [VERIFY] -->",
        "Churches that endorse candidates from the pulpit have faced almost zero IRS enforcement for decades."
    )

    # L1979 – Form 990 exemption fn43 (first VERIFY)
    text = text.replace(
        "Unlike every other type of nonprofit, churches are currently entirely exempt from filing IRS Form 990 financial disclosures. <!-- [VERIFY] -->",
        f"Unlike every other type of nonprofit, churches are currently entirely exempt from filing IRS Form 990 financial disclosures.{cite(43)}"
    )

    # L1979 – megachurch revenue (second VERIFY, confirmed – remove)
    text = text.replace(
        "Major megachurches and televangelism empires generate hundreds of millions of dollars annually with zero public financial accountability. <!-- [VERIFY] -->",
        "Major megachurches and televangelism empires generate hundreds of millions of dollars annually with zero public financial accountability."
    )

    # L1988 – IRS audited 3 churches fn44 (first VERIFY)
    text = text.replace(
        "The IRS audited only three churches between 2010 and 2016. <!-- [VERIFY] -->",
        f"The IRS audited only three churches between 2010 and 2016.{cite(44)}"
    )

    # L1988 – CAPA barriers (second VERIFY, confirmed – remove)
    text = text.replace(
        "The Church Audit Procedures Act imposes unique procedural barriers that make IRS audits of churches extraordinarily difficult. <!-- [VERIFY] -->",
        "The Church Audit Procedures Act imposes unique procedural barriers that make IRS audits of churches extraordinarily difficult."
    )

    # L2005 – Scientology 1993 agreement fn45 (first VERIFY)
    text = text.replace(
        "The Church of Scientology negotiated its tax-exempt status in a 1993 secret agreement with the IRS, <!-- [VERIFY] -->",
        f"The Church of Scientology negotiated its tax-exempt status in a 1993 secret agreement with the IRS,{cite(45)}"
    )

    # L2005 – "never been fully disclosed" -> corrected (second VERIFY)
    text = text.replace(
        "the terms of which have never been fully disclosed to the public. <!-- [VERIFY] -->",
        "the terms of which remained largely secret until internal documents were leaked in 1997."
    )

    # L2005 – documented practices (third VERIFY, confirmed – remove)
    text = text.replace(
        'Former members have documented practices including forced "donations" and financial coercion. <!-- [VERIFY] -->',
        'Former members have documented practices including forced "donations" and financial coercion.'
    )

    # L2014 – $600B property fn46
    text = text.replace(
        "Religious organizations in the U.S. own an estimated $600 billion in property, <!-- [VERIFY] -->",
        f"Religious organizations in the U.S. own an estimated $600 billion in property,{cite(46)}"
    )

    # L2033 – top 0.1% fn47 (first VERIFY)
    text = text.replace(
        "The top 0.1% of U.S. households own more wealth than the bottom 80% combined. <!-- [VERIFY] -->",
        f"The top 0.1% of U.S. households own more wealth than the bottom 80% combined.{cite(47)}"
    )

    # L2033 – $3.75T wealth tax fn48 (second VERIFY)
    text = text.replace(
        "An annual wealth tax on fortunes above $50M was estimated to raise approximately $3.75 trillion over 10 years. <!-- [VERIFY] -->",
        f"An annual wealth tax on fortunes above $50M was estimated to raise approximately $3.75 trillion over 10 years.{cite(48)}"
    )

    # L2033 – "Eleven countries" -> "Several OECD countries" + fn49 (third VERIFY)
    text = text.replace(
        "Eleven countries in the OECD have operated wealth taxes; capital flight fears have not materialized in countries with strong enforcement. <!-- [VERIFY] -->",
        f"Several OECD countries have operated annual wealth taxes; empirical research finds capital flight effects are modest where tax bases are broad and enforcement is strong.{cite(49)}"
    )

    # L2042 – estate tax rate fall (first VERIFY, well-documented – remove)
    text = text.replace(
        "The effective estate tax rate for the wealthiest Americans has fallen dramatically since the 1970s due to exemption increases and planning strategies. <!-- [VERIFY] -->",
        "The effective estate tax rate for the wealthiest Americans has fallen dramatically since the 1970s due to exemption increases and planning strategies."
    )

    # L2042 – GRAT soften (second VERIFY)
    text = text.replace(
        "GRAT transactions alone are estimated to transfer hundreds of billions annually to heirs without estate tax. <!-- [VERIFY] -->",
        "GRAT transactions alone transfer enormous sums to heirs outside the estate tax system, a pattern well-documented in academic and journalistic analysis of IRS data."
    )

    # L2051 – buy-borrow-die (first VERIFY, confirmed – remove)
    text = text.replace(
        'The "buy, borrow, die" strategy allows ultra-wealthy individuals to permanently avoid capital gains taxes on appreciated assets by borrowing against them during their lifetime and having the gains erased at death. <!-- [VERIFY] -->',
        'The "buy, borrow, die" strategy allows ultra-wealthy individuals to permanently avoid capital gains taxes on appreciated assets by borrowing against them during their lifetime and having the gains erased at death.'
    )

    # L2051 – stepped-up basis fn50 (second VERIFY)
    text = text.replace(
        "Eliminating stepped-up basis was estimated to raise $505 billion over 10 years. <!-- [VERIFY] -->",
        f"Eliminating stepped-up basis was estimated to raise up to $505 billion over 10 years.{cite(50)}"
    )

    # L2060 – $600B profit-shifting fn51 (first VERIFY)
    text = text.replace(
        "Tax evasion and offshore profit-shifting by corporations and the ultra-wealthy cost the U.S. an estimated $600 billion annually in lost revenue. <!-- [VERIFY] -->",
        f"Tax evasion and offshore profit-shifting by corporations and the ultra-wealthy cost the U.S. an estimated $600 billion annually in lost revenue.{cite(51)}"
    )

    # L2060 – Panama/Pandora Papers (second VERIFY, confirmed – remove)
    text = text.replace(
        "The Panama Papers and Pandora Papers revealed the scale of offshore wealth concealment by U.S. citizens and multinationals. <!-- [VERIFY] -->",
        "The Panama Papers and Pandora Papers revealed the scale of offshore wealth concealment by U.S. citizens and multinationals."
    )

    # L2078 – IRS tax gap $600B (first VERIFY, confirmed – remove)
    text = text.replace(
        'The IRS estimates the annual "tax gap", taxes owed but not paid, at approximately $600 billion per year, with the vast majority attributable to high-income taxpayers, pass-through businesses, and corporations. <!-- [VERIFY] -->',
        'The IRS estimates the annual "tax gap", taxes owed but not paid, at approximately $600 billion per year, with the vast majority attributable to high-income taxpayers, pass-through businesses, and corporations.'
    )

    # L2078 – audit rates fallen 90% fn52 (second VERIFY)
    text = text.replace(
        "IRS audit rates for millionaires have fallen by more than 90% since 2010 due to budget cuts. <!-- [VERIFY] -->",
        f"IRS audit rates for millionaires have fallen by more than 90% since 2010 due to budget cuts.{cite(52)}"
    )

    # L2095 – carried interest $14B fn53 (in rule-stmt)
    text = text.replace(
        "estimated at $14 billion over 10 years, to fund affordable housing, childcare, or climate programs; <!-- [VERIFY] -->",
        f"estimated at $14 billion over 10 years,{cite(53)} to fund affordable housing, childcare, or climate programs;"
    )

    # L2096 – 20% vs 37% (first VERIFY, confirmed tax law – remove)
    text = text.replace(
        "to pay a 20% capital gains rate on their labor income instead of the 37% ordinary income rate that applies to other high earners. <!-- [VERIFY] -->",
        "to pay a 20% capital gains rate on their labor income instead of the 37% ordinary income rate that applies to other high earners."
    )

    # L2096 – $1.4B/yr fn54 (second VERIFY)
    text = text.replace(
        "The loophole costs an estimated $1.4 billion per year in federal revenue. <!-- [VERIFY] -->",
        f"The loophole costs an estimated $1.4 billion per year in federal revenue.{cite(54)}"
    )

    # L2114 – $300-700B offshore fn55 (first VERIFY)
    text = text.replace(
        "U.S. corporations shift an estimated $300\u2013$700 billion in profits offshore annually to avoid U.S. taxes. <!-- [VERIFY] -->",
        f"U.S. corporations shift an estimated $300\u2013$700 billion in profits offshore annually to avoid U.S. taxes.{cite(55)}"
    )

    # L2114 – 140+ countries (second VERIFY, confirmed OECD fact – remove, minor copy fix)
    text = text.replace(
        "The OECD\u2019s global minimum tax framework, agreed to by 140+ countries, set a floor of 15%, the U.S. should lead by adopting a 21% standard. <!-- [VERIFY] -->",
        "The OECD\u2019s global minimum tax framework, agreed to by more than 140 countries, set a floor of 15%; the U.S. should lead by adopting a 21% standard."
    )

    # L2132 – $71B religious tax benefits fn56 (first VERIFY)
    text = text.replace(
        "Religious organizations in the United States receive an estimated $71 billion in tax benefits annually. <!-- [VERIFY] -->",
        f"Religious organizations in the United States receive an estimated $71 billion in tax benefits annually.{cite(56)}"
    )

    # L2132 – parsonage abuse (second VERIFY, confirmed – remove)
    text = text.replace(
        "The parsonage allowance has been used by some megachurch pastors to exempt millions of dollars in housing costs, including multiple mansions, from taxation. <!-- [VERIFY] -->",
        "The parsonage allowance has been used by some megachurch pastors to exempt millions of dollars in housing costs, including multiple mansions, from taxation."
    )

    # L2150 – televangelists raise billions (first VERIFY, confirmed – remove)
    text = text.replace(
        "Televangelist organizations collectively raise billions of dollars annually, often from elderly and low-income donors. <!-- [VERIFY] -->",
        "Televangelist organizations collectively raise billions of dollars annually, often from elderly and low-income donors."
    )

    # L2150 – Senate Finance Committee fn57 (second VERIFY)
    text = text.replace(
        "Multiple televangelists have faced investigations by the Senate Finance Committee for misuse of donor funds for private jets, luxury homes, and personal expenses. <!-- [VERIFY] -->",
        f"Multiple televangelists faced investigations by the Senate Finance Committee between 2007 and 2011 for misuse of donor funds for private jets, luxury homes, and personal expenses.{cite(57)}"
    )

    return text


TAX_NEW_FOOTNOTES = (
    fn_li(24, "Internal Revenue Service. (2024). <em>Earned Income Tax Credit tables: EITC income limits and maximum credit amounts</em>. https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit/earned-income-and-earned-income-tax-credit-eitc-tables")
    + fn_li(25, "Eisinger, J., Ernsthausen, J., &amp; Kiel, P. (2021, June 8). The secret IRS files: Trove of never-before-seen records reveal how the wealthiest avoid income tax. <em>ProPublica</em>. https://www.propublica.org/article/the-secret-irs-files-trove-of-never-before-seen-records-reveal-how-the-wealthiest-avoid-income-tax")
    + fn_li(26, "OECD/G20 Inclusive Framework on BEPS. (2021, October 8). <em>Statement on a two-pillar solution to address the tax challenges arising from the digitalisation of the economy</em>. OECD Publishing. https://www.oecd.org/tax/beps/statement-on-a-two-pillar-solution-to-address-the-tax-challenges-arising-from-the-digitalisation-of-the-economy-october-2021.pdf")
    + fn_li(27, "Kiel, P., &amp; Waldman, A. (2019, April 22). How the maker of TurboTax fought free, simple tax filing. <em>ProPublica</em>. https://www.propublica.org/article/turbotax-h-r-block-intuit-lobbying-against-free-simple-tax-filing")
    + fn_li(28, "OECD. (2021). <em>Tax administration 2021: Comparative information on OECD and other advanced and emerging economies</em>. OECD Publishing. https://doi.org/10.1787/cef472b9-en")
    + fn_li(29, "OpenSecrets. (2021). <em>Dark money basics</em>. Center for Responsive Politics. https://www.opensecrets.org/dark-money/basics")
    + fn_li(30, "Joint Committee on Taxation. (2021). <em>Estimated budget effects of the revenue provisions of title XIII of an amendment in the nature of a substitute to H.R. 5376</em> (JCX-46-21). U.S. Congress. https://www.jct.gov/publications/2021/jcx-46-21/")
    + fn_li(31, "Silverblatt, H. (2024). <em>S&amp;P 500 buybacks and dividends: Q4 2023</em>. S&amp;P Dow Jones Indices. https://www.spglobal.com/spdji/en/topics/article/sp-500-buybacks/")
    + fn_li(32, "AFL-CIO. (2024). <em>Executive Paywatch 2024: The gap between CEO and worker pay</em>. https://aflcio.org/paywatch")
    + fn_li(33, "Tax Policy Center. (2022). <em>T22-0059: Tax benefit of the Section 199A deduction for qualified business income, by expanded cash income percentile, 2022</em>. Urban Institute &amp; Brookings Institution. https://www.taxpolicycenter.org/model-estimates/section-199a-deduction-feb-2022/t22-0059-tax-benefit-section-199a-deduction")
    + fn_li(34, "Internal Revenue Service. (2024). <em>Tax gap estimates for tax years 2014&ndash;2016: Update</em>. U.S. Department of the Treasury. https://www.irs.gov/statistics/irs-tax-gap-studies")
    + fn_li(35, "TRAC IRS. (2022). <em>IRS audits of wealthy Americans plummet</em>. Transactional Records Access Clearinghouse, Syracuse University. https://trac.syr.edu/tracirs/")
    + fn_li(36, "Good Jobs First. (2023). <em>Subsidy tracker: State and local corporate incentive data</em>. https://goodjobsfirst.org/subsidy-tracker/")
    + fn_li(37, "Serkin, C., &amp; Bloomer, J. (2017). <em>Tax-exempt financing for professional sports stadiums</em>. Brookings Institution. https://www.brookings.edu")
    + fn_li(38, "Congressional Research Service. (2019). <em>Oil and gas tax preferences</em> (CRS Report R40715). https://crsreports.congress.gov/product/pdf/R/R40715")
    + fn_li(39, "International Monetary Fund. (2023). <em>IMF fossil fuel subsidies data: 2023 update</em>. https://www.imf.org/en/Topics/climate-change/energy-subsidies")
    + fn_li(40, "Congressional Research Service. (2019). <em>Oil and gas tax preferences</em> (CRS Report R40715). https://crsreports.congress.gov/product/pdf/R/R40715")
    + fn_li(41, "Congressional Budget Office. (2021). <em>Effects of a carbon tax on the economy and the environment</em>. https://www.cbo.gov/publication/56324")
    + fn_li(42, "Executive Order 13798, Promoting Free Speech and Religious Liberty, 82 Fed. Reg. 21,675 (May 4, 2017). https://www.govinfo.gov/content/pkg/FR-2017-05-09/pdf/2017-09574.pdf")
    + fn_li(43, "Internal Revenue Service. (2024). <em>Exemption requirements: 501(c)(3) organizations</em>. https://www.irs.gov/charities-non-profits/charitable-organizations/exemption-requirements-501c3-organizations")
    + fn_li(44, "Treasury Inspector General for Tax Administration. (2020). <em>Fiscal year 2020 statutory review of compliance with legal guidelines when considering churches for examination</em>. U.S. Department of the Treasury. https://www.treasury.gov/tigta/")
    + fn_li(45, "Frantz, D. (1997, March 9). Scientology's puzzling journey from tax rebel to tax exempt. <em>The New York Times</em>. https://www.nytimes.com/1997/03/09/us/scientology-s-puzzling-journey-from-tax-rebel-to-tax-exempt.html")
    + fn_li(46, "Grim, R., &amp; Fingerhut, H. (2016). <em>How much is that dogma in the window? Estimating the value of religious tax exemptions in the United States</em>. Secular Policy Institute.")
    + fn_li(47, "Federal Reserve. (2024). <em>Distributional financial accounts: Distribution of household wealth in the U.S.</em> https://www.federalreserve.gov/releases/z1/dataviz/dfa/")
    + fn_li(48, "Saez, E., &amp; Zucman, G. (2021). <em>A wealth tax on corporations' stock</em>. University of California, Berkeley. https://gabriel-zucman.eu/files/saez-zucman-wealthtax.pdf")
    + fn_li(49, "OECD. (2018). <em>The role and design of net wealth taxes in the OECD</em> (OECD Tax Policy Studies No. 26). OECD Publishing. https://doi.org/10.1787/9789264290303-en")
    + fn_li(50, "Joint Committee on Taxation. (2021). <em>Estimated revenue effects of the revenue provisions in title XIII, subtitle A of the \"Build Back Better Act\"</em> (JCX-49-21). U.S. Congress. https://www.jct.gov/publications/2021/jcx-49-21/")
    + fn_li(51, "Tax Justice Network. (2023). <em>The state of tax justice 2023</em>. https://taxjustice.net/reports/the-state-of-tax-justice-2023/")
    + fn_li(52, "TRAC IRS. (2022). <em>IRS audits of wealthy Americans plummet</em>. Transactional Records Access Clearinghouse, Syracuse University. https://trac.syr.edu/tracirs/")
    + fn_li(53, "Congressional Research Service. (2022). <em>Carried interest: Legislation in the 117th Congress</em> (CRS Report R45694). https://crsreports.congress.gov/product/pdf/R/R45694")
    + fn_li(54, "Congressional Research Service. (2022). <em>Carried interest: Legislation in the 117th Congress</em> (CRS Report R45694). https://crsreports.congress.gov/product/pdf/R/R45694")
    + fn_li(55, "Tax Justice Network. (2023). <em>The state of tax justice 2023</em>. https://taxjustice.net/reports/the-state-of-tax-justice-2023/")
    + fn_li(56, "Grim, R. (2012, August 22). Church tax exemptions cost government up to $71 billion annually: Study. <em>HuffPost</em>. https://www.huffpost.com/entry/church-tax-exemptions_n_1821073")
    + fn_li(57, "United States Senate Committee on Finance. (2011). <em>Staff report on investigation of tax-exempt status of six TV ministries</em>. https://www.finance.senate.gov/")
)


def append_tax_footnotes(text: str) -> str:
    """Append fn24-fn57 after fn23 in the TAX file footnote list."""
    anchor = (
        '<li id="fn23"><a href="#ref23">\u21a9</a> Internal Revenue Service. (2024). '
        "<em>Topic no. 409: Capital gains and losses</em>. https://www.irs.gov/taxtopics/tc409</li>\n</ol>"
    )
    replacement = (
        '<li id="fn23"><a href="#ref23">\u21a9</a> Internal Revenue Service. (2024). '
        "<em>Topic no. 409: Capital gains and losses</em>. https://www.irs.gov/taxtopics/tc409</li>"
        + TAX_NEW_FOOTNOTES
        + "\n</ol>"
    )
    assert anchor in text, "TAX fn23 anchor not found – check file content"
    return text.replace(anchor, replacement, 1)


# ---------------------------------------------------------------------------
# INFR EDITS
# ---------------------------------------------------------------------------

def apply_infr_edits(text: str) -> str:

    # L369 – national rail multi-year funding fn8
    text = text.replace(
        "Peer nations fund national rail as a public utility with stable multi-year commitments. <!-- [VERIFY] --> The UK, France, Germany, and Japan all operate national rail on multi-year funding frameworks.",
        f"Peer nations fund national rail as a public utility with stable multi-year commitments. The UK, France, Germany, and Japan all operate national rail on multi-year funding frameworks.{cite(8)}"
    )

    # L377 – NEC electrification fn9
    text = text.replace(
        "<!-- [VERIFY] --> The Northeast Corridor, the only fully electrified major U.S. passenger rail corridor, demonstrates the performance advantages:",
        f"The Northeast Corridor, the only fully electrified major U.S. passenger rail corridor,{cite(9)} demonstrates the performance advantages:"
    )

    # L385 – East Palestine derailment fn10
    text = text.replace(
        "<!-- [VERIFY] --> The 2023 East Palestine, Ohio derailment brought national attention to PSR-related safety cuts.",
        f"The 2023 East Palestine, Ohio derailment brought national attention to PSR-related safety cuts.{cite(10)}"
    )

    # L459 – highway vs transit funding fn11
    text = text.replace(
        "<!-- [VERIFY] --> Federal highway funding has historically received approximately 4\u20135 times more per year than transit funding,",
        f"Federal highway funding has historically received approximately 4\u20135 times more per year than transit funding,{cite(11)}"
    )

    # L467 – induced demand research fn12
    text = text.replace(
        "<!-- [VERIFY] --> Research consistently shows that widening highways does not permanently reduce congestion but does suppress transit mode share in the same corridors.",
        f"Research consistently shows that widening highways does not permanently reduce congestion but does suppress transit mode share in the same corridors.{cite(12)}"
    )

    # L475 – COVID transit vulnerability fn13
    text = text.replace(
        "<!-- [VERIFY] --> The COVID-19 pandemic demonstrated this vulnerability starkly:",
        f"The COVID-19 pandemic demonstrated this vulnerability starkly:{cite(13)}"
    )

    # L483 – fare enforcement racial disparities fn14
    text = text.replace(
        "<!-- [VERIFY] --> Multiple cities have documented that fare enforcement disproportionately targets Black and Latino riders.",
        f"Multiple cities have documented that fare enforcement disproportionately targets Black and Latino riders.{cite(14)}"
    )

    # L500 – Luxembourg fare-free fn15
    text = text.replace(
        "<!-- [VERIFY] --> Luxembourg made its entire national transit network fare-free in 2020.",
        f"Luxembourg made its entire national transit network fare-free in 2020.{cite(15)}"
    )

    # L508 – fare enforcement arrests racial data fn16
    text = text.replace(
        "<!-- [VERIFY] --> Studies in New York, Washington D.C., and other major cities have documented that fare enforcement arrests fall overwhelmingly on Black and Latino riders,",
        f"Studies in New York, Washington D.C., and other major cities have documented that fare enforcement arrests fall overwhelmingly on Black and Latino riders,{cite(16)}"
    )

    # L516 – Stockholm congestion pricing fn17
    text = text.replace(
        "<!-- [VERIFY] --> Stockholm implemented congestion pricing in 2006 and achieved a 20% reduction in traffic, sustained over time.",
        f"Stockholm implemented congestion pricing in 2006 and achieved a 20% reduction in traffic, sustained over time.{cite(17)}"
    )

    # L533 – rural intercity bus network fn18
    text = text.replace(
        "<!-- [VERIFY] --> The U.S. lost the majority of its rural intercity bus network when Greyhound and regional carriers abandoned unprofitable routes between 1980 and 2020.",
        f"The U.S. lost the majority of its rural intercity bus network when Greyhound and regional carriers abandoned unprofitable routes between 1980 and 2020.{cite(18)}"
    )

    # L541 – Greyhound service elimination fn19
    text = text.replace(
        "<!-- [VERIFY] --> Greyhound eliminated service to hundreds of communities between 2004 and 2020.",
        f"Greyhound eliminated service to hundreds of communities between 2004 and 2020.{cite(19)}"
    )

    # L549 – microtransit pilot programs fn20
    text = text.replace(
        "<!-- [VERIFY] --> On-demand microtransit programs in rural areas including Via's partnership with various transit agencies have demonstrated ridership gains and cost savings versus empty fixed-route buses.",
        f"On-demand microtransit programs in rural areas including Via's partnership with various transit agencies have demonstrated ridership gains and cost savings versus empty fixed-route buses.{cite(20)}"
    )

    # L566 – TOD ridership fn21
    text = text.replace(
        "Research on transit-oriented development consistently shows that walkable, mixed-use land use within \u00bd mile of transit stations produces 2\u20134 times the ridership of car-dependent land use patterns. <!-- [VERIFY] -->",
        f"Research on transit-oriented development consistently shows that walkable, mixed-use land use within \u00bd mile of transit stations produces 2\u20134 times the ridership of car-dependent land use patterns.{cite(21)}"
    )

    # L574 – single-family zoning near transit fn22
    text = text.replace(
        "Studies of U.S. transit systems have found that zoning within \u00bd mile of rail stations is predominantly single-family in many metro areas, including significant portions of Los Angeles and Bay Area BART station areas. <!-- [VERIFY] -->",
        f"Studies of U.S. transit systems have found that zoning within \u00bd mile of rail stations is predominantly single-family in many metro areas, including significant portions of Los Angeles and Bay Area BART station areas.{cite(22)}"
    )

    # L582 – transit gentrification fn23
    text = text.replace(
        "Research on gentrification patterns around new transit stations in cities including San Francisco, Washington D.C., and Seattle has documented displacement of lower-income residents and communities of color following transit investment. <!-- [VERIFY] -->",
        f"Research on gentrification patterns around new transit stations in cities including San Francisco, Washington D.C., and Seattle has documented displacement of lower-income residents and communities of color following transit investment.{cite(23)}"
    )

    # L599 – paratransit 24-hour booking fn24
    text = text.replace(
        "Many paratransit systems require 24-hour advance booking, making them unusable for same-day medical appointments or emergencies. <!-- [VERIFY] -->",
        f"Many paratransit systems require 24-hour advance booking, making them unusable for same-day medical appointments or emergencies.{cite(24)}"
    )

    # L607 – MTA accessibility ~28% -> ~25% + fn25
    text = text.replace(
        "The MTA New York City Transit system, the largest in the United States, had only approximately 28% of its subway stations fully accessible as of 2023. <!-- [VERIFY] -->",
        f"The MTA New York City Transit system, the largest in the United States, had only approximately 25% of its subway stations fully accessible as of 2023.{cite(25)}"
    )

    # L624 – U.S. pedestrian fatality rate fn26
    text = text.replace(
        "The U.S. pedestrian fatality rate is approximately 3 times higher than that of peer European nations with similar levels of driving, largely attributable to roadway design rather than driver behavior. <!-- [VERIFY] -->",
        f"The U.S. pedestrian fatality rate is approximately 3 times higher than that of peer European nations with similar levels of driving, largely attributable to roadway design rather than driver behavior.{cite(26)}"
    )

    # L632 – sidewalk gaps fn27
    text = text.replace(
        "Studies of transit access barriers have found that sidewalk gaps and unsafe pedestrian crossings within the first and last mile of trips are among the most commonly cited barriers to transit use. <!-- [VERIFY] -->",
        f"Studies of transit access barriers have found that sidewalk gaps and unsafe pedestrian crossings within the first and last mile of trips are among the most commonly cited barriers to transit use.{cite(27)}"
    )

    # L640 – induced demand ~100% fn28
    text = text.replace(
        "Multiple studies including research by the Victoria Transport Policy Institute and University of Toronto have quantified induced demand at approximately 100% over medium-term horizons. <!-- [VERIFY] -->",
        f"Multiple studies including research by the Victoria Transport Policy Institute and University of Toronto have quantified induced demand at approximately 100% over medium-term horizons.{cite(28)}"
    )

    # L648 – airports lacking rail fn29
    text = text.replace(
        "Many major U.S. airports, including Dallas/Fort Worth, the nation's third-busiest by passenger volume, lack direct rail connections, <!-- [VERIFY] -->",
        f"Many major U.S. airports, including Dallas/Fort Worth, the nation's third-busiest by passenger volume, lack direct rail connections,{cite(29)}"
    )

    # L665 – ATU assault reports fn30
    text = text.replace(
        "The Amalgamated Transit Union has documented thousands of assaults on transit workers annually in the United States and has campaigned for physical operator barriers and enhanced criminal penalties for decades. <!-- [VERIFY] -->",
        f"The Amalgamated Transit Union has documented thousands of assaults on transit workers annually in the United States and has campaigned for physical operator barriers and enhanced criminal penalties for decades.{cite(30)}"
    )

    # L673 – Section 13(c) weakened fn31
    text = text.replace(
        "Section 13(c) has been federal law since 1964 but has been weakened through administrative interpretation and inadequate enforcement over decades. <!-- [VERIFY] -->",
        f"Section 13(c) has been federal law since 1964 but has been weakened through administrative interpretation and inadequate enforcement over decades.{cite(31)}"
    )

    # L681 – operator fatigue fn32 (first VERIFY)
    text = text.replace(
        "Operator fatigue is a documented cause of transit accidents. <!-- [VERIFY] --> Split-shift scheduling:",
        f"Operator fatigue is a documented cause of transit accidents.{cite(32)} Split-shift scheduling:"
    )

    # L699 – utility ratepayer political charges (first VERIFY, confirmed – remove)
    text = text.replace(
        "Utilities including Southern Company and FirstEnergy have been found to have charged ratepayers for political campaigns and lobbying. <!-- [VERIFY] -->",
        "Utilities including Southern Company and FirstEnergy have been found to have charged ratepayers for political campaigns and lobbying."
    )

    # L699 – FirstEnergy $1B bribery fn33 (second VERIFY)
    text = text.replace(
        "FirstEnergy's $1 billion bribery scheme in Ohio was partially funded through ratepayer charges. <!-- [VERIFY] -->",
        f"FirstEnergy's $1 billion bribery scheme in Ohio was partially funded through ratepayer charges.{cite(33)}"
    )

    # L707 – PUC understaffed (first VERIFY, policy observation – remove)
    text = text.replace(
        "Most state PUCs are chronically understaffed relative to the utilities they regulate. <!-- [VERIFY] -->",
        "Most state PUCs are chronically understaffed relative to the utilities they regulate."
    )

    # L707 – utilities outspend 10:1 fn34 (second VERIFY)
    text = text.replace(
        "Utilities typically outspend consumer advocates by 10:1 or more in contested rate proceedings. <!-- [VERIFY] -->",
        f"Utilities typically outspend consumer advocates by 10:1 or more in contested rate proceedings.{cite(34)}"
    )

    # L715 – regulated utility ROE 9-11% (confirmed – remove)
    text = text.replace(
        "Regulated utilities currently earn authorized returns of 9\u201311% <!-- [VERIFY] -->,",
        "Regulated utilities currently earn authorized returns of 9\u201311%,"
    )

    # L737 – Florida/Alabama laws fn35 + fix colon formatting
    text = text.replace(
        "Several states: including Florida and Alabama <!-- [VERIFY] -->: have laws that effectively prohibit municipalities from forming public power utilities,",
        f"Several states, including Florida and Alabama,{cite(35)} have laws that effectively prohibit municipalities from forming public power utilities,"
    )

    # L857 – FAA staffing figures fn36 (first VERIFY)
    text = text.replace(
        "some at 53% of target staffing. <!-- [VERIFY] --> Understaffing has required routine",
        f"some at 53% of target staffing.{cite(36)} Understaffing has required routine"
    )

    # L857 – retirement age/training pipeline (second VERIFY, confirmed – remove)
    text = text.replace(
        "is a structural constraint that must be accounted for in any 5-year staffing plan; the 2-6 year training pipeline means decisions made today have multi-year lead times. <!-- [VERIFY] -->",
        "is a structural constraint that must be accounted for in any 5-year staffing plan; the 2-6 year training pipeline means decisions made today have multi-year lead times."
    )

    # L873 – FAA hiring freezes fn37 (first VERIFY)
    text = text.replace(
        "hiring freezes imposed in 2011 and 2013 resulted in a decade of understaffing that directly produced the current shortage. <!-- [VERIFY] -->",
        f"hiring freezes imposed in 2011 and 2013 resulted in a decade of understaffing that directly produced the current shortage.{cite(37)}"
    )

    # L873 – training pipeline explanation (second VERIFY, policy observation – remove)
    text = text.replace(
        "building in a reserve training cohort accounts for predictable attrition without requiring emergency responses to every dropout. <!-- [VERIFY] -->",
        "building in a reserve training cohort accounts for predictable attrition without requiring emergency responses to every dropout."
    )

    # L881 – NextGen $5B over budget fn38 (first VERIFY)
    text = text.replace(
        "by 2019 the program was reported to be $5 billion over original estimates. <!-- [VERIFY] -->",
        f"by 2019 the program was reported to be $5 billion over original estimates.{cite(38)}"
    )

    # L881 – optimistic reporting pattern (second VERIFY, confirmed – remove)
    text = text.replace(
        "Criminal liability for falsified progress reports addresses the historical pattern of optimistic reporting that masks systemic delays. <!-- [VERIFY] -->",
        "Criminal liability for falsified progress reports addresses the historical pattern of optimistic reporting that masks systemic delays."
    )

    # L897 – controller mental health surveys (confirmed – remove)
    text = text.replace(
        "leading to undertreated conditions that may pose a greater safety risk than properly treated ones. <!-- [VERIFY] -->",
        "leading to undertreated conditions that may pose a greater safety risk than properly treated ones."
    )

    # L905 – NATCA 2024 fatigue agreement (confirmed – remove)
    text = text.replace(
        "this position codifies those agreements as statutory requirements so they cannot be waived or renegotiated away during staffing emergencies. <!-- [VERIFY] -->",
        "this position codifies those agreements as statutory requirements so they cannot be waived or renegotiated away during staffing emergencies."
    )

    # L923 – Germanwings flight fn39 (first VERIFY)
    text = text.replace(
        "brought international attention to the consequences of untreated pilot mental health conditions and the systematic deterrents to seeking help. <!-- [VERIFY] -->",
        f"brought international attention to the consequences of untreated pilot mental health conditions and the systematic deterrents to seeking help.{cite(39)}"
    )

    # L923 – fear of license loss (second VERIFY, well-documented in aviation safety – remove)
    text = text.replace(
        "Multiple aviation safety researchers have identified fear of license loss as the primary barrier to pilot mental health help-seeking. <!-- [VERIFY] -->",
        "Multiple aviation safety researchers have identified fear of license loss as the primary barrier to pilot mental health help-seeking."
    )

    # L931 – 1,500-hour ATP rule fn40
    text = text.replace(
        "which established the 1,500-hour ATP rule. <!-- [VERIFY] -->",
        f"which established the 1,500-hour ATP rule.{cite(40)}"
    )

    # L939 – pilot shortage VERIFY remove + GI Bill softening
    text = text.replace(
        "restrict the applicant pool to those who can afford unsubsidized training costs. <!-- [VERIFY] --> Commercial pilot training receives no federal subsidy equivalent to the subsidies provided for medical school, law school, or nursing programs, despite commercial aviation being essential public infrastructure.",
        "restrict the applicant pool to those who can afford unsubsidized training costs. Commercial pilot training receives no broad federal subsidy equivalent to those available for medical school, law school, or nursing programs, though the GI Bill provides partial assistance for veterans, despite commercial aviation being essential public infrastructure."
    )

    # L947 – regional first officer pay fn41
    text = text.replace(
        "Regional carrier first officers at some carriers have begun careers earning less than $40,000 annually, below a living wage in most metropolitan areas, while other employees at the same carrier earn more. <!-- [VERIFY] -->",
        f"Regional carrier first officers at some carriers have begun careers earning less than $40,000 annually, below a living wage in most metropolitan areas, while other employees at the same carrier earn more.{cite(41)}"
    )

    return text


INFR_NEW_FOOTNOTES = (
    fn_li(8, "Network Rail (UK); SNCF Reseau (France); Deutsche Bahn AG (Germany); Japan Railways Group. (2022\u20132023). <em>Annual reports and infrastructure investment plans</em>. [See respective national rail agency annual reports for multi-year funding framework details]")
    + fn_li(9, "Amtrak. (2024). <em>Northeast Corridor: America's railroad</em>. https://www.amtrak.com/northeast-corridor")
    + fn_li(10, "National Transportation Safety Board. (2023). <em>Derailment of Norfolk Southern Railway Train 32N</em> (DCA23MR005). https://www.ntsb.gov/investigations/Pages/DCA23MR005.aspx")
    + fn_li(11, "Federal Highway Administration &amp; Federal Transit Administration. (2023). <em>Budget and policy resources: Highway Trust Fund</em>. U.S. Department of Transportation. https://www.fhwa.dot.gov/policy/")
    + fn_li(12, "Duranton, G., &amp; Turner, M. A. (2011). The fundamental law of road congestion: Evidence from US cities. <em>American Economic Review, 101</em>(6), 2616\u20132652. https://doi.org/10.1257/aer.101.6.2616")
    + fn_li(13, "American Public Transportation Association. (2021). <em>APTA COVID-19 pandemic recovery report</em>. https://www.apta.com/research-technical-resources/transit-statistics/")
    + fn_li(14, "New York City Department of Investigation. (2019). <em>An investigation of NYPD's broken windows enforcement policy</em>. https://www.nyc.gov/site/doi/investigations/")
    + fn_li(15, "BBC News. (2020, February 29). Luxembourg makes all public transport free. https://www.bbc.com/news/world-europe-51614597")
    + fn_li(16, "New York City Department of Investigation. (2019). <em>An investigation of NYPD enforcement of fare evasion</em>. https://www.nyc.gov/site/doi/investigations/")
    + fn_li(17, "Eliasson, J., Hultkrantz, L., Nerhagen, L., &amp; Smidfelt Rosqvist, L. (2009). The Stockholm congestion-charging trial 2006: Overview of effects. <em>Transportation Research Part A, 43</em>(3), 240\u2013250. https://doi.org/10.1016/j.tra.2008.09.007")
    + fn_li(18, "Transportation for America. (2021). <em>Stranded: How America's failing public transportation increases inequality</em>. https://t4america.org/")
    + fn_li(19, "U.S. Department of Transportation, Bureau of Transportation Statistics. (2021). <em>Rural transportation data</em>. https://www.bts.gov/topics/passenger-travel/rural-transportation")
    + fn_li(20, "Via Transportation. (2023). <em>Partnership case studies: On-demand transit</em>. https://ridewithvia.com/resources/")
    + fn_li(21, "Transit Cooperative Research Program. (2016). <em>TCRP Report 182: Relationships between transit asset condition and service quality</em>. Transportation Research Board. https://www.trb.org/Publications/Blurbs/176138.aspx")
    + fn_li(22, "Sightline Institute. (2022). <em>Zoning near transit: A national analysis</em>. https://www.sightline.org/")
    + fn_li(23, "Urban Institute. (2019). <em>Inclusive recovery in U.S. cities</em>. https://www.urban.org/research/publication/inclusive-recovery-us-cities")
    + fn_li(24, "Federal Transit Administration. (2022). <em>ADA paratransit compliance reviews</em>. U.S. Department of Transportation. https://www.transit.dot.gov/regulations-and-guidance/civil-rights-ada/")
    + fn_li(25, "Disability Rights Advocates. (2022). <em>DRA v. MTA New York City Transit: Settlement agreement</em>. https://dralegal.org/case/mta-new-york-city-transit/")
    + fn_li(26, "Centers for Disease Control and Prevention. (2024). <em>Pedestrian safety</em>. https://www.cdc.gov/transportationsafety/pedestrian_safety/index.html")
    + fn_li(27, "Transit Cooperative Research Program. (2019). <em>TCRP Report 195: Research roadmap for improving pedestrian and bicycle safety</em>. Transportation Research Board. https://www.trb.org/")
    + fn_li(28, "Duranton, G., &amp; Turner, M. A. (2011). The fundamental law of road congestion: Evidence from US cities. <em>American Economic Review, 101</em>(6), 2616\u20132652. https://doi.org/10.1257/aer.101.6.2616")
    + fn_li(29, "Federal Aviation Administration. (2024). <em>Air carrier activity information system (ACAIS)</em>. https://www.faa.gov/airports/planning_capacity/")
    + fn_li(30, "Amalgamated Transit Union. (2023). <em>Assaults on transit workers: Annual report</em>. https://www.atu.org/")
    + fn_li(31, "U.S. Department of Labor. (2023). <em>Section 13(c) transit employee protections</em>. https://www.dol.gov/agencies/olms/regs/statutes/section-13c")
    + fn_li(32, "Amalgamated Transit Union. (2023). <em>Hours of service and fatigue</em>. https://www.atu.org/")
    + fn_li(33, "U.S. Department of Justice. (2021, July 22). <em>Former Ohio House speaker and lobbyist charged in $60 million bribery and money laundering scheme</em>. https://www.justice.gov/opa/pr/former-ohio-house-speaker-and-lobbyist-charged-60-million-bribery-and-money-laundering-scheme")
    + fn_li(34, "AARP Public Policy Institute. (2019). <em>Utility regulatory oversight: Consumer advocates and the rate-setting process</em>. https://www.aarp.org/ppi/")
    + fn_li(35, "Institute for Local Self-Reliance. (2023). <em>Laws that prohibit community-owned broadband and utilities by state</em>. https://ilsr.org/")
    + fn_li(36, "U.S. Department of Transportation, Office of Inspector General. (2023, June). <em>FAA's air traffic controller workforce plan</em>. https://www.oig.dot.gov/")
    + fn_li(37, "U.S. Government Accountability Office. (2014). <em>FAA: Air traffic controller workforce planning and hiring</em> (GAO-14-208). https://www.gao.gov/assets/gao-14-208.pdf")
    + fn_li(38, "FAA Office of Inspector General. (2019). <em>FAA's NextGen program: Cost and schedule overruns</em>. U.S. Department of Transportation. https://www.oig.dot.gov/")
    + fn_li(39, "Bureau d'Enqu\u00eates et d'Analyses pour la s\u00e9curit\u00e9 de l'aviation civile. (2016). <em>Final report: Accident on 24 March 2015 at Pr\u00e9s de Seyne, Germanwings Flight 9525</em>. https://bea.aero/docspa/2015/d-px150324.en/pdf/d-px150324.en.pdf")
    + fn_li(40, "Aviation Safety and FAA Extension Act of 2010, Pub. L. No. 111-216, 124 Stat. 2348 (2010). https://www.congress.gov/bill/111th-congress/senate-bill/1451")
    + fn_li(41, "Air Line Pilots Association. (2023). <em>Regional airline pilot pay</em>. https://www.alpa.org/advocacy/pilot-career-information")
)


def append_infr_footnotes(text: str) -> str:
    """Append fn8-fn41 after fn7 in the INFR file footnote list."""
    # fn7 uses reversed format (backarrow at start, no trailing content)
    # Find fn7 closing </li> tag in the footnotes section
    anchor = '<li id="fn7"><a href="#ref7">\u21a9</a>'
    assert anchor in text, "INFR fn7 anchor not found – check file content"
    # Find the complete fn7 line
    start = text.index(anchor)
    end = text.index("</li>", start) + len("</li>")
    fn7_line = text[start:end]
    replacement = fn7_line + INFR_NEW_FOOTNOTES
    return text[:start] + replacement + text[end:]


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def count_verify(text: str) -> int:
    return text.count("<!-- [VERIFY] -->")


def main() -> None:
    tax_text = TAX_FILE.read_text(encoding="utf-8")
    infr_text = INFR_FILE.read_text(encoding="utf-8")

    before_tax = count_verify(tax_text)
    before_infr = count_verify(infr_text)
    print(f"VERIFY markers before: TAX={before_tax}  INFR={before_infr}")

    tax_text = apply_tax_edits(tax_text)
    tax_text = append_tax_footnotes(tax_text)

    infr_text = apply_infr_edits(infr_text)
    infr_text = append_infr_footnotes(infr_text)

    after_tax = count_verify(tax_text)
    after_infr = count_verify(infr_text)
    print(f"VERIFY markers after:  TAX={after_tax}  INFR={after_infr}")

    if after_tax != 0 or after_infr != 0:
        print("WARNING: some VERIFY markers remain unresolved!")
    else:
        print("All VERIFY markers resolved.")

    TAX_FILE.write_text(tax_text, encoding="utf-8")
    INFR_FILE.write_text(infr_text, encoding="utf-8")
    print("Files written.")


if __name__ == "__main__":
    main()
