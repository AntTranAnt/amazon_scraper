import tkinter as tk
from tkinter import filedialog
from BenqAmazonScraper import BenqAmazonScraper

# Top level window 
window = tk.Tk() 
window.title("TextBox Input") 

# Create a BooleanVar to track button state
browse_state = tk.BooleanVar()
file_state = tk.BooleanVar()

# Function to lookup folder path
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    pathLabel.config(text = "Folder Path: " + folder_path, fg = "black")
    amazonScraper.setFolderPath(folder_path)
    browse_state.set(True)

#Create button to browse for file
browse_file_button = tk.Button(window, text="Browse File")
browse_file_button.grid(row=1, column=0, pady=5)

# Create a button to browse for a folder
browse_button = tk.Button(window, text="Browse Folder", command = browse_folder)
browse_button.grid(row=1, column=0, pady=5)

pathFolderLabel = tk.Label(window, text = "")
pathFolderLabel.grid(row=1, column=1)