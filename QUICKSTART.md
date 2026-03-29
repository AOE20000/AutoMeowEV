# 快速开始指南

## Windows

1. **安装依赖**
   ```bash
   pip install -r requirements_pyqt6.txt
   ```

2. **测试环境**
   ```bash
   python test_qt_version.py
   ```

3. **运行程序**
   - 双击 `run.bat`
   - 或右键 → 以管理员身份运行

## Linux

1. **安装系统依赖**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-pyqt6 python3-pip
   
   # Fedora
   sudo dnf install python3-qt6 python3-pip
   
   # Arch Linux
   sudo pacman -S python-pyqt6 python-pip
   ```

2. **安装 Python 依赖**
   ```bash
   pip3 install -r requirements_pyqt6.txt
   ```

3. **运行程序**
   ```bash
   chmod +x run.sh
   sudo ./run.sh
   ```

## macOS

1. **安装依赖**
   ```bash
   pip3 install -r requirements_pyqt6.txt
   ```

2. **运行程序**
   ```bash
   sudo python3 meow_parser.py
   ```

## 首次使用

1. 程序启动后会在系统托盘显示"喵"字图标
2. 图标颜色：
   - 🔴 红色 = 禁用
   - 🟢 绿色 = 启用
3. 右键点击图标可以：
   - 启用/禁用功能
   - 打开窗口管理
   - 配置替换规则
   - 查看调试信息

## 基本使用

1. 右键托盘图标 → 启用/禁用
2. 在任意输入框中输入文字
3. 按空格键触发悬浮窗
4. 在悬浮窗中输入内容
5. 按回车发送（会自动添加"喵"）

## 常见问题

### Q: 提示需要管理员权限？
A: 键盘监听需要管理员/root 权限，请以管理员身份运行。

### Q: 悬浮窗没有弹出？
A: 
1. 检查是否已启用（图标是否为绿色）
2. 检查当前窗口是否在白名单中
3. 确保先输入内容再按空格

### Q: Linux 下无法获取窗口信息？
A: 需要安装 xdotool：
```bash
sudo apt-get install xdotool  # Ubuntu/Debian
sudo dnf install xdotool       # Fedora
```

### Q: 如何添加窗口到白名单？
A: 右键托盘图标 → 窗口管理 → 双击要启用的窗口

### Q: 从旧版本迁移需要做什么？
A: 只需安装新依赖即可，配置文件完全兼容。详见 [MIGRATION.md](MIGRATION.md)

## 获取帮助

- 查看 [README.md](README.md) 了解详细功能
- 查看 [QUICKSTART.md](QUICKSTART.md) 快速开始
- 查看 [MIGRATION.md](MIGRATION.md) 了解版本差异
- 提交 Issue 报告问题
