import os
import tempfile
import unittest

import main
from main import load_last_dir, read_settings, save_setting


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.original_settings_file = main.SETTINGS_FILE
        main.SETTINGS_FILE = os.path.join(self.tmpdir.name, "settings.txt")
        self.some_dir = os.path.join(self.tmpdir.name, "music")
        os.makedirs(self.some_dir)

    def tearDown(self):
        main.SETTINGS_FILE = self.original_settings_file

    def test_read_missing_file_returns_empty_dict(self):
        self.assertEqual(read_settings(), {})

    def test_save_then_read_roundtrip_preserves_other_keys(self):
        save_setting("LAST_DIR", self.some_dir)
        save_setting("FILENAME_FORMAT", "numbers")
        settings = read_settings()
        self.assertEqual(settings["LAST_DIR"], self.some_dir)
        self.assertEqual(settings["FILENAME_FORMAT"], "numbers")

    def test_saved_value_survives_reload(self):
        save_setting("PART_LENGTH_MINUTES", "15.0")
        self.assertTrue(os.path.isfile(main.SETTINGS_FILE))
        with open(main.SETTINGS_FILE) as f:
            content = f.read()
        self.assertIn("PART_LENGTH_MINUTES=15.0\n", content)

    def test_comments_and_blank_lines_ignored(self):
        with open(main.SETTINGS_FILE, "w") as f:
            f.write("# a comment\n\nNOT_A_SETTING\nKEY=value\n")
        self.assertEqual(read_settings(), {"KEY": "value"})


class TestLastDirPersistence(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.original_settings_file = main.SETTINGS_FILE
        main.SETTINGS_FILE = os.path.join(self.tmpdir.name, "settings.txt")
        self.some_dir = os.path.join(self.tmpdir.name, "music")
        os.makedirs(self.some_dir)

    def tearDown(self):
        main.SETTINGS_FILE = self.original_settings_file

    def test_load_missing_file_returns_empty(self):
        self.assertEqual(load_last_dir(), "")

    def test_load_garbage_line_returns_empty(self):
        with open(main.SETTINGS_FILE, "w") as f:
            f.write("no equals sign here\n")
        self.assertEqual(load_last_dir(), "")

    def test_load_nonexistent_directory_returns_empty(self):
        save_setting("LAST_DIR", "/definitely/not/here")
        self.assertEqual(load_last_dir(), "")

    def test_save_then_load_roundtrip(self):
        save_setting("LAST_DIR", self.some_dir)
        self.assertEqual(load_last_dir(), self.some_dir)


class TestLogging(unittest.TestCase):
    def setUp(self):
        import main as m
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.log_path = os.path.join(self.tmpdir.name, "test.log")
        self.original_handlers = m.logger.handlers[:]
        self.original_log_file = m.LOG_FILE
        m.LOG_FILE = self.log_path

    def tearDown(self):
        main.logger.handlers = self.original_handlers
        main.LOG_FILE = self.original_log_file

    def _read_log(self):
        with open(self.log_path, encoding="utf-8") as f:
            return f.read()

    def test_setup_logging_writes_timestamped_lines_to_file(self):
        main.setup_logging()
        main.logger.info("hello log")
        content = self._read_log()
        self.assertIn("INFO hello log", content)
        self.assertRegex(content, r"^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\] INFO hello log$")

    def test_error_level_is_recorded(self):
        main.setup_logging()
        main.logger.error("boom")
        self.assertIn("ERROR boom", self._read_log())

    def test_repeated_setup_does_not_duplicate_entries(self):
        main.setup_logging()
        main.setup_logging()
        main.logger.info("once only")
        self.assertEqual(self._read_log().count("once only"), 1)

    def test_splitter_warnings_share_the_same_log_file(self):
        from libs.splitter import logger as splitter_logger
        self.assertIs(splitter_logger, main.logger)


if __name__ == "__main__":
    unittest.main()
