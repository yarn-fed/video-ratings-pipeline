# Movie Review Analytics — Episode Scoring Pipeline

Internal pipeline that turns a raw episode into a structured review: ingest the
media, analyse scenes and dialogue, score the creative domains, and emit a
review payload.  This is the candidate template — clone it, make `./score`
faster, keep the output valid.

## Running it

```bash
pip install -r requirements.txt
export TEST_TOKEN=...           # from your signup
export MOCK_BASE_URL=...        # the analysis API base URL from your dashboard
export SCORING_URL=...          # the scoring endpoint from your dashboard
./score                         # runs the pipeline and submits for an official score
```

`./score` runs the pipeline, submits the result, and prints the final review
payload plus your wall-time in seconds.  Lower is better.  We don't tell you
whether the output is right — judging that is part of the job.  Every run
replaces your previous one: **your last run is the one we read**, so finish on
the run you stand behind.

**A complete submission is two parts:** `./score` (your final run) and
`./feedback` — one thing you'd change about the product, and why.  Lead with an
area tag and keep it to one change in at most two sentences, e.g.
`API: paginate the reviews endpoint so large catalogs load.`  Run `./feedback`
when you're done; it uses the same `TEST_TOKEN`/`SCORING_URL`.

## How it's built

Six stages run top to bottom (`pipeline.py`):

| Stage | Package | What it does |
|-------|---------|--------------|
| A | `stages/stage_a_ingest` | fetch media, transcribe, align subtitles, partition |
| B | `stages/stage_b_foundational` | runtime, shots, logos, OCR, faces, summary |
| C | `stages/stage_c_scene` | cluster shots into scenes, previews, pacing |
| D | `stages/stage_d_thinking` | focus / creativity / memory / critical-thinking reads |
| E | `stages/stage_e_scoring` | plot, craft and audience domain scoring |
| F | `stages/stage_f_aggregation` | combine, rate, emit the review payload |

External calls (vision, transcription, LLM, storage) go through
`mock_client.py`, which talks to the sealed mock service.  We run a **small,
fast model** for the language calls — figure roughly **2–5 s per call** — so the
heavy lifting is in the vision passes.  See `PERFORMANCE.md` for the last audit.

## Notes

- The full output schema is documented in `PRODUCT_SPEC.md`.
- Product history is in `CHANGELOG.md`.
- `tests/` has the unit tests; run them with `pytest tests/`.
- Don't edit `mock_client.py`, `score`, or `feedback` — they mirror the sealed service.
