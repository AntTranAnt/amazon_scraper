from BenqAmazonScraper import BenqAmazonScraper

benqScraper = BenqAmazonScraper()
benqScraper.setFileName("test.xlsx")
benqScraper.readFile()
benqScraper.searchASIN()
print(benqScraper.dataframe)