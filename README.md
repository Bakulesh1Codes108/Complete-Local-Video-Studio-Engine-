# 🎬 Antigravity Local Video Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-555555.svg)]()
[![Cost](https://img.shields.io/badge/Cost-100%25%20Free%20%26%20Local-success.svg)]()
[![Engines](https://img.shields.io/badge/Engines-Remotion%20%7C%20HyperFrames%20%2B%20GSAP%203-orange.svg)]()
[![Memory](https://img.shields.io/badge/Memory-Graphify%20Knowledge%20Graph-brightgreen.svg)]()
[![Models](https://img.shields.io/badge/LLMs-Gemini%20Flash%20%7C%20Local%20Llama%203.2%20%7C%20OpenRouter-blueviolet.svg)]()

> **100% Free, Code-Driven AI Documentary & Video Production Studio.**  
> Turn prompts, voiceovers, and research notes into deterministic, broadcast-quality **16:9 Documentaries** and **9:16 Shorts/Reels** using **Remotion, HyperFrames, Graphify Context Memory, and Edge-TTS**.  
> Features an **Intelligent Model Router** with **Local Llama (Ollama) offline fallback**, **OpenRouter free gateway**, and **Prompt Compression** to save tokens from messy input.  
> **Zero Cloud Subscriptions • Zero API Costs • Zero Watermarks • Hardware Accelerated.**

---

## 📘 Comprehensive Free Guide Included

This repository comes with the official, full-length guide:  
👉 **[Download: Antigravity-Video-Free-Guide.pdf](./Antigravity-Video-Free-Guide.pdf)** 👈

---

## 🌟 The Unified 4-Pillar Architecture

```mermaid
flowchart TD
    subgraph InputLayer ["1. Input & Token Compression"]
        Raw["Messy / Colloquial Prompt<br>('umm you know can you like make a scene...')"]
        Comp["Prompt Compressor<br>(Strips fillers, extracts duration & motion, saves 30-70% tokens)"]
        Raw --> Comp
    end

    subgraph RoutingLayer ["2. Intelligent Model Router & Cost Optimizer"]
        Router["Model Router Agent"]
        Comp --> Router
        Router -->|Local & Offline| Ollama["Local Ollama<br>(Llama 3.2 / Qwen 2.5 on HP Laptop GPU)"]
        Router -->|Free Cloud Gateway| OR["OpenRouter Free Tier<br>(openrouter/free, llama-3.3-70b:free)"]
        Router -->|High Context| Gem["Google Gemini / Jio AI Pro<br>(Gemini 2.0 Flash)"]
        Router -->|Zero Network Fallback| Rule["Studio Deterministic Parser<br>($0.00, 100% Offline)"]
    end

    subgraph MemoryLayer ["3. Graphify Context Memory"]
        G1["graphify-out/graph.json<br>(Persistent Film Memory)"]
        G2["graphify-out/GRAPH_REPORT.md<br>(Live Continuity Tracker)"]
        Ollama --> G1
        OR --> G1
        Gem --> G1
        Rule --> G1
        G1 --> G2
    end

    subgraph VideoEngines ["4. Dual Deterministic Video Engines"]
        R1["Remotion Studio Core<br>(React + Vite + Ken Burns + Kinetic Captions)"]
        H1["HyperFrames + GSAP 3<br>(Fluid Motion, SVG Infographics & Explainer Stems)"]
        G1 -->|Sub-50 token timeline.json| R1
        G1 -->|Sub-50 token timeline.json| H1
    end
```

---

## 🧠 Smart Model Router & Token Compressor

The studio includes a built-in cost-optimizer that protects you against token burn and API downtime:

### 1. Token-Saving Prompt Compressor
If you input unstructured, rambling prompts:
```bash
python3 scripts/studio.py clean "umm you know can you please basically make a scene about black holes for like 7 seconds pan right"
```
* Strips conversational filler (*"umm", "you know", "can you please like", "basically"*).
* Saves **20% to 70% of tokens** before making any LLM call.
* Automatically extracts duration (`7 seconds`) and camera motion (`pan-right`).

### 2. Zero-Cost Fallback Cascade
When your tokens run out or you work offline:
* **Local Llama 3.2 via Ollama (`http://localhost:11434`):** Runs 100% free on your local GPU (ideal on the HP Pavilion Gaming NVIDIA card).
* **OpenRouter Free Tier:** Supports `openrouter/free`, `meta-llama/llama-3.3-70b-instruct:free`, and `deepseek/deepseek-r1:free` with zero cost.
* **Google Gemini (Jio AI Pro):** Uses Gemini 2.0 Flash for massive context and complex documentary direction.
* **Studio Rule Parser:** Internal deterministic fallback that ensures the studio **never crashes or hangs** even with no internet connection.

---

## 🚀 Quick Start (Autonomous Studio CLI)

### 1. Check Model Providers & Router Status
```bash
python3 scripts/studio.py models
```

### 2. Add a Scene with Smart AI Routing & Prompt Cleaning
One command cleans your prompt, selects the optimal zero-cost model, and registers the scene into Graphify memory:
```bash
python3 scripts/studio.py smart-scene scene_01 "umm can you like make a scene about ancient ruins hidden under dense jungle for 6 seconds zoom out"
```

### 3. Check Film Reel Continuity Report
```bash
python3 scripts/studio.py status
# Or inspect graphify-out/GRAPH_REPORT.md
```

### 4. Generate Free Neural Voiceovers
```bash
python3 scripts/studio.py audio
```

### 5. Preview Live in Remotion
```bash
npm install
npm run preview
```

### 6. Render Broadcast MP4
```bash
npm run render
```

---

## 💻 Dual-Machine Production Guide

| Feature | On Mac (Intel i5, 8GB) | On HP Pavilion Gaming (NVIDIA GPU) |
| :--- | :--- | :--- |
| **Brain / Scripting** | Gemini Advanced (Jio AI Pro) | Gemini Advanced (Jio AI Pro) |
| **Local LLM Fallback** | Ollama (CPU mode) | **Ollama Llama 3.2 (CUDA GPU accelerated)** |
| **Memory Graph** | `scripts/studio.py` | `scripts/studio.py` |
| **Voiceover Engine** | Edge-TTS (Cloud Neural) | Edge-TTS (Cloud Neural) |
| **Image Keyframes** | Cloud (Imagen 3 / Pollinations) | **Fooocus Local (CUDA SDXL accelerated)** |
| **Remotion Rendering** | CPU Render | **NVIDIA Hardware Accelerated** |

---

## 📂 Repository Structure

```
antigravity-video-studio/
├── Antigravity-Video-Free-Guide.pdf   # Complete official user guide (PDF)
├── model_router.config.json          # Smart router endpoints & cost rules
├── graphify-out/
│   ├── graph.json                    # Persistent film memory graph
│   └── GRAPH_REPORT.md               # Live film reel & continuity report
├── graphify.config.json              # Graphify memory schema
├── timeline.json                     # Code-ready Remotion timeline recipe
├── remotion.config.ts                # Remotion video configuration
├── packages/
│   └── extension/                    # In-Editor Sidebar Webview (CaldiaWorks Core)
├── src/
│   ├── Root.tsx                      # Remotion composition registry
│   ├── index.ts                      # Remotion root entry
│   ├── types/timeline.ts             # TypeScript definitions
│   └── compositions/
│       ├── DocumentaryComposition.tsx# Master timeline sequencer
│       ├── KenBurns.tsx              # Cinematic sub-pixel camera motion
│       ├── KineticSubtitle.tsx       # Physics-based spring subtitles
│       └── AudioMixer.tsx            # Auto voice ducking audio mixer
├── scripts/
│   ├── studio.py                     # Unified master CLI
│   ├── model_router.py               # Prompt compressor & multi-tier router
│   ├── graph_memory.py               # Graphify memory manager
│   ├── make_voiceovers.py            # Free Edge-TTS audio synthesizer
│   ├── local_ai_director.py          # Bridge to local Ollama/Qwen/Llama models
│   ├── extract_vocals.py             # Demucs stem separator
│   └── transcribe_sync.py            # Whisper.cpp millisecond timestamp extractor
├── app/
│   ├── main.py                       # Cross-platform desktop backend
│   └── ui.html                       # Dark studio GUI interface
├── templates/
│   ├── lyric-video/                  # Base 9:16 GSAP template
│   └── nikhil-kamath-wtf-infographics/# Podcast infographic explainer template
├── examples/                         # Production showcase MP4 files
├── setup.sh                          # macOS setup script
├── setup.bat                         # Windows batch installer
└── README.md                         # Unified studio documentation
```

---

## 📄 License
MIT License. Open-source, royalty-free for personal, educational, and commercial video creation.
