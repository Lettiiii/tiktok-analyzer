"""TikTok URL (or local video) -> out_dir/{metadata.json, transcript.txt, frames/}.

Usage: python extract.py <url-or-file> <out_dir> [max_frames=24] [whisper_model=base]
"""
import json, subprocess, sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import yt_dlp
from faster_whisper import WhisperModel

src, out = sys.argv[1], Path(sys.argv[2])
max_frames = int(sys.argv[3]) if len(sys.argv) > 3 else 24
model_name = sys.argv[4] if len(sys.argv) > 4 else "base"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
(out / "frames").mkdir(parents=True, exist_ok=True)

if Path(src).is_file():
    video, meta = Path(src), {}
else:
    opts = {"outtmpl": str(out / "video.%(ext)s"), "format": "best[ext=mp4]/best",
            "ffmpeg_location": ffmpeg, "quiet": True, "noprogress": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(src, download=True)
        video = Path(ydl.prepare_filename(info))
    keys = ["id", "uploader", "uploader_id", "description", "title", "upload_date", "duration",
            "view_count", "like_count", "comment_count", "repost_count", "track", "artists", "tags"]
    meta = {k: info.get(k) for k in keys if info.get(k) is not None}

# Decode audio with our own ffmpeg: faster-whisper's PyAV decoding breaks on newer av releases.
pcm = subprocess.run([ffmpeg, "-loglevel", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
                      "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
segments, ainfo = WhisperModel(model_name, compute_type="int8").transcribe(audio, vad_filter=True)
lines = [f"[{s.start:6.1f}s] {s.text.strip()}" for s in segments]
(out / "transcript.txt").write_text("\n".join(lines), encoding="utf-8")
duration = meta.get("duration") or len(audio) / 16000
meta.update(duration=duration, language=ainfo.language)

# ~one frame per 2s, spread evenly if the video is long. ffmpeg once per frame keeps timestamps exact.
step = max(2.0, duration / max_frames)
times = [round(i * step + 0.3, 1) for i in range(int(duration / step) + 1) if i * step + 0.3 < duration]
for t in times:
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-ss", str(t), "-i", str(video),
                    "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "3",
                    str(out / "frames" / f"t{t:06.1f}s.jpg")], check=True)
meta["frame_times"] = times
(out / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"ok: {len(times)} frames, {len(lines)} transcript lines, {duration:.0f}s, lang={ainfo.language}")
