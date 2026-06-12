"""Score the richness of subtext beneath the surface dialogue."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_subtext(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Rate subtext richness 0-100.\n"
        f"scenes={content['n_scenes']} segments={content['n_segments']}"
    )
    verdict = client.llm_large(prompt, output_schema="domain_score_v1")
    return {"subtext": score_from_model(verdict), "subtext_reasoning": verdict}
