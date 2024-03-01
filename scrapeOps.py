import requests
from parsel import Selector
from urllib.parse import urljoin

# Code
# https://scrapeops.io/web-scraping-playbook/how-to-scrape-amazon/
# https://oxylabs.io/blog/how-to-scrape-amazon-product-data

custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9'
}

product_urls = []
product_asins = []
product_overview = []
keyword = 'benq'

url = f'https://www.amazon.com/s?k={keyword}&page=1'

try:
    response = requests.get(url, headers=custom_header)
    if response.status_code == 200:
        sel =  Selector(text=response.text)

        ## Extract Product Page URLs
        search_products = sel.css("div.s-result-item[data-component-type=s-search-result]")
        for product in search_products:
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            product_urls.append(product_url) 
            asin = relative_url.split('/')[3] if len(relative_url.split('/')) >= 4 else None
            product_asins.append(asin)
except Exception as e:
    print("Error", e)

print(product_urls)
print(product_asins)
            