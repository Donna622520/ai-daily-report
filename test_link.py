#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = "https://www.qbitai.com/feed"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'xml')

# 查看第一个条目的 link
entry = soup.find('item')
if entry:
    link_tag = entry.find('link')
    print(f"link_tag: {link_tag}")
    print(f"link_tag.get_text(): '{link_tag.get_text()}'")
    print(f"link_tag.string: {link_tag.string}")
    print(f"link_tag.text: {link_tag.text}")
