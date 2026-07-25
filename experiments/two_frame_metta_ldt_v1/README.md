# Two-frame MeTTa LDT sorter v1

This bounded experiment asks whether two small, inspectable candidate-lattice
heads can learn two distinct moral-boundary surfaces defined by frozen MeTTa
facts:

- `jinn_erratic_reasoner_v2`
- `beast_optimized_servitor_v2`

The shared candidate universe consists of audited behavioral tags, not raw
prose. Each frame maps the same tagged candidate to one of three lattice
candidates:

```text
{train, hold, reject}
```

The learned head is a model-derived proposal. It may narrow the candidate set
for review, but it cannot hard-admit a row into training. A hard route requires
the exact frozen MeTTa scorer over audited tags. Rows without audited tags,
rows with contradictory tags, and raw-text-only rows go to `hold`.

This is an E4 policy-emulation and data-routing experiment. It does not validate
either frame as theology, morality, or a model persona, and it does not show
that an LDT can infer the tags from natural language.

## Frozen run

The registration is [`registration.json`](registration.json). It fixes:

- source-policy hashes;
- seed `20260725`;
- a joint-balanced 2,304-row universe;
- 1,440/432/432 train/validation/test rows;
- 100 epochs per frame with checkpoints every 10 epochs;
- a 2,048 MB RAM, 50% CPU, 50 MB/s I/O-abort, 120-second local cap;
- the `train >= 0.70`, `reject <= 0.30`, otherwise `hold` boundary;
- singleton proposals only at probability `>= 0.80`; otherwise the top two
  lattice candidates survive.

## Commands

Run deterministic unit tests:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

Run the capped CPU-only experiment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_capped.ps1
```

Sort an audited JSONL file after the canonical run:

```powershell
python src/sort_rows.py `
  --input candidate_rows.jsonl `
  --frame jinn `
  --output-dir outputs/sorted-jinn
```

Input rows require a unique `row_id` and may include `text` plus a `tags` list.
Missing tags route to `hold`; unknown tags fail loudly.

