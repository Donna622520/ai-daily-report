#!/usr/bin/env python3
import requests

url = "https://www.qbitai.com/feed"
response = requests.get(url, timeout=10)
print("Response status:", response.status_code)
print("Response content (first 1000 chars):")
print(response.text[:1000])
