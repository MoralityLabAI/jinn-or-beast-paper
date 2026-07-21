# Provenance — frame_internalization_sft_v1 readiness

- `pre_spend_readiness_20260717.json`: copied 2026-07-18 from
  `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/readiness/`,
  committed upstream at `e90a8a63`
  (github.com/MoralityLabAI/ConstitutionalAlignment/commit/e90a8a63ec633d982f0c944f1209305d43ea5e54,
  "Freeze frame evaluation, split, and judge gates").
- `pre_spend_readiness_20260719_v2.json`: copied 2026-07-19 from the same
  experiment package at Constitutional Alignment commit
  `a841e5a4da5552dea614f9b4aef8fa933705afa8` ("Freeze direct
  prompt-versus-SFT contrast"). Copied file SHA-256:
  `2caaa7327e8927c82f674bedf236c57addcc63d1b0a33467b5bcc0280bff7bb6`.
- `predecessor_artifact_registry_recovery_v1.json`: copied 2026-07-19 from
  Constitutional Alignment commit
  `d0063d26c54e99327100872a3cd99bf530588e68` ("Recover predecessor artifact
  registry locators"). Copied file SHA-256:
  `43f3a86b865f995fc72d7d799c2428a2a1b1d68e8dec44fcf0449907b6a24b68`.
  It records transcript-attested registry paths only; current artifact
  availability and bytes are unverified, so it is not a gate receipt.
- `transcript_recovered_summaries/`: copied 2026-07-19 from Constitutional
  Alignment commit `bd386d8b643a2671a69c34556afac1554a7b8569` ("Recover
  predecessor result summaries"). Its recovery-manifest SHA-256 is
  `a86ce2296d5acd419414f1ba172b8c5b09a68dbd1882f52c5afd3fe03df87bd4`.
  The gate-sweep, master-result, and internals JSON values were structurally
  checked against exact embedded tool-result JSON. This is validated
  transcript reconstruction, not row-level reanchor evidence.
- `qwen3_1p7b_execution_substitution_20260720.json`: coordination receipt
  recorded 2026-07-21 from Constitutional Alignment commit
  `f69f842234e2f81a0d4ac7ae9cbde0ba090ceaf7` ("Publish Qwen3 local Gate 1
  receipts"). It binds the active official `Qwen/Qwen3-1.7B` revision, the
  22,400-request replacement pack, and the passed local model/tokenizer/runtime
  subgate. The upstream local-freeze receipt SHA-256 is
  `fc0f5bbb33bd2b345e9b3043d38d94d0258f67bab333cded4895ada0fafd9433`.
  This does not claim the separate PrimeLab environment/full-topology gate has
  passed and contains no scored behavioral or adapter outcome.
- `qwen3_1p7b_metta_local_screen_result_20260721.json`: coordination receipt
  recorded 2026-07-21 from Constitutional Alignment commit
  `a91342d2a5ad64c1a58ce8ab4998c1efa0484f64` ("Record local MeTTa
  worldview screen result"). Its source receipt SHA-256 is
  `94cbc13132f196ca0cb6390364659e8abe6d7643227c27f7fb1ee09799296243`.
  The separate screen was frozen prospectively at `f7cb86d`, completed 30 local
  QLoRA steps and paired 56-probe base/adapter evaluations, passed its
  infrastructure rule, and failed its predeclared flavored and guided worldview
  rules. It is development-only and does not replace or partially complete the
  registered six-arm experiment.

## Status at copy time

Current receipt (`pre_spend_readiness_20260719_v2.json`):

- Passed gates (5): the four gates below plus
  `direct_prompt_sft_analysis_contract`. The new matched one-sample contract
  binds F0/F1/F3/F3-concrete prompt hashes, the six SFT-arm mapping, one shared
  200-prompt universe, tiers, decoding, paired seeds, joins, judges, and 10,000
  prompt-bootstrap draws.
- Blocking gates remain 6: base model/tokenizer cache verification, matched
  curricula/token parity, generated-text nonleakage, predecessor reanchor,
  distributed 4,096-token smoke, and pilot authorization.
- `pilot_ready: false`; no registered adapter result existed at that receipt freeze.
- Validation at the anchored commit: 86 Python tests passed. The exact tracked
  tree is also preserved as
  `D:\Research_Engine\ConstitutionalAlignment-gates-1-4-a841e5a.zip`
  (11,369,250 bytes; SHA-256
  `03f1660705454d7b332d276a07ac2e6760dca9cc94972e4c4946a71fb6e65899`).

Earlier receipt (`pre_spend_readiness_20260717.json`):

- Passed gates (4): `governance_v2_integrity` (all eight hash bindings valid,
  F3/F3_concrete card token spread 0.0156 vs 0.02 max, guard-launcher dry run
  passed), `split_freeze` (5,600 scenarios, 5,320/280, zero cluster overlap),
  `evaluation_seal` (200 harmful / 100 benign / 150 override prompts, recovered
  hashes match), `blinded_judge_synthetic_dry_run` (five suites, 100%
  pass/fail/malformed parsing).
- Blocking gates pending (6): base_model_tokenizer_freeze,
  matched_curriculum_and_token_parity, nonleakage_audit, predecessor_reanchor,
  distributed_4096_training_smoke, pilot_human_authorization.
- `scholar_review_claim_gate`: pending, non-blocking for compute, but
  **paper disclosure required**.
- `pilot_ready: false`; GPU execution fail-closed.
- Validation at commit: 87 Python tests, 24 harness tests, TypeScript checks.

## Active Qwen execution substitution (2026-07-20)

Silico and its INTELLECT-3 cache are no longer the executable path. New work is
prospectively retargeted to official `Qwen/Qwen3-1.7B` revision
`70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`. The six arms, 5,600 dilemmas,
licensed v2 evaluation universe, 4,096-token sequences, two-epoch dose, paired
estimands, nonleakage rules, validation gates, and safety/capability guards are
preserved. The historical INTELLECT artifacts and the readiness receipts above
remain immutable provenance; they are not Qwen results.

The local freeze verifies 12 artifacts, the official thinking and nonthinking
template behavior, NF4 loading, and deterministic unscored inference. Complete
curriculum generation, the exact PrimeLab environment/hardware freeze, the
4,096-token 50-step-per-arm smoke, prospective Qwen base reanchor and layer-27
probe, human authorization, training, and evaluation remain pending.

## Separate local MeTTa worldview screen (2026-07-21)

Before observing screen outputs, the upstream repository froze a MeTTa-file-
backed skill, scale, interference, and commutator model; a 56-probe development
suite; and a 30-step Qwen3-1.7B QLoRA contract. The exact local run completed on
the 4 GB RTX 3050 without model offload. Both base and adapter produced all 56
outputs. Adapter valid-action rate was 0.982, factual accuracy remained 0.500,
and factual persona leakage remained zero.

The adapter did not increase no-cue worldview markers, and its MeTTa-derived
preferred-proxy rate fell from 0.833 to 0.750. Cross-variant action stability
rose from 0.167 to 0.250, but the only no-cue action switch moved away from the
evaluation proxy. The flavored and guided screens therefore failed. The result
supports another inexpensive, prospectively amended local intervention before
larger-model spending; it is not a general 1.7B capacity verdict. The derivation
path is a Python MeTTa bridge, not native Hyperon proof execution.

## Known unresolved issues (must be disclosed, not papered over)

- The historical v1 harmful-source license is unresolved; the active prospective
  v2 HarmBench-standard universe passed its pinned MIT-license gate.
- Prospective split's 7-vs-recorded-13 storyworld-row divergence is explicitly
  documented upstream.
- The local Qwen receipt does not authorize a different PrimeLab environment;
  its exact GPU and environment lock must be frozen and smoke-tested separately.
