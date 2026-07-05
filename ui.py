import tkinter as tk
from tkinter import ttk

pad = 10 # common padding for UI
pad_xs = 5 
pad_xl = 20


def alert(message, title="Alert"):
    # Create a new top-level window
    alert_window = tk.Toplevel()
    
    # Set the window title and size
    alert_window.title(title)
    alert_window.geometry("300x150")
    alert_window.transient(True) # Make it appear on top of the main window
    alert_window.grab_set()      # Make it modal
    alert_window.update()
        
    # Create a Label widget to display the message
    message_label = ttk.Label(alert_window, text=message, wraplength=250, justify="center")
    message_label.pack(padx=pad, pady=pad, expand=True)
    
    # Add a "OK" button to close the window
    ok_button = ttk.Button(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(side=tk.BOTTOM, anchor=tk.S, padx=pad, pady=pad)

def create_main_window(root, split_file, close_app):
    # Use ttk style
    style = ttk.Style()
    
    # Create the main window and set its properties
    root.title("Music Splitter")
    root.geometry("600x400")

    # Main container frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header section
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Title label
    title_label = ttk.Label(header_frame, text="Music Splitter", font=("Arial", 18, "bold"))
    title_label.pack(side=tk.LEFT)

    # Action area (Split Button + Description)
    action_frame = ttk.Frame(main_frame)
    action_frame.pack(fill=tk.X, pady=10)

    split_button = ttk.Button(action_frame, text="Split File", command=split_file)
    split_button.pack(side=tk.LEFT, padx=(0, 20))

    description = "Split the selected audio file into multiple tracks."
    description_label = ttk.Label(action_frame, text=description, wraplength=300)
    description_label.pack(side=tk.LEFT)

    # --- NEW: File Selection Display ---
    file_display_frame = ttk.LabelFrame(main_frame, text="Selected File", padding="10")
    file_display_frame.pack(fill=tk.X, pady=10)

    file_path_label = ttk.Label(file_display_frame, text="No file selected", font=("Arial", 9, "italic"))
    file_path_label.pack(fill=tk.X)

    # --- NEW: Status/Log Area ---
    log_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="10")
    log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    log_text = tk.Text(log_frame, height=6, state='disabled', font=("Consolas", 9))
    log_text.pack(fill=tk.BOTH, expand=True)

    # Bottom area (Close button)
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

    close_button = ttk.Button(bottom_frame, text="Close", command=close_app)
    close_button.pack(side=tk.RIGHT)

    # Helper functions to interact with the UI from outside
    def update_file_label(path):
        file_path_label.config(text=path if path else "No file selected")

    def log_message(msg):
        log_text.config(state='normal')
        log_text.insert(tk.END, f"> {msg}\n")
        log_text.see(tk.END)
        log_text.config(state='disabled')

    return update_file_label, log_message
