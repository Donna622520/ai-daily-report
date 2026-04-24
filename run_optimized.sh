#!/bin/bash

# AI Daily Report - 优化版运行脚本
# 使用 blogwatcher 监控官方博客 + 多源验证策略

set -e

PROJECT_DIR="/home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424"
cd "$PROJECT_DIR"

# 创建日志目录
mkdir -p logs archive/$(date +%Y-%m)

echo "=== AI Daily Report - $(date +%Y-%m-%d) ===" | tee logs/run.log

# 1. 使用 blogwatcher 监控官方博客（如果已安装）
if command -v blogwatcher-cli &> /dev/null; then
    echo "📰 扫描官方博客更新..." | tee -a logs/run.log
    blogwatcher-cli scan 2>> logs/run.log || true
    blogwatcher-cli articles >> logs/blogwatcher.log 2>> logs/run.log || true
    echo "✅ 博客监控完成" | tee -a logs/run.log
else
    echo "⚠️  blogwatcher 未安装，跳过博客监控" | tee -a logs/run.log
    echo "安装：curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli" | tee -a logs/run.log
fi

# 2. 使用 Python 爬虫采集新闻
echo "🕷️  运行爬虫..." | tee -a logs/run.log
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

import logging
from crawler.github import GitHubCrawler
from crawler.verifier import Verifier
from generator.report import ReportGenerator
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crawler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info('开始采集新闻...')

all_articles = []

# GitHub 爬虫（最可靠）
try:
    logger.info('采集 GitHub Trending...')
    gh = GitHubCrawler()
    gh_articles = gh.crawl()
    logger.info(f'GitHub: {len(gh_articles)} 条')
    all_articles.extend(gh_articles)
except Exception as e:
    logger.error(f'GitHub 失败：{e}')

# 交叉验证
if all_articles:
    verifier = Verifier()
    verified = verifier.cross_verify(all_articles)
    verified = verifier.prioritize_sources(verified)
    logger.info(f'验证后：{len(verified)} 条新闻')
else:
    verified = []
    logger.warning('没有采集到任何新闻')

# 生成报告
date = datetime.now().strftime('%Y-%m-%d')
generator = ReportGenerator()
report_path = generator.generate_report(verified, date)
logger.info(f'报告已生成：{report_path}')

if verified:
    logger.info('\n新闻列表:')
    for i, art in enumerate(verified, 1):
        logger.info(f'{i}. {art.get("title", "无标题")}')
else:
    logger.info('\n⚠️  没有采集到新闻，生成空报告')
EOF

echo "✅ 爬虫完成" | tee -a logs/run.log

# 3. 发送飞书通知（通过 Hermes 工具）
echo "📱 准备发送飞书通知..." | tee -a logs/run.log
# 注意：飞书通知需要通过 send_message 工具发送，这里仅记录

echo "=== 完成 ===" | tee -a logs/run.log
echo "日报路径：archive/$(date +%Y-%m)/$(date +%Y-%m-%d).html" | tee -a logs/run.log
