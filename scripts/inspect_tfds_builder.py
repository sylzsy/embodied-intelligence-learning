"""Inspect a TensorFlow Datasets builder without downloading full data."""

from __future__ import annotations

import argparse
import json
from typing import Any

import tensorflow_datasets as tfds


def feature_to_dict(feature: Any) -> Any:
    if hasattr(feature, "items"):
        return {key: feature_to_dict(value) for key, value in feature.items()}
    return str(feature)


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a TFDS dataset builder.")
    parser.add_argument("--dataset", default="bridge", help="TFDS dataset name.")
    args = parser.parse_args()

    builder = tfds.builder(args.dataset)
    info = builder.info

    summary = {
        "name": info.name,
        "full_name": info.full_name,
        "version": str(info.version),
        "homepage": info.homepage,
        "citation": bool(info.citation),
        "features": feature_to_dict(info.features),
        "splits": {
            split_name: {
                "num_examples": split_info.num_examples,
                "num_shards": split_info.num_shards,
            }
            for split_name, split_info in info.splits.items()
        },
        "download_size": str(info.download_size),
        "dataset_size": str(info.dataset_size),
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
