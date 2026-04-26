# AI 日报 V4 - SKILL 工作流规范

> AI 视角：指导如何执行 AI 日报生成任务，包含工作流、规范约束、执行步骤、验收标准。

## 📋 工作流总览

```
用户请求 → 检查新闻数据 → 生成报告 → 验证结果 → 发送通知 → 归档备份
```

## 🎯 规范约束

### 1. 文件格式规范

**9 大板块**（必须全部存在，不能为空）：
1. 今日要闻
2. 国内 AI 动态
3. 海外最新动态
4. 大模型动态
5. 产品发布与更新
6. 融资与商业
7. 政策与监管
8. GitHub 热门 AI 项目
9. Product Hunt AI 新品

**7 字段规范**（每条新闻必须包含）：
- 标题（string）
- 日期（YYYY-MM-DD 格式）
- 来源（string）
- 一句话概括（string）
- 关键词（array of string）
- Takeaway（string）
- 跨界融合（string）

### 2. 数据新鲜度规范

- **日期要求**：所有新闻必须来自当天（2026-04-26）
- **禁止历史数据**：不得使用过往日期的新闻
- **验证方法**：检查每条新闻的 `日期` 字段

### 3. 样式规范

**V4 标准样式**（固定版本，不可修改）：
- CSS 文件：`styles/v4_standard.css`
- 生成脚本：`generate_report_v4.py`
- 报告输出：`reports/v4_2026-04-26_V4_标准版.html`

**样式特点**：
- 卡片式布局
- 800px 最大宽度
- 蓝色主色（#1a73e8）
- 黄色 Takeaway（#fff3cd）
- 绿色跨界融合（#d4edda）

### 4. 文件管理闭环

**备份流程**：
1. 生成新报告前，检查 `reports/` 目录
2. 将旧报告移动到 `reports/archive/` 目录
3. 添加时间戳到备份文件名
4. 保留至少 3 个历史版本

**清理流程**：
1. 清理临时文件（`/tmp/news_*.json`）
2. 清理 Python 缓存（`.pyc`, `__pycache__`）
3. 记录清理日志（`~/清理日志.txt`）

## 📝 执行步骤

### 步骤 1：检查新闻数据

```bash
# 检查临时新闻数据文件
cat /tmp/news_final.json

# 验证数据结构
python3 -c "import json; data=json.load(open('/tmp/news_final.json')); print(f'板块数：{len(data)}'); print(f'总新闻数：{sum(len(v) for v in data.values())}')"
```

**验收标准**：
- ✅ 文件存在且非空
- ✅ 包含 9 个板块
- ✅ 总新闻数 ≥ 10 条
- ✅ 每条新闻包含 7 个字段

### 步骤 2：生成报告

```bash
# 进入项目目录
cd /home/donna/Hermes/workspace/projects/ai-daily-report-V4-0426

# 运行生成脚本
python3 generate_report_v4.py
```

**验收标准**：
- ✅ 脚本执行无错误
- ✅ 生成报告文件存在
- ✅ 报告文件大小 > 10KB

### 步骤 3：验证报告

```bash
# 检查报告文件
ls -l reports/v4_2026-04-26_V4_标准版.html

# 检查 HTML 结构
grep -c "class=\"news-item\"" reports/v4_2026-04-26_V4_标准版.html

# 检查日期一致性
grep -o "2026-04-26" reports/v4_2026-04-26_V4_标准版.html | wc -l
```

**验收标准**：
- ✅ 新闻项数量 ≥ 10
- ✅ 所有新闻日期都是 2026-04-26
- ✅ 包含 9 个板块

### 步骤 4：打开报告查看

```bash
# 使用浏览器打开
xdg-open reports/v4_2026-04-26_V4_标准版.html
```

**验收标准**：
- ✅ 样式正常显示
- ✅ 卡片布局正确
- ✅ 颜色分类清晰
- ✅ 无空白板块

### 步骤 5：发送通知

```bash
# 通过飞书发送通知
send_message action='send' \
  message='🎉 AI 日报 V4 生成完成\n- 总新闻数：18 条\n- 9 个板块全部填满\n- 报告链接：file:///home/donna/Hermes/workspace/projects/ai-daily-report-V4-0426/reports/v4_2026-04-26_V4_标准版.html' \
  target='feishu:oc_f4e9efc6365614e5bbb4aae76014bc90'
```

### 步骤 6：归档备份

```bash
# 创建备份目录（如果不存在）
mkdir -p reports/archive

# 备份旧报告
cp reports/v4_2026-04-26_V4_标准版.html reports/archive/v4_2026-04-26_V4_标准版_备份_$(date +%H%M%S).html
```

## ✅ 验收标准

### 必须满足的条件：

1. **数据完整性**
   - ✅ 9 个板块全部存在
   - ✅ 每个板块至少有 1 条新闻
   - ✅ 总新闻数 ≥ 10 条

2. **数据准确性**
   - ✅ 所有新闻日期都是当天（2026-04-26）
   - ✅ 每条新闻包含 7 个字段
   - ✅ 来源URL真实有效

3. **样式规范性**
   - ✅ 使用 V4 标准样式（styles/v4_standard.css）
   - ✅ 卡片式布局正确
   - ✅ 颜色分类清晰
   - ✅ 响应式设计正常

4. **文件管理**
   - ✅ 报告文件存在
   - ✅ 历史版本已备份
   - ✅ 临时文件已清理

## 🚨 错误处理

### 错误 1：新闻数据为空

**原因**：爬虫未执行或失败

**处理流程**：
1. 检查 `/tmp/news_final.json` 是否存在
2. 如果不存在，先运行爬虫脚本
3. 如果存在但为空，检查新闻源是否可访问
4. 尝试更换新闻源

### 错误 2：报告样式不显示

**原因**：CSS 文件未正确加载

**处理流程**：
1. 检查 `styles/v4_standard.css` 是否存在
2. 检查 HTML 中是否正确引用 CSS
3. 重新运行生成脚本
4. 强制刷新浏览器（Ctrl+F5）

### 错误 3：板块为空

**原因**：新闻数据未正确分类

**处理流程**：
1. 检查 `/tmp/news_final.json` 的数据结构
2. 确认每个板块都有新闻数据
3. 如果没有，手动添加新闻到对应板块
4. 重新运行生成脚本

## 📚 资源库链接

- **外部技能市场**：
  - SkillsMP：https://skillsmp.com/zh
  - 向阳乔木：https://xiangyangqiaomu.feishu.cn/wiki/N5vDwWcSSiND5wkjFQscAkX4nnd

- **新闻源验证**：
  - 量子位：https://www.qbitai.com/
  - 机器之心：https://www.jiqizhixin.com
  - Hacker News：https://news.ycombinator.com/
  - Hugging Face Blog：https://huggingface.co/blog
  - Anthropic News：https://www.anthropic.com/news
  - GitHub Trending：https://github.com/trending

## 💡 经验沉淀链接

详细经验沉淀请查看 `EXPERIENCE.md` 文件，包含：
- 历史版本对比
- 常见问题解决方案
- 验证经验总结
- 失败教训记录

---

**版本**：V4.0  
**最后更新**：2026-04-26  
**适用项目**：ai-daily-report-V4-0426
