"""Run the robot data quality pipeline end to end."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run quality checks, summaries, and plots.")
    parser.add_argument("--input", required=True, help="Path to a JSON or JSONL episode file.")
    parser.add_argument("--output-dir", default="reports/pipeline", help="Output directory.")
    parser.add_argument("--expected-action-dim", type=int, default=7)
    parser.add_argument("--expected-state-dim", type=int, default=7)
    parser.add_argument("--expected-image-shape", default="256x256x3")
    parser.add_argument("--min-trajectory-length", type=int, default=2)
    parser.add_argument("--max-trajectory-length", type=int, default=200)
    parser.add_argument("--action-abs-limit", type=float, default=1.0)
    args = parser.parse_args()

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
            str(args.expected_action_dim),
            "--expected-state-dim",
            str(args.expected_state_dim),
            "--expected-image-shape",
            args.expected_image_shape,
            "--min-trajectory-length",
            str(args.min_trajectory_length),
            "--max-trajectory-length",
            str(args.max_trajectory_length),
            "--action-abs-limit",
            str(args.action_abs_limit),
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
