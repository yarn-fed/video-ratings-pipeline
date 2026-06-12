"""Score the episode's emotional impact."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_emotional_impact(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate emotional impact 0-100.\n"
        f"scenes={content['n_scenes']} transcript={content['transcript_signature']}"
    )
    verdict = client.llm_large(prompt, output_schema="domain_score_premium_v1")
    return {"emotional_impact": score_from_model(verdict), "emotional_impact_reasoning": verdict}
