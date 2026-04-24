"""
官方博客爬虫
采集 AI 公司的官方博客新闻
"""

import logging
from .base import BaseCrawler

logger = logging.getLogger(__name__)


class BlogCrawler(BaseCrawler):
    """官方博客爬虫"""
    
    BLOGS = [
        {
            'name': 'Anthropic',
            'url': 'https://www.anthropic.com/news',
            'keywords': ['Claude', 'AI', 'anthropic']
        },
        {
            'name': 'OpenAI',
            'url': 'https://openai.com/blog',
            'keywords': ['GPT', 'AI', 'openai']
        },
        {
            'name': '智谱',
            'url': 'https://www.zhipuai.cn/news',
            'keywords': ['智谱', 'AI', 'GLM']
        },
        {
            'name': '通义千问',
            'url': 'https://www.aliyun.com/product/qwen',
            'keywords': ['通义千问', 'AI', 'Qwen']
        }
    ]
    
    def __init__(self):
        super().__init__(
            name="BlogCrawler",
            url="",
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
    
    def crawl(self) -> list:
        """采集所有官方博客新闻"""
        articles = []
        
        for blog in self.BLOGS:
            logger.info(f"采集 {blog['name']} 博客...")
            html = self.fetch(blog['url'])
            
            if not html:
                logger.warning(f"{blog['name']} 博客获取失败")
                continue
            
            soup = self.parse_html(html)
            
            # 提取新闻列表 (根据不同网站结构调整)
            for item in soup.find_all('article')[:5]:
                title_tag = item.find('h2') or item.find('h3') or item.find('a')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link_tag = item.find('a')
                    link = link_tag.get('href', '') if link_tag else ''
                    
                    if link and not link.startswith('http'):
                        link = blog['url'] + link
                    
                    article = {
                        'title': title,
                        'link': link,
                        'date': '2026-04-24',
                        'source': blog['name']
                    }
                    articles.append(article)
        
        return articles
