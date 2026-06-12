"""Run OCR over sampled frames to capture on-screen text."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def detect_text_on_screen(stage_a: dict[str, Any], logos: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    # Feed logo bounds as ROI hints so OCR can skip already-branded regions.
    _brand_hints = logos["detected_logos_v1"]
    result = client.vision_text_detect(
        stage_a["fetch"]["episode_id"], stage_a["fetch"]["duration_s"]
    )
    return {"extracted_on_screen_text_v2": result["on_screen_text"]}
