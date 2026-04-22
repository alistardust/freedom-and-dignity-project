/* American Renewal Project — site data */
const ARP = {
  foundations: [
    {
      id: 'accountable-power',
      num: 'I', title: 'Accountable Power',
      color: '#bf0a30',
      belief: 'Power exists to serve people. When it doesn\'t answer to the people, it stops being power and starts being abuse.',
      value: 'The right to be governed by those who answer to you, not to their donors.',
      why: 'The promise of democracy has been hollowed out by money in politics, courts captured by ideology, and an executive branch that has learned to govern by fiat. Accountability is not a procedural nicety—it is the bedrock of consent.',
      demands: ['Term limits and fitness standards for every federal office', 'Campaign finance reform that ends the donor class\'s veto over legislation', 'Courts that apply the law, not an agenda', 'An executive constrained by law, not just norms'],
      rejects: ['The idea that money is speech', 'Lifetime tenure without accountability', 'Executive power that expands in darkness'],
      pillars: ['executive_power', 'checks_and_balances', 'term_limits_and_fitness', 'courts_and_judicial_system', 'administrative_state', 'legislative_reform']
    },
    {
      id: 'clean-democracy',
      num: 'II', title: 'Clean Democracy',
      color: '#2471a3',
      belief: 'Your vote must mean what it says. One person, one vote—not one dollar, one vote.',
      value: 'The right to elections that are free, fair, and free of manipulation.',
      why: 'Gerrymandering, voter suppression, dark money, and media monopolies have turned democracy into a performance. Cleaning it up is not a partisan cause—it is the prerequisite for every other cause.',
      demands: ['Independent redistricting for every state', 'Automatic voter registration', 'Antitrust enforcement that breaks up media monopolies', 'Full disclosure of political spending'],
      rejects: ['Rigged maps drawn to protect incumbents', 'Corporate capture of media and information', 'Concentration of ownership in any industry vital to democracy'],
      pillars: ['elections_and_representation', 'anti_corruption', 'antitrust_and_corporate_power', 'information_and_media']
    },
    {
      id: 'equal-justice',
      num: 'III', title: 'Equal Justice',
      color: '#1e8449',
      belief: 'Justice that bends for the powerful isn\'t justice. It\'s a protection racket.',
      value: 'The right to be treated equally under the law regardless of race, origin, income, or status.',
      why: 'We have never fully delivered on the promise written in our founding documents. Equal justice is unfinished business—not a gift to be granted, but a debt long overdue.',
      demands: ['Police accountability with teeth, not just policies', 'An immigration system built on dignity and due process', 'Civil rights enforcement that matches the scale of the problem'],
      rejects: ['Two systems of justice—one for the powerful, one for everyone else', 'Dehumanization of immigrants', 'Civil rights as an aspiration rather than a guarantee'],
      pillars: ['equal_justice_and_policing', 'immigration', 'rights_and_civil_liberties']
    },
    {
      id: 'real-freedom',
      num: 'IV', title: 'Real Freedom',
      color: '#7d3c98',
      belief: 'Freedom isn\'t just the absence of government interference. It\'s the presence of real choices.',
      value: 'The right to live your life free from surveillance, coercion, and the tyranny of concentrated power—public or private.',
      why: 'The old freedom debate is over. The threats to freedom today come not just from government but from corporations with unprecedented power to monitor, manipulate, and control. Real freedom requires confronting both.',
      demands: ['Constitutional protection against corporate surveillance', 'Algorithmic accountability for platforms that shape public life', 'Sensible gun policy grounded in public safety and the actual text of the Second Amendment'],
      rejects: ['The surveillance economy as the price of modernity', 'Platforms that amplify hate and call it free speech', 'Weapons of war in civilian hands'],
      pillars: ['rights_and_civil_liberties', 'gun_policy', 'technology_and_ai', 'consumer_rights']
    },
    {
      id: 'freedom-to-thrive',
      num: 'V', title: 'Freedom to Thrive',
      color: '#c9952a',
      belief: 'You can\'t be free if you\'re sick, homeless, or in debt.',
      value: 'The right to healthcare, housing, a living wage, clean air, clean water, and an economy that works for you—not just for the people at the top.',
      why: 'FDR called it the Second Bill of Rights. We are completing that work for the 21st century. Economic security is not charity. It is the foundation on which every other freedom rests.',
      demands: ['Universal healthcare as a right, not a commodity', 'Housing as a human necessity, not a speculative asset', 'Clean water and clean air as constitutional rights — not regulatory privileges subject to rollback', 'A tax system that rewards work over wealth', 'A livable planet for the next generation', 'Water conservation, infrastructure, and equitable access as national priorities'],
      rejects: ['Healthcare tied to employment', 'A housing market that treats homes as investment vehicles', 'An economy that socializes losses and privatizes gains', 'Privatization of water systems that communities depend on for survival'],
      pillars: ['healthcare', 'taxation_and_wealth', 'environment_and_agriculture', 'infrastructure_and_public_goods', 'education', 'labor_and_workers_rights', 'housing']
    }
  ],

  pillars: [
    { id: 'executive_power',               title: 'Executive Power',               foundation: 'accountable-power',  summary: 'The presidency must be accountable to law and to Congress, not just to norms and custom.',                                      points: ['Restore congressional war powers', 'Enforce separation of powers through the courts', 'Require transparency in executive action'] },
    { id: 'checks_and_balances',           title: 'Checks & Balances',             foundation: 'accountable-power',  summary: 'The system of institutional limits on power must be rebuilt to withstand authoritarian pressure.',                          points: ['Legislative independence from executive coercion', 'Inspector general protections', 'Contempt of Congress with real consequences'] },
    { id: 'term_limits_and_fitness',       title: 'Term Limits & Fitness',         foundation: 'accountable-power',  summary: 'Elected and appointed officials must be term-limited and meet basic fitness requirements.',                                points: ['Congressional term limits', 'Cognitive and fitness assessments for federal office', 'Mandatory retirement for federal judges'] },
    { id: 'courts_and_judicial_system',    title: 'Courts & Judicial System',      foundation: 'accountable-power',  summary: 'Federal courts must reflect the diversity of the nation and apply the law without ideological capture.',                     points: ['Supreme Court reform and expansion', 'Ethics enforcement for federal judges', 'Transparent confirmation standards'] },
    { id: 'administrative_state',          title: 'Administrative State',          foundation: 'accountable-power',  summary: 'Federal agencies serve the public, not the industries they are supposed to regulate.',                                     points: ['Revolving door restrictions', 'Agency independence from political interference', 'Rulemaking transparency and accountability'] },
    { id: 'elections_and_representation',  title: 'Elections & Representation',    foundation: 'clean-democracy',    summary: 'Every eligible voter must be able to vote, every vote must count, and every district must be fairly drawn.',                points: ['Automatic voter registration', 'Independent redistricting', 'Ranked choice voting'] },
    { id: 'anti_corruption',              title: 'Anti-Corruption',               foundation: 'clean-democracy',    summary: 'Public office must not be a path to private enrichment.',                                                                  points: ['Disclosure of all political spending', 'Congressional stock trading ban', 'Post-government employment restrictions'] },
    { id: 'antitrust_and_corporate_power', title: 'Antitrust & Corporate Power',   foundation: 'clean-democracy',    summary: 'Monopoly power corrupts markets and democracy alike. It must be broken up.',                                               points: ['Aggressive antitrust enforcement', 'Breaking up media monopolies', 'Labor market concentration rules'] },
    { id: 'information_and_media',         title: 'Information & Media',           foundation: 'clean-democracy',    summary: 'A functioning democracy requires a free, diverse, and trustworthy press.',                                                  points: ['Local news funding', 'Platform transparency requirements', 'Algorithmic accountability'] },
    { id: 'equal_justice_and_policing',    title: 'Equal Justice & Policing',      foundation: 'equal-justice',      summary: 'The law must apply equally. Policing must protect communities, not prey on them.',                                          points: ['National use-of-force standards', 'Civilian oversight with real authority', 'End of qualified immunity'] },
    { id: 'immigration',                   title: 'Immigration',                   foundation: 'equal-justice',      summary: 'Immigration policy must be grounded in dignity, due process, and the reality of who built this country.',                  points: ['Clear path to citizenship', 'Due process in deportation proceedings', 'Family unity as a core principle'] },
    { id: 'rights_and_civil_liberties',    title: 'Rights & Civil Liberties',      foundation: 'equal-justice',      summary: 'Civil rights enforcement must match the scale and sophistication of modern discrimination.',                               points: ['Strengthen the Voting Rights Act', 'LGBTQ+ non-discrimination protections', 'Disability rights enforcement'] },
    { id: 'gun_policy',                    title: 'Gun Policy',                    foundation: 'real-freedom',       summary: 'Public safety and the Second Amendment are not in conflict. Sensible policy honors both.',                                  points: ['Universal background checks', 'Red flag laws', 'Assault weapons and high-capacity magazine restrictions'] },
    { id: 'technology_and_ai',             title: 'Technology & AI',               foundation: 'real-freedom',       summary: 'Technology must serve people. Surveillance capitalism and unaccountable AI are threats to freedom.',                       points: ['Federal data privacy law', 'AI accountability framework', 'Antitrust action against Big Tech'] },
    { id: 'healthcare',                    title: 'Healthcare',                    foundation: 'freedom-to-thrive',  summary: 'Healthcare is a right. No one should go bankrupt, go without, or die because they couldn\'t afford care.',                  points: ['Universal coverage', 'Drug price negotiation', 'Mental health parity'] },
    { id: 'taxation_and_wealth',           title: 'Taxation & Wealth',             foundation: 'freedom-to-thrive',  summary: 'The tax system must reward work, not inheritance. Extreme concentration of wealth is incompatible with democracy.',        points: ['Wealth tax on extreme fortunes', 'Capital gains taxed as ordinary income', 'End of stepped-up basis loophole'] },
    { id: 'environment_and_agriculture',   title: 'Environment & Agriculture',     foundation: 'freedom-to-thrive',  summary: 'A livable planet and a food supply that is clean, safe, and fairly produced are non-negotiable.',                          points: ['Carbon pricing and clean energy transition', 'Family farm protections', 'Clean water enforcement'] },
    { id: 'infrastructure_and_public_goods', title: 'Infrastructure & Public Goods', foundation: 'freedom-to-thrive', summary: 'The electrical grid, internet, water systems, and transportation must serve everyone — not be monopolized or left to decay.', points: ['Modernize the electrical grid for clean energy', 'Internet as public infrastructure with universal rural access', 'Carbon-neutral construction standards and clean transportation transition'] },
    { id: 'education',                     title: 'Education',                     foundation: 'freedom-to-thrive',  summary: 'Every person deserves access to a high-quality education regardless of wealth, zip code, or background.',               points: ['Equitable school funding', 'Student debt relief and affordable higher education', 'Universal pre-K and school-based support'] },
    { id: 'labor_and_workers_rights',      title: 'Labor & Workers\' Rights',      foundation: 'freedom-to-thrive',  summary: 'Workers have the right to organize, bargain collectively, and share in the productivity they create.',                    points: ['Strengthen collective bargaining rights', 'Federal minimum wage and overtime reform', 'End worker misclassification and wage theft'] },
    { id: 'housing',                       title: 'Housing',                       foundation: 'freedom-to-thrive',  summary: 'Housing is a human necessity. No one should be priced out of stability by speculation or policy failure.',                 points: ['Anti-speculation controls and vacancy taxes', 'Community land trust investment', 'Tenant protections and anti-eviction standards'] },
    { id: 'consumer_rights',               title: 'Consumer Rights',               foundation: 'real-freedom',       summary: 'Corporations cannot be allowed to strip consumers of rights through contracts, monopoly, or engineered dependency.',        points: ['Right-to-repair legislation', 'Ban mandatory arbitration clauses', 'Data exploitation and dark pattern protections'] },
    { id: 'legislative_reform',            title: 'Legislative Reform',            foundation: 'accountable-power',  summary: 'Congress must be able to legislate. Structural dysfunction serves concentrated power and no one else.',                    points: ['Filibuster reform to restore majority governance', 'Senate representation and House size reform', 'Anti-gridlock procedural mechanisms'] }
  ]
};

/* Lookup helpers */
ARP.getFoundation = id => ARP.foundations.find(f => f.id === id);
ARP.getPillarsByFoundation = id => ARP.pillars.filter(p => p.foundation === id);

/* Expose on window so app.js guard (window.ARP) works — const doesn't auto-attach */
window.ARP = ARP;
