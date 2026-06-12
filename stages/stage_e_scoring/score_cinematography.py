"""Score the cinematography."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_cinematography(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate cinematography 0-100.\n"
        f"shots={content['n_shots']} frames={content['frame_signature']}"
    )
    verdict = client.llm_large(prompt, output_schema="domain_score_v1")
    return {"cinematography": score_from_model(verdict), "cinematography_reasoning": verdict}
