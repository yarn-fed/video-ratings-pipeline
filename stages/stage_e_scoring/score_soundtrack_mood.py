"""Classify the soundtrack mood."""

from __future__ import annotations

from typing import Any

from mock_client import get_client


def score_soundtrack_mood(content: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    prompt = f"Classify the soundtrack mood.\nsummary={content['summary'][:64]}"
    mood = client.llm_large(prompt, output_schema="soundtrack_mood_v1")
    return {"soundtrack_mood": mood}
