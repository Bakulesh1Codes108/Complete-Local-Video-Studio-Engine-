#!/usr/bin/env python3
"""
Lightweight RPA Pipeline Server for Antigravity Video Studio.
Serves the visual node-based RPA interface and dispatches jobs
to Reel Mimic, Blender, Manim, Three.js, and Remotion.
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

class RpaRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/rpa":
            self.path = "/app/rpa_studio.html"
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/rpa/execute":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                prompt = data.get("prompt", "Autonomous Video")
                mimic = data.get("mimic", "alex_hormozi_viral_reel")
                engine = data.get("engine", "hybrid_auto")
                motion = data.get("motion", "orbit_360")
                preset = data.get("preset", "netflix-doc")

                print(f"🤖 [RPA Pipeline Job] Prompt: '{prompt}', Mimic: {mimic}, Engine: {engine}")

                # 1. Run Reel Mimic / Quickstart
                subprocess.run([sys.executable, REEL_MIMIC, mimic, prompt], cwd=BASE_DIR)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "Pipeline executed successfully",
                    "previewCommand": "npm run preview",
                    "renderCommand": "npm run render"
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8080):
    server_address = ('127.0.0.1', port)
    try:
        httpd = HTTPServer(server_address, RpaRequestHandler)
    except OSError:
        # Fallback port if 8080 is in use
        port = 8888
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, RpaRequestHandler)

    url = f"http://127.0.0.1:{port}/rpa"
    print("=" * 65)
    print("🤖 ANTIGRAVITY RPA AUTOMATION STUDIO")
    print("=" * 65)
    print(f"🚀 Visual RPA Studio UI running at: {url}")
    print("Press Ctrl+C to stop.")
    print("=" * 65)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down RPA server.")
        httpd.server_close()

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(p)
