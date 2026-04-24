"""
基础爬虫类
提供通用的爬虫功能和配置
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseCrawler:
    """基础爬虫类"""
    
    def __init__(self, name: str, url: str, headers: dict = None):
        self.name = name
        self.url = url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch(self, url: str = None) -> str:
        """获取网页内容"""
        target_url = url or self.url
        try:
            response = requests.get(target_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"获取 {target_url} 失败: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """解析 HTML"""
        if not html:
            return None
        return BeautifulSoup(html, 'lxml')
    
    def extract_date(self, soup: BeautifulSoup) -> str:
        """提取日期 (YYYY-MM-DD 格式)"""
        # 尝试从 meta 标签提取
        meta_date = soup.find('meta', property='article:published_time')
        if meta_date:
            return meta_date.get('content', '')[:10]
        
        # 尝试从 time 标签提取
        time_tag = soup.find('time')
        if time_tag:
            return time_tag.get('datetime', '')[:10]
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        title_tag = soup.find('title') or soup.find('h1')
        if title_tag:
            return title_tag.get_text(strip=True)
        return ""
    
    def extract_link(self, soup: BeautifulSoup) -> str:
        """提取链接"""
        link_tag = soup.find('a')
        if link_tag:
            href = link_tag.get('href', '')
            return href if href.startswith('http') else self.url + href
        return ""
    
    def crawl(self) -> list:
        """爬虫主方法，子类需要实现"""
        raise NotImplementedError
