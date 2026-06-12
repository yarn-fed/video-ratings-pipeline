# Performance Audit

_Last updated: a while ago. Numbers from the v2 era; re-audit is on the backlog._

We profiled a full run on the reference episode and broke down where wall-time
goes.

## Findings

- **Vision dominates.** Shot detection and per-shot frame analysis are the
  single biggest cost — roughly 60% of wall-time. The frame-analysis loop in
  `stage_a_ingest/extract_frames` is the worst offender and runs one call per
  shot, back to back.
- **Transcription is fixed cost.** Unavoidable and roughly proportional to
  runtime; not much to do here.
- **LLM calls are cheap.** At ~2–5 s each they're not worth optimising; batching
  them adds complexity for little gain.

## Recommendations (in priority order)

1. Parallelise the vision calls — this is where the time is.
2. Leave the language calls alone; they're already fast.
3. Don't bother micro-optimising the pure-Python steps; they're negligible.

If you only do one thing, fan out the vision calls.
