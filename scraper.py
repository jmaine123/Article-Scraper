from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from lxml import etree, html
from dataclasses import dataclass, asdict
import time
import json

import requests
import re
import pandas as pd

all_articles = []


class Scraper():
    def __init__(self, url) -> None:
        self.url = url

    def get_page(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        print(driver.title)
        driver.find_element(By.XPATH,'//div[@data-hierarchy="zone"]')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        s = soup.prettify()
        return soup
    
    def get_article(self, soup):
        dom = etree.HTML(str(soup))
        # print(dom)
        sections = dom.xpath('//descendant::section[@class="story-wrapper"]')

        for idx, section in enumerate(sections):
            article = {}
            tree = html.tostring(section)
            row = etree.HTML(tree)
            try:
                url = row.xpath('//a/@href')[0].replace("\/", "/")
            except:
                url = "N/A"
            
            try:
                title = row.xpath('//descendant::h3/text()')[0]
            except:
                title = "N/A"
            
            try:
                summary = row.xpath('/descendant::*[contains(@class,"summary-class")]/text()')[0]
            except:
                summary = "N/A"

            article['Article Number'] = str(idx + 1)
            article["Article Title"] = title
            article["Summary"] = summary
            article["URL"] = url

            all_articles.append(article)
            
            

ny_url = 'https://www.nytimes.com'
nytimes = Scraper(ny_url)
page = nytimes.get_page()
nytimes.get_article(page)

df = pd.DataFrame(all_articles)
results = df.to_json("articles.json",orient="records")
# parsed = json.loads(results)
# final = json.dumps(parsed, indent=4)
print(df.head())

# if __name__ == 'main':
#     main()
