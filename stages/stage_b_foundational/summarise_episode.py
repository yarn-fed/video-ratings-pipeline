"""Produce a free-text episode summary used to ground later scoring prompts."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def summarise_episode(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    transcript = stage_a["transcribe"]["transcript"]
    joined = " ".join(seg["text"] for seg in transcript["segments"])

    prompt = (
        "Summarise this episode in three short paragraphs for an internal "
        f"reviewer.\ntranscript={joined}"
    )
    summary = client.llm(prompt, model="pro", output_schema="episode_summary_v1")
    return {"summary": summary}
