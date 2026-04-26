"""
报告生成器
生成 AI 日报 HTML 报告
"""

import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, archive_path: str = "archive"):
        self.archive_path = archive_path
    
    def generate_report(self, articles: list, date: str = None, sections: dict = None, version: str = None) -> str:
        """生成日报报告"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 确保归档目录存在
        archive_dir = os.path.join(self.archive_path, date[:7])  # YYYY-MM
        os.makedirs(archive_dir, exist_ok=True)
        
        # 从配置读取版本号，如果没有传入则使用默认值
        if not version:
            try:
                import yaml
                with open('config.yaml', 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    version = config.get('version', {}).get('number', 'v3')
            except Exception as e:
                logger.warning(f"读取配置失败，使用默认版本号 v3: {e}")
                version = 'v3'
        
        # 生成文件名：{version}_{date}.html
        filename = f"{version}_{date}.html"
        filepath = os.path.join(archive_dir, filename)
        
        # 生成 HTML 内容
        html_content = self._generate_html(articles, date, sections)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"报告已生成：{filepath}")
        return filepath
    
    def _generate_html(self, articles: list, date: str, sections: dict = None) -> str:
        """生成 HTML 内容"""
        # 定义板块结构
        section_titles = {
            'highlights': '🔥 今日要闻',
            'llm_updates': '🤖 大模型动态',
            'github_trending': '📊 GitHub Trending AI',
            'tech_media': '📰 科技媒体精选',
            'community': '💬 社区热议',
            'academic': '🎓 学术前沿'
        }
        
        # 如果没有传入 sections 参数，使用默认顺序
        if not sections:
            sections = {
                'highlights': [],
                'llm_updates': [],
                'github_trending': [],
                'tech_media': [],
                'community': [],
                'academic': []
            }
            
            # 根据来源分类文章
            for article in articles:
                source = article.get('source', '').lower()
                if 'product hunt' in source or 'github' in source:
                    sections['highlights'].append(article)
                elif 'anthropic' in source or 'openai' in source or 'zhipu' in source or 'qwen' in source:
                    sections['llm_updates'].append(article)
                elif 'github' in source:
                    sections['github_trending'].append(article)
                elif 'techcrunch' in source or 'the verge' in source or '36 氪' in source or '机器之心' in source or '量子位' in source:
                    sections['tech_media'].append(article)
                elif 'hacker news' in source or 'reddit' in source or 'v2ex' in source:
                    sections['community'].append(article)
                elif 'arxiv' in source or 'hugging face' in source:
                    sections['academic'].append(article)
        
        
        # 生成 HTML 内容
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报 - {date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .date {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-left: 15px;
            border-left: 4px solid #667eea;
        }}
        
        .article {{
            padding: 20px;
            background: #fafafa;
            margin-bottom: 15px;
            border-radius: 8px;
        }}
        
        .article:last-child {{
            margin-bottom: 0;
        }}
        
        .article h2 {{
            font-size: 18px;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .article h2 a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .article h2 a:hover {{
            color: #667eea;
        }}
        
        .meta {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }}
        
        .meta span {{
            margin-right: 15px;
        }}
        
        .summary {{
            font-size: 15px;
            color: #444;
            line-height: 1.6;
        }}
        
        .no-news {{
            padding: 30px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            color: #856404;
        }}
        
        .no-news h3 {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        
        .no-news p {{
            font-size: 14px;
            margin-bottom: 5px;
        }}
        
        .footer {{
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 日报</h1>
            <div class="date">{date}</div>
        </div>
        
        <div class="content">
"""
        
        # 遍历所有板块
        for section_key, section_name in section_titles.items():
            section_articles = sections.get(section_key, [])
            
            if section_articles:
                # 有新闻的板块
                html_content += f"""
            <div class="section">
                <h2 class="section-title">{section_name}</h2>
"""
                for i, article in enumerate(section_articles, 1):
                    html_content += f"""
                <div class="article">
                    <h2>{i}. <a href="{article['link']}" target="_blank">{article['title']}</a></h2>
                    <div class="meta">
                        <span>📅 {article.get('date', '未知日期')}</span>
                        <span>📰 {article.get('source', '未知来源')}</span>
                    </div>
                    <div class="summary">
                        {article.get('summary', '暂无摘要')}
                    </div>
                </div>
"""
                html_content += """
            </div>
"""
            else:
                # 没有新闻的板块 - 明确标注
                html_content += f"""
            <div class="section">
                <h2 class="section-title">{section_name}</h2>
                <div class="no-news">
                    <h3>❌ 未找到 {section_name} 新闻</h3>
                    <p>原因：当天无相关新闻或爬虫未能成功抓取</p>
                    <p>建议：手动访问相关网站查看</p>
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>AI 日报 - 每日 9 点自动更新</p>
            <p>数据来源：官方可验证的真实消息</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
