#!/usr/bin/env python3
"""
Master Studio CLI for Antigravity Video Studio
Unifies:
  - Graphify Context Memory (<6 KB)
  - Remotion + GSAP Deterministic Render Core
  - Open Higgsfield Camera Motion Rigs (Orbit 360, FPV Dive, Vertigo)
  - Three.js 3D Procedural Scenes (Globe, Particles, Isometric Chart)
  - Manim Mathematical & Scientific Animation Dispatcher
  - Blender Headless 3D Render Engine
  - Reel Mimic Viral Video Pacing Cloner (Hormozi, Vox, MrBeast)
  - Visual RPA Automation Pipeline & UI
  - DaVinci Resolve Color Science & OpenCut J-Cuts
"""

import sys
import os
import subprocess
import json
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

GRAPH_MEMORY = os.path.join(SCRIPTS_DIR, "graph_memory.py")
GRAPH_EDITOR = os.path.join(SCRIPTS_DIR, "graph_editor.py")
VOICEOVER = os.path.join(SCRIPTS_DIR, "make_voiceovers.py")
MODEL_ROUTER = os.path.join(SCRIPTS_DIR, "model_router.py")
DIRECTOR_PRESETS = os.path.join(SCRIPTS_DIR, "director_presets.py")
DEVICE_ADVISOR = os.path.join(SCRIPTS_DIR, "device_advisor.py")
QUICKSTART = os.path.join(SCRIPTS_DIR, "quickstart.py")
REEL_MIMIC = os.path.join(SCRIPTS_DIR, "reel_mimic.py")
BLENDER_ENGINE = os.path.join(SCRIPTS_DIR, "blender_engine.py")
MANIM_ENGINE = os.path.join(SCRIPTS_DIR, "manim_engine.py")
RPA_SERVER = os.path.join(SCRIPTS_DIR, "rpa_server.py")

def run_cmd(args):
    return subprocess.run(args, cwd=BASE_DIR)

def extract_json_from_llm(text: str) -> dict:
    if not text:
        return {}
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    return {}

def print_help():
    print("""
🎬 Antigravity Video Studio CLI (Multi-Engine & RPA Pipeline)

Usage:
  python3 scripts/studio.py rpa                         [Launch Visual RPA Automation UI]
  python3 scripts/studio.py quickstart "<story idea>"   [1-Click full film generator]
  python3 scripts/studio.py mimic <preset> "<topic>"    [Clone viral pacing: hormozi | vox | mrbeast]
  python3 scripts/studio.py blender [type] [title]      [Headless 3D Blender render: 3d_chrome_title]
  python3 scripts/studio.py manim [type] [id]           [3Blue1Brown math render: neural_network | quantum_formula]
  python3 scripts/studio.py advisor                     [Hardware, RAM & disk space advisor]
  python3 scripts/studio.py models                      [Check local Llama / OpenRouter / Gemini]
  python3 scripts/studio.py presets                     [List DaVinci cinematic color palettes]
  python3 scripts/studio.py clean "<noisy prompt>"      [Compress prompt & save 30-70% tokens]
  python3 scripts/studio.py edit "<edit command>"       [Prompt-driven graph memory editor]
  python3 scripts/studio.py director-scene <id> "<idea>" [preset] [Add scene with DaVinci grade & J-Cut]
  python3 scripts/studio.py smart-scene <id> "<prompt>" [Smart model router scene generation]
  python3 scripts/studio.py status                      [View live film reel report]
  python3 scripts/studio.py audio [voice_name]          [Generate free Microsoft Neural voiceovers]
  python3 scripts/studio.py preview                     [Open in-editor Remotion Player]
  python3 scripts/studio.py render                      [Render broadcast MP4]
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "rpa":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        run_cmd([sys.executable, RPA_SERVER, str(port)])
    elif cmd == "mimic":
        pname = sys.argv[2] if len(sys.argv) > 2 else "alex_hormozi_viral_reel"
        topic = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "AI Video Revolution"
        run_cmd([sys.executable, REEL_MIMIC, pname, topic])
    elif cmd == "blender":
        stype = sys.argv[2] if len(sys.argv) > 2 else "3d_chrome_title"
        title = sys.argv[3] if len(sys.argv) > 3 else "FUTURE CINEMA"
        run_cmd([sys.executable, BLENDER_ENGINE, stype, title])
    elif cmd == "manim":
        stype = sys.argv[2] if len(sys.argv) > 2 else "neural_network"
        sid = sys.argv[3] if len(sys.argv) > 3 else "manim_01"
        run_cmd([sys.executable, MANIM_ENGINE, stype, sid])
    elif cmd in ["advisor", "doctor", "sysinfo"]:
        run_cmd([sys.executable, DEVICE_ADVISOR])
    elif cmd in ["quickstart", "generate"]:
        prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "The mystery of deep space radio bursts"
        run_cmd([sys.executable, QUICKSTART, prompt])
    elif cmd == "init":
        title = sys.argv[2] if len(sys.argv) > 2 else "Autonomous AI Documentary"
        run_cmd([sys.executable, GRAPH_MEMORY, "init", title])
    elif cmd == "status":
        run_cmd([sys.executable, GRAPH_MEMORY, "status"])
    elif cmd == "models":
        run_cmd([sys.executable, MODEL_ROUTER, "status"])
    elif cmd == "presets":
        run_cmd([sys.executable, DIRECTOR_PRESETS])
    elif cmd == "clean":
        raw = " ".join(sys.argv[2:])
        run_cmd([sys.executable, MODEL_ROUTER, "clean", raw])
    elif cmd == "edit":
        if len(sys.argv) < 3:
            print("Usage: python3 scripts/studio.py edit '<natural language edit command>'")
            sys.exit(1)
        instruction = " ".join(sys.argv[2:])
        run_cmd([sys.executable, GRAPH_EDITOR, "prompt", instruction])
    elif cmd == "director-scene":
        if len(sys.argv) < 4:
            print("Usage: python3 scripts/studio.py director-scene <id> '<rough concept>' [preset_name]")
            sys.exit(1)
        sid = sys.argv[2]
        raw_concept = sys.argv[3]
        preset = sys.argv[4] if len(sys.argv) > 4 else "netflix-doc"

        from model_router import PromptCompressor
        compressor = PromptCompressor()
        cleaned = compressor.clean_noisy_prompt(raw_concept)
        print(f"🧹 Cleaned Concept ({cleaned['estimated_token_savings']} token savings): '{cleaned['cleaned_prompt']}'")

        from director_presets import enhance_prompt
        enhanced = enhance_prompt(cleaned['cleaned_prompt'], preset)
        print(f"🎨 Applied DaVinci Preset: {enhanced['preset_title']} ({enhanced['colorGrade']}, J-Cut: {enhanced['jCutFrames']} frames)")

        title = sid.replace("_", " ").title()
        narration = cleaned['cleaned_prompt']
        dur = cleaned['detected_duration']
        motion = cleaned['detected_motion']
        vp = enhanced['enhanced_visual_prompt']

        run_cmd([sys.executable, GRAPH_MEMORY, "add-scene", sid, title, narration, str(dur), vp, motion])
        run_cmd([sys.executable, GRAPH_MEMORY, "export-timeline"])
        print(f"✨ Scene [{sid}] saved with {preset} cinematic color grade and J-Cut pacing!")

    elif cmd == "smart-scene":
        if len(sys.argv) < 4:
            print("Usage: python3 scripts/studio.py smart-scene <id> '<rough noisy prompt>'")
            sys.exit(1)
        sid = sys.argv[2]
        raw_prompt = " ".join(sys.argv[3:])
        
        from model_router import PromptCompressor, ModelRouter
        compressor = PromptCompressor()
        router = ModelRouter()
        
        cleaned = compressor.clean_noisy_prompt(raw_prompt)
        print(f"🧹 Cleaned noisy prompt ({cleaned['estimated_token_savings']} token savings): '{cleaned['cleaned_prompt']}'")
        
        suggestion = router.suggest_tier(cleaned['cleaned_prompt'])
        print(f"💡 Suggested Model: {suggestion['recommended_provider']} ({suggestion['model']}) | Cost: {suggestion['estimated_cost']}")
        
        gen_result = router.generate_with_fallback(cleaned['cleaned_prompt'])
        
        title = sid.replace("_", " ").title()
        narration = cleaned['cleaned_prompt']
        duration = cleaned['detected_duration']
        motion = cleaned['detected_motion']
        visual_prompt = f"Cinematic photorealistic documentary shot: {cleaned['cleaned_prompt']}, 35mm lens, 8k"
        
        parsed = extract_json_from_llm(str(gen_result.get("content", "")))
        if parsed:
            title = parsed.get("title", title)
            narration = parsed.get("narration", narration)
            visual_prompt = parsed.get("visualPrompt", visual_prompt)
            duration = parsed.get("duration", duration)
            motion = parsed.get("motion", motion)

        run_cmd([sys.executable, GRAPH_MEMORY, "add-scene", sid, title, narration, str(duration), visual_prompt, motion])
        run_cmd([sys.executable, GRAPH_MEMORY, "export-timeline"])
        print(f"✨ Successfully integrated [{sid}] via smart router into Graphify Memory & Remotion Timeline!")

    elif cmd == "add-scene":
        if len(sys.argv) < 5:
            print("Usage: python3 scripts/studio.py add-scene <id> <title> <narration> [dur] [prompt] [motion]")
            sys.exit(1)
        run_cmd([sys.executable, GRAPH_MEMORY, "add-scene"] + sys.argv[2:])
        run_cmd([sys.executable, GRAPH_MEMORY, "export-timeline"])
    elif cmd == "sync":
        run_cmd([sys.executable, GRAPH_MEMORY, "export-timeline"])
    elif cmd == "audio":
        voice = sys.argv[2] if len(sys.argv) > 2 else "en-US-ChristopherNeural"
        run_cmd([sys.executable, VOICEOVER, voice])
    elif cmd == "preview":
        run_cmd(["npx", "remotion", "preview", "src/index.ts"])
    elif cmd == "render":
        run_cmd(["npx", "remotion", "render", "src/index.ts", "Documentary", "out/documentary.mp4"])
    else:
        print_help()
