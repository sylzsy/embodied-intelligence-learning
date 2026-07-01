"""Quality checks for small robot episode datasets.

Expected input: JSON or JSONL. Each episode should look like:

{
  "episode_id": "demo_001",
  "steps": [
    {
      "observation": {
        "image": {"width": 256, "height": 256, "channels": 3},
        "state": [0.1, 0.2],
        "language_instruction": "pick up the cup"
      },
      "action": [0.01, 0.0, 0.02, 1.0],
      "timestamp": 0.0
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


def load_episodes(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        episodes = []
        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    episodes.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
        return episodes

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "episodes" in data:
        return data["episodes"]
    raise ValueError("JSON input must be a list or an object with an 'episodes' key.")


def image_shape(image: Any) -> tuple[int, int, int] | None:
    if not isinstance(image, dict):
        return None
    width = image.get("width")
    height = image.get("height")
    channels = image.get("channels", 3)
    if not all(isinstance(value, int) for value in [width, height, channels]):
        return None
    return (height, width, channels)


def check_episodes(episodes: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    trajectory_lengths: list[int] = []
    action_dims: Counter[int] = Counter()
    image_shapes: Counter[tuple[int, int, int]] = Counter()
    instructions: Counter[str] = Counter()
    step_records: list[dict[str, Any]] = []

    for episode_index, episode in enumerate(episodes):
        episode_id = episode.get("episode_id", f"episode_{episode_index}")
        steps = episode.get("steps")

        if not isinstance(steps, list):
            issues.append(
                {
                    "episode_id": episode_id,
                    "step": None,
                    "type": "missing_steps",
                    "message": "Episode has no valid steps list.",
                }
            )
            continue

        trajectory_lengths.append(len(steps))
        if len(steps) < 2:
            issues.append(
                {
                    "episode_id": episode_id,
                    "step": None,
                    "type": "short_trajectory",
                    "message": "Episode has fewer than 2 steps.",
                }
            )

        previous_timestamp: float | None = None
        for step_index, step in enumerate(steps):
            observation = step.get("observation") if isinstance(step, dict) else None
            if not isinstance(observation, dict):
                issues.append(issue(episode_id, step_index, "missing_observation"))
                continue

            shape = image_shape(observation.get("image"))
            if shape is None:
                issues.append(issue(episode_id, step_index, "invalid_image"))
            else:
                image_shapes[shape] += 1
                step_records.append(
                    {
                        "episode_id": episode_id,
                        "step": step_index,
                        "field": "image_shape",
                        "value": shape,
                    }
                )

            state = observation.get("state")
            if not isinstance(state, list) or not state:
                issues.append(issue(episode_id, step_index, "invalid_state"))

            instruction = observation.get("language_instruction")
            if not isinstance(instruction, str) or not instruction.strip():
                issues.append(issue(episode_id, step_index, "missing_language_instruction"))
            else:
                instructions[instruction.strip().lower()] += 1

            action = step.get("action")
            if not isinstance(action, list) or not action:
                issues.append(issue(episode_id, step_index, "invalid_action"))
            else:
                action_dims[len(action)] += 1
                step_records.append(
                    {
                        "episode_id": episode_id,
                        "step": step_index,
                        "field": "action_dim",
                        "value": len(action),
                    }
                )

            timestamp = step.get("timestamp")
            if isinstance(timestamp, (int, float)):
                if previous_timestamp is not None and timestamp <= previous_timestamp:
                    issues.append(issue(episode_id, step_index, "non_increasing_timestamp"))
                previous_timestamp = float(timestamp)
            else:
                issues.append(issue(episode_id, step_index, "invalid_timestamp"))

    issues.extend(consistency_issues(step_records, "action_dim", action_dims))
    issues.extend(consistency_issues(step_records, "image_shape", image_shapes))

    return {
        "episodes": len(episodes),
        "steps": sum(trajectory_lengths),
        "trajectory_length": summarize_numbers(trajectory_lengths),
        "action_dimensions": dict(action_dims),
        "image_shapes": {str(key): value for key, value in image_shapes.items()},
        "unique_language_instructions": len(instructions),
        "top_language_instructions": instructions.most_common(10),
        "issue_count": len(issues),
        "issue_types": dict(Counter(item["type"] for item in issues)),
        "issues": issues,
    }


def issue(episode_id: str, step: int, issue_type: str) -> dict[str, Any]:
    return {
        "episode_id": episode_id,
        "step": step,
        "type": issue_type,
        "message": issue_type.replace("_", " "),
    }


def consistency_issues(
    step_records: list[dict[str, Any]],
    field: str,
    values: Counter[Any],
) -> list[dict[str, Any]]:
    if len(values) <= 1:
        return []

    expected = values.most_common(1)[0][0]
    issue_type = f"inconsistent_{field}"
    results = []
    for record in step_records:
        if record["field"] == field and record["value"] != expected:
            results.append(
                {
                    "episode_id": record["episode_id"],
                    "step": record["step"],
                    "type": issue_type,
                    "message": f"{field} is {record['value']}, expected common value {expected}",
                }
            )
    return results


def summarize_numbers(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "max": None, "mean": None}
    return {"min": min(values), "max": max(values), "mean": round(mean(values), 2)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check robot episode dataset quality.")
    parser.add_argument("--input", required=True, help="Path to a JSON or JSONL episode file.")
    parser.add_argument("--output", help="Optional path for the JSON summary.")
    args = parser.parse_args()

    input_path = Path(args.input)
    episodes = load_episodes(input_path)
    summary = check_episodes(episodes)

    output = json.dumps(summary, ensure_ascii=False, indent=2)
    print(output)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
