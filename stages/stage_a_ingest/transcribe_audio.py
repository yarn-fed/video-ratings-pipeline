"""Transcribe the episode audio."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def transcribe_audio(episode: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    transcript = client.transcribe(
        audio_id=episode["episode_id"],
        duration_s=episode["duration_s"],
        enable_diarization=True,
    )
    return {"transcript": transcript}
