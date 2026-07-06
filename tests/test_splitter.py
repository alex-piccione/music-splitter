import unittest
import os
import shutil
from libs.splitter import MP3Splitter
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

class TestMP3Splitter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_path = 'tests/fixtures/sample.mp3'
        cls.output_dir = 'tests/output_test'
        cls.splitter = MP3Splitter()

    def setUp(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_split_success(self):
        """Verify splitting works and creates correct filenames."""
        # sample.mp3 is 12 seconds. Split into 4 second segments -> 3 parts.
        # We pass duration in minutes. 4 seconds = 4/60 minutes = 0.0666...
        parts = self.splitter.split(self.fixture_path, self.output_dir, 4/60)
        
        self.assertEqual(len(parts), 3)
        for i in range(1, 4):
            expected_filename = f"{str(i).zfill(2)}.mp3"
            expected_path = os.path.join(self.output_dir, expected_filename)
            self.assertTrue(os.path.exists(expected_path))

    def test_invalid_extension(self):
        """Ensure non-mp3 files trigger ValueError."""
        bad_file = 'tests/fixtures/not_an_audio.txt'
        with open(bad_file, 'w') as f:
            f.write("Not audio")
        
        try:
            with self.assertRaises(ValueError) as cm:
                self.splitter.split(bad_file, self.output_dir, 1.0)
            self.assertEqual(str(cm.exception), "Only MP3 files are supported.")
        finally:
            if os.path.exists(bad_file):
                os.remove(bad_file)

    def test_invalid_duration(self):
        """Ensure non-positive durations raise ValueError."""
        bad_duration = 0
        with self.assertRaises(ValueError) as cm:
            self.splitter.split(self.fixture_path, self.output_dir, bad_duration)
        self.assertEqual(str(cm.exception), "Segment duration must be greater than zero.")

    def test_file_not_found(self):
        """Ensure FileNotFoundError is raised for missing files."""
        with self.assertRaises(FileNotFoundError):
            self.splitter.split("non_existent.mp3", self.output_dir, 1.0)

    def test_metadata_preservation(self):
        """Verify metadata is copied correctly."""
        parts = self.splitter.split(self.fixture_path, self.output_dir, 4/60)
        first_part = parts[0]
        
        audio = MP3(first_part)
        self.assertIn('TIT2', audio)
        self.assertEqual(str(audio['TIT2'][0]), 'Test Title')
        self.assertIn('TPE1', audio)
        self.assertEqual(str(audio['TPE1'][0]), 'Test Artist')
        self.assertIn('TALB', audio)
        self.assertEqual(str(audio['TALB'][0]), 'Test Album')

if __name__ == '__main__':
    unittest.main()
