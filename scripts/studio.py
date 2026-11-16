#!/usr/bin/env python3
"""
Master Studio CLI for Antigravity Video Studio
Unifies Graphify Memory, Edge-TTS Audio Engine, Remotion Timeline,
Smart Model Router, DaVinci Cinematic Grading & Hardware Space Advisor.
"""

import sys
import os
import subprocess
import json
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)

# Ensure scripts directory is on sys.path for direct imports
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

GRAPH_MEMORY = os.path.join(SCRIPTS_DIR, "graph_memory.py")
GRAPH_EDITOR = os.path.join(SCRIPTS_DIR, "graph_editor.py")
VOICEOVER = os.path.join(SCRIPTS_DIR, "make_voiceovers.py")
MODEL_ROUTER = os.path.join(SCRIPTS_DIR, "model_router.py")
DIRECTOR_PRESETS = os.path.join(SCRIPTS_DIR, "director_presets.py")
DEVICE_ADVISOR = os.path.join(SCRIPTS_DIR, "device_advisor.py")
QUICKSTART = os.path.join(SCRIPTS_DIR, "quickstart.py")

def run_cmd(args):
    return subprocess.run(args, cwd=BASE_DIR)

def extract_json_from_llm(text: str) -> dict:
    """Robustly extracts JSON from raw LLM responses or Markdown code blocks."""
    if not text:
        return {}
    # Look for ```json ... ``` or { ... }
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    # Look for raw { ... }
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    return {}

def print_help():
    print("""
🎬 Antigravity Video Studio CLI

Usage:
  python3 scripts/studio.py quickstart "<story idea>"   [1-Click full film generator]
  python3 scripts/studio.py advisor                     [Hardware & disk space analysis]
  python3 scripts/studio.py init "<Film Title>"
  python3 scripts/studio.py status
  python3 scripts/studio.py models
  python3 scripts/studio.py presets
  python3 scripts/studio.py clean "<noisy prompt>"
  python3 scripts/studio.py edit "<natural language edit command>"
  python3 scripts/studio.py director-scene <id> "<rough idea>" [preset_name]
  python3 scripts/studio.py smart-scene <id> "<rough prompt>"
  python3 scripts/studio.py add-scene <id> "<title>" "<narration>" [dur] [prompt] [motion]
  python3 scripts/studio.py sync
  python3 scripts/studio.py audio [voice_name]
  python3 scripts/studio.py preview
  python3 scripts/studio.py render
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ["advisor", "doctor", "sysinfo"]:
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
            print("Examples:")
            print("  python3 scripts/studio.py edit 'make scene_01 8 seconds and zoom-in'")
            print("  python3 scripts/studio.py edit 'change subtitle of scene_02 to The world changed forever'")
            print("  python3 scripts/studio.py edit 'switch global style to netflix-doc'")
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
