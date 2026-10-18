# tiktok-analyzer

A Claude Code skill that lets Claude analyze a TikTok video from its link.

Claude can't play video or open TikTok pages. Give this skill a TikTok URL (or a saved video file) and it produces three things Claude can read: the post metadata, a timestamped transcript of the speech, and a frame every couple of seconds. Claude then answers from those, keeping apart what was said, what was shown on screen, and what the caption claims.

Everything runs locally. No API keys.

## Example

Prompt: "What does this say, and which repo does he mention?" The link was a 53-second TikTok by @bengusberg recommending a GitHub repo for Claude Code.

The transcript covered the speech. It listed four complaints about Claude Code (assumptions without asking, over-complicated code, unrelated breakage, no loops) and a recommendation to install a free GitHub repo. The repo name is never spoken. It appears on screen at about 44 seconds as `multica-ai/andrej-karpathy-skills`, and the frame at about 9 seconds shows the repo with 216.3k stars. Without the frames, the answer would have been missing the one thing the viewer needs.

Whisper also wrote "cloud" every time the creator said "Claude". Claude read it from context and said it had corrected it.

The video is used here only as a test input: https://www.tiktok.com/@bengusberg/video/7691911646532439309

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
- It is built for pulling facts out of a video (claims, steps, names, quotes). I have not tested it on questions about hooks, pacing or why a video performed well.

## Responsible use

Use it for personal analysis. Downloading videos can go against TikTok's terms of service, and the videos belong to their creators. You are responsible for how you use it.

## License

MIT
