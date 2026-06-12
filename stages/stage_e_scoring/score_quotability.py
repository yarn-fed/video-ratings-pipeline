"""Score how quotable the episode's dialogue is."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_quotability(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = f"Rate quotability 0-100; transcript={content['transcript_signature']}."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"quotability": score_from_model(verdict), "quotability_reasoning": verdict}
