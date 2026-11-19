# 🎙️ Voice Clone Samples

Drop your 5-to-10 second clean voice recording here to clone your voice for your video studio narrations.

### Instructions:
1. Record a **5-to-10 second** clean audio clip of yourself speaking clearly without background noise or music.
   - Example phrase: *"Welcome to this documentary. Today we are exploring the frontiers of technology and science."*
2. Save it as **`my_voice.wav`** (or `my_voice.mp3`) in this directory (`assets/voice_samples/my_voice.wav`).
3. Run the studio voiceover with the `--clone` flag:
   ```bash
   python scripts/studio.py audio --clone
   ```
   Or directly clone a specific sample:
   ```bash
   python scripts/studio.py clone-voice assets/voice_samples/my_voice.wav
   ```

### Hardware Support:
* **HP Pavilion Gaming PC (NVIDIA CUDA):** High-speed GPU accelerated voice synthesis via F5-TTS / MOSS-TTS.
* **Mac (Intel / Apple Silicon):** Supported via CPU/MPS or Edge-TTS cloud neural fallback.
