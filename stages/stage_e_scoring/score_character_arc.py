"""Score the strength of character arcs."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_character_arc(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = f"Rate character-arc strength 0-100 across {content['n_scenes']} scenes."
    verdict = client.llm_large(prompt, output_schema="domain_score_v1")
    return {"character_arc": score_from_model(verdict), "character_arc_reasoning": verdict}
