import json
import os
import tkinter as tk
from tkinter import filedialog
from ui import create_main_window, alert
from libs.splitter import MP3Splitter

PREFERENCES_FILE = "preferences.json"


def load_last_dir():
    """Return the last directory used in the file dialog, or '' if unknown."""
    try:
        with open(PREFERENCES_FILE) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return ""
    d = data.get("last_dir") if isinstance(data, dict) else None
    return d if isinstance(d, str) and os.path.isdir(d) else ""


def save_last_dir(dir_path):
    try:
        with open(PREFERENCES_FILE, "w") as f:
            json.dump({"last_dir": dir_path}, f)
    except OSError:
        pass


class MusicSplitterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.last_selected_file = ""
        self.last_dir = load_last_dir()
        
        # Load settings from config.txt
        self.config = self._read_config()
        self.segment_minutes = float(self.config.get("SPLIT_FIXED_DURATION_MINUTES", 10.0))
        self.filename_format = self.config.get("FILENAME_FORMAT", "numbers")
        
        # Initialize UI and get callback functions
        self.update_file_label, self.log_message, self.get_filename_format = create_main_window(
            self.root, 
            self.on_split_button_click, 
            self.close_app,
            filename_format=self.filename_format,
        )

    @staticmethod
    def _read_config():
        """Parse KEY=VALUE lines from config.txt into a dict."""
        config = {}
        try:
            with open("config.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        config[k.strip()] = v.strip()
        except FileNotFoundError:
            pass
        return config

    @staticmethod
    def _save_config_key(key, value):
        """Persist one setting, preserving any other lines currently in config.txt."""
        config = MusicSplitterApp._read_config()
        config[key] = value
        try:
            with open("config.txt", "w") as f:
                for k, v in config.items():
                    f.write(f"{k}={v}\n")
        except OSError:
            pass

    def select_file(self, extension):
        if not extension:
            alert("Please, provide an extension.", "Select a file", master=self.root)
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
            save_last_dir(self.last_dir)
            self.update_file_label(filename)
            self.log_message(f"File selected: {os.path.basename(filename)}")
        else:
            self.log_message("File selection cancelled.")
        
        return filename

    def on_split_button_click(self):
        mp3_file = self.select_file("mp3")
        if not mp3_file:
            return

        self.log_message(f"Starting split process for: {os.path.basename(mp3_file)}")
        alert(f"Processing: {os.path.basename(mp3_file)}", "Process Started", master=self.root)
        
        naming = self.get_filename_format()
        if naming != self.filename_format:
            self.filename_format = naming
            self._save_config_key("FILENAME_FORMAT", naming)

        try:
            splitter = MP3Splitter()
            output_folder = MP3Splitter.default_output_folder(mp3_file)
            created_files = splitter.split(
                mp3_file, output_folder, self.segment_minutes, naming=naming,
            )
            self.log_message(f"Split complete: {len(created_files)} segments created in {output_folder}")
        except Exception as e:
            self.log_message(f"Error during split: {e}")
            alert(str(e), "Split Error", master=self.root)

    def close_app(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MusicSplitterApp()
    app.run()
