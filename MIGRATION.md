# 迁移指南：从 tkinter 到 PyQt6

本文档说明如何从旧的 tkinter 版本（v1.x）迁移到 PyQt6 版本（v2.x）。

> **注意**: tkinter 版本已停止维护，建议所有用户迁移到 PyQt6 版本。

## 为什么迁移？

PyQt6 版本提供了以下优势：

1. **跨平台支持** - Windows、Linux、macOS 全平台支持
2. **更好的焦点管理** - 解决了 tkinter 版本的焦点问题
3. **现代化 UI** - 使用暗色主题，界面更美观
4. **更稳定** - 更少的崩溃和卡死问题
5. **持续维护** - PyQt6 是唯一维护的版本

## 配置文件兼容性

好消息！配置文件完全兼容：

- `window_settings.json` - 窗口白名单设置
- `replacement_rules.json` - 文本替换规则

你可以直接使用现有的配置文件，无需任何修改。

## 迁移步骤

1. **卸载旧版本（如果已安装）**

   ```bash
   # 停止运行旧版本
   # 可选：备份配置文件
   copy window_settings.json window_settings.json.bak
   copy replacement_rules.json replacement_rules.json.bak
   ```

2. **安装 PyQt6 依赖**

   ```bash
   pip install -r requirements_pyqt6.txt
   ```

3. **测试环境**

   ```bash
   python test_qt_version.py
   ```

4. **运行 PyQt6 版本**

   Windows:
   ```bash
   # 双击运行
   run_qt.bat
   
   # 或命令行
   python meow_parser.py
   ```

   Linux:
   ```bash
   chmod +x run_qt.sh
   sudo ./run_qt.sh
   ```

5. **验证功能**

   - 检查系统托盘图标是否正常显示
   - 测试窗口管理功能
   - 测试替换规则功能
   - 测试悬浮窗输入

6. **清理旧文件（可选）**

   如果确认 PyQt6 版本工作正常，旧文件已被移除：
   - `auto_meow_ev.py` (已删除，旧版本)
   - `auto_meow_ev.spec` (已删除，旧版本)
   - `requirements.txt` (已删除)

## 功能对比

| 功能 | tkinter 版本 (v1.x) | PyQt6 版本 (v2.x) |
|------|---------------------|-------------------|
| 平台支持 | Windows | Windows/Linux/macOS |
| 悬浮输入窗口 | ✓ | ✓ |
| 文本替换 | ✓ | ✓ |
| 正则表达式 | ✓ | ✓ |
| 窗口白名单 | ✓ | ✓ |
| 系统托盘 | ✓ | ✓ |
| 调试窗口 | ✓ | ✓ |
| 焦点管理 | 一般 | 优秀 |
| UI 风格 | 系统默认 | 暗色主题 |
| 稳定性 | 一般 | 优秀 |
| 维护状态 | 已停止 | 活跃维护 |

## 常见问题

### Q: 旧版本的配置会丢失吗？

A: 不会。PyQt6 版本完全兼容旧版本的配置文件。

### Q: 可以回退到 tkinter 版本吗？

A: 不建议。tkinter 版本已停止维护，且存在已知问题。如果确实需要，可以从 Git 历史中恢复旧文件。

### Q: PyQt6 版本有什么改进？

A: 主要改进包括：
- 更好的焦点管理和窗口激活
- 跨平台支持（Linux/macOS）
- 更稳定的悬浮窗显示
- 改进的窗口枚举性能（避免死锁）
- 现代化暗色主题 UI
- 更好的线程安全性

### Q: Linux 下需要额外安装什么？

A: 需要安装 `xdotool` 和 `wmctrl` 用于窗口管理：
```bash
# Ubuntu/Debian
sudo apt-get install xdotool wmctrl

# Fedora
sudo dnf install xdotool wmctrl

# Arch Linux
sudo pacman -S xdotool wmctrl
```

## 获取帮助

如果遇到问题：
1. 查看 [README.md](README.md) 了解详细功能
2. 查看 [QUICKSTART.md](QUICKSTART.md) 快速开始
3. 提交 Issue 报告问题

## 贡献

欢迎提交 PR 帮助完善 PyQt6 版本！

特别需要：
- macOS 测试和优化
- UI 美化和优化
- 文档改进
