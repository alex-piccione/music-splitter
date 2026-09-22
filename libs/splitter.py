import os
import math
import shutil
import subprocess
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, COMM, TRK

UI_TEXT_FILE = Path(__file__).resolve().parent.parent / "ui-text" / "english.yml"
DEFAULT_PROVENANCE_TEXT = "Original file split with Music Splitter by Alessandro Piccione."
PROVENANCE_LANG = "eng"
PROVENANCE_DESC = "Splitter provenance"


def load_provenance_text(path: Path = UI_TEXT_FILE) -> str:
    """Read the provenance comment from ui-text/english.yml, falling back to a built-in default."""
    try:
        import yaml
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        text = data.get("comm provenance text")
        if isinstance(text, str) and text.strip():
            return text.strip()
    except Exception:
        pass
    return DEFAULT_PROVENANCE_TEXT


class MP3Splitter:
    """
    A utility class to split MP3 files into equal segments while preserving metadata.
    Uses FFmpeg stream-copy (-c copy): lossless and fast, no re-encoding.
    """

    def __init__(self, provenance_text: str | None = None):
        self.provenance_text = provenance_text if provenance_text is not None else load_provenance_text()

    @staticmethod
    def default_output_folder(input_path: str) -> str:
        """Returns <source_dir>/<source_stem>, i.e. a folder named after the source file."""
        directory = os.path.dirname(os.path.abspath(input_path))
        stem = os.path.splitext(os.path.basename(input_path))[0]
        return os.path.join(directory, stem)

    @staticmethod
    def _find_ffmpeg() -> str:
        path = shutil.which("ffmpeg")
        if not path:
            raise RuntimeError(
                "FFmpeg was not found on PATH. Install FFmpeg and ensure 'ffmpeg' is accessible."
            )
        return path

    NAMING_NUMBERS = "numbers"
    NAMING_FILE_PLUS_NUMBERS = "file+numbers"

    def split(self, input_path: str, output_folder: str, segment_minutes: float,
              naming: str = NAMING_NUMBERS) -> list[str]:
        """
        Splits an MP3 file into multiple parts of specified duration and copies metadata.

        Args:
            input_path (str): Path to the source MP3 file.
            output_folder (str): Directory where the parts will be saved.
            segment_minutes (float): Duration of each segment in minutes.
            naming (str): Filename style: "numbers" ("01.mp3") or
                "file+numbers" ("<source_stem>_01.mp3").

        Returns:
            list[str]: A list of paths to the created MP3 segments.

        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If the segment duration is invalid or file is not an MP3.
            Exception: For errors during audio processing.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Source file not found: {input_path}")

        if not input_path.lower().endswith(".mp3"):
            raise ValueError("Only MP3 files are supported.")

        if segment_minutes <= 0:
            raise ValueError("Segment duration must be greater than zero.")

        if naming not in (self.NAMING_NUMBERS, self.NAMING_FILE_PLUS_NUMBERS):
            raise ValueError(f"Unknown filename format: {naming}")

        stem = os.path.splitext(os.path.basename(input_path))[0]

        # Ensure output directory exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        try:
            ffmpeg = self._find_ffmpeg()

            duration_s = MP3(input_path).info.length
            segment_s = segment_minutes * 60
            num_segments = max(1, math.ceil(duration_s / segment_s))

            # Prepare metadata from original file
            original_tags = None
            try:
                original_tags = ID3(input_path)
            except ID3NoHeaderError:
                pass  # No tags present

            created_files = []
            for i in range(num_segments):
                start_s = i * segment_s
                length_s = min(segment_s, duration_s - start_s)

                num = str(i + 1).zfill(2)
                if naming == self.NAMING_FILE_PLUS_NUMBERS:
                    filename = f"{stem}_{num}.mp3"
                else:
                    filename = f"{num}.mp3"
                output_path = os.path.join(output_folder, filename)

                cmd = [
                    ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", f"{start_s:.3f}",
                    "-t", f"{length_s:.3f}",
                    "-i", input_path,
                    "-c", "copy",
                    output_path,
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(result.stderr.strip())

                # Copy metadata if available
                try:
                    target_tags = ID3(output_path)
                    if original_tags:
                        for key, value in original_tags.items():
                            target_tags.add(value)
                    # Label each part with its position unless the source already had a track number.
                    # Note: the frame class is named TRK but its ID3v2 code (and dict key) is 'TRCK'
                    if 'TRCK' not in target_tags:
                        target_tags.add(TRK(encoding=3, text=f"{i+1}/{num_segments}"))
                    # Stamp every part with its origin; skip if an identical frame was already copied from the source.
                    has_same_comm = any(
                        f.lang == PROVENANCE_LANG and f.desc == PROVENANCE_DESC
                        for f in target_tags.getall('COMM')
                    )
                    if not has_same_comm:
                        target_tags.add(COMM(
                            encoding=3, lang=PROVENANCE_LANG,
                            desc=PROVENANCE_DESC, text=[self.provenance_text],
                        ))
                    target_tags.save()
                except Exception as e:
                    print(f"Warning: Could not copy metadata to {filename}: {e}")

                created_files.append(output_path)

            return created_files

        except Exception as e:
            raise Exception(f"An error occurred during splitting: {str(e)}")
