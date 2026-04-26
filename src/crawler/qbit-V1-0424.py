#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量子位 AI 新闻爬虫
来源：https://www.qbitai.com/
RSS: https://www.qbitai.com/feed
"""

import os
import sys
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class QbitCrawler:
    """量子位 AI 新闻爬虫"""
    
    def __init__(self):
        self.name = "量子位"
        self.url = "https://www.qbitai.com/"
        self.rss_url = "https://www.qbitai.com/feed"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml'
        }
    
    def fetch(self):
        """抓取量子位 AI 新闻"""
        print(f"📰 正在抓取量子位 AI 新闻...")
        
        try:
            response = requests.get(self.rss_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # 查找条目
            entries = soup.find_all('item')
            
            articles = []
            for entry in entries[:10]:  # 最多抓取 10 条
                try:
                    title_tag = entry.find('title')
                    link_tag = entry.find('link')
                    pub_date_tag = entry.find('pubDate')
                    description_tag = entry.find('description')
                    
                    if not title_tag or not link_tag:
                        continue
                    
                    title = title_tag.get_text().strip()
                    link = link_tag.get_text().strip()
                    # RSS 中的链接已经是完整的 URL，不需要修改
                    
                    pub_date = pub_date_tag.get_text().strip() if pub_date_tag else datetime.now().strftime('%Y-%m-%d')
                    
                    # 清理描述
                    description = description_tag.get_text().strip() if description_tag else ''
                    description = re.sub(r'<[^>]+>', '', description)[:300]
                    
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
                    continue
            
            print(f"✅ 成功抓取 {len(articles)} 条量子位 AI 新闻")
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
        stop_words = {'公司', '项目', '产品', '技术', '发展', '发布', '推出', '最新', '新闻', '文章', '量子位'}
        keywords = [w for w in chinese_words if w not in stop_words]
        return list(set(keywords))[:5]  # 去重，最多 5 个


def main():
    """主函数"""
    crawler = QbitCrawler()
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
        output_file = f"logs/qbit_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == "__main__":
    main()
