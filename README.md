# AI Daily Report - 自动化早报系统

## 📋 项目概述

AI 日报项目是一个自动化系统，每日 9:00 自动采集 AI 新闻，生成早报并通过飞书推送。

**核心功能**:
- 每日 9:00 自动采集 AI 新闻
- 交叉验证确保数据准确性
- 生成 HTML 格式早报
- 飞书通知推送

**GitHub**: https://github.com/Donna622520/ai-daily-report  
**GitHub Pages**: https://donna622520.github.io/ai-daily-report/

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424
sudo apt-get install -y python3-pip python3-bs4 python3-lxml python3-yaml python3-dateutil
```

### 2. 运行日报

```bash
chmod +x run.sh
./run.sh
```

### 3. 查看日报

日报生成后位于：
```
archive/YYYY-MM/v3_YYYY-MM-DD.html  # V3 版标准 (6 个板块)
```

**V3 版特性**:
- ✅ 6 个板块结构：今日要闻、大模型动态、GitHub Trending AI、科技媒体精选、社区热议、学术前沿
- ✅ 未找到板块明确标注原因和建议
- ✅ 飞书消息使用 Markdown 超链接格式

---

## 📊 板块结构

1. **🔥 今日要闻** - Product Hunt, GitHub Trending 最新产品
2. **🤖 大模型动态** - Anthropic, OpenAI, 智谱，通义千问等官方博客
3. **📊 GitHub Trending AI** - AI 相关开源项目
4. **📰 科技媒体精选** - TechCrunch, The Verge, 36 氪等
5. **💬 社区热议** - Hacker News, Reddit, V2EX
6. **🎓 学术前沿** - arXiv, Hugging Face Blog

---

## 🔧 配置说明

### 飞书通知

**配置方式**:
- **目标**: `feishu:oc_f4e9efc6365614e5bbb4aae76014bc90`
- **方式**: 使用 `send_message` 工具
- **无需**: webhook URL 配置

**消息格式**:
```markdown
📰 **AI 日报 - {date}**

🔗 **查看日报**: [完整链接](完整链接)

📚 **历史归档**: [归档页面](归档链接)

---
**今日重点**:
1. 重点新闻 1
2. 重点新闻 2
```

**超链接格式**:
- ✅ 正确：`[显示文本](URL)`
- ❌ 错误：`URL`（纯文本会显示为黑色字符串）

---

## 📅 定时任务

```bash
crontab -e
# 添加：0 9 * * * /home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/run.sh >> logs/cron.log 2>&1
```

---

## 📚 相关文档

- **经验总结**: [EXPERIENCE.md](EXPERIENCE.md) - 成功/失败经验、最佳实践
- **交付流程**: [delivery-pipeline](~/.hermes/skills/devops/delivery-pipeline/SKILL.md) - 任务交付标准化流程
- **技能文档**: [ai-daily-report](~/.hermes/skills/devops/ai-daily-report/SKILL.md) - 详细操作流程

---

## 🛠️ 技术栈

- **Python**: requests, BeautifulSoup, lxml
- **Bash**: 脚本自动化
- **Git**: 版本控制
- **GitHub CLI (gh)**: 仓库管理
- **飞书**: 通知推送

---

## 📝 版本历史

- **V3 (2026-04-24)**: 6 个板块结构，未找到板块明确标注
- **V2**: 来源优先级标识，分段生成策略
- **V1**: 基础版本

---

*最后更新：2026-04-24*
*项目路径：/home/donna/Hermes/workspace/projects/ai-daily-report-V1-0424/*
