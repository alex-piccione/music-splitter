# Music Splitter

A utility tool designed to split large MP3 audio files into smaller segments based on a specified duration while preserving ID3 metadata (Artist, Album, Title). It ensures that the resulting files are ready for playback on various media players.

## Features

- **Automated Splitting**: Segment long MP3 files into equal durations.
- **Metadata Preservation**: Automatically copies ID3 tags (Artist, Album, Title) from the source file to all generated segments.
- **User Interface**: A clean Tkinter-based GUI for easy interaction.
- **Error Handling**: Robust validation for file types and segment durations.

## Prerequisites

This application requires **FFmpeg** to process audio files via the `pydub` library.

### Installation of FFmpeg

#### Windows
1. Download the latest build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the archive to a permanent location (e.g., `C:\ffmpeg`).
3. Add the `bin` directory (e.g., `C:\ffmpeg\bin`) to your system's **PATH** environment variable.
4. Verify installation by running `ffmpeg -version` in a terminal.

#### macOS
Using Homebrew:
```bash
brew install ffmpeg
```

#### Linux
Using your package manager (e.g., Ubuntu/Debian):
```bash
sudo apt update && sudo apt install ffmpeg
```

## Installation

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — fast Python package manager
- [FFmpeg](https://ffmpeg.org) — required by `pydub` for audio processing

### Setup

1. Clone this repository.
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv .venv --python 3.14
   uv pip install -r requirements.txt
   ```

## Usage

> **Note:** VS Code will automatically detect and offer to activate `.venv`. You can also select the interpreter via `Ctrl+Shift+P` → `Python: Select Interpreter`.

Activate the virtual environment and run:
```bash
source .venv/bin/activate
python main.py
```

Or run directly without activating:
```bash
.venv/bin/python main.py
```

## CUE file

.cue file example:
```
PERFORMER "Various Artists"
TITLE "Ambient Lounge  - Vol. 5 - CD 1"
FILE "Ambient Lounge - Vol. 5 - CD 1.mp3" MP3
  TRACK 01 AUDIO
    TITLE "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    PERFORMER "1 Giant Leap feat. Ro. Williams & Maxi Jazz - My Culture "
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Groove Armada - Lovebox"
    PERFORMER "Groove Armada - Lovebox"
    INDEX 01 05:24:10
  TRACK 03 AUDIO
    TITLE "4 Hero - Hold it down"
    PERFORMER "4 Hero - Hold it down"
    INDEX 01 11:01:01
```

## Project Management


- [TODO.md](./TODO.md) - Current tasks and upcoming work.
- [CHANGELOG.md](./CHANGELOG.md) - Historical record of completed features and changes.
