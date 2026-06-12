"""Score the episode's overall pacing."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_pacing(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = f"Rate pacing 0-100 across {content['n_scenes']} scenes, {content['n_shots']} shots."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"pacing": score_from_model(verdict), "pacing_reasoning": verdict}
