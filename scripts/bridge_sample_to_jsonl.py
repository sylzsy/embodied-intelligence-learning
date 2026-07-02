"""Convert a tiny BridgeData-style sample into the project JSONL format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def build_bridge_like_sample() -> list[dict[str, Any]]:
    return [
        {
            "episode_metadata": {
                "episode_id": "bridge_mock_001",
                "file_path": "mock/bridge/train/bridge_mock_001",
            },
            "steps": [
                {
                    "action": [0.01, 0.0, 0.02, 0.0, 0.0, 0.01, 1.0],
                    "language_instruction": "put the carrot on the plate",
                    "observation": {
                        "image_0": {"height": 256, "width": 256, "channels": 3},
                        "state": [0.1, 0.2, 0.3, 0.0, 0.0, 0.1, 1.0],
                    },
                    "timestamp": 0.0,
                },
                {
                    "action": [0.02, 0.0, 0.01, 0.0, 0.0, 0.01, 0.8],
                    "language_instruction": "put the carrot on the plate",
                    "observation": {
                        "image_0": {"height": 256, "width": 256, "channels": 3},
                        "state": [0.12, 0.21, 0.32, 0.0, 0.0, 0.1, 0.8],
                    },
                    "timestamp": 0.1,
                },
            ],
        }
    ]


def convert_episode(episode: dict[str, Any]) -> dict[str, Any]:
    metadata = episode.get("episode_metadata", {})
    converted_steps = []

    for step in episode.get("steps", []):
        observation = step.get("observation", {})
        converted_steps.append(
            {
                "observation": {
                    "image": observation.get("image_0"),
                    "state": observation.get("state"),
                    "language_instruction": step.get("language_instruction"),
                },
                "action": step.get("action"),
                "timestamp": step.get("timestamp"),
            }
        )

    return {
        "episode_id": metadata.get("episode_id", metadata.get("file_path", "bridge_episode")),
        "source_dataset": "bridge",
        "steps": converted_steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a tiny BridgeData-style sample to project JSONL."
    )
    parser.add_argument(
        "--output",
        default="scripts/bridge_mock_episodes.jsonl",
        help="Output JSONL path.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    converted = [convert_episode(episode) for episode in build_bridge_like_sample()]
    with output_path.open("w", encoding="utf-8") as file:
        for episode in converted:
            file.write(json.dumps(episode, ensure_ascii=False) + "\n")

    print(f"Wrote {len(converted)} episode(s) to {output_path}")
    print(json.dumps(converted[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
