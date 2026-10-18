# tiktok-analyzer

A Claude Code skill that lets Claude analyze a TikTok video from its link.

Claude can't play video or open TikTok pages. This skill closes that gap. Give it a TikTok URL (or a saved video file) and it produces three things Claude can read: the post metadata, a timestamped transcript of the speech, and a frame every couple of seconds. Claude then answers from those, separating what was said, what was shown on screen, and what the caption claims.

Everything runs locally. No API keys.

## Install

Clone the repo into your Claude Code skills folder under the same name:

```
git clone https://github.com/Lettiiii/tiktok-analyzer ~/.claude/skills/tiktok-analyzer
python -m pip install -r ~/.claude/skills/tiktok-analyzer/requirements.txt
```

ffmpeg is bundled through `imageio-ffmpeg`, so there is nothing else to install. The first run downloads the Whisper speech model once, which takes a few minutes.

## Use

Copy a link from TikTok (Share, then Copy link) and paste it into Claude Code with a question, for example "what does this say?" or "pull out the facts and the repo he mentions". The skill triggers on TikTok links by itself.

You can also run the extractor directly:

```
python scripts/extract.py "<url-or-video-file>" "<out_dir>" [max_frames] [whisper_model]
```

It writes `metadata.json`, `transcript.txt` and `frames/` into `<out_dir>`.

## Limits

- Frames are samples, so something brief can fall between two of them. Raise `max_frames` to look closer.
- Whisper mishears names and numbers. Claude is told to cross-check against on-screen text.
- Photo carousels, private, deleted and region-blocked videos may not download. Save the video and pass the file path instead.
- TikTok changes often. If a download fails, run `python -m pip install -U "yt-dlp[curl-cffi]"` first.
