"""
GitHub 爬虫
采集 AI 相关热门项目
"""

import logging
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class GitHubCrawler(BaseCrawler):
    """GitHub 爬虫"""
    
    def __init__(self):
        super().__init__(
            name="GitHub",
            url="https://github.com/trending",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
    
    def crawl(self) -> list:
        """采集 GitHub 上的 AI 热门项目"""
        articles = []
        
        # 获取 trending 页面
        html = self.fetch(self.url)
        
        if not html:
            logger.warning("GitHub trending 获取失败")
            return articles
        
        soup = self.parse_html(html)
        
        # 提取项目列表
        for article in soup.find_all('article', class_='Box'):
            title_tag = article.find('h2', class_='f3')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link_tag = title_tag.find('a')
                link = link_tag.get('href', '') if link_tag else ''
                
                if link and not link.startswith('http'):
                    link = 'https://github.com' + link
                
                # 提取 stars 数量
                stars_tag = article.find('span', class_='text-emphasized')
                stars = stars_tag.get_text(strip=True) if stars_tag else '0'
                
                article_data = {
                    'title': title,
                    'link': link,
                    'stars': stars,
                    'date': '2026-04-24',
                    'source': 'GitHub'
                }
                articles.append(article_data)
        
        return articles[:10]  # 最多返回 10 条
