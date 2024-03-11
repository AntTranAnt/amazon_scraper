import tkinter as tk
from tkinter import filedialog
  
# Top level window 
window = tk.Tk() 
window.title("TextBox Input") 
window.geometry('400x200') 

# Function to get input and print
def printInput(): 
    inp = inputtxt.get() 
    lbl.config(text = "Provided Input: "+inp)

# Function to lookup folder path
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    pathLabel.config(text = "Folder Path: " + folder_path)

# TextBox Creation 
inputtxt = tk.Entry(window, 
                   width = 20) 
  
inputtxt.pack()

# Button Creation 
printButton = tk.Button(window, text = "Print",  command = printInput) 
printButton.pack() 

# Label Creation 
lbl = tk.Label(window, text = "") 
lbl.pack()

pathLabel = tk.Label(window, text = "")
pathLabel.pack()

# Create a button to browse for a folder
browse_button = tk.Button(window, text="Browse Folder", command=browse_folder)
browse_button.pack()

window.mainloop()