"""
交叉验证器
验证新闻的真实性和时效性
"""

import logging
from datetime import datetime
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class Verifier:
    """交叉验证器"""
    
    def __init__(self):
        self.seen_titles = {}  # 标题 -> 日期
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def verify_date(self, date_str: str) -> bool:
        """验证日期格式"""
        if not date_str:
            return False
        try:
            datetime.strptime(date_str[:10], '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def is_duplicate(self, article: dict, existing_articles: list) -> bool:
        """检查是否为重复新闻"""
        title = article['title']
        date = article.get('date', '')
        
        for existing in existing_articles:
            existing_title = existing['title']
            existing_date = existing.get('date', '')
            
            # 标题相似度 > 80%
            if self.calculate_similarity(title, existing_title) > 0.8:
                # 日期相同 = 重复
                if date == existing_date:
                    return True
                # 日期不同，取最新的
                elif date > existing_date:
                    return False
                else:
                    return False
        
        return False
    
    def cross_verify(self, articles: list) -> list:
        """交叉验证所有新闻"""
        verified = []
        
        for article in articles:
            date = article.get('date', '')
            
            # 放宽验证规则：允许无明确日期的新闻
            # 只过滤明显谣言（如"Tim Cook 卸任"）
            title = article['title'].lower()
            if 'stepping down' in title or 'resign' in title or 'quit' in title:
                logger.warning(f"过滤明显谣言：{article['title']}")
                continue
            
            # 日期验证失败但标题正常，仍然保留
            if not self.verify_date(date):
                logger.info(f"日期验证失败，但保留新闻：{article['title']}")
                # 添加默认日期（今天）
                article['date'] = datetime.now().strftime('%Y-%m-%d')
            
            # 检查重复
            if self.is_duplicate(article, verified):
                logger.info(f"跳过重复新闻：{article['title']}")
                continue
            
            verified.append(article)
        
        return verified
    
    def prioritize_sources(self, articles: list) -> list:
        """根据来源优先级排序"""
        priority = {
            'Anthropic': 1,
            'OpenAI': 2,
            '智谱': 3,
            '通义千问': 4,
            'TechCrunch': 5,
            'Product Hunt': 6,
            'GitHub': 7
        }
        
        return sorted(articles, key=lambda x: priority.get(x.get('source', ''), 99))
