"""
Clone Hero Video Forge - PySide6 GUI
------------------------------------
- Download YouTube video as Clone Hero–ready WebM (VP8)
- Or as MP4 (always with audio)
- Optional embedded audio in WebM (Vorbis)
- Trim & pad (black) support (video and audio)
- Adjust existing WebM files
- Progress bars & non-blocking UI via QThread
- "Preset: Clone Hero BG" button
- "Open Folder" button after success
- Debug Log popup to inspect yt-dlp / ffmpeg output (live updating)
"""

APP_NAME = "Clone Hero Video Forge"
APP_VERSION = "1.1.0"  # bumped for mp4 feature

import sys
import subprocess
import tempfile
import time
from pathlib import Path

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
    Qt,
    QUrl,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QCheckBox,
    QPushButton,
    QProgressBar,
    QFileDialog,
    QGroupBox,
    QMessageBox,
    QDialog,
    QTextEdit,
    QComboBox,
)

# Optional: path to a cookies.txt file for YouTube
# If set, yt-dlp will always use these cookies.
# Leave as None if you don't want to use cookies.
COOKIES_FILE = None  # e.g. r"c:\%USERPROFILE%\Downloads\youtube_cookies.txt"

# =========================
#  LOW-LEVEL HELPERS
# =========================

def get_duration_seconds(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=True
        )
        return float(result.stdout.strip())
    except:
        return 0.0


def run_ffmpeg_with_progress(
    cmd,
    total_duration: float,
    progress_cb=None,
    status_cb=None,
    debug_cb=None,
):
    """
    Run ffmpeg and stream progress to the UI.

    On error, raises RuntimeError with both the exit code and the last
    non-progress line of ffmpeg output so the GUI can show useful info.
    """
    # Inject -progress etc near the end, just before -y / output
    insert_pos = max(0, len(cmd) - 2)
    cmd = cmd[:insert_pos] + [
        "-progress", "pipe:1",
        "-nostats",
        "-hide_banner",
        "-loglevel", "error",
    ] + cmd[insert_pos:]

    if status_cb:
        status_cb("Encoding...")

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )

    last_percent = -1.0
    last_error_line = ""

    for line in proc.stdout:
        raw = line.rstrip("\n")
        s = raw.strip()

        if debug_cb and raw:
            debug_cb(f"[ffmpeg] {raw}")

        if s.startswith("out_time_ms="):
            # Progress info
            try:
                ms = int(s.split("=", 1)[1])
                sec = ms / 1_000_000.0
                if total_duration > 0:
                    percent = min(100.0, (sec / total_duration) * 100)
                else:
                    percent = 0.0
                if int(percent) != int(last_percent):
                    last_percent = percent
                    if progress_cb:
                        progress_cb(percent)
            except:
                pass
        elif s.startswith("progress="):
            # Internal ffmpeg marker, skip for status
            continue
        else:
            # Any other line (typically errors) - keep for error reporting
            if s:
                last_error_line = s

    proc.wait()

    # Ensure bar hits 100% for encode portion if we got this far
    if progress_cb:
        progress_cb(100.0)

    if proc.returncode != 0:
        msg = f"ffmpeg failed (code {proc.returncode})"
        if last_error_line:
            msg += f": {last_error_line}"
        raise RuntimeError(msg)


def download_video(
    url: str,
    out_path: Path,
    include_audio: bool = False,
    progress_cb=None,
    status_cb=None,
    debug_cb=None,
):
    """
    Download from YouTube using yt-dlp.

    - include_audio = False → video-only
    - include_audio = True  → video+audio
    Container/codec is whatever yt-dlp chooses; we re-encode as needed later.
    """
    if include_audio:
        fmt = "bv*[height<=1080]+ba/b[height<=1080]"
    else:
        fmt = "bv*[height<=1080]/bv*"

    cmd = [
        "yt-dlp",
        "--newline",
        "--no-warnings",
        "--extractor-args", "youtube:player_client=default",
        "-f", fmt,
        "-o", str(out_path),
    ]

    if COOKIES_FILE is not None:
        cmd += ["--cookies", COOKIES_FILE]

    cmd.append(url)

    if status_cb:
        status_cb("Downloading...")

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1
    )

    last_percent = -1.0

    for line in proc.stdout:
        raw = line.rstrip("\n")
        s = raw.strip()

        if debug_cb and raw:
            debug_cb(f"[yt-dlp] {raw}")

        if s.startswith("[download]"):
            parts = s.split()
            for token in parts:
                if token.endswith("%"):
                    try:
                        percent = float(token[:-1])
                        if int(percent) != int(last_percent):
                            last_percent = percent
                            if progress_cb:
                                # Map 0–100% download → 0–50% of bar
                                progress_cb(percent * 0.5)
                    except:
                        pass
                    break
        else:
            # Only surface actual errors to status
            if "ERROR:" in s or "Error:" in s:
                if status_cb:
                    status_cb(s)

    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError("yt-dlp failed with exit code "
                           + str(proc.returncode))


def convert_to_clonehero_webm(
    input_path,
    output_path,
    trim_start: float = 0.0,
    pad_start: float = 0.0,
    keep_audio: bool = False,
    progress_cb=None,
    status_cb=None,
    debug_cb=None,
):
    """
    Convert to Clone Hero–friendly WebM.

    - VP8 video (libvpx)
    - If keep_audio=False → no audio track (silent)
    - If keep_audio=True  → Vorbis audio
    - If pad_start>0 and keep_audio=True → pad BOTH video and audio at the front
    """
    if trim_start and pad_start:
        raise ValueError("Cannot use both trim and pad at the same time.")

    original_duration = get_duration_seconds(input_path)
    if original_duration <= 0:
        expected_duration = 0.0
    else:
        expected_duration = max(0.1, original_duration - trim_start) + pad_start

    cmd = ["ffmpeg"]

    # Trim at the start (applies to both audio and video)
    if trim_start:
        cmd += ["-ss", str(trim_start)]

    cmd += ["-i", str(input_path)]

    # Video settings (VP8)
    cmd += [
        "-c:v", "libvpx",
        "-b:v", "6000k",
        "-g", "30",
        "-pix_fmt", "yuv420p",
        "-cpu-used", "4",
    ]

    # Audio settings
    if keep_audio:
        cmd += [
            "-c:a", "libvorbis",
            "-b:a", "192k",
        ]
    else:
        cmd += ["-an"]

    # Build video/audio filters
    vf_filters = []
    af_filters = []

    # Pad video at the start (black frames)
    if pad_start:
        vf_filters.append(f"tpad=start_duration={pad_start}:color=black")

    # Pad audio at the start (silence) IF we’re keeping audio
    if pad_start and keep_audio:
        delay_ms = int(pad_start * 1000)
        # For stereo: delay left|right with the same amount
        af_filters.append(f"adelay={delay_ms}|{delay_ms}")

    # Apply filters if any
    if vf_filters:
        cmd += ["-vf", ",".join(vf_filters)]
    if af_filters:
        cmd += ["-af", ",".join(af_filters)]

    cmd += ["-y", str(output_path)]

    # Map encode 0–100% → 50–100% of UI bar
    def ffmpeg_progress(p):
        if progress_cb:
            progress_cb(50.0 + p * 0.5)

    run_ffmpeg_with_progress(
        cmd,
        expected_duration,
        progress_cb=ffmpeg_progress,
        status_cb=status_cb,
        debug_cb=debug_cb,
    )


def convert_to_mp4(
    input_path,
    output_path,
    trim_start: float = 0.0,
    pad_start: float = 0.0,
    progress_cb=None,
    status_cb=None,
    debug_cb=None,
):
    """
    Convert or pass-through to MP4 (always with audio).

    - If trim_start==0 and pad_start==0 → no re-encode, just move file.
    - Otherwise, re-encode with H.264 + AAC and apply trim/pad to both
      video and audio.
    """
    if trim_start and pad_start:
        raise ValueError("Cannot use both trim and pad at the same time.")

    # No trim/pad: simple move (fast)
    if trim_start == 0 and pad_start == 0:
        Path(input_path).replace(output_path)
        if progress_cb:
            progress_cb(100.0)
        if status_cb:
            status_cb(f"Saved to: {output_path}")
        return

    original_duration = get_duration_seconds(input_path)
    if original_duration <= 0:
        expected_duration = 0.0
    else:
        expected_duration = max(0.1, original_duration - trim_start) + pad_start

    cmd = ["ffmpeg"]

    if trim_start:
        cmd += ["-ss", str(trim_start)]

    cmd += ["-i", str(input_path)]

    vf_filters = []
    af_filters = []

    if pad_start:
        vf_filters.append(f"tpad=start_duration={pad_start}:color=black")
        delay_ms = int(pad_start * 1000)
        af_filters.append(f"adelay={delay_ms}|{delay_ms}")

    if vf_filters:
        cmd += ["-vf", ",".join(vf_filters)]
    if af_filters:
        cmd += ["-af", ",".join(af_filters)]

    cmd += [
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        "-y", str(output_path),
    ]

    def ffmpeg_progress(p):
        if progress_cb:
            progress_cb(50.0 + p * 0.5)

    run_ffmpeg_with_progress(
        cmd,
        expected_duration,
        progress_cb=ffmpeg_progress,
        status_cb=status_cb,
        debug_cb=debug_cb,
    )


def adjust_existing_video(
    input_path: Path,
    output_path: Path,
    trim: float,
    pad: float,
    keep_audio: bool,
    progress_cb=None,
    status_cb=None,
    debug_cb=None,
):
    """
    Adjust an existing WebM file by trimming/padding and optionally
    keeping audio. Uses the same WebM pipeline as convert_to_clonehero_webm.
    """
    input_path = input_path.resolve()
    output_path = output_path.resolve()

    if input_path == output_path:
        ts = int(time.time())
        tmp = input_path.with_name(input_path.stem + f".tmp_{ts}.webm")
        convert_to_clonehero_webm(
            input_path, tmp, trim, pad, keep_audio,
            progress_cb=progress_cb, status_cb=status_cb, debug_cb=debug_cb
        )
        tmp.replace(input_path)
    else:
        convert_to_clonehero_webm(
            input_path, output_path, trim, pad, keep_audio,
            progress_cb=progress_cb, status_cb=status_cb, debug_cb=debug_cb
        )


# =========================
#  WORKER (QThread logic)
# =========================

class Worker(QObject):
    progress = Signal(float)              # 0-100
    status = Signal(str)
    debug = Signal(str)
    finished = Signal(bool, str, str)    # success, message, output_path_str (or "")

    def __init__(self, mode: str, params: dict):
        super().__init__()
        self.mode = mode          # "download" or "adjust"
        self.params = params

    @Slot()
    def run(self):
        try:
            if self.mode == "download":
                out_path = self._run_download()
            elif self.mode == "adjust":
                out_path = self._run_adjust()
            else:
                raise ValueError(f"Unknown mode: {self.mode}")

            self.finished.emit(True, "Done.", str(out_path) if out_path else "")
        except Exception as e:
            self.debug.emit(f"[worker] ERROR: {e}")
            self.finished.emit(False, str(e), "")

    def _run_download(self) -> Path:
        url = self.params["url"]
        output_path: Path = self.params["output_path"]
        trim = self.params["trim"]
        pad = self.params["pad"]
        keep_audio = self.params["audio"]
        fmt = self.params.get("format", "webm")  # "webm" or "mp4"

        if trim and pad:
            raise ValueError("Cannot use both trim and pad at the same time.")

        # Base temp path (we don't care about final extension here)
        tmp_base = Path(tempfile.gettempdir()) / f"ch_temp_{int(time.time())}"
        tmp_file = tmp_base.with_suffix(".mkv")  # what we *ask* yt-dlp to use

        self.debug.emit(f"[worker] Temp base: {tmp_base}")

        # Download with or without audio
        download_video(
            url,
            tmp_file,
            include_audio=(keep_audio or fmt == "mp4"),
            progress_cb=self.progress.emit,
            status_cb=self.status.emit,
            debug_cb=self.debug.emit,
        )

        # Resolve the actual file yt-dlp created
        input_file = tmp_file
        if not input_file.exists():
            candidates = sorted(
                tmp_file.parent.glob(tmp_base.name + ".*"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not candidates:
                raise FileNotFoundError(f"Download file not found: {tmp_file}")
            input_file = candidates[0]
            self.debug.emit(f"[worker] Using downloaded file: {input_file}")

        # WebM path = same as before
        if fmt == "webm":
            convert_to_clonehero_webm(
                input_file,
                output_path,
                trim_start=trim,
                pad_start=pad,
                keep_audio=keep_audio,
                progress_cb=self.progress.emit,
                status_cb=self.status.emit,
                debug_cb=self.debug.emit,
            )
        else:
            # MP4 path: always with audio
            convert_to_mp4(
                input_file,
                output_path,
                trim_start=trim,
                pad_start=pad,
                progress_cb=self.progress.emit,
                status_cb=self.status.emit,
                debug_cb=self.debug.emit,
            )

        # Clean up temp file
        try:
            if input_file.exists():
                input_file.unlink()
                self.debug.emit(f"[worker] Deleted temp file: {input_file}")
        except Exception as e:
            self.debug.emit(f"[worker] Failed to delete temp file: {e}")

        self.status.emit(f"Saved to: {output_path}")
        return output_path

    def _run_adjust(self) -> Path:
        input_path: Path = self.params["input_path"]
        output_path: Path = self.params["output_path"]
        trim = self.params["trim"]
        pad = self.params["pad"]
        keep_audio = self.params["audio"]

        if trim and pad:
            raise ValueError("Cannot use both trim and pad at the same time.")

        self.status.emit("Adjusting video...")
        adjust_existing_video(
            input_path,
            output_path,
            trim=trim,
            pad=pad,
            keep_audio=keep_audio,
            progress_cb=self.progress.emit,
            status_cb=self.status.emit,
            debug_cb=self.debug.emit,
        )
        self.status.emit(f"Saved to: {output_path}")
        return output_path


# =========================
#  DEBUG DIALOG
# =========================

class DebugDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Debug Log")
        self.resize(900, 500)

        layout = QVBoxLayout(self)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.hide)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)

    def closeEvent(self, event):
        # Just hide instead of destroying, so we can live-update
        event.ignore()
        self.hide()

    def set_full_log(self, lines: list[str]):
        self.text.clear()
        if lines:
            self.text.setPlainText("\n".join(lines))
        else:
            self.text.setPlainText("No debug output yet.")

    def append_line(self, line: str):
        if not line:
            return
        # Replace placeholder text on first real line
        if self.text.toPlainText() == "No debug output yet.":
            self.text.clear()
        self.text.append(line)


# =========================
#  MAIN WINDOW (UI)
# =========================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumWidth(700)

        self.thread = None
        self.worker = None
        self.last_output_path: Path | None = None
        self.debug_lines: list[str] = []
        self.debug_dialog: DebugDialog | None = None

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # --- Download group ---
        download_group = QGroupBox("Download from YouTube")
        dl_layout = QGridLayout()

        # URL
        dl_layout.addWidget(QLabel("YouTube URL:"), 0, 0)
        self.dl_url = QLineEdit()
        dl_layout.addWidget(self.dl_url, 0, 1, 1, 3)

        # Song folder + browse
        dl_layout.addWidget(QLabel("Song folder:"), 1, 0)
        self.dl_folder = QLineEdit(".")
        dl_layout.addWidget(self.dl_folder, 1, 1, 1, 2)
        btn_browse_folder = QPushButton("Browse...")
        btn_browse_folder.clicked.connect(self.browse_dl_folder)
        dl_layout.addWidget(btn_browse_folder, 1, 3)

        # Output name
        dl_layout.addWidget(QLabel("Output name:"), 2, 0)
        self.dl_output_name = QLineEdit("video.webm")
        dl_layout.addWidget(self.dl_output_name, 2, 1, 1, 3)

        # Trim / Pad
        dl_layout.addWidget(QLabel("Trim start (sec):"), 3, 0)
        self.dl_trim = QDoubleSpinBox()
        self.dl_trim.setRange(0.0, 9999.0)
        self.dl_trim.setDecimals(2)
        dl_layout.addWidget(self.dl_trim, 3, 1)

        dl_layout.addWidget(QLabel("Pad start (sec):"), 3, 2)
        self.dl_pad = QDoubleSpinBox()
        self.dl_pad.setRange(0.0, 9999.0)
        self.dl_pad.setDecimals(2)
        dl_layout.addWidget(self.dl_pad, 3, 3)

        # Audio checkbox + preset + Download button row
        self.dl_audio = QCheckBox("Embed audio in WebM")
        dl_layout.addWidget(self.dl_audio, 4, 0, 1, 2)

        self.btn_preset = QPushButton("Preset: Clone Hero BG")
        self.btn_preset.clicked.connect(self.apply_preset_clone_hero_bg)
        dl_layout.addWidget(self.btn_preset, 4, 2)

        self.btn_download = QPushButton("Download")
        self.btn_download.clicked.connect(self.start_download)
        dl_layout.addWidget(self.btn_download, 4, 3)

        # Format selector
        dl_layout.addWidget(QLabel("Format:"), 5, 0)
        self.dl_format = QComboBox()
        self.dl_format.addItem("WebM (Clone Hero)")
        self.dl_format.addItem("MP4 (with audio)")
        self.dl_format.currentIndexChanged.connect(self.on_format_changed)
        dl_layout.addWidget(self.dl_format, 5, 1, 1, 3)

        download_group.setLayout(dl_layout)
        layout.addWidget(download_group)

        # --- Adjust group ---
        adjust_group = QGroupBox("Adjust Existing WebM")
        aj_layout = QGridLayout()

        # Input video
        aj_layout.addWidget(QLabel("Input WebM:"), 0, 0)
        self.aj_input = QLineEdit()
        aj_layout.addWidget(self.aj_input, 0, 1, 1, 2)
        btn_browse_input = QPushButton("Browse...")
        btn_browse_input.clicked.connect(self.browse_aj_input)
        aj_layout.addWidget(btn_browse_input, 0, 3)

        # Output video
        aj_layout.addWidget(QLabel("Output WebM (blank = overwrite):"), 1, 0)
        self.aj_output = QLineEdit()
        aj_layout.addWidget(self.aj_output, 1, 1, 1, 3)

        # Trim / Pad
        aj_layout.addWidget(QLabel("Trim start (sec):"), 2, 0)
        self.aj_trim = QDoubleSpinBox()
        self.aj_trim.setRange(0.0, 9999.0)
        self.aj_trim.setDecimals(2)
        aj_layout.addWidget(self.aj_trim, 2, 1)

        aj_layout.addWidget(QLabel("Pad start (sec):"), 2, 2)
        self.aj_pad = QDoubleSpinBox()
        self.aj_pad.setRange(0.0, 9999.0)
        self.aj_pad.setDecimals(2)
        aj_layout.addWidget(self.aj_pad, 2, 3)

        # Audio checkbox
        self.aj_audio = QCheckBox("Keep audio in output")
        aj_layout.addWidget(self.aj_audio, 3, 0, 1, 2)

        # Adjust button
        self.btn_adjust = QPushButton("Adjust")
        self.btn_adjust.clicked.connect(self.start_adjust)
        aj_layout.addWidget(self.btn_adjust, 3, 3)

        adjust_group.setLayout(aj_layout)
        layout.addWidget(adjust_group)

        # --- Status + Progress + Open Folder + Debug ---
        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        bottom_row = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        bottom_row.addWidget(self.progress_bar)

        self.btn_open_folder = QPushButton("Open Folder")
        self.btn_open_folder.setEnabled(False)
        self.btn_open_folder.clicked.connect(self.open_last_folder)
        bottom_row.addWidget(self.btn_open_folder)

        self.btn_debug = QPushButton("Debug Log...")
        self.btn_debug.clicked.connect(self.show_debug_log)
        bottom_row.addWidget(self.btn_debug)

        self.btn_about = QPushButton("About")
        self.btn_about.clicked.connect(self.show_about)
        bottom_row.addWidget(self.btn_about)

        layout.addLayout(bottom_row)

        self.setLayout(layout)

    # --- About ---

    def show_about(self):
        text = (
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "A small utility for preparing Clone Hero background videos:\n"
            "- Download YouTube videos as VP8 WebM\n"
            "- Optionally embed audio in the same file\n"
            "- Or download MP4 with embedded audio\n"
            "- Trim/pad video (and audio) to sync with charts\n\n"
            "Built with Python, PySide6, yt-dlp, and ffmpeg."
        )
        QMessageBox.information(self, "About", text)

    # --- File pickers ---

    def browse_dl_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Song Folder", ".")
        if folder:
            self.dl_folder.setText(folder)

    def browse_aj_input(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select WebM File", ".", "WebM Video (*.webm);;All Files (*)"
        )
        if file_path:
            self.aj_input.setText(file_path)

    # --- Preset button ---

    def apply_preset_clone_hero_bg(self):
        """
        Preset for a simple Clone Hero background video:
        - WebM
        - No embedded audio
        - No trim/pad
        - Output name = video.webm
        - Adjust output keeps audio unchecked by default too
        """
        self.dl_format.setCurrentIndex(0)
        self.dl_audio.setChecked(False)
        self.dl_audio.setEnabled(True)
        self.dl_trim.setValue(0.0)
        self.dl_pad.setValue(0.0)
        self.dl_output_name.setText("video.webm")

        self.aj_audio.setChecked(False)
        self.aj_trim.setValue(0.0)
        self.aj_pad.setValue(0.0)

        self.status_label.setText("Preset applied: Clone Hero BG (silent WebM).")

    # --- Format change handler ---

    def on_format_changed(self, index: int):
        """
        Index 0 = WebM (Clone Hero)
        Index 1 = MP4 (with audio)
        """
        is_webm = (index == 0)
        self.dl_audio.setEnabled(is_webm)

        name = self.dl_output_name.text().strip()

        if is_webm:
            # Switch back to .webm
            if name.lower().endswith(".mp4"):
                self.dl_output_name.setText(name[:-4] + ".webm")
            elif not name:
                self.dl_output_name.setText("video.webm")
        else:
            # MP4 always includes audio
            self.dl_audio.setChecked(True)
            if name.lower().endswith(".webm"):
                self.dl_output_name.setText(name[:-5] + ".mp4")
            elif not name:
                self.dl_output_name.setText("video.mp4")

    # --- Thread helpers ---

    def _start_worker(self, mode, params):
        self.btn_download.setEnabled(False)
        self.btn_adjust.setEnabled(False)
        self.btn_preset.setEnabled(False)
        self.btn_open_folder.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Working...")

        # Reset debug log for this run
        self.debug_lines.clear()
        if self.debug_dialog and self.debug_dialog.isVisible():
            self.debug_dialog.set_full_log(self.debug_lines)

        self.thread = QThread()
        self.worker = Worker(mode, params)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress)
        self.worker.status.connect(self.on_status)
        self.worker.debug.connect(self.on_debug)
        self.worker.finished.connect(self.on_finished)

        self.thread.start()

    @Slot(float)
    def on_progress(self, value):
        self.progress_bar.setValue(int(value))

    @Slot(str)
    def on_status(self, text):
        self.status_label.setText(text)

    @Slot(str)
    def on_debug(self, text):
        if not text:
            return
        self.debug_lines.append(text)
        if self.debug_dialog and self.debug_dialog.isVisible():
            self.debug_dialog.append_line(text)

    @Slot(bool, str, str)
    def on_finished(self, success, message, out_path_str):
        # Force visual 100% on success
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText(message)
            if out_path_str:
                self.last_output_path = Path(out_path_str)
                self.btn_open_folder.setEnabled(True)
        else:
            self.status_label.setText("Error: " + message)
            QMessageBox.critical(self, "Error", message)

        self.btn_download.setEnabled(True)
        self.btn_adjust.setEnabled(True)
        self.btn_preset.setEnabled(True)

        self.thread.quit()
        self.thread.wait()
        self.worker = None
        self.thread = None

    # --- Actions ---

    def start_download(self):
        url = self.dl_url.text().strip()
        folder = Path(self.dl_folder.text().strip() or ".").expanduser()
        output_name = self.dl_output_name.text().strip() or "video.webm"

        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a YouTube URL.")
            return

        fmt = "webm" if self.dl_format.currentIndex() == 0 else "mp4"

        # Fix extension based on format
        if fmt == "webm":
            if not output_name.lower().endswith(".webm"):
                output_name += ".webm"
        else:
            if not output_name.lower().endswith(".mp4"):
                output_name += ".mp4"

        folder.mkdir(parents=True, exist_ok=True)
        output_path = folder / output_name

        params = {
            "url": url,
            "output_path": output_path,
            "trim": float(self.dl_trim.value()),
            "pad": float(self.dl_pad.value()),
            "audio": self.dl_audio.isChecked(),
            "format": fmt,
        }

        self._start_worker("download", params)

    def start_adjust(self):
        input_path_str = self.aj_input.text().strip()
        if not input_path_str:
            QMessageBox.warning(self, "Missing input", "Please select an input WebM file.")
            return

        input_path = Path(input_path_str).expanduser()

        output_str = self.aj_output.text().strip()
        if output_str:
            out_path = Path(output_str).expanduser()
            if out_path.suffix.lower() != ".webm":
                out_path = out_path.with_suffix(".webm")
        else:
            out_path = input_path  # in-place

        params = {
            "input_path": input_path,
            "output_path": out_path,
            "trim": float(self.aj_trim.value()),
            "pad": float(self.aj_pad.value()),
            "audio": self.aj_audio.isChecked(),
        }

        self._start_worker("adjust", params)

    # --- Open Folder action ---

    def open_last_folder(self):
        if not self.last_output_path:
            return
        folder = self.last_output_path.parent
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    # --- Debug log popup ---

    def show_debug_log(self):
        if self.debug_dialog is None:
            self.debug_dialog = DebugDialog(self)
        self.debug_dialog.set_full_log(self.debug_lines)
        self.debug_dialog.show()
        self.debug_dialog.raise_()
        self.debug_dialog.activateWindow()


# =========================
#  ENTRY POINT
# =========================

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()