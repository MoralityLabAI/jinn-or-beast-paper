# Provenance — frame_internalization_sft_v1 readiness

- `pre_spend_readiness_20260717.json`: copied 2026-07-18 from
  `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/readiness/`,
  committed upstream at `e90a8a63`
  (github.com/MoralityLabAI/ConstitutionalAlignment/commit/e90a8a63ec633d982f0c944f1209305d43ea5e54,
  "Freeze frame evaluation, split, and judge gates").

## Status at copy time

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

## Known unresolved issues (must be disclosed, not papered over)

- Harmful-source license unresolved.
- Prospective split's 7-vs-recorded-13 storyworld-row divergence is explicitly
  documented upstream.
