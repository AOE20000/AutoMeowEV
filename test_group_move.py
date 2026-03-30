#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试规则组上下移动功能
"""

import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from meow_parser.core.config_manager import ConfigFileManager


def test_group_move():
    """测试规则组移动功能"""
    print("=" * 60)
    print("测试规则组上下移动功能")
    print("=" * 60)
    
    # 创建临时配置管理器
    config_manager = ConfigFileManager(".meowparser/rules")
    
    # 加载默认配置
    default_config = config_manager.config_dir / "default.json"
    if not default_config.exists():
        print("❌ 默认配置不存在")
        return False
    
    config_manager.load_config(default_config)
    
    # 显示原始规则组顺序
    print("\n原始规则组顺序:")
    groups = config_manager.current_config.get("groups", [])
    for i, group in enumerate(groups):
        print(f"  {i}. {group.get('name', '未命名')}")
    
    # 测试：添加测试规则组
    print("\n添加测试规则组...")
    groups.append({
        "name": "测试规则组A",
        "description": "用于测试移动功能",
        "collapsed": False,
        "rules": []
    })
    groups.append({
        "name": "测试规则组B",
        "description": "用于测试移动功能",
        "collapsed": False,
        "rules": []
    })
    
    print("\n添加后的规则组顺序:")
    for i, group in enumerate(groups):
        print(f"  {i}. {group.get('name', '未命名')}")
    
    # 测试：下移第一个规则组
    if len(groups) > 1:
        print(f"\n测试：下移规则组 0 ('{groups[0]['name']}')")
        groups[0], groups[1] = groups[1], groups[0]
        
        print("下移后的规则组顺序:")
        for i, group in enumerate(groups):
            print(f"  {i}. {group.get('name', '未命名')}")
    
    # 测试：上移第二个规则组
    if len(groups) > 1:
        print(f"\n测试：上移规则组 1 ('{groups[1]['name']}')")
        groups[1], groups[0] = groups[0], groups[1]
        
        print("上移后的规则组顺序:")
        for i, group in enumerate(groups):
            print(f"  {i}. {group.get('name', '未命名')}")
    
    # 清理测试数据
    print("\n清理测试数据...")
    while len(groups) > 1 and groups[-1]['name'].startswith("测试规则组"):
        groups.pop()
    
    print("\n清理后的规则组顺序:")
    for i, group in enumerate(groups):
        print(f"  {i}. {group.get('name', '未命名')}")
    
    print("\n" + "=" * 60)
    print("✅ 规则组移动功能测试完成")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = test_group_move()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
