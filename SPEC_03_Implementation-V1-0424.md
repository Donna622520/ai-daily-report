# AI 日报项目 - 规格说明书 (SPEC) - 第 3 部分

## 7. 定时任务配置

### 7.1 Cron vs systemd 对比

#### Cron (推荐)
**优点:**
- 最简单，一行命令配置
- 系统自带，无需额外安装
- 适合简单定时任务
- 日志容易查看 (`/var/log/cron`)

**缺点:**
- 功能相对简单
- 错误处理需要自己写脚本

**适合场景**: 你的需求（每日 9 点执行脚本）

#### systemd timer
**优点:**
- 功能更强大
- 更好的日志管理 (`journalctl`)
- 可以依赖其他服务
- 支持失败重试

**缺点:**
- 配置复杂
- 需要额外学习
- 调试相对麻烦

**适合场景**: 复杂服务、需要依赖管理

### 7.2 Cron 配置方案
```bash
# 编辑 crontab
crontab -e

# 添加定时任务 (每日 9:00 执行)
0 9 * * * /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/cron_job.sh >> /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/logs/cron.log 2>&1
```

### 7.3 Cron 日志查看
```bash
# 查看 cron 日志
sudo tail -f /var/log/cron

# 查看项目日志
tail -f /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/logs/crawler.log
```

---

## 8. 开发计划

### 8.1 阶段 1: 基础架构 (已完成)
- [x] 创建项目目录结构
- [x] 编写 SPEC 文档
- [x] 配置 Python 依赖

### 8.2 阶段 2: 爬虫开发
- [ ] 实现基础爬虫类 (base.py)
- [ ] 实现 Product Hunt 爬虫
- [ ] 实现 GitHub 爬虫
- [ ] 实现 TechCrunch 爬虫
- [ ] 实现官方博客爬虫
- [ ] 实现交叉验证器

### 8.3 阶段 3: 报告生成
- [ ] 实现报告生成器 (report.py)
- [ ] 实现 HTML 模板 (template.html)
- [ ] 实现 AI 内容生成 (关键词、概括、Takeaway 等)

### 8.4 阶段 4: 通知与日志
- [ ] 实现飞书通知 (feishu.py)
- [ ] 实现日志记录
- [ ] 实现错误处理

### 8.5 阶段 5: 定时任务
- [ ] 创建运行脚本 (run.sh)
- [ ] 创建 cron 任务脚本 (cron_job.sh)
- [ ] 配置 cron 定时任务
- [ ] 测试定时任务

### 8.6 阶段 6: 测试与优化
- [ ] 测试数据抓取
- [ ] 测试交叉验证
- [ ] 测试报告生成
- [ ] 测试飞书通知
- [ ] 优化性能和准确性

---

## 9. 依赖清单

### 9.1 Python 依赖 (requirements.txt)
```
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
python-dateutil>=2.8.2
pyyaml>=6.0
```

### 9.2 系统依赖
- Python 3.8+
- cron (Linux 系统自带)
- 飞书机器人 Webhook

---

## 10. 配置说明

### 10.1 config.yaml 配置
```yaml
# 定时任务配置
scheduler:
  time: "0 9 * * *"  # 每日 9:00
  timezone: "Asia/Shanghai"

# 数据来源配置
sources:
  product_hunt:
    enabled: true
    keywords: ["artificial-intelligence", "machine-learning", "ai"]
    frequency: hourly
  
  github:
    enabled: true
    keywords: ["artificial-intelligence", "machine-learning", "ai"]
    frequency: daily
  
  techcrunch:
    enabled: true
    rss: "https://techcrunch.com/category/artificial-intelligence/feed/"
    frequency: hourly
  
  blogs:
    - name: "Anthropic"
      url: "https://www.anthropic.com/news"
      frequency: daily
    - name: "OpenAI"
      url: "https://openai.com/blog"
      frequency: daily
    - name: "智谱"
      url: "https://www.zhipuai.cn/news"
      frequency: daily
    - name: "通义千问"
      url: "https://www.aliyun.com/product/qwen"
      frequency: daily

# 飞书通知配置
feishu:
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  enabled: true
  notify_on_success: true
  notify_on_error: true

# 归档配置
archive:
  path: "archive"
  format: "{year}-{month}/{year}-{month}-{day}.html"
```

---

## 11. 验收标准

### 11.1 功能验收
- [ ] 每日 9:00 自动更新早报
- [ ] 数据来源为官方可验证的真实消息
- [ ] 交叉验证机制正常工作
- [ ] 飞书通知正常推送
- [ ] 历史早报正确归档

### 11.2 质量验收
- [ ] 新闻标题准确
- [ ] 关键词提取准确
- [ ] 一句话概括准确
- [ ] 具体内容详细
- [ ] Takeaway 有洞察力
- [ ] 跨界延伸有深度

### 11.3 性能验收
- [ ] 单次更新耗时 < 5 分钟
- [ ] 内存占用 < 500MB
- [ ] 日志记录完整
- [ ] 错误处理完善

---

## 12. 维护与更新

### 12.1 日常维护
- 定期检查日志
- 检查飞书通知是否正常
- 检查归档文件是否完整

### 12.2 版本更新
- 每次更新版本号 (V1, V2, V3...)
- 更新 SPEC 文档
- 记录更新日志

### 12.3 数据备份
- 定期备份 archive/ 目录
- 定期备份 config.yaml
- 定期备份 logs/ 目录

---

## 附录

### A. 参考链接
- [aidailytrending.com](https://aidailytrending.com/)
- [Product Hunt API](https://api.producthunt.com/)
- [GitHub API](https://docs.github.com/en/rest)
- [TechCrunch RSS](https://techcrunch.com/feed/)

### B. 术语表
- **交叉验证**: 通过多个独立来源确认同一新闻的真实性
- **官方优先**: 优先收录官方博客、官方 API 等权威来源
- **时间戳验证**: 提取并验证新闻的发布日期，确保是最新数据
