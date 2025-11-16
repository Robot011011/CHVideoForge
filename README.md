# Clone Hero Video Forge

[![Latest Release](https://img.shields.io/github/v/release/Robot011011/CHVideoForge?label=latest%20release)](https://github.com/Robot011011/CHVideoForge/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Robot011011/CHVideoForge/total)](https://github.com/Robot011011/CHVideoForge/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Built with Python](https://img.shields.io/badge/built%20with-Python%203.x-blue)

---

Clone Hero Video Forge is a lightweight desktop tool for creating, adjusting, and syncing **background videos for Clone Hero**.  
It downloads videos from YouTube, converts them to Clone-Hero-friendly VP8 WebM, optionally embeds audio, and provides simple trim/pad tools for perfect timing.

This project is completely open-source and community-driven.

---

# 🎸 Features

### 🎥 **YouTube → VP8 WebM Conversion**
- High-quality WebM output (up to 1080p)
- Optional audio embedding (single file)
- Full control over filename and destination folder

### ✂️ **Trim & Pad Controls**
- Trim video/audio from the start  
- Add black frames + silence for precise timing  
- Audio and video remain perfectly in sync

### 🔧 **Adjust Existing WebM**
- Load an existing `.webm` and re-trim/re-pad it  
- Optional overwrite or new output name  
- Works with audio or silent videos

### 📡 **Smart UI & Feedback**
- Progress bar for download & encoding  
- Open-Folder button after completion  
- Live-updating Debug Log  
- Filename conflict detection  
- Auto-cleanup of temp files  
- Auto-append `.webm` when missing

### ⚙️ **Preset Button**
- "Preset: Clone Hero BG" instantly configures typical CH video settings

---

# 📦 Download

Grab the latest Windows release here:

👉 **https://github.com/Robot011011/CHVideoForge/releases/latest**

> Does **not** require Python.  
> Just run the executable.

---

# 📘 Quick Usage Guide

### 1. **Downloading a Video**
1. Paste a YouTube URL  
2. Select your Clone Hero song folder  
3. Choose an output name (Ex: `video.webm`)  
4. Optional:  
   - Trim start  
   - Pad start  
   - Embed audio  
5. Press **Download**  
6. Click **Open Folder** when done

### 2. **Adjusting an Existing `.webm`**
1. Choose a `.webm` file  
2. Choose output name (or leave blank to overwrite)  
3. Choose trim/pad values  
4. (Optional) Keep embedded audio  
5. Press **Adjust**  

### 3. **Using the Video in Clone Hero**
Place your final file inside the song folder:

```
song.ini
song.ogg
*.chart or *.mid
video.webm
```

---

# 🧩 Requirements (Source Version)

```
Python 3.10+
ffmpeg in PATH
yt-dlp in PATH
```

Install dependencies:

```
pip install -r requirements.txt
```

Run:

```
python ch_video_gui.py
```

---

# 🛠 Building the EXE

```
pyinstaller ^
  --noconsole ^
  --onefile ^
  --name "Clone Hero Video Forge" ^
  ch_video_gui.py
```

---

# ⚖️ License

MIT License – see LICENSE file.

---

# Legal Notes
You agree to:
- Follow YouTube’s Terms of Service  
- Only download content you are legally allowed to  
- Accept full responsibility for use of the tool  

This tool is **not affiliated** with Clone Hero or YouTube.

---

# 🤝 Contributing

See **CONTRIBUTING.md**.

---

# 🔐 Security

See **SECURITY.md**.

---

# 📚 Full User Manual

See **USING_CLONE_HERO_VIDEO_FORGE.md**.

---

# 🚀 Enjoy the Forge!

If this tool helped you, star ⭐ the repo!




