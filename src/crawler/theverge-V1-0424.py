#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Verge AI 新闻爬虫
来源：https://www.theverge.com/ai
RSS: https://www.theverge.com/rss/ai/index.xml
"""

import os
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class TheVergeCrawler:
    """The Verge AI 新闻爬虫"""
    
    def __init__(self):
        self.name = "The Verge"
        self.url = "https://www.theverge.com/ai"
        self.rss_url = "https://www.theverge.com/rss/ai/index.xml"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch(self):
        """抓取 The Verge AI 新闻"""
        print(f"📰 正在抓取 The Verge AI 新闻...")
        
        try:
            # 使用 RSS 抓取
            response = requests.get(self.rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            articles = []
            for item in items:
                try:
                    title = item.find('title').get_text().strip()
                    link = item.find('link').get_text().strip()
                    pub_date = item.find('pubDate').get_text().strip()
                    description = item.find('description').get_text().strip()
                    
                    # 提取关键词
                    keywords = self._extract_keywords(title, description)
                    
                    article = {
                        'title': title,
                        'url': link,
                        'source': self.name,
                        'pub_date': pub_date,
                        'summary': self._clean_description(description),
                        'keywords': keywords,
                        'crawl_time': datetime.now().isoformat()
                    }
                    articles.append(article)
                    
                except Exception as e:
                    print(f"⚠️ 解析条目失败：{e}")
                    continue
            
            print(f"✅ 成功抓取 {len(articles)} 条 The Verge AI 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取失败：{e}")
            return []
    
    def _extract_keywords(self, title, description):
        """提取关键词"""
        # 简单的关键词提取逻辑
        text = f"{title} {description}"
        # 提取英文单词（AI 相关）
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        # 过滤常见词
        stop_words = {'The', 'And', 'For', 'With', 'From', 'This', 'That', 'New', 'AI'}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords[:5]  # 最多 5 个关键词
    
    def _clean_description(self, description):
        """清理描述文本"""
        # 移除 HTML 标签
        description = re.sub(r'<[^>]+>', '', description)
        # 移除多余空白
        description = re.sub(r'\s+', ' ', description).strip()
        # 限制长度
        if len(description) > 300:
            description = description[:300] + "..."
        return description


def main():
    """主函数"""
    crawler = TheVergeCrawler()
    articles = crawler.fetch()
    
    # 打印结果
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源：{article['source']}")
        print(f"   链接：{article['url']}")
        print(f"   摘要：{article['summary'][:100]}...")
        print(f"   关键词：{', '.join(article['keywords'])}")
    
    # 保存为 JSON
    if articles:
        output_file = f"logs/theverge_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == "__main__":
    main()
