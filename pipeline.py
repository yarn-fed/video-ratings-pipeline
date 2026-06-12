"""Top-level pipeline orchestrator.

Runs the six stages in order; each stage's output feeds the next.  Everything
runs in-process and serially.
"""

from __future__ import annotations

from typing import Any

from stages.common import frame_signature, transcript_signature
from stages.stage_a_ingest import (
    align_subtitles,
    extract_frames,
    fetch_episode,
    partition_episode,
    transcribe_audio,
)
from stages.stage_b_foundational import (
    detect_explicit_content,
    detect_face_tracks,
    detect_logos,
    detect_shot_changes,
    detect_text_on_screen,
    export_shots,
    extract_runtime,
    summarise_episode,
)
from stages.stage_c_scene import (
    assemble_scene_previews,
    attach_scene_transcripts,
    cluster_shots_moving_window,
    cluster_shots_to_scenes,
    dedupe_scenes,
    score_scene_pacing,
)
from stages.stage_d_thinking import (
    extract_dialogue_repetition,
    score_creative_thinking,
    score_critical_thinking,
    score_fantastical_intensity,
    score_focus_cues,
    score_memory_demand,
)
from stages.stage_e_scoring import (
    aggregate_audience,
    aggregate_craft,
    aggregate_plot,
    score_age_appropriateness,
    score_character_arc,
    score_cinematography,
    score_demographic_fit,
    score_dialogue_quality,
    score_editing,
    score_emotional_impact,
    score_lighting,
    score_pacing,
    score_plot_coherence,
    score_quotability,
    score_rewatch_value,
    score_sound_design,
    score_soundtrack_mood,
    score_subtext,
    score_themes,
)
from stages.stage_f_aggregation import (
    combine_domain_scores,
    compute_overall_rating,
    emit_review_payload,
)


def run_pipeline(episode_input: dict[str, Any]) -> dict[str, Any]:
    # --- Stage A: ingest ---------------------------------------------------
    fetch = fetch_episode(episode_input)
    frames = extract_frames(fetch)
    transcribe = transcribe_audio(fetch)
    align = align_subtitles(transcribe, fetch)
    partition = partition_episode(fetch, frames)
    stage_a = {
        "fetch": fetch,
        "frames": frames,
        "transcribe": transcribe,
        "align": align,
        "partition": partition,
    }

    # --- Stage B: foundational analysis ------------------------------------
    runtime = extract_runtime(stage_a)
    detect_shot_changes(stage_a)
    export_shots(stage_a)
    logos = detect_logos(stage_a)
    explicit = detect_explicit_content(stage_a)
    on_screen_text = detect_text_on_screen(stage_a, logos)
    faces = detect_face_tracks(stage_a, on_screen_text)
    summary = summarise_episode(stage_a)
    stage_b = {
        "summary": summary,
        "faces": faces,
        "explicit": explicit,
        "logos": logos,
        "on_screen_text": on_screen_text,
    }

    # --- Stage C: scene/shot -----------------------------------------------
    clustered = cluster_shots_to_scenes(stage_a, stage_b)
    cluster_shots_moving_window(stage_a, stage_b)
    assemble_scene_previews(clustered)
    attached = attach_scene_transcripts(clustered, stage_a)
    score_scene_pacing(attached)
    deduped = dedupe_scenes(attached)
    stage_c = {"scenes": deduped["scenes"]}

    # --- Stage D: thinking/connection --------------------------------------
    repetition = extract_dialogue_repetition(stage_a)
    focus = score_focus_cues(stage_c, stage_a)
    fantastical = score_fantastical_intensity(stage_b)
    creative = score_creative_thinking(stage_c)
    memory = score_memory_demand(stage_c)
    critical = score_critical_thinking(stage_c)
    thinking = {**repetition, **focus, **creative, **memory, **critical}

    # --- Stage E: domain scoring -------------------------------------------
    content = {
        "episode_id": fetch["episode_id"],
        "duration_s": fetch["duration_s"],
        "n_scenes": len(stage_c["scenes"]),
        "n_shots": len(frames["shots"]),
        "n_segments": len(align["aligned_segments"]),
        "transcript_signature": transcript_signature(transcribe["transcript"]),
        "frame_signature": frame_signature(frames),
        "summary": summary["summary"],
        "fantastical_intensity": fantastical["fantastical_intensity"],
        "face_track_ids": faces["face_track_ids"],
        "explicit_flag": explicit["explicit_flag"],
    }

    plot_parts = {
        **score_plot_coherence(content),
        **score_pacing(content),
        **score_dialogue_quality(content),
        **score_character_arc(content),
        **score_subtext(content),
    }
    themes = score_themes(content)
    plot_agg = aggregate_plot(plot_parts)

    craft_parts = {
        **score_cinematography(content),
        **score_editing(content),
        **score_sound_design(content),
        **score_lighting(content),
        **score_soundtrack_mood(content),
    }
    craft_agg = aggregate_craft(craft_parts)

    audience_parts = {
        **score_emotional_impact(content),
        **score_rewatch_value(content),
        **score_age_appropriateness(content),
        **score_quotability(content),
        **score_demographic_fit(content),
    }
    audience_agg = aggregate_audience(audience_parts)

    # --- Stage F: aggregation ----------------------------------------------
    extras = {
        "soundtrack_mood": craft_parts.get("soundtrack_mood"),
        "theme_tags": themes["theme_tags"],
        "demographic_fit": audience_parts.get("demographic_fit"),
        "logos": logos["detected_logos_v1"],
        "on_screen_text": on_screen_text["extracted_on_screen_text_v2"],
        "face_tracks": faces["face_track_ids"],
        "fantastical_intensity": fantastical["fantastical_intensity"],
        "runtime_minutes": runtime["runtime_minutes"],
    }
    combined = combine_domain_scores(
        stage_a, stage_c, thinking, plot_agg, craft_agg, audience_agg, extras
    )
    rating = compute_overall_rating(combined)
    payload = emit_review_payload(combined, rating)
    return payload
