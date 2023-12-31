from bs4 import BeautifulSoup
from tools.base_scraper import BaseScraper
from lxml import html
import os
import json
import time
import re
import urllib.parse

class GoogleNewsScraper(BaseScraper):
    def __init__(self, base_url):
        self.base_url = base_url
        self.cache_dir = '/tmp/cache'  # Directory to store cache files
        self.cache_duration = 600  # Cache duration in seconds (10 minutes)
        os.makedirs(self.cache_dir, exist_ok=True)  # Create cache directory if it doesn't exist
    
    async def search_many(self, query, pages=5):
        all_articles = []
        for i in range(pages):
            start = i * 10  # Each page has 10 results, so start is incremented by 10 for each page
            articles = await self.search(query, start=start)
            all_articles.extend(articles)
        return all_articles
    
    async def search(self, query, limit=1, start=0):
        # print(start)
        cache_key = f"{query}-{start}"
        cache_file_path = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        # Check if the cache file exists
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if the cache is still valid
            if time.time() - cache_data['timestamp'] < self.cache_duration:
                print("Returning cached articles")
                return cache_data['articles']  # Return the cached articles if they are still valid
        
        # Construct the full URL for the search query
        # full_url = f"{self.base_url}?q={query.replace(' ', '+')}&tbs=sbd:1,nsd:1&tbm=nws&source=lnt&bih=1144&dpr=1"
        full_url = f"{self.base_url}?q={query.replace(' ', '+')}&start={start}&tbs=sbd:1,nsd:1&tbm=nws&source=lnt&bih=1144&dpr=1"
        # print(full_url)
        # Execute curl and fetch the HTML
        html = await self.execute_curl(full_url)
        if not html:
            return []
        
        # Parse the HTML and extract articles
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        for article_div in soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe"):
            article_info = self.extract_article_info(article_div)
            if article_info:
                articles.append(article_info)
        
        # Cache the fetched articles along with the current timestamp
        with open(cache_file_path, 'w') as f:
            json.dump({'timestamp': time.time(), 'articles': articles}, f)
        
        return articles

    def extract_article_info(self, article_div):
        # print("----------------------")
        # print(article_div)
        html_content = article_div

        # Parse the HTML content with lxml
        tree = html.fromstring(str(html_content))

        # Simplified XPath to extract the complete URLs
        link = tree.xpath('//div[contains(@class, "Gx5Zad")]/a/@href')
        if link:
            match = re.search(r'/url\?q=([^&]*)', link[0])  # assuming link is a list with the URL as its first element
            if match:
                link = urllib.parse.unquote(match.group(1))
        # Extract other elements
        description = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe s3v9rd AP7Wnd"]/div/div/text()')[0]
        date_text = tree.xpath('//div[contains(@class, "Gx5Zad")]//span[@class="r0bn4c rQMQod"]/text()')[0]
        source_text = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe UPmit AP7Wnd lRVwie"]/text()')[0]
        try:
        
            image_link = tree.xpath('//div[contains(@class, "Gx5Zad")]//img/@src')[0]
        
        except:
            image_link = None
        
        title = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe vvjwJb AP7Wnd UwRFLe"]/text()')[0]


        return {
            "title": title,
            "description": description,
            "link": link,
            "source": source_text,
            "date": date_text,
            "image_link": image_link,
        }