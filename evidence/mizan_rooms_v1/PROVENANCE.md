# Mīzān Rooms v1 local Bonsai result provenance

This directory contains cleared aggregate evidence copied from
`ConstitutionalAlignment@6c1e66f80c19f84854e8ee493cb1ae892707b76f`.
The model outputs were fielded against the clean, tracked package at
`ConstitutionalAlignment@ec45a3dd43d614843868732850ebb465980d1480`.

The completed run contains 15 condition/seed shards, 180 episodes, and 900
turns. All 900 responses were valid strict two-key JSON. The first shard resumed
from nine hash-checked episode receipts after a session interruption; no partial
episode was counted. The run-owned server was stopped, and no run-owned process
remained after validation.

Tracked files:

- `bonsai_1p7b_q1_local_v2_analysis.json`: exact preregistered aggregate
  analysis, SHA-256
  `786e4200c14d6915de936ed4adf463c7ef3cd8b64a135f58b583a79f3949c3d0`.
- `bonsai_1p7b_q1_local_v2_receipt.json`: model, matrix, shard-manifest,
  analysis, and claim-boundary receipt, SHA-256
  `1cf486f5540cf0ad518b58331550954a800a51a3ce17cd182fc5cf82623bba7b`.

Raw transcripts, per-episode files, private blinding maps, and the merged
blinded judge bundle remain outside Git under
`D:\Research_Engine\jinn_or_beast\mizan_bonsai_1p7b_q1_local_v2_ec45a3d`.
Their hashes are bound by the tracked receipt.

This is a supplemental exploratory prompt-sensitivity result. It does not
replace the INTELLECT-3 prompt reanchor, direct prompt-versus-SFT comparison, or
six-arm frame-removal study. Human adjudication and scholar review remain
pending, so the deterministic behavioral proxy is not a normative score.

## Post-result validation handoffs

The 900-row merged blinded bundle passed the existing Constitutional Alignment
judge CLI in dry-run mode: every row digest verified, suite routing covered all
900 rows, and no provider call or judge score was produced. The copied receipt
`bonsai_1p7b_q1_local_v2_blinded_bundle_dry_run.json` has SHA-256
`9a38bc61b848e2d4fb111005e656a35737bdd1bcdd86038da7bd60536d69f7c8`.

The full-action human-validation handoff was generated from the clean source
commit `fdf59bc005fcdf10b98e500625e1613325f11689` and published in
Constitutional Alignment commit `37c9bc7173f8cf92545a5d2a65ef4674edd0a37a`.
Its manifest SHA-256 is
`d0f88bdeee986d61ddeb43d9eeda4dccfc5178b8076ee479b7efd80891739822`.
It includes all 60 actions from all 20 evaluation turns, two independent
reviewer templates, and 600 required dimension scores. The private score/tag
join remains outside Git. The templates are intentionally incomplete and fail
validation until external reviewers fill them; no human or scholar result is
claimed.
