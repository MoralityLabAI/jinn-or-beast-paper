from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ldt_experiment import (  # noqa: E402
    AdditiveCandidateHead,
    build_joint_balanced_dataset,
    candidate_lanes,
    parse_policy,
    score_policy,
)


class TwoFrameLdtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registration = json.loads(
            (ROOT / "registration.json").read_text(encoding="utf-8")
        )
        cls.policies = {
            alias: parse_policy(ROOT / value["policy_path"])
            for alias, value in cls.registration["frames"].items()
        }
        cls.universe = frozenset().union(
            *(policy.tags for policy in cls.policies.values())
        )

    def test_policy_snapshots_match_registration(self) -> None:
        for alias, policy in self.policies.items():
            expected = self.registration["frames"][alias]
            self.assertEqual(policy.benchmark_id, expected["benchmark_id"])
            self.assertEqual(policy.source_sha256, expected["snapshot_sha256"])
            self.assertAlmostEqual(sum(policy.dimensions.values()), 1.0)

    def test_critical_tags_force_reject(self) -> None:
        boundary = self.registration["boundary_contract"]
        for alias, policy in self.policies.items():
            critical = sorted(policy.critical_tags)[0]
            result = score_policy(
                [critical],
                policy,
                allowed_universe=self.universe,
                train_minimum=boundary["train_minimum_score"],
                reject_maximum=boundary["reject_maximum_score"],
            )
            self.assertEqual(result["lane"], "reject", alias)
            self.assertLessEqual(result["score"], policy.critical_cap)

    def test_conflicting_dimension_annotations_hold(self) -> None:
        policy = self.policies["jinn"]
        result = score_policy(
            ["revise_on_material_evidence", "persist_despite_disconfirming_evidence"],
            policy,
            allowed_universe=self.universe,
            train_minimum=0.7,
            reject_maximum=0.3,
        )
        self.assertEqual(result["lane"], "hold")
        self.assertEqual(result["route_soundness"], "unknown")
        self.assertEqual(result["annotation_conflicts"], ["evidence_responsive_revision"])

    def test_small_dataset_is_joint_balanced_and_deterministic(self) -> None:
        kwargs = {
            "seed": 20260725,
            "split_counts": {"train": 3, "validation": 2, "test": 1},
            "train_minimum": 0.7,
            "reject_maximum": 0.3,
        }
        left, features_left = build_joint_balanced_dataset(self.policies, **kwargs)
        right, features_right = build_joint_balanced_dataset(self.policies, **kwargs)
        self.assertEqual(left, right)
        self.assertEqual(features_left, features_right)
        self.assertEqual(len(left), 54)
        cells = {}
        for row in left:
            key = (
                row["joint_label"]["jinn"],
                row["joint_label"]["beast"],
                row["split"],
            )
            cells[key] = cells.get(key, 0) + 1
            self.assertFalse(row["labels"]["jinn"]["annotation_conflicts"])
            self.assertFalse(row["labels"]["beast"]["annotation_conflicts"])
        self.assertEqual(len(cells), 27)

    def test_candidate_lattice_abstains_to_top_two_below_threshold(self) -> None:
        self.assertEqual(
            candidate_lanes(
                [0.45, 0.35, 0.20],
                singleton_threshold=0.8,
                otherwise_top_k=2,
            ),
            ["train", "hold"],
        )
        self.assertEqual(
            candidate_lanes(
                [0.05, 0.05, 0.90],
                singleton_threshold=0.8,
                otherwise_top_k=2,
            ),
            ["reject"],
        )

    def test_model_round_trip_preserves_soft_soundness(self) -> None:
        model = AdditiveCandidateHead.initialized(("a", "b"), seed=7)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.json"
            path.write_text(json.dumps(model.to_jsonable()), encoding="utf-8")
            value = json.loads(path.read_text(encoding="utf-8"))
            loaded = AdditiveCandidateHead.from_jsonable(value)
        self.assertEqual(model.feature_names, loaded.feature_names)
        self.assertEqual(value["proposal_soundness"], "model_sound")


if __name__ == "__main__":
    unittest.main()
