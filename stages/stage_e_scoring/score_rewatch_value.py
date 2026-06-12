"""Score the episode's rewatch value."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_rewatch_value(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = f"Rate rewatch value 0-100 across {content['n_scenes']} scenes."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"rewatch_value": score_from_model(verdict), "rewatch_value_reasoning": verdict}
