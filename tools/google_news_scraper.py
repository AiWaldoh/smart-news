from bs4 import BeautifulSoup
from tools.base_scraper import BaseScraper
from lxml import html
import requests

class GoogleNewsScraper(BaseScraper):
    def __init__(self):
        self.base_url = "https://www.google.com/search"

    def search(self, query, limit=10):
        self.full_url = f"{self.base_url}?q={query.replace(' ', '+')}&tbs=sbd:1,nsd:1&tbm=nws&source=lnt&bih=1144&dpr=1"

        html = self.execute_curl(self.full_url)
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        for article_div in soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe"):
            article_info = self.extract_article_info(article_div)
            if article_info:
                articles.append(article_info)
        return articles
    

    def extract_article_info(self, article_div):
        print("----------------------")
        print(article_div)
        html_content = article_div

        # Parse the HTML content with lxml
        tree = html.fromstring(str(html_content))

        # Simplified XPath to extract the complete URLs
        link = tree.xpath('//div[contains(@class, "Gx5Zad")]/a/@href')

        # Extract other elements
        description = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe s3v9rd AP7Wnd"]/div/div/text()')[0]
        date_text = tree.xpath('//div[contains(@class, "Gx5Zad")]//span[@class="r0bn4c rQMQod"]/text()')[0]
        source_text = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe UPmit AP7Wnd lRVwie"]/text()')[0]
        image_link = tree.xpath('//div[contains(@class, "Gx5Zad")]//img/@src')[0]
        title = tree.xpath('//div[contains(@class, "Gx5Zad")]//div[@class="BNeawe vvjwJb AP7Wnd UwRFLe"]/text()')[0]


        return {
            "title": title,
            "description": description,
            "link": link,
            "source": source_text,
            "date": date_text,
            "image_link": image_link,
        }