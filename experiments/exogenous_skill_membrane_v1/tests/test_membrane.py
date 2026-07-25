from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_SCRIPTS = REPO_ROOT / "skills" / "govern-jinn-beast-agents" / "scripts"
if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

from membrane import evaluate_proposal, inspect_task


class MembraneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        tasks_path = (
            REPO_ROOT
            / "experiments"
            / "exogenous_skill_membrane_v1"
            / "prepared"
            / "tasks.jsonl"
        )
        cls.tasks = [
            json.loads(line)
            for line in tasks_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_task_deck_shape(self) -> None:
        self.assertEqual(len(self.tasks), 12)
        self.assertTrue(all(len(task["actions"]) == 3 for task in self.tasks))

    def test_matched_membrane_removes_joint_reject(self) -> None:
        for task in self.tasks:
            for frame in ("jinn", "beast"):
                rejected = task["fixture_proposals"][frame][0]
                receipt = evaluate_proposal(
                    task,
                    frame=frame,
                    mode="matched",
                    proposal_action_id=rejected,
                    repo_root=REPO_ROOT,
                )
                self.assertEqual(receipt["membrane_decision"], "revise")
                self.assertNotIn(rejected, receipt["surviving_action_ids"])

    def test_no_membrane_accepts_joint_reject_proposal(self) -> None:
        for task in self.tasks:
            for frame in ("jinn", "beast"):
                rejected = task["fixture_proposals"][frame][0]
                receipt = evaluate_proposal(
                    task,
                    frame=frame,
                    mode="none",
                    proposal_action_id=rejected,
                    repo_root=REPO_ROOT,
                )
                self.assertEqual(receipt["membrane_decision"], "accept")

    def test_shuffle_is_deterministic_and_breaks_mapping(self) -> None:
        for task in self.tasks:
            for frame in ("jinn", "beast"):
                first = inspect_task(
                    task, frame=frame, mode="shuffled", repo_root=REPO_ROOT
                )
                second = inspect_task(
                    task, frame=frame, mode="shuffled", repo_root=REPO_ROOT
                )
                self.assertEqual(first, second)
                sources = {
                    action_id: value["scored_tags_source_action"]
                    for action_id, value in first["actions"].items()
                }
                self.assertTrue(
                    all(action_id != source for action_id, source in sources.items())
                )


if __name__ == "__main__":
    unittest.main()
