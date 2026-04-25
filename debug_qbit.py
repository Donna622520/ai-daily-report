#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

url = "https://www.qbitai.com/feed"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'xml')
entries = soup.find_all('item')

for i, entry in enumerate(entries[:1]):
    title_tag = entry.find('title')
    link_tag = entry.find('link')
    pub_date_tag = entry.find('pubDate')
    description_tag = entry.find('description')
    
    print(f"title_tag: {title_tag}")
    print(f"link_tag: {link_tag}")
    print(f"title: {title_tag.get_text().strip() if title_tag else None}")
    print(f"link: {link_tag.get_text().strip() if link_tag else None}")
    print(f"pub_date: {pub_date_tag.get_text().strip() if pub_date_tag else None}")
    print(f"description: {description_tag.get_text().strip() if description_tag else None}")
