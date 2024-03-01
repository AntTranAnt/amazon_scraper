import requests
from bs4 import BeautifulSoup

custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9'
}

product_urls = []
keyword = 'benq'

url = f'https://www.amazon.com/s?k={keyword}&page=1'

url2 = 'https://www.amazon.com/dp/B0BTTVM832'

response = requests.get(url, headers=custom_header)
print(response.status_code)
# soup = BeautifulSoup(response.text, 'lxml')

# product_title_element = soup.select_one('#productTitle')
# product_title = product_title_element.text.strip()

# print(product_title)