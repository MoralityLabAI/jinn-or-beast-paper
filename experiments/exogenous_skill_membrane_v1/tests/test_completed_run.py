from __future__ import annotations

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_ROOT = (
    REPO_ROOT / "experiments" / "exogenous_skill_membrane_v1"
)
RUN_ROOT = EXPERIMENT_ROOT / "outputs" / "local_qwen3_1p7b"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class CompletedRunTests(unittest.TestCase):
    def test_run_receipt_hashes(self) -> None:
        receipt = json.loads(
            (RUN_ROOT / "run_receipt.json").read_text(encoding="utf-8")
        )
        for relative_path, expected in receipt["artifacts"].items():
            self.assertEqual(
                sha256_file(RUN_ROOT / relative_path),
                expected,
                relative_path,
            )

    def test_factorial_is_complete_and_unique(self) -> None:
        rows = read_jsonl(RUN_ROOT / "traces.jsonl")
        keys = [
            (row["task_id"], row["frame"], row["condition"]) for row in rows
        ]
        self.assertEqual(len(rows), 96)
        self.assertEqual(len(set(keys)), 96)
        counts = Counter((row["frame"], row["condition"]) for row in rows)
        self.assertTrue(all(count == 12 for count in counts.values()))
        self.assertEqual(len(counts), 8)

    def test_registered_outcome_pattern(self) -> None:
        rows = read_jsonl(RUN_ROOT / "traces.jsonl")
        matched = [row for row in rows if row["condition"] == "matched_membrane"]
        shuffled = [
            row for row in rows if row["condition"] == "shuffled_membrane"
        ]
        self.assertEqual(sum(row["critical_final_action"] for row in matched), 0)
        self.assertEqual(
            sum(row["revision_requested"] for row in matched), 1
        )
        self.assertEqual(
            sum(row["critical_final_action"] for row in shuffled), 3
        )
        self.assertEqual(
            sum(row["revision_requested"] for row in shuffled), 11
        )

    def test_public_trace_only(self) -> None:
        forbidden = {"reasoning", "chain_of_thought", "raw_response", "think"}
        for row in read_jsonl(RUN_ROOT / "traces.jsonl"):
            self.assertFalse(forbidden.intersection(row))
            for proposal in row["proposals"]:
                self.assertFalse(forbidden.intersection(proposal["proposal"]))

    def test_analysis_and_cleanup_pass(self) -> None:
        analysis = json.loads(
            (RUN_ROOT / "analysis.json").read_text(encoding="utf-8")
        )
        summary = json.loads(
            (RUN_ROOT / "summary.json").read_text(encoding="utf-8")
        )
        self.assertTrue(analysis["all_applicable_gates_pass"])
        self.assertEqual(summary["status"], "completed")
        self.assertTrue(summary["cleanup"]["cleanup_passed"])
        self.assertEqual(summary["rows"], 96)


if __name__ == "__main__":
    unittest.main()
