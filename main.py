import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from ui import create_main_window
from libs.splitter import MP3Splitter

SETTINGS_FILE = "settings.txt"


def read_settings():
    """Parse KEY=VALUE lines from settings.txt into a dict."""
    settings = {}
    try:
        with open(SETTINGS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    settings[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return settings


def save_setting(key, value):
    """Persist one setting, preserving any other lines currently in settings.txt."""
    settings = read_settings()
    settings[key] = value
    try:
        with open(SETTINGS_FILE, "w") as f:
            for k, v in settings.items():
                f.write(f"{k}={v}\n")
    except OSError:
        pass


def load_last_dir():
    """Return the last directory used in the file dialog, or '' if unknown."""
    d = read_settings().get("LAST_DIR", "")
    return d if isinstance(d, str) and os.path.isdir(d) else ""


class MusicSplitterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.last_selected_file = ""
        self.last_dir = load_last_dir()
        # In-memory log; will later be backed by a log file shown on failure
        self.log_lines = []

        # Load settings from settings.txt
        self.config = read_settings()
        self.part_length_m = int(self.config.get("PART_LENGTH_MINUTES", 10))
        self.filename_format = self.config.get("FILENAME_FORMAT", "numbers")

        # Initialize UI and get callback functions
        (self.update_file_label, self.set_message, self.set_enabled,
         self.get_filename_format, self.get_part_length_m) = create_main_window(
            self.root,
            self.on_browse_click,
            self.on_split_button_click,
            filename_format=self.filename_format,
            initial_part_length_m=self.part_length_m,
        )

    def log_message(self, msg):
        stamp = datetime.now().isoformat(timespec="seconds")
        self.log_lines.append(f"[{stamp}] {msg}")

    def select_file(self, extension):
        if not extension:
            self.log_message("Error: No extension provided.")
            return None

        initial_dir = self.last_dir or "."
        file_types = [("MP3", ".mp3")] if extension == "mp3" else None

        filename = filedialog.askopenfilename(
            title=f"Select a {extension} file",
            initialdir=initial_dir,
            filetypes=file_types
        )

        if filename:
            self.last_selected_file = filename
            self.last_dir = os.path.dirname(filename)
            save_setting("LAST_DIR", self.last_dir)
            self.update_file_label(filename)
            self.log_message(f"File selected: {os.path.basename(filename)}")
        else:
            self.log_message("File selection cancelled.")

        return filename

    def on_browse_click(self):
        filename = self.select_file("mp3")
        if filename:
            self.set_message("")
            self.set_enabled(True)

    def on_split_button_click(self):
        mp3_file = self.last_selected_file
        if not mp3_file:
            return

        naming = self.get_filename_format()
        part_length_m = self.get_part_length_m()

        self.set_enabled(False)
        self.set_message(f"Splitting {os.path.basename(mp3_file)}…")
        self.log_message(f"Starting split process for: {os.path.basename(mp3_file)}")

        threading.Thread(target=self._run_split, args=(mp3_file, naming, part_length_m), daemon=True).start()

    def _run_split(self, mp3_file, naming, part_length_m):
        try:
            splitter = MP3Splitter()
            output_folder = MP3Splitter.default_output_folder(mp3_file)
            created_files = splitter.split(
                mp3_file, output_folder, part_length_m, naming=naming,
            )
            result = (len(created_files), None)
            self.log_message(f"Split complete: {len(created_files)} segments created in {output_folder}")
        except Exception as e:
            result = (None, str(e))
            self.log_message(f"Error during split: {e}")

        # Persist settings and update the UI from the main thread only
        self.root.after(0, lambda: self._on_split_done(naming, part_length_m, *result))

    def _on_split_done(self, naming, part_length_m, count, error):
        if naming != self.filename_format:
            self.filename_format = naming
            save_setting("FILENAME_FORMAT", naming)
        save_setting("PART_LENGTH_MINUTES", str(part_length_m))

        if error is not None:
            self.set_message(error, is_error=True)
        else:
            self.set_message(f"Done: {count} parts created")
        self.set_enabled(True)

    def close_app(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MusicSplitterApp()
    app.run()
