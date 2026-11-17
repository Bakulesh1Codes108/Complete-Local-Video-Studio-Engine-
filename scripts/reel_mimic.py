#!/usr/bin/env python3
"""
Reel Mimic Engine for Antigravity Video Studio.
Analyzes viral video pacing, audio energy beats, and aspect ratios
to clone viral reel structures and apply them to new AI prompts.
"""

import sys
import os
import json
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
GRAPH_MEMORY = os.path.join(SCRIPTS_DIR, "graph_memory.py")

VIRAL_PRESETS = {
    "alex_hormozi_viral_reel": {
        "title": "Alex Hormozi High-Retention Reel",
        "aspectRatio": "9:16",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "averageCutSeconds": 2.2,
        "subtitleStyle": "kinetic_single_word_bounce",
        "colorGrade": "clean",
        "higgsfieldMotion": "whip_pan",
        "musicDucking": 0.25,
        "structure": [
            {"beat": "Aggressive Contrarian Hook", "duration": 2.0, "motion": "zoom-in", "higgsfield": "crash_zoom"},
            {"beat": "The False Belief Callout", "duration": 2.2, "motion": "pan-left", "higgsfield": "handheld_subtle"},
            {"beat": "The Hidden Real Truth", "duration": 2.4, "motion": "zoom-in", "higgsfield": "bullet_time_freeze"},
            {"beat": "Concrete 1-2 Action Step", "duration": 2.6, "motion": "pan-right", "higgsfield": "orbit_360"},
            {"beat": "Punchline / Follow Call-to-Action", "duration": 2.0, "motion": "zoom-out", "higgsfield": "fpv_drone_dive"}
        ]
    },
    "vox_highlighter_explainer": {
        "title": "Vox Data & Geopolitics Explainer",
        "aspectRatio": "16:9",
        "width": 1920,
        "height": 1080,
        "fps": 30,
        "averageCutSeconds": 3.8,
        "subtitleStyle": "yellow_highlighter_box",
        "colorGrade": "clean",
        "higgsfieldMotion": "crane_up_reveal",
        "musicDucking": 0.18,
        "structure": [
            {"beat": "Historical Mystery Hook", "duration": 3.5, "motion": "zoom-in", "higgsfield": "crane_up_reveal"},
            {"beat": "The 3D Map / Data Perspective", "duration": 4.2, "motion": "pan-left", "higgsfield": "orbit_360", "engine": "threejs"},
            {"beat": "The Unseen Economic Factor", "duration": 3.8, "motion": "pan-right", "higgsfield": "handheld_subtle"},
            {"beat": "Modern Consequence", "duration": 4.0, "motion": "zoom-out", "higgsfield": "vertigo_dolly_zoom"}
        ]
    },
    "mrbeast_retention_hook": {
        "title": "MrBeast Hyper-Retention Fast Cut",
        "aspectRatio": "9:16",
        "width": 1080,
        "height": 1920,
        "fps": 30,
        "averageCutSeconds": 1.6,
        "subtitleStyle": "bold_outlined_pop",
        "colorGrade": "teal-and-orange",
        "higgsfieldMotion": "fpv_drone_dive",
        "musicDucking": 0.28,
        "structure": [
            {"beat": "Extreme Premise in 1 Second", "duration": 1.5, "motion": "zoom-in", "higgsfield": "fpv_drone_dive"},
            {"beat": "High Stakes Explanation", "duration": 1.8, "motion": "pan-left", "higgsfield": "whip_pan"},
            {"beat": "Countdown / Tension Build", "duration": 1.6, "motion": "zoom-in", "higgsfield": "bullet_time_freeze"},
            {"beat": "Unexpected Twist", "duration": 1.9, "motion": "pan-right", "higgsfield": "orbit_360"}
        ]
    }
}

def mimic_reel(preset_name: str, new_topic: str):
    preset = VIRAL_PRESETS.get(preset_name, VIRAL_PRESETS["alex_hormozi_viral_reel"])
    print("=" * 65)
    print(f"🧬 REEL MIMIC: Cloning Viral Structure: '{preset['title']}'")
    print(f"📐 Aspect Ratio: {preset['aspectRatio']} ({preset['width']}x{preset['height']}) @ {preset['fps']} FPS")
    print(f"⏱️ Pacing: ~{preset['averageCutSeconds']}s per cut | Motion Rig: {preset['higgsfieldMotion']}")
    print("=" * 65)

    timeline_scenes = []
    fps = preset["fps"]

    for i, s in enumerate(preset["structure"]):
        sid = f"mimic_{i+1:02d}"
        dur_sec = s["duration"]
        frames = int(dur_sec * fps)
        subtitle_text = f"{s['beat']}: {new_topic}"
        engine_type = s.get("engine", "remotion")

        scene_obj = {
            "id": sid,
            "durationInFrames": frames,
            "engine": engine_type,
            "voiceover": f"assets/audio/{sid}.mp3",
            "visual": f"assets/visuals/{sid}.jpg",
            "subtitle": subtitle_text,
            "motion": s["motion"],
            "higgsfieldMotion": s.get("higgsfield", preset["higgsfieldMotion"]),
            "colorGrade": preset["colorGrade"],
            "threeJsScene": "3d_rotating_globe" if engine_type == "threejs" else None,
            "jCutFrames": 8
        }
        timeline_scenes.append(scene_obj)

    timeline_data = {
        "project": f"Mimic: {preset['title']} - {new_topic[:30]}",
        "fps": preset["fps"],
        "width": preset["width"],
        "height": preset["height"],
        "letterbox": False if preset["aspectRatio"] == "9:16" else True,
        "defaultColorGrade": preset["colorGrade"],
        "scenes": timeline_scenes
    }

    out_timeline = os.path.join(BASE_DIR, "timeline.json")
    with open(out_timeline, "w", encoding="utf-8") as f:
        json.dump(timeline_data, f, indent=2)

    print(f"✨ Successfully cloned viral pacing into: {out_timeline}")
    print(f"🎬 Total Scenes: {len(timeline_scenes)} | Total Duration: {sum(s['durationInFrames'] for s in timeline_scenes)/fps:.1f}s")
    print("To preview immediately:")
    print("  npm run preview")
    return timeline_data

if __name__ == "__main__":
    pname = sys.argv[1] if len(sys.argv) > 1 else "alex_hormozi_viral_reel"
    topic = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "How Artificial Intelligence is Automating Filmmaking in 2026"

    if pname == "list":
        print("Available Viral Reel Templates to Mimic:")
        for k, v in VIRAL_PRESETS.items():
            print(f"  • {k:28} -> {v['title']} ({v['aspectRatio']}, ~{v['averageCutSeconds']}s cuts)")
        sys.exit(0)

    mimic_reel(pname, topic)
