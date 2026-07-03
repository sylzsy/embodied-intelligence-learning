"""Summarize action/state distributions for robot episode JSONL datasets."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any

from check_dataset_quality import load_episodes


def collect_vectors(episodes: list[dict[str, Any]], field: str) -> list[list[float]]:
    vectors: list[list[float]] = []
    for episode in episodes:
        for step in episode.get("steps", []):
            if field == "action":
                value = step.get("action")
            elif field == "state":
                observation = step.get("observation", {})
                value = observation.get("state") if isinstance(observation, dict) else None
            else:
                raise ValueError(f"Unsupported field: {field}")

            if isinstance(value, list) and value and all(isinstance(item, (int, float)) for item in value):
                vectors.append([float(item) for item in value])
    return vectors


def summarize_vectors(vectors: list[list[float]]) -> dict[str, Any]:
    if not vectors:
        return {"count": 0, "dim": None, "per_dim": []}

    dims = sorted({len(vector) for vector in vectors})
    if len(dims) != 1:
        return {
            "count": len(vectors),
            "dim": None,
            "dimension_mismatch": dims,
            "per_dim": [],
        }

    dim = dims[0]
    per_dim = []
    for index in range(dim):
        values = [vector[index] for vector in vectors]
        avg = mean(values)
        variance = mean([(value - avg) ** 2 for value in values])
        per_dim.append(
            {
                "index": index,
                "min": round(min(values), 6),
                "max": round(max(values), 6),
                "mean": round(avg, 6),
                "std": round(math.sqrt(variance), 6),
            }
        )

    return {"count": len(vectors), "dim": dim, "per_dim": per_dim}


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize robot dataset action/state distributions.")
    parser.add_argument("--input", required=True, help="Path to a JSON or JSONL episode file.")
    parser.add_argument("--output", help="Optional path for the JSON summary.")
    args = parser.parse_args()

    episodes = load_episodes(Path(args.input))
    summary = {
        "input": args.input,
        "episodes": len(episodes),
        "action_summary": summarize_vectors(collect_vectors(episodes, "action")),
        "state_summary": summarize_vectors(collect_vectors(episodes, "state")),
    }

    output = json.dumps(summary, ensure_ascii=False, indent=2)
    print(output)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
