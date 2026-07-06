import os
import math
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError

class MP3Splitter:
    """
    A utility class to split MP3 files into equal segments while preserving metadata.
    """

    def __init__(self):
        pass

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
            # Load the audio file
            audio = AudioSegment.from_file(input_path, format="mp3")
            duration_ms = len(audio)
            segment_ms = int(segment_minutes * 60 * 1000)
            
            num_segments = math.ceil(duration_ms / segment_ms)
            created_files = []

            # Prepare metadata from original file
            original_tags = None
            try:
                original_tags = ID3(input_path)
            except ID3NoHeaderError:
                pass # No tags present

            for i in range(num_segments):
                start_time = i * segment_ms
                end_time = min((i + 1) * segment_ms, duration_ms)
                
                # Extract the segment
                segment = audio[start_time:end_time]
                
                # Generate filename: 01.mp3, 02.mp3, etc.
                filename = f"{str(i + 1).zfill(2)}.mp3"
                output_path = os.path.join(output_folder, filename)
                
                # Export the segment
                segment.export(output_path, format="mp3")
                
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
