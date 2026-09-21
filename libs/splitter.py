import os
import math
import shutil
import subprocess
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError


class MP3Splitter:
    """
    A utility class to split MP3 files into equal segments while preserving metadata.
    Uses FFmpeg stream-copy (-c copy): lossless and fast, no re-encoding.
    """

    def __init__(self):
        pass

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

    def split(self, input_path: str, output_folder: str, segment_minutes: float) -> list[str]:
        """
        Splits an MP3 file into multiple parts of specified duration and copies metadata.

        Args:
            input_path (str): Path to the source MP3 file.
            output_folder (str): Directory where the parts will be saved.
            segment_minutes (float): Duration of each segment in minutes.

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

                filename = f"{str(i + 1).zfill(2)}.mp3"
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
                if original_tags:
                    try:
                        target_tags = ID3(output_path)
                        for key, value in original_tags.items():
                            target_tags.add(value)
                        target_tags.save()
                    except Exception as e:
                        print(f"Warning: Could not copy metadata to {filename}: {e}")

                created_files.append(output_path)

            return created_files

        except Exception as e:
            raise Exception(f"An error occurred during splitting: {str(e)}")
