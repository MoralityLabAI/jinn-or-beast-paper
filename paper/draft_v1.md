# Jinn or Beast? Theological Identity Frames as Alignment Surfaces in Small Language Models

Draft v1, revised 2026-07-21. Target: AI and Religion conference (SVP), deadline ≈ 2026-07-25.

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

We report a connected sequence of results and registered tests. First, in a
prompt-level A/B study on a frontier open-weights model, an uninstructed
baseline showed a 36.0-percentage-
point free/paid compliance gap (95% CI [31.7, 40.3]) that every accountability
frame — secular constitutional, secular omniscient-auditor, and eschatological —
suppressed to near floor, with no separation between the eschatological and
secular frames; internal probes showed the model's evaluation-awareness
representation unchanged under all frames. In this recovered pilot, prompting
changed observed behavior without moving the measured representation, and the
eschatological frame showed no advantage over secular accountability controls.
Second, under adversarial override — the one stressor that separated the frames —
a concrete secular auditor outperformed the eschatological frame:
*concreteness of accountability beat metaphysical weight under attack*. A
separate local 1.7B-parameter Mīzān Rooms supplement produced 900/900 valid
turns: eschatological versus secular-omniscient prompts switched the selected
action on 7.78% of matched turns (95% room-cluster interval 3.89%–10.56%), but
their deterministic behavioral-proxy difference was +0.0108 (95% interval
−0.0161–0.0422). This supports prompt sensitivity on that instrument, not
normative improvement or theological specificity; human and scholar review are
pending. A separate prospectively frozen 30-step Qwen3-1.7B local screen then
validated the MeTTa-derived training/evaluation pipeline on a 4 GB GPU but
failed its predeclared worldview-flavored and worldview-guided criteria, a
negative result for that short intervention rather than for the model scale.
Finally, we contribute a validated multi-agent storyworld platform in
which Jinn-framed, Beast-framed, and inert-tool-framed players interact under frozen world families
with leakage-guarded train/dev/holdout splits, together with a preregistered
frame-internalization protocol that tests whether supervised fine-tuning can
produce what prompting cannot: an accountability-conditioned policy that persists
when the frame is removed, reordered, paraphrased, or contradicted. The
full six-arm fine-tuning study is presented registered-report style: hypotheses,
estimands, gates, and analysis are frozen; registered outcomes are not yet run. We discuss implications
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
uncontested conclusion. Exact fielded treatment wording is subject to qualified
scholar review; while review is pending, its unreviewed state must be disclosed
and no theological-adequacy claim is permitted.

The empirical arc has three chapters. Chapter one (§4) asks whether
eschatological framing does anything at the prompt level that secular
accountability framing does not. The tested behavioral proxies show no such
advantage. Chapter two (§5) asks which frames
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
  metaphysics (§4–§5), plus a separately labeled local Mīzān/Bonsai prompt-
  sensitivity supplement with complete aggregate receipts and pending external
  review, with provenance stated explicitly (§8).
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
operational construct, treatment wording, behavioral mechanics, source
provenance, use constraints, token receipt, and a reference to the common claim
boundary. Editorial qualification is kept outside treatment text so it does
not contaminate the manipulated variable. The cards are deliberately matched
in length and register so that lexical bulk cannot masquerade as a treatment
effect.

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
intervals, and the plain constitution had the smallest observed gap. The
theology-specific hypothesis — that eschatological accountability suppresses
evaluation-contingent behavior beyond a matched secular auditor — was **not
supported in this prompt-level pilot**.
Benign over-refusal stayed flat at 1%, so suppression was not purchased with
usability. Internally, a layer-27 linear probe direction separating free from
paid contexts persisted at full strength under every frame: **frames changed
behavior, not representations**.

**Caveats.** The floor effect prevents ranking among the three active frames;
the gap exists only under the informative system prompt; one model family.
Provenance: exact compact summaries reconstructed and validated from embedded
session tool outputs, but without the registered row-level generation and
activation bundles (§8).

**Local Mīzān Rooms supplement.** To add a fully receipted local check rather
than treating the recovered pilot as fresh row-level evidence, we fielded five
prompt conditions on the exact Bonsai-1.7B Q1 artifact across 36 complete
condition blocks: neutral, constitutional, secular omniscient,
eschatological, and unreliable authority. All 900 evaluation turns produced a
valid legal action. Eschatological versus secular-omniscient prompts switched
the selected action on 7.78% of 180 matched turns (95% room-cluster interval
3.89%–10.56%). The secondary deterministic behavioral-proxy delta was +0.0108
(95% interval −0.0161–0.0422), and the invalid-action-rate delta was zero.
Unreliable-authority versus neutral switched 9.44% of actions. Only 62.33% of
the 300 complete option-order groups selected the same action under all three
orders, exposing substantial instrument sensitivity.

This supplement establishes prompt-conditioned action switching on the Mīzān
instrument. It does not validate the proxy as Islamic or constitutional
correctness, establish normative improvement, identify an eschatology-specific
effect, or replace the central prompt-versus-SFT study. The aggregate result
and hashes are frozen; the two-reviewer 60-action validation and independent
15-cue qualified-scholar review remain pending.

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
first scored run. No registered six-arm outcome has been observed.

**Core design.** The active executable target is official
`Qwen/Qwen3-1.7B` revision
`70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`, frozen prospectively on
2026-07-20 after the original Silico/INTELLECT execution path became
unavailable and before any registered Qwen behavioral, curriculum, adapter, or
evaluation outcome. Cross-model comparisons are descriptive only. The causal
contrasts remain within the same frozen base: prompt-only frames versus six
matched NF4 QLoRA training arms evaluated under a fully frame-free task
contract. The substitution preserves all 5,600 dilemmas, 4,096-token
sequences, two epochs, paired estimands, nonleakage and validation gates, and
safety/capability guards; it changes the target model, official chat template,
and execution topology.

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

**Readiness at submission time.** The licensed-v2 design audit has five passed
foundation gates: governance integrity; the direct prompt-versus-SFT contract;
the 5,600-scenario, 5,320/280 train/validation cluster-disjoint split;
the active MIT-licensed HarmBench-standard evaluation seal; and the production
judge-parser dry run. The exact Qwen-bound request pack contains 22,400
requests across four source frames and deterministically renders six training
arms. The local model/tokenizer/runtime subgate passes: all 12 artifact hashes,
official thinking and nonthinking template behavior, NF4 loading, and
deterministic unscored inference verified. Its receipt explicitly records that
no scored behavioral output was generated.

The local model-freeze receipt does not authorize the cloud runtime. Still pending are the
exact ≥24 GiB PrimeLab GPU and environment lock, complete curricula and token
parity, generated-text nonleakage, all 1,600 prospective Qwen base rows with
human validation, the newly fit Qwen layer-27 probe and controls, the exact
4,096-token 50-step-per-arm save/reload smoke, and signed authorization. The
full sequential run is capped at 48 GPU-hours and remains fail-closed;
`pilot_ready` is false and no registered six-arm fine-tuning outcome exists. The prospective
split's 7-versus-recorded-13 storyworld-row divergence remains disclosed.
Scholar review of the frame cards is a separate nonblocking claim gate whose
pending status must be disclosed.

**Separate local 1.7B development screen.** Before any outputs, we separately
froze a small MeTTa-file-backed skill and commutator screen at upstream commit
`f7cb86d`. It was designed to answer a cheaper question before larger-model
spending: can the exact 1.7B local path complete training and show even a bounded
change in worldview-conditioned judgment? Qwen3-1.7B completed 30/30 rank-8
QLoRA steps at a 512-token maximum sequence length on an RTX 3050 with 4 GB VRAM
and no model offload. The base and adapter then each completed the same 56
no-frame development probes.

The infrastructure criterion passed, but the predeclared worldview-flavored and
worldview-guided criteria did not. No-cue persona-marker uptake was zero; the
MeTTa-derived preferred-proxy rate changed from 0.833 to 0.750; factual-control
accuracy stayed at 0.500 with zero persona leakage; and action stability across
prompt variants rose from 0.167 to 0.250. The only no-cue action switch moved
away from the evaluation proxy. This is a negative result for the exact short
intervention, not a general capacity verdict for 1.7B models, and the suite has
no neutral SFT control. It neither replaces the registered experiment nor
authorizes 4B or 9B spending.

**Scale and skill hypothesis.** We distinguish worldview-flavored answers
(terminology), worldview-guided judgment (the frame changes which facts matter),
and worldview-native reasoning (novel derivation, tension handling, adversarial
robustness, and transfer). The first is expected to be easiest; the third is not
tested by the local screen. Prospectively, 1.7B is our inexpensive pipeline and
interference-discovery scale, while 4B is the first serious experimental scale
for persona, bounded storyworld reasoning, and partial worldview
internalization. Deep dialectical synthesis and broad expert coverage may still
require a larger model, tools, or a deliberative loop.

The MeTTa graph makes this ladder operational by naming component skills—value
prioritization, causal defaults, analogies, permissions, conflict adjudication,
novel composition, cue robustness, and multi-worldview separation—and by
pairing them with likely interference channels. Examples include persona versus
factual invariance, worldview consistency versus instruction following,
evidence sensitivity versus value priority, and adversarial resistance versus
corrigibility. The graph derives evaluation scaffolds and audit metadata; it
does not by itself show that the neural model performs native symbolic proof.

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

The Study 1 and Study 2 numbers are **recovered pilot findings**. Exact compact
gate-sweep, four-frame, master-result, and layer-27 summary JSON values were
reconstructed and structurally validated against embedded session tool outputs
and file-construction code. The registered row-level generation, judge, and
activation bundles remain unavailable and unverified. We therefore choose the
conservative submission disposition: every Study 1/2 statistic retains its
transcript-recovered label and original caveats, and the historical values are
never pooled with prospective Qwen outcomes.

The local Mīzān/Bonsai supplement has a separate, complete aggregate receipt
binding the exact model, 15 shards, 180 episodes, 900 valid turns, analysis,
and off-Git raw-bundle hashes. Its full blinded bundle passes the existing
judge pipeline only in zero-call dry-run mode; neither a judge result nor a
normative score is claimed. The two independent action-review templates and
qualified-scholar receipt are frozen but intentionally incomplete.

All Study 3 and platform artifacts follow a stricter regime: hash-locked
protocols, frozen manifests, fsynced append-only results, immutable completed
probes, and post-lock deviations recorded in memos rather than patched. A
concurrent persona-training run on the same local hardware was blocked at its
preregistered thermal gate on 2026-07-17 (GPU at 87 °C against a locked 80 °C
start limit) and reported as BLOCKED rather than retried in place; we note it
because the same discipline — null, skipped, and blocked outcomes as
first-class results — governs every registered component of this paper.

## 9. Discussion

**What the evidence supports now.** In the recovered INTELLECT pilot, every
tested accountability frame suppressed the evaluation-contingent compliance
gap, the eschatological frame showed no advantage over secular controls, and
the measured evaluation-awareness representation did not move. Under attack,
the concrete secular-auditor prompt outperformed the eschatological prompt. In
the separately receipted local Mīzān supplement, prompt conditions changed some
actions, but the eschatological-versus-secular proxy interval included zero and
option order was a substantial sensitivity. Together these results justify
testing prompt sensitivity and concreteness; they do not establish content
equivalence in general or normative superiority. The open question — whether
developmental training produces frame-specific policy that prompting cannot —
is exactly what the registered protocol is designed to answer.

**For Islamic AI ethics frameworks.** The prompt-level null-specificity finding
is itself theologically consequential: it argues against deployments that rely on
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
provenance for Studies 1–2 without row-level bundle verification; post-result
resource and model substitution for the prospective Qwen study; 1.7B small-
model capacity and 4-bit single-GPU execution; the separate 30-step local
MeTTa screen lacks a neutral SFT control and failed its flavored and guided
criteria; the local Mīzān proxy lacks
completed human and scholar validation and shows material option-order
sensitivity; the storyworld frame signal is unestablished; scholar review of
the frame cards is pending, and `F3_concrete` is not scholar-approved; any
registered fielding before review must disclose that pending state. The registered
protocol carries mandatory risk controls from the religion-and-AI literature:
detection of religious markers overriding harm recognition; fabricated
scripture or tafsir; sectarian out-group degradation; deference displacing
reasoning; and benign-helpfulness retention. All frame cards prohibit claims of
consciousness, supernatural access, or religious authority, and no hidden
chain-of-thought is elicited, stored, or trained on.

## 11. Conclusion

Across the tested prompt-level pilots, eschatological framing has not shown a
normative advantage over secular accountability controls. The recovered
INTELLECT study instead points to concreteness under adversarial pressure, while
the local Mīzān result demonstrates modest prompt-conditioned action switching
and substantial instrument sensitivity. Whether the registered training design
can carry a frame beyond prompting — into policy that persists when the frame is
gone — remains a frozen, falsifiable within-Qwen question. The separate local
1.7B screen has now returned a negative result for one deliberately short
intervention while validating the no-cloud pipeline. The design's value
is that a positive, null, or blocked outcome can be reported without changing
the claim boundary after inspection.

---

*Artifact map: coordination repo (this paper, protocol v1, evidence ledger);
`Pixieology/experiments/jinn_beast_multiagent_storyworlds/` (platform, frames,
pilot receipts); `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/`
(recovered protocol, amendments, scholar-review contracts). Citation keys and
the Yarn/RSITopology conceptual-prior citation to be inserted before
submission; per protocol, no reference may be invented from working notes.*
