import os
import math
from pydub import AudioSegment

class MP3Splitter:
    """
    A utility class to split MP3 files into equal segments.
    """

    def __init__(self):
        pass

    def split(self, input_path: str, output_folder: str, segment_minutes: float) -> list[str]:
        """
        Splits an MP3 file into multiple parts of specified duration.

        Args:
            input_path (str): Path to the source MP3 file.
            output_folder (str): Directory where the parts will be saved.
            segment_minutes (float): Duration of each segment in minutes.

        Returns:
            list[str]: A list of paths to the created MP3 segments.

        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If the segment duration is invalid.
            Exception: For errors during audio processing.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Source file not found: {input_path}")

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
                created_files.append(output_path)

            return created_files

        except Exception as e:
            raise Exception(f"An error occurred during splitting: {str(e)}")
