# Changelog

## 2026-09-22
- Feature 10: every split part is stamped with a provenance `COMM` frame (`eng` / "Splitter provenance" / "Original file split with Music Splitter by Alessandro Piccione."); the values live in `ui-text/english.yml`, with a built-in fallback if the file is missing; a source COMM frame with the same language+description is kept as-is, never duplicated.
- Feature 8: split parts now carry a track-number frame (`TRCK`, e.g. `2/5`) indicating their position among the generated parts; if the source file already has one, it is copied as-is and never overridden.
- Reworked UI layout: fixed-height message bar on top, Browse row (button + selected file), then *File names* and *Part length* settings, and a big **SPLIT** button disabled until a source file is chosen.
- Removed the "Selected File" frame, the Status Log widget, the Close button and all alert popups; status and errors are shown in the top message bar (errors in red).
- Splitting now runs in a background thread with the UI frozen while running; result reported as "Done: N parts created".
- Logging kept internally (timestamped in-memory list); will later become a log file shown via a button on failure.
- Unified user settings into a single `settings.txt` (KEY=VALUE), replacing the split between `config.txt` and `preferences.json`; removed the stray committed `config.txt`.
- Feature 4: added a "File names" selector (radio buttons): *Numbers* (`01.mp3`) or *File+Numbers* (`<source_stem>_01.mp3`); choice is persisted in `config.txt` (`FILENAME_FORMAT`).
- Added `ID3_tag.md` documenting the ID3v2 tags written to split files; linked from README.
- Feature 1: "Split File" dialog now opens in the last directory used, persisted across app runs via `preferences.json`.

## 2026-09-21
- Added "File names" option (radio buttons): *Numbers* (`01.mp3`) or *File+Numbers* (`<source_stem>_01.mp3`); choice persisted in `config.txt`.
- Part length is now user-selectable via radio buttons: **5**, **10** or **15 minutes** (default: 10); persisted as `PART_LENGTH_MINUTES`. Removed the obsolete `SPLIT_FIXED_DURATION_MINUTES` setting.
- Split output now goes into a folder named after the source file (e.g., `My Mix.mp3` → `My Mix/01.mp3`, …), created next to the source file.
- Removed the obsolete `OUTPUT_FOLDER` setting from `config.txt`.
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
