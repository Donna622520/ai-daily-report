# 版本号管理规范

## 📋 概述
AI 日报项目的版本号统一管理规范，避免硬编码导致的版本不一致问题。

## 🎯 设计原则

### 1. 单一数据源
- **版本号只在 `config.yaml` 中定义**
- 所有模块从配置文件读取版本号
- 禁止在任何代码中硬编码版本号

### 2. 动态提取
- 飞书通知从文件名动态提取版本号
- 使用正则表达式 `v(\d+)` 匹配
- 默认值为 `v3`（如果提取失败）

### 3. 自动验证
- 生成后验证文件名与配置一致
- 不一致时抛出异常，阻止流程继续
- 记录验证日志

## 📁 文件结构

### config.yaml
```yaml
version:
  number: "v3"  # 版本号
  changelog: "6 个板块结构，优化验证规则"
```

### src/generator/report.py
```python
# 从配置读取版本号
import yaml
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
version = config.get('version', {}).get('number', 'v3')

# 生成文件名
filename = f"{version}_{date}.html"
```

### src/notifier/feishu.py
```python
# 从文件名提取版本号
import re
version_match = re.search(r'v(\d+)', report_path)
version = version_match.group(1) if version_match else '3'

# 使用版本号
message = f"🤖 **AI 日报 V{version} 已生成**"
```

### run.sh
```python
# 验证版本号一致性
expected_filename = f"{version}_{date}.html"
actual_filename = os.path.basename(report_path)
if expected_filename != actual_filename:
    raise ValueError(f"版本号验证失败")
```

## 🔄 版本号升级流程

### 步骤 1: 更新 config.yaml
```yaml
version:
  number: "v4"
  changelog: "新增功能描述"
```

### 步骤 2: 测试验证
```bash
# 手动运行脚本
python3 -c "..."

# 检查生成的文件名
ls -la archive/2026-04/
# 应该看到：v4_2026-04-25.html
```

### 步骤 3: 提交代码
```bash
git add config.yaml src/ run.sh
git commit -m "feat: 升级到 V4 版本"
git push
```

## ✅ 验证清单

- [ ] `config.yaml` 中定义了版本号
- [ ] `report.py` 从配置读取版本号
- [ ] `feishu.py` 从文件名动态提取版本号
- [ ] `run.sh` 验证版本号一致性
- [ ] 生成的文件名与配置一致
- [ ] 飞书通知显示正确的版本号

## 🚫 禁止事项

- ❌ 禁止在代码中硬编码版本号（如 `v2_`、`v3_`）
- ❌ 禁止在多个地方定义版本号
- ❌ 禁止手动修改生成的文件名
- ❌ 禁止跳过版本号验证

## 📝 历史版本

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1 | 2026-04-24 | 初始版本 |
| v2 | 2026-04-24 | 测试版本 |
| v3 | 2026-04-25 | 6 个板块结构，优化验证规则 |

## 🔧 故障排查

### 问题 1: 版本号不一致
**症状**: 飞书通知显示 V3，但文件名是 v2

**原因**: 代码中硬编码了版本号

**解决**: 
1. 检查所有模块是否从 `config.yaml` 读取
2. 运行版本号验证
3. 重新生成日报

### 问题 2: 飞书通知显示 V3，但实际是 v4
**症状**: 文件名是 `v4_2026-04-25.html`，但通知显示 V3

**原因**: `feishu.py` 中硬编码了 V3

**解决**: 
1. 更新 `feishu.py` 使用正则表达式动态提取
2. 重新运行脚本

### 问题 3: 验证失败
**症状**: `ValueError: 版本号验证失败`

**原因**: 生成的文件名与配置不一致

**解决**: 
1. 检查 `config.yaml` 中的版本号
2. 检查 `report.py` 是否正确读取配置
3. 重新生成日报

## 📌 相关文档
- [SPEC_01_Intro.md](./SPEC_01_Intro.md) - 项目介绍
- [SPEC_02_Verification.md](./SPEC_02_Verification.md) - 验证规则
- [EXPERIENCE.md](./EXPERIENCE.md) - 项目经验
