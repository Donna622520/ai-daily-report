"""
TechCrunch AI 爬虫
采集 AI 相关新闻
"""

import logging
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class TechCrunchCrawler(BaseCrawler):
    """TechCrunch AI 爬虫"""
    
    def __init__(self):
        super().__init__(
            name="TechCrunch AI",
            url="https://techcrunch.com/category/artificial-intelligence/",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
    
    def crawl(self) -> list:
        """采集 TechCrunch AI 新闻"""
        articles = []
        
        # 获取 RSS 源
        rss_url = "https://techcrunch.com/category/artificial-intelligence/feed/"
        html = self.fetch(rss_url)
        
        if not html:
            logger.warning("TechCrunch RSS 获取失败")
            return articles
        
        soup = self.parse_html(html)
        
        # 提取新闻条目
        for item in soup.find_all('item'):
            title = item.find('title')
            link = item.find('link')
            pub_date = item.find('pubDate')
            
            if title and link:
                article = {
                    'title': title.get_text(strip=True),
                    'link': link.get_text(strip=True),
                    'date': pub_date.get_text(strip=True)[:10] if pub_date else None,
                    'source': 'TechCrunch'
                }
                articles.append(article)
        
        return articles[:10]  # 最多返回 10 条
