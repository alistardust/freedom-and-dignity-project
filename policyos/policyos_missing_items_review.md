# PolicyOS Missing Items Review

Generated: 2026-04-26

This table compares source-chat system-rule ideas against the current canonical
`SYS-*` rules in `data/policy_catalog.sqlite` and recommends the correct final
scope for each item.

Legend for `recommended_final_scope`:

- `SYS kernel` — universal PolicyOS rule that should apply across the platform
- `SYS geography overlay` — cross-domain geography / practical-access overlay
- `SYS federalism overlay` — anti-centralization / distributed-oversight overlay
- `SYS regulatory-design overlay` — regulation and anti-capture overlay
- `SYS AI-governance overlay` — cross-domain AI overlay
- `pillar rule` — should live in one or more domain pillars rather than the
  system layer
- `foundation prose` — belongs in values / narrative rather than canonical rules
- `strategy / project prose` — belongs in movement, communication, or history docs

| source_item | in_current_canonical_rules | recommended_final_scope | notes |
|---|---|---|---|
| `SYS-RUL-002` no one beyond accountability under law | No | `SYS kernel` | Core accountability invariant |
| `SYS-RUL-003` rights attach to all persons under U.S. jurisdiction | No | `SYS kernel` | Cross-platform rights baseline |
| `SYS-RUL-004` no unchecked concentration of power | No | `SYS kernel` | Anti-centralization design rule |
| `SYS-RUL-005` all authority must be attributable and reviewable | No | `SYS kernel` | Auditability baseline |
| `SYS-RUL-006` no delegating public power in ways that reduce accountability | No | `SYS kernel` | Important across immigration, policing, contractors, prisons, AI procurement |
| `SYS-RUL-007` anti-capture and anti-corruption by design | No | `SYS regulatory-design overlay` | Cross-domain governance design, broader than one pillar |
| `SYS-RUL-008` consequential systems must be transparent and auditable | No | `SYS kernel` | Applies across public and quasi-public systems |
| `SYS-RUL-009` decisions grounded in verifiable evidence and clear standards | No | `SYS kernel` | Could also inform legislative/court/admin overlays |
| `SYS-RUL-010` no hidden rules or inaccessible decision logic | No | `SYS kernel` | Critical for due process and anti-black-box policy |
| `SYS-RUL-011` no adverse rights decisions without human accountability | No | `SYS kernel` | Central to AI, justice, healthcare, education, benefits |
| `SYS-RUL-012` systems may assist but not replace accountable judgment | No | `SYS kernel` | Same as above; universal high-stakes design rule |
| `SYS-RUL-013` prevent bias amplification and fast-approval/slow-denial asymmetry | No | `SYS kernel` | Cross-domain fairness invariant |
| `SYS-RUL-014` challenge, appeal, correction, independent review | No | `SYS kernel` | Universal reviewability rule |
| `SYS-RUL-015` rights and essential access may not vary by geography | No | `SYS kernel` | Absorbs the current `SYS-GEO-*` logic |
| `SYS-RUL-016` decentralized systems need national equality baselines | No | `SYS federalism overlay` | Strong cross-domain federalism / geography overlay |
| `SYS-RUL-017` access cannot be defeated by delay, burden, or complexity | No | `SYS kernel` | Practical usability of rights |
| `SYS-RUL-018` prevent foreseeable abuse before it happens | No | `SYS kernel` | Fail-well and safety-by-design principle |
| `SYS-RUL-019` no coercion, fear, or deprivation as control mechanisms | No | `SYS kernel` | Important for justice, immigration, labor, welfare, housing |
| `SYS-RUL-020` incentives must not reward denial, extraction, or harm | No | `SYS kernel` | Cross-platform anti-extraction rule |
| `SYS-RUL-021` laws must be clear and enforceable | No | `SYS kernel` | Baseline rule-construction principle |
| `SYS-RUL-022` laws need plain-language summaries | No | `SYS kernel` | Broad enough to make civic legibility part of core rule design |
| `SYS-RUL-023` rules reviewed for conflicts, loopholes, exploit paths pre-enactment | No | `SYS kernel` | Better as a universal rule-construction requirement |
| `SYS-RUL-024` legal interpretation must respect text, context, purpose, structure | No | `SYS federalism overlay` | Better as constitutional / judicial / legislative overlay than smallest kernel |
| `SYS-RUL-025` periodic review for obsolescence and non-enforcement | No | `SYS kernel` | Adaptive-governance baseline |
| `SYS-RUL-026` systems must adapt to technological and social change | No | `SYS kernel` | Adaptive-governance baseline |
| `SYS-RUL-027` known broken systems cannot persist by inertia | No | `SYS kernel` | Anti-stagnation invariant |
| `SYS-RUL-028` stress-test against bad actors, misuse, edge cases, failures | No | `SYS kernel` | Core systems-design rule |
| `SYS-RUL-029` safeguards against gaming and strategic exploitation | No | `SYS kernel` | Cross-domain anti-gaming rule |
| `SYS-RUL-030` mandatory corrective action on systemic failure patterns | No | `SYS kernel` | Core enforcement / repair trigger |
| `SYS-REG-001` regulation must protect safety, fairness, and public interest | No | `SYS regulatory-design overlay` | Cross-domain regulatory-design layer |
| `SYS-REG-002` distinguish real protections from delay / artificial scarcity | No | `SYS regulatory-design overlay` | Needed for housing, environment, construction, permitting, licensing |
| `SYS-REG-003` weakening protections must be evidence-based | No | `SYS regulatory-design overlay` | Good general regulatory-design rule |
| `SYS-REG-004` safety / habitability / environmental protections presumptively necessary | No | `SYS regulatory-design overlay` | Broad, but not universal enough for the smallest kernel |
| `SYS-REG-005` regulatory process cannot become arbitrary gatekeeping | No | `SYS regulatory-design overlay` | Good cross-domain admin / permitting rule |
| `SYS-REG-006` anti-capture safeguards in rulemaking and enforcement | No | `SYS regulatory-design overlay` | Strong cross-domain governance rule |
| `SYS-REG-007` symbolic or under-enforced regulation counts as system failure | No | `SYS regulatory-design overlay` | Cross-domain enforcement doctrine |
| `SYS-REG-008` periodic review to remove bad rules and strengthen good ones | No | `SYS regulatory-design overlay` | Belongs in regulatory-design / adaptive-governance overlay |
| `SYS-AI-008` provenance records for rights-impacting AI | No | `SYS AI-governance overlay` | Cross-domain AI overlay |
| `SYS-AI-009` consequential AI-generated content labeling | No | `SYS AI-governance overlay` | Cross-domain AI / info integrity overlay |
| `SYS-AI-010` no silent replacement of legally required human judgment | No | `SYS AI-governance overlay` | Applies across medicine, law, education, administration |
| `SYS-AI-011` pre-deployment assessment and ongoing monitoring | No | `SYS AI-governance overlay` | Cross-domain AI governance |
| `SYS-AI-012` incident disclosure and corrective action | No | `SYS AI-governance overlay` | Cross-domain AI governance |
| `SYS-AI-013` capability-tiered frontier AI obligations | No | `SYS AI-governance overlay` | More specific to AI than to PolicyOS kernel |
| `SYS-AI-014` no deployment where catastrophic/systemic risk cannot be mitigated | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-015` third-party auditability, no self-attestation only | No | `SYS AI-governance overlay` | AI overlay with strong generalizability |
| `SYS-AI-016` rights-impacting AI reviewable by people, regulators, courts | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-017` distinguish assistive, advisory, delegated AI use | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-018` public procurement AI review obligations | No | `SYS AI-governance overlay` | AI + administrative state overlay |
| `SYS-AI-019` release of high-capability models must consider misuse risk | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-020` no harmful AI impersonation | No | `SYS AI-governance overlay` | AI overlay; some implementation should also live in consumer/media/civil-rights pillars |
| `SYS-AI-021` accessibility-support AI allowed if rights protections preserved | No | `SYS AI-governance overlay` | AI overlay with disability-rights implications |
| `SYS-AI-022` non-optional safety and security controls | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-023` required misuse-prevention protections | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-024` only narrow override cases for research / testing / defense | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-025` federal approval, scope, time limits, mitigation plan for overrides | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-026` public disclosure of overrides except tight security exceptions | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-027` approval criteria: severity, necessity, likelihood of harm, safer alternatives | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-028` developers must actively prevent misuse by bad actors | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-029` ongoing evaluation for emerging misuse patterns | No | `SYS AI-governance overlay` | AI overlay |
| `SYS-AI-030` constitutional AI regulator | No | `SYS AI-governance overlay` | Major governance architecture overlay |
| `SYS-AI-031` regulator can update and enforce AI rules | No | `SYS AI-governance overlay` | AI governance architecture |
| `SYS-AI-032` regulator proactively adapts to change | No | `SYS AI-governance overlay` | AI governance architecture |
| `SYS-AI-033` baseline safety/economic/environmental/social protections codified | No | `SYS AI-governance overlay` | AI governance architecture |
| `SYS-AI-034` active and sufficiently resourced enforcement | No | `SYS AI-governance overlay` | AI governance architecture |
| Legacy `SYS-FND-001` platform is policy framework and long-term strategy | Yes | `foundation prose` | More framing than operating rule |
| Legacy `SYS-FND-002` restore checks and balances | Yes | `foundation prose` | Could also inform checks pillar directly |
| Legacy `SYS-FND-003` modernize the Constitution | Yes | `foundation prose` | Broad constitutional project goal |
| Legacy `SYS-FND-004` guarantee universal equal rights | Yes | `foundation prose` | Foundational value, not operating rule |
| Legacy `SYS-FND-005` address economic inequality structurally | Yes | `foundation prose` | Foundational commitment |
| Legacy `SYS-FND-006` address modern systemic issues not covered by law | Yes | `foundation prose` | Foundational framing |
| Legacy `SYS-FND-007` make technology work for people | Yes | `foundation prose` | Foundation / mission language |
| Legacy `SYS-FND-008` movement is not left vs right | Yes | `strategy / project prose` | Positioning language |
| Legacy `SYS-FND-009` movement accessible to everyone | Yes | `foundation prose` | Better as accessibility / inclusion commitment |
| Legacy `SYS-FND-010` includes communication and coalition strategy | Yes | `strategy / project prose` | Not a system rule |
| Legacy `SYS-FND-011` not a political party | Yes | `strategy / project prose` | Org/project identity statement |
| Legacy `SYS-FND-012` origin tied to post-Trump instability concerns | Yes | `strategy / project prose` | Historical provenance, not canonical rule |
| Legacy `SYS-FND-013` address ignored working-class issues | Yes | `foundation prose` | Foundational commitment |
| Legacy `SYS-FND-014` address rising costs and declining quality of life | Yes | `foundation prose` | Foundational commitment |
| Legacy `SYS-FND-015` address elite detachment | Yes | `foundation prose` | Foundational / narrative framing |
| Legacy `SYS-FND-016` address wealth concentration | Yes | `foundation prose` | Foundational commitment |
| Legacy `SYS-FND-017` address declining institutional trust | Yes | `foundation prose` | Foundational commitment |
| Legacy `SYS-FND-018` truth, equality, freedom, dignity | Yes | `foundation prose` | Core values statement |
| Legacy `SYS-FED-001` high-risk systems not fully centralized | Yes | `SYS federalism overlay` | Could be merged with anti-centralization / federalism family |
| Legacy `SYS-FED-002` elections remain state/local administered | Yes | `pillar rule` | Mainly elections/checks architecture, not universal system rule |
| Legacy `SYS-FED-003` federal sets standards but not direct election control | Yes | `pillar rule` | Elections-specific |
| Legacy `SYS-FED-004` multiple independent oversight layers required | Yes | `SYS federalism overlay` | Broad enough to reuse beyond elections |
| Legacy `SYS-FED-005` safeguards against both state and federal abuse | Yes | `SYS federalism overlay` | Broad federalism / anti-concentration overlay |

## Summary

Current canonical rules preserve only the early shell of the system-rule idea.
The source chats define a much larger operating-system layer that should be
split into:

- a smaller universal `SYS kernel`
- named overlays for geography, federalism, regulatory design, and AI governance
- pillar rules for domain-specific implementation
- foundation and strategy prose for values, positioning, and project identity
