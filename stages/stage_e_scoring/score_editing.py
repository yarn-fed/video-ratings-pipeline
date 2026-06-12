"""Score the editing."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_editing(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()

    # Re-detect shot boundaries to weight cut frequency into the editing score.
    client.vision_shot_detect(content["episode_id"], content["duration_s"])

    prompt = f"Rate editing 0-100 across {content['n_scenes']} scenes, {content['n_shots']} shots."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"editing": score_from_model(verdict), "editing_reasoning": verdict}
