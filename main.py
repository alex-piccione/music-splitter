import os
import tkinter as tk
from tkinter import filedialog
from ui import create_main_window, alert

mp3splt_path = "./libs/mp3splt_2.6.2_i386/mp3splt.exe"
last_selected_file = ""  # variable to store the last selected file
initial_path = "A:/"


def select_file(extension):
    if not extension: return alert("Please, provide an extension.", "Select a file")
    
    global last_selected_file
        
    # Use the directory of the last selected file as the initial directory
    initial_dir = os.path.dirname(last_selected_file) if last_selected_file else "."
    file_types = [("MP3", ".mp3")] if extension == "mp3" else None
    filename = filedialog.askopenfilename(title=f"Select a {extension} file", initialdir=initial_dir, filetypes=file_types)    

    # Update the last selected file variable
    if filename:
        last_selected_file = filename
    
    # returns the full file path
    return filename

def split_file():
    mp3_file = select_file("mp3")
    if not mp3_file: return

    alert("mp3 selected")

    #os.system(f"{mp3splt_path} {mp3_file}")


def close_app():
    root.destroy()

root = tk.Tk()
create_main_window(root, split_file, close_app)
root.mainloop()


root.mainloop()