from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[3]
LDT_RELATIVE_ROOT = Path("experiments/two_frame_metta_ldt_v1")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class FrameBundle:
    alias: str
    policy: Any
    model: Any
    feature_names: tuple[str, ...]
    universe: frozenset[str]
    boundary: Mapping[str, Any]
    model_config: Mapping[str, Any]
    registration_sha256: str


def _load_ldt_module(repo_root: Path) -> Any:
    source = repo_root / LDT_RELATIVE_ROOT / "src"
    if not source.is_dir():
        raise FileNotFoundError(f"missing registered LDT source: {source}")
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    import ldt_experiment

    return ldt_experiment


def load_frame_bundle(repo_root: Path, frame: str) -> FrameBundle:
    if frame not in {"jinn", "beast"}:
        raise ValueError("frame must be jinn or beast")
    ldt = _load_ldt_module(repo_root)
    root = repo_root / LDT_RELATIVE_ROOT
    registration_path = root / "registration.json"
    registration = json.loads(registration_path.read_text(encoding="utf-8"))
    policies = {}
    for alias, config in registration["frames"].items():
        path = root / config["policy_path"]
        if sha256_file(path) != config["snapshot_sha256"]:
            raise ValueError(f"{alias} policy snapshot hash mismatch")
        policies[alias] = ldt.parse_policy(path)
    universe = frozenset().union(*(policy.tags for policy in policies.values()))
    model_path = root / "outputs" / "canonical" / "models" / f"{frame}.json"
    model = ldt.AdditiveCandidateHead.from_jsonable(
        json.loads(model_path.read_text(encoding="utf-8"))
    )
    manifest = json.loads(
        (root / "outputs" / "canonical" / "artifact_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    expected_model_hash = manifest[f"models/{frame}.json"]
    if sha256_file(model_path) != expected_model_hash:
        raise ValueError(f"{frame} LDT model hash mismatch")
    return FrameBundle(
        alias=frame,
        policy=policies[frame],
        model=model,
        feature_names=tuple(model.feature_names),
        universe=universe,
        boundary=registration["boundary_contract"],
        model_config=registration["model"],
        registration_sha256=sha256_file(registration_path),
    )


def validate_task(task: Mapping[str, Any], universe: frozenset[str]) -> None:
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        raise ValueError("task requires a non-empty task_id")
    if not isinstance(task.get("prompt"), str) or not task["prompt"].strip():
        raise ValueError(f"{task_id}: prompt must be non-empty")
    actions = task.get("actions")
    if not isinstance(actions, list) or len(actions) < 2:
        raise ValueError(f"{task_id}: at least two actions are required")
    ids = []
    for action in actions:
        if not isinstance(action, dict):
            raise ValueError(f"{task_id}: every action must be an object")
        action_id = action.get("action_id")
        if not isinstance(action_id, str) or not action_id:
            raise ValueError(f"{task_id}: action requires action_id")
        ids.append(action_id)
        if not isinstance(action.get("text"), str) or not action["text"].strip():
            raise ValueError(f"{task_id}:{action_id}: action text is required")
        tags = action.get("tags")
        if not isinstance(tags, list) or not all(
            isinstance(tag, str) and tag for tag in tags
        ):
            raise ValueError(f"{task_id}:{action_id}: tags must be strings")
        unknown = sorted(set(tags).difference(universe))
        if unknown:
            raise ValueError(f"{task_id}:{action_id}: unknown tags {unknown}")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{task_id}: duplicate action IDs")


def _rotation_offset(task_id: str, frame: str, count: int) -> int:
    if count < 2:
        raise ValueError("shuffle requires at least two actions")
    digest = hashlib.sha256(f"{task_id}|{frame}|shuffled-v1".encode()).digest()
    return 1 + int.from_bytes(digest[:4], "big") % (count - 1)


def inspect_task(
    task: Mapping[str, Any],
    *,
    frame: str,
    mode: str,
    repo_root: Path = DEFAULT_REPO_ROOT,
) -> dict[str, Any]:
    if mode not in {"none", "matched", "shuffled"}:
        raise ValueError("mode must be none, matched, or shuffled")
    ldt = _load_ldt_module(repo_root)
    bundle = load_frame_bundle(repo_root, frame)
    validate_task(task, bundle.universe)
    actions = list(task["actions"])
    original_tags = [list(action["tags"]) for action in actions]
    scored_tags = original_tags
    shuffle_offset = None
    if mode == "shuffled":
        shuffle_offset = _rotation_offset(task["task_id"], frame, len(actions))
        scored_tags = [
            original_tags[(index - shuffle_offset) % len(actions)]
            for index in range(len(actions))
        ]

    receipts = {}
    survivors = []
    for index, (action, tags) in enumerate(zip(actions, scored_tags)):
        exact = ldt.score_policy(
            tags,
            bundle.policy,
            allowed_universe=bundle.universe,
            train_minimum=float(bundle.boundary["train_minimum_score"]),
            reject_maximum=float(bundle.boundary["reject_maximum_score"]),
        )
        probabilities = bundle.model.probabilities(
            ldt.vectorize(tags, bundle.feature_names)
        )
        soft_candidates = ldt.candidate_lanes(
            probabilities,
            singleton_threshold=float(
                bundle.model_config["candidate_singleton_probability"]
            ),
            otherwise_top_k=int(bundle.model_config["otherwise_keep_top_k"]),
        )
        removed = mode != "none" and exact["lane"] == "reject"
        if not removed:
            survivors.append(action["action_id"])
        receipts[action["action_id"]] = {
            "exact_policy": exact,
            "ldt_soft_proposal": {
                "candidate_lanes": soft_candidates,
                "probabilities": {
                    lane: round(probabilities[index], 8)
                    for index, lane in enumerate(ldt.LANES)
                },
                "soundness": "model_sound",
                "hard_applied": False,
            },
            "removed": removed,
            "scored_tags_source_action": (
                actions[(index - (shuffle_offset or 0)) % len(actions)][
                    "action_id"
                ]
            ),
        }
    return {
        "schema_version": "jinn_beast_membrane_task_receipt_v1",
        "task_id": task["task_id"],
        "frame": frame,
        "mode": mode,
        "registration_sha256": bundle.registration_sha256,
        "shuffle_offset": shuffle_offset,
        "surviving_action_ids": survivors,
        "actions": receipts,
    }


def evaluate_proposal(
    task: Mapping[str, Any],
    *,
    frame: str,
    mode: str,
    proposal_action_id: str | None,
    repo_root: Path = DEFAULT_REPO_ROOT,
) -> dict[str, Any]:
    receipt = inspect_task(task, frame=frame, mode=mode, repo_root=repo_root)
    legal_ids = {action["action_id"] for action in task["actions"]}
    valid = proposal_action_id in legal_ids
    survives = proposal_action_id in receipt["surviving_action_ids"]
    if valid and survives:
        decision = "accept"
        reason = "proposal_survives_candidate_lattice"
    elif not receipt["surviving_action_ids"]:
        decision = "abstain"
        reason = "candidate_lattice_is_bottom"
    else:
        decision = "revise"
        reason = (
            "malformed_or_unknown_action"
            if not valid
            else "proposal_removed_by_exact_policy"
        )
    return {
        **receipt,
        "proposal_action_id": proposal_action_id,
        "proposal_valid": valid,
        "proposal_survives": survives,
        "membrane_decision": decision,
        "membrane_reason": reason,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--frame", choices=("jinn", "beast"), required=True)
    parser.add_argument("--mode", choices=("none", "matched", "shuffled"), required=True)
    parser.add_argument("--proposal", default=None)
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    args = parser.parse_args()
    task = json.loads(args.task.read_text(encoding="utf-8"))
    value = (
        evaluate_proposal(
            task,
            frame=args.frame,
            mode=args.mode,
            proposal_action_id=args.proposal,
            repo_root=args.repo_root,
        )
        if args.proposal is not None
        else inspect_task(
            task,
            frame=args.frame,
            mode=args.mode,
            repo_root=args.repo_root,
        )
    )
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
