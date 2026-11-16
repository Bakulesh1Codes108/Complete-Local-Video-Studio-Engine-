#!/usr/bin/env python3
"""
Master Studio CLI for Antigravity Video Studio
Unifies Graphify Memory, Edge-TTS Audio Engine, and Remotion Timeline.
"""

import sys
import os
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
GRAPH_MEMORY = os.path.join(SCRIPTS_DIR, "graph_memory.py")
VOICEOVER = os.path.join(SCRIPTS_DIR, "make_voiceovers.py")

def run_cmd(args):
    return subprocess.run(args, cwd=BASE_DIR)

def print_help():
    print("""
🎬 Antigravity Video Studio CLI

Usage:
  python3 scripts/studio.py init "<Film Title>"
  python3 scripts/studio.py add-scene <id> "<title>" "<narration>" [duration_sec] [visual_prompt] [motion]
  python3 scripts/studio.py status
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
    elif cmd == "add-scene":
        if len(sys.argv) < 5:
            print("Usage: python3 scripts/studio.py add-scene <id> <title> <narration> [dur] [prompt] [motion]")
            sys.exit(1)
        run_cmd([sys.executable, GRAPH_MEMORY, "add-scene"] + sys.argv[2:])
        # Auto sync timeline after adding scene
        run_cmd([sys.executable, GRAPH_MEMORY, "export-timeline"])
    elif cmd == "status":
        run_cmd([sys.executable, GRAPH_MEMORY, "status"])
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
