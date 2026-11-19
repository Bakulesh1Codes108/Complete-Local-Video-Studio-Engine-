#!/usr/bin/env python3
"""
Lightweight Studio & RPA Pipeline Server for Antigravity Video Studio.
Serves:
  - '/' or '/studio' -> Pro Desktop NLE Studio UI (app/studio_pro.html)
    with DaVinci Resolve, CapCut, Adobe Premiere, and Final Cut Pro themes.
  - '/rpa' -> Visual Node RPA Automation Canvas (app/rpa_studio.html)
  - API Endpoints: /api/rpa/execute, /api/convert, /api/render, /api/voice-clone, /api/upscale
"""

import sys
import os
import json
import subprocess
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
STUDIO = os.path.join(SCRIPTS_DIR, "studio.py")
REEL_MIMIC = os.path.join(SCRIPTS_DIR, "reel_mimic.py")
VOICE_CLONE = os.path.join(SCRIPTS_DIR, "voice_clone.py")
UPSCALER = os.path.join(SCRIPTS_DIR, "upscaler.py")

class RpaRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path in ["/", "/studio", "/pro", "/edit"]:
            self.path = "/app/studio_pro.html"
        elif self.path == "/rpa":
            self.path = "/app/rpa_studio.html"
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        try:
            data = json.loads(body) if body.strip() else {}
        except Exception:
            data = {}

        if self.path == "/api/rpa/execute":
            try:
                prompt = data.get("prompt", "Autonomous Video")
                mimic = data.get("mimic", "alex_hormozi_viral_reel")
                engine = data.get("engine", "hybrid_auto")
                fmt = data.get("format", "16:9")

                print(f"🎬 [Studio RPA Job] Prompt: '{prompt}', Mimic: {mimic}, Format: {fmt}")

                # If vertical format requested, ensure project is switched
                if fmt in ["9:16", "vertical"]:
                    subprocess.run([sys.executable, STUDIO, "convert", "9:16"], cwd=BASE_DIR)

                # Run Reel Mimic / Quickstart generator
                subprocess.run([sys.executable, REEL_MIMIC, mimic, prompt], cwd=BASE_DIR)

                self._send_json({
                    "status": "success",
                    "message": "Pipeline executed successfully",
                    "previewCommand": "npm run preview",
                    "renderCommand": "npm run render"
                })
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=500)

        elif self.path == "/api/convert":
            try:
                target_fmt = data.get("format", "16:9")
                print(f"🔄 [Studio Format Convert] Switching to {target_fmt}...")
                subprocess.run([sys.executable, STUDIO, "convert", target_fmt], cwd=BASE_DIR)
                self._send_json({"status": "success", "format": target_fmt})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=500)

        elif self.path == "/api/render":
            try:
                print("⚡ [Studio Render] Dispatched Remotion render...")
                # Run render
                subprocess.Popen([sys.executable, STUDIO, "render"], cwd=BASE_DIR)
                self._send_json({"status": "success", "message": "Render job dispatched to Remotion"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=500)

        elif self.path == "/api/voice-clone":
            try:
                print("🎙️ [Studio Voice Clone] Triggered 5-second voice clone synthesis...")
                subprocess.Popen([sys.executable, STUDIO, "clone-voice"], cwd=BASE_DIR)
                self._send_json({"status": "success", "message": "5-Second voice clone started"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=500)

        elif self.path == "/api/upscale":
            try:
                target_file = data.get("file", "")
                print(f"🔍 [Studio Upscaler] Upscaling {target_file} to 4K...")
                subprocess.Popen([sys.executable, STUDIO, "upscale", target_file], cwd=BASE_DIR)
                self._send_json({"status": "success", "message": "Upscale job launched"})
            except Exception as e:
                self._send_json({"status": "error", "message": str(e)}, status=500)

        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, payload, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

def run_server(port=8080):
    server_address = ('127.0.0.1', port)
    try:
        httpd = HTTPServer(server_address, RpaRequestHandler)
    except OSError:
        # Fallback port if 8080 is in use
        port = 8888
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, RpaRequestHandler)

    pro_url = f"http://127.0.0.1:{port}/"
    rpa_url = f"http://127.0.0.1:{port}/rpa"
    print("=" * 70)
    print("🎬 ANTIGRAVITY UNIFIED VIDEO STUDIO PRO")
    print("=" * 70)
    print(f"✨ Pro Desktop NLE UI : {pro_url}")
    print(f"🤖 Visual RPA Canvas  : {rpa_url}")
    print("🎨 Themes: DaVinci Resolve | CapCut Neon | Premiere Pro | Final Cut")
    print("Press Ctrl+C to stop.")
    print("=" * 70)

    try:
        webbrowser.open(pro_url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Studio server.")
        httpd.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(p)
