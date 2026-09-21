import unittest
import tkinter as tk
from tkinter import ttk

from ui import create_main_window


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.browse_calls = []
        self.split_calls = []
        (self.update_file_label, self.set_message, self.set_enabled,
         self.get_filename_format, self.get_part_length_m) = create_main_window(
            self.root,
            lambda: self.browse_calls.append(1),
            lambda: self.split_calls.append(1),
        )

    def tearDown(self):
        self.root.destroy()

    @staticmethod
    def _collect(parent, cls, out):
        for w in parent.winfo_children():
            if isinstance(w, cls):
                out.append(w)
            TestMainWindow._collect(w, cls, out)
        return out

    def _buttons(self):
        return self._collect(self.root, ttk.Button, [])

    def _radios(self):
        return self._collect(self.root, ttk.Radiobutton, [])

    def _all_label_text(self):
        texts = []
        stack = list(self.root.winfo_children())
        while stack:
            w = stack.pop()
            if isinstance(w, ttk.Label):
                texts.append(str(w.cget("text")))
            stack.extend(w.winfo_children())
        return " ".join(texts)

    def test_window_title(self):
        self.assertEqual(self.root.title(), "Music Splitter")

    def test_browse_button_triggers_callback(self):
        button = next(b for b in self._buttons() if "Browse" in str(b.cget("text")))
        button.invoke()
        self.assertEqual(self.browse_calls, [1])

    def test_split_button_disabled_initially(self):
        button = next(b for b in self._buttons() if b.cget("text") == "SPLIT")
        self.assertEqual(str(button["state"]), "disabled")

    def test_set_enabled_toggles_controls(self):
        split = next(b for b in self._buttons() if b.cget("text") == "SPLIT")
        browse = next(b for b in self._buttons() if "Browse" in str(b.cget("text")))
        self.set_enabled(True)
        self.assertEqual(str(split["state"]), "normal")
        self.assertEqual(str(browse["state"]), "normal")
        self.set_enabled(False)
        self.assertEqual(str(split["state"]), "disabled")
        self.assertEqual(str(browse["state"]), "disabled")
        for radio in self._radios():
            self.assertEqual(str(radio["state"]), "disabled")

    def test_update_file_label_shows_basename(self):
        self.update_file_label("/tmp/some mix.mp3")
        self.assertIn("some mix.mp3", self._all_label_text())

    def test_set_message_updates_bar(self):
        self.set_message("Done: 3 parts created")
        self.assertIn("Done: 3 parts created", self._all_label_text())

    def test_set_error_message_uses_red_foreground(self):
        self.set_message("boom", is_error=True)
        labels = self._collect(self.root, ttk.Label, [])
        error_labels = [l for l in labels if "boom" in str(l.cget("text"))]
        self.assertTrue(error_labels)
        self.assertEqual(str(error_labels[0].cget("foreground")), "red")

    def test_part_length_default(self):
        self.assertEqual(self.get_part_length_m(), 10)

    def test_part_length_options(self):
        radios = [r for r in self._radios()
                  if str(r.cget("value")) in {"5", "10", "15"}]
        self.assertEqual({str(r.cget("value")) for r in radios}, {"5", "10", "15"})

    def test_part_length_selection_reports_choice(self):
        target = next(r for r in self._radios() if str(r.cget("value")) == "15")
        target.invoke()
        self.assertEqual(self.get_part_length_m(), 15)

    def test_naming_radios_default_to_numbers(self):
        radios = [r for r in self._radios()
                  if str(r.cget("value")) in {"numbers", "file+numbers"}]
        self.assertEqual(len(radios), 2)
        self.assertEqual(self.get_filename_format(), "numbers")

    def test_naming_selector_reports_selection(self):
        target = next(r for r in self._radios() if str(r.cget("value")) == "file+numbers")
        target.invoke()
        self.assertEqual(self.get_filename_format(), "file+numbers")

    def test_create_main_window_accepts_persisted_values(self):
        root2 = tk.Tk()
        root2.withdraw()
        try:
            _, _, _, get_fmt, get_len = create_main_window(
                root2, lambda: None, lambda: None,
                filename_format="file+numbers", initial_part_length_m=5,
            )
            self.assertEqual(get_fmt(), "file+numbers")
            self.assertEqual(get_len(), 5)
        finally:
            root2.destroy()


if __name__ == "__main__":
    unittest.main()
