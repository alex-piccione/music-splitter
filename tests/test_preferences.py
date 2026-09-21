import json
import os
import tempfile
import unittest

import main
from main import load_last_dir, save_last_dir


class TestLastDirPersistence(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.original_pref_file = main.PREFERENCES_FILE
        main.PREFERENCES_FILE = os.path.join(self.tmpdir.name, "preferences.json")
        self.some_dir = os.path.join(self.tmpdir.name, "music")
        os.makedirs(self.some_dir)

    def tearDown(self):
        main.PREFERENCES_FILE = self.original_pref_file

    def test_load_missing_file_returns_empty(self):
        self.assertEqual(load_last_dir(), "")

    def test_load_corrupt_file_returns_empty(self):
        with open(main.PREFERENCES_FILE, "w") as f:
            f.write("{not valid json")
        self.assertEqual(load_last_dir(), "")

    def test_load_nonexistent_directory_returns_empty(self):
        with open(main.PREFERENCES_FILE, "w") as f:
            json.dump({"last_dir": "/definitely/not/here"}, f)
        self.assertEqual(load_last_dir(), "")

    def test_save_then_load_roundtrip(self):
        save_last_dir(self.some_dir)
        self.assertEqual(load_last_dir(), self.some_dir)

    def test_saved_value_survives_reload(self):
        save_last_dir(self.some_dir)
        # Simulate a fresh app start by reading again
        self.assertTrue(os.path.isfile(main.PREFERENCES_FILE))
        with open(main.PREFERENCES_FILE) as f:
            data = json.load(f)
        self.assertEqual(data["last_dir"], self.some_dir)


if __name__ == "__main__":
    unittest.main()
