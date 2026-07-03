"""Run the robot data quality pipeline end to end."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_PROFILE = {
    "dataset": "bridge",
    "expected_action_dim": 7,
    "expected_state_dim": 7,
    "expected_image_shape": "256x256x3",
    "min_trajectory_length": 2,
    "max_trajectory_length": 200,
    "action_abs_limit": 1.0,
}


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, check=True)


def load_profile(path: str | None) -> dict:
    profile = dict(DEFAULT_PROFILE)
    if path:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
        profile.update(loaded)
    return profile


def override_if_set(profile: dict, key: str, value) -> None:
    if value is not None:
        profile[key] = value


def main() -> None:
    parser = argparse.ArgumentParser(description="Run quality checks, summaries, and plots.")
    parser.add_argument("--input", required=True, help="Path to a JSON or JSONL episode file.")
    parser.add_argument("--output-dir", default="reports/pipeline", help="Output directory.")
    parser.add_argument("--profile", help="Dataset profile JSON path.")
    parser.add_argument("--expected-action-dim", type=int)
    parser.add_argument("--expected-state-dim", type=int)
    parser.add_argument("--expected-image-shape")
    parser.add_argument("--min-trajectory-length", type=int)
    parser.add_argument("--max-trajectory-length", type=int)
    parser.add_argument("--action-abs-limit", type=float)
    args = parser.parse_args()

    profile = load_profile(args.profile)
    override_if_set(profile, "expected_action_dim", args.expected_action_dim)
    override_if_set(profile, "expected_state_dim", args.expected_state_dim)
    override_if_set(profile, "expected_image_shape", args.expected_image_shape)
    override_if_set(profile, "min_trajectory_length", args.min_trajectory_length)
    override_if_set(profile, "max_trajectory_length", args.max_trajectory_length)
    override_if_set(profile, "action_abs_limit", args.action_abs_limit)

    output_dir = Path(args.output_dir)
    plot_dir = output_dir / "plots"
    output_dir.mkdir(parents=True, exist_ok=True)

    quality_json = output_dir / "quality_summary.json"
    distribution_json = output_dir / "distribution_summary.json"
    manifest_json = output_dir / "manifest.json"

    python = sys.executable
    run(
        [
            python,
            "scripts/check_dataset_quality.py",
            "--input",
            args.input,
            "--expected-action-dim",
            str(profile["expected_action_dim"]),
            "--expected-state-dim",
            str(profile["expected_state_dim"]),
            "--expected-image-shape",
            str(profile["expected_image_shape"]),
            "--min-trajectory-length",
            str(profile["min_trajectory_length"]),
            "--max-trajectory-length",
            str(profile["max_trajectory_length"]),
            "--action-abs-limit",
            str(profile["action_abs_limit"]),
            "--output",
            str(quality_json),
        ]
    )
    run(
        [
            python,
            "scripts/summarize_dataset.py",
            "--input",
            args.input,
            "--output",
            str(distribution_json),
        ]
    )
    run(
        [
            python,
            "scripts/plot_distribution.py",
            "--input",
            str(distribution_json),
            "--output-dir",
            str(plot_dir),
        ]
    )

    manifest = {
        "input": args.input,
        "profile_path": args.profile,
        "profile": profile,
        "quality_summary": str(quality_json),
        "distribution_summary": str(distribution_json),
        "plots": [
            str(plot_dir / "action_range.png"),
            str(plot_dir / "action_std.png"),
            str(plot_dir / "state_range.png"),
            str(plot_dir / "state_std.png"),
        ],
    }
    manifest_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote pipeline manifest to {manifest_json}")


if __name__ == "__main__":
    main()
