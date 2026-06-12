"""Score age-appropriateness, gating on explicit content."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_age_appropriateness(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()

    # Check for explicit content before scoring.
    client.vision_explicit_detect(content["episode_id"], content["duration_s"])

    prompt = f"Rate age-appropriateness 0-100; explicit={content['explicit_flag']}, scenes={content['n_scenes']}."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"age_appropriateness": score_from_model(verdict), "age_appropriateness_reasoning": verdict}
