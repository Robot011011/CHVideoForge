# Clone Hero Video Forge

[![Latest Release](https://img.shields.io/github/v/release/Robot011011/CHVideoForge?label=latest%20release)](https://github.com/Robot011011/CHVideoForge/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/Robot011011/CHVideoForge/total)](https://github.com/Robot011011/CHVideoForge/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Built with Python](https://img.shields.io/badge/built%20with-Python%203.x-blue)

---

Clone Hero Video Forge is a small desktop utility that prepares **background videos for Clone Hero**.

It can:

- Download YouTube videos
- Convert them to **VP8 WebM**
- Optionally embed audio in the same file
- Trim and pad the start to sync with your chart
- Adjust existing `.webm` files without re-downloading

---

## ✨ Features

- 🎞 **YouTube → WebM**
  - Downloads up to 1080p using `yt-dlp`
  - Converts to VP8 WebM via `ffmpeg`
  - Optionally embeds audio (Vorbis) in the same `.webm`

- ✂️ **Trim & Pad**
  - Trim start of video/audio (skip intros)
  - Add black frames (and silence if audio is included) at the beginning
  - Keeps audio and video in sync

- 🔧 **Adjust Existing WebM**
  - Re-trim or re-pad background videos without re-downloading
  - Overwrite files or save as new output
  - Optionally keep audio in the adjusted file

- 📡 **Progress & Debug**
  - Progress bar for download + encoding
  - Live-updating debug log window for yt-dlp and ffmpeg output

- 🧹 **Quality-of-Life**
  - Automatic temp file cleanup
  - Auto-append `.webm` if the user forgets
  - File name conflict checks before encoding
  - “Open Folder” button after success
  - “Preset: Clone Hero BG” button for fast setup

---

## 📦 Downloads

You can download the latest Windows `.exe` here:

👉 **[Latest Release](https://github.com/your-username/your-repo/releases/latest)**

> The `.exe` is distributed via GitHub Releases.  
> You do **not** need Python to run the compiled version.

---

## 🧩 Requirements

To run the compiled `.exe`:

- Windows 10 or 11
- `ffmpeg` installed and available in `PATH`
- `yt-dlp` installed and available in `PATH`

To run from source:

- Python 3.10+
- Install Python dependencies:
  ```bash
  pip install -r requirements.txt
