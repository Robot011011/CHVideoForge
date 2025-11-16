# 🎸 Clone Hero Video Forge  
*A standalone tool for downloading, syncing, and preparing background videos for Clone Hero.*

Clone Hero Video Forge makes it easy to turn any YouTube video into a properly formatted `.webm` background for Clone Hero, with optional audio, trimming, padding, and fine-tuned sync control.

---

# 🚀 Features

### ✅ Download YouTube Videos (Up to 1080p)
- Converts automatically to **VP8 WebM**, fully compatible with Clone Hero.
- Optional: include audio embedded into the same `.webm`.

### ✂️ Trimming & Padding
- **Trim Start** → remove unwanted intro from the video/audio.
- **Pad Start** → add black frames (and silence if audio is enabled) before the video starts.
- Perfect for chart syncing.

### 🔧 Adjust Existing WebM Files
- Re-trim or re-pad background videos **without re-downloading**.
- Supports overwrite or saving as a new file.

### 📡 Live Progress & Debugging
- Smooth progress bar for download + encoding.
- Optional live-updating debug console.

### 📁 Workflow Helpers
- “Open Folder” button after a successful conversion.
- Automatic cleanup of temp files.
- Automatic fixing of missing file extensions.
- “Clone Hero BG Preset” button for instant default setup.

---

# 🧩 Requirements

Clone Hero Video Forge requires:

- **Windows 10 or 11**
- **ffmpeg** installed and available in PATH  
  (`ffmpeg -version` should work in a terminal)
- **yt-dlp** installed and available in PATH  
  (`yt-dlp --version` should work)

---

# 📥 Installing

### If you're using the EXE:
No installation needed.

1. Place `Clone Hero Video Forge.exe` anywhere you like.
2. Make sure `ffmpeg` and `yt-dlp` are installed.
3. Double-click the EXE to launch the app.

### If you're running from source (Python):
```bash
pip install -r requirements.txt
python ch_video_gui_v1_public.py
```

## ⚠️ Legal Notice / Disclaimers

### YouTube Terms of Service
Clone Hero Video Forge does **not** bypass YouTube's protections.  
Users are responsible for complying with all applicable platform Terms of Service.

By using this tool, **you acknowledge that:**
- You must only download videos you have the right to use.
- You are responsible for following YouTube’s Terms of Service and local copyright laws.
- You understand that this project merely automates `yt-dlp` and `ffmpeg`, both of which have their own licenses and usage requirements.

### Copyright Responsibility
This tool is provided for:
- Personal use  
- Educational use  
- Clone Hero chart authors who have rights/permission to use the media  

**You are solely responsible for ensuring you have permission to download, modify, and use any video or audio processed by this tool.**

The maintainers of this project:
- Do **not** encourage piracy  
- Do **not** take responsibility for how the tool is used  
- Will comply with valid DMCA or takedown requests

### Not Affiliated With Clone Hero
Clone Hero Video Forge is an **independent third-party tool** and is **not affiliated with**, endorsed by, or associated with:
- Clone Hero developers or team members  
- Guitar Hero, Rock Band, or any related trademarks  
- YouTube, Google, or Alphabet Inc.  

All trademarks remain the property of their respective owners.

### Software Warranty Disclaimer
This software is provided **“as-is,” without warranty of any kind**, express or implied.  
This includes, but is not limited to:
- No guarantee of accuracy  
- No guarantee of compatibility  
- No guarantee that downloaded media will work with every chart or Clone Hero version  

Use at your own risk.

### Limitation of Liability
Under no circumstances shall the developers or contributors be liable for:
- Copyright violations committed by users  
- YouTube account issues, rate limiting, blocks, or ToS violations  
- Lost data, corrupted files, or any damages caused by using this tool  

By using Clone Hero Video Forge, you agree that **you assume full responsibility for all actions** performed with the software.

### Security Notice
This tool relies on:
- `yt-dlp` (external utility)  
- `ffmpeg` (external utility)

These applications are maintained by third parties.  
Users are responsible for verifying the authenticity and security of these dependencies.

---

By continuing to use Clone Hero Video Forge, you agree to all of the above terms.
