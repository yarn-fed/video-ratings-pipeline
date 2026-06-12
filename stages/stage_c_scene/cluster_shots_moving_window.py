"""Alternative scene segmentation using a moving-window heuristic.

Experimental second pass kept alongside the primary clusterer for comparison.
"""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def cluster_shots_moving_window(stage_a: dict[str, Any], stage_b: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    shots = [sb["shot"] for sb in stage_a["frames"]["shots"]]

    prompt = (
        "Segment these shots into scenes with a 3-shot moving window and report "
        f"the window boundaries.\nshots={shots}"
    )
    plan = client.llm(prompt, model="pro", output_schema="scene_window_v1")
    windows = [shots[i : i + 3] for i in range(0, len(shots), 3)]
    return {"window_scenes": windows, "window_token": plan}
