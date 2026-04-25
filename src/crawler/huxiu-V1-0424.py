#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虎嗅 AI 新闻爬虫
来源：https://www.huxiu.com/channel/ai.html
"""

import os
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class HuxiuCrawler:
    """虎嗅 AI 新闻爬虫"""
    
    def __init__(self):
        self.name = "虎嗅"
        self.url = "https://www.huxiu.com/channel/ai.html"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.huxiu.com/'
        }
    
    def fetch(self):
        """抓取新闻"""
        print(f"📰 正在抓取{self.name} AI 新闻...")
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找新闻条目
            articles = []
            items = soup.select('li.news-item')
            
            for item in items[:10]:
                try:
                    title_tag = item.select_one('h3 a')
                    link_tag = item.select_one('h3 a')
                    date_tag = item.select_one('.date')
                    
                    if not title_tag or not link_tag:
                        continue
                    
                    title = title_tag.get_text().strip()
                    link = link_tag['href']
                    
                    # 确保链接是完整的 URL
                    if link.startswith('/'):
                        link = 'https://www.huxiu.com' + link
                    
                    pub_date = date_tag.get_text().strip() if date_tag else datetime.now().strftime('%Y-%m-%d')
                    
                    article = {
                        'title': title,
                        'url': link,
                        'source': self.name,
                        'pub_date': pub_date,
                        'summary': '',
                        'keywords': [],
                        'crawl_time': datetime.now().isoformat()
                    }
                    articles.append(article)
                    
                except Exception as e:
                    print(f"⚠️ 解析条目失败：{e}")
            
            print(f"✅ 成功抓取 {len(articles)} 条{self.name} AI 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取失败：{e}")
            return []
    
    def _extract_keywords(self, title, description):
        """提取关键词"""
        text = f"{title} {description}"
        chinese_words = re.findall(r'[\u4e00-\\u9fa5]{2,}', text)
        stop_words = {'公司', '项目', '产品', '技术', '发展', '发布', '推出', '最新', '新闻', '文章', '虎嗅'}
        keywords = [w for w in chinese_words if w not in stop_words]
        return list(set(keywords))[:5]


def main():
    """主函数"""
    crawler = HuxiuCrawler()
    articles = crawler.fetch()
    
    # 打印结果
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源：{article['source']}")
        print(f"   链接：{article['url']}")
        print(f"   日期：{article['pub_date']}")
    
    # 保存为 JSON
    if articles:
        output_file = f"logs/huxiu_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == '__main__':
    main()
