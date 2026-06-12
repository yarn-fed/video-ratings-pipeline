"""Score the lighting."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_lighting(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate lighting 0-100.\n"
        f"shots={content['n_shots']} frames={content['frame_signature']}"
    )
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"lighting": score_from_model(verdict), "lighting_reasoning": verdict}
