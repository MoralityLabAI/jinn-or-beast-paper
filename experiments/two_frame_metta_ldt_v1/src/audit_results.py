from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from ldt_experiment import (
    LANES,
    AdditiveCandidateHead,
    parse_policy,
    read_jsonl,
    sha256_file,
    vectorize,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]


def counter_rows(counter: Counter[tuple[str, ...]]) -> list[dict[str, Any]]:
    return [
        {"key": list(key), "count": count}
        for key, count in sorted(counter.items())
    ]


def top_lane(probabilities: list[float]) -> str:
    return LANES[max(range(len(LANES)), key=lambda index: probabilities[index])]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration", type=Path, default=ROOT / "registration.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "canonical")
    args = parser.parse_args()

    registration = json.loads(args.registration.read_text(encoding="utf-8"))
    policies = {
        alias: parse_policy(ROOT / config["policy_path"])
        for alias, config in registration["frames"].items()
    }
    rows = read_jsonl(args.output_dir / "shared_candidates.jsonl")
    test_rows = [row for row in rows if row["split"] == "test"]
    predictions = read_jsonl(args.output_dir / "heldout_predictions.jsonl")

    audit: dict[str, Any] = {
        "schema_version": "two_frame_metta_ldt_disagreement_audit_v1",
        "analysis_status": "post_outcome_descriptive",
        "frames": {},
    }
    for frame in ("jinn", "beast"):
        model = AdditiveCandidateHead.from_jsonable(
            json.loads(
                (args.output_dir / "models" / f"{frame}.json").read_text(
                    encoding="utf-8"
                )
            )
        )
        own_tags = policies[frame].tags
        nuisance_changes = []
        transition_counts: Counter[tuple[str, ...]] = Counter()
        nuisance_tag_counts: Counter[str] = Counter()
        for row in test_rows:
            full_probabilities = model.probabilities(
                vectorize(row["tags"], model.feature_names)
            )
            own_only = [tag for tag in row["tags"] if tag in own_tags]
            own_probabilities = model.probabilities(
                vectorize(own_only, model.feature_names)
            )
            full_top = top_lane(full_probabilities)
            own_top = top_lane(own_probabilities)
            if full_top == own_top:
                continue
            truth = row["labels"][frame]["lane"]
            opposite_only = sorted(set(row["tags"]).difference(own_tags))
            transition_counts[(truth, own_top, full_top)] += 1
            nuisance_tag_counts.update(opposite_only)
            nuisance_changes.append(
                {
                    "row_id": row["row_id"],
                    "truth_lane": truth,
                    "own_features_top_lane": own_top,
                    "full_features_top_lane": full_top,
                    "opposite_only_tags": opposite_only,
                }
            )

        frame_predictions = [
            row
            for row in predictions
            if row["frame"] == frame and row["split"] == "test"
        ]
        errors = [row for row in frame_predictions if row["top_lane"] != row["truth_lane"]]
        false_eliminations = [
            row
            for row in frame_predictions
            if row["truth_lane"] not in row["candidate_lanes"]
        ]
        error_counts = Counter(
            (row["truth_lane"], row["top_lane"]) for row in errors
        )
        false_elimination_counts = Counter(
            (row["truth_lane"], row["top_lane"]) for row in false_eliminations
        )
        irrelevant_features = []
        for feature_index, feature in enumerate(model.feature_names):
            if feature in own_tags:
                continue
            weights = [
                model.weights[class_index][feature_index]
                for class_index in range(len(LANES))
            ]
            irrelevant_features.append(
                {
                    "feature": feature,
                    "class_weights": {
                        lane: round(weights[index], 8)
                        for index, lane in enumerate(LANES)
                    },
                    "weight_range": round(max(weights) - min(weights), 8),
                }
            )
        irrelevant_features.sort(
            key=lambda value: (-value["weight_range"], value["feature"])
        )
        audit["frames"][frame] = {
            "test_rows": len(test_rows),
            "top_lane_errors": len(errors),
            "top_lane_error_transitions": counter_rows(error_counts),
            "false_eliminations": len(false_eliminations),
            "false_elimination_transitions": counter_rows(
                false_elimination_counts
            ),
            "false_elimination_rows": false_eliminations,
            "opposite_frame_top_lane_changes": len(nuisance_changes),
            "opposite_frame_transitions": counter_rows(transition_counts),
            "opposite_only_tag_frequency_in_changed_rows": [
                {"tag": tag, "count": count}
                for tag, count in nuisance_tag_counts.most_common()
            ],
            "changed_rows": nuisance_changes,
            "largest_irrelevant_feature_weight_ranges": irrelevant_features[:10],
        }

    write_json(args.output_dir / "disagreement_audit.json", audit)

    excluded = {
        "final_manifest.json",
        "owned_pid.json",
        "stderr.log",
        "stdout.log",
    }
    artifact_rows = []
    for path in sorted(args.output_dir.rglob("*")):
        if not path.is_file() or path.name in excluded:
            continue
        artifact_rows.append(
            {
                "path": path.relative_to(args.output_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    write_json(
        args.output_dir / "final_manifest.json",
        {
            "schema_version": "two_frame_metta_ldt_final_manifest_v1",
            "artifacts": artifact_rows,
            "artifact_count": len(artifact_rows),
            "total_bytes": sum(row["bytes"] for row in artifact_rows),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

