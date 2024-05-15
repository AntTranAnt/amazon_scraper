import tkinter as tk
from tkinter import filedialog
from BenqAmazonScraper import BenqAmazonScraper
import time

amazonScraper = BenqAmazonScraper()

# Top level window 
window = tk.Tk() 
window.title("BenQ Amazon Webscraper") 

# Create a BooleanVar to track button state
browse_state = tk.BooleanVar()
file_state = tk.BooleanVar()

# Function to lookup folder path
def browse_folder():
    folder_path = filedialog.askdirectory()  # Open a folder selection dialog
    pathFolderLabel.config(text = "Folder Path: " + folder_path, fg = "black")
    amazonScraper.setFolderPath(folder_path)
    browse_state.set(True)

#Function to look for input file
def browse_file():
    file_path = filedialog.askopenfilename()
    pathFileLabel.config(text = "File Name: " + file_path, fg = "black")
    amazonScraper.setFileName(file_path)
    file_state.set(True)

#Function to scrape
def scrape():
    if browse_state.get() and file_state.get():
        window.after(0, lambda: scrape_button.config(text="Loading", state="disabled"))
        scrape2()
    else:
        loadingMsg.config(text="Pick a File and Folder before Scraping", fg="red")


def scrape2():
    amazonScraper.searchASIN()
    window.after(0, lambda: scrape_button.config(text="Finished", state="normal"))
    loadingMsg.config(text="", fg="green")

#Create Label Discription for application
appLabel = tk.Label(window, text="Application to scrape Amazon for Price, Seller Data, and Shipping Data from ASIN")
appLabel.grid(row=0, column=0, columnspan=2, padx=10)
appLabel2 = tk.Label(window, text="Steps:")
appLabel2.grid(row=1, column=0, columnspan=2, padx=10)
appLabel3 = tk.Label(window, text="1) Select a .xlsx file to scrape information")
appLabel3.grid(row=2, column=0, columnspan=2, padx=10)
appLabel4 = tk.Label(window, text="2) Select a folder to download the results to")
appLabel4.grid(row=3, column=0, columnspan=2, padx=10)
appLabel5 = tk.Label(window, text="3) Press the Start Button to start scraping")
appLabel5.grid(row=4, column=0, columnspan=2, padx=10)
appLabel6 = tk.Label(window, text="**IMPORTANT**", fg="red")
appLabel6.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 0))
appLabel7 = tk.Label(window, text="WAIT A COUPLE MINUTES BEFORE EACH SCRAPE.", fg="red")
appLabel7.grid(row=6, column=0, columnspan=2, padx=10)
appLabel8 = tk.Label(window, text="AMAZON HAS LIMITS FOR HOW MANY TIMES A PERSON A SCRAPE FOR INFORMATION WITHIN A SHORT TIME", padx=10, fg="red")
appLabel8.grid(row=7, column=0, columnspan=2, padx=10, pady=(1, 5))

#Create button to browse for file
browse_file_button = tk.Button(window, text="Browse File", command = browse_file)
browse_file_button.grid(row=8, column=0, pady=5)

pathFileLabel = tk.Label(window, text = "", bg="gray")
pathFileLabel.grid(row=8, column=1)

# Create a button to browse for a folder
browse_button = tk.Button(window, text="Browse Folder", command = browse_folder)
browse_button.grid(row=9, column=0, pady=5, padx=10)

pathFolderLabel = tk.Label(window, text = "", bg="gray")
pathFolderLabel.grid(row=9, column=1)

#Create a button to start scrape
scrape_button = tk.Button(window, text = "Start", command=scrape)
scrape_button.grid(row=10, column=0, columnspan=2, pady=(1, 5))

loadingMsg = tk.Label(window, text="")
loadingMsg.grid(row=11, column=0, columnspan=2)

window.mainloop()