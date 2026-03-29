#!/bin/bash

echo "========================================"
echo "  MeowParser - 喵语解析器"
echo "========================================"
echo ""
echo "正在启动..."
echo ""

# 检查是否有 root 权限
if [ "$EUID" -ne 0 ]; then
    echo "错误: 需要 root 权限运行（用于键盘监听）"
    echo "请使用: sudo ./run.sh"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 运行程序
python3 meow_parser.py

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败！请检查："
    echo "1. 是否已安装依赖: pip3 install -r requirements_pyqt6.txt"
    echo "2. 是否已安装系统依赖: xdotool, wmctrl"
    echo ""
    read -p "按任意键退出..."
fi
