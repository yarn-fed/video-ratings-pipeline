"""Attach transcript segments to the scene that contains them."""

from __future__ import annotations

from typing import Any


def attach_scene_transcripts(scenes_bundle: dict[str, Any], stage_a: dict[str, Any]) -> dict[str, Any]:
    scenes = scenes_bundle["scenes"]
    segments = stage_a["align"]["aligned_segments"]

    # Round-robin segments across scenes by index (segments are time-ordered).
    by_scene: dict[str, list[Any]] = {scene["scene_id"]: [] for scene in scenes}
    scene_ids = list(by_scene.keys())
    for i, seg in enumerate(segments):
        by_scene[scene_ids[i % len(scene_ids)]].append(seg)

    enriched = [{**scene, "segments": by_scene[scene["scene_id"]]} for scene in scenes]
    return {"scenes": enriched}
