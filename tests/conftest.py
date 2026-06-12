"""Shared pytest fixtures.

Tests run against an in-process fake of the service client, so they're fast and
need no network or token.  The fake returns deterministic placeholder shapes; it
is not the hosted service and won't reproduce official scores.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import mock_client  # noqa: E402


def _h(*parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()


class FakeClient:
    """Deterministic, in-process stand-in for the service client."""

    def __init__(self) -> None:
        self.calls: dict[str, int] = {}

    def _count(self, method: str) -> None:
        self.calls[method] = self.calls.get(method, 0) + 1

    def blob_fetch(self, key: str) -> dict[str, Any]:
        self._count("blob_fetch")
        return {"key": key, "blob_hash": _h(key), "size_bytes": 12_345_678}

    def blob_put(self, key: str, data: Any) -> dict[str, Any]:
        self._count("blob_put")
        return {"key": key, "etag": _h(key, data)[:16]}

    def vision_shot_detect(self, video_id: str, duration_s: float) -> list[dict[str, Any]]:
        self._count("vision_shot_detect")
        d = int(duration_s)
        seed = _h(video_id, d)
        n = 8 + (int(seed[:4], 16) % 5)
        bounds = sorted({(int(seed[i : i + 4], 16) % d) for i in range(0, n * 4, 4)})
        bounds = sorted(set([0, *bounds, d]))
        return [
            {"shot_id": f"{video_id}_shot_{i}", "start_s": bounds[i], "end_s": bounds[i + 1]}
            for i in range(len(bounds) - 1)
        ]

    def vision_frame_analyse(self, frame_ids: list[str]) -> dict[str, Any]:
        self._count("vision_frame_analyse")
        return {"frames": [{"frame_id": f, "scene_label": _h(f)[:8], "objects": [_h(f, "o")[:6]]} for f in frame_ids]}

    def vision_logo_detect(self, video_id: str, duration_s: float) -> dict[str, Any]:
        self._count("vision_logo_detect")
        return {"logos": [_h(video_id, "logo", i)[:6] for i in range(3)]}

    def vision_explicit_detect(self, video_id: str, duration_s: float) -> dict[str, Any]:
        self._count("vision_explicit_detect")
        seed = int(_h(video_id, "explicit")[:4], 16)
        return {"explicit": seed % 5 == 0, "confidence": (seed % 100) / 100.0}

    def vision_text_detect(self, video_id: str, duration_s: float) -> dict[str, Any]:
        self._count("vision_text_detect")
        return {"on_screen_text": [_h(video_id, "ocr", i)[:10] for i in range(4)]}

    def vision_face_detect(self, video_id: str, duration_s: float) -> dict[str, Any]:
        self._count("vision_face_detect")
        return {"face_tracks": [_h(video_id, "face", i)[:8] for i in range(5)]}

    def transcribe(self, audio_id: str, duration_s: float, enable_diarization: bool = True) -> dict[str, Any]:
        self._count("transcribe")
        d = int(duration_s)
        n = 8 + (int(_h(audio_id, d)[:4], 16) % 6)
        return {
            "audio_id": audio_id,
            "language": "en",
            "segments": [
                {
                    "start_s": d * i // n,
                    "end_s": d * (i + 1) // n,
                    "text": _h(audio_id, i)[:32],
                    "speaker": (f"S{i % 3}" if enable_diarization else None),
                }
                for i in range(n)
            ],
        }

    def llm(self, prompt: str, *, model: str = "pro", output_schema: str | None = None) -> str:
        self._count("llm")
        return _h(prompt, output_schema)

    def llm_large(self, prompt: str, *, output_schema: str | None = None) -> str:
        return self.llm(prompt, model="pro", output_schema=output_schema)

    def llm_medium(self, prompt: str, *, output_schema: str | None = None) -> str:
        return self.llm(prompt, model="flash", output_schema=output_schema)

    def llm_small(self, prompt: str, *, output_schema: str | None = None) -> str:
        return self.llm(prompt, model="nano", output_schema=output_schema)


@pytest.fixture(autouse=True)
def fake_client() -> FakeClient:
    client = FakeClient()
    mock_client._default_client = client
    return client


@pytest.fixture
def episode_input() -> dict:
    with open(ROOT / "fixtures" / "episode_001.json") as f:
        return json.load(f)
