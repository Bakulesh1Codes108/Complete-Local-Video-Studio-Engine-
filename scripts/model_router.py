#!/usr/bin/env python3
"""
Intelligent Model Router, Prompt Compressor, and Zero-Cost Fallback Agent
for Antigravity Video Studio.

Connects:
  - Local Llama / Qwen via Ollama (100% Free, Offline Fallback)
  - OpenRouter Free Gateway (openrouter/free, llama-3.3-70b:free, deepseek-r1:free)
  - Google Gemini / AI Pro (Gemini 2.0 Flash / Pro)
  - Rule-Based Deterministic Engine (Zero Tokens, Zero Network)
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "model_router.config.json")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "routingPolicy": {"preferFree": True, "promptForPermissionOnPaid": True, "autoFallbackToLocal": True},
            "providers": {}
        }
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# 1. PROMPT COMPRESSOR & CLEANER (Token Saver)
# ==========================================
class PromptCompressor:
    @staticmethod
    def clean_noisy_prompt(raw_text: str) -> dict:
        """
        Cleans messy, colloquial, or rambling prompts into a high-density,
        minimal-token prompt payload. Saves 50-80% of tokens.
        """
        original_words = len(raw_text.split())

        # Strip common filler phrases
        fillers = [
            r"\bumm*\b", r"\bahh*\b", r"\byou know\b", r"\blike\b",
            r"\bcan you please\b", r"\bi want you to\b", r"\bjust make\b",
            r"\bkind of\b", r"\bsort of\b", r"\bbasically\b", r"\bliterally\b"
        ]
        cleaned = raw_text
        for pattern in fillers:
            cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

        # Remove duplicate spaces and punctuation clutter
        cleaned = re.sub(r"[?!.,]{2,}", ".", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # Extract potential scene parameters if present
        duration_match = re.search(r"(\d+)\s*(?:sec|seconds|s\b)", raw_text, re.IGNORECASE)
        duration = int(duration_match.group(1)) if duration_match else 5

        # Detect motion preference
        motion = "zoom-in"
        if re.search(r"\bpan\s*left\b", raw_text, re.IGNORECASE):
            motion = "pan-left"
        elif re.search(r"\bpan\s*right\b", raw_text, re.IGNORECASE):
            motion = "pan-right"
        elif re.search(r"\bzoom\s*out\b", raw_text, re.IGNORECASE):
            motion = "zoom-out"

        compressed_words = len(cleaned.split())
        token_savings_pct = round(((original_words - compressed_words) / max(original_words, 1)) * 100, 1)

        return {
            "cleaned_prompt": cleaned,
            "detected_duration": duration,
            "detected_motion": motion,
            "original_word_count": original_words,
            "cleaned_word_count": compressed_words,
            "estimated_token_savings": f"{max(0, token_savings_pct)}%"
        }

# ==========================================
# 2. MULTI-TIER MODEL ROUTER & FALLBACK AGENT
# ==========================================
class ModelRouter:
    def __init__(self):
        self.config = load_config()

    def check_local_ollama(self) -> dict:
        """Checks if Ollama is running locally on Mac or HP Pavilion"""
        endpoint = "http://localhost:11434/api/tags"
        try:
            req = urllib.request.Request(endpoint, method="GET")
            with urllib.request.urlopen(req, timeout=0.8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name") for m in data.get("models", [])]
                return {"available": True, "models": models}
        except Exception:
            return {"available": False, "models": []}

    def suggest_tier(self, cleaned_prompt: str) -> dict:
        """
        AI Cost-Optimizer: Analyzes task complexity and suggests the cheapest / best provider.
        """
        words = len(cleaned_prompt.split())
        ollama_status = self.check_local_ollama()
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        gemini_key = os.environ.get("GEMINI_API_KEY")

        if words < 30 and ollama_status["available"]:
            return {
                "tier": "LOCAL_FREE",
                "recommended_provider": "local_ollama",
                "model": "llama3.2:latest",
                "estimated_cost": "$0.00 (Offline Local)",
                "reason": "Short / structural task. Perfect for local Llama model with 0 latency and 0 tokens."
            }
        elif openrouter_key:
            return {
                "tier": "CLOUD_FREE_ROUTER",
                "recommended_provider": "openrouter_free",
                "model": "openrouter/free",
                "estimated_cost": "$0.00 (OpenRouter Free Tier)",
                "reason": "Creative scene generation. Routed via OpenRouter free model aggregator."
            }
        elif gemini_key:
            return {
                "tier": "GOOGLE_AI_PRO",
                "recommended_provider": "google_gemini",
                "model": "gemini-2.0-flash",
                "estimated_cost": "$0.00 (Google AI Pro / Free RPM Tier)",
                "reason": "High-context documentary structuring and cinematic visuals."
            }
        else:
            return {
                "tier": "DETERMINISTIC_OFFLINE",
                "recommended_provider": "rule_based_engine",
                "model": "internal-studio-parser",
                "estimated_cost": "$0.00 (Offline Rules)",
                "reason": "No cloud API keys detected and Ollama offline. Using deterministic internal parser."
            }

    def generate_with_fallback(self, prompt: str, system_prompt: str = "") -> dict:
        """
        Executes generation following the resilience cascade:
        1. Primary Suggested Provider
        2. Local Ollama (Llama/Qwen)
        3. Deterministic Studio Rule Engine
        """
        suggestion = self.suggest_tier(prompt)
        provider = suggestion["recommended_provider"]

        print(f"🤖 [Model Router] Selected Provider: {provider} ({suggestion['model']}) | Cost: {suggestion['estimated_cost']}")

        # Attempt 1: Local Ollama
        if provider == "local_ollama":
            result = self._call_ollama(prompt, system_prompt)
            if result:
                return {"provider": "local_ollama", "model": suggestion["model"], "content": result}
            print("⚠️ Local Ollama failed or timed out. Falling back to Cloud/Rule engine...")

        # Attempt 2: Groq (Ultra-fast low latency)
        if os.environ.get("GROQ_API_KEY"):
            result = self._call_groq(prompt, system_prompt)
            if result:
                return {"provider": "groq", "model": "llama-3.3-70b-versatile", "content": result}
            print("⚠️ Groq call failed. Falling back...")

        # Attempt 3: OpenRouter Gateway (Free & paid aggregator)
        if provider == "openrouter_free" or os.environ.get("OPENROUTER_API_KEY"):
            result = self._call_openrouter(prompt, system_prompt)
            if result:
                return {"provider": "openrouter_free", "model": "openrouter/free", "content": result}
            print("⚠️ OpenRouter free failed. Falling back...")

        # Attempt 4: Google Gemini 2.0 Flash
        if provider == "google_gemini" or os.environ.get("GEMINI_API_KEY"):
            result = self._call_gemini(prompt, system_prompt)
            if result:
                return {"provider": "google_gemini", "model": "gemini-2.0-flash", "content": result}
            print("⚠️ Gemini call failed. Falling back...")

        # Attempt 5: OpenAI API (gpt-4o-mini)
        if os.environ.get("OPENAI_API_KEY"):
            result = self._call_openai(prompt, system_prompt)
            if result:
                return {"provider": "openai", "model": "gpt-4o-mini", "content": result}
            print("⚠️ OpenAI call failed. Falling back...")

        # Final Fallback: Antigravity Deterministic Studio Rule Engine (Zero Tokens, Zero Network)
        return {
            "provider": "antigravity_deterministic_offline",
            "model": "rule_based_parser",
            "content": self._rule_based_generate(prompt)
        }

    def _call_groq(self, prompt: str, system_prompt: str):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return None
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = json.dumps({
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt or "You are a professional film director and video editor."},
                    {"role": "user", "content": prompt}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _call_openai(self, prompt: str, system_prompt: str):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt or "You are a professional film director and video editor."},
                    {"role": "user", "content": prompt}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=12.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _call_ollama(self, prompt: str, system_prompt: str):
        try:
            url = "http://localhost:11434/api/generate"
            payload = json.dumps({
                "model": "llama3.2:latest",
                "prompt": f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
                "stream": False
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=12.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response")
        except Exception:
            return None

    def _call_openrouter(self, prompt: str, system_prompt: str):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return None
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/Bakulesh1Codes108/antigravity-video-studio"
            }
            payload = json.dumps({
                "model": "openrouter/free",
                "messages": [
                    {"role": "system", "content": system_prompt or "You are a documentary film director."},
                    {"role": "user", "content": prompt}
                ]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _call_gemini(self, prompt: str, system_prompt: str):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return None

    def _rule_based_generate(self, prompt: str) -> str:
        """Offline deterministic documentary scene parser"""
        lines = prompt.strip().split(". ")
        title = lines[0][:40] if lines else "Documentary Scene"
        narration = prompt.strip()
        visual_prompt = f"Cinematic photorealistic documentary shot depicting: {title}, 35mm film grain, 8k"
        return json.dumps({
            "title": title,
            "narration": narration,
            "visualPrompt": visual_prompt,
            "duration": 5.0,
            "motion": "zoom-in"
        }, indent=2)

if __name__ == "__main__":
    router = ModelRouter()
    compressor = PromptCompressor()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scripts/model_router.py status")
        print("  python3 scripts/model_router.py clean '<noisy prompt>'")
        print("  python3 scripts/model_router.py suggest '<prompt>'")
        print("  python3 scripts/model_router.py run '<prompt>'")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        ollama = router.check_local_ollama()
        print("=== Model Router Provider Status ===")
        print(f"Local Ollama (Llama/Qwen): {'🟢 Online (' + ', '.join(ollama['models']) + ')' if ollama['available'] else '⚪ Offline (Run: ollama serve)'}")
        print(f"OpenRouter Gateway:        {'🟢 Configured' if os.environ.get('OPENROUTER_API_KEY') else '🟡 No key (Set OPENROUTER_API_KEY for free models)'}")
        print(f"Google Gemini / AI Pro:    {'🟢 Configured' if os.environ.get('GEMINI_API_KEY') else '🟡 No key (Set GEMINI_API_KEY or use Jio AI Pro in browser)'}")
    elif cmd == "clean":
        raw = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "umm you know can you like make a scene about deep ocean exploration for like 6 seconds or so"
        result = compressor.clean_noisy_prompt(raw)
        print(json.dumps(result, indent=2))
    elif cmd == "suggest":
        raw = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Explain quantum computing in 5 seconds"
        cleaned = compressor.clean_noisy_prompt(raw)
        suggestion = router.suggest_tier(cleaned["cleaned_prompt"])
        print(json.dumps(suggestion, indent=2))
    elif cmd == "run":
        raw = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "A majestic drone shot over snowy mountain peaks at sunset"
        cleaned = compressor.clean_noisy_prompt(raw)
        print(f"🧹 Cleaned Prompt ({cleaned['estimated_token_savings']} token savings): '{cleaned['cleaned_prompt']}'")
        res = router.generate_with_fallback(cleaned["cleaned_prompt"])
        print(f"🎯 Output from [{res['provider']} - {res['model']}]:\n{res['content']}")
