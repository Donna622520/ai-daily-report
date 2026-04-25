#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ars Technica AI 新闻爬虫
来源：https://arstechnica.com/information-technology/
RSS: https://arstechnica.com/feed/
"""

import os
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class ArstechnicaCrawler:
    """Ars Technica AI 新闻爬虫"""
    
    def __init__(self):
        self.name = "Ars Technica"
        self.url = "https://arstechnica.com/feed/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml'
        }
    
    def fetch(self):
        """抓取新闻"""
        print(f"📰 正在抓取{self.name} AI 新闻...")
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'xml')
            
            # 查找条目
            entries = soup.find_all('item')
            
            articles = []
            for entry in entries[:10]:
                try:
                    title_tag = entry.find('title')
                    link_tag = entry.find('link')
                    pub_date_tag = entry.find('pubDate')
                    description_tag = entry.find('description')
                    
                    if not title_tag or not link_tag:
                        continue
                    
                    title = title_tag.get_text().strip()
                    link = link_tag.get_text().strip()
                    pub_date = pub_date_tag.get_text().strip() if pub_date_tag else datetime.now().strftime('%Y-%m-%d')
                    
                    # 清理描述
                    description = description_tag.get_text().strip() if description_tag else ''
                    description = re.sub(r'<[^>]+>', '', description)[:300]
                    
                    # 检查是否是 AI 相关文章
                    if not self._is_ai_article(title, description):
                        continue
                    
                    # 提取关键词
                    keywords = self._extract_keywords(title, description)
                    
                    article = {
                        'title': title,
                        'url': link,
                        'source': self.name,
                        'pub_date': pub_date,
                        'summary': description,
                        'keywords': keywords,
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
    
    def _is_ai_article(self, title, description):
        """检查是否是 AI 相关文章"""
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'llm', 'gpt', 'chatgpt', 'openai', 'anthropic', 'google', 'microsoft', 'meta', 'nvidia', 'cuda', 'transformer', 'neural network', 'chatbot']
        text = f"{title} {description}".lower()
        return any(keyword in text for keyword in ai_keywords)
    
    def _extract_keywords(self, title, description):
        """提取关键词"""
        text = f"{title} {description}"
        # 提取英文关键词
        words = re.findall(r'\b\w{4,}\b', text)
        stop_words = {'article', 'news', 'story', 'report', 'latest', 'new', 'today', 'ars', 'technica'}
        keywords = [w for w in words if w.lower() not in stop_words]
        return list(set(keywords))[:5]


def main():
    """主函数"""
    crawler = ArstechnicaCrawler()
    articles = crawler.fetch()
    
    # 打印结果
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源：{article['source']}")
        print(f"   链接：{article['url']}")
        print(f"   日期：{article['pub_date']}")
        print(f"   摘要：{article['summary'][:100]}...")
        print(f"   关键词：{', '.join(article['keywords'])}")
    
    # 保存为 JSON
    if articles:
        output_file = f"logs/arstechnica_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == '__main__':
    main()
