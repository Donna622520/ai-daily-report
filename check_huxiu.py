#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = "https://www.huxiu.com/channel/ai.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.huxiu.com/'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

# 查找所有 li 标签
items = soup.find_all('li')
print(f"找到 {len(items)} 个 li 标签")

# 查找包含 'news-item' 的 li
news_items = [item for item in items if 'news-item' in item.get('class', [])]
print(f"找到 {len(news_items)} 个 news-item")

# 打印前 3 个
for i, item in enumerate(news_items[:3]):
    print(f"\n{i+1}. {item}")
