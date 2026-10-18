---
name: tiktok-analyzer
description: Analyze a TikTok video from its URL (or a downloaded video file) by extracting metadata, a timestamped audio transcript and sampled frames, then reading them to pull out facts, claims, steps, products, quotes and on-screen text. Use this whenever the user pastes a tiktok.com / vm.tiktok.com / vt.tiktok.com link, asks what a TikTok says or shows, wants a TikTok summarized, fact-checked, or turned into notes, or says Claude can't open a TikTok link. Also use for any short-form vertical video file (mp4/mov) the user wants analyzed. Claude cannot play video or fetch TikTok pages itself, so do not guess from the URL, run this skill first.
---

# TikTok analyzer

Claude cannot watch video or open TikTok links, but it can read images and text. This skill converts the video into both: a timestamped transcript, evenly spaced frames, and the post metadata. Then you read them and answer.

## Steps

1. Run the extractor (works for a URL or a local video path):
   ```
   python ~/.claude/skills/tiktok-analyzer/scripts/extract.py "<url-or-file>" "<out_dir>"
   ```
   Use the scratchpad or a temp dir for `<out_dir>`, not the user's project. Optional args: max frames (default 24), Whisper model (default `base`; use `small` if the speech is noisy, accented or non-English). First run downloads the Whisper model, so allow a few minutes.
2. Read `metadata.json` (caption, author, date, hashtags, counts, sound), then `transcript.txt`.
3. Read the frames in `frames/` with the Read tool, in order. File names carry the timestamp (`t0012.3s.jpg`), so you can line each frame up with the transcript. Frames matter because much of TikTok's information is burned-in text, product shots, charts and demos that are never spoken.
4. Answer the user's actual question. For fact extraction, separate what was **said** (transcript), **shown** (frames, including on-screen text), and **claimed in the caption**. Cite timestamps so the user can check the source.

## Rules for honest analysis

- Frames are samples, about one per 2 seconds. Do not claim something was absent from the video, only that it did not appear in the sampled frames or transcript. For a specific moment, re-run with a higher max frames count.
- Whisper makes mistakes on names, brands, numbers and slang. Flag any fact that hinges on one transcribed word or number, and cross-check it against on-screen text.
- A creator saying something is not evidence it is true. When the user wants fact-checking, list the claims, mark which are verifiable, and verify with a web search rather than repeating the claim as fact.
- Whisper often mishears product names (it heard "Claude" as "cloud" every time in testing). Use context and the on-screen text to correct these, and say you did.
- Engagement counts and captions are context, not verdicts.

## When it fails

- **Photo carousels / slideshows**: yt-dlp may not download them. Ask the user to screen-record or save the video, then pass the file path.
- **Login-walled, private, region-blocked or deleted videos**: the download errors out. Ask for a saved file instead.
- **"Unexpected response from webpage request"**: TikTok's bot check needs browser impersonation. Run `python -m pip install -U "yt-dlp[curl-cffi]"` and retry. This was needed on the first real test.
- **HTTP 403 or other extractor errors**: TikTok changes often. Run `python -m pip install -U yt-dlp` and retry once.
- **No speech**: the transcript is empty, lean on frames and caption, and say so.
- Missing packages: `python -m pip install "yt-dlp[curl-cffi]" imageio-ffmpeg faster-whisper` (ffmpeg is bundled through imageio-ffmpeg, no system install needed).
