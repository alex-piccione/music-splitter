import tkinter as tk

pad = 10 # common padding for UI
pad_xs = 5 
pad_xl = 20

button_blue = {"bg": "blue", "fg": "white", "font": ("Arial", 12, "bold")}
button_red = {"bg": "red", "fg": "white", "font": ("Arial", 12, "bold")}


def alert(message, title="Alert"):
    # Create a new top-level window
    alert_window = tk.Toplevel()
    
    # Set the window title and size
    alert_window.title(title)
    alert_window.geometry("200x100")
    alert_window.update()
        
    # Create a Label widget to display the message
    message_label = tk.Label(alert_window, text=message)
    message_label.pack(padx=pad, pady=pad)
    
    # Add a "OK" button to close the window
    button_width = alert_window.winfo_width() - 2 * pad
    ok_button = tk.Button(alert_window, text="OK", width=button_width, command=alert_window.destroy)
    #ok_button.pack(pady=5, anchor="bottom")
    ok_button.pack(side=tk.BOTTOM, anchor=tk.S,  padx=pad, pady=pad,)

def create_main_window(root, split_file, close_app):

    # Create the main window and set its properties
    root.title("Music Splitter")
    root.geometry("600x400")

    # Create the "Select File" button
    #select_button = tk.Button(root, text="Split File", command=split_file)
    #select_button.pack(padx=pad, pady=pad_xs)
    # crear el botón "Split File" y posicionarlo en la izquierda
    split_button = tk.Button(root, text="Split File", command=split_file, **button_blue)
    split_button.grid(row=0, column=0, padx=pad, pady=pad)

    # agregar la descripción a la derecha del botón
    description = "Split the selected audio file into multiple tracks."
    description_label = tk.Label(root, text=description, justify=tk.LEFT)
    description_label.grid(row=0, column=1, padx=pad, pady=pad)

    # Create the "Close" button
    #close_button = tk.Button(root, text="Close", command=close_app)
    #close_button.pack(side="bottom", anchor=tk.E, padx=pad, pady=pad)
    # Create the "Close" button
    close_button = tk.Button(root, text="Close", command=close_app, **button_red)
    close_button.grid(row=1, column=1, sticky=tk.E, padx=pad, pady=pad)

    # Configure the rows and columns of the grid to expand automatically
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)