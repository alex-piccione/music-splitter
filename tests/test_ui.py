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
        self.update_file_label, self.log_message, self.get_naming = create_main_window(
            self.root,
            lambda: self.split_calls.append(1),
            lambda: setattr(self, "close_called", True),
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

    def test_naming_default(self):
        self.assertEqual(self.get_naming(), "numbers")

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
