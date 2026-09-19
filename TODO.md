# TODO

## Backlog


- **[fix/08_replace_pydub_ffmpeg]** Remove pydub, split via FFmpeg stream-copy (`-c copy -f segment`) + mutagen for duration/tags. Fixes on Python 3.14:
  - `ModuleNotFoundError: No module named 'audioop'` (removed in 3.13; pydub fallback `pyaudioop` not installed) → app crashes at startup
  - `SyntaxWarning: "\(" is an invalid escape sequence` spam from `pydub/utils.py` in terminal
  Also drops lossy decode/re-encode of every segment. Update unit tests (currently mock pydub) and CHANGELOG.
