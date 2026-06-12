"""Guardrail on the number of model calls a run makes."""

from __future__ import annotations

from pipeline import run_pipeline


def test_llm_call_budget(episode_input, fake_client):
    run_pipeline(episode_input)
    assert fake_client.calls.get("llm", 0) == 30


def test_transcribe_call_budget(episode_input, fake_client):
    run_pipeline(episode_input)
    assert fake_client.calls.get("transcribe", 0) == 3
