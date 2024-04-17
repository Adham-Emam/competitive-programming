"""
FileFlow
A simple file organizer application.
"""

import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import shutil
import json
import os

# Constants
WINDOW_TITLE = "FileFlow"
WINDOW_SIZE = "400x225"
FONT_STYLE = ("Calibri", 18)
ICON_PATH = "icon.ico"

# Global Variables
selected_dir = ""


def main():
    """Create the main window and configure the user interface."""
    root = tk.Tk()

    # Set the title of the window
    root.title(WINDOW_TITLE)

    # Set window size
    root.geometry(WINDOW_SIZE)

    # Create a styled frame
    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    create_ui(frame)

    # Run the Tkinter event loop
    root.mainloop()


def create_ui(frame):
    title_label = ttk.Label(
        frame, text="Select a Directory to organize", font=FONT_STYLE
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    selected_directory_label = ttk.Label(
        frame, text="No directory selected.", wraplength=300
    )
    selected_directory_label.grid(row=1, column=0, columnspan=2, pady=10)

    msg_label = ttk.Label(frame, text="", wraplength=300)
    msg_label.grid(row=2, column=0, columnspan=2, pady=10)

    select_button = ttk.Button(
        frame,
        text="Browse",
        command=lambda: handle_select_click(selected_directory_label, msg_label),
    )
    select_button.grid(row=3, column=0, pady=20, padx=5, sticky=tk.W)

    open_button = ttk.Button(frame, text="Open", command=handle_open_click)
    open_button.grid(row=3, column=1, columnspan=2, pady=20, padx=5, sticky=tk.W)

    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(1, weight=1)


def handle_select_click(dir_label, msg_label):
    """Handle the click on the Browse button."""
    global selected_dir
    selected_dir = select_directory(dir_label)
    if selected_dir:
        organize()
        msg_label.config(text="Directory Organized Successfully")


def select_directory(dir_label):
    """Open a directory selection dialog and update the directory label."""
    directory_path = filedialog.askdirectory()

    if directory_path:
        dir_label.config(text=f"Selected Directory: {directory_path}")
        return directory_path
    else:
        dir_label.config(text="No directory selected.")


def handle_open_click():
    """Handle the click on the Open button."""
    try:
        # Check if the file exists
        if os.path.exists(selected_dir):
            # Get the absolute path of the file
            abs_path = os.path.abspath(selected_dir)
            # Check the operating system and execute the appropriate command
            if os.name == "nt":  # Windows
                subprocess.run(["explorer.exe", "/select,", abs_path], shell=True)
            elif os.name == "posix":  # macOS and Linux
                subprocess.run(["open", "-R", abs_path])
            else:
                print("Unsupported operating system.")
        else:
            print(f"File '{selected_dir}' does not exist.")
    except NameError:
        pass


def organize():
    """Organize files based on the specified rules."""
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)

    # Change directory to the selected one
    os.chdir(selected_dir)

    # call the organizing functions
    create_directories(data)
    move_files(data)
    remove_empty_directories()


def create_directories(data):
    """Create Directories"""
    try:
        for key in data:
            dir_path = os.path.join(selected_dir, key)
            os.makedirs(dir_path, exist_ok=True)
    except FileExistsError:
        pass


def move_files(data):
    """move each file to its specified directory"""
    for file_name in os.listdir(selected_dir):
        file_path = os.path.join(selected_dir, file_name)
        # check if file
        if os.path.isfile(file_path):
            # check exetention and move file to the appropriate directory
            ext = os.path.splitext(file_name)[-1]
            for key in data:
                if ext in data[key]:
                    destination_dir = os.path.join(selected_dir, key)
                    print(f"Moving {file_name} to {destination_dir}")
                    shutil.move(file_path, os.path.join(destination_dir, file_name))


def remove_empty_directories():
    for root, dirs, files in os.walk(selected_dir, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")
            except OSError:
                # Directory not empty, skip
                pass


if __name__ == "__main__":
    main()
