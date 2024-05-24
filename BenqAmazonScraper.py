#Extended class for BenQ scraping
#Takes in excel file and scrapes each ASIN to find company name and price
import pandas as pd
import requests
from parsel import Selector

from AmazonScraper import AmazonScraper
from bs4 import BeautifulSoup
import re

import time
import random
from datetime import datetime

class BenqAmazonScraper(AmazonScraper):
    filePath: str
    dataframe: pd

    # Use the methods in linear order

    # 1. Method to set file name of import excel file to search
    def setFileName(self, filePath):
        self.filePath = filePath
        self.readFile()
    
    # 2. Method to read excel file to data frame
    # Make sure in external program to call setfilePath first
    def readFile(self):
        self.dataframe = pd.read_excel(self.filePath, usecols=[0])
        self.dataframe['Price'] = ''
        self.dataframe['SKU'] = ''
        self.dataframe['Sold By'] = ''
        self.dataframe['Ships From'] = ''
    
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
            # wait before accessing page
            self.wait()
            try:
                response = requests.get(baseLink, headers=self.custom_header)
                if response.status_code == 200:
                    sel = Selector(text=response.text)
                    price = "$" + sel.css('.a-price-whole ::text').get("") + "." + sel.css('.a-price-fraction ::text').get("")
                    self.dataframe.iat[index, 2] = str(price)
                    # Try using beautiful soup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    buybox = soup.find(id='desktop_buybox')
                    buyboxSoup = BeautifulSoup(str(buybox), 'html.parser')
                    shipsFrom = buyboxSoup.find(id='shipFromSoldByAbbreviated_feature_div')
                    shipsFrom2 = buyboxSoup.find(id="sellerProfileTriggerId")

                    # Scrape SKU
                    name = sel.css("#productTitle::text").get("").strip()
                    SKU = self.SKUSearch(name)

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
                        soldByOutput = "Unavailable"

                    if len(span_elements) == 0:
                        shipsFromOutput = soldByOutput #Ships from
                    else:
                        indexy = 0
                        while indexy < len(span_elements) - 1:
                            if span_elements[indexy].text.strip() == "Ships from:":
                                # Return this
                                shipsFrom = str(span_elements[indexy + 1].text)
                                shipsFromOutput = str(shipsFrom) #Ships from
                                indexy = len(span_elements)
                            else:
                                indexy += 1
                    
                    # Case for when Sold By is Unavailable and Ships From is not
                    if shipsFromOutput != "Unavailable" and soldByOutput == "Unavailable":
                        soldByOutput = shipsFromOutput
                    self.dataframe.iat[index, 1] = str(SKU)
                    self.dataframe.iat[index, 3] = str(soldByOutput)
                    self.dataframe.iat[index, 4] = str(shipsFromOutput)
        
            except Exception as e:
                print(e)
        self.exportExcel()
    
    def wait(self):
        wait_time = random.uniform(0.5, 1.0)  # Generate a random float between 0.5 and 1
        interval = 0.1  # Interval of 0.1 seconds

        while wait_time > 0:
            # Sleep for the interval
            time.sleep(interval)
            wait_time -= interval
    
    # Regex expression to search for SKU in title
    def SKUSearch(self, text):
        pattern = r'[A-Z]+[0-9]+[A-Z0-9]*\b'
        SKUString = re.search(pattern, text)
        if SKUString:
            return SKUString.group()
        else:
            return None


    # 4. Export database to excel file
    # change name of output to date
    def exportExcel(self):
        # export to excel
        current_time = datetime.now()
        excel_file_path = self.folderPath + '/output_' + current_time.strftime("%Y_%j_%H_%M") + '.xlsx'
        self.dataframe.to_excel(excel_file_path, index=False)