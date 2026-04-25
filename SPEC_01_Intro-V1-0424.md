# AI 日报项目 - 规格说明书 (SPEC)

## 1. 项目概述

### 1.1 项目目标
开发一个本地部署的 AI 早报网站，每日 9 点自动更新，收录过去 24 小时内官方可验证的真实 AI 新闻。

### 1.2 核心要求
- **数据来源**: 仅收录官方可验证的真实消息，排除传闻、谣言及编造新闻
- **更新频率**: 每日 9:00 自动更新
- **交叉验证**: 确保数据源是最新的，准确提取年月日信息
- **通知机制**: 飞书推送通知
- **历史归档**: 保存所有历史早报

### 1.3 技术栈选择
- **前端**: 纯 HTML + CSS (美观版，单文件可直接浏览器打开)
- **爬虫**: Python (requests + BeautifulSoup + lxml)
- **定时任务**: cron (Linux 系统自带)
- **通知**: 飞书 Webhook
- **部署**: 本地运行，无需服务器

---

## 2. 项目结构

```
/home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/
├── src/
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── base.py              # 基础爬虫类
│   │   ├── product_hunt.py      # Product Hunt 爬虫
│   │   ├── github.py            # GitHub 爬虫
│   │   ├── techcrunch.py        # TechCrunch 爬虫
│   │   ├── blog.py              # 官方博客爬虫
│   │   └── verifier.py          # 交叉验证器
│   ├── generator/
│   │   ├── __init__.py
│   │   ├── report.py            # 报告生成器
│   │   └── template.html        # HTML 模板
│   └── notifier/
│       ├── __init__.py
│       └── feishu.py            # 飞书通知
├── archive/                     # 历史早报归档
│   ├── 2026-04/
│   │   └── 2026-04-22.html
│   └── 2026-05/
├── logs/
│   └── crawler.log
├── config.yaml                  # 配置
├── requirements.txt             # Python 依赖
├── run.sh                       # 运行脚本
└── cron_job.sh                  # cron 定时任务脚本
```

---

## 3. 数据来源与采集策略

### 3.1 官方渠道列表

#### 3.1.1 Product Hunt (产品发布)
- **URL**: https://www.producthunt.com/
- **API**: `https://api.producthunt.com/v2/`
- **RSS**: `https://www.producthunt.com/feed`
- **关键词**: `artificial-intelligence`, `machine-learning`, `ai`
- **采集频率**: 每小时 1 次

#### 3.1.2 GitHub Trending (热门项目)
- **URL**: https://github.com/trending
- **API**: `https://api.github.com/search/repositories`
- **关键词**: `artificial-intelligence`, `machine-learning`, `ai`
- **排序**: `stars` + `updated_at`
- **采集频率**: 每日 1 次

#### 3.1.3 TechCrunch AI (商业新闻)
- **URL**: https://techcrunch.com/category/artificial-intelligence/
- **RSS**: `https://techcrunch.com/category/artificial-intelligence/feed/`
- **关键词**: `AI`, `artificial intelligence`
- **采集频率**: 每小时 1 次

#### 3.1.4 官方博客 (中英文)
- **Anthropic**: https://www.anthropic.com/news
- **OpenAI**: https://openai.com/blog
- **智谱**: https://www.zhipuai.cn/news
- **通义千问**: https://www.aliyun.com/product/qwen
- **采集频率**: 每日 2 次

#### 3.1.5 技术博客 (英文)
- **Simon Willison**: https://simonwillison.net/
- **Andrej Karpathy**: https://karpathy.ai/
- **采集频率**: 每日 1 次

### 3.2 数据采集流程
1. 定时触发爬虫任务
2. 从各渠道提取新闻标题、链接、发布时间
3. 提取发布时间戳 (YYYY-MM-DD 格式)
4. 交叉验证去重
5. 生成早报内容
