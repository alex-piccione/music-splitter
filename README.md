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

1. Ensure you have [Python 3.x](https://www.python.org/) installed.
2. Clone this repository.
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using:
```bash
python main.py
```

## Project Management

- [TODO.md](./TODO.md) - Current tasks and upcoming work.
- [CHANGELOG.md](./CHANGELOG.md) - Historical record of completed features and changes.
