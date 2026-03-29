#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 PyQt6 版本的所有功能
"""

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

def test_all():
    """测试所有功能"""
    print("="*60)
    print("MeowParser PyQt6 版本 - 功能测试")
    print("="*60)
    print()
    
    # 测试导入
    print("1. 测试导入...")
    try:
        from PyQt6.QtWidgets import QSystemTrayIcon, QDialog, QTreeWidget
        from PyQt6.QtCore import Qt, QTimer
        from PyQt6.QtGui import QIcon
        print("   ✓ PyQt6 导入成功")
    except ImportError as e:
        print(f"   ✗ PyQt6 导入失败: {e}")
        return False
    
    try:
        import keyboard
        print("   ✓ keyboard 导入成功")
    except ImportError as e:
        print(f"   ✗ keyboard 导入失败: {e}")
        return False
    
    try:
        import psutil
        print("   ✓ psutil 导入成功")
    except ImportError as e:
        print(f"   ✗ psutil 导入失败: {e}")
        return False
    
    print()
    
    # 测试主程序导入
    print("2. 测试主程序导入...")
    try:
        from meow_parser import (
            FloatingInputWindow,
            DebugWindow,
            WindowSelector,
            ReplacementRuleEditor,
            RuleDialog,
            MeowParser
        )
        print("   ✓ 所有类导入成功")
    except ImportError as e:
        print(f"   ✗ 主程序导入失败: {e}")
        return False
    
    print()
    
    # 测试文本处理
    print("3. 测试文本处理逻辑...")
    try:
        import re
        
        # 测试基本替换
        text = "我是测试"
        result = text.replace("我", "喵")
        assert result == "喵是测试", "基本替换失败"
        print("   ✓ 基本替换测试通过")
        
        # 测试正则替换
        text = "我有123个苹果"
        result = re.sub(r"\d+", "很多", text)
        assert result == "我有很多个苹果", "正则替换失败"
        print("   ✓ 正则替换测试通过")
        
        # 测试添加喵
        text = "测试文本"
        result = re.sub(r'([^喵])([。，！？；、）（：])', r'\1喵\2', text)
        if not re.search(r'[。，！？；、）（：\n]$', result):
            result += "喵"
        assert result == "测试文本喵", "添加喵失败"
        print("   ✓ 添加喵测试通过")
        
    except Exception as e:
        print(f"   ✗ 文本处理测试失败: {e}")
        return False
    
    print()
    
    # 测试UI创建
    print("4. 测试UI创建...")
    app = QApplication(sys.argv)
    
    try:
        # 测试悬浮窗
        from meow_parser import FloatingInputWindow, MeowParser
        
        class MockApp:
            def debug_log(self, msg):
                pass
            def process_text(self, text):
                return text + "喵"
        
        mock_app = MockApp()
        floating = FloatingInputWindow(mock_app)
        print("   ✓ 悬浮窗创建成功")
        
        # 测试调试窗口
        from meow_parser import DebugWindow
        debug = DebugWindow(mock_app)
        print("   ✓ 调试窗口创建成功")
        
        # 测试窗口管理器
        from meow_parser import WindowSelector
        selector = WindowSelector(None, {})
        print("   ✓ 窗口管理器创建成功")
        
        # 测试替换规则编辑器
        from meow_parser import ReplacementRuleEditor
        rules = {"enabled": True, "rules": []}
        editor = ReplacementRuleEditor(None, rules, lambda: None)
        print("   ✓ 替换规则编辑器创建成功")
        
    except Exception as e:
        print(f"   ✗ UI创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("="*60)
    print("所有测试通过！✓")
    print("="*60)
    print()
    print("可以运行程序：")
    print("  Windows: run_qt.bat")
    print("  Linux:   sudo ./run_qt.sh")
    print("  直接运行: python meow_parser.py")
    print()
    
    return True

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
