# Clone Hero Video Forge – How to Use

Clone Hero Video Forge is a tool for downloading, converting, trimming, padding, and adjusting background videos for Clone Hero. All output videos are saved as `.webm` and are ready to drop directly into your Clone Hero song folders.

---

## 🎞 Downloading a New Video

1. **YouTube URL**  
   Paste the full link to the video you want.

2. **Song Folder**  
   Select the folder where your Clone Hero song lives  
   (the same folder containing `song.ini`, chart files, and audio files).

3. **Output Name (.webm)**  
   Recommended name:  
   video.webm
   Clone Hero auto-detects this file name.

4. **Trim Start (seconds)** (optional)  
Removes time from the beginning of both the video and audio.  
Use this if the music starts later in the video.

5. **Pad Start (seconds)** (optional)  
Adds black frames (and silence if audio is included) before the video begins.  
Use this if you need the video to start later without cutting anything.

6. **Embed Audio in WebM**  
- **On**: Downloads + embeds audio inside the `.webm`  
- **Off**: Creates a silent background video

7. **Click Download**  
- The progress bar shows download and encoding steps  
- When finished, the **Open Folder** button becomes available

8. Place the final `.webm` file inside your Clone Hero song folder.

---

## 🔧 Adjusting an Existing `.webm`

Use this if you already have a `.webm` background video and want to fix timing or sync issues.

1. **Input WebM**  
Select the existing `.webm` file you want to adjust.

2. **Output WebM**  
- Leave blank to overwrite the original file  
- OR enter a new name to save an adjusted copy

3. **Trim Start (seconds)**  
Cuts time off the beginning.

4. **Pad Start (seconds)**  
Adds black frames (and silence if audio is included).

5. **Keep Audio in Output**  
- On: Retains and adjusts audio  
- Off: Output file is silent

6. **Click Adjust**  
The processed `.webm` is saved into the same folder.

---

## ⚡ Preset: Clone Hero BG

Pressing **Preset: Clone Hero BG** automatically:

- Sets the output name to `video.webm`
- Disables audio
- Resets trim to 0
- Resets pad to 0

Use this for fast, simple background video conversions.

---

## 🐞 Debug Log

Click **Debug Log…** to open a live-updating log window.  
It shows:

- yt-dlp download output  
- ffmpeg encoding messages  
- internal worker diagnostics  

Use this for troubleshooting if something fails.

---

## 🎮 Using the Video in Clone Hero

Place the final `.webm` file in the same folder as:

- `song.ini`
- Your chart (`.chart` or `.mid`)
- Your audio file (`song.ogg`, `song.mp3`, etc.)

Then enable **Song Videos** in Clone Hero’s settings.

The background video will automatically play during gameplay.

