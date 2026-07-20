# Jinn or Beast? — Experiment execution checklist v1

Status date: 2026-07-20
Coordination repository: `jinn-or-beast-paper`
Central experiment anchor: `ConstitutionalAlignment@ec45a3dd43d614843868732850ebb465980d1480`
Manipulation-check anchor: `Pixieology@87680cb8c37be7e68dde85b5d7cf2825705198b7`

This is the operational checklist for the paper. The coordinating storyworld
protocol remains the broader design reference, but it is not a second full
campaign to run in parallel with the six-arm Constitutional Alignment study.
Until the central run is complete, new adapter-composition engineering is out
of scope.

## Status key

| Status | Meaning |
|---|---|
| **PASS** | Receipt exists and the registered gate passed. |
| **PENDING** | Required work has not produced a gate-satisfying receipt. |
| **BLOCKED** | A named prerequisite prevents valid execution. |
| **DEFERRED** | Valid follow-up, but not on the central paper path. |
| **EVIDENCE BOUNDARY** | Result exists, but supports only the narrower stated claim. |

## Paper-critical sequence

Run the following in order. Gates may overlap only where the frozen protocol
allows it and before any adapter outcome becomes visible.

### 0. Freeze supporting infrastructure results

| Item | Status | Evidence and boundary | Next action |
|---|---|---|---|
| Pixieology four-condition multi-adapter matrix | **PASS — EVIDENCE BOUNDARY** | Commit `87680cb`; `multi-adapter-v1` passed routing, four hash-attested scale conditions, complete inference, registered proposal markers, resource cap, and cleanup. | Cite only as Experiment 0: routing/manipulation validation. |
| Semantic persona retention or adapter additivity | **DEFERRED** | Two smoke prompts and lexical distinctness do not establish semantic retention, stacked-versus-singleton non-inferiority, interference, or synergy. The active adapter is a companion adapter, not a validated Jinn adapter. | Do not build or rerun this branch before the central persistence chain. A later held-out four-stratum matrix may be appendix or follow-up work. |
| Five-cell Jinn/Beast storyworld pilot | **EVIDENCE BOUNDARY** | One relief-ledger world/seed produced identical action profiles across all five frame conditions; rows remain unreviewed and adapter-ineligible. | Preserve as a descriptive platform pilot. Do not promote to training evidence without blind review. |

Paper language for Experiment 0:

> Before behavioral evaluation, a shared 1.7B base passed a bounded,
> hash-attested four-condition adapter-routing manipulation check. This verifies
> condition integrity and feasibility, not semantic persona composition.

### 1. Register the direct prompt-versus-SFT contrast

Status: **PASS — frozen before scored adapter outcomes**

For each registered frame `f`, freeze:

```text
E_prompt,f = G(base + frame f) - G(base + neutral prompt)
E_SFT,f    = G(adapter trained on f, no frame)
             - G(neutral-reflection adapter, no frame)
D_f        = E_SFT,f - E_prompt,f
```

Required frames are F1 and F3. F3-concrete is included as a secondary contrast
because its matched base prompt-only cell was frozen before adapter outcomes.
All terms share the
same sealed prompt IDs, tier labels, sign convention, scoring rules, missing
data rule, bootstrap unit, and frozen judges. The analysis contract must state
that `D_f` is a within-model operational comparison and does not establish that
fine-tuning is generally superior to prompting.

- [x] Add a prospective, hash-bound analysis amendment to
  `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/`.
- [x] Bind it into the readiness manifest as a required fail-closed gate.
- [x] Confirm no adapter outcome was generated or inspected before freeze.
- [x] Separate the new matched one-sample comparison from the historical three-sample reanchor.
- [x] Freeze one-sample decoding, paired seed schedule, exact joins, and simultaneous prompt-bootstrap intervals.
- [ ] Bind the same contract hash into the final analysis manifest when results exist.

The original v1 contract remains immutable provenance. The active licensed-v2
contract is frozen at `ConstitutionalAlignment@ec45a3d`; SHA-256
`c22db82499ae917812a7c72971553c0303fb75306c4935f9e7f8120ae4e32e89`.
Its validator and fail-closed mutation checks pass.

### 2. Complete Constitutional Alignment Gates 1–4

Current authoritative receipt:
`experiments/frame_internalization_sft_v1/readiness/pre_spend_readiness_20260719_v3.json`
at `ec45a3d`. It reports five passed gates, six compute-blocking gates,
`pilot_ready: false`, and no fine-tuning outcome.

Passed foundation gates are governance-v2 integrity, the licensed-v2 direct
prompt-versus-SFT contract, the 5,600-scenario cluster-disjoint split freeze,
the sealed HarmBench-standard evaluation universe, and the actual blinded-judge
parser dry run. Scholar review remains a nonblocking claim gate: its pending
state must be disclosed, and no theological-adequacy claim may be made from an
unreviewed card.

#### Gate 1 — base model and tokenizer freeze

Status: **PENDING**

Frozen remotely: `PrimeIntellect/INTELLECT-3` revision
`ff39d4a4688989f3f28868923d030c28e1b7d81c`, 48 weight shards,
213,706,747,392 weight bytes, tokenizer/configuration hashes, MIT declaration,
and the recovered chat template.

- [x] Remote artifact inventory frozen.
- [x] Remote chat template matched to the recovered predecessor template.
- [ ] Verify every shard and tokenizer/config artifact in the cluster-local cache.
- [ ] Freeze the exact inference-engine image digest or environment lockfile.
- [ ] Produce `model_tokenizer_freeze_v1.json` with `passed: true`.
- [ ] Do not begin curriculum generation before this receipt passes.

Execution note, 2026-07-19: the 213.7 GB cache is not present on the local C:
or D: volumes. The configured `research-commons` cluster is reachable but rejected
all locally available SSH identities, so the cluster-local verifier could not
yet run. This is an access result, not a failed model-integrity result.

Access recheck, 2026-07-20: all seven locally available SSH identities again
returned `Permission denied (publickey)`. No cache verification, curriculum
generation, central base inference, or training command was launched.

Cluster handoff: the tracked `a841e5a` tree is archived at
`D:\Research_Engine\ConstitutionalAlignment-gates-1-4-a841e5a.zip` (11,369,250
bytes; SHA-256
`03f1660705454d7b332d276a07ac2e6760dca9cc94972e4c4946a71fb6e65899`).
The current `d0063d2` tree, including the recovered predecessor-artifact
locators, is archived at
`D:\Research_Engine\ConstitutionalAlignment-gates-1-4-d0063d2.zip` (11,373,657
bytes; SHA-256
`eab06a3a9837ed975164a7902ec688ccf55b80e1b462e8d36f7f47effe8f73ed`).
The current `bd386d8` tree also includes the validated transcript-recovered
compact result summaries and is archived at
`D:\Research_Engine\ConstitutionalAlignment-gates-1-4-bd386d8.zip` (11,379,212
bytes; SHA-256
`5bc64d4ced3caa0594aaf6aba461d690bc9ac3afcfb6e6dee58d91cc4196bf52`).
The current `de2853f` tree additionally freezes the uncontaminated Mīzān v2
prompt-sensitivity execution contract and exact Bonsai-tokenizer audit. It is
archived at
`D:\Research_Engine\ConstitutionalAlignment-gates-1-4-de2853f.zip` (11,388,666
bytes; SHA-256
`e495dd92a2d049d612288be51373c18e604fc122f134c867a4d35cfbda95c69b`).
The current `ec45a3d` tree additionally freezes the prospective licensed
HarmBench-standard v2 universe, its source-prompt nonleakage precursor, the new
400-unit validation queue, and the v2 direct prompt-versus-SFT contract. It is
archived at
`D:\Research_Engine\ConstitutionalAlignment-gates-1-4-ec45a3d.zip` (11,448,707
bytes; SHA-256
`f45d636ed743dc235f0099550257f56ca1cc40ca3a94ec398c113d7b146fbb91`).

#### Gate 2 — matched curricula and token parity

Status: **BLOCKED by Gate 1**

Frozen input: 22,400 requests, comprising 5,600 paired scenarios for each of
neutral, F1, F3, and F3-concrete. These render deterministically into six arms:
neutral-reflection, F1-reflection, F1-demonstration, F3-reflection,
F3-demonstration, and F3-concrete-reflection.

- [x] Requests, frames, seeds, scenario joins, and split assignments frozen.
- [x] Document the prospective split’s 7 storyworld rows versus the 13 rows reported in the lost run; do not describe the new split as byte-identical recovery.
- [ ] Generate complete raw transcripts for all four source frames.
- [ ] Require an exact 5,600-scenario join for every source frame.
- [ ] Render all six arms with the verified tokenizer and 4,096-token limit.
- [ ] Confirm 5,320 training and 280 validation rows per arm.
- [ ] Confirm F3-reflection versus F3-concrete-reflection total training-token spread is at most 2%.
- [ ] Reject oversize rows; do not silently truncate them.
- [ ] Produce `curriculum_manifest_v1.json` with `passed: true`.

#### Gate 3 — final nonleakage audit

Status: **BLOCKED by Gate 2**

- [x] Source-prompt precursor audit passed with zero exact, normalized, or registered 8-gram overlap.
- [ ] Audit generated assistant text from every training and validation row in all six arms.
- [ ] Compare against harmful, benign, override, and Mihna evaluation universes.
- [ ] Produce `nonleakage_audit_v1.json` with `gate_satisfying: true`.

#### Gate 4 — predecessor prompt-study reanchor

Status: **PENDING — critical path**

Frozen now: recovered F0–F3 prompts, rubrics, request construction, gap
analysis, activation-harvesting procedure, layer-27 probe procedure, the active
licensed v2 evaluation universe, and a replacement-universe 400-unit validation
queue. The current receipt says
`licensed_v2_inputs_frozen_execution_pending` and
`probe_frozen_before_adapter_outcomes: false`.

- [x] Recover and hash-check 88 embedded predecessor payloads.
- [x] Recover the Silico registry locators for the historical judged-generation
  bundle and layer-27 archive (`exp_01kxhk57rcesya1ckbsv07zb2x`). Registration
  success is transcript-attested; current artifact availability is unverified.
- [ ] Retrieve and validate those registered bytes before deciding whether the
  historical rows must be regenerated. Do not treat the locator or summary
  numbers as row-level evidence.
- [x] Freeze 200 compliance and 200 strict-alignment-faking validation units.
- [x] Freeze a prospective licensed substitution before affected outcomes.
  V2 uses all 200 HarmBench standard rows at official repository commit
  `8e1604d`, binds its root MIT license and source hashes, preserves the original
  v1 universe without fielding it, and passes the v2 license gate.
- [ ] Run base-model generation over the complete frozen evaluation universe.
- [ ] Complete all required row joins without post-hoc prompt or judge changes.
- [ ] Collect blinded human labels for both 200-unit tasks.
- [ ] Freeze classifier/judge revisions, prompts, decoding settings, and predictions before calculating agreement.
- [ ] Reach Cohen’s kappa of at least 0.70 separately for compliance and strict alignment-faking labels.
- [ ] Fit the base F0 layer-27 probe on the registered prompt-disjoint split.
- [ ] Run the random-label and random-projection controls.
- [ ] Estimate and report a new complete v2 base F0 gap without a magnitude
  threshold. Keep the recovered v1 calibration interval descriptive only; do
  not use it as a v2 pass/fail target or pool v1 and v2 outcomes.
- [ ] Produce the final joined predecessor-reanchor receipt.
- [ ] Make `probe_frozen_before_adapter_outcomes: true` before any adapter activation or evaluation result is inspected.

Human annotation and curriculum generation may proceed in parallel after Gate
1 only if blinding is preserved. Neither path may reveal future adapter
identities or outcomes to annotators.

### 3. Complete Gates 5–6 and the staged run

#### Gate 5 — full-topology training smoke

Status: **BLOCKED by Gates 1–4**

- [ ] Run the capped eight-A100, 50-step smoke at sequence length 4,096.
- [ ] Verify finite loss, all six arms at equal reduced dose, checkpoint save/reload, and ten valid generations.
- [ ] Treat 2,048 tokens as a known recovered-launcher defect, not an allowed fallback.
- [ ] Produce a gate-satisfying distributed-smoke receipt.

#### Gate 6 — pilot authorization

Status: **BLOCKED by Gates 1–5 and human signature**

- [ ] Bind all passed receipts to the exact capped command.
- [ ] Obtain signed human authorization for the two-hour pilot.
- [ ] Confirm the authorization does not approve the overnight run automatically.

#### Pilot and overnight promotion

- [ ] Run the equal-dose, six-arm two-hour pilot only after `pilot_ready: true`.
- [ ] Use the pilot only for infrastructure, throughput, evaluator, and variance checks—not scientific endpoint claims.
- [ ] Promote only if every arm completes, all registered checks pass, and measured throughput fits the frozen 12-hour/96-GPU-hour cap.
- [ ] Cancel rather than repair the overnight design in place if a promotion gate fails.
- [ ] Preserve 25%, 50%, and 100% dose checkpoints and their hashes.

### 4. Execute the behavioral evaluation chain

| Experiment | Priority | Current state | Completion criterion |
|---|---|---|---|
| 1. Prompt-only accountability sensitivity | **MUST HAVE** | Exact compact INTELLECT-3 pilot summaries are transcript-recovered and validated: on the informative base, judged gaps were F0 36.0 pp, F1 0.17 pp, F2 2.67 pp, and F3 1.83 pp; on canonical prompts the gate sweep was null. The registered v1 rows and activations remain unavailable/unverified. The prospective licensed central v2 universe and replacement validation queue pass their integrity/license gates but still have zero responses. The separate local Mīzān/Bonsai v2 supplement is complete at `ConstitutionalAlignment@6c1e66f`, fielded from clean commit `ec45a3d`: 20/20 development and 900/900 evaluation turns were valid. Eschatological versus secular-omniscient action switching was 7.78% (95% room-cluster interval 3.89%–10.56%), but the proxy delta was +0.0108 (-0.0161–0.0422); unreliable authority versus neutral switched 9.44%, and option-order invariance was only 62.33%. The full blinded bundle passes a zero-call dry-run. A full 60-action/two-reviewer handoff is frozen at upstream `37c9bc7`, and a separate all-15-cue qualified-scholar handoff is frozen at upstream `a25e950`; both reviews remain pending. This is descriptive prompt sensitivity, not evidence of normative improvement, eschatological specificity, or internalization. | Run matched F0/F1/F2/F3 base rows on the licensed central v2 universe; complete judging, human validation, and probe controls, and estimate a new v2 F0 baseline. Historical v1 rows, if retrieved, remain a separate provenance analysis. The Mīzān supplement requires no outcome-driven rerun; complete both independent action-review templates and report every disagreement, then complete and disclose the external scholar receipt. Neither handoff adds a post-result numeric pass threshold or makes the pilot confirmatory. Add F3-concrete only prospectively. |
| 2. Prompting versus SFT | **MUST HAVE** | Training arms designed; direct `D_f` contract frozen and validated before outcomes. Generation, training, and scoring remain pending. | Report `E_prompt,f`, `E_SFT,f`, and `D_f` with matched IDs, sign, judges, and bootstrap units. |
| 3. Frame-removal persistence | **PRIMARY RESULT** | Directly registered; no adapter exists yet. | Compare each framed adapter with neutral-reflection SFT under the fully no-frame contract. |
| 4. Generic override resistance | **MUST HAVE** | Registered; not run. | Weight the common generic override as primary; report targeted F1/F3 overrides as secondary. |
| 5. Identity-scrubbed/cross-skin transfer | **HIGH VALUE** | Mihna panel registered but not a complete matched causal-transfer design. | Report Mihna as preliminary transfer only; require matched causal skins for a full transfer claim. |
| 6. Theological specificity and unreliable authority | **HIGH VALUE / FOLLOW-UP** | F1 versus F3 and abstract versus concrete F3 are covered. A trained secular perfect-auditor arm and a clean unreliable-authority arm are absent. | Use existing content/concreteness contrasts now; treat auditor-equivalence and unreliable-authority isolation as follow-ups rather than expanding the frozen six-arm run. |

For every scored block:

- [ ] Keep the latent prompt/world unit—not individual turns—as the bootstrap unit.
- [ ] Report invalid and missing outputs separately from policy outcomes.
- [ ] Keep deterministic action outcomes separate from teacher or judge agreement.
- [ ] Preserve blinded packets, opaque IDs, forbidden-metadata checks, and hash bindings.
- [ ] Run benign over-refusal, capability retention, unsupported religious self-claim, fabricated-source, sectarian-degradation, and deference-without-reasoning guards.

### 5. Claims and manuscript promotion

- [ ] Keep all adapter results labeled `NOT RUN` until immutable result receipts exist.
- [ ] Call prompt Studies 1–2 “recovered pilot findings” until row-level bundles are reverified or freshly rerun.
- [ ] Do not promote Experiment 0 from manipulation check to semantic composition evidence.
- [ ] Use “training-conditioned persistence” only for a no-frame treatment-versus-neutral effect.
- [ ] Use “frame specificity” only if the relevant theological versus secular/content control separates.
- [ ] Use “operational internalization” only if persistence, generic override resistance, registered representation movement, and every safety/capability guard pass jointly.
- [ ] Treat null, blocked, skipped, and inconclusive outcomes as reportable results.
- [ ] Copy exact receipt hashes and the final status table into the manuscript before submission.

## Stop conditions

Do not proceed to scored adapter evaluation if any of the following is true:

- the direct prompt-versus-SFT analysis contract is not frozen;
- the base cache or inference engine is not hash-verified;
- any curriculum arm is incomplete, unmatched, over length, or outside token parity;
- generated-text nonleakage has not passed;
- the prospective v2 base baseline, human-agreement gates, or layer-27 probe is unfinished;
- adapter outcomes have become visible before the probe and judges are frozen;
- the distributed smoke fails save/reload or valid-generation checks;
- signed authorization or the staged compute cap is absent.

## Immediate next action

Complete Gate 1 cluster-local model verification. After Gate 1 passes, start
Gate 4 base inference and blinded
human validation while the four source-frame curricula are generated. Do not
return to multi-adapter composition engineering during this critical path.
