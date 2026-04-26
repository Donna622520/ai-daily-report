#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 日报 V4 - 报告生成脚本（配置化版本）
使用 Jinja2 模板 + CSS 变量
"""

import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

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

# 设置 Jinja2 环境
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report.html')

# 生成 HTML
html_content = template.render(
    title=f"AI 日报 V4 - {datetime.now().strftime('%Y-%m-%d')}",
    header_title="📰 AI 日报 V4",
    date=datetime.now().strftime('%Y-%m-%d'),
    generate_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    total_news=total_news,
    sections=sections,
    section_titles=section_titles
)

# 保存报告
report_path = 'reports/v4_2026-04-26_配置化.html'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 报告已生成：{report_path}")
print(f"📊 总新闻数：{total_news} 条")
print("\n📋 新闻分布:")
for section, news_list in sections.items():
    print(f"  - {section}: {len(news_list)} 条")
