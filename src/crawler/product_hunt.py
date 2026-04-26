"""
Product Hunt 爬虫
采集 AI 相关产品发布
"""

import logging
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class ProductHuntCrawler(BaseCrawler):
    """Product Hunt 爬虫"""
    
    def __init__(self):
        super().__init__(
            name="Product Hunt",
            url="https://www.producthunt.com/",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        self.api_url = "https://api.producthunt.com/v2/"
    
    def crawl(self) -> list:
        """采集 Product Hunt 上的 AI 产品"""
        articles = []
        
        # 尝试使用 RSS 源
        rss_url = "https://www.producthunt.com/feed"
        html = self.fetch(rss_url)
        
        if not html:
            logger.warning("Product Hunt RSS 获取失败")
            return articles
        
        soup = self.parse_html(html)
        
        # 提取 AI 相关条目
        for item in soup.find_all('item'):
            title = item.find('title')
            if title and 'AI' in title.get_text():
                link = item.find('link')
                pub_date = item.find('pubDate')
                
                if title and link:
                    article = {
                        'title': title.get_text(strip=True),
                        'link': link.get_text(strip=True),
                        'date': pub_date.get_text(strip=True)[:10] if pub_date else None,
                        'source': 'Product Hunt'
                    }
                    articles.append(article)
        
        return articles[:10]  # 最多返回 10 条
