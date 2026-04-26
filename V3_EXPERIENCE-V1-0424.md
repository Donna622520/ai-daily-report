# AI 日报 V3 经验总结 - 分段生成最佳实践

## 问题背景

**问题**: 一次性生成完整 HTML 并输出到终端会导致输出截断

**错误做法**:
- 在 Python 脚本中直接 print 完整 HTML
- 使用 `echo` 一次性输出所有内容
- 尝试在内存中构建完整文档后发送

**正确做法**:
1. 使用 `cat >> file.html` 分段追加到文件
2. 所有操作在文件层面完成，不输出完整 HTML 到终端
3. 飞书通知只包含链接和摘要，完整内容通过链接查看

## V3 版最佳实践 (2026-04-24 更新)

### 步骤 1: 创建 HTML 骨架

```bash
cat > /tmp/daily_header.html << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>AI 日报 - V3</title>
    <!-- CSS 样式 -->
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 日报</h1>
            <div class="date">2026-04-24 V3</div>
        </div>
        <div class="content">
EOF
```

### 步骤 2: 分段添加板块内容

每次只添加 1-2 个板块，避免单次输出过长：

```bash
# 板块 1-2: 今日要闻 + 大模型动态
cat >> /tmp/daily_header.html << 'EOF'
            <div class="section">
                <h2 class="section-title">🔥 今日要闻</h2>
                <div class="no-news">...</div>
            </div>
            <div class="section">
                <h2 class="section-title">🤖 大模型动态</h2>
                <div class="article">...</div>
            </div>
EOF

# 板块 3-4: GitHub Trending + 科技媒体
cat >> /tmp/daily_header.html << 'EOF'
            <div class="section">
                <h2 class="section-title">📊 GitHub Trending AI</h2>
                <div class="article">...</div>
            </div>
            <div class="section">
                <h2 class="section-title">📰 科技媒体精选</h2>
                <div class="article">...</div>
            </div>
EOF

# 板块 5-6: 社区热议 + 学术前沿
cat >> /tmp/daily_header.html << 'EOF'
            <div class="section">
                <h2 class="section-title">💬 社区热议</h2>
                <div class="article">...</div>
            </div>
            <div class="section">
                <h2 class="section-title">🎓 学术前沿</h2>
                <div class="article">...</div>
            </div>
EOF
```

### 步骤 3: 添加 HTML 尾部

```bash
cat >> /tmp/daily_header.html << 'EOF'
        </div>
        <div class="footer">
            <p>AI 日报 V3 - 每日自动生成 | <a href="https://github.com/Donna622520/ai-daily-report" target="_blank">GitHub</a></p>
        </div>
    </div>
</body>
</html>
EOF
```

### 步骤 4: 移动文件并更新

```bash
mv /tmp/daily_header.html archive/2026-04/v3_2026-04-24.html
sed -i 's/v2_2026-04-24.html/v3_2026-04-24.html/g' index.html
```

### 步骤 5: 发送通知（只发送摘要）

```bash
send_message(
    message="🤖 AI 日报 V3 - 2026-04-24\n\n✅ 生成完成，包含 6 个板块\n📄 日报链接：[查看完整日报](archive/2026-04/v3_2026-04-24.html)",
    target="feishu:oc_f4e9efc6365614e5bbb4aae76014bc90"
)
```

## 关键要点

1. **文件层面操作**: 所有 HTML 生成在文件层面完成，不输出到终端
2. **分段追加**: 每次只添加 1-2 个板块，避免单次输出过长
3. **飞书通知**: 只包含链接和摘要，完整内容通过链接查看
4. **追加模式**: 使用 `cat >>` 追加模式，避免覆盖已写入内容
5. **版本追踪**: V3 版使用 `v3_YYYY-MM-DD.html` 命名，V2 版保留为 `v2_YYYY-MM-DD.html`

## 技术原理

- **large-document-writing 策略**: 通过分段写入文件，避免单次输出超过终端限制
- **search-automation 三遍规则**: 爬虫尝试 3 次无效即停止，切换手动采集
- **飞书 Markdown 格式**: 使用 `[显示文本](URL)` 格式，而非纯文本 URL

## 适用场景

- 任何需要生成长文档的场景
- 输出内容超过终端限制时
- 需要分阶段构建复杂结构时

## 相关技能

- `large-document-writing`: 长文档分段生成策略
- `search-automation`: 搜索三遍规则
- `ai-daily-report`: AI 日报自动化系统

## 版本历史

- **2026-04-24**: V3 版发布，6 个板块结构 + 分段生成最佳实践
- **2026-04-24**: 更新经验总结，明确"文件层面操作"原则

---

**总结**: 分段生成不是"分段输出"，而是"分段写入文件"。所有操作在文件层面完成，只发送摘要到飞书，完整内容通过链接查看。
