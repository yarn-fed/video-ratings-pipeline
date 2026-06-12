"""Partition episode into act-level chunks for downstream stages."""

from __future__ import annotations

from typing import Any


def partition_episode(episode: dict[str, Any], frames_bundle: dict[str, Any]) -> dict[str, Any]:
    raw_partitions = episode["raw_metadata"].get("act_breaks", [])
    shots = frames_bundle["shots"]

    # Must stay sequential: act alignment depends on processing shots in order.
    partitions = []
    for shot_bundle in shots:
        shot = shot_bundle["shot"]
        midpoint = (shot["start_s"] + shot["end_s"]) / 2
        partition_label = "unknown"
        for p in raw_partitions:
            if p["start_s"] <= midpoint < p["end_s"]:
                partition_label = p["label"]
                break
        partitions.append({"shot_id": shot["shot_id"], "partition": partition_label})

    return {"partitions": partitions}
