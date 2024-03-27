#Extended class for BenQ scraping
#Takes in excel file and scrapes each ASIN to find company name and price
import pandas as pd

from AmazonScraper import AmazonScraper

class BenqAmazonScraper(AmazonScraper):
    fileName: str
    dataframe: pd

    # Use the methods in linear order

    # 1. Method to set file name of import excel file to search
    def setFileName(self, fileName):
        self.fileName = fileName
    
    # 2. Method to read excel file to data frame
    # Make sure in external program to call setFileName first
    def readFile(self):
        self.dataframe = pd.read_excel(self.fileName)
    
    # 3. Method to search each ASIN for company name and price
    # Adds to dataframe property
    def searchASIN(self):
        # https://www.amazon.com/dp/
        baseLink = "https://www.amazon/dp/"

    # 4. Export database to excel file
    def exportExcel(self):
        # do i call exportExcel from superclass?