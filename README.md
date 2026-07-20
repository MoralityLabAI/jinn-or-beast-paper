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
| `protocols/` | `storyworld_internalization_experiment_protocol_v1` (GPT Pro consolidation, docx + markdown conversion) and the current cross-repository [experiment execution checklist](protocols/experiment_execution_checklist_v1.md). |
| `notes/` | Consolidated Silico suggestions and direction (2026-07-16). |
| `evidence/` | Frozen receipts / result bundles copied in as they are verified. Nothing in here may be cited in the paper without a provenance note. |

## Where the experiments live

| Program | Location | Status (2026-07-20) |
|---|---|---|
| exp:1 prompt-level framing A/B (INTELLECT-3) | recovered Silico sessions (`silico_reports/`, `D:\Research_Engine\recovered_silico_sessions_20260716`) | COMPLETED 2026-07-15. Exact compact gate-sweep, four-frame, and layer-27 JSON summaries have now been reconstructed and validated against embedded tool results. The registered row and activation bundles remain unavailable/unverified, so cite as transcript-recovered pilot findings pending retrieval or reanchor. |
| exp:2 frame robustness under stress (11,700 generations) | recovered Silico sessions | COMPLETED 2026-07-16; same artifact-status caveat. |
| exp:3 frame internalization SFT | `ConstitutionalAlignment/experiments/frame_internalization_sft_v1/` | CENTRAL EXPERIMENT. Current upstream `a25e950`; the central freeze/readiness state remains `ec45a3d`: **5 gates passed, 6 compute-blocking gates pending**, `pilot_ready: false`, and no fine-tuning outcome. The active v2 direct prompt-versus-SFT `D_f` contract and prospective licensed HarmBench-standard universe pass. The old F0 interval is descriptive only; a new v2 base baseline, Gate 1 cluster-cache verification, curricula, final nonleakage, human validation/probe freeze, distributed smoke, and authorization remain pending. See the [execution checklist](protocols/experiment_execution_checklist_v1.md). |
| Supplemental Mīzān/Bonsai prompt sensitivity | `ConstitutionalAlignment/experiments/mizan_rooms_v1/` | COMPLETE exploratory run at result commit `6c1e66f`, fielded from clean commit `ec45a3d`: development 20/20 and evaluation 900/900 valid turns. Eschatological versus secular-omniscient action-switch rate was 7.78% (95% room-cluster interval 3.89%–10.56%), while the behavioral-proxy delta was +0.0108 (-0.0161–0.0422). The unreliable-authority control switched 9.44% versus neutral, and option-order invariance was 62.33%. This supports prompt sensitivity on the instrument, not normative improvement, theological specificity, or internalization. The full blinded bundle passes a zero-call dry-run. A 60-action/two-reviewer human-validation handoff is frozen at upstream `37c9bc7`, and an all-15-cue qualified-scholar handoff is frozen at `a25e950`; both external reviews remain pending. Aggregate evidence is in [`evidence/mizan_rooms_v1/`](evidence/mizan_rooms_v1/). |
| Storyworld internalization protocol v1 | `protocols/` here; repo anchor ConstitutionalAlignment commit `48277a6e` | Working protocol from GPT Pro; freeze checklist not yet executed. This is the coordinating design for the prompt-vs-SFT causal chapter. |
| Jinn/Beast multi-agent storyworlds | `Pixieology/experiments/jinn_beast_multiagent_storyworlds/` | Five-cell dyad matrix COMPLETE on relief-ledger seed 23 (2026-07-18): action-level frame convergence (identical profiles all conditions), 2/40 justification turns deviate in frame-predicted directions. UNREVIEWED, nothing adapter-eligible. Receipts in `evidence/jinn_beast_multiagent_storyworlds/`. Next: blind review; harder worlds + adversarial stressors for paper cells. |
| Experiment 0: multi-adapter routing/manipulation validation | `Pixieology/experiments/lora_pixie_village/`, commit `87680cb` | PASS within its boundary: four hash-attested adapter-scale conditions, complete inference, proposal-marker checks, bounded resources, and clean shutdown. This is a manipulation check, not semantic persona retention or adapter-composition evidence. Further composition work is deferred behind the central SFT persistence chain. |
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
