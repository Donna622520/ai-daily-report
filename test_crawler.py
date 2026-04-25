#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = "https://www.leiphone.com/category/ai"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'lxml')

# 查找新闻链接
news_links = soup.select('a[href*="/a/"]')
print(f"找到 {len(news_links)} 条新闻链接")

for i, link in enumerate(news_links[:5], 1):
    title = link.get_text(strip=True)
    href = link.get('href', '')
    print(f"{i}. {title[:50]} -> {href}")
