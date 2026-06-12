"""Persist the detected shots to blob storage for downstream stages."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def export_shots(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    shots = [sb["shot"] for sb in stage_a["frames"]["shots"]]
    ref = client.blob_put(f"shots/{stage_a['fetch']['episode_id']}.json", shots)
    return {"export_ref": ref, "n_shots": len(shots)}
