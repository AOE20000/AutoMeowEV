#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试窗口枚举功能
"""

import sys
import psutil

IS_WINDOWS = sys.platform == 'win32'

if IS_WINDOWS:
    import win32gui
    import win32process

def test_windows_enum():
    """测试 Windows 窗口枚举"""
    print("=== 测试 Windows 窗口枚举 ===\n")
    
    window_count = 0
    
    def enum_callback(hwnd, _):
        nonlocal window_count
        try:
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and len(title.strip()) > 0:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    try:
                        process_name = psutil.Process(pid).name()
                    except:
                        process_name = "Unknown"
                    
                    window_count += 1
                    print(f"{window_count}. [{process_name}] {title}")
        except Exception as e:
            print(f"错误: {e}")
        return True
    
    try:
        win32gui.EnumWindows(enum_callback, None)
        print(f"\n总共找到 {window_count} 个窗口")
    except Exception as e:
        print(f"枚举失败: {e}")

def test_linux_enum():
    """测试 Linux 窗口枚举"""
    print("=== 测试 Linux 窗口枚举 ===\n")
    
    try:
        import subprocess
        
        # 测试 wmctrl
        print("测试 wmctrl...")
        result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print(f"找到 {len(lines)} 个窗口:\n")
            for i, line in enumerate(lines, 1):
                parts = line.split(None, 3)
                if len(parts) >= 4:
                    window_id = parts[0]
                    title = parts[3]
                    
                    # 尝试获取进程名
                    try:
                        pid_result = subprocess.run(['xdotool', 'getwindowpid', window_id],
                                                  capture_output=True, text=True, timeout=1)
                        if pid_result.returncode == 0:
                            pid = int(pid_result.stdout.strip())
                            process_name = psutil.Process(pid).name()
                        else:
                            process_name = "Unknown"
                    except:
                        process_name = "Unknown"
                    
                    print(f"{i}. [{process_name}] {title}")
        else:
            print(f"wmctrl 失败: {result.stderr}")
    except FileNotFoundError:
        print("错误: wmctrl 未安装")
        print("请运行: sudo apt-get install wmctrl")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    print("窗口枚举测试工具\n")
    
    if IS_WINDOWS:
        test_windows_enum()
    else:
        test_linux_enum()
    
    print("\n测试完成！")
