# AI 日报 V4 - 自动化新闻聚合系统

> 每日自动生成 AI 领域新闻日报，支持 9 大板块 + 7 字段规范，卡片式布局，易读性强。

## 📌 项目概述

AI 日报 V4 是一个自动化新闻聚合系统，每天从多个新闻源采集 AI 领域新闻，自动生成结构化的 HTML 日报。

**核心特性**：
- ✅ **9 大板块**：今日要闻、国内 AI 动态、海外最新动态、大模型动态、产品发布与更新、融资与商业、政策与监管、GitHub 热门 AI 项目、Product Hunt AI 新品
- ✅ **7 字段规范**：标题、日期、来源、一句话概括、关键词、Takeaway、跨界融合
- ✅ **V4 标准样式**：卡片式布局、800px 最佳阅读宽度、响应式设计
- ✅ **自动清理**：定期清理临时文件和缓存，节省磁盘空间

## 🚀 快速开始

### 1. 环境准备

```bash
# 进入项目目录
cd /home/donna/Hermes/workspace/projects/ai-daily-report-V4-0426

# 安装依赖（如果需要）
pip install jinja2 -q
```

### 2. 生成日报

```bash
# 运行生成脚本
python3 generate_report_v4.py

# 打开报告
xdg-open reports/v4_2026-04-26_V4_标准版.html
```

### 3. 配置新闻源

编辑 `config.yaml` 文件，添加或修改新闻源：

```yaml
sources:
  - https://www.qbitai.com/           # 量子位
  - https://www.jiqizhixin.com        # 机器之心
  - https://36kr.com/                 # 36Kr
  - https://news.ycombinator.com/     # Hacker News
  - https://huggingface.co/blog       # Hugging Face Blog
  - https://www.anthropic.com/news    # Anthropic News
  - https://openai.com/news           # OpenAI News
  - https://github.com/trending       # GitHub Trending
  - https://www.producthunt.com/topics/ai  # Product Hunt AI
```

### 4. 定时任务（可选）

添加到 crontab 实现每日自动运行：

```bash
# 编辑 crontab
crontab -e

# 添加每日 9:00 运行（修改为实际时间）
0 9 * * * cd /home/donna/Hermes/workspace/projects/ai-daily-report-V4-0426 && python3 generate_report_v4.py
```

## 📁 项目结构

```
ai-daily-report-V4-0426/
├── config.yaml              # 新闻源配置
├── config-ui.yaml           # UI 配置（颜色、字体、布局）
├── generate_report_v4.py    # 报告生成脚本
├── styles/
│   └── v4_standard.css      # V4 标准样式
├── templates/
│   └── report.html          # Jinja2 模板（可选）
├── reports/
│   ├── v4_2026-04-26_V4_标准版.html  # 最新报告
│   └── archive/             # 历史版本备份
├── README.md                # 项目说明（本文件）
├── SKILL.md                 # AI 工作流规范
└── EXPERIENCE.md            # 经验沉淀文档
```

## 🎨 样式说明

**V4 标准样式特点**：
- **卡片式布局**：每个板块和新闻都是独立卡片
- **颜色分类**：
  - 蓝色（#1a73e8）：主色、标题、关键词
  - 黄色（#fff3cd）：Takeaway 高亮
  - 绿色（#d4edda）：跨界融合高亮
  - 灰色（#f5f5f5）：页面背景
- **最佳阅读宽度**：800px（60-75 字符/行）
- **响应式设计**：支持移动端（600px 断点）
- **悬停交互**：鼠标悬停卡片有阴影效果

## 📊 数据格式

每条新闻包含 7 个字段：

```json
{
  "标题": "新闻标题",
  "日期": "2026-04-26",
  "来源": "新闻源名称",
  "一句话概括": "简要描述新闻内容",
  "关键词": ["关键词 1", "关键词 2"],
  "Takeaway": "影响/启示",
  "跨界融合": "AI+ 其他领域的融合应用"
}
```

## 🔧 故障排查

### 问题 1：报告样式不显示

**原因**：CSS 文件未正确加载

**解决方案**：
```bash
# 检查 CSS 文件是否存在
ls -l styles/v4_standard.css

# 如果不存在，重新生成
python3 generate_report_v4.py
```

### 问题 2：新闻源无法访问

**原因**：网络问题或网站反爬

**解决方案**：
```bash
# 检查网络连接
ping www.qbitai.com

# 更换新闻源
# 编辑 config.yaml，移除无法访问的源
```

### 问题 3：报告内容为空

**原因**：新闻数据未正确采集

**解决方案**：
```bash
# 检查临时数据文件
cat /tmp/news_final.json

# 如果为空，重新运行爬虫脚本
# （需要单独的新闻采集脚本）
```

## 📚 相关文档

- **SKILL.md**：AI 工作流规范，指导如何执行任务
- **EXPERIENCE.md**：经验沉淀，记录成功经验和失败教训
- **资源库.md**：外部技能资源库，记录可集成的技能市场链接

## 🔄 版本历史

- **V4 (2026-04-26)**：固定标准样式，卡片式布局，9 大板块
- **V3**：早期版本，样式未固定
- **V2**：尝试多种样式
- **V1**：初始版本

## 📝 维护说明

**备份策略**：
- 每日报告自动保存到 `reports/` 目录
- 历史版本自动备份到 `reports/archive/` 目录
- 每次生成新报告前，旧报告自动归档

**清理策略**：
- 临时文件（`/tmp/news_*.json`）定期清理
- Python 缓存（`.pyc`, `__pycache__`）定期清理
- 超过 30 天的报告可手动删除

## 🤝 贡献指南

如需修改样式或添加新功能：

1. **修改样式**：编辑 `styles/v4_standard.css`
2. **修改模板**：编辑 `templates/report.html`（如果使用模板）
3. **修改配置**：编辑 `config.yaml` 或 `config-ui.yaml`
4. **测试验证**：运行 `python3 generate_report_v4.py` 生成报告查看效果

## 📄 许可证

本项目为个人项目，仅供学习和研究使用。

---

**最后更新**：2026-04-26  
**版本**：V4.0  
**作者**：Donna
