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
    
    def generate_report(self, articles: list, date: str = None) -> str:
        """生成日报报告"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 确保归档目录存在
        archive_dir = os.path.join(self.archive_path, date[:7])  # YYYY-MM
        os.makedirs(archive_dir, exist_ok=True)
        
        # 生成文件名
        filename = f"{date}.html"
        filepath = os.path.join(archive_dir, filename)
        
        # 生成 HTML 内容
        html_content = self._generate_html(articles, date)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"报告已生成：{filepath}")
        return filepath
    
    def _generate_html(self, articles: list, date: str) -> str:
        """生成 HTML 内容"""
        return f"""<!DOCTYPE html>
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
        
        .article {{
            padding: 20px;
            border-bottom: 1px solid #eee;
        }}
        
        .article:last-child {{
            border-bottom: none;
        }}
        
        .article h2 {{
            font-size: 20px;
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
        
        for i, article in enumerate(articles, 1):
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
        
        <div class="footer">
            <p>AI 日报 - 每日 9 点自动更新</p>
            <p>数据来源：官方可验证的真实消息</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
