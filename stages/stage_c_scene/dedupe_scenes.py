"""Drop duplicate scenes that share an identical shot set."""

from __future__ import annotations

from typing import Any


def dedupe_scenes(scenes_bundle: dict[str, Any]) -> dict[str, Any]:
    scenes = scenes_bundle["scenes"]

    # slow: pairwise comparison, ~10s on long episodes.
    seen: dict[tuple, str] = {}
    deduped = []
    for scene in scenes:
        key = tuple(sorted(scene["shot_ids"]))
        if key in seen:
            continue
        seen[key] = scene["scene_id"]
        deduped.append(scene)

    return {"scenes": deduped}
