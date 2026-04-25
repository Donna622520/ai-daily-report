#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷锋网 AI 新闻爬虫
来源：https://www.leiphone.com/category/ai
"""

import os
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class LeiphoneCrawler:
    """雷锋网 AI 新闻爬虫"""
    
    def __init__(self):
        self.name = "雷锋网"
        self.url = "https://www.leiphone.com/category/ai"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.leiphone.com/'
        }
    
    def fetch(self):
        """抓取雷锋网 AI 新闻"""
        print(f"📰 正在抓取雷锋网 AI 新闻...")
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 查找新闻列表
            articles = []
            news_items = soup.select('.news-item, .article-item, .list-item')
            
            # 如果没有找到特定选择器，尝试通用选择器
            if not news_items:
                news_items = soup.select('a[href*="/news/"], a[href*="/a/"]')
            
            for item in news_items[:10]:  # 最多抓取 10 条
                try:
                    title_tag = item.select_one('h2, h3, h4, .title, .news-title')
                    if not title_tag:
                        continue
                    
                    title = title_tag.get_text(strip=True)
                    href = item.get('href', '')
                    
                    if not href or not href.startswith('/'):
                        continue
                    
                    url = 'https://www.leiphone.com' + href
                    
                    # 提取发布时间
                    date_tag = item.select_one('.date, .time, .pub-date')
                    pub_date = date_tag.get_text(strip=True) if date_tag else datetime.now().strftime('%Y-%m-%d')
                    
                    # 提取摘要
                    summary_tag = item.select_one('.summary, .desc, .abstract')
                    summary = summary_tag.get_text(strip=True) if summary_tag else ''
                    
                    # 提取关键词
                    keywords = self._extract_keywords(title, summary)
                    
                    article = {
                        'title': title,
                        'url': url,
                        'source': self.name,
                        'pub_date': pub_date,
                        'summary': summary[:300] if summary else '',
                        'keywords': keywords,
                        'crawl_time': datetime.now().isoformat()
                    }
                    articles.append(article)
                    
                except Exception as e:
                    print(f"⚠️ 解析条目失败：{e}")
                    continue
            
            print(f"✅ 成功抓取 {len(articles)} 条雷锋网 AI 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取失败：{e}")
            return []
    
    def _extract_keywords(self, title, description):
        """提取关键词"""
        text = f"{title} {description}"
        # 提取中文关键词
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        # 过滤常见词
        stop_words = {'公司', '项目', '产品', '技术', '发展', '发布', '推出', '最新', '新闻'}
        keywords = [w for w in chinese_words if w not in stop_words]
        return list(set(keywords))[:5]  # 去重，最多 5 个


def main():
    """主函数"""
    crawler = LeiphoneCrawler()
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
        output_file = f"logs/leiphone_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == "__main__":
    main()
