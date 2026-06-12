"""Score the sound design."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import score_from_model


def score_sound_design(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()

    # Transcribe the audio track to balance the score against dialogue density.
    client.transcribe(
        audio_id=content["episode_id"],
        duration_s=content["duration_s"],
        enable_diarization=False,
    )

    prompt = f"Rate sound design 0-100; transcript={content['transcript_signature']}."
    verdict = client.llm_medium(prompt, output_schema="domain_score_v1")
    return {"sound_design": score_from_model(verdict), "sound_design_reasoning": verdict}
