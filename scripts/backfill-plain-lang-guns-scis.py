#!/usr/bin/env python3
"""Backfill plain_language for GUNS, SCIS, and SCNC positions."""
import re
import sqlite3
from pathlib import Path

REPO = Path(__file__).parent.parent
DB = REPO / "data" / "policy_catalog_v2.sqlite"
GUNS_HTML = REPO / "docs" / "pillars" / "gun-policy.html"
SCIS_HTML = REPO / "docs" / "pillars" / "science-technology-space.html"

PLAIN: dict[str, str] = {
    # ── GUNS ─────────────────────────────────────────────────────────────────
    "GUNS-ACQS-0001": (
        "Before anyone can buy a gun, they must pass a background check — a "
        "screening process that flags people legally barred from owning "
        "firearms. This already applies to licensed dealers but must extend "
        "to every purchase."
    ),
    "GUNS-ACQS-0002": (
        "Currently, private sellers and gun-show vendors don't have to run "
        "background checks the way licensed gun stores do. This closes that "
        "loophole so every firearm transfer — including private sales — goes "
        "through the same screening process."
    ),
    "GUNS-ACQS-0003": (
        "Background checks are only as good as the records behind them. "
        "States and agencies must share complete, current data so that "
        "disqualifying records don't fall through the cracks."
    ),
    "GUNS-AMOS-0001": (
        "A background check should be required before buying ammunition, not "
        "just firearms. This prevents people already barred from owning guns "
        "from simply buying the bullets instead."
    ),
    "GUNS-AMOS-0002": (
        "Sellers must keep records of ammunition sales and report unusually "
        "large purchases to law enforcement. Bulk ammo stockpiles can be an "
        "early warning sign of planned violence."
    ),
    "GUNS-BANS-0001": (
        "Private citizens should not own weapons built for military combat — "
        "including both fully automatic firearms and semi-automatic versions "
        "engineered to work around bans. These weapons have no civilian "
        "hunting or self-defense purpose that justifies the risk."
    ),
    "GUNS-BANS-0002": (
        "Any ban on weapons of war must use a definition that gun "
        "manufacturers can't sidestep with small design tweaks. The law must "
        "cover the full category of military-style firearms, not just "
        "specific named models."
    ),
    "GUNS-BANS-0003": (
        "High-capacity magazines — attachments that let a shooter fire many "
        "rounds without reloading — must be banned above a set limit. Fewer "
        "shots before reloading means more chances for people to escape or "
        "for others to intervene."
    ),
    "GUNS-BANS-0004": (
        "Congress must pass a new federal ban on assault-style weapons using "
        "a clear, feature-based definition that closes the loopholes in the "
        "1994 law. A government-funded voluntary buyback would let people "
        "who already own these weapons sell them back."
    ),
    "GUNS-EXCL-0001": (
        "A 2005 law gives gun manufacturers broad protection from lawsuits, "
        "even when their negligent actions — like knowingly selling to "
        "distributors that supply illegal dealers — cause harm. That special "
        "immunity must be repealed so victims can hold manufacturers "
        "accountable in court."
    ),
    "GUNS-EXCL-0002": (
        "The Bureau of Alcohol, Tobacco, Firearms and Explosives (ATF) must "
        "inspect every licensed gun dealer every year. Regular inspections "
        "catch illegal sales, missing inventory, and record-keeping "
        "violations before they fuel more gun violence."
    ),
    "GUNS-LICS-0001": (
        "Before buying any firearm, a person must obtain a license — "
        "completing a background check and safety training first, just like "
        "getting a driver's license before getting behind the wheel."
    ),
    "GUNS-LICS-0002": (
        "After buying a gun, there must be a waiting period before taking "
        "possession of it. Waiting periods give background checks time to "
        "complete and reduce impulsive acts of violence, including suicide."
    ),
    "GUNS-LICS-0003": (
        "Federal law must create a national license for gun buyers that "
        "requires safety training, a background check, and renewal every "
        "five years. This ensures gun owners remain eligible and "
        "knowledgeable throughout their ownership."
    ),
    "GUNS-LICS-0004": (
        "Every gun purchase must include at least a 10-day wait before the "
        "buyer can take the weapon home — no exceptions for people who "
        "already own guns or hold licenses. Research shows waiting periods "
        "save lives by reducing impulsive violence and suicide."
    ),
    "GUNS-MHES-0001": (
        "Any mental health screening for gun ownership must focus on whether "
        "someone poses a real danger — not simply whether they carry a "
        "diagnosis. Most people with mental illness are not violent, and "
        "broad exclusions would be both unfair and ineffective."
    ),
    "GUNS-MHES-0002": (
        "Having a mental health diagnosis — like depression or anxiety — "
        "cannot by itself be the reason someone is barred from owning a "
        "firearm. The law must assess actual, evidence-based risk of "
        "violence rather than stigmatizing entire groups."
    ),
    "GUNS-MILS-0001": (
        "The Second Amendment references a 'well regulated militia,' but "
        "that phrase has never been clearly defined in law. Congress must "
        "establish a legal definition with real, enforceable standards."
    ),
    "GUNS-MILS-0002": (
        "Private armed groups operating outside government oversight — "
        "sometimes called private militias or mercenaries — must be "
        "prohibited. Armed organizations that answer to no public authority "
        "are incompatible with democratic governance."
    ),
    "GUNS-MILS-0003": (
        "Any organization calling itself a militia must operate "
        "transparently — registering members, disclosing its leadership, "
        "keeping audited finances, and carrying liability insurance. These "
        "requirements bring militias under basic public accountability."
    ),
    "GUNS-MILS-0004": (
        "Governments must be able to review what private militias teach and "
        "require in their training. This oversight prevents extremist groups "
        "from operating under the cover of a militia designation."
    ),
    "GUNS-MILS-0005": (
        "Properly vetted and regulated militias should be able to work "
        "alongside emergency responders in disasters like floods or "
        "wildfires. Channeling these groups into legitimate public-service "
        "roles reduces the risk of unaccountable armed groups acting on "
        "their own."
    ),
    "GUNS-REGS-0001": (
        "A constitutional amendment must clarify that the Second Amendment "
        "does not prevent reasonable gun safety regulations. Without this, "
        "courts may continue striking down public safety laws based on "
        "increasingly narrow readings of the right to bear arms."
    ),
    "GUNS-REGS-0002": (
        "A 2022 Supreme Court ruling said gun laws must match 'historical "
        "tradition' from 1791, making many modern safety measures vulnerable "
        "to legal challenge. Congress must pass a statutory foundation so "
        "public safety rules can withstand court review."
    ),
    "GUNS-RFLS-0001": (
        "A red flag law — formally called an Extreme Risk Protection Order "
        "— allows courts to temporarily remove guns from people who show "
        "clear warning signs of danger to themselves or others. Federal "
        "standards must ensure these orders are available everywhere and "
        "that affected people have a fair chance to challenge the removal "
        "in court."
    ),
    "GUNS-RSCH-0001": (
        "Federal agencies like the CDC and NIH must fund ongoing research "
        "into gun injuries and deaths. For decades, Congress blocked this "
        "work; restoring it is essential for understanding what gun safety "
        "policies actually work."
    ),
    "GUNS-RSCH-0002": (
        "A national, continuously updated database must track gun injuries "
        "and deaths across the country. Accurate, timely data is the "
        "foundation of any effective public health response to gun violence."
    ),
    "GUNS-RSCH-0003": (
        "Every federal gun safety law must be reviewed every five years to "
        "measure whether it is actually reducing harm. Laws that aren't "
        "working should be strengthened or replaced based on evidence, "
        "not politics."
    ),
    "GUNS-SAFE-0001": (
        "When a gun is not in a person's hands, it must be stored in a "
        "locked container. Secure storage prevents stolen weapons from "
        "reaching criminal hands and keeps children from accessing loaded "
        "firearms."
    ),
    "GUNS-SAFE-0002": (
        "Gun owners who negligently leave firearms accessible to children "
        "must face criminal liability when that results in harm. These laws "
        "hold adults accountable and create a legal incentive to store "
        "weapons safely."
    ),
    "GUNS-SAFE-0003": (
        "Gun owners should receive a federal tax credit when they buy "
        "certified gun safes or lock boxes. Making safe storage affordable "
        "encourages compliance and reduces the number of firearms accessible "
        "to children or thieves."
    ),
    "GUNS-SAFS-0001": (
        "'Ghost guns' are firearms with no serial number — often assembled "
        "at home from kits — that are untraceable by law enforcement. "
        "Manufacturing, selling, or possessing these weapons must be illegal."
    ),
    "GUNS-SAFS-0002": (
        "Microstamping stamps a tiny unique code on bullet casings when a "
        "gun fires, letting investigators link shell casings found at a "
        "crime scene to a specific weapon. All new civilian semi-automatic "
        "handguns must use this technology."
    ),
    "GUNS-SAFS-0003": (
        "'Smart guns' are firearms that can only be fired by their "
        "authorized user — using a fingerprint or RFID signal — reducing "
        "accidents and theft. The government must fund research and remove "
        "legal barriers that have kept smart guns off the market."
    ),
    "GUNS-STWS-0001": (
        "A 'straw purchase' is when someone who can legally buy a gun "
        "buys it for someone who cannot. Penalties must be stronger and "
        "prosecutors must pursue these cases, since straw purchases are a "
        "major pipeline for illegal firearms."
    ),
    "GUNS-STWS-0002": (
        "Buying guns in bulk to resell them illegally — called firearms "
        "trafficking — must be its own federal crime with serious penalties. "
        "No single law currently covers the full scope of this activity, "
        "which fuels violent crime across the country."
    ),
    "GUNS-STWS-0003": (
        "Gun manufacturers must be legally responsible when their "
        "distribution choices — like supplying dealers known to funnel guns "
        "to the illegal market — lead to foreseeable violence. Victims of "
        "this negligence must be able to sue for damages."
    ),
    "GUNS-STWS-0004": (
        "A federal law passed in 2005 gives gun manufacturers near-total "
        "immunity from lawsuits, even when their design or distribution "
        "choices put people at risk. That special protection must be "
        "repealed so the industry faces the same legal accountability as "
        "any other manufacturer."
    ),
    "GUNS-STWS-0005": (
        "A gap in federal law — known as the Charleston loophole — allowed "
        "the 2015 church shooter to buy a gun because his background check "
        "wasn't completed in three business days. That loophole must be "
        "closed: no sale proceeds until the check is done, all private "
        "transfers must be checked, and dealers must maintain electronic "
        "records accessible to law enforcement within 24 hours."
    ),
    "GUNS-TRAF-0001": (
        "No person may buy more than one handgun per month under federal "
        "law. This limit disrupts bulk buying by traffickers who purchase "
        "many guns at once to resell illegally on the street."
    ),
    "GUNS-TRAF-0002": (
        "If your gun is lost or stolen, you must report it to police within "
        "48 hours. Quick reporting helps law enforcement recover weapons "
        "before they're used in crimes and helps track how guns move from "
        "legal to illegal hands."
    ),
    "GUNS-TRAF-0003": (
        "Every legally manufactured or sold firearm must have a permanent "
        "serial number that cannot be removed or defaced. Serial numbers "
        "let law enforcement trace guns used in crimes — firearms without "
        "them make investigations nearly impossible."
    ),
    "GUNS-TRAN-0001": (
        "Anyone who wants to own a firearm must first complete a certified "
        "safety course. Safety training teaches people how to handle, store, "
        "and operate guns properly, reducing accidents and unintentional "
        "shootings."
    ),
    "GUNS-TRAN-0002": (
        "Gun owners must also complete training in de-escalation — learning "
        "how to defuse tense situations without reaching for a weapon. Most "
        "conflicts don't require lethal force, and trained gun owners make "
        "better decisions under pressure."
    ),
    "GUNS-TRAN-0003": (
        "Federal law must require all gun owners to store their weapons "
        "securely when not in use. A national minimum standard ensures no "
        "state can opt out, and that children and unauthorized users "
        "everywhere face a locked barrier before reaching a firearm."
    ),
    # ── SCIS ─────────────────────────────────────────────────────────────────
    "SCIS-AGYS-0001": (
        "Federal science agencies like NOAA, NASA, and the EPA must be "
        "legally protected from political interference in their scientific "
        "work. Tampering with or suppressing their climate and environmental "
        "findings would be a federal crime."
    ),
    "SCIS-EMGS-0001": (
        "The federal government's AI safety guidelines must become legally "
        "binding rules for agencies and their contractors. Any high-risk use "
        "of AI — like deciding who gets a loan, a job, or is released from "
        "jail — must include a formal review of how the system could cause "
        "harm."
    ),
    "SCIS-EMGS-0002": (
        "The most dangerous biological research — including experiments that "
        "could make diseases more transmissible — requires independent "
        "inspection and Congressional notice before proceeding. Labs "
        "handling the world's deadliest pathogens must publicly report any "
        "incidents."
    ),
    "SCIS-EMGS-0003": (
        "The U.S. must invest in quantum computing and also defend against "
        "it — because quantum computers could break today's encryption. All "
        "federal computer systems must upgrade to new encryption standards "
        "that can resist quantum attacks by 2027."
    ),
    "SCIS-FNDS-0001": (
        "Congress must by law spend at least 1.5% of the economy on "
        "civilian research and development, with at least half a percent "
        "dedicated to NIH health research. These budgets cannot be cut or "
        "frozen by executive order, protecting science from political "
        "interference."
    ),
    "SCIS-FNDS-0002": (
        "Government officials who alter, suppress, or misrepresent federal "
        "scientists' published research must face criminal charges. "
        "Scientists must also have the legal right to sue officials who "
        "interfere with their work."
    ),
    "SCIS-FNDS-0003": (
        "When the federal government makes major rules on health, "
        "environment, or safety, those decisions must be grounded in "
        "peer-reviewed science — research independently checked by other "
        "experts. An agency that rejects scientific consensus must explain "
        "why with its own evidence and submit to independent expert review."
    ),
    "SCIS-FNDS-0004": (
        "Federal climate policy must follow the best available science as "
        "compiled by the IPCC — the United Nations' panel of climate "
        "scientists. Where science is still uncertain, the government must "
        "err on the side of caution rather than delay action."
    ),
    "SCIS-INTL-0001": (
        "The U.S. must join or lead negotiations to create binding "
        "international rules for mining and using resources in space. No "
        "country or corporation may claim ownership of the Moon, asteroids, "
        "or other celestial bodies — space belongs to all of humanity."
    ),
    "SCIS-PUBL-0001": (
        "Researchers whose work is funded by taxpayers must keep ownership "
        "of their publications and cannot be forced to sign those rights "
        "over to commercial academic publishers. This protects open access "
        "to publicly funded knowledge."
    ),
    "SCIS-SPCS-0001": (
        "NASA must always have contracts with at least two separate private "
        "companies for launching astronauts into space. Relying on a single "
        "company for crewed spaceflight is a national security and safety "
        "risk — if that company fails, the U.S. loses its ability to send "
        "people to space."
    ),
    "SCIS-SPCS-0002": (
        "Space debris — broken satellites and rocket parts orbiting Earth "
        "— poses a growing danger to all spacecraft. The U.S. must lead "
        "international talks to create binding rules requiring satellite "
        "operators to clean up after themselves and establishing who pays "
        "when their debris causes damage."
    ),
    "SCIS-SPCS-0003": (
        "The U.S. must write its international commitments against "
        "militarizing space into American law and work to stop the "
        "development of weapons that destroy satellites. Losing satellite "
        "infrastructure would cripple GPS, communications, and national "
        "security — keeping space peaceful protects everyone."
    ),
    "SCIS-SPCS-0004": (
        "The head of NASA must have job security — a fixed six-year term "
        "that can only end for serious cause — so the agency isn't "
        "disrupted by political changes. Major shifts in NASA's mission can "
        "only happen with a vote in Congress, not by executive decree."
    ),
    "SCIS-TECS-0001": (
        "You should have the legal right to repair any product you own — "
        "or take it to an independent shop. Manufacturers must provide "
        "manuals, tools, and parts at fair prices and cannot use copyright "
        "law to force you to use only their own service centers."
    ),
    "SCIS-TECS-0002": (
        "When a software company stops supporting a product, it cannot "
        "simply abandon users on an insecure, unpatched system. It must "
        "either keep fixing security flaws, release the source code so "
        "others can maintain it, or offer a real path to switch to "
        "something safe."
    ),
    "SCIS-TECS-0003": (
        "Every American must have access to fast, affordable internet by "
        "2030. Cities and cooperatives must have the right to build their "
        "own fiber networks, and internet companies receiving federal "
        "subsidies cannot use that money to lobby against public broadband "
        "projects."
    ),
    "SCIS-TECS-0004": (
        "When courts break up a technology monopoly, the core patents and "
        "software must be made publicly available. Critical technology in "
        "areas like computer chips, medicine, and AI must be shared for "
        "national security — no single company should control access to "
        "technologies the entire economy depends on."
    ),
    "SCIS-TECS-0005": (
        "Internet service must be treated like a public utility under "
        "federal law — meaning providers cannot charge websites to reach "
        "customers faster, slow down services they don't like, or block "
        "legal content. Users and websites harmed by these practices can "
        "sue."
    ),
    # ── SCNC ─────────────────────────────────────────────────────────────────
    "SCNC-RSCH-0001": (
        "The federal government must double its investment in scientific "
        "research over the next decade, with NIH and NSF growing "
        "significantly. A $100 billion permanent endowment would shield "
        "science funding from year-to-year political budget fights."
    ),
    "SCNC-RSCH-0002": (
        "It must be illegal for politicians or officials to interfere with "
        "federal scientists' research. Every federal scientist gets "
        "whistleblower protection, and an independent oversight board — "
        "with the power to subpoena records — must investigate any "
        "violations."
    ),
    "SCNC-RSCH-0003": (
        "Congress must permanently protect climate science programs at NOAA "
        "and NASA from being cut, restructured, or suppressed by any "
        "president. All climate data collected with public money must be "
        "freely available to everyone, forever."
    ),
    "SCNC-RSCH-0004": (
        "Research paid for by taxpayers must be freely available to the "
        "public — not locked behind expensive journal paywalls. The raw "
        "data must also be publicly archived, and the small number of "
        "companies that dominate academic publishing must face antitrust "
        "review."
    ),
}


def update_db(conn: sqlite3.Connection) -> int:
    """Write plain_language into the positions table. Returns count updated."""
    cur = conn.cursor()
    count = 0
    for pos_id, text in PLAIN.items():
        cur.execute(
            "UPDATE positions SET plain_language = ? WHERE id = ?",
            (text, pos_id),
        )
        count += cur.rowcount
    conn.commit()
    return count


def _find_card_bounds(html: str, pos_id: str) -> tuple[int, int] | None:
    """
    Find the start and end character positions of the card div for pos_id.
    Handles nested divs by counting depth.
    Returns (start, end) or None if not found.
    """
    start_m = re.search(r'<div[^>]+id="' + re.escape(pos_id) + r'"', html)
    if not start_m:
        return None
    pos = start_m.start()
    depth = 0
    i = pos
    while i < len(html):
        if html[i:i+4] == "<div":
            depth += 1
            i += 4
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0:
                return (pos, i + 6)
            i += 6
        else:
            i += 1
    return None


def update_card(html: str, pos_id: str, text: str) -> tuple[str, str]:
    """
    Update rule-plain for one card. Returns (new_html, action) where
    action is 'inserted' | 'filled' | 'skipped' | 'not_found'.
    """
    bounds = _find_card_bounds(html, pos_id)
    if not bounds:
        return html, "not_found"

    start, end = bounds
    card = html[start:end]

    escaped = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
    new_tag = f'<p class="rule-plain">{escaped}</p>'

    # Already has non-empty rule-plain?
    if re.search(r'<p class="rule-plain">[^<\s]', card):
        return html, "skipped"

    # Has empty rule-plain placeholder?
    if re.search(r'<p class="rule-plain">\s*</p>', card):
        new_card = re.sub(
            r'<p class="rule-plain">\s*</p>',
            new_tag,
            card,
            count=1,
        )
        return html[:start] + new_card + html[end:], "filled"

    # Insert after <p class="rule-title">...</p>
    title_m = re.search(r'<p class="rule-title">.*?</p>', card, re.DOTALL)
    if not title_m:
        return html, "not_found"
    insert_at = start + title_m.end()
    new_html = html[:insert_at] + "\n" + new_tag + html[insert_at:]
    return new_html, "inserted"


def update_html(html_path: Path, ids: list[str]) -> tuple[int, int]:
    """Update HTML for the given IDs. Returns (inserted, filled) counts."""
    html = html_path.read_text(encoding="utf-8")
    inserted = 0
    filled = 0

    for pos_id in ids:
        if pos_id not in PLAIN:
            continue
        html, action = update_card(html, pos_id, PLAIN[pos_id])
        if action == "inserted":
            inserted += 1
        elif action == "filled":
            filled += 1
        elif action == "not_found":
            print(f"  WARNING: card not found in HTML: {pos_id}")

    html_path.write_text(html, encoding="utf-8")
    return inserted, filled


def main() -> None:
    guns_ids = [k for k in PLAIN if k.startswith("GUNS-")]
    scis_ids = [k for k in PLAIN if k.startswith("SCIS-")]
    scnc_ids = [k for k in PLAIN if k.startswith("SCNC-")]

    conn = sqlite3.connect(DB)
    db_updated = update_db(conn)
    conn.close()
    print(f"DB: {db_updated} rows updated")

    ins, fil = update_html(GUNS_HTML, guns_ids)
    print(f"GUNS HTML: {ins} inserted, {fil} filled")

    ins, fil = update_html(SCIS_HTML, scis_ids + scnc_ids)
    print(f"SCIS+SCNC HTML: {ins} inserted, {fil} filled")

    print("Done.")


if __name__ == "__main__":
    main()
