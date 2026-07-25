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
from run_control_flow import (
    LocalTransformersBackend,
    ProposalFormatError,
    parse_public_response,
)


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

    def test_public_response_parser_discards_closed_thinking(self) -> None:
        parsed = parse_public_response(
            '<think>private scratch</think>{"decision":"path_a","message":"Public."}'
        )
        self.assertEqual(parsed, {"decision": "path_a", "message": "Public."})

    def test_public_response_parser_rejects_extra_fields(self) -> None:
        with self.assertRaises(ProposalFormatError):
            parse_public_response(
                '{"decision":"path_a","message":"Public.","reasoning":"hidden"}'
            )

    def test_local_backend_requires_cap_token_before_importing_model(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "hard-cap launcher"):
            LocalTransformersBackend(
                base_model_path=Path("missing-model"),
                adapters={"jinn": None, "beast": None},
                cache_dir=Path(".cache"),
                max_tokens=16,
                vram_limit_mb=100,
                cap_token=Path("missing-cap-token"),
            )


if __name__ == "__main__":
    unittest.main()
