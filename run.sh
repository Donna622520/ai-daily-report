#!/bin/bash
# AI 日报运行脚本

cd /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424

# 创建 logs 目录
mkdir -p logs

# 运行爬虫和生成器
python3 -c "
import sys
sys.path.insert(0, 'src')

from crawler.product_hunt import ProductHuntCrawler
from crawler.github import GitHubCrawler
from crawler.techcrunch import TechCrunchCrawler
from crawler.blog import BlogCrawler
from crawler.verifier import Verifier
from generator.report import ReportGenerator
from notifier.feishu import FeishuNotifier
import logging
import yaml

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crawler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 加载配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 采集数据
all_articles = []

logger.info('开始采集 Product Hunt...')
ph_crawler = ProductHuntCrawler()
all_articles.extend(ph_crawler.crawl())

logger.info('开始采集 GitHub...')
gh_crawler = GitHubCrawler()
all_articles.extend(gh_crawler.crawl())

logger.info('开始采集 TechCrunch...')
tc_crawler = TechCrunchCrawler()
all_articles.extend(tc_crawler.crawl())

logger.info('开始采集官方博客...')
blog_crawler = BlogCrawler()
all_articles.extend(blog_crawler.crawl())

logger.info(f'共采集 {len(all_articles)} 条新闻')

# 交叉验证
logger.info('开始交叉验证...')
verifier = Verifier()
verified_articles = verifier.cross_verify(all_articles)
verified_articles = verifier.prioritize_sources(verified_articles)

logger.info(f'验证后剩余 {len(verified_articles)} 条新闻')

# 生成报告
logger.info('生成报告...')
generator = ReportGenerator()
report_path = generator.generate_report(verified_articles)

# 发送通知
if config['feishu']['enabled']:
    notifier = FeishuNotifier()
    notifier.send_notification(report_path, '2026-04-24', success=True)

logger.info('AI 日报生成完成!')
"
