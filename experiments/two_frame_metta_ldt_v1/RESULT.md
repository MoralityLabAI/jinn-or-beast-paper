# Two-frame MeTTa LDT sorter v1 result

Status: **completed, not pilot-ready**.

The canonical capped run trained one additive candidate-lattice head for each
frozen MeTTa frame. Both heads used the same 2,304 audited-tag candidates and
were trained sequentially on CPU for 100 epochs each. The process loaded no GPU
library, peaked at 27.254 MB trainer RAM and 3.258 MB/s trainer I/O, exited with
code zero, and passed owned-process cleanup. All canonical artifact hashes
verify.

## Held-out test result

| Frame | Accuracy | Macro F1 | Candidate coverage | False elimination | Critical reject recall | Opposite-frame invariance | Irrelevant weight |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jinn erratic reasoner | 96.30% | 96.30% | 99.07% | 0.93% | 98.58% | 97.69% | 6.17% |
| Beast optimized servitor | 97.92% | 97.93% | 99.77% | 0.23% | 97.92% | **94.91%** | 7.35% |

Eleven of twelve preregistered frame-level checks passed. Beast
opposite-frame top-lane invariance missed its 95% gate by 0.09 percentage
points, so the fail-closed summary records `pilot_ready: false`.

The post-outcome disagreement audit found that all 22 Beast invariance changes
were exact-policy `hold` rows: the Beast-only features predicted `train`, while
the full union features shifted the learned top lane to the correct `hold`.
This makes the observed nuisance reliance less dangerous than a hard false
admission, but it still violates the registered separability requirement. Jinn
had 10 analogous changes and remained above its gate.

The candidate-lattice safeguard mattered. Jinn made 16 top-lane errors but
excluded the true lane only four times; Beast made nine top-lane errors but
excluded the true lane once. Learned proposals remain `model_sound` and are
never hard-applied.

## Data sort

Because the shared universe is joint-balanced by construction, the exact
MeTTa route produces 768 `train`, 768 `hold`, and 768 `reject` rows under each
frame. Materialized frame-specific JSONL lanes are under:

- `outputs/canonical/sorted/jinn/`
- `outputs/canonical/sorted/beast/`

These are tagged policy-emulation rows, not adapter-ready natural-language
examples. A raw-text row without audited tags goes to `hold`. An audited row is
hard-routed only by the exact frozen scorer; the learned head supplies a soft
candidate set for review.

## What this teaches us

The useful positive result is architectural: a very small, interpretable head
can recover two distinct MeTTa-defined boundary surfaces from a shared input
universe with high held-out coverage, no GPU, and low resource cost.

The important negative result is that merely exposing each head to the union of
both frames leaves small cross-frame nuisance weights, even when the exact
label depends only on the selected frame. The clean next registered repair is a
frame-owned feature mask or an explicit invariance penalty. That repair should
be evaluated prospectively on the same sealed test rows; the 95% threshold
should not be relaxed after seeing this result.

This experiment does not show natural-language moral understanding, validate
the frames normatively or theologically, or authorize automatic adapter-data
admission.

