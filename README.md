# Clone Hero Video Forge

**Clone Hero Video Forge** is a GUI tool that makes it stupid-easy to prepare background videos for **Clone Hero songs**.

It can:

- Download YouTube videos at up to **1080p**
- Output **WebM (VP8)** or **MP4 (H.264/AAC)** depending on your choice
- Embed audio into WebM if desired
- Trim or pad videos (and audio) for chart syncing
- Adjust any existing WebM without redownloading
- Show realtime progress for yt-dlp and ffmpeg
- Display a live-updating debug console
- Package into a standalone Windows EXE (no Python required)

This project is fully open source under the MIT License.

---

## ✨ Features

### ✅ Download From YouTube

- Download in **WebM (VP8)** or **MP4 (H.264)**
- Optional **embedded audio** (Vorbis for WebM)
- Automatic format selection
- Trim or pad the video during download

### ✅ Adjust Existing WebM

- Trim the start
- Add silence/black padding
- Keep or remove audio
- Overwrite in place or save as a new file

### ✅ Quality of Life

- **Preset: Clone Hero BG** button
- Live debug log window
- Progress bars for both downloading & encoding
- Open output folder when done

---

## 📦 Installation (End-Users)

Download the latest release EXE from:

> https://github.com/Robot011011/CHVideoForge/releases

Run the EXE — no Python, no setup, no dependencies needed.

---

## 🧑‍💻 Installation (Developers)

### 1. Clone the repo

```sh
git clone https://github.com/Robot011011/CHVideoForge.git
cd CHVideoForge
```

### 2. Create a virtual environment

```sh
python -m venv .venv
.\.venv\Scripts ctivate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Run the GUI

```sh
python ch_video_gui.py
```

---

## 🏗 Building the EXE (Windows)

Requires:

- Python 3.10–3.12
- PyInstaller (`pip install pyinstaller`)

Build with:

```sh
pyinstaller --onefile --noconsole --name CHVideoForge ch_video_gui.py
```

Your EXE will appear in:

```text
dist/CHVideoForge.exe
```

---

## 🎮 Using Clone Hero Video Forge

### 1. Downloading a YouTube Video

1. Paste a YouTube link.
2. Choose your **song folder**.
3. Set the **output name** (without extension, e.g. `video` or `gurenge_bg`).
4. Choose format:
   - WebM mode (default) — optionally embed audio.
   - MP4 mode — video+audio combined.
5. Set **Trim start** and/or **Pad start** (in seconds), if needed.
6. Click **Download**.

A ready-to-use `video.webm` or `video.mp4` will appear in your song folder.

> 🔎 Tip: The “Preset: Clone Hero BG” button will:
> - Turn off audio embedding
> - Reset trim/pad to `0.0`
> - Set the output name to `video.webm`

### 2. Adjusting an Existing WebM

1. In **Adjust Existing WebM**, pick an input `.webm` file.
2. Leave **Output WebM** blank to overwrite, or enter a new name.
3. Set **Trim start** and/or **Pad start**.
4. Check **Keep audio in output** if you want to keep audio.
5. Click **Adjust**.

The tool will re-encode to a Clone Hero–friendly VP8 WebM, trimming and/or padding both video and audio where appropriate.

### 3. Using Videos in Clone Hero

In your song’s folder, you typically have:

```text
song.ini
song.ogg
notes.mid  (or notes.chart)
video.webm  (or video.mp4)
```

In Clone Hero:

1. Enable **Song Videos** in the game settings.
2. Make sure the video file is in the same folder as `song.ini`.

Clone Hero will detect and use the video automatically.

---

## ⚠️ Disclaimer

This tool:

- Does **not** encourage copyright infringement.
- Does **not** bypass YouTube restrictions.
- Requires users to **respect copyright law**.
- Is meant only for use with videos you have the rights to download.

By using this project, you agree to be responsible for how you download and use content.

---

## 🙌 Contributing

Contributions are welcome!

- Open issues for bugs, feature requests, and ideas.
- Fork the repo, make a feature branch, and submit a pull request.

See **CONTRIBUTING.md** for details on coding style, branching, and PR guidelines.

---

## 🔒 Security

If you discover a security issue:

1. Please **do not** open a public GitHub issue first.
2. Email the repository owner or open a private security advisory on GitHub.
3. Allow a reasonable amount of time for investigation and a fix.

See **SECURITY.md** for more details.

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and redistribute this project, provided you keep the copyright and license notice in derivative works.

See `LICENSE` for the full text.