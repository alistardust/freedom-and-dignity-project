from bs4 import BeautifulSoup
from pathlib import Path

PLAIN_LANGUAGE = {
    # SYSR — System/Structural
    "LABR-SYSR-0001": "This position holds that work must give people fair pay, safe conditions, dignity, and freedom — and must protect them from being exploited by the people who employ them.",
    "LABR-SYSR-0002": "This position holds that workers must receive a fair share of the value they produce, and the rules of the labor market may not be structured to systematically shortchange workers while enriching employers.",
    "LABR-SYSR-0003": "This position prohibits employment systems that use fear, financial desperation, or power imbalances to keep workers compliant — the workplace must operate on fair and equal terms, not coercion.",

    # RGTS — Rights
    "LABR-RGTS-0001": "This position guarantees every worker the right to fair pay, safe conditions, reasonable hours, and protection from discrimination and retaliation — no exceptions.",
    "LABR-RGTS-0002": "This position ensures that your labor rights are clear and legally enforceable no matter what kind of job you have, how much you earn, or what industry you work in.",
    "LABR-RGTS-0003": "This position requires that labor protections apply equally to every type of worker — full-time, part-time, contract, gig, and temp — so that classification cannot be used to strip anyone of their rights on the job.",

    # PAYS — Pay/Compensation
    "LABR-PAYS-0001": "This position holds that your paycheck must be enough to actually live on — covering housing, food, healthcare, and transportation — not merely token compensation that leaves workers in poverty.",
    "LABR-PAYS-0002": "This position requires that pay be transparent, predictable, and free of hidden deductions or manipulation so that workers always know what they're earning and why.",
    "LABR-PAYS-0003": "This position treats wage theft, worker misclassification, unpaid labor, and delayed paychecks as serious violations — not minor technicalities — and demands strong enforcement with real consequences.",
    "LABR-PAYS-0004": "This position holds that when the gap between CEO pay and worker pay exists because executives are extracting wealth rather than creating it, that gap must be limited.",
    "LABR-PAYS-0005": "This position requires companies to publicly report how much they pay top executives compared to their average worker, using a standardized format that anyone can read and compare.",
    "LABR-PAYS-0006": "This position permits the government to use taxes, regulations, or governance tools to discourage companies from heaping extreme rewards on executives while leaving workers behind.",
    "LABR-PAYS-0007": "This position prohibits pay structures that reward executives for short-term gains at the expense of workers, product quality, or the long-term health of the business.",
    "LABR-PAYS-0008": "This position requires all employers with 25 or more workers to post the full salary or hourly pay range on every job listing — internal or external — share it with any applicant before a first interview, and never ask about or use a candidate's prior salary. Violations carry civil fines of $1,000 per posting, and workers can sue — including as a class — for systemic violations.",
    "LABR-PAYS-0009": "This position requires employers with 100 or more employees to submit yearly pay equity audits to the EEOC broken down by race, sex, and ethnicity, with results published in a public searchable database within 90 days. Employers whose pay gaps persist over two or more audit cycles must file binding remediation plans, and workers can sue for systemic pay discrimination.",
    "LABR-PAYS-0010": "This position makes the Pregnant Workers Fairness Act permanent and stronger — expanding it to all employers regardless of size, protecting workers for 12 months after birth, covering pregnancy loss including miscarriage and abortion, and banning any adverse action for requesting or using pregnancy-related accommodations. Workers have up to four years to file a lawsuit and can seek compensatory and punitive damages.",

    # LVES — Leave
    "LABR-LVES-0001": "This position guarantees every worker paid time off — including vacation, sick days, parental leave, and medical leave — so that taking care of yourself and your family doesn't cost you your livelihood.",
    "LABR-LVES-0002": "This position requires that paid leave actually works in practice — meaning enough days off and genuinely accessible to lower-wage and hourly workers who need it most, not just on paper.",
    "LABR-LVES-0003": "This position prohibits employers from punishing, retaliating against, or shortchanging workers who use the paid leave they're legally entitled to.",
    "LABR-LVES-0004": "This position requires governments to ensure that workers at small businesses can access paid leave through subsidies, pooled systems, or public programs — so small employers are not left to bear the cost alone.",
    "LABR-LVES-0005": "This position requires that leave systems cover caregiving, family crises, reproductive healthcare, recovery, and major life events — so workers are never forced to choose between keeping their job and meeting a basic human need.",

    # SURS — Surveillance
    "LABR-SURS-0001": "This position prohibits employers from using invasive surveillance — cameras, biometrics, or behavioral tracking — in ways that undermine your privacy, dignity, or ability to make your own decisions at work without clear justification.",
    "LABR-SURS-0002": "This position holds that constant monitoring of workers through cameras, biometric scanners, keystroke logging, or behavioral analytics must be limited by law and subject to clear, enforceable rules.",
    "LABR-SURS-0003": "This position requires that any data collected about workers be gathered transparently, kept to a minimum, and used only for legitimate work purposes — not to build a surveillance dossier or control behavior.",
    "LABR-SURS-0004": "This position guarantees workers the right to know what data their employer is collecting about them, how it is being used, and to challenge any misuse of that information.",
    "LABR-SURS-0005": "This position prohibits employers from using monitoring systems to enforce unreasonable productivity targets, punish lawful on-the-job behavior, or create a pressure-cooker environment that strips workers of their autonomy.",

    # HRSS — Hours/Scheduling
    "LABR-HRSS-0001": "This position holds that your work schedule must be reasonably predictable and stable — employers may not arbitrarily change your hours at the last minute without compensating you for the disruption to your life.",
    "LABR-HRSS-0002": "This position holds that extreme working hours that harm your health, safety, or quality of life must be limited by law.",
    "LABR-HRSS-0003": "This position guarantees workers overtime pay when they work beyond set hour limits — including salaried workers whose pay does not reflect the extra hours they actually put in.",
    "LABR-HRSS-0004": "This position requires scheduling protections that account for real life — caregiving responsibilities, health conditions, disabilities, education, and basic life planning — so your schedule doesn't punish you for having obligations outside work.",
    "LABR-HRSS-0005": "This position prohibits employers from using unpredictable on-call shifts, chronic under-scheduling, or wildly fluctuating hours as a tool to control workers — unless workers receive compensation and legal safeguards in return.",
    "LABR-HRSS-0006": "This position requires employers to define your work hours in writing, and prohibits penalizing workers for not responding to calls, messages, or emails outside those hours. Any work done outside scheduled hours at a supervisor's direction counts as overtime and must be compensated at the overtime rate — and employers cannot contract around this protection.",

    # COES — Coercion
    "LABR-COES-0001": "This position prohibits employers from using financial pressure, scheduling power, or benefit threats to coerce workers into accepting unfair conditions — your employer cannot hold your livelihood hostage to demand compliance.",
    "LABR-COES-0002": "This position ensures that workers can actually leave a bad job without facing impossible obstacles — like non-compete clauses, retaliation threats, or losing essential benefits simply for seeking better work elsewhere.",

    # CLSS — Classification
    "LABR-CLSS-0001": "This position requires that how a worker is classified — employee, contractor, or otherwise — reflect the real working relationship, and prohibits employers from manipulating labels to avoid paying benefits or providing legal protections.",
    "LABR-CLSS-0002": "This position treats the misclassification of employees as independent contractors as a serious legal violation with enforcement penalties — not a minor paperwork error to be quietly corrected.",
    "LABR-CLSS-0003": "This position designates the willful misclassification of employees as federal wage theft, carrying criminal penalties for executives who authorize it, triple damages for affected workers, class action rights, and joint liability for companies that knowingly benefit from misclassified labor. No statute of limitations applies when the employer actively concealed the misclassification.",

    # COLS — Collective/Organizing
    "LABR-COLS-0001": "This position guarantees workers the right to form a union, join one, and negotiate collectively over their pay and working conditions — without fear of retaliation or employer interference.",
    "LABR-COLS-0002": "This position prohibits employers from engaging in union-busting, intimidation, or any effort to interfere with workers who are trying to organize and act collectively.",
    "LABR-COLS-0003": "This position requires that your right to organize and bargain together be real and enforceable — not just a technicality that employers can frustrate with delays and legal tactics.",
    "LABR-COLS-0004": "This position holds that collective bargaining is a vital check on the power of large employers and must be protected as a core labor right — not a privilege that employers can choose to respect or ignore.",
    "LABR-COLS-0005": "This position extends collective bargaining rights to all types of workers — including gig workers, contractors, and those in non-traditional arrangements — so that no one can be excluded from organizing based on how their job is structured.",
    "LABR-COLS-0006": "This position requires removing legal barriers that prevent workers from organizing simply because of their job classification or the industry they work in.",
    "LABR-COLS-0007": "This position guarantees government workers the right to organize and bargain collectively, with appropriate safeguards for truly essential services where strikes could cause serious public harm.",
    "LABR-COLS-0008": "This position holds that any restrictions on collective action in essential services — such as limits on striking — must be narrowly drawn and paired with real alternative dispute-resolution options, so workers are not left without bargaining power.",

    # SFTS — Safety
    "LABR-SFTS-0001": "This position requires employers to maintain safe workplaces and prohibits them from exposing workers to preventable harm or hazardous conditions.",
    "LABR-SFTS-0002": "This position guarantees workers the right to report unsafe conditions on the job and to refuse dangerous work — without fear of being fired, disciplined, or penalized for speaking up.",
    "LABR-SFTS-0003": "This position makes any willful OSHA violation that kills a worker a felony with a minimum 10-year prison sentence. Corporate officers who knew about the hazard face personal criminal liability. OSHA penalties survive bankruptcy so companies cannot escape accountability through restructuring.",
    "LABR-SFTS-0004": "This position requires employers with 50 or more workers to assess and address mental health hazards on the job — like chronic overwork, understaffing, harassment, or trauma exposure — and to provide free, confidential mental health resources. Workers' compensation must cover job-related mental health conditions on the same terms as physical injuries, and reporting psychosocial hazards is protected from retaliation.",

    # TRAN — Transition/Transparency
    "LABR-TRAN-0001": "This position requires employers to tell workers upfront about the key terms of their job — wages, schedule, benefits, and any monitoring or surveillance practices — so there are no hidden surprises after you've started.",
    "LABR-TRAN-0002": "This position holds that when the economy shifts, workers should not bear the cost of changes they did not cause — transition systems must be designed to support worker stability, not punish people for market forces beyond their control.",
    "LABR-TRAN-0003": "This position holds that employers and platforms that eliminate jobs through automation or restructuring should contribute to worker retraining and transition support — the costs of technological progress should not fall entirely on the workers displaced by it.",

    # ENFL — Enforcement
    "LABR-ENFL-0001": "This position requires that violations of labor law carry real consequences — including financial penalties, restitution to harmed workers, and mandatory corrective action — not just warnings.",
    "LABR-ENFL-0002": "This position guarantees that workers can actually report violations and seek remedies through accessible channels — without facing retaliation for speaking up about what was done to them.",
    "LABR-ENFL-0003": "This position requires that the government agencies responsible for enforcing labor law have enough funding, authority, and independence to actually do their job — they cannot be defunded or hamstrung into uselessness.",
    "LABR-ENFL-0004": "This position requires that employers who repeatedly break labor law face escalating consequences — including restrictions on government contracts — rather than treating violations as an acceptable cost of doing business.",
    "LABR-ENFL-0005": "This position ensures that workers can sue to enforce their collective bargaining rights themselves when public enforcement agencies are not getting the job done.",
    "LABR-ENFL-0006": "This position requires enforcement agencies to have the authority to investigate labor violations, bring charges, and pursue accountability not only against corporations but against the individual executives and managers who directed the violations.",
    "LABR-ENFL-0007": "This position ensures labor rights are enforceable through multiple channels — government action, individual lawsuits, collective remedies, and strong anti-retaliation protections — so workers always have a real path to justice.",
    "LABR-ENFL-0008": "This position requires that repeat labor lawbreakers face escalating consequences — including heavy fines, restitution, personal liability for leaders, loss of government contracts, and structural intervention when ordinary penalties are not working.",
    "LABR-ENFL-0009": "This position requires that labor systems be judged by real-world outcomes — like whether wages are growing, workers can organize, and exploitation is declining — not just whether companies filed the right paperwork.",

    # UNNS — Union/Organizing Standards
    "LABR-UNNS-0001": "This position requires that forming a union be fast and fair — free from employer delay tactics and procedural manipulation — so workers can organize when they choose to without years of obstruction.",
    "LABR-UNNS-0002": "This position prohibits employers from using procedural tricks or legal maneuvering to drag out, challenge, or derail a union election once workers have begun organizing.",
    "LABR-UNNS-0003": "This position requires that when a majority of workers demonstrate they want a union — through verified means — union recognition must happen promptly without unnecessary bureaucratic delay.",
    "LABR-UNNS-0004": "This position gives workers the option to form a union simply by signing authorization cards — a majority-sign-up method — rather than being forced through a prolonged formal election process.",
    "LABR-UNNS-0005": "This position prohibits employers from engaging in union-busting tactics — including intimidating workers, forcing them to attend anti-union meetings, surveilling organizing activity, or sending coercive messages designed to discourage organizing.",
    "LABR-UNNS-0006": "This position requires that any employer who retaliates against workers for organizing — by firing them, disciplining them, or cutting their hours — face immediate enforcement and real legal remedies.",
    "LABR-UNNS-0007": "This position requires that penalties for violating union rights be serious enough to actually deter employers — not nominal fines that large companies simply absorb as the cost of fighting unions.",
    "LABR-UNNS-0008": "This position prohibits employers from splitting up their workforce, relabeling jobs, or restructuring the company specifically to avoid collective bargaining obligations.",
    "LABR-UNNS-0009": "This position prohibits the use of corporate structures — such as subsidiaries, franchises, or shell companies — as shields to escape collective bargaining responsibilities.",
    "LABR-UNNS-0010": "This position guarantees workers the ability to communicate with each other about organizing — through digital platforms and physical spaces at work — without employer interference or monitoring.",
    "LABR-UNNS-0011": "This position prohibits employers from restricting or punishing lawful communication among workers related to organizing, solidarity, or collective action.",
    "LABR-UNNS-0012": "This position holds that executives, managers, and anyone who directs or knowingly participates in union-busting can be held personally liable — not just the company they work for.",
    "LABR-UNNS-0013": "This position extends personal liability for unlawful anti-union conduct to executives, managers, HR personnel, outside consultants, and any other agents acting on an employer's behalf — protecting workers from the full chain of command.",
    "LABR-UNNS-0014": "This position prevents companies from hiding behind outside consultants or union-busting firms to escape responsibility — hiring a third party to do the dirty work does not shield anyone from liability.",
    "LABR-UNNS-0015": "This position identifies specific prohibited conduct: firing or punishing workers for organizing, threatening or coercing them, surveilling their activities, interfering with organizing efforts, and spreading lies to prevent workers from unionizing.",
    "LABR-UNNS-0016": "This position holds that individuals found personally responsible for union-busting can face civil fines, be ordered to pay restitution to harmed workers, and be liable for damages.",
    "LABR-UNNS-0017": "This position requires that civil penalties for labor violations be large enough to actually stop bad behavior — not fixed at amounts so low that large companies barely notice them.",
    "LABR-UNNS-0018": "This position holds that intentional, repeated, or especially egregious labor violations — including organized union-busting campaigns — can lead to criminal charges, not just civil fines.",
    "LABR-UNNS-0019": "This position holds that criminal liability for labor violations requires clear proof of intent or knowing disregard for workers' rights — reckless indifference to workers' legal rights also qualifies.",
    "LABR-UNNS-0020": "This position prohibits individuals from escaping personal responsibility for labor violations by hiding behind corporate structures, delegating illegal acts to subordinates, or exercising only indirect control over the unlawful conduct.",
    "LABR-UNNS-0021": "This position holds that individuals found responsible for serious labor violations can be barred from serving in executive, managerial, or fiduciary roles at companies going forward.",
    "LABR-UNNS-0022": "This position requires that fines for union-busting be large, scalable, and genuinely punishing — not small enough for companies to treat them as a routine cost of keeping unions out.",
    "LABR-UNNS-0023": "This position requires that penalties scale with the size of the violating company — including as a percentage of revenue, profit, or payroll — so that large employers cannot make fines disappear in their accounting.",
    "LABR-UNNS-0024": "This position prohibits large companies from receiving reduced effective penalties just because of their scale — fine structures must increase proportionally so that bigger companies face bigger real consequences.",
    "LABR-UNNS-0025": "This position holds that each separate act of retaliation, interference, or illegal conduct is its own violation — employers cannot lump multiple acts together to reduce the total penalty.",
    "LABR-UNNS-0026": "This position requires that ongoing, unresolved violations trigger daily or periodic escalating fines — the longer an employer refuses to comply, the more it costs.",
    "LABR-UNNS-0027": "This position holds that employers who repeatedly violate labor law face multiplied fines, increased oversight, and potential restrictions on their operations — not just the same penalty applied again and again.",
    "LABR-UNNS-0028": "This position holds that persistent refusal to comply with labor law can result in structural limits on a company — including restrictions on expanding, entering contracts, or participating in markets.",
    "LABR-UNNS-0029": "This position requires that workers harmed by union-busting receive full restitution — including their lost wages, benefits, damages, and the right to get their job back where applicable.",
    "LABR-UNNS-0030": "This position requires that remedies for union-busting address not just the direct financial harm to individual workers, but also the broader chilling effect that intimidation has on every worker who considered organizing.",
    "LABR-UNNS-0031": "This position holds that companies with a serious or repeated record of union-busting can be disqualified from receiving government contracts, subsidies, or tax incentives.",
    "LABR-UNNS-0032": "This position requires that labor violations and the penalties imposed for them be reported publicly in an accessible format — including tracking of repeat offenders — so the public can hold companies accountable.",
    "LABR-UNNS-0033": "This position prevents companies from using private settlements to escape accountability for systematic or repeated labor violations — any settlement must include real corrective actions that can be independently enforced.",
    "LABR-UNNS-0034": "This position requires Congress to enact card check union recognition: when a majority of workers sign verified authorization cards, the union is certified without a separate NLRB election. If a first contract is not reached within 120 days, binding arbitration kicks in automatically. Workers fired during an organizing campaign must be reinstated by court order within 30 days of a charge being filed.",
    "LABR-UNNS-0035": "This position requires Congress to ban captive audience meetings — employers may not force workers to attend meetings where the employer pushes anti-union views, and workers who decline cannot be penalized. If an employer communicates with workers about unionization, the union receives equal paid access to worker audiences of equal size and duration. Each violation carries a $10,000 fine, and workers or unions can sue directly.",
    "LABR-UNNS-0036": "This position requires Congress to reform the Taft-Hartley Act to allow secondary boycotts and solidarity strikes when the targeted company shares ownership, supply chain ties representing more than 20% of its revenue, or subcontracting relationships with the primary dispute employer. Restrictions on genuinely independent businesses with no supply chain connection to the dispute are preserved.",

    # CBAS — Collective Bargaining
    "LABR-CBAS-0001": "This position requires employers to bargain in good faith with a newly recognized union — they cannot stall indefinitely, delay negotiations, or refuse to work toward a real first contract.",
    "LABR-CBAS-0002": "This position holds that if an employer and union cannot reach a first contract within a defined period, there must be a formal mechanism — such as mediation or binding arbitration — to get workers a contract rather than leaving them in limbo.",
    "LABR-CBAS-0003": "This position supports creating industry-wide or sectoral bargaining systems that set minimum standards for entire sectors — so all workers in an industry benefit from collective bargaining, not just those whose specific employer was organized.",
    "LABR-CBAS-0004": "This position holds that industry-wide bargaining agreements can set the floor on wages, benefits, scheduling, safety, and working conditions across an entire sector — lifting standards for everyone.",
    "LABR-CBAS-0005": "This position requires that when bargaining takes place across a full industry, workers, employers, and voices representing the broader public all have meaningful seats at the table.",
    "LABR-CBAS-0006": "This position requires that collective bargaining cover the full range of issues that affect your job — including your paycheck, schedule, workplace conditions, surveillance practices, and job security.",
    "LABR-CBAS-0007": "This position gives workers the right to negotiate with their employer over the introduction of automation, new technology, and restructuring — so workers are not blindsided by changes that eliminate or transform their jobs.",
    "LABR-CBAS-0008": "This position requires that collective bargaining agreements be legally enforceable, with mechanisms for resolving disputes, going to arbitration, and monitoring whether both sides are living up to what they agreed to.",
    "LABR-CBAS-0009": "This position requires that when employers violate a collective bargaining agreement, workers receive meaningful remedies — including restitution and penalties — not just a symbolic acknowledgment that a rule was broken.",
    "LABR-CBAS-0010": "This position requires Congress to establish a federal Sectoral Bargaining Board with authority to set binding wage floors and working conditions for any industry employing more than 500,000 workers — raising the floor for entire sectors of the economy.",

    # PLTS — Platform Workers
    "LABR-PLTS-0001": "This position guarantees workers who are managed by apps, algorithms, or automated systems the right to collectively bargain over their pay, conditions, and how those systems govern their working lives.",
    "LABR-PLTS-0002": "This position prohibits platforms from using algorithmic control, lack of transparency about how decisions are made, or classification manipulation to prevent workers from organizing together.",
    "LABR-PLTS-0003": "This position gives workers the right to understand how the algorithms affecting their pay, scheduling, and access to work actually operate — and to have a meaningful voice in shaping those systems.",

    # AINL — AI in Labor
    "LABR-AINL-0001": "This position requires that AI systems used in employment preserve decision logs and scoring records in enough detail for workers to challenge decisions that affect them and for regulators to audit for violations.",
    "LABR-AINL-0002": "This position requires that any AI system affecting your hiring, pay, schedule, productivity review, discipline, or termination be independently audited and continuously monitored for bias, coercive patterns, and illegal labor practices.",
    "LABR-AINL-0003": "This position prohibits moving an AI tool from a helpful support function to one that makes binding employment decisions without strong legal safeguards, disclosure to affected workers, and independent oversight.",

    # AUTS — Automation
    "LABR-AUTS-0001": "This position requires employers to give workers meaningful advance notice, real consultation, and transition planning before making major automation or restructuring decisions that could eliminate or fundamentally change jobs.",
    "LABR-AUTS-0002": "This position guarantees workers and their union representatives the right to bargain over automation, AI deployment, deskilling, and changes in how productivity is measured — so technology serves workers rather than simply replacing them.",
    "LABR-AUTS-0003": "This position prohibits employers from using automation as a cover to escape labor standards, weaken union power, or force displaced workers to absorb all the costs of technological change on their own.",

    # BENS — Benefits
    "LABR-BENS-0001": "This position guarantees every worker reliable access to core benefits — healthcare, paid leave, retirement savings, unemployment protection, and disability protection — regardless of what type of job they have or how their employer is structured.",
    "LABR-BENS-0002": "This position prohibits structuring essential worker protections so that they depend entirely on keeping one specific job — that kind of dependency traps workers in bad situations rather than protecting them.",
    "LABR-BENS-0003": "This position requires that benefit systems be designed to follow workers through job changes, multiple jobs, temporary work, gig work, and employment gaps — not disappear every time your work situation changes.",
    "LABR-BENS-0004": "This position supports portable benefit systems that let workers build up vacation time, healthcare coverage, and retirement savings that travel with them from job to job or platform to platform.",
    "LABR-BENS-0005": "This position requires employers and platforms to contribute to portable benefit systems in proportion to the work performed and value extracted — the more they benefit from your labor, the more they must contribute.",
    "LABR-BENS-0006": "This position prohibits using portable benefit systems as a loophole to deny workers employee status — offering portable benefits does not justify misclassifying someone who should legally be an employee.",
    "LABR-BENS-0007": "This position requires that portable benefit systems be standardized, clearly explained, and genuinely easy for workers to understand and access — not buried in technical fine print.",
    "LABR-BENS-0008": "This position holds that your access to healthcare should not depend on keeping a particular job — losing or leaving work should not mean immediately losing health coverage.",
    "LABR-BENS-0009": "This position prohibits job transitions, layoffs, reduced hours, or platform deactivations from immediately cutting off essential health coverage — continuity protections must bridge the gap so workers are not left uninsured overnight.",
    "LABR-BENS-0010": "This position supports reducing workers' forced dependence on employer-tied healthcare by building toward universal systems, portable options, or other mechanisms that keep you covered regardless of your employment status.",

    # GIGS — Gig Workers
    "LABR-GIGS-0001": "This position guarantees full labor protections to workers who do their jobs through apps or digital platforms — regardless of what classification label the platform places on them.",
    "LABR-GIGS-0002": "This position requires that worker classification reflect the actual reality of the working relationship — how much control the employer has, how economically dependent you are — not just what a contract labels you.",
    "LABR-GIGS-0003": "This position requires that workers be classified as employees — with all the protections that status carries — when the platform controls their pricing, access to work, performance reviews, or working conditions.",
    "LABR-GIGS-0004": "This position permits independent contractor classification only when workers genuinely set their own prices, choose their own clients, control their own schedule, and determine how they do their work.",
    "LABR-GIGS-0005": "This position treats misclassification — labeling someone a contractor to avoid paying wages, benefits, or legal protections — as a serious violation with real penalties and restitution for the workers who were shortchanged.",
    "LABR-GIGS-0006": "This position requires that platform workers earn at least minimum wage after all of their actual time, out-of-pocket costs, and waiting periods are factored in — not just on the trips or tasks completed.",
    "LABR-GIGS-0007": "This position requires that pay calculations include all of your working time — including time waiting for an assignment, traveling to a pickup, or sitting idle because the platform paused work.",
    "LABR-GIGS-0008": "This position requires platforms and employers to reimburse workers for necessary work-related expenses like fuel, vehicle maintenance, equipment, and depreciation — workers should not be subsidizing their employer's business costs out of their own paycheck.",
    "LABR-GIGS-0009": "This position requires platforms to show you your expected pay, all fees, and any deductions in real time — before you accept a job — so you always know what you will actually be paid.",
    "LABR-GIGS-0010": "This position guarantees workers access to detailed earnings records and clear explanations of how their pay was calculated, so they can spot errors or shortchanging.",
    "LABR-GIGS-0011": "This position guarantees workers managed by algorithms the right to know how decisions affecting their pay, schedule, and access to work are actually being made — the algorithm cannot be a black box.",
    "LABR-GIGS-0012": "This position prohibits platforms from using algorithmic systems to impose hidden penalties, manipulate workers' behavior, or create conditions that feel coercive rather than genuinely free.",
    "LABR-GIGS-0013": "This position gives workers the right to contest, appeal, and demand a human review of any automated decision that affects their income — algorithms are not the last word on your livelihood.",
    "LABR-GIGS-0014": "This position prohibits platforms from cutting off or restricting a worker's access to income without a clear stated reason, meaningful advance notice, and a real opportunity to appeal.",
    "LABR-GIGS-0015": "This position requires that when an algorithm recommends deactivating a worker, a human being must review that decision and apply due process protections before it takes effect.",
    "LABR-GIGS-0016": "This position prohibits platforms from using psychological tricks — game-like rewards, artificial urgency, or hidden incentives — to pressure workers into unsafe, excessive, or unfair work patterns.",
    "LABR-GIGS-0017": "This position guarantees workers the ability to turn down a job or task without any further penalty beyond simply not getting paid for that particular opportunity.",
    "LABR-GIGS-0018": "This position guarantees gig and platform workers the right to form a union, organize, and bargain collectively — regardless of how the platform classifies them.",
    "LABR-GIGS-0019": "This position prohibits platforms from using classification systems to block workers from exercising their collective bargaining and organizing rights.",
    "LABR-GIGS-0020": "This position guarantees workers access to and control over the data a platform has collected about them — including ratings, performance metrics, and work history — so they understand how they're being evaluated.",
    "LABR-GIGS-0021": "This position gives workers the right to take their work history, ratings, and professional reputation with them when they move to a different platform, where technically feasible.",
    "LABR-GIGS-0022": "This position requires that platform rating systems be transparent, fair, and protected from arbitrary or biased use that could reduce a worker's income or access to assignments.",
    "LABR-GIGS-0023": "This position gives workers the right to challenge ratings that are inaccurate, made in bad faith, or are the product of discrimination.",
    "LABR-GIGS-0024": "This position requires that platform workers have access to healthcare, paid leave, and unemployment protections — through employer responsibility, portable benefit systems, or public programs — not just earnings with no safety net.",
    "LABR-GIGS-0025": "This position holds that benefit systems must be designed to follow workers across platforms and employment types — so benefits do not disappear when you switch apps or juggle multiple gig jobs.",
    "LABR-GIGS-0026": "This position prohibits platforms from manipulating work availability, worker visibility, or scheduling in ways that artificially limit your income or force you into dependent positions you did not freely choose.",
    "LABR-GIGS-0027": "This position prohibits platforms from restructuring, relabeling, or redesigning their systems specifically to escape labor protections or dodge enforcement.",
    "LABR-GIGS-0028": "This position requires that labor laws be enforced against gig platforms with the same seriousness as against traditional employers — including financial penalties, restitution, and structural remedies.",
    "LABR-GIGS-0029": "This position holds that platforms that repeatedly violate labor law can face restrictions on their operations, limits on market access, or structural intervention by regulators.",
    "LABR-GIGS-0030": "This position requires Congress to make the ABC test the only federal legal standard for classifying workers — workers are presumed to be employees unless the employer proves all three prongs of the test — and treats any failure to meet that standard as an automatic wage law violation carrying civil penalties for each affected worker.",
    "LABR-GIGS-0031": "This position requires gig platforms with more than 1,000 active workers to contribute at least 8% of each worker's gross earnings to healthcare coverage, 3% to retirement savings, and 2% to paid leave — in a worker-directed portable benefits account — regardless of how workers are classified. Contributions must be made within 30 days of each earning period, and disputes over classification do not suspend the obligation.",

    # GOVN — Governance
    "LABR-GOVN-0001": "This position holds that when major business decisions about pay, safety, scheduling, automation, or job security directly affect workers' lives, workers should have a meaningful voice in how those decisions are made — not just receive notice after the fact.",
    "LABR-GOVN-0002": "This position holds that large companies may be required by law to include worker representatives on their boards or governing bodies — giving the people who do the work real input into decisions that shape their working lives.",
    "LABR-GOVN-0003": "This position requires that worker governance mechanisms provide genuine influence over corporate decisions — not symbolic consultation that management can ignore without consequence.",

    # OWNS — Ownership
    "LABR-OWNS-0001": "This position supports policies that encourage worker ownership of businesses, employee-run cooperatives, worker equity stakes, and shared governance models — so the people doing the work can also share in owning and running the enterprise.",
    "LABR-OWNS-0002": "This position requires governments to actively support the creation and growth of worker cooperatives and employee-owned firms — through financing, technical assistance, and legal structures — rather than simply allowing them to exist without support.",
    "LABR-OWNS-0003": "This position gives workers a real pathway to take over ownership of a business when it is being sold, closed, or transferred — especially when a closure would devastate the surrounding community.",
    "LABR-OWNS-0004": "This position holds that workers should share in the gains from higher productivity, automation, and long-term company success — through profit sharing, gain sharing, equity, or similar mechanisms — not just watch those gains flow upward to executives and shareholders.",
    "LABR-OWNS-0005": "This position prohibits compensation systems that funnel almost all productivity gains to executives and capital holders while leaving workers with stagnant wages and growing economic insecurity.",
    "LABR-OWNS-0006": "This position permits government contracts, tax benefits, or public incentives to be made conditional on companies adopting broad-based worker profit sharing or ownership participation programs.",

    # RETS — Retirement
    "LABR-RETS-0001": "This position guarantees workers access to retirement savings systems that are portable, clearly explained, and do not require continuous employment with a single employer to build up — so changing jobs does not mean starting over.",
    "LABR-RETS-0002": "This position requires retirement systems to work for workers with uneven career paths — including people who changed jobs often, worked multiple part-time gigs, took time off to care for family, or did platform-based work.",

    # WRKS — Work Structure
    "LABR-WRKS-0001": "This position calls for establishing a standard 4-day, 32-hour work week without any reduction in pay — so workers get more time for their health, family, and lives without losing income.",
    "LABR-WRKS-0002": "This position holds that when AI and automation make workers more productive, those gains should translate into shorter working hours for workers — not a heavier workload imposed on the same number of people for the same pay.",
    "LABR-WRKS-0003": "This position guarantees overtime pay protections for all workers — including salaried employees — above defined hour or salary thresholds, with appropriate safeguards to prevent employers from reclassifying workers to dodge these rules.",

    # NCPS — Non-Competes
    "LABR-NCPS-0001": "This position bans or strictly limits non-compete agreements for workers below the senior executive level — an estimated 30 million workers are currently subject to these agreements, which suppress wages and trap people in jobs without any legitimate competitive justification.",
    "LABR-NCPS-0002": "This position holds that no-poach agreements between employers and non-solicitation clauses must face the same strict scrutiny as non-competes — employers may not use these tools to achieve through the back door what is prohibited through the front.",
    "LABR-NCPS-0003": "This position gives workers whose job prospects or wages were suppressed by unlawful non-compete, no-poach, or mobility-restriction agreements the right to sue and recover damages, with legal fees paid by the employer who violated the law.",
    "LABR-NCPS-0004": "This position requires Congress to pass a federal law banning non-compete agreements — replacing an FTC rule that was struck down in court — with treble damages and attorney fees paid by any employer who attempts to enforce one against a worker.",
    "LABR-NCPS-0005": "This position requires treating wage-fixing deals and no-poach agreements between competing employers as automatic violations of antitrust law under the Sherman Act — subject to criminal prosecution and a direct private right of action for affected workers.",

    # DOMS — Domestic Workers
    "LABR-DOMS-0001": "This position requires that domestic workers — including nannies, housekeepers, home health aides, and household employees — receive full coverage under federal labor law, closing exclusions that have historically left these workers, predominantly women of color, without legal protections.",
    "LABR-DOMS-0002": "This position requires that domestic workers receive written employment agreements, enforceable rest and overtime rights, and full protection from retaliation when they assert their legal rights on the job.",
    "LABR-DOMS-0003": "This position requires that home care workers and personal care assistants be covered by workers' compensation, unemployment insurance, and Social Security on the same terms as any other worker — regardless of whether their employer is a private household or a government program.",
    "LABR-DOMS-0004": "This position requires Congress to extend full collective bargaining and overtime protections to agricultural workers under the NLRA and FLSA — removing exclusions that were originally written into law as part of a Jim Crow-era racial compromise with Southern legislators.",

    # PRLS — Prison Labor
    "LABR-PRLS-0001": "This position holds that incarcerated people may not be forced to work without pay that bears a real relationship to the value of their labor — the 13th Amendment's punishment exception cannot be used to authorize unpaid or near-zero-pay forced work that enriches private companies.",
    "LABR-PRLS-0002": "This position requires that when incarcerated workers do work for private corporations — through labor contracts, work release, or similar programs — they must be paid the prevailing wage for equivalent work outside prison walls.",
    "LABR-PRLS-0003": "This position requires larger corporations to audit their entire supply chain for forced labor, prison labor, and coerced work at every tier — and to publicly report what they find, with timelines for remediation.",

    # CLMS — Climate/Heat Safety
    "LABR-CLMS-0001": "This position guarantees every worker an enforceable right to protection from dangerous heat — including mandatory rest breaks, free access to cool water and shade, acclimatization protocols for new workers, and emergency response plans when temperatures reach dangerous levels.",
    "LABR-CLMS-0002": "This position requires additional, category-specific heat protections for outdoor workers in agriculture, construction, landscaping, and delivery, and for indoor workers in non-climate-controlled facilities such as warehouses and fulfillment centers.",
    "LABR-CLMS-0003": "This position protects workers who reasonably refuse to work in conditions presenting an imminent heat danger from being fired, disciplined, or penalized — consistent with workers' existing rights under OSHA.",
    "LABR-CLMS-0004": "This position requires OSHA to publish a binding federal heat illness prevention standard within one year, covering all industries. At 80°F indoors or 90°F outdoors, employers must provide free water, shade, and mandatory rest breaks every two hours. At 95°F indoors or 103°F outdoors, non-emergency work must stop. New workers must follow an acclimatization schedule, and supervisors must be trained annually in recognizing and responding to heat illness.",

    # SCHS — Scheduling
    "LABR-SCHS-0001": "This position requires employers in retail, food service, and hospitality to post workers' schedules at least 14 days in advance — giving workers enough time to arrange childcare, transportation, and second jobs around their shifts.",
    "LABR-SCHS-0002": "This position requires employers to pay workers premium compensation when they make last-minute changes to a posted schedule — including cancellations and alterations — to compensate workers for the disruption those changes cause to their lives.",
    "LABR-SCHS-0003": "This position gives workers the right to request schedule changes — like predictable hours, accommodations for caregiving, or avoiding split shifts — without facing retaliation or having hours cut in response to the request.",
    "LABR-SCHS-0004": "This position requires Congress to enact a federal predictive scheduling law for retail, food service, and healthcare employers with 50 or more employees. Schedules must be posted 14 days in advance; any change within 72 hours triggers 1.5x pay for affected shifts. Employers must offer extra hours to current qualified workers before hiring new staff. Workers can request schedule changes without retaliation, and all records must be kept for three years.",

    # PBNS — Portable Benefits
    "LABR-PBNS-0001": "This position requires that workplace benefits — including paid leave, retirement savings, healthcare contributions, and training credits — travel with you as you move between employers, platforms, and types of work, so you never have to start over from zero.",
    "LABR-PBNS-0002": "This position requires businesses and platforms that rely heavily on independent contractors for core functions to make proportional contributions to portable benefit funds on those contractors' behalf — regardless of how those workers are classified.",
    "LABR-PBNS-0003": "This position requires paid leave and retirement savings systems to be redesigned so that workers holding multiple part-time jobs can accumulate benefits across all of them — not be penalized compared to someone with a single full-time employer.",
    "LABR-PBNS-0004": "This position requires Congress to create a federal Portable Benefits Trust: every worker gets a portable account funded by mandatory employer and platform contributions of at least 8% of gross earnings for healthcare, 3% for retirement, and 2% for paid leave — with no minimum hours and no waiting period. Accounts follow workers across all jobs and platforms, and employers may not cut pay to offset their contribution obligations.",

    # CRCS — Child Care
    "LABR-CRCS-0001": "This position requires the federal government to treat affordable child care as essential public infrastructure — like roads or schools — recognizing that the current cost and scarcity of child care is a structural barrier to equal workforce participation that falls disproportionately on working mothers and low-income families.",
    "LABR-CRCS-0002": "This position requires larger employers to provide child care benefits — through on-site facilities, subsidized third-party care, or portable child care savings contributions — for workers with young children. Smaller employers receive government support to meet equivalent standards without being placed at a competitive disadvantage.",
    "LABR-CRCS-0003": "This position requires that child care workers be paid wages and receive benefits comparable to similarly credentialed public school teachers — reflecting the equal developmental importance of early childhood care — and that compensation cannot depend on what families can afford to pay.",

    # LABS — Parental Leave / Small Business
    "LABR-LABS-0001": "This position requires the government to subsidize or support paid parental leave for small businesses, so that workers at smaller employers can take paid leave when a child is born or adopted — the same as workers at large corporations.",

    # JCAU — Just Cause
    "LABR-JCAU-0001": "This position requires Congress to establish a federal just-cause termination standard: after six months on the job, employers may only fire you for a legitimate, documented reason — replacing the current 'at-will' system that allows termination for any reason or no reason at all.",

    # FARM — Farmworkers
    "LABR-FARM-0001": "This position requires Congress to extend full NLRA and FLSA protections — including the right to organize, minimum wage, and overtime — to farmworkers, repealing exclusions that have no justification other than their origins in racially discriminatory New Deal-era political compromises.",
    "LABR-FARM-0002": "This position requires Congress to reform the H-2A agricultural guest worker program so that workers can change jobs freely — ending the current system that ties visa status to a single employer, giving that employer near-total control over a worker's ability to stay in the country.",
    "LABR-FARM-0003": "This position requires OSHA to issue and enforce mandatory federal heat illness prevention and pesticide safety standards that apply to all agricultural workers — the same baseline protections that workers in other industries are entitled to.",

    # TRCK — Truckers
    "LABR-TRCK-0001": "This position requires Congress to ban predatory lease-to-own truck contracts that leave drivers earning below 150% of minimum wage after all expenses. Carriers must issue weekly itemized earnings statements, and any driver using a carrier vehicle and working primarily for one carrier is presumed to be an employee. Criminal penalties of up to $100,000 per driver per year and five years imprisonment apply to carrier executives who knowingly design contracts to produce sub-minimum wages.",
    "LABR-TRCK-0002": "This position requires Congress to cap truck driving to 10 hours per day with a mandatory 10-hour rest period, require full hourly pay for dock and terminal waiting time beyond one hour, establish a federal minimum per-mile rate ensuring at least $25 per hour in net earnings adjusted annually for inflation, and create a public database of carriers with wage and safety violations. Criminal penalties apply for falsifying electronic logging data.",

    # GIIG — Gig (Additional)
    "LABR-GIIG-0001": "This position requires making the ABC test the federal standard for worker classification — workers are presumed employees unless the hiring entity can affirmatively prove all three prongs of the test — applying to all federal and state labor law.",
    "LABR-GIIG-0002": "This position requires any entity that engages a worker for more than 100 hours in a year to contribute at least 15% of that worker's wages to a portable benefits account owned by the worker — regardless of how the worker is classified.",
    "LABR-GIIG-0003": "This position gives workers managed by algorithms the right to a plain-language explanation of any adverse automated decision, at least 72 hours of advance notice before adverse action takes effect, and the right to demand human review and appeal within that window.",
    "LABR-GIIG-0004": "This position guarantees app-based and gig workers the full right to collectively organize and bargain — and prohibits using antitrust law as a weapon to prevent gig workers from acting together to improve their pay and conditions.",

    # SAFE — Safety (Additional)
    "LABR-SAFE-0001": "This position requires OSHA to promulgate a binding federal heat illness prevention standard covering all outdoor and indoor workers — so every employer is required by law to protect workers from dangerous heat, not just those in states with their own rules.",
    "LABR-SAFE-0002": "This position requires OSHA to issue an ergonomics standard to prevent musculoskeletal injuries — like repetitive strain, back injuries, and joint damage — in high-risk industries such as warehousing, meatpacking, poultry processing, and construction.",
    "LABR-SAFE-0003": "This position protects workers who report workplace safety violations from retaliation, and requires that any worker fired, disciplined, or demoted for reporting a safety concern be reinstated within 30 days with full back pay.",
    "LABR-SAFE-0004": "This position prohibits employers from using safety incentive programs that discourage workers from reporting injuries — like bonuses tied to 'zero incident' records — and requires employers to publish their workplace injury and illness data publicly so everyone can see their actual safety record.",

    # PUBL — Public Sector
    "LABR-PUBL-0001": "This position guarantees federal employees the full right to collectively bargain over all terms and conditions of their employment — wages, hours, benefits, staffing levels, and working conditions — removing current statutory exclusions of these subjects from bargaining.",
    "LABR-PUBL-0002": "This position replaces the blanket ban on federal employee strikes with a carefully designed framework that permits strikes except in functions that are genuinely critical to national security — ensuring that federal workers have real bargaining power, not just the right to negotiate without leverage.",
    "LABR-PUBL-0003": "This position requires the United States Postal Service to be fully funded with its services restored, and establishes postal banking so that post offices can provide basic financial services to the tens of millions of Americans who lack access to a bank.",
    "LABR-PUBL-0004": "This position requires federal protection for state and local government workers in states that currently prohibit public sector collective bargaining — so that the state you happen to live in cannot strip you of rights that workers in other states have.",

    # GIGW — Gig Workers (Detailed)
    "LABR-GIGW-0001": "This position requires Congress to enact a federal ABC test making workers presumptive employees unless all three prongs are proven, applying to minimum wage, overtime, unemployment, workers' comp, and organizing rights. Misclassification carries civil penalties of $5,000 to $25,000 per worker per year, criminal penalties for willful violations, and the NLRB must have jurisdiction over organizing activity by all app-based workers.",
    "LABR-GIGW-0002": "This position requires Congress to direct the DOL to set minimum earnings standards for rideshare and delivery workers, guaranteeing the greater of $1.28 per mile on a trip or 120% of the local minimum wage for all time logged in and available. Platforms must reimburse the full IRS mileage rate and provide weekly itemized earnings statements. Criminal liability applies to platform executives who knowingly pay workers below the minimum.",
    "LABR-GIGW-0003": "This position requires that 100% of any tip paid through a digital platform go directly to the worker — platforms and employers may not keep any portion, charge processing fees against tips, or reduce base pay in response to tips received. Platforms must disclose to customers exactly what percentage of their tip reaches the worker, and tip manipulation by algorithm is a per se unfair business practice under federal law.",
    "LABR-GIGW-0004": "This position requires Congress to extend full collective bargaining rights to all app-based workers regardless of classification, including the rights to strike, form associations, and negotiate over earnings and algorithm transparency. Any adverse algorithmic action within 90 days of protected union activity is presumptively retaliatory. Platforms with more than 10,000 workers must establish an elected Gig Worker Advisory Board with real negotiating authority.",

    # VETS — Veterans
    "LABR-VETS-0001": "This position requires Congress to strengthen USERRA with criminal penalties — up to $100,000 in fines and three years imprisonment — for employers who willfully violate veterans' reemployment rights. Veterans get a direct right to sue in federal court without first filing an administrative complaint. Employers with 50 or more workers must designate a Military Liaison Officer, and military leave may not count against performance metrics or attendance records.",
    "LABR-VETS-0002": "This position requires Congress to reform the military Transition Assistance Program so that it begins 18 months before separation, is mandatory, and includes individualized career counseling, military-to-civilian skills translation, licensing and certification support, entrepreneurship training, and financial literacy. The Defense Department must track and publish post-separation employment outcomes by branch and demographic to continuously improve the program.",
    "LABR-VETS-0003": "This position requires Congress to expand hiring preferences for military spouses across all federal agencies including remote positions, enact a federal license portability law granting military spouses a 12-month temporary license in any state within 30 days of a PCS move, require federal contractors with 100 or more employees to offer remote work during relocations, and establish a $100 million annual Military Spouse Entrepreneurship Fund.",
    "LABR-VETS-0004": "This position requires Congress to increase the federal contracting goal for veteran-owned and service-disabled veteran-owned small businesses to 30% of all prime and subcontract dollars — up from the current 3% goal — with annual agency scorecards, a Veteran Mentor-Protégé Program, and a $500 million Veteran Entrepreneurship Capital Fund to support veteran-owned businesses that cannot access traditional bank financing.",

    # UNON — Unions (Detailed)
    "LABR-UNON-0001": "This position requires Congress to enact the PRO Act in full — mandating card check recognition, 10-day NLRB elections, binding first contract arbitration within 90 days, a ban on captive audience meetings, a ban on permanently replacing striking workers, personal criminal liability for executives who commit labor violations, and a private right of action for harmed workers with doubled damages for willful retaliation.",
    "LABR-UNON-0002": "This position requires Congress to close the loophole that lets employers secretly pay union-busting consultants, require all anti-union firms to register with the DOL in a public database, ban specific union-busting tactics including one-on-one supervisor pressure and worker surveillance, and grant unions equal communication access whenever employers communicate with workers about organizing. Criminal penalties of up to $1 million and five years imprisonment apply for threatening or surveilling workers for union activity.",
    "LABR-UNON-0003": "This position requires Congress to create a Federal Sectoral Bargaining System with Industry Standards Boards for at least 10 major low-wage sectors — including retail, food service, home care, warehousing, domestic work, and agriculture. Each board includes equal worker, employer, and public interest representation with binding authority to set sector-wide wages, maximum hours, minimum leave, safety standards, and scheduling rules that apply to every employer in the sector, with automatic $5,000 per worker per week penalties for noncompliance.",
    "LABR-UNON-0004": "This position requires Congress to amend the Federal Service Labor-Management Relations Statute to give all federal employees the right to bargain collectively over wages, hours, benefits, staffing levels, and all working conditions. It prohibits any President or agency head from unilaterally voiding a collective bargaining agreement without formal congressional approval, and grants federal unions the right to strike on non-safety issues after exhausting mediation and arbitration.",

    # GINC — Guaranteed Income
    "LABR-GINC-0001": "This position requires Congress to establish a federal Guaranteed Income program paying $1,000 per month to every adult whose household income is below 200% of the federal poverty level. Payments are delivered monthly, adjusted annually for inflation, and funded through program consolidation, a 0.05% financial transaction tax, and a carbon dividend. Employers, landlords, and lenders may not use receipt of guaranteed income as grounds to deny a job, housing, or credit.",

    # GIGS-0032 through 0034 (additional gig cards)
    "LABR-GIGS-0032": "This position requires Congress to enact a federal ABC test establishing a legal presumption that any worker is an employee unless the hiring entity proves all three prongs. The standard supersedes any weaker state law, applies to all federal and state labor laws, and prohibits platforms from conditioning work access on waiving classification rights. Platforms with revenue above $100 million must provide all workers a minimum earnings floor of 120% of minimum wage after expenses, transparent pay calculations, and advance notice of pay rate changes.",
    "LABR-GIGS-0033": "This position requires Congress to create a Federal Portable Benefits Fund requiring gig platforms with more than 100 workers to contribute 15% of each worker's earnings to portable benefit accounts covering health insurance, paid sick leave, paid family leave, retirement savings, and workers' compensation. Accounts are fully transferable between platforms, and platforms may not reduce base pay to offset contribution obligations.",
    "LABR-GIGS-0034": "This position requires Congress to enact the Platform Worker Algorithmic Accountability Act, requiring large gig platforms to explain how work is assigned and pay is calculated, publish annual algorithmic transparency reports, and conduct annual disparate impact audits by race, sex, and age. Any adverse action within six months of a labor complaint or protected activity is presumptively retaliatory. Platforms must give workers 14 days' notice and an appeal opportunity before deactivation.",

    # WGTH — Wage Theft
    "LABR-WGTH-0001": "This position requires Congress to criminalize systematic wage theft — any employer who knowingly shortchanges 10 or more employees faces federal felony charges with up to $1 million in fines and 10 years imprisonment for responsible officers. A joint DOL-DOJ Federal Wage Theft Enforcement Unit is established with a public tip line. A public Federal Wage Theft Registry bars listed employers from government contracts. Victims have a private right of action for all unpaid wages plus triple damages and attorney fees.",
    "LABR-WGTH-0002": "This position requires Congress to ban pre-dispute mandatory arbitration in all employment contracts for wage, discrimination, harassment, and safety claims — restoring workers' right to go to court and join class actions. Employers may not condition a job or promotion on signing an arbitration agreement, existing such provisions are voided for unresolved claims, and all employment arbitration awards must be published publicly.",

    # TIPD — Tips
    "LABR-TIPD-0001": "This position requires Congress to phase out the federal tipped minimum wage — currently $2.13 per hour — over three years, so all workers including tipped employees receive the full minimum wage before any tips are counted. Tips belong entirely to the worker; employers may not use tips to offset their wage obligation, retain any portion, or include managers in tip pools. All tip income must be tracked through certified payroll systems to protect workers' future Social Security and Medicare benefits.",

    # WRHS — Warehouse Workers
    "LABR-WRHS-0001": "This position requires Congress to enact the Warehouse Worker Protection Act — prohibiting any automated productivity monitoring system that generates disciplinary actions without human review, tracks workers during bathroom breaks, or sets quotas certified by a qualified ergonomist to exceed safe physical limits. Employers must provide each worker a written disclosure — in their primary language — of every monitoring system in use, every metric measured, and exactly how those metrics affect employment decisions.",
}


def main() -> None:
    html_path = Path("docs/pillars/labor-and-workers-rights.html")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")

    updated = 0
    missing_in_dict = []
    already_filled = 0

    for card in soup.find_all("div", class_="policy-card"):
        card_id = card.get("id", "")
        plain_p = card.find("p", class_="rule-plain")

        if plain_p is not None:
            existing_text = plain_p.get_text(strip=True)
            if existing_text:
                already_filled += 1
                continue
            # Empty tag already present — fill it
            if card_id in PLAIN_LANGUAGE:
                plain_p.string = PLAIN_LANGUAGE[card_id]
                updated += 1
            else:
                missing_in_dict.append(card_id)
            continue

        # No rule-plain tag at all — insert one after rule-title
        if card_id not in PLAIN_LANGUAGE:
            missing_in_dict.append(card_id)
            continue

        title_p = card.find("p", class_="rule-title")
        if title_p is None:
            missing_in_dict.append(card_id)
            continue

        new_p = soup.new_tag("p", attrs={"class": "rule-plain"})
        new_p.string = PLAIN_LANGUAGE[card_id]
        title_p.insert_after(new_p)
        updated += 1

    html_path.write_text(str(soup), encoding="utf-8")

    print(f"Updated:        {updated} cards")
    print(f"Already filled: {already_filled} cards")
    if missing_in_dict:
        print(f"Missing from PLAIN_LANGUAGE dict ({len(missing_in_dict)}):")
        for mid in missing_in_dict:
            print(f"  {mid}")


if __name__ == "__main__":
    main()
