import os
import math
import shutil
import subprocess
import yaml
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, TRK, COMM


class MP3Splitter:
    """
    A utility class to split MP3 files into equal segments while preserving metadata.
    Uses FFmpeg stream-copy (-c copy): lossless and fast, no re-encoding.
    """

    UI_TEXT_FILE = os.path.join(os.path.dirname(__file__), "..", "ui-text", "english.yml")

    def __init__(self):
        pass

    @classmethod
    def load_comm_settings(cls) -> dict | None:
        """Read the provenance COMM frame values from ui-text/english.yml.

        Returns {'lang', 'description', 'text'} or None if unavailable/invalid,
        so splitting still works when the file is missing or unreadable.
        """
        try:
            with open(cls.UI_TEXT_FILE, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError):
            return None
        comm = data.get("comm")
        if not isinstance(comm, dict) or not comm.get("text"):
            return None
        return {
            "lang": str(comm.get("language", "eng")),
            "description": str(comm.get("description", "")),
            "text": str(comm["text"]),
        }

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

            comm_cfg = self.load_comm_settings()

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
                    # Add the provenance comment unless an identical one was already copied from the source.
                    if comm_cfg and not any(
                        c.lang == comm_cfg["lang"] and c.desc == comm_cfg["description"]
                        for c in target_tags.getall("COMM")
                    ):
                        target_tags.add(COMM(encoding=3, lang=comm_cfg["lang"],
                                             desc=comm_cfg["description"], text=[comm_cfg["text"]]))
                    # Label each part with its position unless the source already had a track number.
                    # Note: the frame class is named TRK but its ID3v2 code (and dict key) is 'TRCK'
                    if 'TRCK' not in target_tags:
                        target_tags.add(TRK(encoding=3, text=f"{i+1}/{num_segments}"))
                    target_tags.save()
                except Exception as e:
                    print(f"Warning: Could not copy metadata to {filename}: {e}")

                created_files.append(output_path)

            return created_files

        except Exception as e:
            raise Exception(f"An error occurred during splitting: {str(e)}")
