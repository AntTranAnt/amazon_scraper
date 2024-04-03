#Extended class for BenQ scraping
#Takes in excel file and scrapes each ASIN to find company name and price
import pandas as pd
import requests
from parsel import Selector

from AmazonScraper import AmazonScraper

class BenqAmazonScraper(AmazonScraper):
    filePath: str
    dataframe: pd

    # Use the methods in linear order

    # 1. Method to set file name of import excel file to search
    def setFileName(self, filePath):
        self.filePath = filePath
    
    # 2. Method to read excel file to data frame
    # Make sure in external program to call setfilePath first
    def readFile(self):
        self.dataframe = pd.read_excel(self.filePath)
    
    # 3. Method to search each ASIN for company name and price
    # Adds to dataframe property
    def searchASIN(self):
        # https://www.amazon.com/dp/
        for index, row in self.dataframe.iterrows():
            baseLink = "https://www.amazon.com/dp/" + str(self.dataframe.iat[index, 0])

            try:
                response = requests.get(baseLink, self.custom_header)
                if response.status_code == 200:
                    sel = Selector(text=response.text)
                    price = sel.css('.a-price span[aria-hidden="true"] ::text').get("")
                    if not price:
                        price = sel.css('.a-price .a-offscreen ::text').get("")
            except Exception as e:
                print("Error")


    # 4. Export database to excel file
    # def exportExcel(self):
        # do i call exportExcel from superclass?