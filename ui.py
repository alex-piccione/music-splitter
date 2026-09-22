import os
import tkinter as tk
from tkinter import ttk

pad = 10 # common padding for UI
pad_xs = 5 
pad_xl = 20


def create_main_window(root, browse_file, split_file, filename_format="numbers", initial_part_length_m=10):
    style = ttk.Style()

    root.title("Music Splitter")
    root.geometry("520x400")

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title label
    title_label = ttk.Label(main_frame, text="Music Splitter", font=("Arial", 16, "bold"))
    title_label.pack(anchor=tk.W, pady=(0, pad))

    # Top message bar: fixed height so controls never move when a message appears
    message_bar = ttk.Frame(main_frame, height=28)
    message_bar.pack(fill=tk.X, pady=(0, pad))
    message_bar.pack_propagate(False)
    message_var = tk.StringVar(value="")
    message_label = ttk.Label(message_bar, textvariable=message_var, anchor=tk.W)
    message_label.pack(side=tk.LEFT, fill=tk.X)

    # Browse row: button + selected file name
    browse_frame = ttk.Frame(main_frame)
    browse_frame.pack(fill=tk.X, pady=(0, pad))

    browse_button = ttk.Button(browse_frame, text="Browse…", command=browse_file)
    browse_button.pack(side=tk.LEFT)

    file_var = tk.StringVar(value="No file selected")
    file_label = ttk.Label(browse_frame, textvariable=file_var, foreground="gray")
    file_label.pack(side=tk.LEFT, padx=(pad_xs * 2, 0))

    # File names format selector
    naming_frame = ttk.LabelFrame(main_frame, text="File names", padding="10")
    naming_frame.pack(fill=tk.X, pady=(0, pad))

    naming_var = tk.StringVar(value=filename_format)
    ttk.Radiobutton(
        naming_frame, text="Numbers (\u201cpart_01.mp3\u201d)",
        variable=naming_var, value="numbers",
    ).pack(side=tk.LEFT, padx=(0, pad_xl))
    ttk.Radiobutton(
        naming_frame, text="File+Numbers (\u201cDJ-AAA_part_01.mp3\u201d)",
        variable=naming_var, value="file+numbers",
    ).pack(side=tk.LEFT)

    # Part length selection (minutes: 5 / 10 / 15)
    part_len_var = tk.StringVar(value=str(initial_part_length_m))
    part_len_frame = ttk.LabelFrame(main_frame, text="Part length", padding="10")
    part_len_frame.pack(fill=tk.X, pady=(0, pad))

    for minutes in ("5", "10", "15"):
        ttk.Radiobutton(
            part_len_frame, text=f"{minutes} min",
            variable=part_len_var, value=minutes,
        ).pack(side=tk.LEFT, padx=(0, pad_xl))

    # Big SPLIT button, disabled until a source file is selected
    style.configure("Big.TButton", font=("Arial", 14, "bold"))
    split_button = ttk.Button(
        main_frame, text="SPLIT", style="Big.TButton",
        state=tk.DISABLED, command=split_file,
    )
    split_button.pack(fill=tk.X, pady=(pad, 0))

    def update_file_label(path):
        if path:
            file_var.set(os.path.basename(path))
            file_label.config(foreground="")
        else:
            file_var.set("No file selected")
            file_label.config(foreground="gray")

    def set_message(msg, is_error=False):
        message_var.set(msg)
        message_label.config(foreground="red" if is_error else "")

    def set_enabled(enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        browse_button.config(state=state)
        split_button.config(state=state)
        for frame in (naming_frame, part_len_frame):
            for child in frame.winfo_children():
                if isinstance(child, ttk.Radiobutton):
                    child.config(state=state)

    def get_filename_format():
        return naming_var.get()

    def get_part_length_m():
        return int(part_len_var.get())

    return update_file_label, set_message, set_enabled, get_filename_format, get_part_length_m
