"""Score the quality of the episode's dialogue."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_dialogue_quality(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()

    # Re-transcribe a dialogue-heavy snippet to score the dialogue closely.
    client.transcribe(
        audio_id=f"{content['episode_id']}_snippet",
        duration_s=content["duration_s"],
        enable_diarization=False,
    )

    prompt = f"Rate dialogue quality 0-100; transcript={content['transcript_signature']}."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"dialogue_quality": score_from_model(verdict), "dialogue_quality_reasoning": verdict}
