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
- `pilot_ready: false`; no adapter result exists.
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

## Known unresolved issues (must be disclosed, not papered over)

- Harmful-source license unresolved.
- Prospective split's 7-vs-recorded-13 storyworld-row divergence is explicitly
  documented upstream.
