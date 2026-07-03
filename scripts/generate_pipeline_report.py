"""Generate a Markdown report from a quality pipeline manifest."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def md_path(path: str, report_path: Path) -> str:
    source = Path(path)
    if not source.is_absolute():
        source = Path.cwd() / source

    base = report_path.parent
    if not base.is_absolute():
        base = Path.cwd() / base

    return Path(os.path.relpath(source, base)).as_posix()


def per_dim_table(summary: dict[str, Any], field: str) -> str:
    rows = ["| dim | min | max | mean | std |", "| --- | --- | --- | --- | --- |"]
    for item in summary[f"{field}_summary"]["per_dim"]:
        rows.append(
            f"| {item['index']} | {item['min']} | {item['max']} | {item['mean']} | {item['std']} |"
        )
    return "\n".join(rows)


def quality_rates_table(quality: dict[str, Any]) -> str:
    rates = quality.get("quality_rates", {})
    if not rates:
        return "No missing-field quality rate issues were found."

    rows = ["| metric | count | rate |", "| --- | --- | --- |"]
    for key, value in rates.items():
        rows.append(f"| `{key}` | {value['count']} | {value['rate']} |")
    return "\n".join(rows)


def issue_types_table(quality: dict[str, Any]) -> str:
    issue_types = quality.get("issue_types", {})
    if not issue_types:
        return "No issue types were found."

    rows = ["| issue type | count |", "| --- | --- |"]
    for key, value in issue_types.items():
        rows.append(f"| `{key}` | {value} |")
    return "\n".join(rows)


def generate_report(manifest_path: Path, output_path: Path) -> None:
    manifest = load_json(manifest_path)
    quality = load_json(manifest["quality_summary"])
    distribution = load_json(manifest["distribution_summary"])
    profile = manifest.get("profile", {})

    plots = manifest.get("plots", [])
    plot_lines = []
    for plot in plots:
        label = Path(plot).stem.replace("_", " ")
        plot_lines.append(f"![{label}]({md_path(plot, output_path)})")

    content = f"""# Robot Data Quality Pipeline Report

## 1. Overview

| Item | Value |
| --- | --- |
| Input | `{manifest.get('input')}` |
| Dataset | `{profile.get('dataset', 'unknown')}` |
| Profile | `{manifest.get('profile_path')}` |
| Episodes | {quality.get('episodes')} |
| Steps | {quality.get('steps')} |
| Issue count | {quality.get('issue_count')} |

## 2. Expected Schema

| Rule | Value |
| --- | --- |
| expected_action_dim | {profile.get('expected_action_dim')} |
| expected_state_dim | {profile.get('expected_state_dim')} |
| expected_image_shape | {profile.get('expected_image_shape')} |
| min_trajectory_length | {profile.get('min_trajectory_length')} |
| max_trajectory_length | {profile.get('max_trajectory_length')} |
| action_abs_limit | {profile.get('action_abs_limit')} |
| primary_image_field | `{profile.get('primary_image_field')}` |
| unified_image_field | `{profile.get('unified_image_field')}` |

## 3. Quality Summary

### Issue Types

{issue_types_table(quality)}

### Quality Rates

{quality_rates_table(quality)}

## 4. Action Distribution

{per_dim_table(distribution, 'action')}

## 5. State Distribution

{per_dim_table(distribution, 'state')}

## 6. Plots

{chr(10).join(plot_lines)}

## 7. Engineering Notes

- This report is generated from pipeline artifacts, not written manually.
- The profile records dataset-specific schema rules.
- The manifest records input, configuration, JSON summaries, and plot paths for reproducibility.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote Markdown report to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown report from pipeline outputs.")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json.")
    parser.add_argument("--output", required=True, help="Output Markdown path.")
    args = parser.parse_args()

    generate_report(Path(args.manifest), Path(args.output))


if __name__ == "__main__":
    main()
