# Changelog

## 2026-09-22
- Feature 1: "Split File" dialog now opens in the last directory used, persisted across app runs via `.music_splitter_state.json`.

## 2026-09-21
- Replaced unmaintained `pydub` with direct FFmpeg stream-copy (`-c copy`) splitting: fixes `audioop` ModuleNotFoundError on Python ≥3.13 and SyntaxWarning noise; splitting is now lossless (no re-encode).
- Removed `pydub` from requirements; FFmpeg is now used directly.
- Made split test robust to MP3 duration estimation padding.

## 2026-07-06
- Implement Core MP3 Splitting Engine.
- Added unit tests for the splitter module.
- Fixed test clarity and TODO casing.

## 2026-07-05
- Implemented modern UI using `tkinter.ttk`.
- Improved Layout (Header, Selected File Display, Status/Log Area).
- Integrated File Selection and Split trigger.
- Enhanced error handling and user feedback.
