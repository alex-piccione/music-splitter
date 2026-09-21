# TODO

## Backlog


- **[docs/01_id3_tag]** Create `ID3_tag.md` documenting the ID3v2 tags written by the app:

  | Code | Meaning                 | Value in test |
  |------|-------------------------|---------------|
  | TIT2 | Title (Track title)     | 'Test Title'  |
  | TPE1 | Lead performer (Artist) | 'Test Artist' |
  | TALB | Album name              | 'Test Album'  |

  Link it from `README.md` so the README stays short.
- **[docs/02_cue_file]** Create `CUE.md` documenting the CUE sheet files produced by the app (structure, fields, how they reference the split segments). Link it from `README.md`.
- **[fix/08_replace_pydub_ffmpeg]** Remove pydub, split via FFmpeg stream-copy (`-c copy -f segment`) + mutagen for duration/tags. Fixes on Python 3.14:
  - `ModuleNotFoundError: No module named 'audioop'` (removed in 3.13; pydub fallback `pyaudioop` not installed) → app crashes at startup
  - `SyntaxWarning: "\(" is an invalid escape sequence` spam from `pydub/utils.py` in terminal
  Also drops lossy decode/re-encode of every segment. Update unit tests (currently mock pydub) and CHANGELOG.
