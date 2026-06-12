"""Output-shape tests."""

from __future__ import annotations

from pipeline import run_pipeline


def test_core_fields_present(episode_input):
    p = run_pipeline(episode_input)
    assert p["episode_id"] == "ep_001"
    assert 0 <= p["overall_rating"] <= 100
    assert set(p["scores"]) == {"plot", "craft", "audience"}
    assert set(p["stats"]) >= {"n_shots", "n_scenes", "n_segments", "transcript_signature"}


def test_domain_scores_in_range(episode_input):
    p = run_pipeline(episode_input)
    for domain, value in p["scores"].items():
        assert 0 <= value <= 100, domain


def test_thinking_scores_present(episode_input):
    p = run_pipeline(episode_input)
    assert set(p["thinking"]) == {
        "repetition_score",
        "focus_cue_score",
        "creative_thinking_score",
        "memory_demand_score",
        "critical_thinking_score",
    }


def test_soundtrack_mood_present(episode_input):
    # The review still carries a soundtrack-mood label.
    p = run_pipeline(episode_input)
    assert p["deprecated"]["soundtrack_mood"] is not None


def test_determinism(episode_input):
    assert run_pipeline(episode_input) == run_pipeline(episode_input)
