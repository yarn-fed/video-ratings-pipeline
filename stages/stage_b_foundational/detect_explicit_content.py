"""Flag explicit content so audience scoring can gate on it."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def detect_explicit_content(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    result = client.vision_explicit_detect(
        stage_a["fetch"]["episode_id"], stage_a["fetch"]["duration_s"]
    )
    return {"explicit_flag": result["explicit"], "explicit_confidence": result["confidence"]}
