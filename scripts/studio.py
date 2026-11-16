#!/usr/bin/env python3
"""
Master Studio CLI for Antigravity Video Studio
Unifies Graphify Memory, Edge-TTS Audio Engine, Remotion Timeline,
and Smart Model Router with Prompt Compression & Zero-Cost Fallbacks.
"""

import sys
import os
import subprocess
import json

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
GRAPH_MEMORY = os.path.join(SCRIPTS_DIR, "graph_memory.py")
VOICEOVER = os.path.join(SCRIPTS_DIR, "make_voiceovers.py")
MODEL_ROUTER = os.path.join(SCRIPTS_DIR, "model_router.py")

def run_cmd(args):
    return subprocess.run(args, cwd=BASE_DIR)

def print_help():
    print("""
🎬 Antigravity Video Studio CLI

Usage:
  python3 scripts/studio.py init "<Film Title>"
  python3 scripts/studio.py status
  python3 scripts/studio.py clean "<noisy prompt>"
  python3 scripts/studio.py models
  python3 scripts/studio.py smart-scene <id> "<rough / noisy prompt>"
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

    if cmd == "init":
        title = sys.argv[2] if len(sys.argv) > 2 else "Autonomous AI Documentary"
        run_cmd([sys.executable, GRAPH_MEMORY, "init", title])
    elif cmd == "status":
        run_cmd([sys.executable, GRAPH_MEMORY, "status"])
    elif cmd == "models":
        run_cmd([sys.executable, MODEL_ROUTER, "status"])
    elif cmd == "clean":
        raw = " ".join(sys.argv[2:])
        run_cmd([sys.executable, MODEL_ROUTER, "clean", raw])
    elif cmd == "smart-scene":
        if len(sys.argv) < 4:
            print("Usage: python3 scripts/studio.py smart-scene <id> '<rough noisy prompt>'")
            sys.exit(1)
        sid = sys.argv[2]
        raw_prompt = " ".join(sys.argv[3:])
        
        # Import directly to run smart pipeline
        from model_router import PromptCompressor, ModelRouter
        compressor = PromptCompressor()
        router = ModelRouter()
        
        cleaned = compressor.clean_noisy_prompt(raw_prompt)
        print(f"🧹 Cleaned noisy prompt ({cleaned['estimated_token_savings']} token savings): '{cleaned['cleaned_prompt']}'")
        
        suggestion = router.suggest_tier(cleaned['cleaned_prompt'])
        print(f"💡 Suggested Model: {suggestion['recommended_provider']} ({suggestion['model']}) | Cost: {suggestion['estimated_cost']}")
        
        gen_result = router.generate_with_fallback(cleaned['cleaned_prompt'])
        
        # Parse generation output into scene parameters
        title = sid.replace("_", " ").title()
        narration = cleaned['cleaned_prompt']
        duration = cleaned['detected_duration']
        motion = cleaned['detected_motion']
        visual_prompt = f"Cinematic photorealistic documentary shot: {cleaned['cleaned_prompt']}, 35mm lens, 8k"
        
        if isinstance(gen_result.get("content"), str) and gen_result["content"].startswith("{"):
            try:
                parsed = json.loads(gen_result["content"])
                title = parsed.get("title", title)
                narration = parsed.get("narration", narration)
                visual_prompt = parsed.get("visualPrompt", visual_prompt)
                duration = parsed.get("duration", duration)
                motion = parsed.get("motion", motion)
            except Exception:
                pass

        # Add to Graphify memory
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
