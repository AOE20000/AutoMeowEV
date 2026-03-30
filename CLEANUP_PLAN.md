# 代码清理计划

## 清理日期
2026-03-30

---

## 发现的问题

### 1. 旧版规则编辑器 ⚠️

**文件：** `meow_parser/ui/rule_editor.py`

**状态：** 已被 `config_editor.py` 替代，但仍在代码库中

**使用情况：**
- ❌ 主应用不使用
- ❌ 只在 `__init__.py` 中导出
- ❌ 无实际引用

**建议：** 保留作为备用（已标记为旧版）

**原因：**
- 提供不同的 UI 风格选择
- 可能有用户习惯旧版界面
- 作为参考实现

### 2. 导出冗余 ⚠️

**文件：** `meow_parser/ui/__init__.py`

**问题：**
- 同时导出 `ConfigFileEditor` 和 `ReplacementRuleEditor`
- 同时导出 `RuleEditDialog` 和 `RuleDialog`

**实际使用：**
- ✅ `ConfigFileEditor` - 主应用使用
- ❌ `ReplacementRuleEditor` - 未使用
- ✅ `RuleEditDialog` - ConfigFileEditor 使用
- ❌ `RuleDialog` - 未使用

**建议：** 保留导出，但添加注释说明

---

## 清理建议

### 方案 A：完全移除（激进）

**移除文件：**
- `meow_parser/ui/rule_editor.py`

**修改文件：**
- `meow_parser/ui/__init__.py` - 移除相关导出

**优点：**
- 代码库更简洁
- 减少维护负担
- 避免混淆

**缺点：**
- 失去备用方案
- 可能影响依赖此文件的外部代码
- 无法回退

### 方案 B：标记为废弃（保守）✓ 推荐

**保留文件：**
- `meow_parser/ui/rule_editor.py` - 添加废弃警告

**修改文件：**
- `meow_parser/ui/__init__.py` - 添加注释说明
- `meow_parser/ui/rule_editor.py` - 添加废弃警告

**优点：**
- 保持向后兼容
- 提供迁移缓冲期
- 可以随时回退

**缺点：**
- 代码库稍大
- 需要维护文档

---

## 实施方案（方案 B）

### 1. 标记旧版编辑器

在 `rule_editor.py` 顶部添加：

```python
"""
旧版规则编辑器模块（已废弃）

警告：此模块已被 config_editor.py 替代，仅保留用于向后兼容。
新项目请使用 ConfigFileEditor。

迁移指南：
- ReplacementRuleEditor → ConfigFileEditor
- RuleDialog → RuleEditDialog
"""
```

### 2. 更新导出注释

在 `__init__.py` 中添加：

```python
# 新版编辑器（推荐）
from .config_editor import ConfigFileEditor, RuleEditDialog

# 旧版编辑器（已废弃，仅用于兼容）
from .rule_editor import ReplacementRuleEditor, RuleDialog
```

### 3. 更新文档

在 README.md 中说明：
- 推荐使用 ConfigFileEditor
- ReplacementRuleEditor 已废弃

---

## 其他发现

### 配置格式演进

**旧格式（rule_editor.py）：**
```json
{
  "groups": {
    "规则组名": {
      "enabled": true,
      "rules": [...]
    }
  }
}
```

**新格式（config_editor.py）：**
```json
{
  "name": "配置名",
  "groups": [
    {
      "name": "规则组名",
      "rules": [...]
    }
  ]
}
```

**兼容性：**
- ✅ ConfigFileManager 支持迁移旧格式
- ✅ 自动转换为新格式

---

## 测试验证

### 需要测试的功能

1. **ConfigFileEditor**
   - ✅ 创建配置
   - ✅ 添加规则组
   - ✅ 添加规则
   - ✅ 编辑规则
   - ✅ 删除规则
   - ✅ 移动规则
   - ✅ 删除规则组
   - ✅ 导入导出

2. **向后兼容**
   - ✅ 加载旧格式配置
   - ✅ 自动迁移
   - ✅ 保存为新格式

3. **ReplacementRuleEditor（如果保留）**
   - ⚠️ 基本功能可用
   - ⚠️ 不推荐使用

---

## 清理时间表

### 立即执行
- ✅ 修复 test_config_editor.py 导入错误
- ✅ 添加废弃警告到 rule_editor.py
- ✅ 更新 __init__.py 注释

### 短期（v2.3）
- [ ] 更新文档说明
- [ ] 添加迁移指南
- [ ] 通知用户废弃信息

### 中期（v2.4）
- [ ] 评估是否有用户使用旧版
- [ ] 决定是否完全移除

### 长期（v3.0）
- [ ] 完全移除旧版编辑器
- [ ] 清理相关代码

---

## 风险评估

### 低风险
- ✅ 添加注释和警告
- ✅ 保留旧代码
- ✅ 向后兼容

### 中风险
- ⚠️ 移除导出
- ⚠️ 修改 API

### 高风险
- ❌ 删除文件
- ❌ 破坏兼容性

---

## 建议

### 当前阶段（v2.2.1）
1. ✅ 保留 rule_editor.py
2. ✅ 添加废弃警告
3. ✅ 更新文档
4. ✅ 修复测试脚本

### 未来版本
1. 收集用户反馈
2. 评估使用情况
3. 逐步淘汰旧版
4. 最终移除

---

## 总结

**当前状态：**
- 代码功能完整
- 存在冗余但无害
- 向后兼容良好

**推荐行动：**
- 采用方案 B（标记废弃）
- 保持向后兼容
- 逐步迁移

**不推荐：**
- 立即删除旧代码
- 破坏向后兼容
- 强制迁移

---

**结论：** 当前代码状态良好，建议保留旧版作为备用，添加适当的警告和文档说明即可。
