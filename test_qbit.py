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
    link = entry.find('link')
    print(f"Link tag: {link}")
    print(f"Link text: {link.get_text() if link else 'None'}")
    
    # 查看所有可用的标签
    print("\n所有可用标签:")
    for tag in entry.find_all():
        print(f"  {tag.name}: {tag.get_text()[:50]}")
