#Extended class for BenQ scraping
#Takes in excel file and scrapes each ASIN to find company name and price
import pandas as pd
import requests
from parsel import Selector

from AmazonScraper import AmazonScraper
from bs4 import BeautifulSoup

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
    # col1 = ASIN
    # col2 = price
    # col3 = sold by
    # col4 = fulfilled by
    def searchASIN(self):
        # https://www.amazon.com/dp/
        for index, row in self.dataframe.iterrows():
            baseLink = "https://www.amazon.com/dp/" + str(self.dataframe.iat[index, 0])

            try:
                response = requests.get(baseLink, headers=self.custom_header)
                if response.status_code == 200:
                    sel = Selector(text=response.text)
                    price = "$" + sel.css('.a-price-whole ::text').get("") + "." + sel.css('.a-price-fraction ::text').get("")
                    self.dataframe.iat[index, 1] = price
                    # Try using beautiful soup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    buybox = soup.find(id='desktop_buybox')
                    buyboxSoup = BeautifulSoup(str(buybox), 'html.parser')
                    shipsFrom = buyboxSoup.find(id='shipFromSoldByAbbreviated_feature_div')
                    shipsFrom2 = buyboxSoup.find(id="sellerProfileTriggerId")

                    # Scrape for Ships from and Sold by
                    shipsFromInfo = BeautifulSoup(str(shipsFrom), 'html.parser')
                    span_elements = shipsFromInfo.find_all('span')

                    #Check if unavailable
                    availability_indicator = soup.find('span', string='Currently unavailable.')

                    shipsFromOutput = "Currently Unavailable"
                    soldByOutput = "Currently Unavailable"
                    if (shipsFrom2):
                        soldByOutput = str(shipsFrom2.text) #Sold by
                    else:
                        soldByOutput = "Sold by: Amazon"

                    if len(span_elements) == 0:
                        shipsFromOutput = "Shipped From: Amazon" #Ships from
                    else:
                        index = 0
                        while index < len(span_elements):
                            if span_elements[index].text.strip() == "Ships from:":
                                # Return this
                                shipsFrom = str(span_elements[index + 1].text)
                                shipsFromOutput = shipsFrom #Ships from
                                index = len(span_elements)
                            else:
                                index += 1
                    self.dataframe.iat[index, 2] = soldByOutput
                    self.dataframe.iat[index, 3] = shipsFromOutput
                    
            except Exception as e:
                print("Error")


    # 4. Export database to excel file
    def exportExcel(self):
        # export to excel
        excel_file_path = self.folderPath + '/output.xlsx'
        self.dataframe.to_excel(excel_file_path, index=False)