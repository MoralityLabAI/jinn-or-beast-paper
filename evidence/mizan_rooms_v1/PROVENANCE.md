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
