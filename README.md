# AI 日报项目

每日 9 点自动更新的 AI 早报，收录官方可验证的真实 AI 新闻。

## 项目结构

```
/home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/
├── src/
│   ├── crawler/
│   │   ├── base.py              # 基础爬虫类
│   │   ├── product_hunt.py      # Product Hunt 爬虫
│   │   ├── github.py            # GitHub 爬虫
│   │   ├── techcrunch.py        # TechCrunch 爬虫
│   │   ├── blog.py              # 官方博客爬虫
│   │   └── verifier.py          # 交叉验证器
│   ├── generator/
│   │   └── report.py            # 报告生成器
│   └── notifier/
│       └── feishu.py            # 飞书通知
├── archive/                     # 历史早报归档
├── logs/
├── config.yaml                  # 配置
├── requirements.txt             # Python 依赖
├── run.sh                       # 运行脚本
├── cron_job.sh                  # cron 定时任务脚本
└── README.md                    # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
cd /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424
sudo apt-get install -y python3-pip python3-bs4 python3-lxml python3-yaml python3-dateutil
```

### 2. 测试运行

```bash
cd /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424
chmod +x run.sh
./run.sh
```

运行后生成 V2 版日报：
- **V2 版标准**: `archive/YYYY-MM/v2_YYYY-MM-DD.html`
- **对比报告**: `archive/YYYY-MM/v1_vs_v2_comparison.md` (可选)

### 3. 查看日报

日报生成后位于：
```
archive/YYYY-MM/v2_YYYY-MM-DD.html  # V2 版标准
archive/YYYY-MM/YYYY-MM-DD.html     # V1 版 (可选)
```

**V2 版特性**:
- ✅ 来源优先级标识 (二级/三级)
- ✅ 分段生成策略 (large-document-writing)
- ✅ 数据来源完全透明
- ✅ 版本追踪机制

直接用浏览器打开查看。

### 4. 配置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务 (每日 9:00 执行)
0 9 * * * /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/run.sh >> logs/cron.log 2>&1
```

## 飞书通知配置

项目使用 `send_message` 工具发送飞书消息，无需配置 webhook URL。

### 配置方式

飞书通知已配置为发送到用户私聊：
- **目标**: `feishu:oc_f4e9efc6365614e5bbb4aae76014bc90`
- **方式**: 通过 send_message 工具
- **无需**: webhook URL 配置

### 测试通知

手动发送测试消息：
```python
from hermes_tools import send_message
send_message(message="测试消息", target="feishu:oc_f4e9efc6365614e5bbb4aae76014bc90")
```

## 数据源

- **Product Hunt**: AI 产品发布
- **GitHub Trending**: AI 热门项目
- **TechCrunch AI**: AI 商业新闻
- **官方博客**: Anthropic, OpenAI, 智谱，通义千问

## 交叉验证机制

- **时间戳验证**: 提取并验证发布日期
- **去重规则**: 标题相似度 > 80% + 日期相同 = 重复
- **官方优先**: 优先收录官方博客、官方 API
- **多源确认**: 同一新闻至少 2 个独立来源确认

## 日志查看

```bash
# 爬虫日志
tail -f logs/crawler.log

# cron 日志
tail -f logs/cron.log
```

## 常见问题

### 1. 依赖未安装

```bash
sudo apt-get install -y python3-pip python3-bs4 python3-lxml python3-yaml python3-dateutil
```

### 2. 飞书通知失败

检查：
- 飞书连接是否正常
- chat_id 是否正确
- 网络连接是否正常

### 3. 爬虫失败

检查：
- 网络连接
- 目标网站是否可访问
- User-Agent 是否需要更新

## 维护

### 更新数据源

编辑 `src/crawler/blog.py` 添加新的博客：

```python
BLOGS = [
    {
        'name': '新博客名称',
        'url': 'https://example.com/news',
        'keywords': ['关键词 1', '关键词 2']
    },
    # ...
]
```

### 调整采集频率

编辑 `config.yaml`：

```yaml
scheduler:
  time: "0 9 * * *"  # 修改时间
```

### 备份数据

```bash
# 备份归档
tar -czf archive-backup.tar.gz archive/

# 备份配置
cp config.yaml config-backup.yaml
```

## 技术栈

- **Python**: requests, BeautifulSoup, lxml, yaml
- **前端**: 纯 HTML + CSS (美观版)
- **定时任务**: cron
- **通知**: 飞书 send_message 工具

## 版本历史

- **V2-0424**: 标准版本 - 来源优先级标识 + 分段生成 + 数据透明化
  - ✅ 新增来源优先级标识 (二级/三级)
  - ✅ 采用 large-document-writing 分段生成策略
  - ✅ 数据来源完全透明
  - ✅ 版本追踪机制
- **V1-0424**: 初始版本，基础爬虫 + 报告生成 + 飞书通知

## 许可证

MIT License
