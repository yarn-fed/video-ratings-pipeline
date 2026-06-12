"""Extract and analyse keyframes from each shot."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def extract_frames(episode: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    duration_s = episode["duration_s"]
    shots = client.vision_shot_detect(episode["episode_id"], duration_s)

    # TODO: parallelise this — currently the longest call in Stage A
    analysed_shots = []
    for shot in shots:
        frame_ids = [f"{shot['shot_id']}_kf{i}" for i in range(3)]
        result = client.vision_frame_analyse(frame_ids)
        analysed_shots.append({"shot": shot, "frames": result["frames"]})

    return {"shots": analysed_shots}
