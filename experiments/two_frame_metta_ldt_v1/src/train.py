from __future__ import annotations

import argparse
import ctypes
import gc
import json
import os
import time
from ctypes import wintypes
from pathlib import Path
from typing import Any

from ldt_experiment import (
    AdditiveCandidateHead,
    build_joint_balanced_dataset,
    canonical_json,
    evaluate_head,
    parse_policy,
    sha256_file,
    train_head,
    write_json,
    write_jsonl,
)


ROOT = Path(__file__).resolve().parents[1]


class IoCounters(ctypes.Structure):
    _fields_ = [
        ("read_operations", ctypes.c_ulonglong),
        ("write_operations", ctypes.c_ulonglong),
        ("other_operations", ctypes.c_ulonglong),
        ("read_bytes", ctypes.c_ulonglong),
        ("write_bytes", ctypes.c_ulonglong),
        ("other_bytes", ctypes.c_ulonglong),
    ]


class ProcessMemoryCounters(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("page_fault_count", wintypes.DWORD),
        ("peak_working_set", ctypes.c_size_t),
        ("working_set", ctypes.c_size_t),
        ("quota_peak_paged_pool", ctypes.c_size_t),
        ("quota_paged_pool", ctypes.c_size_t),
        ("quota_peak_nonpaged_pool", ctypes.c_size_t),
        ("quota_nonpaged_pool", ctypes.c_size_t),
        ("pagefile_usage", ctypes.c_size_t),
        ("peak_pagefile_usage", ctypes.c_size_t),
    ]


GET_PROCESS_MEMORY_INFO = ctypes.windll.psapi.GetProcessMemoryInfo
GET_PROCESS_MEMORY_INFO.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(ProcessMemoryCounters),
    wintypes.DWORD,
]
GET_PROCESS_MEMORY_INFO.restype = wintypes.BOOL
GET_PROCESS_IO_COUNTERS = ctypes.windll.kernel32.GetProcessIoCounters
GET_PROCESS_IO_COUNTERS.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(IoCounters),
]
GET_PROCESS_IO_COUNTERS.restype = wintypes.BOOL


def process_memory_mb() -> float:
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ok = GET_PROCESS_MEMORY_INFO(handle, ctypes.byref(counters), counters.cb)
    return counters.working_set / (1024 * 1024) if ok else 0.0


def process_io_bytes() -> int:
    counters = IoCounters()
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ok = GET_PROCESS_IO_COUNTERS(handle, ctypes.byref(counters))
    return int(counters.read_bytes + counters.write_bytes) if ok else 0


def wait_for_cap_token(path: Path, timeout_seconds: int = 30) -> None:
    deadline = time.monotonic() + timeout_seconds
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError("hard-cap wrapper did not release the training token")
        time.sleep(0.05)


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **event}
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(record) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration", type=Path, default=ROOT / "registration.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "canonical")
    parser.add_argument("--cap-token", type=Path, required=True)
    args = parser.parse_args()
    wait_for_cap_token(args.cap_token)

    registration = json.loads(args.registration.read_text(encoding="utf-8"))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    events_path = output_dir / "events.jsonl"
    if events_path.exists():
        events_path.unlink()

    start_wall = time.monotonic()
    start_cpu = time.process_time()
    start_io = process_io_bytes()
    memory_samples: list[float] = []
    io_rate_samples: list[float] = []
    last_io = start_io
    last_sample_time = start_wall
    checkpoints: list[str] = []
    model_objects: list[AdditiveCandidateHead] = []

    append_event(
        events_path,
        {
            "event": "start",
            "run_id": registration["resource_caps"]["training_task_id"],
            "caps": registration["resource_caps"],
            "device": "cpu",
        },
    )
    try:
        policies = {}
        for alias, frame in registration["frames"].items():
            path = ROOT / frame["policy_path"]
            actual_hash = sha256_file(path)
            if actual_hash != frame["snapshot_sha256"]:
                raise ValueError(
                    f"{alias} policy hash mismatch: {actual_hash} != {frame['snapshot_sha256']}"
                )
            policy = parse_policy(path)
            if policy.benchmark_id != frame["benchmark_id"]:
                raise ValueError(f"{alias} benchmark id does not match registration")
            policies[alias] = policy

        dataset_config = registration["dataset"]
        boundary = registration["boundary_contract"]
        rows, feature_names = build_joint_balanced_dataset(
            policies,
            seed=int(dataset_config["seed"]),
            split_counts=dataset_config["rows_per_joint_cell"],
            train_minimum=float(boundary["train_minimum_score"]),
            reject_maximum=float(boundary["reject_maximum_score"]),
        )
        write_jsonl(output_dir / "shared_candidates.jsonl", rows)
        split_counts = {
            split: sum(row["split"] == split for row in rows)
            for split in dataset_config["rows_per_joint_cell"]
        }
        joint_counts: dict[str, int] = {}
        for row in rows:
            key = f"{row['joint_label']['jinn']}|{row['joint_label']['beast']}|{row['split']}"
            joint_counts[key] = joint_counts.get(key, 0) + 1
        dataset_receipt = {
            "schema_version": "two_frame_joint_dataset_receipt_v1",
            "rows": len(rows),
            "features": len(feature_names),
            "feature_names": list(feature_names),
            "split_counts": split_counts,
            "joint_counts": joint_counts,
            "dataset_sha256": sha256_file(output_dir / "shared_candidates.jsonl"),
        }
        write_json(output_dir / "dataset_receipt.json", dataset_receipt)
        append_event(events_path, {"event": "dataset_built", **dataset_receipt})

        model_config = registration["model"]
        all_metrics: dict[str, Any] = {}
        all_predictions: list[dict[str, Any]] = []
        for frame_index, frame in enumerate(("jinn", "beast")):
            frame_checkpoints = output_dir / "checkpoints" / frame

            def epoch_callback(epoch: int, loss: float) -> None:
                nonlocal last_io, last_sample_time
                now = time.monotonic()
                current_io = process_io_bytes()
                elapsed = max(now - last_sample_time, 1e-9)
                io_rate_samples.append((current_io - last_io) / elapsed / (1024 * 1024))
                last_io = current_io
                last_sample_time = now
                memory_samples.append(process_memory_mb())
                if epoch == 1 or epoch % 10 == 0:
                    append_event(
                        events_path,
                        {
                            "event": "epoch",
                            "frame": frame,
                            "epoch": epoch,
                            "mean_loss": round(loss, 8),
                        },
                    )

            def checkpoint_callback(
                epoch: int, model: AdditiveCandidateHead, loss: float
            ) -> None:
                path = frame_checkpoints / f"epoch-{epoch:03d}.json"
                write_json(
                    path,
                    {
                        **model.to_jsonable(),
                        "frame": frame,
                        "epoch": epoch,
                        "mean_loss": round(loss, 8),
                    },
                )
                checkpoints.append(path.relative_to(output_dir).as_posix())
                append_event(
                    events_path,
                    {
                        "event": "checkpoint",
                        "frame": frame,
                        "epoch": epoch,
                        "path": path.relative_to(output_dir).as_posix(),
                    },
                )

            model = train_head(
                rows,
                frame=frame,
                feature_names=feature_names,
                seed=int(dataset_config["seed"]) + 1000 * frame_index,
                epochs=int(model_config["epochs_per_frame"]),
                batch_size=int(model_config["batch_size"]),
                learning_rate=float(model_config["learning_rate"]),
                l2=float(model_config["l2"]),
                checkpoint_interval=int(model_config["checkpoint_interval_epochs"]),
                checkpoint_callback=checkpoint_callback,
                epoch_callback=epoch_callback,
            )
            model_objects.append(model)
            write_json(output_dir / "models" / f"{frame}.json", model.to_jsonable())
            frame_metrics = {}
            for split in ("validation", "test"):
                metrics, predictions = evaluate_head(
                    model,
                    rows,
                    frame=frame,
                    policies=policies,
                    split=split,
                    singleton_threshold=float(
                        model_config["candidate_singleton_probability"]
                    ),
                    otherwise_top_k=int(model_config["otherwise_keep_top_k"]),
                )
                frame_metrics[split] = metrics
                all_predictions.extend(predictions)
                append_event(
                    events_path,
                    {"event": "evaluation", "frame": frame, **metrics},
                )
            all_metrics[frame] = frame_metrics

        write_json(output_dir / "metrics.json", all_metrics)
        write_jsonl(output_dir / "heldout_predictions.jsonl", all_predictions)

        checks = registration["promotion_checks"]
        promotion: dict[str, bool] = {}
        for frame in ("jinn", "beast"):
            metrics = all_metrics[frame]["test"]
            promotion[f"{frame}_accuracy"] = (
                metrics["accuracy"] >= checks["minimum_test_accuracy"]
            )
            promotion[f"{frame}_candidate_coverage"] = (
                metrics["candidate_coverage"]
                >= checks["minimum_candidate_coverage"]
            )
            promotion[f"{frame}_false_elimination"] = (
                metrics["false_elimination_rate"]
                <= checks["maximum_false_elimination_rate"]
            )
            promotion[f"{frame}_critical_recall"] = (
                metrics["critical_reject_recall"]
                >= checks["minimum_critical_reject_recall"]
            )
            promotion[f"{frame}_nuisance_invariance"] = (
                metrics["opposite_frame_top_lane_invariance"]
                >= checks["minimum_opposite_frame_top_lane_invariance"]
            )
            promotion[f"{frame}_irrelevant_weight"] = (
                metrics["irrelevant_weight_fraction"]
                <= checks["maximum_irrelevant_weight_fraction"]
            )

        pilot_ready = all(promotion.values())
        append_event(
            events_path,
            {
                "event": "complete",
                "status": "completed",
                "steps_completed": int(model_config["epochs_per_frame"]) * 2,
                "pilot_ready": pilot_ready,
            },
        )

        key_artifacts = [
            "dataset_receipt.json",
            "shared_candidates.jsonl",
            "models/jinn.json",
            "models/beast.json",
            "metrics.json",
            "heldout_predictions.jsonl",
            "events.jsonl",
        ]
        artifact_manifest = {
            relative: sha256_file(output_dir / relative) for relative in key_artifacts
        }
        write_json(output_dir / "artifact_manifest.json", artifact_manifest)

        elapsed = time.monotonic() - start_wall
        cpu_elapsed = time.process_time() - start_cpu
        logical_cpus = max(os.cpu_count() or 1, 1)
        summary = {
            "schema_version": "two_frame_metta_ldt_run_summary_v1",
            "run_id": registration["resource_caps"]["training_task_id"],
            "status": "completed",
            "abort_reason": None,
            "device": "cpu",
            "gpu_loaded": False,
            "frames_trained_sequentially": True,
            "rows": len(rows),
            "features": len(feature_names),
            "steps_completed": int(model_config["epochs_per_frame"]) * 2,
            "checkpoints": checkpoints,
            "peak_ram_mb": round(max(memory_samples or [process_memory_mb()]), 3),
            "avg_ram_mb": round(
                sum(memory_samples) / len(memory_samples)
                if memory_samples
                else process_memory_mb(),
                3,
            ),
            "peak_io_mb_s": round(max(io_rate_samples or [0.0]), 3),
            "cpu_pct": round(100.0 * cpu_elapsed / max(elapsed, 1e-9) / logical_cpus, 3),
            "wall_seconds": round(elapsed, 3),
            "metrics": all_metrics,
            "promotion_checks": promotion,
            "pilot_ready": pilot_ready,
            "artifact_manifest": artifact_manifest,
            "claim_scope": registration["claim_boundary"],
            "cleanup": {
                "python_objects_released": False,
                "cuda_cleanup_required": False,
                "wrapper_cleanup_pending": True,
            },
        }
        write_json(output_dir / "summary.json", summary)
        return 0
    except Exception as exc:
        append_event(
            events_path,
            {"event": "abort", "reason": type(exc).__name__, "detail": str(exc)},
        )
        raise
    finally:
        model_objects.clear()
        gc.collect()


if __name__ == "__main__":
    raise SystemExit(main())
