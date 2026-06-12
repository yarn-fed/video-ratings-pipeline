"""Assemble and emit the final review payload."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def emit_review_payload(combined: dict[str, Any], rating: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    payload = {
        "episode_id": combined["episode_id"],
        "overall_rating": rating["overall_rating"],
        "scores": {
            "plot": combined["plot_score"],
            "craft": combined["craft_score"],
            "audience": combined["audience_score"],
        },
        "thinking": combined["thinking"],
        "stats": {
            "n_shots": combined["n_shots"],
            "n_scenes": combined["n_scenes"],
            "n_segments": combined["n_segments"],
            "transcript_signature": combined["transcript_signature"],
        },
        "summary": rating["summary"],
        "details": combined["details"],
        "deprecated": combined["deprecated"],
    }

    client.blob_put(f"reviews/{payload['episode_id']}.json", payload)
    return payload
