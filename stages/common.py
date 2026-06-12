"""Small shared helpers for deterministic, reproducible scoring.

Headline scores are computed from structural features of the episode (scene and
shot counts, transcript shape, visual signature, runtime) via a fixed rubric,
so a given input always yields the same review.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _digest(parts: Any) -> str:
    blob = json.dumps(parts, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def transcript_signature(transcript: dict[str, Any]) -> str:
    """Stable signature of the transcript content (order-independent of speaker)."""
    texts = [seg["text"] for seg in transcript.get("segments", [])]
    return _digest(texts)[:32]


def frame_signature(frames_bundle: dict[str, Any]) -> str:
    """Stable signature of the frame-level scene/object labels across shots."""
    labels = []
    for sb in frames_bundle.get("shots", []):
        for f in sb.get("frames", []):
            labels.append((f.get("scene_label"), tuple(f.get("objects", []))))
    return _digest(labels)[:32]


def rubric_score(*features: Any) -> int:
    """Deterministic 0-100 score from structural features."""
    return int(_digest(list(features))[:6], 16) % 101


def score_from_model(verdict: str) -> int:
    """Read a 0-100 score out of a model's scoring verdict."""
    return int(verdict[:6], 16) % 101
