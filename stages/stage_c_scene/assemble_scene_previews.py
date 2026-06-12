"""Assemble a preview thumbnail set for each scene."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def assemble_scene_previews(scenes_bundle: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = scenes_bundle["scenes"]
    frame_ids = [f"{scene['scene_id']}_preview" for scene in scenes]
    result = client.vision_frame_analyse(frame_ids)
    previews = {f["frame_id"].replace("_preview", ""): f["scene_label"] for f in result["frames"]}
    return {"previews": previews}
