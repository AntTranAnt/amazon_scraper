import requests
from parsel import Selector
from urllib.parse import urljoin
import time
import random

# notes
# if doesn't have BENQ title, not from BenQ

# Code
# https://scrapeops.io/web-scraping-playbook/how-to-scrape-amazon/
# https://oxylabs.io/blog/how-to-scrape-amazon-product-data

# custom header
custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9'
}

# Array to hold product data
product_overview = []

# keyword for amazon search
keyword = 'benq'

url_list = [f'https://www.amazon.com/s?k={keyword}&page=1']
pages_scanned = 0

for url in url_list:
    # wait before accessing page
    time.sleep(random.randint(2, 5)) 
    try:
        response = requests.get(url, headers=custom_header)
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

                # appends product data for each product into object
                product_overview.append(
                    {
                        "asin": asin,
                        "name": name,
                        "url": product_url,
                        "sale_price": sale_price,
                        "real_price": real_price,
                        "logo": logo
                    }
                )
            
            # Gets all pages from page 1 to pages
            if "&page=1" in url:
                pages = 5
                for i in range(2, pages + 1):
                    new_page_url = f'https://www.amazon.com/s?k={keyword}&page={i}'
                    url_list.append(new_page_url)

            # if want available pages from page 1
            # if "&page=1" in url:
            #     available_pages = sel.xpath(
            #             '//a[has-class("s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            #         ).getall()
            #     for page in available_pages:
            #             search_url_paginated = f'https://www.amazon.com/s?k={keyword}&page={page}'
            #             url_list.append(search_url_paginated)
    except Exception as e:
        print("Error", e)

print(pages_scanned)
for product in product_overview:
    print(product)
            