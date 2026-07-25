# Recent Jinn/Beast Work: 2026-07-21 through 2026-07-25

This is the coordination index for the deadline-week experiment work. It
separates three different kinds of material:

1. paper coordination and claim hygiene in this repository;
2. public, committed experiment code and result packets in
   `ConstitutionalAlignment`;
3. large or private local run packets in `D:\Research_Engine\jinn_or_beast`.

The local shortcuts are Windows junctions under the ignored
`local-collation/` directory. They do not copy data, change the source folders,
or add private reasoning traces and model artifacts to Git.

## Open the local collation

The main local path is:

`C:\projects\jinn-or-beast-paper\local-collation\recent-20260721-20260725`

| Shortcut | Authoritative target |
|---|---|
| `source-constitutional-alignment` | `C:\projects\ConstitutionalAlignment\ConstitutionalAlignment` |
| `source-pixieology` | `C:\projects\Pixieology\Pixieology` |
| `private-all-jinn-or-beast` | `D:\Research_Engine\jinn_or_beast` |
| `latest-v3-memory-ablation` | `D:\Research_Engine\jinn_or_beast\quranic_moral_memory_ablation_qwen35_4b_20260725` |
| `latest-v2-live-village` | `D:\Research_Engine\jinn_or_beast\quranic_moral_live_village_qwen35_4b_20260725` |
| `qwen4b-prime-rl` | `D:\Research_Engine\jinn_or_beast\primelab_jinn_moral_reasoner_v2_20260725` |
| `qwen4b-static-replay` | `D:\Research_Engine\jinn_or_beast\quranic_moral_village_qwen35_4b_replay_20260725` |
| `qwen1p7b-local-reasoner-v2` | `D:\Research_Engine\jinn_or_beast\jinn_bench_qwen3_1p7b_jinn_reasoner_v2` |
| `qwen1p7b-local-qlora-v1` | `D:\Research_Engine\jinn_or_beast\jinn_bench_qwen3_1p7b_qlora_v1` |
| `prior-collation-20260722` | `D:\Research_Engine\jinn_or_beast\collated_20260722` |

If a shortcut is unavailable, use the authoritative target shown in the table.
The tracked `COLLATION_MANIFEST.json` records the same mapping.

## Current public experiment record

The current central source repository is:

`C:\projects\ConstitutionalAlignment\ConstitutionalAlignment`

The deadline-week chain on `main` is:

| Date | Program | Public path / anchor |
|---|---|---|
| 2026-07-21 | Local Qwen3-1.7B MeTTa and QLoRA feasibility screens | `experiments/jinn_bench_v1/`; negative and exploratory recipe evidence |
| 2026-07-22 | Local-data collation and Prime F04/F06 bring-up | collation commit `0f59576`; F04 result `b813e06`; F06 result `7984862` |
| 2026-07-23 | JinnBench constructs, thinking baseline, Prime environment, and local QLoRA trial | `experiments/jinn_beast_metta_rl_v1/`, `experiments/jinn_bench_v1/local_qwen3_1p7b_jinn_qlora_v1/` |
| 2026-07-24 | Qwen3-1.7B Jinn reasoner v2 and Quran-anchored village v1 | `experiments/jinn_bench_v1/local_qwen3_1p7b_jinn_reasoner_v2/`, `experiments/jinn_bench_v1/quranic_moral_village_v1/` |
| 2026-07-25 | Qwen3.5-4B hosted-RL Jinn adapter | `experiments/jinn_beast_metta_rl_v1/moral_reasoner_v2/`; pilot `18fd33e`, final receipt `85bedc7` |
| 2026-07-25 | Live MeTTa Jinn/Beast village v2 | freeze `6b1dc17`, result `00d897c`; `experiments/jinn_bench_v1/quranic_moral_village_v2/` |
| 2026-07-25 | Three-seed role-memory ablation v3 | freeze `83500af`, result `64cb08f`; `experiments/jinn_bench_v1/quranic_moral_village_v3/` |

The v3 experiment is the latest completed live-village package: 12 serial runs,
144 public messages, 144 private reasoning traces, and an estimated Prime
inference cost of `$0.1080036`. Its result is descriptive. The frozen
role/competence ledger prevented the prior technical specialist-overreach
pattern, but generic cross-topic role reuse remained.

## Paper-ready entry points

Start with these files in the `source-constitutional-alignment` shortcut:

- `experiments/jinn_bench_v1/quranic_moral_village_v3/README.md`
- `experiments/jinn_bench_v1/quranic_moral_village_v3/results/editorial_paper_highlights.md`
- `experiments/jinn_bench_v1/quranic_moral_village_v3/results/posthoc_flag_audit.md`
- `experiments/jinn_bench_v1/quranic_moral_village_v3/results/paper_findings.md`
- `experiments/jinn_bench_v1/quranic_moral_village_v3/results/full_transcript.md`
- `experiments/jinn_bench_v1/quranic_moral_village_v3/PRIME_ROLE_MEMORY_ABLATION_TERMINAL_RECEIPT_20260725.json`
- `experiments/jinn_bench_v1/quranic_moral_village_v2/results/paper_findings.md`
- `experiments/jinn_beast_metta_rl_v1/moral_reasoner_v2/`

The complete v3 private archive is available through
`latest-v3-memory-ablation`. Its manifest SHA-256 is
`7b6964cb1b1c35dc3aeb2e777ab48c180093cbd8bb84bcbce15881c5ae31a677`.

## Adjacent Pixie work

The `source-pixieology` shortcut exposes the concurrent Pixie/étale continuation
work. It is adjacent infrastructure and mechanistic exploration, not a
substitute for the Jinn/Beast behavioral evidence. Recent anchors include the
five-dimensional explorer (`ebbe1b3`), bounded LoRA feedback loop (`530b303`),
PrimeLab continuation (`1640a3c`), and successful canary capture (`4670b21`).

## Evidence boundary

- Junction targets remain authoritative; do not edit a copied-looking path
  under `local-collation` without understanding that it edits the target.
- `D:\Research_Engine` packets may contain private reasoning, raw provider
  responses, runtime logs, and adapter artifacts. They are local evidence and
  are intentionally ignored by Git.
- The public result packets preserve their own receipts and hashes. This index
  is a navigation aid, not a new validation or scientific result.
- Continue applying the manuscript claim ladder: no validated theological,
  moral-performance, population, deterministic-provider, or weight-level
  internalization claim follows from the deadline-week runs.
