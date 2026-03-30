#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置编辑器功能测试
"""

import sys
from PyQt6.QtWidgets import QApplication
from meow_parser.core.config_manager import ConfigFileManager
from meow_parser.ui.config_editor import ConfigFileEditor


def main():
    """测试配置编辑器"""
    app = QApplication(sys.argv)
    
    # 创建配置管理器
    config_manager = ConfigFileManager()
    
    # 创建编辑器
    editor = ConfigFileEditor(None, config_manager, lambda: print("配置已保存"))
    editor.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
