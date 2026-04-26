"""
Fill plain-language descriptions into education pillar policy cards.
Inserts <p class="rule-plain"> after <p class="rule-title"> where missing,
and fills in any existing empty rule-plain paragraphs.
"""

from bs4 import BeautifulSoup
from pathlib import Path

PLAIN_LANGUAGE = {
    # ── SYSR: System foundations ──────────────────────────────────────────────
    "EDUC-SYSR-0001": (
        "This foundational rule requires education systems to give every person "
        "access to high-quality learning. Good education helps people think "
        "critically, earn a living, and take part in democratic life."
    ),
    "EDUC-SYSR-0002": (
        "This rule prohibits any system that lets wealth, zip code, race, "
        "disability, or family background determine whether a child gets a good "
        "education. Where a child is born must not decide what they have the "
        "chance to learn."
    ),
    "EDUC-SYSR-0003": (
        "This rule requires schools to focus on helping students grow as whole "
        "people over time, rather than chasing short-term test scores or "
        "administrative shortcuts. The goal is lasting development, not just "
        "passing the next exam."
    ),
    "EDUC-SYSR-0004": (
        "This rule states that people must be able to get the education they "
        "need to find work and build a stable life without taking on years of "
        "crushing debt to pay for it."
    ),
    "EDUC-SYSR-0005": (
        "This rule establishes that education is a public good and must be "
        "delivered mainly through a publicly run, high-quality system — not "
        "handed over to private markets that put profit before students."
    ),
    "EDUC-SYSR-0006": (
        "This rule prohibits using public education money in ways that weaken "
        "the public school system. Tax dollars meant for education must "
        "strengthen public schools, not be diverted in ways that undercut "
        "access or quality for everyone."
    ),

    # ── ACCS: Access ──────────────────────────────────────────────────────────
    "EDUC-ACCS-0001": (
        "This rule guarantees every person free access to high-quality K–12 "
        "education. No child should have to pay to attend a quality primary or "
        "secondary school."
    ),
    "EDUC-ACCS-0002": (
        "This rule requires that higher education, job training, and lifelong "
        "learning be widely available and not blocked by financial barriers. "
        "People should be able to continue learning throughout their lives "
        "regardless of income."
    ),
    "EDUC-ACCS-0003": (
        "This rule requires education systems to actively fix unequal access, "
        "resources, and outcomes rather than allowing gaps between regions and "
        "populations to persist unchallenged."
    ),
    "EDUC-ACCS-0004": (
        "This rule guarantees that students with disabilities receive full "
        "access to education along with the specific supports and "
        "accommodations they need to learn effectively."
    ),
    "EDUC-ACCS-0005": (
        "This rule ensures every student has access to safe, reliable "
        "transportation to get to school. Transportation is treated as an "
        "essential part of the right to attend school."
    ),
    "EDUC-ACCS-0006": (
        "This rule prohibits transportation systems from being set up in ways "
        "that effectively block lower-income or rural students from reaching "
        "higher-quality schools available in other areas."
    ),
    "EDUC-ACCS-0007": (
        "This rule requires all publicly funded schools to operate "
        "transparently, treat all students equally, and be subject to public "
        "oversight — so communities can see how their schools are run and "
        "hold them accountable."
    ),
    "EDUC-ACCS-0008": (
        "This rule prohibits any school that receives public funding from "
        "turning away students based on ability level, disability, behavior, "
        "religion, or economic background. Public money must serve all students."
    ),

    # ── FNDS: Funding equity ──────────────────────────────────────────────────
    "EDUC-FNDS-0001": (
        "This rule prohibits funding schools primarily based on local property "
        "values, which causes wealthier neighborhoods to have far better "
        "schools than poorer ones. Funding must not replicate wealth-based "
        "inequality in educational quality."
    ),
    "EDUC-FNDS-0002": (
        "This rule requires public funding to ensure every school — regardless "
        "of location — has comparable resources, facilities, staff, and "
        "materials, so that geography does not determine educational quality."
    ),
    "EDUC-FNDS-0003": (
        "This rule guarantees that schools serving students with greater needs "
        "— such as those in poverty or with disabilities — receive extra "
        "funding specifically to address those needs, not just an equal share."
    ),

    # ── QLTS: Quality standards ───────────────────────────────────────────────
    "EDUC-QLTS-0001": (
        "This rule requires schools to provide genuinely high-quality teaching, "
        "up-to-date learning materials, and good learning environments — not "
        "just go through the motions of holding classes."
    ),
    "EDUC-QLTS-0002": (
        "This rule requires school curricula to cover reading, math, science, "
        "history, civics, critical thinking, and media literacy, giving "
        "students a well-rounded foundation for life."
    ),
    "EDUC-QLTS-0003": (
        "This rule requires schools to teach practical life skills — including "
        "how to manage money, navigate the internet safely, and handle everyday "
        "responsibilities — so students are prepared for real life, not just "
        "academic tests."
    ),
    "EDUC-QLTS-0004": (
        "This rule prohibits schools from relying too heavily on standardized "
        "tests as the main way to judge learning or school quality. Tests are "
        "one tool, not the only measure of whether students and schools "
        "are succeeding."
    ),

    # ── WRKS: Educator workforce ──────────────────────────────────────────────
    "EDUC-WRKS-0001": (
        "This rule requires teachers to be paid well enough to reflect how "
        "important their work is and to encourage good teachers to stay in "
        "the profession long-term."
    ),
    "EDUC-WRKS-0002": (
        "This rule ensures teachers have access to ongoing training and "
        "professional development so they can keep improving their skills "
        "throughout their careers."
    ),
    "EDUC-WRKS-0003": (
        "This rule prohibits school systems from relying on teachers to work "
        "unpaid overtime or burning out from excessive workloads. Teacher "
        "workloads must be reasonable and sustainable."
    ),
    "EDUC-WRKS-0004": (
        "This rule protects teachers' ability to make professional decisions "
        "about how they teach, as long as they work within established "
        "curriculum standards — preventing micromanagement that undermines "
        "effective instruction."
    ),

    # ── STUS: Student support ─────────────────────────────────────────────────
    "EDUC-STUS-0001": (
        "This rule requires schools to care for students' physical health, "
        "mental health, and emotional well-being alongside academic learning. "
        "A student who is struggling emotionally cannot learn effectively."
    ),
    "EDUC-STUS-0002": (
        "This rule ensures every student has access to counselors, mental "
        "health services, and a safe place to learn — not just academic "
        "instruction without support."
    ),
    "EDUC-STUS-0003": (
        "This rule requires school discipline to be fair and appropriate to "
        "the situation, and prohibits punishment systems that push certain "
        "groups of students out of school or cause lasting harm."
    ),

    # ── EXTS: Exploitation prevention ─────────────────────────────────────────
    "EDUC-EXTS-0001": (
        "This rule prohibits structuring education systems in ways that extract "
        "profit at students' expense. Schools must prioritize learning and "
        "access, not generating revenue for owners or shareholders."
    ),
    "EDUC-EXTS-0002": (
        "This rule requires strict rules against predatory student lending, "
        "for-profit schools, and certification programs that exploit students "
        "with false promises and trapping debt."
    ),
    "EDUC-EXTS-0003": (
        "This rule prohibits burdening students with excessive debt just to "
        "access education they need. Getting an education should not mean "
        "years of financial hardship afterward."
    ),

    # ── VOCS: Vocational education ────────────────────────────────────────────
    "EDUC-VOCS-0001": (
        "This rule requires education systems to include strong vocational, "
        "technical, and apprenticeship paths alongside traditional college "
        "tracks, so students who want to learn a trade have a real, "
        "well-funded option."
    ),
    "EDUC-VOCS-0002": (
        "This rule establishes that vocational and technical education must be "
        "treated as equally valuable and dignified as college-prep academics. "
        "Choosing a trade is not a lesser choice."
    ),
    "EDUC-VOCS-0003": (
        "This rule requires that when schools partner with businesses and "
        "industries, those partnerships must benefit workers and students — "
        "not simply give companies access to cheap or exploitable labor."
    ),

    # ── HEDS: Higher education ────────────────────────────────────────────────
    "EDUC-HEDS-0001": (
        "This rule requires higher education to be affordable and prohibits "
        "systems that force students to take on more debt than they can "
        "realistically repay. Going to college should not lead to a lifetime "
        "of financial burden."
    ),
    "EDUC-HEDS-0002": (
        "This rule requires that public investment in higher education "
        "prioritize keeping tuition affordable, maintaining educational quality, "
        "and ensuring research is conducted with integrity rather than for "
        "corporate benefit."
    ),
    "EDUC-HEDS-0003": (
        "This rule requires student loan systems to include real protections for "
        "borrowers — including fair repayment options and debt relief — so "
        "that people are not trapped by loans that grow faster than they can "
        "pay them down."
    ),
    "EDUC-HEDS-0004": (
        "This rule guarantees tuition-free attendance at all public community "
        "colleges, technical schools, and trade programs for eligible students. "
        "Two-year and vocational education must not cost students money to access."
    ),
    "EDUC-HEDS-0005": (
        "This rule requires that tuition-free programs cover actual "
        "instructional costs and prohibits schools from using hidden fees or "
        "administrative charges to make tuition-free programs effectively "
        "unaffordable in practice."
    ),
    "EDUC-HEDS-0006": (
        "This rule ensures that tuition-free higher education programs include "
        "part-time students, adult learners, and workers who need to retrain "
        "for a new career — not just recent high school graduates attending "
        "full-time."
    ),
    "EDUC-HEDS-0007": (
        "This rule requires that vocational, trade, and certification programs "
        "receive the same level of public funding and institutional support as "
        "traditional academic degree programs."
    ),
    "EDUC-HEDS-0008": (
        "This rule requires that public investment in community colleges and "
        "technical education be guided by what the job market actually needs, "
        "while making sure that training programs do not become tools for "
        "suppressing worker wages or making it easier to exploit workers."
    ),
    "EDUC-HEDS-0009": (
        "This rule establishes that higher education must serve the public "
        "interest by expanding knowledge and opportunity — not function as a "
        "debt-generation machine or a system where prestige gates "
        "access to a decent life."
    ),
    "EDUC-HEDS-0010": (
        "This rule requires college admissions to be fair and transparent, "
        "and prohibits giving preference to applicants based on family wealth, "
        "legacy status (parents attended the school), or donor connections."
    ),
    "EDUC-HEDS-0011": (
        "This rule prohibits colleges from using admissions practices that "
        "systematically block students from low-income backgrounds, students "
        "with disabilities, or students who lacked access to expensive test "
        "prep and private counseling."
    ),
    "EDUC-HEDS-0012": (
        "This rule prohibits using standardized test scores as the main or "
        "only factor in admissions when doing so consistently disadvantages "
        "students due to structural inequality rather than actual ability or "
        "potential."
    ),
    "EDUC-HEDS-0013": (
        "This rule requires colleges to offer multiple ways for students to "
        "get in — including transfer pathways, adult entry programs, and "
        "options for students who did not follow a traditional academic path."
    ),
    "EDUC-HEDS-0014": (
        "This rule requires publicly funded colleges to be held accountable "
        "for how their students actually do — including graduation rates, "
        "employment after graduation, and how much debt students carry."
    ),
    "EDUC-HEDS-0015": (
        "This rule requires institutions that consistently fail to meet basic "
        "outcome standards to face corrective action or lose eligibility for "
        "public funding — so that students are not trapped in low-quality "
        "programs subsidized by taxpayers."
    ),
    "EDUC-HEDS-0016": (
        "This rule prohibits colleges from growing enrollment or raising tuition "
        "without actually improving educational quality and student outcomes. "
        "Growth for its own sake does not justify higher costs to students."
    ),
    "EDUC-HEDS-0017": (
        "This rule requires colleges to use tuition and public funding primarily "
        "on teaching, student services, and academic quality — not on "
        "administrative expansion that does not directly help students learn."
    ),
    "EDUC-HEDS-0018": (
        "This rule subjects colleges to review when their administrative "
        "spending grows excessively without improving student outcomes. "
        "Money that goes to management bloat instead of students must be "
        "corrected."
    ),
    "EDUC-HEDS-0019": (
        "This rule requires that any tuition increases at publicly funded "
        "colleges be clearly justified and subject to public oversight — so "
        "schools cannot raise prices without explaining why and who is watching."
    ),
    "EDUC-HEDS-0020": (
        "This rule requires colleges to maintain a stable, fairly paid "
        "teaching workforce and prohibits over-reliance on adjunct or part-time "
        "instructors paid poverty wages to teach the majority of courses."
    ),
    "EDUC-HEDS-0021": (
        "This rule protects faculty members' right to teach, research, and "
        "publish honestly within their field without facing pressure to "
        "distort their findings or suppress inconvenient conclusions."
    ),
    "EDUC-HEDS-0022": (
        "This rule requires that working conditions for college faculty align "
        "with normal labor standards — fair pay, job security, and reasonable "
        "workloads — including for adjuncts and part-time instructors."
    ),
    "EDUC-HEDS-0023": (
        "This rule requires colleges to maintain strong policies against "
        "academic fraud, data fabrication, and research misconduct, so that "
        "degrees and research results mean what they claim to mean."
    ),
    "EDUC-HEDS-0024": (
        "This rule prohibits corporate or private funding from compromising the "
        "independence of academic research. Funders may not pressure researchers "
        "to produce predetermined results or suppress unwanted findings."
    ),
    "EDUC-HEDS-0025": (
        "This rule requires that conflicts of interest in academic research — "
        "such as a researcher being paid by a company whose product they are "
        "studying — be publicly disclosed so others can evaluate the findings "
        "with full information."
    ),
    "EDUC-HEDS-0026": (
        "This rule requires accreditation systems to genuinely measure "
        "educational quality and student outcomes rather than acting as a "
        "gatekeeping club that locks out newer or alternative institutions "
        "regardless of quality."
    ),
    "EDUC-HEDS-0027": (
        "This rule requires accreditation to be based on whether students "
        "actually succeed — not on how old, famous, or traditionally prestigious "
        "an institution is."
    ),
    "EDUC-HEDS-0028": (
        "This rule requires that new or innovative education providers have a "
        "clear, fair path to accreditation if they demonstrate real quality "
        "and good outcomes for students."
    ),
    "EDUC-HEDS-0029": (
        "This rule guarantees that college students have the right to fair "
        "treatment, a fair process if they face discipline, and protection "
        "from discrimination or retaliation for speaking up."
    ),
    "EDUC-HEDS-0030": (
        "This rule requires colleges to give students clear, honest information "
        "about what a program costs, what graduates typically earn, what the "
        "degree is actually worth, and what career paths it opens."
    ),
    "EDUC-HEDS-0031": (
        "This rule prohibits schools from misleading students about job "
        "placement rates, expected earnings, or how effective their programs "
        "really are. Students deserve honest information before taking on debt."
    ),
    "EDUC-HEDS-0032": (
        "This rule requires colleges to maintain safe campuses with strong "
        "policies against harassment, sexual assault, and abuse — protecting "
        "students from harm both inside and outside the classroom."
    ),
    "EDUC-HEDS-0033": (
        "This rule requires that campus reporting systems for harassment or "
        "assault be genuinely accessible and fair, and prohibits systems "
        "designed to protect the institution's reputation rather than "
        "student safety."
    ),
    "EDUC-HEDS-0034": (
        "This rule ensures that students can transfer credits between accredited "
        "colleges without losing the work they have already done and paid for. "
        "Transferring should not mean starting over."
    ),
    "EDUC-HEDS-0035": (
        "This rule requires public higher education systems to create "
        "standardized credit frameworks so students can move between schools "
        "more easily and do not have to repeat coursework when they transfer."
    ),
    "EDUC-HEDS-0036": (
        "This rule requires colleges to recognize learning gained through work "
        "experience, military service, or non-traditional education pathways "
        "where that learning genuinely meets academic standards."
    ),
    "EDUC-HEDS-0037": (
        "This rule establishes that public universities must serve broad "
        "community goals — including generating knowledge, training a skilled "
        "workforce, and building an informed citizenry — not just producing "
        "revenue."
    ),
    "EDUC-HEDS-0038": (
        "This rule prohibits public colleges and universities from prioritizing "
        "their rankings, exclusivity, or brand prestige over actual access, "
        "affordability, and benefit to the public."
    ),
    "EDUC-HEDS-0039": (
        "This rule prohibits higher education from operating primarily as a "
        "way to extract revenue from students through ever-rising tuition, fees, "
        "and loan interest."
    ),
    "EDUC-HEDS-0040": (
        "This rule requires reforming or eliminating higher education business "
        "models that depend on trapping students in unmanageable debt or selling "
        "programs that do not deliver what they promise."
    ),

    # ── LIFS: Lifelong learning ───────────────────────────────────────────────
    "EDUC-LIFS-0001": (
        "This rule guarantees that people can continue learning, retrain for "
        "new jobs, and pursue continuing education throughout their lives — "
        "not only during traditional school years."
    ),
    "EDUC-LIFS-0002": (
        "This rule requires public systems to support workers who need to "
        "change careers because of automation, economic shifts, or job "
        "displacement — so that technological change does not leave workers "
        "behind without help."
    ),

    # ── CIVL: Civic education ─────────────────────────────────────────────────
    "EDUC-CIVL-0001": (
        "This rule requires all schools to include strong civics education — "
        "teaching how government works, what rights people have, what "
        "responsibilities come with those rights, and how to participate "
        "in democracy."
    ),
    "EDUC-CIVL-0002": (
        "This rule requires schools to teach students how to evaluate news, "
        "information sources, and political arguments critically, so they are "
        "not easily misled by misinformation or propaganda."
    ),
    "EDUC-CIVL-0003": (
        "This rule prohibits using public education to push a political ideology "
        "or suppress honest inquiry into factual questions. Schools must "
        "support critical thinking, not indoctrinate students."
    ),

    # ── GOVN: Governance and accountability ───────────────────────────────────
    "EDUC-GOVN-0001": (
        "This rule requires education systems to operate transparently, be held "
        "accountable for real outcomes, and be subject to public oversight — "
        "so communities know what is working and what is not."
    ),
    "EDUC-GOVN-0002": (
        "This rule requires that education policies be judged on whether "
        "students actually learn and succeed over time — not just on "
        "administrative efficiency or paperwork compliance."
    ),
    "EDUC-GOVN-0003": (
        "This rule gives communities meaningful say in education decisions, "
        "while ensuring that local input cannot be used to justify "
        "discrimination, exclusion, or unequal access to resources."
    ),
    "EDUC-GOVN-0004": (
        "This rule requires education systems to publicly report data on school "
        "segregation, resource differences, and student outcomes — so problems "
        "are visible and cannot be ignored."
    ),
    "EDUC-GOVN-0005": (
        "This rule requires that when data shows persistent patterns of "
        "segregation or inequality, state or federal authorities must take "
        "mandatory corrective action rather than waiting for the problem "
        "to fix itself."
    ),
    "EDUC-GOVN-0006": (
        "This rule requires that any policy that makes school segregation or "
        "inequality worse be reviewed and changed or removed before more harm "
        "is done."
    ),

    # ── DEBT: Student debt ────────────────────────────────────────────────────
    "EDUC-DEBT-0001": (
        "This rule requires the federal government to implement broad student "
        "loan forgiveness to relieve or eliminate existing debt burdens that "
        "have become unsustainable for millions of borrowers."
    ),
    "EDUC-DEBT-0002": (
        "This rule requires debt relief to focus first on borrowers hit hardest "
        "by economic hardship, predatory lending, or programs that failed to "
        "deliver good outcomes — while also providing broad-based relief for "
        "all affected borrowers."
    ),
    "EDUC-DEBT-0003": (
        "This rule requires restructuring the student loan system after "
        "forgiveness so that the same problem does not simply rebuild itself, "
        "trapping future students in the same cycle of unmanageable debt."
    ),
    "EDUC-DEBT-0004": (
        "This rule requires that interest rates, repayment terms, and loan "
        "servicing be fair and transparent — not structured to squeeze maximum "
        "money out of borrowers over as long a period as possible."
    ),
    "EDUC-DEBT-0005": (
        "This rule requires schools with consistently poor student outcomes, "
        "high loan default rates, or deceptive practices to face penalties, "
        "funding cuts, or loss of access to federal student aid."
    ),
    "EDUC-DEBT-0006": (
        "This rule prohibits educational institutions from passing all the "
        "financial risk of a failed education onto students while keeping the "
        "tuition revenue regardless of whether students succeed."
    ),
    "EDUC-DEBT-0007": (
        "This rule prohibits predatory student lending — including misleading "
        "marketing, abusive loan terms, and misrepresenting what a program "
        "will do for a student's career or earnings."
    ),
    "EDUC-DEBT-0008": (
        "This rule requires the companies that service student loans to be "
        "regulated so they give borrowers accurate information, treat them "
        "fairly, and actually connect them to repayment and relief options."
    ),
    "EDUC-DEBT-0009": (
        "This rule calls for public education funding models to reduce the "
        "country's dependence on student debt by investing directly in "
        "education through subsidies and alternative financing methods."
    ),
    "EDUC-DEBT-0010": (
        "This rule requires that any new model for financing education must not "
        "simply recreate debt by another name or put even more risk on students "
        "than the current loan system does."
    ),

    # ── SECU: Separation of church and state in schools ───────────────────────
    "EDUC-SECU-0001": (
        "This rule requires public schools to remain religiously neutral — "
        "they may not promote or oppose any religion, and must protect every "
        "student's right to follow their own conscience."
    ),
    "EDUC-SECU-0002": (
        "This rule prohibits public school employees from trying to convert "
        "students to any religion or officially endorsing any belief system "
        "in their role as school staff."
    ),
    "EDUC-SECU-0003": (
        "This rule prohibits school policies, curricula, or official activities "
        "from pressuring or incentivizing students to participate in religious "
        "activities or adopt religious beliefs."
    ),
    "EDUC-SECU-0004": (
        "This rule prohibits the use of school time, public facilities, or "
        "school-sponsored platforms to promote or advance religious teaching "
        "or doctrine."
    ),
    "EDUC-SECU-0005": (
        "This rule protects students' personal right to pray privately, "
        "express their religious identity, and take part in student-led "
        "religious activities — as long as the school itself is not "
        "sponsoring or requiring it."
    ),
    "EDUC-SECU-0006": (
        "This rule prohibits schools from punishing, harassing, or "
        "discriminating against students because of their religion, lack of "
        "religion, or personal beliefs."
    ),
    "EDUC-SECU-0007": (
        "This rule requires that when schools violate religious neutrality or "
        "teach non-scientific content as science, those violations must be "
        "investigated and corrected by educational and legal authorities."
    ),
    "EDUC-SECU-0008": (
        "This rule requires that students and families have accessible, easy-to-use "
        "processes for reporting when a school promotes religion or teaches "
        "content that should not be in a public school curriculum."
    ),

    # ── SCIS: Science curriculum ──────────────────────────────────────────────
    "EDUC-SCIS-0001": (
        "This rule requires public school science classes to be based on "
        "established scientific methods, real evidence, and the consensus of "
        "the scientific community — not on personal belief or tradition."
    ),
    "EDUC-SCIS-0002": (
        "This rule prohibits teaching religious or metaphysical explanations "
        "— like creationism — as if they were scientific theories in science "
        "class. Science class must teach science."
    ),
    "EDUC-SCIS-0003": (
        "This rule allows religion, philosophy, and cultural belief systems to "
        "be taught in appropriate classes like history or comparative religion "
        "— but only as subjects of study, not as truth claims being endorsed "
        "by the school."
    ),
    "EDUC-SCIS-0004": (
        "This rule prohibits presenting frameworks like Intelligent Design as "
        "scientific theory in public school science classes because they lack "
        "the empirical evidence and peer-reviewed testing that define "
        "actual science."
    ),

    # ── STRS: Structural segregation ──────────────────────────────────────────
    "EDUC-STRS-0001": (
        "This rule prohibits education systems from being designed or operating "
        "in ways that sort students by race, income, disability, or geography "
        "into separate and unequal schools."
    ),
    "EDUC-STRS-0002": (
        "This rule requires school assignment systems to balance students' "
        "ability to attend a nearby school with ensuring fairness, diversity, "
        "and equal educational opportunity across the system."
    ),

    # ── ZONS: Attendance zones and district boundaries ─────────────────────────
    "EDUC-ZONS-0001": (
        "This rule prohibits drawing or maintaining school district boundaries "
        "in ways that create extreme gaps in resources or student outcomes "
        "between neighboring districts."
    ),
    "EDUC-ZONS-0002": (
        "This rule requires states to periodically review and redraw school "
        "district lines to reduce segregation and make sure all students have "
        "fair access to a quality education."
    ),
    "EDUC-ZONS-0003": (
        "This rule requires states to create regional or multi-district systems "
        "when local district structures are producing persistent inequality that "
        "cannot be fixed within existing boundaries."
    ),
    "EDUC-ZONS-0004": (
        "This rule requires any regional education systems to distribute "
        "resources fairly, allow students to enroll across schools, and "
        "provide transportation so access is real, not just on paper."
    ),

    # ── INTL: Integration methods ─────────────────────────────────────────────
    "EDUC-INTL-0001": (
        "This rule requires education systems to use legal, evidence-based "
        "strategies to bring students of different economic and demographic "
        "backgrounds together in schools, rather than allowing deep "
        "segregation to continue unchallenged."
    ),
    "EDUC-INTL-0002": (
        "This rule allows school assignment systems to consider factors like "
        "neighborhood and family income to reduce segregation and improve "
        "access, rather than relying solely on geographic zones that "
        "mirror housing inequality."
    ),
    "EDUC-INTL-0003": (
        "This rule prohibits tracking programs, gifted education structures, "
        "and selective admissions within public schools from being set up in "
        "ways that effectively separate students by race or income, creating "
        "internal segregation."
    ),

    # ── CHOS: School choice ───────────────────────────────────────────────────
    "EDUC-CHOS-0001": (
        "This rule requires public school choice programs — which let families "
        "apply to schools outside their neighborhood — to expand real access "
        "and opportunity rather than increase segregation or drain resources "
        "from some schools to benefit others."
    ),
    "EDUC-CHOS-0002": (
        "This rule requires charter schools and other public alternative schools "
        "to meet the same equity, open access, and accountability standards as "
        "traditional public schools — they may not operate by different rules "
        "just because they have a different structure."
    ),
    "EDUC-CHOS-0003": (
        "This rule prohibits school choice policies from being used to screen "
        "out or indirectly filter lower-income students, students with "
        "disabilities, or students with academic challenges from certain schools."
    ),

    # ── PRIV: Private schools and public funds ────────────────────────────────
    "EDUC-PRIV-0001": (
        "This rule requires that any public money going to private schools come "
        "with strict accountability conditions — including non-discrimination "
        "requirements and educational quality standards — so public dollars "
        "are used responsibly."
    ),
    "EDUC-PRIV-0002": (
        "This rule prohibits voucher and subsidy programs from enabling school "
        "segregation, excluding certain students, or draining public school "
        "funding in ways that genuinely harm the public education system."
    ),
    "EDUC-PRIV-0003": (
        "This rule applies the same restrictions to tax-credit scholarship "
        "programs, education savings accounts, and other indirect subsidy "
        "schemes as to direct vouchers — because they have the same effect "
        "even if structured differently."
    ),
    "EDUC-PRIV-0004": (
        "This rule prohibits transferring public school funding, facilities, "
        "or staff to private operators in ways that weaken the public school "
        "system's ability to serve all students."
    ),
    "EDUC-PRIV-0005": (
        "This rule requires private K–12 schools with annual revenues over "
        "$1 million to file public financial disclosures — reporting income, "
        "spending, and executive pay — so taxpayers and families can see how "
        "money is being used."
    ),
    "EDUC-PRIV-0006": (
        "This rule requires that any private school accepting public funds — "
        "including vouchers, Title I services, or school lunch funds — employ "
        "only state-credentialed teachers or those actively working toward "
        "credentials."
    ),
    "EDUC-PRIV-0007": (
        "This rule prohibits using public education money — including Title I, "
        "IDEA, or vouchers — to pay for religious instruction, worship services, "
        "or the purchase of religious texts used as primary curriculum. "
        "Public money must fund secular education only."
    ),
    "EDUC-PRIV-0008": (
        "This rule prohibits any federal education funding from flowing to "
        "private or religious schools that discriminate in admissions or "
        "discipline, refuse to administer standard assessments, or hide their "
        "financial information from the public."
    ),
    "EDUC-PRIV-0009": (
        "This rule requires states receiving federal education funds to maintain "
        "oversight of all children educated at home — including annual academic "
        "assessments, welfare checks, and registration — so that no child falls "
        "through the cracks without accountability."
    ),
    "EDUC-PRIV-0010": (
        "This rule requires religious organizations with revenues above $500,000 "
        "to file the same financial disclosures as other nonprofits, fully "
        "enforces the ban on political activity by tax-exempt groups, and "
        "subjects commercial activities of religious organizations to the same "
        "taxes as secular nonprofits."
    ),
    "EDUC-PRIV-0011": (
        "This rule requires the FTC to police false or manipulative fundraising "
        "by religious broadcasters — including fake promises of healings, "
        "guaranteed returns on donations, or targeting elderly and vulnerable "
        "people — and provides refunds to defrauded donors."
    ),

    # ── AINL: AI in education ─────────────────────────────────────────────────
    "EDUC-AINL-0001": (
        "This rule requires that AI systems used in education maintain enough "
        "records to allow students and families to challenge decisions about "
        "grades, placement, discipline, or access — so that an algorithm "
        "cannot make a life-changing decision with no explanation."
    ),
    "EDUC-AINL-0002": (
        "This rule requires that high-impact AI tools in education go through "
        "testing for educational harm, bias, and developmental risk before "
        "being rolled out to students — not after problems are already "
        "causing harm."
    ),
    "EDUC-AINL-0003": (
        "This rule prohibits AI tools that are introduced as tutoring helpers "
        "from quietly expanding their role to make discipline, placement, or "
        "grading decisions without clear authorization and human oversight."
    ),

    # ── DATA: Student data privacy ────────────────────────────────────────────
    "EDUC-DATA-0001": (
        "This rule requires that all data collected about students — including "
        "their behavior and learning activity — be kept private and may not "
        "be used for commercial purposes, advertising, or surveillance outside "
        "of education."
    ),
    "EDUC-DATA-0002": (
        "This rule prohibits schools from collecting more data about students "
        "than is genuinely necessary to provide education, support services, "
        "and ensure safety."
    ),
    "EDUC-DATA-0003": (
        "This rule requires strong justification and safeguards before schools "
        "or vendors can collect sensitive data like biometrics, behavioral "
        "profiles, psychological assessments, or predictive scores on students."
    ),
    "EDUC-DATA-0004": (
        "This rule prohibits the sale, trade, or licensing of student data "
        "for advertising, profiling, or commercial use. Children's school "
        "records are not a product to be bought and sold."
    ),
    "EDUC-DATA-0005": (
        "This rule prohibits education technology companies from using student "
        "data to train their commercial AI models or other unrelated products "
        "that have nothing to do with the student's education."
    ),
    "EDUC-DATA-0006": (
        "This rule prohibits schools from installing broad surveillance systems "
        "that monitor students' behavior beyond what is actually necessary for "
        "safety. Schools must not become surveillance environments."
    ),
    "EDUC-DATA-0007": (
        "This rule prohibits using AI or automated systems to build behavioral "
        "profiles or risk scores on students that then affect their discipline, "
        "opportunities, or access — unless strong safeguards and human review "
        "are in place."
    ),
    "EDUC-DATA-0008": (
        "This rule guarantees that students and families have the right to see "
        "what data schools hold about them, correct errors, and challenge "
        "records they believe are wrong."
    ),
    "EDUC-DATA-0009": (
        "This rule requires schools and education technology providers to "
        "clearly inform students and families about what data is being "
        "collected, how it is used, and who has access to it."
    ),
    "EDUC-DATA-0010": (
        "This rule requires that violations of student data protections trigger "
        "investigation, financial penalties, and corrective action — so that "
        "there are real consequences for mishandling children's data."
    ),
    "EDUC-DATA-0011": (
        "This rule requires education systems to maintain records and oversight "
        "mechanisms tracking how student data is accessed, used, and shared — "
        "creating an audit trail that can be reviewed if something goes wrong."
    ),

    # ── ECES: Early childhood education and childcare ──────────────────────────
    "EDUC-ECES-0001": (
        "This rule establishes early childhood education and childcare as "
        "essential public infrastructure — as important as roads or utilities — "
        "not a private luxury that families must figure out on their own."
    ),
    "EDUC-ECES-0002": (
        "This rule prohibits access to quality early childhood education from "
        "being determined primarily by a family's income, where they live, "
        "or whether their employer offers childcare benefits."
    ),
    "EDUC-ECES-0003": (
        "This rule guarantees universal access to high-quality pre-kindergarten "
        "for all children. Every child must have access to pre-K, not just "
        "those whose families can pay or who live in well-funded districts."
    ),
    "EDUC-ECES-0004": (
        "This rule requires that affordable, high-quality childcare be broadly "
        "available for infants, toddlers, and preschool-age children — not "
        "scarce, unaffordable, or only available in certain neighborhoods."
    ),
    "EDUC-ECES-0005": (
        "This rule requires childcare access systems to include full-time, "
        "part-time, and flexible options so that families with non-standard "
        "work schedules, single parents, and caregivers all have real access."
    ),
    "EDUC-ECES-0006": (
        "This rule requires early childhood programs to meet strong standards "
        "for child development, safety, staffing qualifications, and "
        "educational quality appropriate to the ages of young children."
    ),
    "EDUC-ECES-0007": (
        "This rule requires early childhood education to prioritize language "
        "development, social-emotional growth, play, and curiosity rather "
        "than pushing narrow academic pressure on very young children."
    ),
    "EDUC-ECES-0008": (
        "This rule prohibits using low-quality, basic daycare — 'custodial "
        "warehousing' — as a substitute for real early childhood education "
        "that supports children's development."
    ),
    "EDUC-ECES-0009": (
        "This rule requires that early childhood educators and childcare "
        "workers be paid wages that reflect the critical and demanding "
        "nature of their work — not poverty-level wages that lead to "
        "constant turnover."
    ),
    "EDUC-ECES-0010": (
        "This rule requires the early childhood workforce to have clear paths "
        "to professional training, credentials, and ongoing learning — so "
        "workers can develop skills and build lasting careers."
    ),
    "EDUC-ECES-0011": (
        "This rule prohibits childcare and early education systems from "
        "depending on chronically underpaid workers, burnout, and high "
        "turnover to stay financially afloat. That approach harms both "
        "workers and the children in their care."
    ),
    "EDUC-ECES-0012": (
        "This rule requires early childhood systems to actively correct "
        "unequal access and quality based on income, disability, race, "
        "language, or geography — so that all children get a strong start "
        "regardless of background."
    ),
    "EDUC-ECES-0013": (
        "This rule requires targeted support for rural areas, lower-income "
        "communities, and underserved regions so families there have the same "
        "practical access to quality early childhood education as families "
        "in well-resourced areas."
    ),
    "EDUC-ECES-0014": (
        "This rule requires early childhood programs to include strong "
        "requirements for including and supporting children with disabilities "
        "and developmental differences — not placing them in separate or "
        "inadequate settings."
    ),
    "EDUC-ECES-0015": (
        "This rule requires childcare and early education systems to support "
        "family stability and allow parents and caregivers to work or study "
        "while knowing their children are safe and well cared for."
    ),
    "EDUC-ECES-0016": (
        "This rule prohibits situations where families are forced to leave the "
        "workforce, stop going to school, or abandon training programs because "
        "no affordable childcare is available."
    ),
    "EDUC-ECES-0017": (
        "This rule requires public funding models to reduce childcare costs to "
        "levels families can actually afford in real life — not just technically "
        "subsidized programs that still cost more than families can pay."
    ),
    "EDUC-ECES-0018": (
        "This rule requires early childhood and childcare funding to prioritize "
        "public, nonprofit, and cooperative providers over for-profit companies "
        "that extract profit rather than investing in children."
    ),
    "EDUC-ECES-0019": (
        "This rule prohibits public funding from being used to sustain "
        "low-quality, poorly regulated, or extractive childcare operations "
        "that do not genuinely serve children and families."
    ),
    "EDUC-ECES-0020": (
        "This rule requires government to directly build, support, or coordinate "
        "childcare capacity in places where private markets have failed to "
        "provide enough affordable, high-quality options."
    ),
    "EDUC-ECES-0021": (
        "This rule requires all early childhood providers to comply with "
        "strong standards for health, safety, staff qualifications, and "
        "preventing abuse — so children are protected wherever they are cared for."
    ),
    "EDUC-ECES-0022": (
        "This rule ensures families have easy access to clear information "
        "about a childcare provider's quality rating, licensing status, "
        "past complaints, inspection results, and safety record."
    ),
    "EDUC-ECES-0023": (
        "This rule requires childcare providers with repeated safety failures, "
        "abuse incidents, or quality violations to face corrective action, "
        "sanctions, or loss of public funding."
    ),
    "EDUC-ECES-0024": (
        "This rule calls for early childhood programs to be connected with "
        "K–12 schools, healthcare, disability services, and family support "
        "systems so children's needs are met comprehensively as they grow."
    ),
    "EDUC-ECES-0025": (
        "This rule requires pre-K and childcare programs to screen children "
        "for developmental, educational, and health needs early, and connect "
        "them with needed services — while protecting against stigma or "
        "exclusion based on screening results."
    ),
    "EDUC-ECES-0026": (
        "This rule prohibits childcare systems from being so bureaucratically "
        "complicated — with unstable eligibility rules or reimbursement "
        "failures — that providers close and families cannot get reliable care."
    ),
    "EDUC-ECES-0027": (
        "This rule requires that families and providers be able to navigate "
        "enrollment, payment, subsidies, and support systems clearly and "
        "without excessive paperwork or procedural barriers."
    ),
    "EDUC-ECES-0028": (
        "This rule requires early childhood systems to be evaluated based on "
        "child development outcomes, safety, equity, family stability, and "
        "workforce sustainability — not just how many children are enrolled."
    ),
    "EDUC-ECES-0029": (
        "This rule requires early childhood policy to recognize the long-term "
        "developmental and economic benefits of quality childcare, and "
        "prohibits treating it as simply a private family problem rather "
        "than a public responsibility."
    ),
    "EDUC-ECES-0030": (
        "This rule guarantees universal access to quality childcare as a "
        "public service for all families who need it — not a scarce benefit "
        "available only to some."
    ),
    "EDUC-ECES-0031": (
        "This rule requires childcare costs to be capped relative to household "
        "income, with public subsidies filling the gap so that childcare is "
        "genuinely affordable at every income level — not just for the "
        "very poor or the wealthy."
    ),
    "EDUC-ECES-0032": (
        "This rule requires government to ensure enough childcare spots actually "
        "exist so families do not face long waiting lists, geographic deserts, "
        "or outright unavailability of care."
    ),
    "EDUC-ECES-0033": (
        "This rule requires the government to directly build or operate "
        "childcare programs in places where private markets have failed to "
        "provide enough capacity on their own."
    ),
    "EDUC-ECES-0034": (
        "This rule requires childcare systems to offer hours and schedules that "
        "match how people actually work — including evening and weekend shifts, "
        "variable hours, and part-time employment."
    ),
    "EDUC-ECES-0035": (
        "This rule prohibits childcare from being restricted to limited hours "
        "that effectively exclude working families who cannot pick up children "
        "mid-afternoon."
    ),
    "EDUC-ECES-0036": (
        "This rule prohibits universal childcare programs from turning away "
        "children based on disability, behavioral needs, family income, or "
        "whether parents are employed. Universal means all children."
    ),
    "EDUC-ECES-0037": (
        "This rule requires universal childcare systems to maintain strong "
        "quality and safety standards even as they expand capacity — "
        "preventing low-cost expansion that means worse care for children."
    ),

    # ── SPDS: Special education ───────────────────────────────────────────────
    "EDUC-SPDS-0001": (
        "This rule guarantees every child with a disability the right to a "
        "free, appropriate, high-quality public education with whatever "
        "supports, accommodations, and services they need to actually "
        "learn and progress."
    ),
    "EDUC-SPDS-0002": (
        "This rule prohibits schools from cutting back on special education "
        "rights due to budget shortfalls, staffing shortages, or administrative "
        "inconvenience. These rights must be protected regardless of "
        "those pressures."
    ),
    "EDUC-SPDS-0003": (
        "This rule establishes that educational access for students with "
        "disabilities is a civil rights obligation — not an optional service "
        "that can be provided or withheld based on what is convenient for "
        "the school."
    ),
    "EDUC-SPDS-0004": (
        "This rule requires schools to proactively identify, evaluate, and "
        "support students with disabilities or developmental differences in a "
        "timely way — not wait until families demand it or students fall "
        "far behind."
    ),
    "EDUC-SPDS-0005": (
        "This rule prohibits schools from using delays, denials, or excessive "
        "bureaucratic requirements to avoid their obligation to evaluate "
        "students and provide services."
    ),
    "EDUC-SPDS-0006": (
        "This rule ensures that students can be re-evaluated and receive updated "
        "supports as their needs change — not be stuck with plans that no "
        "longer meet their actual situation."
    ),
    "EDUC-SPDS-0007": (
        "This rule gives families the clear right to request that their child "
        "be evaluated for special education needs, seek an independent "
        "assessment if they disagree, and challenge school determinations "
        "they believe are wrong."
    ),
    "EDUC-SPDS-0008": (
        "This rule requires that students with disabilities receive "
        "individualized supports strong enough to provide real educational "
        "benefit — not just token accommodations that technically satisfy "
        "a legal requirement without helping the child."
    ),
    "EDUC-SPDS-0009": (
        "This rule requires individualized education plans (IEPs) and similar "
        "documents to be specific, enforceable, and written in clear language "
        "that families can actually understand and act on."
    ),
    "EDUC-SPDS-0010": (
        "This rule prohibits schools from offering watered-down or minimally "
        "compliant supports when a student clearly needs stronger, more "
        "individualized help to access their education."
    ),
    "EDUC-SPDS-0011": (
        "This rule requires schools to provide accommodations, therapies, "
        "assistive technology, and related services promptly once they are "
        "identified as necessary — not place students on indefinite waiting lists."
    ),
    "EDUC-SPDS-0012": (
        "This rule requires that students with disabilities be educated "
        "alongside their non-disabled peers to the greatest extent appropriate, "
        "with adequate supports to make that inclusion genuinely beneficial."
    ),
    "EDUC-SPDS-0013": (
        "This rule limits the use of separate, segregated placements to "
        "situations where they are clearly necessary for the student's "
        "well-being — not used as a convenient way for the school to avoid "
        "providing inclusive support."
    ),
    "EDUC-SPDS-0014": (
        "This rule guards against two opposite failures: using the goal of "
        "inclusion as an excuse to withhold specialized services, and using "
        "specialized placement as an excuse to segregate students who could "
        "thrive in inclusive settings."
    ),
    "EDUC-SPDS-0015": (
        "This rule requires schools to have enough qualified special education "
        "teachers, aides, therapists, and related staff to actually meet "
        "students' needs — not just list services in a plan that cannot "
        "be delivered."
    ),
    "EDUC-SPDS-0016": (
        "This rule prohibits schools from using staffing shortages as a reason "
        "to deny or reduce services that students with disabilities are legally "
        "entitled to receive."
    ),
    "EDUC-SPDS-0017": (
        "This rule requires special education staff to receive strong initial "
        "training, ongoing support, and manageable workloads so they can "
        "provide genuinely effective services."
    ),
    "EDUC-SPDS-0018": (
        "This rule gives families meaningful participation rights in all "
        "aspects of their child's special education — including planning, "
        "placement decisions, reviews, and dispute processes — not just "
        "token invitations to meetings."
    ),
    "EDUC-SPDS-0019": (
        "This rule requires schools to explain to families in clear terms what "
        "services their child is entitled to, what options exist, what "
        "timelines apply, and how to appeal decisions they disagree with."
    ),
    "EDUC-SPDS-0020": (
        "This rule requires that advocacy support, translation, and "
        "interpretation services be available to families so that language "
        "barriers or lack of legal knowledge do not prevent them from "
        "exercising their rights."
    ),
    "EDUC-SPDS-0021": (
        "This rule prohibits schools from retaliating against families who "
        "advocate for their child's disability rights, request services, "
        "or challenge school decisions. Standing up for a child's rights "
        "must not lead to punishment."
    ),
    "EDUC-SPDS-0022": (
        "This rule requires that special education rights be enforceable through "
        "accessible complaint processes, hearings, corrective action, court "
        "review, and meaningful remedies — not just paper promises with "
        "no real enforcement."
    ),
    "EDUC-SPDS-0023": (
        "This rule prohibits dispute-resolution systems from being designed "
        "to wear families down through cost, delay, or procedural complexity "
        "until they give up seeking the services their child is owed."
    ),
    "EDUC-SPDS-0024": (
        "This rule requires that when a school fails to provide required "
        "services, remedies must include make-up services, reimbursement, "
        "corrective plans, and additional enforcement — not just an "
        "apology and a promise to do better."
    ),
    "EDUC-SPDS-0025": (
        "This rule requires state or federal intervention, sanctions, and "
        "oversight when a school or district repeatedly or systemically "
        "fails to meet its disability education obligations."
    ),
    "EDUC-SPDS-0026": (
        "This rule prohibits disciplining, excluding, restraining, or removing "
        "students with disabilities at higher rates than other students when "
        "those actions are triggered by disability-related behavior or unmet "
        "support needs."
    ),
    "EDUC-SPDS-0027": (
        "This rule requires schools to consider a student's disability, "
        "communication needs, trauma history, and unmet support needs before "
        "resorting to exclusionary discipline rather than addressing the "
        "root cause."
    ),
    "EDUC-SPDS-0028": (
        "This rule strictly limits the use of physical restraint, seclusion, "
        "and other coercive practices in schools — requiring they be "
        "documented transparently and used only in genuine emergencies, "
        "not as routine management tools."
    ),
    "EDUC-SPDS-0029": (
        "This rule requires that all educational materials, platforms, "
        "facilities, and communications be accessible to students with "
        "disabilities — so a textbook, website, or classroom that cannot "
        "be used is not truly available."
    ),
    "EDUC-SPDS-0030": (
        "This rule requires schools to provide assistive technology, accessible "
        "materials, and adaptive tools to students who need them without "
        "unreasonable delay or passing the costs on to families."
    ),
    "EDUC-SPDS-0031": (
        "This rule requires digital education tools and platforms used in "
        "schools to meet accessibility standards so that students with "
        "disabilities can participate fully in technology-based instruction."
    ),
    "EDUC-SPDS-0032": (
        "This rule requires special education systems to monitor and correct "
        "racial, linguistic, geographic, and income-based disparities in how "
        "students are identified, placed, disciplined, and served."
    ),
    "EDUC-SPDS-0033": (
        "This rule confirms that disability rights in education apply from "
        "early childhood through K–12 and into higher education and vocational "
        "training — not only during traditional school years."
    ),
    "EDUC-SPDS-0034": (
        "This rule requires special education programs to include planning "
        "for adulthood — helping students with disabilities prepare for "
        "employment, college, independent living, and participation "
        "in the community."
    ),
    "EDUC-SPDS-0035": (
        "This rule prohibits transition services for students with disabilities "
        "from being treated as symbolic or optional. They must be real, "
        "tailored to each student's actual goals, and backed by genuine support."
    ),
    "EDUC-SPDS-0036": (
        "This rule requires education systems to collect and publish "
        "standardized data on evaluation timelines, service delivery, "
        "inclusion rates, discipline, and outcomes for students with "
        "disabilities — so progress and failures are visible."
    ),
    "EDUC-SPDS-0037": (
        "This rule requires that special education policy be judged on whether "
        "students actually access education, make progress, and are included "
        "in school life — not just on whether legal paperwork requirements "
        "have been technically satisfied."
    ),

    # ── HSGS: Housing and school access ───────────────────────────────────────
    "EDUC-HSGS-0001": (
        "This rule requires education policy to account for how housing — "
        "including zoning rules, affordability, and displacement — shapes "
        "which schools children can access. Where a family can afford to "
        "live must not determine the quality of schooling their child receives."
    ),
    "EDUC-HSGS-0002": (
        "This rule requires governments to coordinate housing and education "
        "policy together so that the two systems work to reduce school "
        "segregation and expand access to quality schools."
    ),

    # ── PUBL: Strengthening public schools ────────────────────────────────────
    "EDUC-PUBL-0001": (
        "This rule requires government to ensure all public schools meet high "
        "standards for safety, quality, staffing, and resources — so that "
        "families do not feel forced to choose private alternatives just "
        "because their local public school is inadequate."
    ),
    "EDUC-PUBL-0002": (
        "This rule requires public education systems to be continuously "
        "evaluated and improved — not left to stagnate — so that gaps in "
        "quality, access, and outcomes across communities are actively "
        "identified and addressed."
    ),
    "EDUC-PUBL-0003": (
        "This rule requires the public school system to offer diverse program "
        "options — including specialized, vocational, and advanced academic "
        "tracks — within the public system so families do not have to go "
        "private to find those options."
    ),

    # ── VCHS: Anti-voucher ────────────────────────────────────────────────────
    "EDUC-VCHS-0001": (
        "This rule prohibits using public tax dollars to subsidize private K–12 "
        "education through vouchers, tax credits, or similar programs. Public "
        "education money must stay in the public system."
    ),
    "EDUC-VCHS-0002": (
        "This rule requires education policy to focus on making public schools "
        "better rather than creating pathways for students and money to leave "
        "them. Investment must go into the public system."
    ),
    "EDUC-VCHS-0003": (
        "This rule allows narrow exceptions to send students to private "
        "schools only when public options genuinely cannot meet a specific "
        "student's needs, and only with strict rules, tight regulation, and "
        "clear sunset provisions so exceptions do not become permanent policy."
    ),

    # ── FINC: Finance stubs ───────────────────────────────────────────────────
    "EDUC-FINC-0001": (
        "This position addresses student loan debt forgiveness and large-scale "
        "restructuring of the federal student loan system to reduce burdens "
        "on borrowers."
    ),

    # ── STDS: Standards ───────────────────────────────────────────────────────
    "EDUC-STDS-0001": (
        "This rule requires education standards to protect against the use "
        "of schools to impose political or ideological viewpoints on students "
        "rather than teach facts, critical thinking, and civic knowledge."
    ),

    # ── DISS: Discipline reform ───────────────────────────────────────────────
    "EDUC-DISS-0001": (
        "This rule requires schools to move away from zero-tolerance "
        "suspension and expulsion policies toward restorative justice "
        "approaches that repair harm and keep students in school. Exclusionary "
        "discipline — suspension, expulsion, or police referral — may only "
        "be used for genuine safety threats, after other options are exhausted."
    ),
    "EDUC-DISS-0002": (
        "This rule requires schools to publicly report discipline data broken "
        "down by race, disability, and gender and to actively address "
        "disparities. It prohibits police referrals and school-based arrests "
        "for non-violent behavior, and bans using law enforcement in roles "
        "that belong to counselors and support staff."
    ),

    # ── LIBS: Academic freedom / book bans ────────────────────────────────────
    "EDUC-LIBS-0001": (
        "This rule protects K–12 teachers from being fired, disciplined, or "
        "sued for teaching factual, peer-reviewed content in history, science, "
        "civics, or social studies — even when those topics are politically "
        "contested — as long as the content aligns with scholarly consensus."
    ),
    "EDUC-LIBS-0002": (
        "This rule prohibits public school districts from banning books, "
        "classroom materials, or library resources because of the political, "
        "social, or historical viewpoints they represent. Removal of materials "
        "must go through a transparent, educator-led review process based on "
        "educational merit, not political objection."
    ),

    # ── BNDS: Broadband and media literacy ────────────────────────────────────
    "EDUC-BNDS-0001": (
        "This rule guarantees every K–12 student reliable home broadband "
        "internet and a suitable device for schoolwork. Internet access "
        "and devices are treated as essential educational tools — like "
        "textbooks and school buses — and must be funded as such."
    ),
    "EDUC-BNDS-0002": (
        "This rule requires media literacy — including how to evaluate sources, "
        "spot misinformation, understand algorithmic bias, and critically "
        "analyze news — to be integrated as a core curriculum component "
        "from middle school through high school."
    ),

    # ── NTRS: School meals ────────────────────────────────────────────────────
    "EDUC-NTRS-0001": (
        "This rule guarantees every student in a publicly funded K–12 school "
        "free breakfast and lunch regardless of household income or application "
        "status. Schools may not deny meals due to debt, shame students with "
        "meal debt, or pursue families for collection. The school lunch and "
        "breakfast programs must be expanded to provide universal free meals."
    ),

    # ── IMMS: Immigration and education ──────────────────────────────────────
    "EDUC-IMMS-0001": (
        "This rule codifies in federal law the constitutional right — established "
        "by the Supreme Court in Plyler v. Doe — that every child has the right "
        "to a free public K–12 education regardless of immigration status. "
        "Schools may not ask about immigration status, and immigration "
        "enforcement is prohibited on school grounds."
    ),
    "EDUC-IMMS-0002": (
        "This rule requires undocumented students and students with DACA status "
        "to be eligible for federal Pell Grants, student loans, and work-study "
        "on the same terms as other domestic students. States that deny "
        "in-state tuition or financial aid to undocumented students would "
        "lose federal education formula grants."
    ),

    # ── LGBS: LGBTQ+ rights in education ─────────────────────────────────────
    "EDUC-LGBS-0001": (
        "This rule requires amending Title IX by statute to explicitly prohibit "
        "discrimination based on sexual orientation and gender identity in all "
        "federally funded education programs — covering enrollment, discipline, "
        "athletics, facilities, and student organizations. Schools may not out "
        "a student's gender identity to parents without the student's consent."
    ),

    # ── TCHS: Teacher pay floor ───────────────────────────────────────────────
    "EDUC-TCHS-0001": (
        "This rule requires a federal minimum starting teacher salary of "
        "$60,000 per year — adjusted for inflation — as a condition of states "
        "receiving Title I and Title II federal education funding. Teachers "
        "with ten or more years of experience must earn at least 150% of "
        "that floor, and the requirement applies to all publicly funded "
        "schools including charters."
    ),

    # ── FOPS: For-profit school bans ──────────────────────────────────────────
    "EDUC-FOPS-0001": (
        "This rule prohibits for-profit corporations from operating or managing "
        "any publicly funded K–12 school, including charter schools. Existing "
        "for-profit management contracts must be terminated within three years, "
        "and states that continue allowing them lose access to federal "
        "charter school grants."
    ),
    "EDUC-FOPS-0002": (
        "This rule prohibits any new for-profit college from becoming eligible "
        "for federal student aid. Existing for-profit institutions must meet "
        "binding accountability standards — minimum graduation rates, maximum "
        "loan default rates, and minimum earnings-to-debt ratios — or face "
        "a mandatory phase-down of federal aid with no new student enrollment. "
        "Students at institutions that lose eligibility receive automatic "
        "debt cancellation."
    ),

    # ── PKUS: Universal pre-K statute ─────────────────────────────────────────
    "EDUC-PKUS-0001": (
        "This rule requires Congress to establish universal free pre-K as a "
        "statutory entitlement for all 3- and 4-year-olds, funded through a "
        "federal-state formula — not competitive grants. Families denied "
        "access must have a right to appeal, and all pre-K programs must "
        "meet quality, class size, and teacher credentialing standards."
    ),

    # ── HSTS: High-stakes testing ban ─────────────────────────────────────────
    "EDUC-HSTS-0001": (
        "This rule prohibits states and districts from using a single "
        "standardized test score as the sole reason to deny a student "
        "high school graduation, grade promotion, or placement in advanced "
        "courses. All high-stakes decisions must use multiple measures of "
        "student learning."
    ),

    # ── CVMS: Civics graduation requirement ───────────────────────────────────
    "EDUC-CVMS-0001": (
        "This rule conditions federal education funding on states requiring "
        "a full-year high school civics course covering the Constitution, "
        "civil rights history, how government works, and how to participate "
        "in democracy. Curriculum must be developed by educators and historians "
        "— not political appointees — and cannot exclude accurate historical "
        "content about race or gender."
    ),

    # ── FRCS: Free college and debt cancellation ──────────────────────────────
    "EDUC-FRCS-0001": (
        "This rule requires the federal government to eliminate tuition at "
        "all public four-year colleges and universities for domestic students "
        "through a federal-state cost-sharing formula. States must maintain "
        "their own funding levels and may not substitute federal money for "
        "existing state investment. Room, board, and textbooks must be "
        "addressed through expanded Pell Grants."
    ),
    "EDUC-FRCS-0002": (
        "This rule requires Congress to cancel all outstanding federal student "
        "loan principal, interest, and fees for all borrowers automatically "
        "— with no application or income verification required. Borrowers "
        "who overpaid under income-driven repayment must receive refunds, "
        "and cancellation must be paired with tuition-free public college "
        "to prevent debt from rebuilding."
    ),

    # ── GRDS: Graduate student and adjunct rights ─────────────────────────────
    "EDUC-GRDS-0001": (
        "This rule requires graduate students who perform teaching, research, "
        "or administrative work at federally funded institutions to be "
        "recognized as employees with full collective bargaining rights. "
        "Their stipends must be at or above the local cost of living, and "
        "institutions must provide comprehensive health insurance at no "
        "cost to the worker."
    ),
    "EDUC-GRDS-0002": (
        "This rule requires institutions receiving federal funding to pay "
        "adjunct and contingent faculty at least $7,000 per course section "
        "(adjusted for inflation) and offer multi-year contracts to those "
        "who have taught for three or more consecutive semesters. Institutions "
        "where adjuncts teach more than half of student contact hours must "
        "convert a proportionate number to full-time positions within "
        "five years."
    ),
    "EDUC-GRDS-0003": (
        "This rule requires federally funded colleges and universities to "
        "maintain formal shared governance structures giving faculty bodies "
        "binding authority over academic standards, curriculum, and faculty "
        "hiring. Student governance bodies must have voting representation on "
        "governing boards and budget committees."
    ),

    # ── IDAS: IDEA enforcement ────────────────────────────────────────────────
    "EDUC-IDAS-0001": (
        "This rule requires amending the Individuals with Disabilities "
        "Education Act (IDEA) to give families of students with disabilities "
        "the explicit right to sue school districts for money damages when "
        "schools fail to provide a free appropriate public education. "
        "Prevailing families must be awarded attorney fees, and class action "
        "suits must be allowed for systemic violations."
    ),

    # ── CHRS: Charter and voucher accountability ──────────────────────────────
    "EDUC-CHRS-0001": (
        "This rule prohibits charter schools and private school voucher "
        "programs from being structured in ways that drain resources from "
        "the public school system without being held to the same accountability "
        "and open-access requirements as public schools."
    ),

    # ── RGTS: Constitutional right to education ───────────────────────────────
    "EDUC-RGTS-0001": (
        "This position establishes that all persons have a constitutionally "
        "protected right to quality public education — making access to "
        "good schooling a fundamental legal right, not a privilege "
        "dependent on where someone is born or how much money their "
        "family has."
    ),

    # ── EARL: Early childhood policy specifics ────────────────────────────────
    "EDUC-EARL-0001": (
        "This rule requires Congress to enact universal free, full-day pre-K "
        "for all 3- and 4-year-olds through a 90/10 federal-state cost-sharing "
        "model funded at no less than $50 billion annually. Class sizes must "
        "be capped at 15, lead teachers must hold at least a bachelor's degree "
        "in early childhood education, and teacher pay must equal that of "
        "K–12 teachers with equivalent credentials."
    ),
    "EDUC-EARL-0002": (
        "This rule requires Congress to cap childcare costs at 7% of family "
        "income for families between 75% and 150% of the State Median Income, "
        "with zero cost for lower-income families, through an $80 billion "
        "annual federal investment. Lead childcare teachers must be paid at "
        "least $25 per hour with full benefits, and a $10 billion fund must "
        "build childcare facilities in areas with too few spots."
    ),
    "EDUC-EARL-0003": (
        "This rule requires Congress to establish a national paid family and "
        "medical leave program guaranteeing all workers — including part-time "
        "and gig workers — at least 12 weeks of fully paid leave per year for "
        "new children, serious illness, or caregiving. Workers earning up to "
        "150% of the federal minimum wage receive 100% wage replacement. "
        "Employers may not penalize workers for taking leave, with criminal "
        "penalties for willful violations."
    ),
    "EDUC-EARL-0004": (
        "This rule requires Congress to make universal free school meals "
        "permanent for all students in public schools, eliminating means-testing "
        "and lunch debt. It expands summer food programs to reach every child "
        "in need, prohibits junk food marketing on school grounds, and funds "
        "$500 million annually for farm-to-school programs connecting local "
        "producers with school cafeterias."
    ),

    # ── EQFS, IDEA, SRCS stubs (placeholder IDs) ─────────────────────────────
    "EDUC-EQFS-0001": (
        "This position addresses educational equity and funding standards to "
        "ensure all students receive fair access to quality education "
        "regardless of where they live."
    ),
    "EDUC-EQFS-0002": (
        "This position addresses educational equity and funding standards to "
        "ensure all students receive fair access to quality education "
        "regardless of where they live."
    ),
    "EDUC-EQFS-0003": (
        "This position addresses educational equity and funding standards to "
        "ensure all students receive fair access to quality education "
        "regardless of where they live."
    ),
    "EDUC-IDEA-0001": (
        "This position addresses the Individuals with Disabilities Education "
        "Act (IDEA) — ensuring students with disabilities receive the "
        "educational supports, accommodations, and legal protections they "
        "are entitled to."
    ),
    "EDUC-IDEA-0002": (
        "This position addresses the Individuals with Disabilities Education "
        "Act (IDEA) — ensuring students with disabilities receive the "
        "educational supports, accommodations, and legal protections they "
        "are entitled to."
    ),
    "EDUC-SRCS-0001": (
        "This position establishes source and evidentiary standards for "
        "education policy — requiring that policy claims be grounded in "
        "credible, peer-reviewed research."
    ),
    "EDUC-SRCS-0002": (
        "This rule prohibits standardized test scores from serving as the "
        "sole basis for high-stakes decisions such as grade retention, "
        "graduation denial, or college admission rejection. All high-stakes "
        "determinations must incorporate multiple measures — including grades, "
        "teacher evaluations, portfolios, and attendance — and students "
        "denied promotion solely on a test score have a private right of action."
    ),

    # ── Old-format IDs (EDU-EQF, EDU-IDEA, EDU-SRC) ──────────────────────────
    "EDU-EQF-001": (
        "This position addresses educational equity and funding — ensuring "
        "all students have fair access to the resources they need to "
        "succeed in school."
    ),
    "EDU-EQF-002": (
        "This position addresses educational equity and funding — ensuring "
        "all students have fair access to the resources they need to "
        "succeed in school."
    ),
    "EDU-EQF-003": (
        "This position addresses educational equity and funding — ensuring "
        "all students have fair access to the resources they need to "
        "succeed in school."
    ),
    "EDU-IDEA-001": (
        "This position addresses the Individuals with Disabilities Education "
        "Act — ensuring students with disabilities receive the supports and "
        "legal protections they are entitled to."
    ),
    "EDU-IDEA-002": (
        "This position addresses the Individuals with Disabilities Education "
        "Act — ensuring students with disabilities receive the supports and "
        "legal protections they are entitled to."
    ),
    "EDU-SRC-001": (
        "This position establishes standards for sourcing and evidence in "
        "education policy — requiring claims to be grounded in credible "
        "research."
    ),
    "EDU-SRC-002": (
        "This rule prohibits standardized test scores from being the sole "
        "basis for high-stakes educational decisions like grade retention or "
        "graduation denial. Schools receiving federal funds must use multiple "
        "measures — grades, teacher evaluations, portfolios, and attendance — "
        "and students denied promotion solely on a test score have a "
        "private right of action."
    ),

    # ── TEST: Standardized testing ────────────────────────────────────────────
    "EDUC-TEST-0001": (
        "This rule prohibits standardized test scores from being the sole basis "
        "for denying a student graduation, grade promotion, or college "
        "admission in any federally funded school. All high-stakes decisions "
        "must use multiple measures including grades, teacher evaluations, "
        "and portfolios, and students wrongly denied solely on a test score "
        "have a private right of action."
    ),
    "EDUC-TEST-0002": (
        "This rule requires all companies that produce standardized tests used "
        "for high-stakes K–12 or college admissions decisions to publish annual "
        "reports disclosing score gaps by race, income, disability status, and "
        "English learner status. A test that shows statistically significant "
        "adverse impact on a protected group without educational justification "
        "is presumptively a civil rights violation."
    ),
    "EDUC-TEST-0003": (
        "This rule gives parents and guardians the right to opt their children "
        "out of standardized tests in federally funded schools, with no "
        "academic penalty to the student or loss of educational services. "
        "Schools may not coerce participation, and states may not override "
        "parental opt-out rights."
    ),
    "EDUC-TEST-0004": (
        "This rule requires states to competitively procure standardized "
        "testing contracts and prohibits a single company from controlling "
        "both test development and scoring in the same state without independent "
        "oversight. All contracts over $10 million must be reviewed for "
        "cost-effectiveness and made public, and testing companies must "
        "disclose conflicts of interest."
    ),

    # ── HOME: Homeschooling ───────────────────────────────────────────────────
    "EDUC-HOME-0001": (
        "This rule requires states receiving federal K–12 education funds to "
        "require annual registration of all homeschooled children with the local "
        "school district, an annual in-person welfare check, and documentation "
        "of curriculum used. Homeschooled children must have equal access to "
        "public school extracurricular activities, counseling, and special "
        "education services."
    ),
    "EDUC-HOME-0002": (
        "This rule requires quarterly welfare checks by a licensed social worker "
        "for any homeschooled child who was previously identified as at risk by "
        "child protective services, a school, or a court. Parents who withdraw "
        "a child from school within 30 days of a CPS contact must notify the "
        "school district, triggering an immediate welfare check within 14 days."
    ),
    "EDUC-HOME-0003": (
        "This rule requires that homeschooled students who complete a program "
        "meeting state academic standards receive a credential recognized by "
        "all public colleges and universities in the state. Colleges may not "
        "require homeschooled applicants to submit GED scores if they have "
        "documented a compliant homeschool program, and states must establish "
        "a standard homeschool transcript format."
    ),

    # ── CURR: History and civics curriculum ───────────────────────────────────
    "EDUC-CURR-0001": (
        "This rule conditions federal education funding on state K–12 history "
        "and social studies curricula meeting national academic framework "
        "standards, preventing any single state's distorted textbook market "
        "from becoming the de facto national curriculum. The Department of "
        "Education must review state history standards for civil rights "
        "compliance."
    ),
    "EDUC-CURR-0002": (
        "This rule requires all K–12 schools receiving federal funds to include "
        "accurate, age-appropriate instruction on slavery, Reconstruction, Jim "
        "Crow, the Civil Rights Movement, and systemic racism. State laws that "
        "ban teaching 'divisive concepts' or restrict accurate racial history "
        "instruction are preempted by federal law, and schools cannot discipline "
        "teachers for providing historically accurate instruction."
    ),
    "EDUC-CURR-0003": (
        "This rule requires Congress to establish federal minimum standards for "
        "K–12 U.S. History, Civics, and Social Studies — including the full "
        "history of slavery, Reconstruction, Indigenous displacement, Jim Crow, "
        "and civil rights movements — and condition all federal education "
        "funding on state compliance. State boards may not adopt standards that "
        "omit, minimize, or mischaracterize required topics, and violations "
        "carry fines up to $500,000 per academic year plus suspension of "
        "federal funding."
    ),
    "EDUC-CURR-0004": (
        "This rule requires Congress to mandate at least one semester of "
        "comprehensive civics as a graduation requirement in all federally "
        "funded schools, covering the Constitution, voting rights history, how "
        "laws are made, and media literacy. Schools must provide voter "
        "registration assistance to students turning 18 before the next "
        "election, with civil penalties of up to $50,000 per year for "
        "non-compliance."
    ),

    # ── VCHR: Voucher regulation ──────────────────────────────────────────────
    "EDUC-VCHR-0001": (
        "This rule prohibits using any federal education funding — including "
        "Title I, IDEA, E-Rate, or school lunch programs — directly or "
        "indirectly to fund private school vouchers, education savings "
        "accounts, or tax credit scholarship programs that redirect public "
        "dollars to private or religious schools."
    ),
    "EDUC-VCHR-0002": (
        "This rule requires any private or religious school that accepts "
        "publicly funded vouchers or education savings accounts to comply "
        "with all federal civil rights laws — including prohibitions on "
        "discrimination based on race, sex, disability, and LGBTQ+ status "
        "— to the same degree as public schools."
    ),
    "EDUC-VCHR-0003": (
        "This rule requires any school accepting publicly funded voucher "
        "students to administer the same state standardized assessments as "
        "public schools, publish annual school performance reports, and be "
        "subject to closure or loss of voucher eligibility for persistently "
        "poor performance. Voucher funds may not be used for religious "
        "instruction."
    ),
    "EDUC-VCHR-0004": (
        "This rule prohibits public vouchers, education savings accounts, or "
        "tax credit scholarship funds from being used at any school whose "
        "science curriculum teaches creationism or intelligent design as "
        "scientific alternatives to evolution, or that denies the scientific "
        "consensus on human-caused climate change."
    ),
    "EDUC-VCHR-0005": (
        "This rule prohibits any public voucher, education savings account, or "
        "tax credit scholarship from being used at a private school that "
        "discriminates in admissions, discipline, or employment based on race, "
        "sex, sexual orientation, gender identity, disability, or religion of "
        "the student. Schools that discriminate may not accept publicly funded "
        "voucher students."
    ),

    # ── HIED: Higher ed loan and accountability detail ────────────────────────
    "EDUC-HIED-0001": (
        "This rule requires the Department of Education to cancel all federal "
        "student loans for borrowers who attended predatory institutions, "
        "provide automatic cancellation after 20 years in repayment, expand "
        "Public Service Loan Forgiveness to all public and nonprofit workers "
        "after 10 years, and implement a single income-driven repayment plan "
        "capping payments at 5% of discretionary income."
    ),
    "EDUC-HIED-0002": (
        "This rule requires the federal government to fund tuition-free "
        "attendance at all public two-year community colleges and technical "
        "schools for all U.S. residents regardless of income or immigration "
        "status. The Pell Grant must be doubled to cover the full cost of "
        "attendance at the lowest-cost public four-year institution in "
        "each state and indexed to inflation."
    ),
    "EDUC-HIED-0003": (
        "This rule reinstates and strengthens the gainful employment rule: "
        "any institution whose graduates' median annual loan payment exceeds "
        "8% of their median earnings must submit a remediation plan, and "
        "institutions that fail two consecutive years lose access to federal "
        "student aid. The 90/10 rule is tightened so for-profit colleges "
        "may receive no more than 85% of revenues from federal sources, "
        "and students defrauded by school misrepresentation receive "
        "automatic debt cancellation."
    ),
    "EDUC-HIED-0004": (
        "This rule requires the Department of Education to consolidate federal "
        "student loan servicing into a single nonprofit or government-operated "
        "servicer, prohibit steering borrowers into forbearance instead of "
        "income-driven repayment, and require proactive notification of all "
        "repayment, forgiveness, and deferment options. Servicers that cause "
        "borrowers to lose loan forgiveness credit through erroneous guidance "
        "must restore lost credit and pay restitution."
    ),

    # ── VETS: Veterans education ──────────────────────────────────────────────
    "EDUC-VETS-0001": (
        "This rule requires Congress to extend Post-9/11 GI Bill benefits from "
        "36 to 48 months, eliminate the 15-year expiration so veterans retain "
        "benefits for life, expand covered programs to include apprenticeships, "
        "industry certifications, and bootcamps, and pay housing allowance at "
        "the full E-5 with-dependents rate for all half-time or greater "
        "enrollment — including online students."
    ),
    "EDUC-VETS-0002": (
        "This rule permanently closes the 90/10 loophole by counting GI Bill "
        "funding toward for-profit colleges' federal revenue cap. It bans any "
        "school found to have misrepresented job placement rates, faced consumer "
        "protection enforcement, or lost accreditation from receiving GI Bill "
        "or military tuition assistance funding, and requires full refunds to "
        "affected veterans. Criminal liability of up to 10 years applies to "
        "administrators who knowingly deceive veterans."
    ),
    "EDUC-VETS-0003": (
        "This rule makes permanent and expands the requirement that all public "
        "colleges and universities charge veterans, active-duty service members, "
        "and their dependents in-state tuition with no waiting period — "
        "regardless of residency. It extends the mandate to National Guard "
        "and Reserve members, requires priority course registration for "
        "veterans, and mandates a Veterans Resource Center staffed by "
        "a VA-certified official at every public institution."
    ),
    "EDUC-VETS-0004": (
        "This rule requires Congress to increase DoDEA school funding to the "
        "90th percentile of national per-pupil spending, fully fund Impact Aid "
        "for districts hosting military families on tax-exempt land, enforce "
        "the Interstate Compact on Military Children's Education in all states, "
        "and establish a Military Children's Education Advocate in every "
        "state to resolve disputes arising from frequent moves."
    ),

    # ── SCHL: School funding equalization ─────────────────────────────────────
    "EDUC-SCHL-0001": (
        "This rule requires Congress to appropriate $100 billion over five "
        "years to guarantee every public school district reaches per-student "
        "funding of at least 85% of its state's average — with federal grants "
        "covering 100% of the gap for the lowest-funded quarter of districts. "
        "States must adopt needs-weighted funding formulas, prohibit student "
        "fees for any core academic program or activity, and a $20 billion "
        "Teacher Compensation Fund ensures no teacher earns less than "
        "$60,000 per year."
    ),

    # ── HMSC: Homeschool safety ───────────────────────────────────────────────
    "EDUC-HMSC-0001": (
        "This rule conditions federal education funding on states requiring "
        "annual homeschool registration — including the child's name, age, "
        "address, and household adults — curriculum documentation, annual "
        "standardized academic assessment, and at least one annual in-person "
        "or video welfare check for every homeschooled child. Every "
        "homeschooled child must have the right to access individual public "
        "school courses and special education services."
    ),
    "EDUC-HMSC-0002": (
        "This rule conditions federal child welfare and education funding on "
        "states establishing a Homeschool Child Safety Protocol requiring "
        "automatic welfare checks when registration is overdue, immediate checks "
        "for children who were previously flagged for abuse concerns before "
        "being withdrawn from public school, and a centralized state registry "
        "of all registered homeschool children accessible to law enforcement "
        "and child protective services."
    ),

    # ── STDT: Student debt detail ─────────────────────────────────────────────
    "EDUC-STDT-0001": (
        "This rule requires Congress to cancel all outstanding federal student "
        "loan principal, interest, and fees for every borrower who attended "
        "any Title IV-eligible school — automatically, 90 days after enactment. "
        "Going forward, income-driven repayment is capped at 5% of "
        "discretionary income with automatic forgiveness after 10 years for "
        "balances of $50,000 or less, and student loan interest rates are "
        "capped at the 10-year Treasury rate."
    ),
}


def insert_or_fill_plain(card, plain_text: str) -> bool:
    """
    Insert or fill a <p class="rule-plain"> in the card.
    Returns True if a change was made.
    """
    existing = card.find("p", class_="rule-plain")
    if existing is not None:
        if not existing.get_text(strip=True):
            existing.string = plain_text
            return True
        return False

    # No rule-plain exists — insert one after rule-title (before rule-stmt)
    title_tag = card.find("p", class_="rule-title")
    if title_tag is None:
        return False

    soup_ref = title_tag.find_parent()  # parent node
    from bs4 import BeautifulSoup as BS4
    new_p = BS4(f'<p class="rule-plain">{plain_text}</p>', "html.parser").find("p")
    title_tag.insert_after(new_p)
    return True


def main() -> None:
    html_path = Path("docs/pillars/education.html")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    updated = 0
    skipped_no_id = 0
    skipped_no_match = 0

    for card in soup.find_all("div", class_="policy-card"):
        card_id = card.get("id", "").strip()
        if not card_id:
            skipped_no_id += 1
            continue
        if card_id not in PLAIN_LANGUAGE:
            skipped_no_match += 1
            continue
        if insert_or_fill_plain(card, PLAIN_LANGUAGE[card_id]):
            updated += 1

    html_path.write_text(str(soup), encoding="utf-8")
    print(f"Updated {updated} cards")
    if skipped_no_id:
        print(f"Skipped {skipped_no_id} cards with no ID")
    if skipped_no_match:
        print(f"Skipped {skipped_no_match} cards not in PLAIN_LANGUAGE dict")


if __name__ == "__main__":
    main()
