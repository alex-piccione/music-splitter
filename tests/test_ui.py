import unittest
import tkinter as tk
from tkinter import ttk

from ui import alert, create_main_window


class TestAlert(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.root.destroy()

    def _find_widget(self, parent, cls):
        found = []
        for w in parent.winfo_children():
            if isinstance(w, cls):
                found.append(w)
            found.extend(self._find_widget(w, cls))
        return found

    def test_alert_creates_titled_dialog(self):
        alert("Hello", "My Title")
        dialogs = [w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel)]
        self.assertEqual(len(dialogs), 1)
        self.assertEqual(dialogs[0].title(), "My Title")

    def test_alert_shows_message_and_ok_closes(self):
        alert("Something happened", "Info")
        dialog = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        labels = self._find_widget(dialog, ttk.Label)
        self.assertTrue(any("Something happened" in str(l.cget("text")) for l in labels))
        buttons = self._find_widget(dialog, ttk.Button)
        ok = next(b for b in buttons if b.cget("text") == "OK")
        ok.invoke()
        self.root.update_idletasks()
        self.assertNotIn(dialog, self.root.winfo_children())


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.split_calls = []
        self.close_called = False
        self.update_file_label, self.log_message, self.get_filename_format, self.get_part_length_m = (
            create_main_window(
                self.root,
                lambda: self.split_calls.append(1),
                lambda: setattr(self, "close_called", True),
            )
        )

    def tearDown(self):
        self.root.destroy()

    def _buttons(self):
        return self._find_buttons(self.root)

    @staticmethod
    def _find_buttons(parent):
        found = []
        for w in parent.winfo_children():
            if isinstance(w, ttk.Button):
                found.append(w)
            found.extend(TestMainWindow._find_buttons(w))
        return found

    def test_window_title(self):
        self.assertEqual(self.root.title(), "Music Splitter")

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

    def test_part_length_custom_initial(self):
        root = tk.Tk()
        root.withdraw()
        callbacks = create_main_window(
            root, lambda: None, lambda: None, initial_part_length_m=5,
        )
        try:
            self.assertEqual(callbacks[3](), 5)
        finally:
            root.destroy()
    def test_split_button_triggers_callback(self):
        button = next(b for b in self._buttons() if b.cget("text") == "Split File")
        button.invoke()
        self.assertEqual(self.split_calls, [1])

    def test_close_button_triggers_callback(self):
        button = next(b for b in self._buttons() if b.cget("text") == "Close")
        button.invoke()
        self.assertTrue(self.close_called)

    def test_update_file_label_updates_text(self):
        self.update_file_label("/tmp/test.mp3")
        labels = [w for w in self.root.winfo_children()]
        text = ""
        stack = list(labels)
        while stack:
            w = stack.pop()
            if isinstance(w, ttk.Label):
                text += str(w.cget("text"))
            stack.extend(w.winfo_children())
        self.assertIn("/tmp/test.mp3", text)

    @staticmethod
    def _collect(parent, cls, out):
        for w in parent.winfo_children():
            if isinstance(w, cls):
                out.append(w)
            TestMainWindow._collect(w, cls, out)
        return out

    def _radios(self):
        return self._collect(self.root, ttk.Radiobutton, [])

    def test_naming_radios_default_to_numbers(self):
        radios = [r for r in self._radios()
                  if str(r.cget("value")) in {"numbers", "file+numbers"}]
        self.assertEqual(len(radios), 2)
        values = {str(r.cget("value")) for r in radios}
        self.assertEqual(values, {"numbers", "file+numbers"})
        self.assertEqual(self.get_filename_format(), "numbers")

    def test_naming_selector_reports_selection(self):
        target = next(r for r in self._radios() if str(r.cget("value")) == "file+numbers")
        target.invoke()
        self.assertEqual(self.get_filename_format(), "file+numbers")

    def test_create_main_window_accepts_persisted_format(self):
        root2 = tk.Tk()
        root2.withdraw()
        try:
            _, _, get_fmt, _ = create_main_window(
                root2, lambda: None, lambda: None, filename_format="file+numbers"
            )
            self.assertEqual(get_fmt(), "file+numbers")
        finally:
            root2.destroy()

    def test_log_message_appends_to_status_log(self):
        self.log_message("hello world")
        texts = []
        stack = list(self.root.winfo_children())
        while stack:
            w = stack.pop()
            if isinstance(w, tk.Text):
                texts.append(w.get("1.0", tk.END))
            stack.extend(w.winfo_children())
        self.assertTrue(any("> hello world" in t for t in texts))


if __name__ == "__main__":
    unittest.main()
