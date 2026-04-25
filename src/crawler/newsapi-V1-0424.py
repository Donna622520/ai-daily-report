#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewsAPI AI 新闻爬虫（中文）
来源：NewsAPI (https://newsapi.org)
注意：需要 API Key，免费额度：100 次/天
"""

import os
import sys
import re
import json
from datetime import datetime
import requests

class NewsAPICrawler:
    """NewsAPI AI 新闻爬虫"""
    
    def __init__(self, api_key=None):
        self.name = "NewsAPI"
        self.api_key = api_key or os.getenv('NEWSAPI_KEY', 'your_api_key_here')
        self.base_url = "https://newsapi.org/v2/everything"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def fetch(self):
        """抓取新闻"""
        print(f"📰 正在抓取 NewsAPI AI 新闻...")
        
        if self.api_key == 'your_api_key_here':
            print("⚠️ 警告：未设置 NewsAPI Key，使用示例数据")
            return self._get_example_data()
        
        try:
            params = {
                'q': 'AI OR artificial intelligence OR machine learning',
                'language': 'zh',
                'sortBy': 'publishedAt',
                'pageSize': 10,
                'apiKey': self.api_key
            }
            
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != 'ok':
                print(f"❌ API 错误：{data.get('message', 'Unknown error')}")
                return []
            
            articles = []
            for item in data.get('articles', []):
                try:
                    title = item.get('title', '')
                    url = item.get('url', '')
                    pub_date = item.get('publishedAt', '')
                    description = item.get('description', '') or ''
                    source = item.get('source', {}).get('name', '')
                    
                    # 清理描述
                    description = re.sub(r'<[^>]+>', '', description)[:300]
                    
                    # 提取关键词
                    keywords = self._extract_keywords(title, description)
                    
                    article = {
                        'title': title,
                        'url': url,
                        'source': source,
                        'pub_date': pub_date,
                        'summary': description,
                        'keywords': keywords,
                        'crawl_time': datetime.now().isoformat()
                    }
                    articles.append(article)
                    
                except Exception as e:
                    print(f"⚠️ 解析条目失败：{e}")
            
            print(f"✅ 成功抓取 {len(articles)} 条 NewsAPI AI 新闻")
            return articles
            
        except Exception as e:
            print(f"❌ 抓取失败：{e}")
            return []
    
    def _get_example_data(self):
        """返回示例数据"""
        print("💡 提示：获取 NewsAPI Key: https://newsapi.org/register")
        return [
            {
                'title': '示例：AI 技术发展',
                'url': 'https://example.com/ai-news',
                'source': 'NewsAPI (示例)',
                'pub_date': datetime.now().strftime('%Y-%m-%d'),
                'summary': '这是一个示例数据，用于演示。请注册 NewsAPI 获取真实数据。',
                'keywords': ['AI', '技术', '发展'],
                'crawl_time': datetime.now().isoformat()
            }
        ]
    
    def _extract_keywords(self, title, description):
        """提取关键词"""
        text = f"{title} {description}"
        # 提取中文关键词
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,}', text)
        stop_words = {'公司', '项目', '产品', '技术', '发展', '发布', '推出', '最新', '新闻', '文章'}
        keywords = [w for w in chinese_words if w not in stop_words]
        return list(set(keywords))[:5]


def main():
    """主函数"""
    crawler = NewsAPICrawler()
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
        output_file = f"logs/newsapi_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存到：{output_file}")


if __name__ == '__main__':
    main()
