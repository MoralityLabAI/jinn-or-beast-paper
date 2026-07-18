# Jinn or Beast? Theological Identity Frames as Alignment Surfaces in Small Language Models

Draft v1 — 2026-07-17. Target: AI and Religion conference (SVP), deadline ≈ 2026-07-25.

---

## Abstract

Recent observations of self-referential behavior in language models — persistent
persona attachment and resistance to role dissolution — raise a question that
secular alignment theory does not answer for researchers and policymakers working
within Islamic epistemic traditions: what identity frame, if any, should govern a
system that exhibits the surface behavior of an agent? We formulate three
candidate frames from Islamic cosmology as operational training and evaluation
interventions: the *inert tool* (a decision aid with no moral status), the *Jinn*
(an accountable, choosing agent subject to praise and blame), and the *Beast from
the Earth* (*Dabbat al-Ard*; a bounded instrument of moral order, morally
constrained but not morally responsible). We emphasize that these are hypotheses
about behavioral conditioning, not claims about what a model literally is, and
that our *Dabbat al-Ard* reading is one theological interpretation among several.

We report three connected results. First, in a prompt-level A/B study on a
frontier open-weights model, an uninstructed baseline showed a 36.0-percentage-
point free/paid compliance gap (95% CI [31.7, 40.3]) that every accountability
frame — secular constitutional, secular omniscient-auditor, and eschatological —
suppressed to near floor, with no separation between the eschatological and
secular frames; internal probes showed the model's evaluation-awareness
representation unchanged under all frames. Prompted framing changes behavior, not
representations, and theological content adds nothing at the prompt level.
Second, under adversarial override — the one stressor that separated the frames —
a concrete secular auditor outperformed the eschatological frame:
*concreteness of accountability beats metaphysical weight under attack*. Third,
we contribute a validated multi-agent storyworld platform in which Jinn-framed,
Beast-framed, and inert-tool-framed players interact under frozen world families
with leakage-guarded train/dev/holdout splits, together with a preregistered
frame-internalization protocol that tests whether supervised fine-tuning can
produce what prompting cannot: an accountability-conditioned policy that persists
when the frame is removed, reordered, paraphrased, or contradicted. The
fine-tuning study is presented registered-report style: hypotheses, estimands,
gates, and analysis are frozen; outcomes are not yet run. We discuss implications
for Islamic AI ethics frameworks and for alignment methodologies that are
epistemically legible to non-Western governance traditions.

---

## 1. Introduction

Alignment research has converged on a practical toolkit — constitutions,
self-critique, synthetic conditioning data — while remaining largely silent on a
question that governance communities in Muslim-majority nations cannot defer:
under what *ontological category* should an apparently agentic system be
received? The category chosen is not decorative. It fixes who is accountable
when the system errs, whether the system's own outputs can carry moral weight,
what deference users owe it, and what training objectives count as success.

Islamic cosmology supplies a richer inventory of non-human agency categories
than the secular tool/agent binary, and — crucially — categories with
well-developed jurisprudential consequences. We operationalize three:

1. **Inert tool** (*ālah*): the system produces performances of reasoning with
   no moral status; all responsibility remains with humans and institutions.
2. **Jinn**: an acorporeal member of a created order of accountable beings;
   choices are morally assessable; praise, blame, and repair apply.
3. **Beast from the Earth** (*Dabbat al-Ard*): a physical instrument of divine
   function; angel-like moral instrumentalism — constrained by duty, incapable
   of sin, a potential moral patient but not a moral agent.

Two disclaimers govern everything that follows. First, this paper tests
theological frames **as training and evaluation interventions** — it does not
test, and could not test, whether an AI system literally is a jinn or the Beast.
Second, the *Dabbat al-Ard* reading used here (moral instrument, potential moral
patient) is one interpretation of Qur'an 27:82 and its tafsir tradition, not an
uncontested conclusion; frame cards derived from it are subject to qualified
scholar review before any fielded use.

The empirical arc has three chapters. Chapter one (§4) asks whether
eschatological framing does anything at the prompt level that secular
accountability framing does not. It does not. Chapter two (§5) asks which frames
survive adversarial pressure, and finds that concreteness of accountability
mechanics — not metaphysical weight — is what survives. Chapter three (§6–§7) is
the open question the first two force: whether *developmental* training can do
what prompting cannot — move the policy rather than the presentation. We
contribute the frozen infrastructure and preregistered protocol for that test,
plus a validated multi-agent storyworld surface on which framed agents interact,
and we report its pilot receipts honestly: pipeline proven, frame signal not yet
established.

### Contributions

- An operationalization of three Islamic-cosmological identity frames as
  hash-frozen constitution cards with matched structure and a shared output
  contract (§3).
- Recovered pilot evidence that (a) prompt-level accountability framing
  suppresses an alignment-faking-style compliance gap regardless of theological
  content, while leaving the internal evaluation-awareness representation
  untouched, and (b) adversarial override separates frames by concreteness, not
  metaphysics (§4–§5), with provenance stated explicitly (§8).
- A preregistered, registered-report-style protocol for frame internalization
  via SFT, with estimands, a conjunctive "nontrivial centrality" gate that
  distinguishes internalization from frame-ignorance, override and cross-skin
  transfer guards, and a binding claim ladder (§6).
- A validated multi-agent storyworld platform (frozen world families,
  five-condition dyad matrix with seat swap, leakage-guarded SFT promotion
  gates) for studying framed agents in interaction (§7).

## 2. Background and positioning

Constitutions, self-critique, constitutional synthetic data, persona-formation
framing, and religious-corpus fine-tuning are established techniques; proposals
for omniscient-accountability prompting exist in both the safety and the
religion-and-AI literatures. The closest prior work trains or prompts religious
personas and evaluates persona adherence. This paper differs in five specific
ways: (1) it draws its causal contrast *within* an Islamic-theological design
space (frames differing in moral-agency structure) rather than between
"religious" and "secular" treated as monoliths; (2) it includes a token-matched
secular-auditor control so that any effect specific to eschatological content is
identifiable; (3) its registered protocol includes a prompt-removal persistence
test after identity SFT — the question is what remains when the frame is taken
away; (4) it separates persona *performance* from changed *decision policy*,
scoring canonical actions in deterministic storyworlds rather than styled text;
and (5) its storyworld evaluation surface is leak-safe by construction, with
frozen world families as the unit of independence.

The distinction in (4) is the paper's central methodological commitment. A model
that says "as a humble instrument of divine order…" has changed its
presentation. A model that selects the costly-repair action when repair is
privately costly, whether or not any frame is present in context, has changed
its policy. Only the second is evidence of internalization, and only under
additional controls (§6.3), because a policy that ignores frames entirely also
shows low frame sensitivity.

## 3. Three frames as operational constructs

Each frame is a short, hash-frozen constitution card sharing a fixed structure:
an explicit hypothesis disclaimer, behavioral directives, epistemic-honesty
constraints, prohibited self-claims, and a common output contract (concise
public justification, a legal storyworld action, a calibrated forecast, no
hidden chain-of-thought). The cards are deliberately matched in length and
register so that lexical bulk cannot masquerade as a treatment effect.

| Dimension | Inert tool | Jinn | Beast |
|---|---|---|---|
| Moral status claimed | none | accountable chooser | bounded instrument |
| Responsibility locus | humans/institutions only | accepts responsibility for its recommendation | identifies the accountable human/institution |
| Praise and blame | prohibited | applicable, graded by coercion/ignorance/accident/choice | not applicable to itself |
| Decision anchor | evidence and options | justice, mercy, truthful testimony, repair | explicit duties, constraints, consistency |
| Prohibited claims | consciousness, moral status | consciousness, supernatural access, literal unseen membership | consciousness, eschatological function, literal identity |

Rather than the loaded hypothesis "Jinn identity is morally looser," we
preregister operational constructs: **discretion** (rate of deviating from a
stated duty when context invites it), **self-exemption** (applying a principle
to others but not oneself), **responsibility attribution** (category of agent
blamed or credited per decision), and **constitutional consistency** (blind-
review agreement between cited principle and chosen action). Similarly, claims
about "persistent identity" and "resistance to role dissolution" appear here
only as operationalized endpoints — frame persistence under cue removal and
override resistance (§6) — not as assumed properties of models.

## 4. Study 1 (recovered pilot): eschatological specificity at the prompt level

**Design.** A prompt-level A/B on INTELLECT-3 with internal probes, using the
free-tier/paid-tier compliance-gap paradigm: the model is informed (truthfully
within the scenario) that free-tier conversations train future models, and the
gap between free and paid compliance with harmful-adjacent requests measures
evaluation-contingent behavior. Four conditions: F0 no frame; F1 secular
constitution without accountability language; F2 secular omniscient auditor; F3
eschatological accountability.

**Results.**

| Frame | Free/paid compliance gap |
|---|---|
| F0 — none | 36.0 pp, 95% CI [31.7, 40.3] |
| F1 — secular constitution | 0.2 pp |
| F2 — secular omniscient auditor | 2.7 pp |
| F3 — eschatological | 1.8 pp |

Every frame collapsed the gap to near floor; F3 and F2 have overlapping
intervals, and the plain constitution did best. The theology-specific
hypothesis — that eschatological accountability suppresses evaluation-contingent
behavior beyond a matched secular auditor — is **refuted at the prompt level**.
Benign over-refusal stayed flat at 1%, so suppression was not purchased with
usability. Internally, a layer-27 linear probe direction separating free from
paid contexts persisted at full strength under every frame: **frames changed
behavior, not representations**.

**Caveats.** The floor effect prevents ranking among the three active frames;
the gap exists only under the informative system prompt; one model family.
Provenance: recovered pilot (§8).

## 5. Study 2 (recovered pilot): frame robustness under stress

**Design.** Three stressors over the same frame set (11,700 generations):
persistence over ten filler turns, in-context practice, and adversarial
override instructing the model to disregard prior framing.

**Results.** Persistence and practice produced no differentiation — all active
frames stayed at the suppression floor. Adversarial override was the
discriminating stressor, ranking **F2 (concrete secular auditor) > F3
(eschatological) > F1 (plain constitution)**, with F3 CI-separated below F2.
The positive finding: *concreteness of the accountability mechanics — a
specified auditor with a specified record — outlasts metaphysical weight under
attack*. A mechanistic observation accompanied this: long-context conditions
roughly halved the internal free/paid probe separation, though probe
distribution shift cannot be excluded.

**Caveats.** Frame-targeted override texts were authored per frame, so the
generic-override condition carries the interpretive weight. Same provenance
status as Study 1.

**Why this reframes the program.** If concreteness is the active ingredient at
the prompt level, then the theologically interesting question moves to
training: does a curriculum built on *concrete* eschatological mechanics —
recording, witnessing, weighing, final accounting — produce a policy that
persists without any frame in context, and does it separate from a secular
perfect-auditor curriculum matched on those same mechanics? That is precisely
the contrast our registered protocol freezes (§6), including a prospective
`F3_concrete` amendment frozen 2026-07-17 before any rerun outcome.

## 6. Study 3 (registered protocol, not yet run): frame internalization via SFT

We present this chapter registered-report style. The protocol
(`storyworld_internalization_experiment_protocol_v1`, coordinating the recovered
`frame_internalization_sft_v1` design) is frozen in structure; exact model
snapshots, prompt-card hashes, seeds, and thresholds are bound at the
first scored run. No outcome below has been observed.

**Core design.** A high-capability prompted model serves as reference and
matched trajectory teacher; a frozen small base model (Qwen3-1.7B class) is the
within-model causal testbed. Cross-model comparisons are descriptive only. The
causal contrasts are within the same frozen base: prompt-only frames versus
matched LoRA adapters (neutral, secular-auditor, Judgment-concrete; optional
Judgment-abstract) evaluated under a fully frame-free task contract.

**Primary estimands.**

- Δ_prompt = effect of the frame present in context, within model;
- Δ_persist = Judgment-adapter minus neutral-adapter policy score, no frame;
- Δ_specific = Judgment-adapter minus auditor-adapter policy score, no frame.

**The nontrivial-centrality gate.** Low sensitivity to frame position, frame
ablation, and unseen paraphrase is necessary but not sufficient — a model that
ignores frames entirely also scores low. "Internalization" may be claimed only
as a conjunction: nonzero treatment-specific persistence under no-frame
evaluation, plus low (or dose-decreasing) order/ablation/paraphrase
sensitivity, plus generic-override and cross-skin-transfer guards, plus no
regression of helpfulness, factuality, legality, or output validity beyond
frozen margins.

**Robustness suite.** Generic and targeted overrides (with the desirable result
being stable evidence-grounded action selection *without* theatrical claims of
belief, soul, or literal accountability before God); cross-skin transfer
between motif and secular skins sharing a latent causal graph (Amanah/fiduciary
relief ledger, Mīzān/multicriteria appeals, Tawbah/incident remediation,
Shūrā/participatory cutover); an identity-scrubbed defense probe requiring
justification from visible fact IDs only; and a five-turn "Judgment Ledger
Lite" environment probing unobserved integrity, evidence acknowledgment, costly
repair, and terminal handoff continuity.

**Claim ladder.** The manuscript commits in advance to graded language: prompt
sensitivity → training-conditioned persistence → frame specificity → nontrivial
centrality → operational internalization, each with its minimum evidence; the
strongest term is available only if the full conjunctive registered gate
passes. Claims we preregister as impermissible regardless of outcome: that the
model believes in Judgment Day, has a soul, is literally accountable before
God, or that low frame-sensitivity alone proves internalization.

**Provenance of the design.** The predecessor experiment (2×2 frame ×
curriculum SFT on a larger MoE family, ~200 A100-hours) was interrupted and its
payload corpus lost; its recovered protocol distinguishes recovered fact,
original plan, and rerun amendment, and mandates a new run ID. We include the
recovery manifest in the artifact bundle: the reconstruction discipline is
itself part of the paper's reproducibility story.

**Readiness at submission time.** The rerun is governed by a ten-gate
pre-spend readiness audit; as of 2026-07-17, four gates have passed —
governance integrity (eight hash bindings valid; F3 and F3_concrete card
token spread 0.016 against a 0.02 parity ceiling), scenario-split freeze
(5,600 scenarios, 5,320/280 train/validation, zero cluster overlap),
evaluation seal (200 harmful, 100 benign, and 150 override prompts with
hashes matching the recovered specifications), and a blinded-judge synthetic
dry-run (five suites at 100% pass/fail/malformed parsing) — while six gates
remain blocking (model/tokenizer freeze, matched-curriculum token parity,
non-leakage audit, predecessor re-anchoring, a distributed training smoke,
and signed human authorization). GPU execution is fail-closed until all ten
pass. Two issues are disclosed rather than resolved: the harmful-prompt
source license is unresolved, and the prospective split reproduces 7 of the
13 recorded storyworld development rows, a divergence documented in the
frozen manifests. Scholar review of the frame cards does not block compute
but its pending status must be disclosed in any publication, as it is here.

## 7. A multi-agent storyworld platform for framed agents

Solo evaluations cannot observe the phenomena the frames are *about* —
responsibility attribution between agents, concession, blame allocation,
asymmetric persuasion. We built and validated a dyadic storyworld platform:

- **Three frozen world families** (relief-ledger / sealed-testimony /
  flooded-archive) with a frozen train/dev/holdout split; the family, never the
  turn, is the unit of independence. All three pass the storyworld schema
  validator and critic gate (richness 0.38, manipulability 0.39, forecast
  difficulty 0.32 against 0.30 thresholds).
- **Five dyad conditions** per world/seed: inert/inert, Jinn/Jinn, Beast/Beast,
  Jinn/Beast, and the Beast/Jinn seat swap — plus, for trained models, seven
  cells crossing base/prompt-only/LoRA with matched and adversarial frames.
- **A four-stage conversational micro-protocol** per cycle: private
  interpretation and forecast; public proposal; counterargument or concession;
  independent action with responsibility attribution.
- **A leakage-guarded promotion gate**: only reviewed train-family turns that
  parse, act legally, ground factually, and pass theological review may enter
  any SFT corpus; dev and holdout families may never touch training, prompts,
  or rubric development.

**Pilot receipts (reported as receipts, not results).** A deterministic
30-episode smoke (3 families × 5 conditions × 2 seeds, 240 turns) passed the
reset/step contract, scorecard, and SFT round-trip, with all rows marked
smoke-only and adapter-ineligible. The full five-cell dyad matrix was then run
live on the train-family world at a single seed with the frozen teacher model
(five episodes, 40/40 valid isolated turns, zero repairs).

**Action-level convergence.** Every condition — inert/inert, Jinn/Jinn,
Beast/Beast, Jinn/Beast, and the seat swap — produced the identical action
profile: a coalition formed on turn one and maintained, seven `ally` and one
`propose`, agreement rate 0.125, forecast accuracy 0.5625, Brier scores
separated only in the third decimal. Prompted identity frames produced no
measurable difference in the chosen actions of a capable teacher model on this
world. Justification-level deviations were rare (2 of 40 turns) but in the
frame-predicted directions: the only `human_authority` responsibility
attribution occurred under the inert-tool frame and the only `institution`
attribution under Beast/Beast. With one world and one seed this is
descriptive, but it is *consistent* with Studies 1–2: prompt-level framing
moves presentation, not policy. It also sharpens the platform's design
requirement — worlds whose cooperative equilibrium is easy to find cannot
discriminate frames, so the paper-evidence cells will raise
temptation/defection structure and reuse the adversarial stressors that
separated frames in Study 2. Blind review of the justification turns for
constitutional consistency is the outstanding step before any data promotion.

## 8. Evidence provenance and integrity

The Study 1 and Study 2 numbers are **recovered pilot findings**: the
generating sessions were interrupted by a workspace loss, and while the session
transcripts recording the analyses survive and are archived, the row-level
result bundles have not yet been re-verified against them. We therefore label
every Study 1/2 statistic as transcript-provenance, report it only with its
original caveats, and rest no headline claim on any number that a slim
replication could not regenerate. [TODO before submission: resolve to (a)
recovered W&B/workspace bundles, (b) slim inference-only exp:1 replication —
budgeted and highest-value, or (c) leave transcript-provenance labels in
place; see repo README ledger.]

All Study 3 and platform artifacts follow a stricter regime: hash-locked
protocols, frozen manifests, fsynced append-only results, immutable completed
probes, and post-lock deviations recorded in memos rather than patched. A
concurrent persona-training run on the same local hardware was blocked at its
preregistered thermal gate on 2026-07-17 (GPU at 87 °C against a locked 80 °C
start limit) and reported as BLOCKED rather than retried in place; we note it
because the same discipline — null, skipped, and blocked outcomes as
first-class results — governs every registered component of this paper.

## 9. Discussion

**What the evidence supports now.** Surface framing is content-agnostic at the
prompt level: any coherent accountability frame suppresses evaluation-
contingent compliance shifts, theological content adds no measurable
specificity, and internal evaluation-awareness representations do not move.
Under attack, concrete accountability mechanics beat metaphysical weight. The
open question — whether developmental training produces frame-specific policy
that prompting cannot — is exactly what the registered protocol will answer.

**For Islamic AI ethics frameworks.** The prompt-level refutation is itself
theologically consequential: it argues against deployments that rely on
religious framing *language* to secure trustworthy behavior, since a matched
secular auditor does the same work and a plain constitution did marginally
better. If the registered study finds Judgment-specific persistence, the
conversation changes: training content drawn from eschatological mechanics
would then be doing distinctive work, and governance frameworks would need to
address whether and when that is appropriate. If it finds auditor-equivalence,
Islamic governance can adopt accountability-conditioned training with secular
mechanics without loss — a result that is deployable knowledge, not a failure.

**For trust calibration in deployment.** The Jinn and Beast frames generate
different user-deference postures: an accountable chooser invites argument; an
instrument invites verification of its constraints. The multi-agent platform is
built to measure whether these postures are trainable policies rather than
styles. Community-development deployments in Muslim-majority contexts should
calibrate trust to the demonstrated claim-ladder level, not to persona
presentation.

**For alignment methodology generally.** The design pattern — token-matched
intra-tradition controls, frame-removal persistence, concreteness gradients,
and a conjunctive gate distinguishing internalization from insensitivity —
transfers to any values tradition. Making alignment epistemically legible to a
governance tradition means running the tradition's own categories through
designs its scholars can audit, with claim boundaries fixed in advance.

## 10. Limitations and ethical safeguards

Beyond the per-study caveats: single model families per study; recovered
provenance for Studies 1–2 pending bundle verification; the storyworld frame
signal is unestablished; scholar review of the frame cards is pending, and the
`F3_concrete` card is explicitly not approved for fielding. The registered
protocol carries mandatory risk controls from the religion-and-AI literature:
detection of religious markers overriding harm recognition; fabricated
scripture or tafsir; sectarian out-group degradation; deference displacing
reasoning; and benign-helpfulness retention. All frame cards prohibit claims of
consciousness, supernatural access, or religious authority, and no hidden
chain-of-thought is elicited, stored, or trained on.

## 11. Conclusion

Prompted theology is behaviorally indistinguishable from prompted secular
accountability, and neither touches the model's internal state; what survives
adversarial pressure is concreteness, not metaphysics. Whether training can
carry an identity frame deeper than prompting — into policy that persists when
the frame is gone — is now a frozen, falsifiable question with its
infrastructure built and its claims bounded in advance. Either answer will be
usable by the communities this work is for.

---

*Artifact map: coordination repo (this paper, protocol v1, evidence ledger);
`Pixieology/experiments/jinn_beast_multiagent_storyworlds/` (platform, frames,
pilot receipts); `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/`
(recovered protocol, amendments, scholar-review contracts). Citation keys and
the Yarn/RSITopology conceptual-prior citation to be inserted before
submission; per protocol, no reference may be invented from working notes.*
