"""Track recurring faces across the episode."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def detect_face_tracks(stage_a: dict[str, Any], on_screen_text: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    # Use detected text boxes as ROI hints so we don't track title-card faces.
    _text_hints = on_screen_text["extracted_on_screen_text_v2"]
    result = client.vision_face_detect(
        stage_a["fetch"]["episode_id"], stage_a["fetch"]["duration_s"]
    )
    return {"face_track_ids": result["face_tracks"]}
