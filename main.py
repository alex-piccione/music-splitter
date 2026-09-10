import os
import tkinter as tk
from tkinter import filedialog
from ui import create_main_window, alert
from libs.splitter import MP3Splitter

class MusicSplitterApp:
    def __init__(self):
        self.root = tk.Tk()
        # TODO: Read mp3splt_path and other configs from config.txt
        self.mp3splt_path = "./libs/mp3splt_2.6.2_i386/mp3splt.exe"
        self.last_selected_file = ""
        
        # Initialize UI and get callback functions
        self.update_file_label, self.log_message = create_main_window(
            self.root, 
            self.on_split_button_click, 
            self.close_app
        )

    def select_file(self, extension):
        if not extension:
            alert("Please, provide an extension.", "Select a file")
            self.log_message("Error: No extension provided.")
            return None
        
        initial_dir = os.path.dirname(self.last_selected_file) if self.last_selected_file else "."
        file_types = [("MP3", ".mp3")] if extension == "mp3" else None
        
        filename = filedialog.askopenfilename(
            title=f"Select a {extension} file", 
            initialdir=initial_dir, 
            filetypes=file_types
        )    

        if filename:
            self.last_selected_file = filename
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

        splitter = MP3Splitter()
        output_folder = os.path.join(os.path.dirname(mp3_file), "split_output")
        try:
            parts = splitter.split(mp3_file, output_folder, segment_minutes=10.0)
            self.log_message(f"Created {len(parts)} segments in: {output_folder}")
            alert(f"Done! {len(parts)} segments saved.", "Split Complete")
        except Exception as e:
            self.log_message(f"Error: {e}")
            alert(str(e), "Split Failed")

    def close_app(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MusicSplitterApp()
    app.run()
