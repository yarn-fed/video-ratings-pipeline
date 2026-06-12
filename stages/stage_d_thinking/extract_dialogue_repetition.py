"""Measure dialogue repetition across the transcript."""

from __future__ import annotations

from typing import Any

from mock_client import get_client
from stages.common import rubric_score


def extract_dialogue_repetition(stage_a: dict[str, Any]) -> dict[str, Any]:
    client = get_client()
    segments = stage_a["transcribe"]["transcript"]["segments"]
    joined = " ".join(seg["text"] for seg in segments)

    # Find repeated phrases.
    prompt = f"List the phrases repeated three or more times in:\n{joined}"
    reasoning = client.llm_large(prompt, output_schema="repetition_v1")

    bigrams: dict[str, int] = {}
    tokens = joined.split()
    for a, b in zip(tokens, tokens[1:]):
        bigrams[f"{a} {b}"] = bigrams.get(f"{a} {b}", 0) + 1

    score = rubric_score("repetition", sorted(bigrams.items()))
    return {"repetition_score": score, "repetition_reasoning": reasoning}
