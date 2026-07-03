"""Streamlit UI for the robot dataset quality pipeline."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).parent
UPLOAD_DIR = ROOT / "reports" / "streamlit_uploads"
OUTPUT_ROOT = ROOT / "reports" / "streamlit_runs"
DEFAULT_PROFILE = ROOT / "configs" / "bridge_v2_profile.json"
SAMPLE_INPUT = ROOT / "scripts" / "bridge_mock_episodes.jsonl"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_uploaded_file(uploaded_file) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = Path(uploaded_file.name).name
    output_path = UPLOAD_DIR / f"{timestamp}_{safe_name}"
    output_path.write_bytes(uploaded_file.getbuffer())
    return output_path


def run_pipeline(input_path: Path, profile_path: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "run_quality_pipeline.py"),
        "--input",
        str(input_path),
        "--profile",
        str(profile_path),
        "--output-dir",
        str(output_dir),
    ]
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def show_metric_cards(quality: dict[str, Any]) -> None:
    cols = st.columns(4)
    cols[0].metric("Episodes", quality.get("episodes", 0))
    cols[1].metric("Steps", quality.get("steps", 0))
    cols[2].metric("Issue Count", quality.get("issue_count", 0))
    cols[3].metric("Language Tasks", quality.get("unique_language_instructions", 0))


def show_plots(output_dir: Path) -> None:
    plot_dir = output_dir / "plots"
    plot_paths = [
        plot_dir / "action_range.png",
        plot_dir / "action_std.png",
        plot_dir / "state_range.png",
        plot_dir / "state_std.png",
    ]

    existing = [path for path in plot_paths if path.exists()]
    if not existing:
        st.info("No plots were generated.")
        return

    cols = st.columns(2)
    for index, path in enumerate(existing):
        with cols[index % 2]:
            st.image(str(path), caption=path.stem.replace("_", " ").title())


def show_downloads(output_dir: Path) -> None:
    report_path = output_dir / "report.md"
    quality_path = output_dir / "quality_summary.json"
    distribution_path = output_dir / "distribution_summary.json"

    cols = st.columns(3)
    if report_path.exists():
        cols[0].download_button(
            "Download report.md",
            report_path.read_text(encoding="utf-8"),
            file_name="report.md",
            mime="text/markdown",
        )
    if quality_path.exists():
        cols[1].download_button(
            "Download quality JSON",
            quality_path.read_text(encoding="utf-8"),
            file_name="quality_summary.json",
            mime="application/json",
        )
    if distribution_path.exists():
        cols[2].download_button(
            "Download distribution JSON",
            distribution_path.read_text(encoding="utf-8"),
            file_name="distribution_summary.json",
            mime="application/json",
        )


def main() -> None:
    st.set_page_config(
        page_title="Robot Dataset Quality Platform",
        page_icon="DQ",
        layout="wide",
    )

    st.title("Robot Dataset Quality Platform")
    st.caption("BridgeData-style episode quality checks, distribution plots, and report generation.")

    with st.sidebar:
        st.header("Input")
        use_sample = st.checkbox("Use sample BridgeData-style JSONL", value=True)
        uploaded_file = st.file_uploader("Upload JSON / JSONL episode file", type=["json", "jsonl"])

        st.header("Profile")
        profile_path_text = st.text_input("Profile path", value=str(DEFAULT_PROFILE.relative_to(ROOT)))
        run_button = st.button("Run Quality Pipeline", type="primary")

    if use_sample:
        input_path = SAMPLE_INPUT
    elif uploaded_file is not None:
        input_path = save_uploaded_file(uploaded_file)
    else:
        input_path = None

    profile_path = ROOT / profile_path_text
    if not profile_path.exists():
        st.error(f"Profile not found: {profile_path}")
        return

    profile = load_json(profile_path)
    with st.expander("Dataset Profile", expanded=False):
        st.json(profile)

    if not run_button:
        st.info("Choose an input file, then click Run Quality Pipeline.")
        return

    if input_path is None:
        st.warning("Please upload a JSON or JSONL file, or use the sample input.")
        return

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = OUTPUT_ROOT / run_id

    with st.spinner("Running quality checks, summaries, plots, and report generation..."):
        result = run_pipeline(input_path, profile_path, output_dir)

    if result.returncode != 0:
        st.error("Pipeline failed.")
        st.code(result.stderr or result.stdout, language="text")
        return

    st.success(f"Pipeline finished: {output_dir.relative_to(ROOT)}")

    quality = load_json(output_dir / "quality_summary.json")
    distribution = load_json(output_dir / "distribution_summary.json")

    show_metric_cards(quality)

    tab_quality, tab_distribution, tab_plots, tab_report, tab_logs = st.tabs(
        ["Quality", "Distribution", "Plots", "Report", "Run Logs"]
    )

    with tab_quality:
        st.subheader("Quality Summary")
        st.json(quality)

    with tab_distribution:
        st.subheader("Action / State Distribution")
        st.json(distribution)

    with tab_plots:
        st.subheader("Distribution Plots")
        show_plots(output_dir)

    with tab_report:
        st.subheader("Generated Markdown Report")
        report_path = output_dir / "report.md"
        if report_path.exists():
            st.markdown(report_path.read_text(encoding="utf-8"))
        show_downloads(output_dir)

    with tab_logs:
        st.subheader("Pipeline Logs")
        st.code(result.stdout, language="text")
        if result.stderr:
            st.code(result.stderr, language="text")


if __name__ == "__main__":
    main()
