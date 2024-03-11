import tkinter as tk
from tkinter import filedialog
  
# Top level window 
window = tk.Tk() 
window.title("TextBox Input") 

# Create a BooleanVar to track button state
browse_state = tk.BooleanVar()

# Function to get input
def getInput(): 
    if (browse_state.get()): 
        inp = inputtxt.get() 
        lbl.config(text = "Provided Input: "+ inp)
    else:
        pathLabel.config(text = "Pick Folder Path", fg = "red")

# Function to lookup folder path
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    pathLabel.config(text = "Folder Path: " + folder_path, fg = "black")
    browse_state.set(True)

# TextBox Creation 
inputtxt = tk.Entry(window, width = 60) 
inputtxt.grid(row=0, column=0)

# Create a button to browse for a folder
browse_button = tk.Button(window, text="Browse Folder", command=browse_folder)
browse_button.grid(row=0, column=1)

pathLabel = tk.Label(window, text = "")
pathLabel.grid(row=1, column=0)

# Button Creation 
printButton = tk.Button(window, text = "Print",  command = getInput) 
printButton.grid(row=2, column=0, columnspan=2)

# Label Creation 
lbl = tk.Label(window, text = "") 
lbl.grid(row=3, column=0)

boollbl = tk.Label(window, text = str(browse_state)) 
boollbl.grid(row=4, column=0)

window.mainloop()