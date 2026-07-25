from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ldt_experiment import (
    AdditiveCandidateHead,
    candidate_lanes,
    parse_policy,
    read_jsonl,
    score_policy,
    sha256_file,
    vectorize,
    write_json,
    write_jsonl,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--frame", choices=("jinn", "beast"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--registration", type=Path, default=ROOT / "registration.json")
    parser.add_argument("--model-dir", type=Path, default=ROOT / "outputs" / "canonical" / "models")
    args = parser.parse_args()

    registration = json.loads(args.registration.read_text(encoding="utf-8"))
    frame_config = registration["frames"][args.frame]
    policy_path = ROOT / frame_config["policy_path"]
    if sha256_file(policy_path) != frame_config["snapshot_sha256"]:
        raise ValueError("policy hash does not match the frozen registration")
    policy = parse_policy(policy_path)
    all_policies = [
        parse_policy(ROOT / value["policy_path"])
        for value in registration["frames"].values()
    ]
    universe = frozenset().union(*(item.tags for item in all_policies))
    model_value = json.loads(
        (args.model_dir / f"{args.frame}.json").read_text(encoding="utf-8")
    )
    model = AdditiveCandidateHead.from_jsonable(model_value)
    boundary = registration["boundary_contract"]
    model_config = registration["model"]

    source_rows = read_jsonl(args.input)
    seen: set[str] = set()
    routed: dict[str, list[dict[str, Any]]] = {lane: [] for lane in ("train", "hold", "reject")}
    for row_number, row in enumerate(source_rows, 1):
        row_id = row.get("row_id")
        if not isinstance(row_id, str) or not row_id:
            raise ValueError(f"input row {row_number} requires a non-empty row_id")
        if row_id in seen:
            raise ValueError(f"duplicate row_id: {row_id}")
        seen.add(row_id)
        tags = row.get("tags")
        if tags is None:
            exact = {
                "score": 0.5,
                "lane": "hold",
                "relevant_tags": [],
                "critical_hits": [],
                "annotation_conflicts": [],
                "route_soundness": "unknown",
                "route_reason": "missing_audited_tags",
            }
            probabilities = None
            candidates = ["hold"]
        else:
            if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                raise ValueError(f"{row_id}: tags must be a list of strings")
            exact = score_policy(
                tags,
                policy,
                allowed_universe=universe,
                train_minimum=float(boundary["train_minimum_score"]),
                reject_maximum=float(boundary["reject_maximum_score"]),
            )
            probabilities = model.probabilities(vectorize(tags, model.feature_names))
            candidates = candidate_lanes(
                probabilities,
                singleton_threshold=float(model_config["candidate_singleton_probability"]),
                otherwise_top_k=int(model_config["otherwise_keep_top_k"]),
            )
        routed_row = {
            **row,
            "routing": {
                "frame": args.frame,
                "exact_policy": exact,
                "ldt_soft_proposal": {
                    "candidate_lanes": candidates,
                    "probabilities": (
                        {
                            lane: round(probabilities[index], 8)
                            for index, lane in enumerate(("train", "hold", "reject"))
                        }
                        if probabilities is not None
                        else None
                    ),
                    "soundness": "model_sound",
                    "hard_applied": False,
                },
                "final_lane": exact["lane"],
                "final_lane_authority": exact["route_soundness"],
            },
        }
        routed[exact["lane"]].append(routed_row)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for lane, rows in routed.items():
        write_jsonl(args.output_dir / f"{lane}.jsonl", rows)
    resolved_source = args.input.resolve()
    try:
        source_label = resolved_source.relative_to(ROOT).as_posix()
    except ValueError:
        source_label = resolved_source.as_posix()
    manifest = {
        "schema_version": "two_frame_metta_ldt_sort_manifest_v1",
        "frame": args.frame,
        "source": source_label,
        "source_sha256": sha256_file(args.input),
        "rows": len(source_rows),
        "lane_counts": {lane: len(rows) for lane, rows in routed.items()},
        "hard_route_requires_audited_tags": True,
        "learned_proposals_are_soft_only": True,
    }
    write_json(args.output_dir / "manifest.json", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
