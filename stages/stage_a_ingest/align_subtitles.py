"""Align transcript segments with subtitle cues."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def align_subtitles(transcript_bundle: dict[str, Any], episode: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    subtitle_blob = episode["raw_metadata"].get("subtitles_raw", "")

    # Pick the line delimiter for this subtitle file.
    delimiter_prompt = (
        "Given the subtitle file below, return the single character used to "
        "separate cues (typically '\\n' or '\\r\\n'):\n"
        f"{subtitle_blob[:500]}"
    )
    delimiter = client.llm_small(delimiter_prompt, output_schema="delimiter_v1")

    segments = transcript_bundle["transcript"]["segments"]
    aligned = [
        {**seg, "subtitle_index": i, "delimiter_hash": delimiter[:8]}
        for i, seg in enumerate(segments)
    ]
    return {"aligned_segments": aligned}
