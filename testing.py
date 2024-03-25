import tkinter as tk
from tkinter import filedialog
from AmazonScraper import AmazonScraper

# Program for BenQ Corp
# Asks for Excel Input of ASIN values
# Returns excel file with price and company name
#

# To do
# modify custom header to mimic user better

# Create scraper object
amazonScraper = AmazonScraper()
  
# Top level window 
window = tk.Tk() 
window.title("TextBox Input") 

# Create a BooleanVar to track button state
browse_state = tk.BooleanVar()
file_state = tk.BooleanVar()

# Function to get input
def getInput(): 
    if (browse_state.get()): 
        inp = inputtxt.get() 
        lbl.config(text = "Searching: " + inp, fg="black")
        amazonScraper.search(input, 3)
        lbl.config(text = "File Exported", fg="green")
    else:
        pathLabel.config(text = "Pick Folder Path", fg = "red")

# Function to lookup folder path
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    pathLabel.config(text = "Folder Path: " + folder_path, fg = "black")
    amazonScraper.setFolderPath(folder_path)
    browse_state.set(True)

#Function to look for input file
def browse_file():
    file_path = filedialog.askopenfilename()
    fileName.config(text = "File Name: " + file_path, fg = "black")
    amazonScraper.setFileName(fileName)
    file_state.set(True)


# TextBox Creation 
inputtxt = tk.Entry(window, width = 60) 
inputtxt.grid(row=0, column=0, pady=5)

# Create a button to browse for a folder
browse_button = tk.Button(window, text="Browse Folder", command = browse_folder)
browse_button.grid(row=0, column=1, pady=5)

pathLabel = tk.Label(window, text = "")
pathLabel.grid(row=1, column=0, columnspan=2)

# Button Creation 
printButton = tk.Button(window, text = "Search",  command = getInput) 
printButton.grid(row=2, column=0, columnspan=2)

# Label Creation 
lbl = tk.Label(window, text = "") 
lbl.grid(row=3, column=0)


window.mainloop()