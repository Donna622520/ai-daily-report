#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = "https://www.theverge.com/rss/ai/index.xml"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")
print(f"Content (first 500 chars):")
print(response.text[:500])
