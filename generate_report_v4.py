#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报 V4 - 报告生成脚本（V4 标准版）
使用固定样式：styles/v4_standard.css
"""

import json
from datetime import datetime

# 读取分类后的新闻
with open('/tmp/news_final.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

# 板块标题映射
section_titles = {
    "今日要闻": "📌 今日要闻",
    "国内 AI 动态": "🇨🇳 国内 AI 动态",
    "海外最新动态": "🌍 海外最新动态",
    "大模型动态": "🤖 大模型动态",
    "产品发布与更新": "📦 产品发布与更新",
    "融资与商业": "💰 融资与商业",
    "政策与监管": "⚖️ 政策与监管",
    "GitHub 热门 AI 项目": "💻 GitHub 热门 AI 项目",
    "Product Hunt AI 新品": "🚀 Product Hunt AI 新品"
}

# 统计总新闻数
total_news = sum(len(news_list) for news_list in sections.values())

# 读取 V4 标准 CSS
with open('styles/v4_standard.css', 'r', encoding='utf-8') as f:
    v4_css = f.read()

# 生成 HTML
generate_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
date = datetime.now().strftime('%Y-%m-%d')

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 日报 V4 - {date}</title>
    <style>
{v4_css}
    </style>
</head>
<body>
    <div class="container">
        <h1>📰 AI 日报 V4</h1>
        <div class="meta">
            <p><strong>生成时间:</strong> {generate_time}</p>
            <p><strong>数据日期:</strong> {date}</p>
            <p><strong>新闻来源:</strong> 量子位、Hacker News、Hugging Face Blog、Anthropic、GitHub Trending、Product Hunt</p>
            <p><strong>总新闻数:</strong> {total_news} 条</p>
        </div>
        
        <!-- 9 个板块 -->
"""

# 添加所有板块
for section_name, news_list in sections.items():
    html += f"""
        <div class="section">
            <h2>{section_titles.get(section_name, section_name)}</h2>
"""
    
    if isinstance(news_list, list) and len(news_list) > 0:
        for news in news_list:
            keywords_html = ''.join([f'<span class="news-keywords">{kw}</span>' for kw in news.get('关键词', [])])
            
            html += f"""
            <div class="news-item">
                <div class="news-title">{news['标题']}</div>
                <div class="news-meta">
                    <span>📅 {news['日期']}</span> | 
                    <span>📰 {news['来源']}</span>
                </div>
                <div class="news-summary">
                    <strong>一句话概括:</strong> {news['一句话概括']}
                </div>
                <div>
                    <strong>关键词:</strong> {keywords_html}
                </div>
                <div class="news-takeaway">
                    <strong>Takeaway:</strong> {news['Takeaway']}
                </div>
                <div class="news-fusion">
                    <strong>跨界融合:</strong> {news['跨界融合']}
                </div>
            </div>
"""
    else:
        html += f"""
            <div class="empty-section">暂无更新</div>
"""
    
    html += """
        </div>
"""

# 添加底部
html += """
    </div>
</body>
</html>
"""

# 保存报告
report_path = 'reports/v4_2026-04-26_V4_标准版.html'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 报告已生成：{report_path}")
print(f"📊 总新闻数：{total_news} 条")
print("\n📋 新闻分布:")
for section, news_list in sections.items():
    print(f"  - {section}: {len(news_list)} 条")
