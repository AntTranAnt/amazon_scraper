#Extended class for BenQ scraping
#Takes in excel file and scrapes each ASIN to find company name and price

from AmazonScraper import AmazonScraper

class BenqAmazonScraper(AmazonScraper):
    fileName: str

    # Method to set file name of import excel file to search
    def setFileName(self, fileName):
        self.fileName = fileName