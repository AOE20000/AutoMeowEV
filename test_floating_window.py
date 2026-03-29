#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试悬浮窗显示 - 简化版
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer
import qdarktheme

class SimpleFloatingWindow(QWidget):
    """简单悬浮窗"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 确保不透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        
        # 设置固定大小
        self.setFixedSize(500, 100)
        
        # 设置样式
        self.setStyleSheet("""
            SimpleFloatingWindow {
                background-color: #1e1e1e;
                border: 3px solid #0078d4;
                border-radius: 6px;
            }
        """)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 标签
        label = QLabel("悬浮窗测试")
        label.setStyleSheet("color: #ffffff; font-size: 12pt;")
        layout.addWidget(label)
        
        # 输入框
        self.entry = QLineEdit()
        self.entry.setFixedHeight(40)
        self.entry.setPlaceholderText("测试输入...")
        self.entry.setStyleSheet("""
            QLineEdit {
                background-color: #252526;
                color: #cccccc;
                border: 2px solid #3e3e42;
                border-radius: 4px;
                padding: 8px;
                font-size: 12pt;
            }
        """)
        layout.addWidget(self.entry)
        
        self.setLayout(layout)
        
        # 事件过滤器
        self.entry.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.entry:
            if event.type() == event.Type.KeyPress:
                if event.key() == Qt.Key.Key_Escape:
                    self.hide()
                    return True
        return super().eventFilter(obj, event)

class MainWindow(QWidget):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.floating_window = None
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("悬浮窗测试 - 简化版")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # 说明
        info = QLabel("点击按钮显示悬浮窗\n悬浮窗应该在屏幕中央显示\n按 ESC 关闭悬浮窗")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # 按钮
        btn1 = QPushButton("显示悬浮窗（屏幕中央）")
        btn1.clicked.connect(self.show_floating_center)
        layout.addWidget(btn1)
        
        btn2 = QPushButton("显示悬浮窗（鼠标位置）")
        btn2.clicked.connect(self.show_floating_mouse)
        layout.addWidget(btn2)
        
        btn3 = QPushButton("测试：创建新悬浮窗")
        btn3.clicked.connect(self.create_new_floating)
        layout.addWidget(btn3)
        
        # 状态标签
        self.status_label = QLabel("状态: 等待操作")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
    def show_floating_center(self):
        """在屏幕中央显示悬浮窗"""
        if self.floating_window is None:
            self.floating_window = SimpleFloatingWindow()
            print("创建新悬浮窗")
        
        # 在屏幕中央显示
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() // 2 - 250
        y = screen.height() // 2 - 50
        
        print(f"\n=== 显示悬浮窗（中央） ===")
        print(f"屏幕大小: {screen.width()}x{screen.height()}")
        print(f"目标位置: ({x}, {y})")
        
        self.floating_window.setGeometry(x, y, 500, 100)
        self.floating_window.show()
        self.floating_window.raise_()
        self.floating_window.activateWindow()
        self.floating_window.entry.setFocus()
        
        # 强制刷新
        self.floating_window.update()
        QApplication.processEvents()
        
        print(f"窗口状态:")
        print(f"  - isVisible: {self.floating_window.isVisible()}")
        print(f"  - geometry: {self.floating_window.geometry()}")
        print(f"  - windowOpacity: {self.floating_window.windowOpacity()}")
        print(f"===================\n")
        
        self.status_label.setText(f"状态: 悬浮窗已显示在 ({x}, {y})")
        
    def show_floating_mouse(self):
        """在鼠标位置显示悬浮窗"""
        if self.floating_window is None:
            self.floating_window = SimpleFloatingWindow()
        
        from PyQt6.QtGui import QCursor
        pos = QCursor.pos()
        x, y = pos.x(), pos.y()
        
        print(f"\n=== 显示悬浮窗（鼠标） ===")
        print(f"鼠标位置: ({x}, {y})")
        
        self.floating_window.setGeometry(x + 10, y + 10, 500, 100)
        self.floating_window.show()
        self.floating_window.raise_()
        self.floating_window.activateWindow()
        self.floating_window.entry.setFocus()
        
        self.status_label.setText(f"状态: 悬浮窗已显示在 ({x+10}, {y+10})")
        
    def create_new_floating(self):
        """创建新的悬浮窗实例"""
        print("\n=== 创建新悬浮窗实例 ===")
        self.floating_window = SimpleFloatingWindow()
        self.status_label.setText("状态: 已创建新悬浮窗实例")
        print("新实例已创建\n")

def main():
    app = QApplication(sys.argv)
    
    # 应用暗色主题
    print("应用 PyQtDarkTheme...")
    qdarktheme.setup_theme("auto")
    
    window = MainWindow()
    window.show()
    
    print("\n主窗口已显示")
    print("请点击按钮测试悬浮窗\n")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
