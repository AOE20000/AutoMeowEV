#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的悬浮窗测试 - 不使用任何主题
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class MinimalFloatingWindow(QWidget):
    """最小化悬浮窗"""
    
    def __init__(self):
        super().__init__()
        
        # 窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 固定大小
        self.setFixedSize(500, 80)
        
        # 简单样式 - 白色背景，红色边框
        self.setStyleSheet("""
            MinimalFloatingWindow {
                background-color: white;
                border: 5px solid red;
            }
            QLineEdit {
                background-color: yellow;
                color: black;
                border: 2px solid blue;
                padding: 10px;
                font-size: 16pt;
            }
        """)
        
        # 布局
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 输入框
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("测试输入 - 按ESC关闭")
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        # 事件过滤
        self.entry.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.entry:
            if event.type() == event.Type.KeyPress:
                if event.key() == Qt.Key.Key_Escape:
                    self.hide()
                    return True
        return super().eventFilter(obj, event)

class TestWindow(QWidget):
    """测试主窗口"""
    
    def __init__(self):
        super().__init__()
        self.floating = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("最简单悬浮窗测试")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        btn = QPushButton("显示悬浮窗（屏幕中央）")
        btn.clicked.connect(self.show_floating)
        layout.addWidget(btn)
        
        self.setLayout(layout)
        
    def show_floating(self):
        if self.floating is None:
            self.floating = MinimalFloatingWindow()
            print("创建悬浮窗")
        
        # 屏幕中央
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() // 2 - 250
        y = screen.height() // 2 - 40
        
        print(f"\n显示悬浮窗: ({x}, {y})")
        
        # 先隐藏
        if self.floating.isVisible():
            self.floating.hide()
            QApplication.processEvents()
        
        # 设置位置
        self.floating.setGeometry(x, y, 500, 80)
        
        # 显示
        self.floating.show()
        
        # 强制刷新
        for _ in range(5):
            self.floating.update()
            self.floating.repaint()
            QApplication.processEvents()
        
        # 提升
        self.floating.raise_()
        self.floating.activateWindow()
        self.floating.entry.setFocus()
        
        print(f"窗口状态:")
        print(f"  isVisible: {self.floating.isVisible()}")
        print(f"  geometry: {self.floating.geometry()}")
        print(f"  windowOpacity: {self.floating.windowOpacity()}")
        print(f"  windowHandle: {self.floating.windowHandle()}")
        if self.floating.windowHandle():
            print(f"  isExposed: {self.floating.windowHandle().isExposed()}")
        print()

def main():
    app = QApplication(sys.argv)
    
    # 不使用任何主题
    print("不使用主题，使用系统默认样式")
    
    window = TestWindow()
    window.show()
    
    print("\n主窗口已显示")
    print("点击按钮测试悬浮窗")
    print("悬浮窗应该有：")
    print("  - 白色背景")
    print("  - 红色边框（5px）")
    print("  - 黄色输入框")
    print("  - 蓝色输入框边框\n")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
