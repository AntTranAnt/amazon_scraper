# Class that searches Amazon pages with inputed word
# Export to Excel File

# Scraping dependencies
import requests
from parsel import Selector
from urllib.parse import urljoin

# Backend dependencies
import time
import random
import pandas as pd

class AmazonScraper:
    # Class to represent AmazonProduct item. Holds basic item descriptors.
    class AmazonProduct:
        # private class variables
        asin: int
        name: str
        productUrl: str
        relativeUrl: str
        sale_price: float
        real_price: float
        logo: str

        def __init__(self, asin=0, name="", productUrl="", relativeUrl="", sale_price=0, real_price=0, logo="None"):
            self.asin = asin
            self.name = name
            self.productUrl = productUrl
            self.relativeUrl = relativeUrl
            self.sale_price = sale_price
            self.real_price = real_price
            self.logo = logo

        # Returns object in dictionary form
        def to_dict(self):
            return {
                'Asin': self.asin,
                'Product Name': self.name,
                'Product Url': self.productUrl,
                'Relative Url': self.relativeUrl,
                'Sales Price': self.sale_price,
                'Real Price': self.real_price,
                'Company': self.logo
            }

    # Private class variables
    folderPath: str

    # custom header
    custom_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'accept-language': 'en-GB,en;q=0.9'
    }

    # Array to hold AmazonProduct
    product_overview = []

    # Method to scrape Amazon search pages for keyword and number of pages
    def search(self, keyword, pages):
        self.product_overview.clear()

        url_list = [f'https://www.amazon.com/s?k={keyword}&page=1']
        pages_scanned = 0

        for url in url_list:
            # wait before accessing page
            time.sleep(random.randint(2, 4)) 
            try:
                response = requests.get(url, headers=self.custom_header)
                if response.status_code == 200:
                    pages_scanned += 1
                    sel =  Selector(text=response.text)
                    print("Page: " + str(pages_scanned))

                    ## Extract Product Page URLs
                    search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")

                    # Searches for basic amazon product data
                    for product in search_products:
                        relative_url = product.css("h2>a::attr(href)").get()
                        product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                        asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
                        sale_price = product.css(".a-price[data-a-size=xl] .a-offscreen::text").get()
                        real_price = product.css(".a-price[data-a-size=b] .a-offscreen::text").get()
                        name = product.css("h2>a>span::text").get()
                        logo = product.css("h2>span::text").get()
                        if real_price == None:
                            real_price = sale_price

                        productObject = self.AmazonProduct(asin, name, product_url, relative_url, sale_price, real_price, logo)

                        # appends product data for each product into object
                        self.product_overview.append(productObject)
                    
                    # Gets all pages from page 1 to pages
                    if "&page=1" in url:
                        for i in range(2, pages + 1):
                            new_page_url = f'https://www.amazon.com/s?k={keyword}&page={i}'
                            url_list.append(new_page_url)

            except Exception as e:
                print("Error", e)
        
        self.exportExcel()

    # Method to export to excel sheet
    # Should only be called from search method to prevent wrong dataframe from being exported
    def exportExcel(self):
        # create dataframe from list of objects
        df = pd.DataFrame([product.to_dict() for product in self.product_overview])

        # export to excel
        excel_file_path = self.folderPath + '/output.xlsx'
        df.to_excel(excel_file_path, index=False)
    
    # Changes folderPath
    def setFolderPath(self, folderPath):
        self.folderPath = folderPath