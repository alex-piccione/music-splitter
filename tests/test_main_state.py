import json
import os
import tempfile
import unittest

from main import load_last_dir, save_last_dir


class TestLastDirPersistence(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.state_path = os.path.join(self.tmpdir.name, "state.json")
        self.some_dir = os.path.join(self.tmpdir.name, "music")
        os.makedirs(self.some_dir)

    def test_load_missing_file_returns_empty(self):
        self.assertEqual(load_last_dir(self.state_path), "")

    def test_load_corrupt_file_returns_empty(self):
        with open(self.state_path, "w") as f:
            f.write("{not valid json")
        self.assertEqual(load_last_dir(self.state_path), "")

    def test_load_nonexistent_directory_returns_empty(self):
        with open(self.state_path, "w") as f:
            json.dump({"last_dir": "/definitely/not/here"}, f)
        self.assertEqual(load_last_dir(self.state_path), "")

    def test_save_then_load_roundtrip(self):
        save_last_dir(self.some_dir, self.state_path)
        self.assertEqual(load_last_dir(self.state_path), self.some_dir)

    def test_saved_value_survives_reload(self):
        save_last_dir(self.some_dir, self.state_path)
        # Simulate a fresh app start by reading again
        self.assertTrue(os.path.isfile(self.state_path))
        with open(self.state_path) as f:
            data = json.load(f)
        self.assertEqual(data["last_dir"], self.some_dir)


if __name__ == "__main__":
    unittest.main()
