"""Score the pacing of each scene."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def score_scene_pacing(scenes_bundle: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    scenes = scenes_bundle["scenes"]

    # Ask the model for a holistic pacing read across the scene set.
    prompt = "Rate the pacing of each scene from the shot counts:\n" + str(
        [(s["scene_id"], len(s["shot_ids"])) for s in scenes]
    )
    client.llm(prompt, model="pro", output_schema="pacing_v1")

    pacing = {s["scene_id"]: rubric_score("pacing", s["scene_id"], len(s["shot_ids"])) for s in scenes}
    return {"scene_pacing": pacing}
