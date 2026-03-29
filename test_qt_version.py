#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 PyQt6 版本的基本功能
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

def test_imports():
    """测试导入"""
    print("测试导入...")
    try:
        from PyQt6.QtWidgets import QSystemTrayIcon
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QIcon
        print("✓ PyQt6 导入成功")
    except ImportError as e:
        print(f"✗ PyQt6 导入失败: {e}")
        return False
    
    try:
        import keyboard
        print("✓ keyboard 导入成功")
    except ImportError as e:
        print(f"✗ keyboard 导入失败: {e}")
        return False
    
    try:
        import psutil
        print("✓ psutil 导入成功")
    except ImportError as e:
        print(f"✗ psutil 导入失败: {e}")
        return False
    
    return True

def test_basic_ui():
    """测试基本UI"""
    print("\n测试基本UI...")
    app = QApplication(sys.argv)
    
    msg = QMessageBox()
    msg.setWindowTitle("MeowParser 测试")
    msg.setText("PyQt6 版本基本功能测试\n\n所有依赖已正确安装！")
    msg.setIcon(QMessageBox.Icon.Information)
    msg.exec()
    
    print("✓ UI 测试成功")

if __name__ == "__main__":
    if test_imports():
        test_basic_ui()
        print("\n所有测试通过！可以运行 meow_parser.py")
    else:
        print("\n请先安装依赖：pip install -r requirements_pyqt6.txt")
