# Jinn or Beast? — Paper Repository

Coordination repo for the AI-and-religion conference paper:

> **Jinn or Beast? Theological Identity Frames as Alignment Surfaces in Small
> Language Models**

The experimental assets live in two sibling repos plus local run archives. This
repo holds the manuscript, the coordinating experiment protocol, and the
evidence-status ledger, so the paper is no longer split between
`Pixieology` and `ConstitutionalAlignment`.

Deadline anchor: ≈ 2026-07-25 (nine days from the 2026-07-16 consolidation).

## Layout

| Path | Contents |
|---|---|
| `paper/` | Manuscript drafts. `abstract_svp_v0_promissory.md` is the original promissory SVP abstract, kept for provenance; the draft supersedes it. |
| `protocols/` | `storyworld_internalization_experiment_protocol_v1` (GPT Pro consolidation, docx + markdown conversion) — the coordinating experiment suite for the prompt-vs-SFT internalization program. |
| `notes/` | Consolidated Silico suggestions and direction (2026-07-16). |
| `evidence/` | Frozen receipts / result bundles copied in as they are verified. Nothing in here may be cited in the paper without a provenance note. |

## Where the experiments live

| Program | Location | Status (2026-07-17) |
|---|---|---|
| exp:1 prompt-level framing A/B (INTELLECT-3) | recovered Silico sessions (`silico_reports/`, `D:\Research_Engine\recovered_silico_sessions_20260716`) | COMPLETED 2026-07-15; **result bundles not recovered** — only chat-relayed numbers. Cite as recovered pilot findings with transcript provenance, or rerun slim. |
| exp:2 frame robustness under stress (11,700 generations) | recovered Silico sessions | COMPLETED 2026-07-16; same artifact-status caveat. |
| exp:3 frame internalization SFT | `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/` | INTERRUPTED, payloads lost; recovered rerun protocol drafted. Pre-spend readiness (2026-07-17, upstream commit `e90a8a63`): **4 gates passed** (governance integrity, split freeze 5,600/zero-overlap, evaluation seal 200+100+150 prompts, blinded-judge dry-run 100%), **6 blocking pending**; `pilot_ready: false`, GPU fail-closed. Scholar review pending — non-blocking for compute but paper disclosure required. Harmful-source license unresolved; 7-vs-13 storyworld-row split divergence documented. Receipt in `evidence/frame_internalization_sft_v1/`. Present registered-report style. |
| Storyworld internalization protocol v1 | `protocols/` here; repo anchor ConstitutionalAlignment commit `48277a6e` | Working protocol from GPT Pro; freeze checklist not yet executed. This is the coordinating design for the prompt-vs-SFT causal chapter. |
| Jinn/Beast multi-agent storyworlds | `Pixieology/experiments/jinn_beast_multiagent_storyworlds/` | Five-cell dyad matrix COMPLETE on relief-ledger seed 23 (2026-07-18): action-level frame convergence (identical profiles all conditions), 2/40 justification turns deviate in frame-predicted directions. UNREVIEWED, nothing adapter-eligible. Receipts in `evidence/jinn_beast_multiagent_storyworlds/`. Next: blind review; harder worlds + adversarial stressors for paper cells. |
| Bonsai 1.7B QLoRA → Q1 transport | `Pixieology/experiments/bonsai_1p7b_q1_lora_feasibility/` | Transport proven; behavioral gate RED (undertrained smoke recipe). |
| LoRA Pixies persona molding (product line) | `D:\Research_Engine\runs\pixie_molding_20260717\` | BLOCKED at preregistered thermal gate (GPU 87 °C > 80 °C); infrastructure gates all passed; no training results. Separate program — not paper evidence. |

## Standing claim-hygiene rules

1. No exp:1/exp:2 number enters the manuscript without its provenance label
   (recovered pilot finding vs. verified bundle vs. fresh rerun).
2. Null, skipped, blocked, and inconclusive outcomes are first-class results.
3. The paper tests theological frames as **training interventions**, never
   whether a model literally is a jinn or the Beast; the Dabbat al-Ard reading
   is one theological interpretation and must be flagged as such.
4. Follow the claim ladder in `protocols/` §1 and the defensible-language list
   in §10; the claims-to-avoid list is binding.
5. Quarantine the overclaiming nested README in `constitutional-harness/`
   before anything is submitted.
