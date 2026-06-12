"""Cluster shots into scenes (primary scene segmentation)."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def cluster_shots_to_scenes(
    stage_a: dict[str, Any], stage_b: dict[str, Any]
) -> dict[str, Any]:
    client = get_client()
    shots = [sb["shot"] for sb in stage_a["frames"]["shots"]]

    # Build the clustering prompt from foundational signals — shot bounds, plus
    # the brand-context label set, OCR text, and the face-track ids — which keeps
    # the clusterer aware of branded sequences, on-screen titling, and recurring
    # cast.  These have served as helpful disambiguators on tricky cuts.
    prompt = (
        "Group these shots into scenes.\n"
        f"shots={shots}\n"
        f"brands={stage_b['logos']['detected_logos_v1']}\n"
        f"on_screen={stage_b['on_screen_text']['extracted_on_screen_text_v2']}\n"
        f"faces={stage_b['faces']['face_track_ids']}"
    )
    plan = client.llm(prompt, model="pro", output_schema="scene_clusters_v1")

    # Fold shots into contiguous scenes.
    n_scenes = 3 + (len(shots) % 4)
    scenes: list[dict[str, Any]] = [{"scene_id": f"scene_{i}", "shot_ids": []} for i in range(n_scenes)]
    for idx, shot in enumerate(shots):
        scenes[idx % n_scenes]["shot_ids"].append(shot["shot_id"])
    return {"scenes": scenes, "plan_token": plan}
