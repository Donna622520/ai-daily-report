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

# 板块 1: 今日要闻 (Product Hunt, GitHub Trending)
logger.info('板块 1: 采集今日要闻...')
ph_crawler = ProductHuntCrawler()
ph_articles = ph_crawler.crawl()
all_articles.extend(ph_articles)

gh_crawler = GitHubCrawler()
gh_articles = gh_crawler.crawl()
all_articles.extend(gh_articles)

# 板块 2: 大模型动态 (官方博客)
logger.info('板块 2: 采集大模型动态...')
blog_crawler = BlogCrawler()
blog_articles = blog_crawler.crawl()
all_articles.extend(blog_articles)

# 板块 3: 科技媒体精选
logger.info('板块 3: 采集科技媒体...')
tc_crawler = TechCrunchCrawler()
tc_articles = tc_crawler.crawl()
all_articles.extend(tc_articles)

# 板块 4: 国内科技媒体 (36 氪，机器之心，量子位)
logger.info('板块 4: 采集国内科技媒体...')
# TODO: 添加国内科技媒体爬虫
# domestic_crawler = DomesticMediaCrawler()
# domestic_articles = domestic_crawler.crawl()
# all_articles.extend(domestic_articles)

# 板块 5: 社区热议 (Hacker News, Reddit, V2EX)
logger.info('板块 5: 采集社区热议...')
# TODO: 添加社区爬虫
# community_crawler = CommunityCrawler()
# community_articles = community_crawler.crawl()
# all_articles.extend(community_articles)

# 板块 6: 学术前沿 (arXiv, Hugging Face)
logger.info('板块 6: 采集学术前沿...')
# TODO: 添加学术爬虫
# academic_crawler = AcademicCrawler()
# academic_articles = academic_crawler.crawl()
# all_articles.extend(academic_articles)

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

# 从配置读取版本号
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
version = config.get('version', {}).get('number', 'v3')

report_path = generator.generate_report(verified_articles, version=version)

# 验证版本号一致性
expected_filename = f"{version}_{date}.html"
actual_filename = os.path.basename(report_path)
if expected_filename != actual_filename:
    logger.error(f"版本号不一致！期望：{expected_filename}, 实际：{actual_filename}")
    raise ValueError(f"版本号验证失败：期望 {expected_filename}, 实际 {actual_filename}")
else:
    logger.info(f"✅ 版本号验证通过：{actual_filename}")

# 发送通知
if config['feishu']['enabled']:
    notifier = FeishuNotifier()
    notifier.send_notification(report_path, date, success=True, news_count=len(verified_articles))

logger.info('AI 日报生成完成!')

# 自动推送到 GitHub
logger.info('推送到 GitHub...')
import subprocess
import datetime
subprocess.run(['git', 'add', '.'], check=True)
subprocess.run(['git', 'commit', '-m', f'auto: 更新日报 {datetime.datetime.now().strftime(\"%Y-%m-%d\")}'], check=True)
subprocess.run(['git', 'push', 'origin', 'master'], check=True)
logger.info('✅ 已推送到 GitHub')

# 生成 GitHub Pages 链接
base_url = 'https://donna622520.github.io/ai-daily-report/'
today = datetime.datetime.now().strftime('%Y-%m-%d')
print(f'📰 日报链接：{base_url}archive/{today[:7]}/{version}_{today}.html')
"
