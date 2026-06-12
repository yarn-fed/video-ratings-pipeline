"""Detect brand logos appearing in the episode."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def detect_logos(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    result = client.vision_logo_detect(
        stage_a["fetch"]["episode_id"], stage_a["fetch"]["duration_s"]
    )
    return {"detected_logos_v1": result["logos"]}
