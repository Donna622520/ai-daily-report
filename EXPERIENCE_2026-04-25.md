# AI 日报推送失败问题复盘

## 📅 问题时间
2026-04-25 09:00

## 🚨 问题现象
- Cron 任务正常执行（09:00:17）
- 日报已生成并推送到 GitHub
- **但飞书通知显示"新闻数量：0"**
- 用户未收到有效日报推送

## 🔍 根本原因

### 1. 验证规则过于严格
**问题代码**（verifier.py 第 61-63 行）：
```python
if not self.verify_date(article.get('date', '')):
    logger.warning(f"日期验证失败：{article['title']}")
    continue  # 直接跳过
```

**影响**：
- 所有无明确日期的新闻都被过滤
- 实际采集的 12 条新闻中，10 条因"日期验证失败"被过滤
- 最终剩余 2 条，但验证器返回 0 条

### 2. 爬虫反爬机制
**失败数据源**：
- GitHub Trending: SSL 错误（反爬拦截）
- OpenAI Blog: 403 Forbidden
- Product Hunt: Cloudflare 防护

**成功数据源**：
- GitHub（部分）
- 智谱博客
- 通义千问博客

### 3. 新闻内容质量问题
**被过滤的新闻示例**：
- "Tim Cook is stepping down" - 明显谣言
- "Google to invest up to $40B in Anthropic" - 无日期
- "Meta's loss is Thinking Machines' gain" - 无日期

## ✅ 解决方案

### 方案 1: 放宽验证规则（已实施）
**修改内容**：
1. 允许无明确日期的新闻通过
2. 只过滤明显谣言（stepping down/resign/quit）
3. 为无日期新闻添加默认日期（今天）

**修改代码**：
```python
# 放宽验证规则：允许无明确日期的新闻
# 只过滤明显谣言（如"Tim Cook 卸任"）
title = article['title'].lower()
if 'stepping down' in title or 'resign' in title or 'quit' in title:
    logger.warning(f"过滤明显谣言：{article['title']}")
    continue

# 日期验证失败但标题正常，仍然保留
if not self.verify_date(date):
    logger.info(f"日期验证失败，但保留新闻：{article['title']}")
    # 添加默认日期（今天）
    article['date'] = datetime.now().strftime('%Y-%m-%d')
```

### 方案 2: 手动生成日报（临时方案）
**已执行**：
- 手动生成 `v3_2026-04-25_manual.html`
- 发送飞书通知
- 提交到 GitHub

### 方案 3: 优化爬虫数据源（待实施）
**计划**：
1. 增加备用数据源（Hacker News、Hugging Face Blog）
2. 实现重试机制（失败后重试 3 次）
3. 使用代理绕过反爬

## 📊 修复效果

**修复前**：
- 采集 12 条 → 验证 0 条 → 推送 0 条

**修复后**（预期）：
- 采集 12 条 → 验证 8-10 条 → 推送 8-10 条

## 🔄 后续优化

### 短期（本周）
- [x] 放宽验证规则
- [x] 手动生成今日日报
- [ ] 增加备用数据源
- [ ] 实现爬虫重试机制

### 中期（本月）
- [ ] 优化反爬处理（代理、User-Agent 轮换）
- [ ] 增加数据源多样性
- [ ] 实现新闻质量评分

### 长期（下月）
- [ ] 引入 AI 新闻真实性检测
- [ ] 建立新闻来源信誉评分
- [ ] 实现多语言支持

## 📝 经验总结

### 1. 验证规则设计原则
- **宁宽勿严**：宁可保留少量假新闻，不可过滤所有新闻
- **事后验证**：先采集，后验证，再过滤
- **人工介入**：发现异常时手动生成日报

### 2. 爬虫反爬处理
- **多数据源**：避免单点失败
- **重试机制**：失败后自动重试
- **备用方案**：手动采集 + 自动生成

### 3. 监控告警
- **日志监控**：定期检查日志中的警告
- **数量告警**：新闻数量 < 3 时发送告警
- **手动兜底**：自动失败时人工介入

## 📌 相关文档
- 修复提交：`git log --oneline | head -5`
- 验证规则：`src/crawler/verifier.py`
- 手动日报：`archive/2026-04/v3_2026-04-25_manual.html`
