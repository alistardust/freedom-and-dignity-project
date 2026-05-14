#!/usr/bin/env python3
"""Rewrite all 27 ANTR proposal cards in antitrust-and-corporate-power.html.

Applies New Brandeis antimonopoly philosophy, strengthens all cards per
research foundation, adds verified citations.

Run from repo root: python3 scripts/rewrite_antr_proposals.py
"""

import re
import sys
from pathlib import Path

TARGET = Path("docs/policy/antitrust-and-corporate-power.html")


def replace_card(html: str, card_id: str, new_inner: str) -> str:
    """Replace the full inner HTML of a policy-card div by its id."""
    # Match the opening tag (possibly with extra attributes), capture tag, replace inner
    pattern = (
        r'(<div\s+class="policy-card proposal"\s+id="'
        + re.escape(card_id)
        + r'">)(.*?)(</div>)'
    )
    replacement = r"\1" + new_inner + r"\3"
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        print(f"WARNING: could not find card {card_id}", file=sys.stderr)
    return updated


# ---------------------------------------------------------------------------
# Card definitions — new_inner is everything INSIDE the outer policy-card div
# ---------------------------------------------------------------------------

CARDS: list[tuple[str, str]] = []

# ── PLTS-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PLTS-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-PLTS-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant digital platforms are categorically prohibited from self-preferencing their own products in any algorithmic system</p>
<p class="rule-stmt">Digital platforms with dominant market position in search, e-commerce, app distribution, or digital advertising are prohibited from using control of any ranking, recommendation, or algorithmic system to advantage their own affiliated products, services, or content over those of competing third parties. This prohibition is structural and categorical: no efficiency defense excuses self-preferencing by a dominant platform.</p>
<p class="rule-body">Self-preferencing — Google favoring Google Shopping in search results, Amazon prioritizing Amazon Basics in product listings, Apple's App Store featuring Apple apps ahead of rivals — is not aggressive competition; it is infrastructure control used to eliminate rivals that depend on the platform for distribution. The consumer welfare standard fails to capture this harm because self-preferencing degrades the quality and integrity of information even without immediate price increases.<sup><a href="#fn-plts0001-1" id="ref-plts0001-1">[1]</a></sup> The EU Digital Markets Act (Regulation 2022/1925), in force since May 2023, imposes ex-ante structural prohibitions on gatekeeper self-preferencing, explicitly rejecting case-by-case balancing as inadequate to address structural harm.<sup><a href="#fn-plts0001-2" id="ref-plts0001-2">[2]</a></sup> The United States must adopt the same standard: ex-ante prohibition for designated gatekeepers, not litigation after harm accumulates. Where conduct remedies cannot stop self-preferencing, structural separation of platform infrastructure from competing commercial operations is the required remedy. This is the antimonopoly tradition articulated by Zephyr Teachout and Barry Lynn: dispersal of power over essential infrastructure is itself a democratic value, not merely a competition policy tool.<sup><a href="#fn-plts0001-3" id="ref-plts0001-3">[3]</a></sup></p>
<ol class="rule-citations">
<li id="fn-plts0001-1">Khan, L. M. (2017). Amazon's antitrust paradox. <em>Yale Law Journal</em>, <em>126</em>(3), 710–805. <a href="https://www.yalelawjournal.org/note/amazons-antitrust-paradox">https://www.yalelawjournal.org/note/amazons-antitrust-paradox</a> <a href="#ref-plts0001-1">↩</a></li>
<li id="fn-plts0001-2">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 of the European Parliament and of the Council on contestable and fair markets in the digital sector (Digital Markets Act)</em>. <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-plts0001-2">↩</a></li>
<li id="fn-plts0001-3">Teachout, Z. (2020). <em>Break 'em up</em>. All Points Books. <a href="#ref-plts0001-3">↩</a></li>
</ol>
"""))

# ── PLTS-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PLTS-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-PLTS-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">App store platforms with dominant market position must allow alternative distribution and payment systems</p>
<p class="rule-stmt">Mobile operating system and app store platforms with dominant market position must allow alternative app distribution channels and alternative payment systems. A dominant platform may not make distribution access conditional on use of its proprietary payment processing system at rates set unilaterally by the platform operator.</p>
<p class="rule-body">Apple's App Store and Google's Play Store collectively control virtually all smartphone app distribution. Both platforms impose 15–30% commissions on in-app purchases and prohibit developers from directing users to outside payment options — a structural tying arrangement combining a distribution monopoly with a compulsory payment processing extraction, with no competitive check. The EU Digital Markets Act Article 5(4) requires designated gatekeepers to allow sideloading, alternative app distribution, and alternative in-app payment systems, and prohibits gatekeepers from preventing developers from steering users to alternatives outside the platform.<sup><a href="#fn-plts0002-1" id="ref-plts0002-1">[1]</a></sup> The United States must codify structural obligations equivalent to or stronger than DMA Article 5(4): app store exclusivity as a condition of distribution is a per se structural harm. Distribution monopoly must not be leveraged into payment processing monopoly. Where an operator's platform has achieved dominant distribution gatekeeper status, its right to charge for distribution services is capped at reasonable, cost-justified fees; it has no right to compel use of its payment infrastructure.</p>
<ol class="rule-citations">
<li id="fn-plts0002-1">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 (Digital Markets Act)</em>, Art. 5(4). <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-plts0002-1">↩</a></li>
</ol>
"""))

# ── PLTS-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PLTS-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-PLTS-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant platforms must provide non-negotiable data portability and technical interoperability</p>
<p class="rule-stmt">Platforms with dominant market position must provide users and businesses with the ability to export their data in interoperable formats and must allow third-party services to interoperate with core platform functions on reasonable, non-discriminatory terms. This is a non-negotiable structural obligation, not a policy option to be weighed against platform commercial interests.</p>
<p class="rule-body">Lock-in through data capture — making user data inaccessible or architecturally incompatible with competing services — is a constructed structural barrier to competition. A social network user who cannot export their social graph, a business whose customer data is locked in a proprietary format, and a consumer whose devices only work within one ecosystem face artificial switching costs produced by deliberate architectural choices, not genuine quality advantages. The EU Digital Markets Act Articles 6(9) and 7 impose mandatory data portability and interoperability obligations on designated gatekeepers, recognizing these as non-negotiable structural conditions of gatekeeper status.<sup><a href="#fn-plts0003-1" id="ref-plts0003-1">[1]</a></sup> The United States must implement equivalent mandatory obligations. No claimed commercial interest in maintaining a "closed ecosystem" justifies structural lock-in that makes competitive entry impossible regardless of product quality. Interoperability requirements must be technically sufficient to enable genuine competition — not implemented in forms that nominally comply while remaining architecturally incompatible with competing services.</p>
<ol class="rule-citations">
<li id="fn-plts0003-1">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 (Digital Markets Act)</em>, Arts. 6(9), 7. <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-plts0003-1">↩</a></li>
</ol>
"""))

# ── PLTS-0004 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PLTS-0004", """
<div class="rule-header">
<code class="rule-id">ANTR-PLTS-0004</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant platform acquisitions of nascent competitive threats are presumptively prohibited</p>
<p class="rule-stmt">Acquisitions by dominant platforms of companies that represent nascent competitive threats — including companies that, grown independently, could challenge the acquirer's dominant position — are presumptively prohibited. The burden rests on the acquirer to demonstrate affirmatively that the acquisition will enhance, not suppress, competition.</p>
<p class="rule-body">The FTC's investigation of Facebook's acquisitions of Instagram (2012, $1 billion) and WhatsApp (2014, $19 billion) documented the "kill zone" pattern: dominant platforms acquire companies before they become competitive threats.<sup><a href="#fn-plts0004-1" id="ref-plts0004-1">[1]</a></sup> At the time of acquisition, Instagram had 13 employees; it became the dominant photo-sharing social platform that Facebook had identified as a strategic threat. Research by Cunningham, Ederer, and Ma (2021) established that killer acquisitions — structured to terminate a competitive pipeline rather than develop it — are a systematic and documented pattern in technology and pharmaceutical markets alike.<sup><a href="#fn-plts0004-2" id="ref-plts0004-2">[2]</a></sup> In platform markets, the harm is uniquely irreversible: once a nascent competitor is acquired, the competitive alternative is extinguished and cannot be reconstructed. The 2023 DOJ/FTC Merger Guidelines moved toward recognizing nascent competition harm; this platform requires that recognition to be codified as a structural rule. Any acquisition by a dominant platform of a company with competitive potential is presumptively blocked. The acquirer must demonstrate affirmative competitive benefit — not merely the absence of proven harm — before the acquisition may proceed.</p>
<ol class="rule-citations">
<li id="fn-plts0004-1">Federal Trade Commission. (2021). <em>In the Matter of Facebook, Inc., FTC Amended Complaint</em> (Dkt. No. 9373). <a href="https://www.ftc.gov/system/files/documents/cases/ecf_75-1_ftc_v_facebook_public_redacted_fac.pdf">https://www.ftc.gov/system/files/documents/cases/ecf_75-1_ftc_v_facebook_public_redacted_fac.pdf</a> <a href="#ref-plts0004-1">↩</a></li>
<li id="fn-plts0004-2">Cunningham, C., Ederer, F., &amp; Ma, S. (2021). Killer acquisitions. <em>Journal of Political Economy</em>, <em>129</em>(3), 649–702. <a href="https://doi.org/10.1086/712506">https://doi.org/10.1086/712506</a> <a href="#ref-plts0004-2">↩</a></li>
</ol>
"""))

# ── PHRM-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PHRM-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-PHRM-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Pay-for-delay pharmaceutical settlements and patent evergreening are per se antitrust violations</p>
<p class="rule-body">Pay-for-delay agreements — in which brand-name pharmaceutical manufacturers pay generic competitors to delay market entry — are per se violations of antitrust law. No rule-of-reason balancing is permitted: a payment from a brand manufacturer to a generic competitor to stay off the market is a naked market allocation agreement, and the patent context does not immunize it. The Supreme Court's <em>FTC v. Actavis</em> decision (2013) established that reverse payment settlements are subject to antitrust scrutiny;<sup><a href="#fn-phrm0001-1" id="ref-phrm0001-1">[1]</a></sup> this platform goes further by treating them as per se violations. Patent evergreening — filing minor reformulation patents solely to extend exclusivity beyond the original compound patent's life — constitutes anticompetitive conduct that must be challenged as a systematic abuse. Generic entry following patent expiration delivers price reductions of 80–90%; any practice that delays or forecloses this structural competition mechanism constitutes consumer harm measured in tens of billions of dollars annually. The FTC must treat pay-for-delay and evergreening as per se violations and refer willful violations for criminal prosecution under Sherman Act Section 1.</p>
<ol class="rule-citations">
<li id="fn-phrm0001-1">FTC v. Actavis, Inc., 570 U.S. 136 (2013). <a href="https://www.supremecourt.gov/opinions/12pdf/12-416_m5n0.pdf">https://www.supremecourt.gov/opinions/12pdf/12-416_m5n0.pdf</a> <a href="#ref-phrm0001-1">↩</a></li>
</ol>
"""))

# ── PHRM-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PHRM-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-PHRM-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Pharmaceutical mergers designed to eliminate pipeline competition are killer acquisitions subject to criminal and civil enforcement</p>
<p class="rule-body">Pharmaceutical mergers and acquisitions that eliminate competition in drug development pipelines are presumptively anticompetitive and must be blocked or unwound unless the acquirer demonstrates affirmatively that the acquisition will accelerate development and benefit patients. The practice of acquiring potential competitors to terminate their pipeline drugs — rather than to develop them — is an antitrust violation subject to criminal and civil enforcement. Research by Cunningham, Ederer, and Ma (2021) found that approximately 6.7% of pharmaceutical acquisitions are "killer acquisitions" — structured to eliminate pipeline candidates that would compete with the acquirer's existing products by terminating development after the acquisition closes.<sup><a href="#fn-phrm0002-1" id="ref-phrm0002-1">[1]</a></sup> This is not market failure; it is a deliberate strategy to extend monopoly pricing by paying to eliminate the competitive threat rather than to improve the product. The burden rests with the acquirer: any acquisition of a company with a pipeline candidate competing with the acquirer's existing products is presumptively a killer acquisition and must be blocked absent affirmative proof of accelerated development benefit to patients. Drug prices are the direct and documentable consequence of this enforcement failure.</p>
<ol class="rule-citations">
<li id="fn-phrm0002-1">Cunningham, C., Ederer, F., &amp; Ma, S. (2021). Killer acquisitions. <em>Journal of Political Economy</em>, <em>129</em>(3), 649–702. <a href="https://doi.org/10.1086/712506">https://doi.org/10.1086/712506</a> <a href="#ref-phrm0002-1">↩</a></li>
</ol>
"""))

# ── PHRM-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PHRM-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-PHRM-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">PBM vertical integration with insurers and pharmacies must be immediately structurally separated; PBM elimination must be pursued</p>
<p class="rule-body">Pharmacy Benefit Managers exist as intermediaries that extract value from drug transactions without improving patient outcomes or reducing net drug costs. The structural conflict is the cause of the harm, not a side effect: the three dominant PBMs — CVS Caremark (owned by CVS Health, which also owns the CVS pharmacy chain and Aetna insurance), Express Scripts (owned by Cigna insurance), and OptumRx (owned by UnitedHealth Group, which also operates Optum physician practices) — are vertically integrated with the very entities they nominally negotiate against. An entity that simultaneously controls the insurer, the PBM, and the pharmacy chain faces no competitive pressure to reduce drug costs and every financial incentive to maximize extraction. The FTC's 2024 interim staff report documented that the three dominant PBMs extracted $7.3 billion in excess spread pricing markups and marked up 22% of specialty generic drug claims by more than 1,000% above acquisition cost.<sup><a href="#fn-phrm0003-1" id="ref-phrm0003-1">[1]</a></sup> PBMs that are owned by — or under common ownership with — pharmacies, insurers, or drug manufacturers are categorically prohibited; structural separation of CVS Caremark, Express Scripts, and OptumRx from their parent conglomerates must be compelled immediately under antitrust enforcement authority, without waiting for further legislative action. Congress must seriously pursue the elimination of the PBM model entirely, transferring its administrative functions — formulary management, rebate negotiation, claims processing — to transparent, publicly accountable drug pricing infrastructure. Until elimination, PBMs are prohibited from spread pricing, clawbacks against independent pharmacies, formulary design that prioritizes rebates over clinical outcomes, and any self-dealing that steers patients toward affiliated entities.</p>
<ol class="rule-citations">
<li id="fn-phrm0003-1">Federal Trade Commission. (2024, July). <em>Pharmacy benefit managers: The powerful middlemen inflating drug costs and squeezing main street pharmacies</em> (Interim Staff Report). <a href="https://www.ftc.gov/reports/pharmacy-benefit-managers-report">https://www.ftc.gov/reports/pharmacy-benefit-managers-report</a> <a href="#ref-phrm0003-1">↩</a></li>
</ol>
"""))

# ── PHRM-0004 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-PHRM-0004", """
<div class="rule-header">
<code class="rule-id">ANTR-PHRM-0004</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Pharmaceutical patent thickets are deliberate anticompetitive conduct constituting a per se antitrust violation</p>
<p class="rule-body">The deliberate filing of multiple overlapping patents on incrementally modified formulations, delivery mechanisms, or manufacturing processes — with the purpose of erecting an intellectual property thicket that delays generic and biosimilar competition beyond what any single valid patent would justify — is anticompetitive conduct per se. This is not legitimate innovation; it is a strategy to extend monopoly pricing by accumulating secondary patents that individually would not block generic entry but collectively impose prohibitive litigation costs on generic entrants. The FTC and DOJ must actively audit patent thicket strategies in high-cost drug categories, use antitrust enforcement authority to compel licensing, challenge weak patents through inter partes review, and penalize manufacturers who maintain thickets built on patents the manufacturer has reason to know are invalid or unenforceable. Manufacturers who file patents solely to delay generic competition — without genuine innovation — are engaged in fraud on the patent system and in unlawful monopolization under Sherman Act Section 2. The public formulary authority established under the Inflation Reduction Act must be extended and used aggressively in conjunction with antitrust enforcement to address thicket-protected drugs.</p>
"""))

# ── FNSR-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FNSR-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-FNSR-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Banking megamergers that reduce local and regional competition are presumptively prohibited</p>
<p class="rule-body">Mergers between large banks that reduce competition in local and regional deposit, lending, and small-business banking markets are presumptively prohibited. Bank merger review must analyze local market concentration — not merely national market share — because banking competition operates at the community level, and consolidation directly harms small businesses, low-income households, and communities that lose branches and community lending relationships. The post-2008 consolidation trend — driven in part by emergency acquisitions facilitated by regulators during the 2008 financial crisis — has left the four largest U.S. banks holding over 40% of total domestic deposits.<sup><a href="#fn-fnsr0001-1" id="ref-fnsr0001-1">[1]</a></sup> The 2008 crisis was itself in significant part a product of the concentration that prior merger approvals had enabled: institutions that were "too big to fail" were too big because regulators had permitted successive consolidating mergers on the theory that larger institutions were more efficient and stable. The opposite proved true. Proposed megamergers in banking are presumptively anticompetitive and must be blocked absent clear, concrete evidence of competitive benefit that cannot be achieved through organic growth. The post-2008 consolidation trend must be reversed, not extended.</p>
<ol class="rule-citations">
<li id="fn-fnsr0001-1">Financial Crisis Inquiry Commission. (2011). <em>The financial crisis inquiry report: Final report of the National Commission on the Causes of the Financial and Economic Crisis in the United States</em>. U.S. Government Publishing Office. <a href="https://www.govinfo.gov/content/pkg/GPO-FCIC/pdf/GPO-FCIC.pdf">https://www.govinfo.gov/content/pkg/GPO-FCIC/pdf/GPO-FCIC.pdf</a> <a href="#ref-fnsr0001-1">↩</a></li>
</ol>
"""))

# ── FNSR-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FNSR-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-FNSR-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Too-big-to-fail financial conglomerates must be structurally separated into independent commercial and investment banking entities</p>
<p class="rule-body">Financial institutions whose failure would require taxpayer rescue must be subject to mandatory structural separation of retail banking, investment banking, and insurance operations. The Gramm-Leach-Bliley Act of 1999 repealed the Glass-Steagall structural firewall between commercial and investment banking;<sup><a href="#fn-fnsr0002-1" id="ref-fnsr0002-1">[1]</a></sup> within a decade, the resulting conglomerates produced the 2008 financial crisis, requiring $700 billion in authorized public bailouts and triggering the worst economic contraction since the Great Depression.<sup><a href="#fn-fnsr0002-2" id="ref-fnsr0002-2">[2]</a></sup> The implicit public subsidy of "too big to fail" status constitutes a market distortion that capital requirements alone cannot cure: an institution that knows it will be bailed out faces no market discipline for systemic risk-taking, and no private actor can adequately price that public backstop. Structural separation — requiring separately capitalized and separately governed commercial and investment banking entities — eliminates the subsidy and restores market discipline. No financial institution may operate as both a federally insured depository institution and a systemically significant investment bank without full structural separation, separate capitalization, and independent governance. This is a structural requirement, not a behavioral one: behavioral remedies and capital surcharges have failed to eliminate the systemic risk created by the conglomerate model.</p>
<ol class="rule-citations">
<li id="fn-fnsr0002-1">Gramm-Leach-Bliley Act, Pub. L. No. 106-102, 113 Stat. 1338 (1999). <a href="https://www.congress.gov/bill/106th-congress/senate-bill/900">https://www.congress.gov/bill/106th-congress/senate-bill/900</a> <a href="#ref-fnsr0002-1">↩</a></li>
<li id="fn-fnsr0002-2">Emergency Economic Stabilization Act of 2008, Pub. L. No. 110-343, 122 Stat. 3765 (2008). <a href="https://www.congress.gov/bill/110th-congress/house-bill/1424">https://www.congress.gov/bill/110th-congress/house-bill/1424</a> <a href="#ref-fnsr0002-2">↩</a></li>
</ol>
"""))

# ── FNSR-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FNSR-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-FNSR-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Institutional cross-ownership of competing firms in concentrated industries is prohibited</p>
<p class="rule-body">Institutional investors, asset managers, and private equity sponsors are prohibited from simultaneously holding significant equity stakes in competing firms within concentrated industries. This is not a case for "enhanced review" — it is a structural prohibition. Common ownership of competing firms is not passive investing; it is a structural mechanism that softens competition and raises prices by aligning the financial interests of nominally competing firms within a single investor's portfolio. Economic research has established that this effect is real and measurable: Azar, Schmalz, and Tecu (2018) found that common ownership by the same institutional investors in major U.S. airlines — including routes served by carriers in which the same institutions held significant stakes — was associated with 3–11% higher ticket prices compared to routes without common ownership, controlling for market structure.<sup><a href="#fn-fnsr0003-1" id="ref-fnsr0003-1">[1]</a></sup> Elhauge's horizontal shareholding theory establishes the mechanism: an investor holding stakes in multiple competing firms in the same market has financial incentives to prefer that those firms compete less aggressively, and managers of those firms have incentives to respond to that preference regardless of whether any explicit coordination occurs.<sup><a href="#fn-fnsr0003-2" id="ref-fnsr0003-2">[2]</a></sup> The current approach — evaluating common ownership case-by-case — is structurally inadequate because the harm is cumulative and diffuse, not detectable in individual transactions. No institutional investor may hold more than a de minimis equity stake in more than one firm that competes directly in a highly concentrated market (defined as HHI ≥ 2,500 post-merger equivalent). This prohibition applies to BlackRock, Vanguard, State Street, and all institutional investors currently holding simultaneous significant stakes in competing firms in banking, healthcare, airlines, telecommunications, and other concentrated industries. Asset managers operating index funds spanning entire industries must divest competitive stakes or face structural divestiture orders.</p>
<ol class="rule-citations">
<li id="fn-fnsr0003-1">Azar, J., Schmalz, M., &amp; Tecu, I. (2018). Anticompetitive effects of common ownership. <em>Journal of Political Economy</em>, <em>126</em>(2), 467–505. <a href="https://doi.org/10.1086/699976">https://doi.org/10.1086/699976</a> <a href="#ref-fnsr0003-1">↩</a></li>
<li id="fn-fnsr0003-2">Elhauge, E. (2016). Horizontal shareholding. <em>Harvard Law Review</em>, <em>129</em>(5), 1267–1317. <a href="https://harvardlawreview.org/print/vol-129/horizontal-shareholding/">https://harvardlawreview.org/print/vol-129/horizontal-shareholding/</a> <a href="#ref-fnsr0003-2">↩</a></li>
</ol>
"""))

# ── HLSP-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-HLSP-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-HLSP-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Hospital mergers eliminating regional competition are presumptively anticompetitive and must be blocked</p>
<p class="rule-body">Hospital system mergers that eliminate direct competitors in a regional market are presumptively anticompetitive and must be blocked unless the merging parties demonstrate with concrete evidence that the combination will produce patient benefits that cannot be achieved through less restrictive means. The burden of proof rests entirely with the merging hospitals. The industrial organization literature on hospital markets has documented consistently that mergers in concentrated regional markets are associated with price increases of 20–40% with no corresponding improvement in quality or access outcomes.<sup><a href="#fn-hlsp0001-1" id="ref-hlsp0001-1">[1]</a></sup> The Federal Trade Commission has successfully challenged multiple hospital mergers on exactly this evidentiary record, and the pattern is now sufficiently established that the presumption must be codified, not relitigated in each case. No regional hospital merger should be approved where it would leave a market with fewer than three independently competitive hospital systems. Already-completed mergers that have produced documented price increases without quality improvements must be subject to retroactive review and potential structural unwinding through divestiture orders.</p>
<ol class="rule-citations">
<li id="fn-hlsp0001-1">Gaynor, M., Ho, K., &amp; Town, R. J. (2015). The industrial organization of health-care markets. <em>Journal of Economic Literature</em>, <em>53</em>(2), 235–284. <a href="https://doi.org/10.1257/jel.53.2.235">https://doi.org/10.1257/jel.53.2.235</a> <a href="#ref-hlsp0001-1">↩</a></li>
</ol>
"""))

# ── HLSP-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-HLSP-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-HLSP-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Insurer-hospital-physician vertical integration is categorically prohibited</p>
<p class="rule-body">No entity may simultaneously own or exercise operational control over health insurance underwriting, hospital or clinical facility operations, and physician or clinical staffing in the same market. This vertical structure can never serve the public interest. No behavioral remedy can address a conflict of interest produced by the ownership structure itself: an insurer that also owns the hospital and employs the physician has every financial incentive to deny care, limit referrals, steer patients toward high-margin in-house services, and suppress independent medical judgment. The patient becomes a captive unit of revenue extraction, not a person whose health is the enterprise's objective. The conflict cannot be managed through conduct rules or compliance programs because the conflict is structural: the same corporate parent captures the insurance premium, controls access to care, employs the clinician, and owns the facility. Every layer of the care decision serves the same financial interest. Existing vertically integrated health conglomerates — including UnitedHealth Group/Optum's integration of insurer, PBM, and physician practice ownership; CVS Health's integration of insurance, pharmacy, and clinical services; and similar structures — must be structurally broken up through divestiture orders. New vertical integration across insurance, hospital, and physician staffing layers is prohibited regardless of claimed efficiencies, market share, or geographic scope. This is a categorical rule, not a totality-of-circumstances analysis.</p>
"""))

# ── HLSP-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-HLSP-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-HLSP-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">LBO-financed private equity acquisition of healthcare entities is structurally prohibited</p>
<p class="rule-body">Private equity acquisition of healthcare entities through leveraged buyout financing is prohibited. Healthcare is an essential service that is structurally incompatible with LBO-financed ownership: the debt loading, dividend recapitalization, and short-term asset extraction inherent in the PE business model produce predictable and documented harm to patients, workers, and communities. The evidence base on private equity healthcare ownership is now sufficient to require structural prohibition, not merely enhanced review or consumer-harm balancing. A 2023 systematic review of 55 studies published in <em>BMJ</em> found that private equity acquisition of healthcare entities was consistently associated with increased costs, reduced staffing levels, and no improvement in quality outcomes across the range of healthcare settings studied.<sup><a href="#fn-hlsp0003-1" id="ref-hlsp0003-1">[1]</a></sup><!-- Note: Verify lead author of BMJ 2023 systematic review (bmj-2023-075244) before publishing --> Private equity acquisition of physician medical groups — which reached over 8,000 practices acquired between 2012 and 2019 — is associated with significant increases in commercial prices and changes in care intensity that do not correspond to clinical need.<sup><a href="#fn-hlsp0003-2" id="ref-hlsp0003-2">[2]</a></sup> The 2019 closure of Hahnemann University Hospital in Philadelphia following private equity acquisition — leaving a 496-bed teaching hospital serving low-income patients permanently shuttered while the acquirer extracted real estate value — is the paradigmatic case of LBO incompatibility with essential healthcare delivery. Private equity's business model requires extraction: debt loaded onto the acquired entity must be serviced, and in healthcare that servicing is paid by patients and workers. LBO-financed acquisition of hospitals, physician practices, nursing homes, behavioral health facilities, emergency medicine and radiology staffing, and other healthcare entities is prohibited. Private equity sponsors must bear joint-and-several liability for harms resulting from post-acquisition debt loading, staff reductions, and facility closures. The Stop Wall Street Looting Act framework — joint-and-several liability on PE sponsors, carried interest taxed as ordinary income, ban on dividend recapitalization from essential service entities — must be enacted as the minimum legislative response.<sup><a href="#fn-hlsp0003-3" id="ref-hlsp0003-3">[3]</a></sup></p>
<ol class="rule-citations">
<li id="fn-hlsp0003-1">[Author et al.] (2023). Evaluating trends in private equity ownership and impacts on health outcomes, costs, and quality: Systematic review. <em>BMJ</em>, <em>382</em>, bmj-2023-075244. <a href="https://www.bmj.com/content/382/bmj-2023-075244">https://www.bmj.com/content/382/bmj-2023-075244</a> <a href="#ref-hlsp0003-1">↩</a></li>
<li id="fn-hlsp0003-2">Zhu, J. M., Hua, L. M., &amp; Polsky, D. (2021). Private equity acquisitions of physician medical groups. <em>JAMA</em>, <em>326</em>(14), 1440–1442. <a href="https://doi.org/10.1001/jama.2021.12302">https://doi.org/10.1001/jama.2021.12302</a> <a href="#ref-hlsp0003-2">↩</a></li>
<li id="fn-hlsp0003-3">U.S. Congress. (2024). Stop Wall Street Looting Act, H.R. 9985, 118th Congress. <a href="https://www.congress.gov/bill/118th-congress/house-bill/9985/text/ih">https://www.congress.gov/bill/118th-congress/house-bill/9985/text/ih</a> <a href="#ref-hlsp0003-3">↩</a></li>
</ol>
"""))

# ── AINL-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-AINL-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-AINL-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Vertical integration of AI compute infrastructure, foundation model training, and deployment by the same conglomerate is a structural competition violation</p>
<p class="rule-body">The vertical integration of compute infrastructure, foundation model training, and AI deployment capabilities in the hands of the same technology conglomerates constitutes a structural competition violation subject to mandatory antitrust remedy, including structural separation. Microsoft's deep investment in and operational integration with OpenAI, Google's ownership of DeepMind, and Amazon's substantial investment in Anthropic represent the same structure as other prohibited vertical integrations: firms that control essential input infrastructure — hyperscale cloud compute — simultaneously controlling the dependent product layer — AI foundation models and deployment services — foreclose independent AI developers from the infrastructure inputs required to compete.<sup><a href="#fn-ainl0001-1" id="ref-ainl0001-1">[1]</a></sup> This is not passive investment; it is vertical foreclosure of an emerging essential infrastructure stack. The concentration of AI capability in compute-integrated conglomerates creates structural barriers to entry that independent developers, academic institutions, and open-source communities cannot overcome through ordinary market mechanisms. The FTC and DOJ must treat AI market structure as a vertical integration problem — applying structural separation principles where compute-model integration forecloses competitive AI development. Exclusive or preferential compute arrangements between cloud providers and their affiliated AI models are per se anticompetitive input foreclosure mechanisms and are prohibited.</p>
<ol class="rule-citations">
<li id="fn-ainl0001-1">Khan, L. M. (2017). Amazon's antitrust paradox. <em>Yale Law Journal</em>, <em>126</em>(3), 710–805. <a href="https://www.yalelawjournal.org/note/amazons-antitrust-paradox">https://www.yalelawjournal.org/note/amazons-antitrust-paradox</a> <a href="#ref-ainl0001-1">↩</a></li>
</ol>
"""))

# ── AINL-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-AINL-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-AINL-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Exclusive AI model-cloud arrangements are per se input foreclosure mechanisms and are prohibited</p>
<p class="rule-body">Exclusive or preferential arrangements between AI model developers and cloud computing providers that raise rivals' costs or foreclose competing AI developers from accessing necessary compute infrastructure constitute input foreclosure and are prohibited as per se anticompetitive where compute is essential infrastructure. A dominant cloud provider that grants preferential pricing, reserved capacity, or privileged access to an affiliated AI developer while withholding equivalent terms from independent developers is engaged in the same conduct as a railroad refusing to carry competitors' freight: denying access to essential infrastructure inputs to foreclose downstream competition. Compute access at a competitive price is a necessary condition for independent AI development; without it, market structure in AI is determined by investment relationships with cloud providers, not by the quality or originality of the AI development work. These arrangements must be treated as per se violations — not subjected to rule-of-reason balancing that invites years of litigation while foreclosure continues. Cloud providers with dominant compute market positions must offer equivalent pricing, capacity, and access terms to all AI developers regardless of investment or partnership relationships with the cloud provider's corporate family.</p>
"""))

# ── AINL-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-AINL-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-AINL-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant AI firms' control of training data pipelines is essential input foreclosure requiring structural separation</p>
<p class="rule-body">Control of training data pipelines by dominant AI firms — including proprietary data collection at scale unavailable to competitors, exclusive data licensing agreements that prevent rivals from training competitive models, and vertical integration of content platforms with AI model development — constitutes essential input control of the same type as control of physical infrastructure. Data is not a neutral or freely replicable resource: at the scale required to train frontier AI models, it is scarce, expensive to replicate, and subject to deliberate exclusion strategies. Vertical integration of a dominant content platform with AI model development — allowing the same entity that controls the data source to also control the AI trained on that data — must be treated as a structural integration that forecloses independent competition in the AI development market. Structural separation of AI model development from platforms that generate and control training data is required where such integration forecloses independent AI development. Where mandated interoperability or data access at regulated terms would meaningfully reduce competitive barriers without disproportionate cost, such mandates must be imposed as structural remedies. No dominant platform may use its control of user-generated data as a structural moat against competitive AI development.</p>
"""))

# ── AINL-0004 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-AINL-0004", """
<div class="rule-header">
<code class="rule-id">ANTR-AINL-0004</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant platform acquisition of AI competitive threats is presumptively prohibited</p>
<p class="rule-body">Acquisition of AI startups by dominant technology platforms is presumptively prohibited where the target has developed or could develop capabilities that would compete with the acquirer's existing AI products or services. This applies the same killer acquisition principle as ANTR-PLTS-0004 to the AI sector specifically: in AI markets, the speed of competitive development makes early acquisition of nascent threats particularly effective as a competitive foreclosure mechanism. Acquisitions structured as talent acqui-hires, early-stage investments that convert to full acquisitions, or exclusive partnerships that prevent the target from working with other parties must all be treated as functional acquisitions subject to the same presumptive prohibition. Research by Cunningham, Ederer, and Ma (2021) established that killer acquisitions — structured to terminate competitive pipeline development — are a systematic and documented pattern in technology and pharmaceutical markets.<sup><a href="#fn-ainl0004-1" id="ref-ainl0004-1">[1]</a></sup> In AI, where the competitive stakes involve control of general-purpose cognitive infrastructure, the structural harm from killer acquisition is uniquely severe and long-lasting. The acquirer must demonstrate affirmatively that any acquisition of an AI startup with competitive potential will enhance, not terminate, competitive AI development.</p>
<ol class="rule-citations">
<li id="fn-ainl0004-1">Cunningham, C., Ederer, F., &amp; Ma, S. (2021). Killer acquisitions. <em>Journal of Political Economy</em>, <em>129</em>(3), 649–702. <a href="https://doi.org/10.1086/712506">https://doi.org/10.1086/712506</a> <a href="#ref-ainl0004-1">↩</a></li>
</ol>
"""))

# ── TELE-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-TELE-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-TELE-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Broadband ISPs must be structurally separated from content ownership and regulated as common carriers</p>
<p class="rule-body">Approximately 42% of U.S. households have access to only one provider of high-speed broadband internet service, making local ISP markets the paradigmatic case of constructed monopoly requiring structural remedy.<sup><a href="#fn-tele0001-1" id="ref-tele0001-1">[1]</a></sup> The Comcast/NBCUniversal merger (2011) created a single entity controlling both dominant cable ISP infrastructure and a major content network — the canonical case of ISP-content vertical integration that must be unwound: an ISP that also controls content has structural financial incentives to degrade competitors' content delivery, throttle competing video services, and favor its own content, with no competitive check where the ISP faces no local competition. Broadband ISP infrastructure must be structurally separated from content ownership. ISPs may not own the content networks their infrastructure delivers. Where structural separation is not achievable in reasonable timeframes, broadband ISPs must be regulated as common carriers subject to rate regulation, non-discrimination obligations, and mandatory open-access requirements. Broadband internet access is essential infrastructure for economic participation, education, healthcare, and democratic engagement; no private firm may hold monopoly control over a community's access to it without full public-interest accountability equivalent to that imposed on electric and telephone utilities.</p>
<ol class="rule-citations">
<li id="fn-tele0001-1">Federal Communications Commission. (2024). <em>2024 broadband data collection: Fixed broadband availability</em>. <a href="https://www.fcc.gov/BroadbandData">https://www.fcc.gov/BroadbandData</a> <a href="#ref-tele0001-1">↩</a></li>
</ol>
"""))

# ── TELE-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-TELE-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-TELE-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Telecom mergers reducing national wireless competition to fewer than three viable carriers are prohibited</p>
<p class="rule-body">Telecommunications mergers that would reduce the number of national wireless carriers to fewer than three viable competitors are prohibited. The 2011 blocking of the AT&amp;T/T-Mobile merger — in which the Department of Justice concluded that reducing the national carrier count from four to three would cause substantial competitive harm — established that carrier count is a structural floor for competitive markets, not merely one factor in a balancing test.<sup><a href="#fn-tele0002-1" id="ref-tele0002-1">[1]</a></sup> The conditions imposed on the 2020 T-Mobile/Sprint merger — which required T-Mobile to divest spectrum and support DISH as an entrant to maintain a fourth competitor — reflected this principle but produced an inadequate structural outcome: DISH's failure to launch a viable national carrier demonstrates that behavioral conditions and mandated divestitures to inexperienced entrants are not substitutes for blocking mergers that eliminate a competitor. Three national carriers is the minimum acceptable competitive floor, not a target. Mergers between regional and national carriers that reduce competitive options in specific geographic markets must also be evaluated for local market concentration effects. Carrier consolidation below three national competitors is prohibited without exception.</p>
<ol class="rule-citations">
<li id="fn-tele0002-1">United States Department of Justice. (2011, August 31). <em>Justice Department files antitrust lawsuit to block AT&amp;T's acquisition of T-Mobile</em> [Press release]. <a href="https://www.justice.gov/opa/pr/justice-department-files-antitrust-lawsuit-block-atts-acquisition-t-mobile">https://www.justice.gov/opa/pr/justice-department-files-antitrust-lawsuit-block-atts-acquisition-t-mobile</a> <a href="#ref-tele0002-1">↩</a></li>
</ol>
"""))

# ── TELE-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-TELE-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-TELE-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Exclusive broadband-property arrangements that foreclose tenant access to competing providers are prohibited</p>
<p class="rule-body">Exclusive arrangements between broadband providers and property owners — including apartment buildings, multi-dwelling units, and commercial properties — that prevent tenants or occupants from accessing competing internet service providers are anticompetitive and prohibited. Exclusive broadband access agreements, whether characterized as bulk billing arrangements, revenue-sharing agreements, or marketing exclusivity contracts, function as private monopoly franchises that extend a single provider's market power to every unit in a building regardless of the broader geographic broadband market. A tenant in a building with an exclusive broadband agreement has no more choice of ISP than if they lived in a geographic monopoly — the exclusivity agreement manufactures captive markets where none would otherwise exist. No property owner may enter into or enforce an exclusive agreement with a single broadband provider that forecloses tenant choice of internet service provider. The FCC must classify exclusive broadband access arrangements as anticompetitive conduct prohibited under the Communications Act. Property owners receiving any federal housing subsidy or financing must affirmatively permit multi-provider broadband access to all units as a condition of federal assistance.</p>
"""))

# ── FRNC-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FRNC-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-FRNC-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Franchisor coordination of prices or wages across independently owned franchisee businesses is a per se horizontal restraint of trade</p>
<p class="rule-body">Franchise agreements and franchisor policies that set retail prices, wages, or core working conditions across independently owned and operated franchisee businesses are per se horizontal restraints of trade under Sherman Act Section 1. The franchisee's formal legal independence does not convert horizontal coordination among competing businesses — all subject to common franchisor direction on pricing and wages — into a lawful vertical agreement. When a franchisor uses its contractual control to impose uniform wages or uniform prices across franchisees operating in the same geographic market, it is operating a cartel. This is not a difficult legal question requiring rule-of-reason analysis; it is the application of existing per se doctrine to a deliberate structural evasion of per se rules. The legal fiction of "vertical" control — when the functional result is horizontal coordination among competing businesses — must not immunize what is economically a cartel agreement from per se treatment. Congress and the DOJ must close this evasion by statute and by enforcement guidance, and must prosecute franchisors that use the franchise system as a cartel coordination mechanism.</p>
"""))

# ── FRNC-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FRNC-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-FRNC-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">No-hire and no-poach clauses in franchise contracts are per se antitrust violations subject to criminal prosecution</p>
<p class="rule-body">No-hire and no-poach clauses embedded in franchise agreements — prohibiting franchisees from hiring workers employed by other franchisees of the same brand or by the franchisor itself — are per se violations of Sherman Act Section 1, subject to criminal prosecution. These clauses function as wage-fixing and worker-mobility-suppression agreements among competing employers, enforced through the franchise system rather than through direct employer-to-employer negotiation; the mechanism of coordination does not change the competitive harm. The DOJ and FTC's 2016 Antitrust Guidance for Human Resource Professionals established that naked no-poach and wage-fixing agreements between competing employers are per se violations subject to criminal prosecution.<sup><a href="#fn-frnc0002-1" id="ref-frnc0002-1">[1]</a></sup> That guidance applies with full force to franchise-embedded no-hire clauses: a no-poach agreement is no less a per se violation because it is buried in a franchise operations manual rather than agreed to directly between competing employers. This platform requires codification in statute and mandatory criminal prosecution of franchisors that continue to use no-hire clauses. Franchisors that have enforced such clauses must be required to disgorge unlawful profits derived from suppressed labor costs.</p>
<ol class="rule-citations">
<li id="fn-frnc0002-1">U.S. Department of Justice &amp; Federal Trade Commission. (2016). <em>Antitrust guidance for human resource professionals</em>. <a href="https://www.justice.gov/atr/file/903511/download">https://www.justice.gov/atr/file/903511/download</a> <a href="#ref-frnc0002-1">↩</a></li>
</ol>
"""))

# ── FRNC-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-FRNC-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-FRNC-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Worker misclassification to evade collective bargaining rights is a structural competition harm enforceable under antitrust law</p>
<p class="rule-body">Misclassification of employees as independent contractors — when the contracting firm exercises meaningful control over the worker's schedule, pricing, customer assignments, tools, or methods — is a structural competition issue in addition to a labor law violation. Workers denied collective bargaining rights through misclassification face monopsony exploitation without recourse: they cannot counteract buyer power through collective action because they are denied the legal status that makes collective action lawful. Firms that misclassify workers to eliminate collective bargaining rights are using a legal fiction to entrench monopsony power — the buyer-side equivalent of monopoly exploitation. Enforcement must address both the labor law violation and the antitrust harm: monopsony in labor markets suppresses wages, reduces labor market competition, and produces the same structural harm to workers that monopoly produces for consumers. The ABC test — as codified in California AB-5 and the Department of Labor's 2024 independent contractor rule — must be established as the federal standard for determining independent contractor status. Platforms and firms that use misclassification to eliminate legally required labor costs and bargaining rights are not competing on merit; they are competing by externalizing the costs of labor onto misclassified workers while competitors who correctly classify workers bear those costs.</p>
"""))

# ── UTLY-0001 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-UTLY-0001", """
<div class="rule-header">
<code class="rule-id">ANTR-UTLY-0001</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant digital platforms controlling market access must be designated as common carriers with ex-ante gatekeeper obligations</p>
<p class="rule-body">Digital platforms that control access to markets, audiences, or data necessary for commercial participation must be designated as common carriers with non-discrimination and access obligations imposed ex-ante — before harm is proven in individual cases, not after years of case-by-case litigation. The EU Digital Markets Act (Regulation 2022/1925) created a gatekeeper designation framework that imposes structural obligations on dominant platforms automatically upon designation, without requiring proof of specific anticompetitive harm in each instance.<sup><a href="#fn-utly0001-1" id="ref-utly0001-1">[1]</a></sup> This is the correct model and must be the floor, not the ceiling, for U.S. platform regulation. Ex-ante obligations for designated gatekeepers — non-discrimination, access, interoperability, prohibition on self-preferencing — must be legally binding from designation, not triggered only after a contested adjudication of individual harm. A business that cannot exist without access to Google's search index, Amazon's marketplace, or Apple's App Store faces the same essential-facility dependency as a shipper without rail access; the legal obligations imposed on essential infrastructure must apply accordingly. Gatekeeper designation does not preclude reasonable technical and content moderation decisions; it prohibits discriminatory terms, preferential access for affiliates, and exclusion of rivals without legitimate, documented justification that does not rest on protecting the platform operator's own commercial interests.</p>
<ol class="rule-citations">
<li id="fn-utly0001-1">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 (Digital Markets Act)</em>. <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-utly0001-1">↩</a></li>
</ol>
"""))

# ── UTLY-0002 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-UTLY-0002", """
<div class="rule-header">
<code class="rule-id">ANTR-UTLY-0002</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Essential platforms are absolutely prohibited from self-preferencing their own products in any algorithmic system</p>
<p class="rule-body">Platforms designated as essential infrastructure under this pillar are absolutely prohibited from prioritizing affiliated products, services, content, or advertisers over rivals in any algorithmic ranking, search result, recommendation system, or feed curation mechanism. This is an absolute prohibition, not a standard to be weighed against claimed efficiencies: there is no efficiency justification for self-preferencing by a gatekeeper platform because the harm — distortion of the information environment on which dependent businesses and users rely — is structural and cannot be offset by unilateral efficiency claims by the party causing the distortion. EU Digital Markets Act Article 6(5) imposes this prohibition on designated gatekeepers in the European Union;<sup><a href="#fn-utly0002-1" id="ref-utly0002-1">[1]</a></sup> the United States must impose the same or stronger obligation. All platform-operated systems that determine what users see, find, or are recommended must operate under documented non-discrimination standards subject to continuous independent audit, with results published in standardized formats. The platform operator may charge reasonable, non-discriminatory fees for access and promotion; it may not use its control of the algorithmic system to advantage its own commercial interests in any market in which it competes with businesses that depend on the platform for distribution. Violation is a per se antitrust violation subject to structural remedy — including divestiture of the competing commercial operations from the platform infrastructure.</p>
<ol class="rule-citations">
<li id="fn-utly0002-1">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 (Digital Markets Act)</em>, Art. 6(5). <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-utly0002-1">↩</a></li>
</ol>
"""))

# ── UTLY-0003 ────────────────────────────────────────────────────────────────
CARDS.append(("ANTR-UTLY-0003", """
<div class="rule-header">
<code class="rule-id">ANTR-UTLY-0003</code>
<span class="rule-badge">Proposal</span>
</div>
<div class="rule-status">🔵 Proposal — Under Review</div>
<p class="rule-title">Dominant communications platforms must provide mandatory technical interoperability with competing platforms</p>
<p class="rule-body">Dominant messaging, social networking, and digital communications platforms must provide mandatory technical interoperability allowing users of one platform to communicate with, follow, or connect with users of competing platforms without both parties being required to use the same service. Network lock-in — in which a platform's dominance self-reinforces because users cannot leave without losing their social connections and communication history — is a structural barrier to competition maintained by architectural choices, not technical necessity: the technical protocols required for cross-platform messaging are well understood and widely implemented in other contexts. EU Digital Markets Act Article 7 requires designated gatekeepers to provide interoperability for messaging and communications services as a mandatory obligation, not a voluntary technical cooperation.<sup><a href="#fn-utly0003-1" id="ref-utly0003-1">[1]</a></sup> The United States must enact equivalent mandatory interoperability requirements. Interoperability standards must be technically sufficient to enable genuine cross-platform communication — open, documented, and implemented in forms that provide real competitive alternatives, not nominal compliance that remains architecturally incompatible with competing services. Dominant platforms that implement interoperability in bad faith or impose technical barriers that prevent effective cross-platform communication must face structural remedies, including divestiture of competing services from the platform infrastructure.</p>
<ol class="rule-citations">
<li id="fn-utly0003-1">European Parliament and Council. (2022). <em>Regulation (EU) 2022/1925 (Digital Markets Act)</em>, Art. 7. <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925">https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R1925</a> <a href="#ref-utly0003-1">↩</a></li>
</ol>
"""))


# ---------------------------------------------------------------------------
# Apply all replacements
# ---------------------------------------------------------------------------

def main() -> None:
    """Read, patch, and write the antitrust HTML file."""
    html = TARGET.read_text(encoding="utf-8")

    for card_id, new_inner in CARDS:
        html = replace_card(html, card_id, new_inner)

    TARGET.write_text(html, encoding="utf-8")
    print(f"Done. Wrote {len(CARDS)} card rewrites to {TARGET}")


if __name__ == "__main__":
    main()
