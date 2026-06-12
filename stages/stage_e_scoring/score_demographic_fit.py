"""Estimate which demographics the episode fits best."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def score_demographic_fit(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = (
        "Estimate the best-fit demographics from the recurring faces.\n"
        f"face_tracks={content.get('face_track_ids')}"
    )
    fit = client.llm_large(prompt, output_schema="demographic_fit_v1")
    return {"demographic_fit": fit}
