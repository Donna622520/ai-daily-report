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

---

## 4. 交叉验证机制

### 4.1 时间戳验证
- **格式**: YYYY-MM-DD HH:MM
- **提取方式**: 
  - 从 HTML meta 标签提取
  - 从 RSS 条目提取
  - 从 API 响应提取
- **验证规则**: 
  - 必须包含完整的年月日
  - 排除年份不匹配的新闻

### 4.2 去重规则
```python
def is_duplicate(news1, news2):
    # 标题相似度 > 80% + 日期相同 = 重复
    if similarity(news1['title'], news2['title']) > 0.8:
        if news1['date'] == news2['date']:
            return True
        # 日期不同，取最新的
        elif news1['date'] > news2['date']:
            return False  # 保留 news1
        else:
            return False  # 保留 news2
    return False
```

### 4.3 官方优先策略
1. **一级优先**: 官方博客、官方 API
2. **二级优先**: 权威新闻网站 (TechCrunch, The Verge)
3. **三级优先**: 第三方聚合 (Product Hunt, GitHub)

### 4.4 多源确认
- 同一新闻至少 2 个独立来源确认
- 官方来源可单独确认
- 排除单一来源的传闻

---

## 5. 早报内容格式

### 5.1 新闻条目模板
```markdown
N. [标题]
关键词：[关键词 1], [关键词 2], [关键词 3]
一句话概括：[核心内容]
具体内容：[详细描述，包括时间、地点、人物、数据等]
Takeaway: [核心洞察或启示]
跨界延伸：[与相关领域或行业的关联性分析]
```

### 5.2 字段说明
- **N**: 序号 (从 1 开始)
- **标题**: 新闻标题
- **关键词**: 3-5 个核心关键词
- **一句话概括**: 50 字以内的核心内容总结
- **具体内容**: 200-500 字的详细描述
- **Takeaway**: 1-2 句核心洞察
- **跨界延伸**: 与相关领域或行业的关联性分析

### 5.3 板块分类
1. 📌 今日要闻
2. 🏢 大模型动态
3. 📱 产品发布与更新
4. 🌐 浏览器 × AI
5. 💰 融资与商业
6. 🧠 技术洞察
7. 📜 政策与监管
8. 📈 GitHub 热门 AI 项目
9. 🚀 Product Hunt AI 新品
