"""Tests covering pre-existing data-quality expectations."""

from __future__ import annotations

from stages.stage_b_foundational import extract_runtime


def test_runtime_matches_duration(episode_input):
    fetch = {"fetch": {"raw_metadata": episode_input["raw_metadata"], "duration_s": episode_input["duration_s"]}}
    result = extract_runtime(fetch)
    expected_minutes = episode_input["duration_s"] // 60
    assert result["runtime_minutes"] == expected_minutes
