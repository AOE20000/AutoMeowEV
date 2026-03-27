import keyboard
import time
import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
import sys
import ctypes
import ctypes.wintypes
from sys import exit
import win32gui
import win32process
import json
import os
import tkinter as tk
from tkinter import ttk
import psutil
import pyperclip
import re

def check_single_instance():
    """检查是否已有实例运行"""
    event_name = r"Global\AutoMeow_SingleInstance_Event"
    
    try:
        # 尝试创建命名事件
        event = ctypes.windll.kernel32.CreateEventW(
            None,    # 默认安全属性
            True,    # 手动重置
            False,   # 初始状态为 non-signaled
            event_name
        )
        
        if event == 0:  # 创建失败
            return False
            
        if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
            ctypes.windll.kernel32.CloseHandle(event)
            return False
            
        # 保存事件句柄供后续使用
        return event
    except:
        if 'event' in locals():
            ctypes.windll.kernel32.CloseHandle(event)
        return False

class WindowSelector:
    def __init__(self, parent, allowed_windows):
        self.window = tk.Toplevel(parent)
        self.window.title("窗口管理")
        self.window.geometry("800x600")  # 加宽窗口以适应更多信息
        self.allowed_windows = allowed_windows
        self.window_list = {}
        
        # 创建搜索框
        search_frame = ttk.Frame(self.window)
        search_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(search_frame, text="搜索窗口：").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_windows)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side='left', fill='x', expand=True)
        
        # 创建窗口列表
        self.tree = ttk.Treeview(self.window, columns=('process', 'title', 'enabled'), show='headings')
        self.tree.heading('process', text='进程名')
        self.tree.heading('title', text='窗口标题')
        self.tree.heading('enabled', text='状态')
        self.tree.column('process', width=150)
        self.tree.column('title', width=500)
        self.tree.column('enabled', width=100, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 绑定点击事件
        self.tree.bind('<Double-1>', self.toggle_window)
        
        # 添加说明标签
        ttk.Label(self.window, text="双击窗口项目可切换启用状态").pack(pady=2)
        
        # 刷新按钮
        ttk.Button(self.window, text="刷新窗口列表", command=self.refresh_windows).pack(pady=5)
        
        # 初始刷新
        self.refresh_windows()
        
    def get_process_name(self, pid):
        try:
            return psutil.Process(pid).name()
        except:
            return "未知进程"
    
    def toggle_window(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        window_key = f"{values[0]} - {values[1]}"
        if window_key in self.allowed_windows:
            del self.allowed_windows[window_key]
        else:
            self.allowed_windows[window_key] = True
        self.refresh_windows()
        
    def refresh_windows(self):
        self.tree.delete(*self.tree.get_children())
        self.window_list.clear()
        
        def enum_windows_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and len(title.strip()) > 0:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    process_name = self.get_process_name(pid)
                    window_key = f"{process_name} - {title}"
                    self.window_list[window_key] = hwnd
                    enabled = "✓ 已启用" if window_key in self.allowed_windows else "✗ 未启用"
                    self.tree.insert('', 'end', values=(process_name, title, enabled))
        
        win32gui.EnumWindows(enum_windows_callback, None)
        
    def filter_windows(self, *args):
        search_text = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for window_key, hwnd in self.window_list.items():
            if search_text in window_key.lower():
                process_name, title = window_key.split(" - ", 1)
                enabled = "✓ 已启用" if window_key in self.allowed_windows else "✗ 未启用"
                self.tree.insert('', 'end', values=(process_name, title, enabled))


class ReplacementRuleEditor:
    def __init__(self, parent, replacement_rules, save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("替换规则管理")
        self.window.geometry("700x500")
        self.replacement_rules = replacement_rules
        self.save_callback = save_callback
        
        # 启用/禁用替换功能
        control_frame = ttk.Frame(self.window)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.enabled_var = tk.BooleanVar(value=self.replacement_rules.get("enabled", True))
        ttk.Checkbutton(control_frame, text="启用文本替换功能", 
                       variable=self.enabled_var,
                       command=self.toggle_replacement).pack(side='left')
        
        # 规则列表
        list_frame = ttk.Frame(self.window)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(list_frame, text="替换规则列表（匹配到的文本将被替换）：").pack(anchor='w')
        
        # 创建表格
        self.tree = ttk.Treeview(list_frame, columns=('pattern', 'replacement'), show='headings', height=10)
        self.tree.heading('pattern', text='匹配文本')
        self.tree.heading('replacement', text='替换为')
        self.tree.column('pattern', width=300)
        self.tree.column('replacement', width=300)
        self.tree.pack(fill='both', expand=True)
        
        # 按钮区域
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="添加规则", command=self.add_rule).pack(side='left', padx=2)
        ttk.Button(button_frame, text="编辑规则", command=self.edit_rule).pack(side='left', padx=2)
        ttk.Button(button_frame, text="删除规则", command=self.delete_rule).pack(side='left', padx=2)
        ttk.Button(button_frame, text="上移", command=self.move_up).pack(side='left', padx=2)
        ttk.Button(button_frame, text="下移", command=self.move_down).pack(side='left', padx=2)
        
        # 说明文本
        info_frame = ttk.Frame(self.window)
        info_frame.pack(fill='x', padx=5, pady=5)
        info_text = "说明：按回车时，程序会扫描当前行文本，将所有匹配的词替换为指定内容。\n规则按顺序依次应用，每个规则会替换文本中所有匹配的位置。\n示例：\"我\" → \"喵\"，则\"我的\"会变成\"喵的\"。"
        ttk.Label(info_frame, text=info_text, wraplength=650, justify='left').pack()
        
        # 加载现有规则
        self.refresh_rules()
        
    def toggle_replacement(self):
        self.replacement_rules["enabled"] = self.enabled_var.get()
        self.save_callback()
        
    def refresh_rules(self):
        self.tree.delete(*self.tree.get_children())
        for rule in self.replacement_rules.get("rules", []):
            self.tree.insert('', 'end', values=(rule.get("pattern", ""), rule.get("replacement", "")))
    
    def add_rule(self):
        dialog = RuleDialog(self.window, "添加规则")
        if dialog.result:
            pattern, replacement = dialog.result
            if pattern:
                self.replacement_rules.setdefault("rules", []).append({
                    "pattern": pattern,
                    "replacement": replacement
                })
                self.refresh_rules()
                self.save_callback()
    
    def edit_rule(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        index = self.tree.index(selection[0])
        rule = self.replacement_rules["rules"][index]
        
        dialog = RuleDialog(self.window, "编辑规则", rule["pattern"], rule["replacement"])
        if dialog.result:
            pattern, replacement = dialog.result
            if pattern:
                self.replacement_rules["rules"][index] = {
                    "pattern": pattern,
                    "replacement": replacement
                }
                self.refresh_rules()
                self.save_callback()
    
    def delete_rule(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        index = self.tree.index(selection[0])
        del self.replacement_rules["rules"][index]
        self.refresh_rules()
        self.save_callback()
    
    def move_up(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        index = self.tree.index(selection[0])
        if index > 0:
            rules = self.replacement_rules["rules"]
            rules[index], rules[index-1] = rules[index-1], rules[index]
            self.refresh_rules()
            self.save_callback()
            # 重新选中移动后的项
            self.tree.selection_set(self.tree.get_children()[index-1])
    
    def move_down(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        index = self.tree.index(selection[0])
        rules = self.replacement_rules["rules"]
        if index < len(rules) - 1:
            rules[index], rules[index+1] = rules[index+1], rules[index]
            self.refresh_rules()
            self.save_callback()
            # 重新选中移动后的项
            self.tree.selection_set(self.tree.get_children()[index+1])


class RuleDialog:
    def __init__(self, parent, title, pattern="", replacement=""):
        self.result = None
        
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.transient(parent)
        dialog.grab_set()
        
        # 匹配文本
        ttk.Label(dialog, text="匹配文本：").pack(padx=10, pady=(10, 0), anchor='w')
        pattern_entry = ttk.Entry(dialog, width=60)
        pattern_entry.pack(padx=10, pady=5, fill='x')
        pattern_entry.insert(0, pattern)
        
        # 替换为
        ttk.Label(dialog, text="替换为：").pack(padx=10, pady=(10, 0), anchor='w')
        replacement_entry = ttk.Entry(dialog, width=60)
        replacement_entry.pack(padx=10, pady=5, fill='x')
        replacement_entry.insert(0, replacement)
        
        # 按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def on_ok():
            self.result = (pattern_entry.get(), replacement_entry.get())
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="确定", command=on_ok).pack(side='left', padx=5)
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side='left', padx=5)
        
        # 绑定回车键
        pattern_entry.focus()
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        dialog.wait_window()

class AutoMeow:
    def __init__(self):
        # 检查单实例
        self.event = check_single_instance()
        if not self.event:
            sys.exit(0)
            
        self.enabled = False
        self.last_time = 0
        self.icon = None
        self.is_admin = self.check_admin()
        self.allowed_windows = self.load_window_settings()
        self.replacement_rules = self.load_replacement_rules()  # 加载替换规则
        self.window_manager = None  # 添加窗口管理器引用
        self.root = None  # 添加tkinter根窗口引用
        self.setup_tray()

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def create_icon(self, color):
        image = Image.new('RGB', (32, 32), color)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("simhei.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "喵"
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        x = (32 - (right - left)) // 2
        y = (32 - (bottom - top)) // 2
        draw.text((x, y), text, font=font, fill='white')
        return image

    def load_window_settings(self):
        """加载窗口白名单设置"""
        try:
            if os.path.exists('window_settings.json'):
                with open('window_settings.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}  # 默认空白名单

    def save_window_settings(self):
        """保存窗口白名单设置"""
        try:
            with open('window_settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.allowed_windows, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_replacement_rules(self):
        """加载替换规则"""
        try:
            if os.path.exists('replacement_rules.json'):
                with open('replacement_rules.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        # 默认替换规则 - 示例：将常见词替换为"喵"
        return {
            "enabled": True,
            "rules": [
                {"pattern": "我", "replacement": "喵"},
                {"pattern": "你", "replacement": "喵"},
                {"pattern": "他", "replacement": "喵"},
                {"pattern": "她", "replacement": "喵"},
            ]
        }

    def save_replacement_rules(self):
        """保存替换规则"""
        try:
            with open('replacement_rules.json', 'w', encoding='utf-8') as f:
                json.dump(self.replacement_rules, f, ensure_ascii=False, indent=2)
        except:
            pass

    def get_active_window_info(self):
        """获取当前活动窗口信息"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            title = win32gui.GetWindowText(hwnd)
            process_name = psutil.Process(pid).name()
            window_key = f"{process_name} - {title}"
            return {'hwnd': hwnd, 'pid': pid, 'title': window_key}
        except:
            return None

    def toggle_current_window(self):
        """切换当前窗口的启用状态"""
        window = self.get_active_window_info()
        if not window:
            self.icon.notify("无法获取当前窗口信息", "错误")
            return

        title = window['title']
        if title in self.allowed_windows:
            del self.allowed_windows[title]
            self.icon.notify(f"已禁用窗口：{title}", "窗口设置")
        else:
            self.allowed_windows[title] = True
            self.icon.notify(f"已启用窗口：{title}", "窗口设置")
        
        self.save_window_settings()
        
    def toggle(self, *args):
        if not self.is_admin:
            self.icon.notify("需要管理员权限才能使用此功能", "权限不足")
            return

        self.enabled = not self.enabled
        if self.icon:
            color = 'green' if self.enabled else 'red'
            self.icon.icon = self.create_icon(color)
            self.icon.title = f"AutoMeow ({'启用' if self.enabled else '禁用'})"
            
            if not self.enabled:
                keyboard.unhook_all()
            else:
                keyboard.on_press_key("enter", self.on_enter, suppress=True)
    
    def show_window_manager(self, *args):
        """显示窗口管理器"""
        if self.window_manager is not None:
            # 如果窗口管理器已经打开，将其提到前台
            self.window_manager.window.lift()
            return
            
        self.root = tk.Tk()
        self.root.withdraw()
        self.window_manager = WindowSelector(self.root, self.allowed_windows)
        
        def on_closing():
            self.save_window_settings()
            self.window_manager.window.destroy()
            self.root.quit()
            self.window_manager = None
            self.root = None
            
        self.window_manager.window.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()
    
    def show_replacement_editor(self, *args):
        """显示替换规则编辑器"""
        root = tk.Tk()
        root.withdraw()
        editor = ReplacementRuleEditor(root, self.replacement_rules, self.save_replacement_rules)
        
        def on_closing():
            editor.window.destroy()
            root.quit()
            
        editor.window.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    
    def setup_tray(self):
        menu = pystray.Menu(
            pystray.MenuItem("启用/禁用", self.toggle),
            pystray.MenuItem("窗口管理", self.show_window_manager),
            pystray.MenuItem("替换规则", self.show_replacement_editor),
            pystray.MenuItem(
                f"权限状态: {'✓ 管理员' if self.is_admin else '✗ 普通用户'}",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem("退出", self.quit_app)
        )
        self.icon = pystray.Icon("AutoMeow", 
                                self.create_icon('red'),
                                "AutoMeow (禁用)", 
                                menu)

    def quit_app(self, *args):
        """确保程序退出时清理所有资源"""
        # 先关闭窗口管理器（如果打开的话）
        if self.window_manager is not None:
            try:
                self.window_manager.window.quit()
                self.window_manager.window.destroy()
            except:
                pass
            self.window_manager = None
            
        if self.root is not None:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
            self.root = None

        self.save_window_settings()
        
        if self.icon:
            self.icon.stop()
            
        keyboard.unhook_all()
        
        if hasattr(self, 'event') and self.event:
            ctypes.windll.kernel32.CloseHandle(self.event)
            
        sys.exit(0)
    
    def on_enter(self, e):
        # 检查当前窗口是否在白名单中
        window = self.get_active_window_info()
        if not window or window['title'] not in self.allowed_windows:
            return True

        # 检查是否有其他键被按下
        if keyboard.is_pressed('shift') or keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt'):
            return True
            
        current_time = time.time()
        # 将冷却时间从0.1秒增加到0.3秒
        if not self.enabled or current_time - self.last_time < 0.3:
            return True
        
        self.last_time = current_time
        e.event_type = 'down'
        keyboard.block_key(e.scan_code)
        
        # 获取当前输入的文本并进行替换
        replaced_text = self.get_and_replace_text()
        
        if replaced_text is not None:
            # 如果有替换内容，清除原文本并输入新文本
            self.clear_current_line()
            time.sleep(0.05)
            keyboard.write(replaced_text)
            time.sleep(0.08)
        else:
            # 如果没有匹配到替换规则，使用原来的逻辑（在末尾添加"喵"）
            keyboard.press('end')
            time.sleep(0.03)
            keyboard.release('end')
            time.sleep(0.02)
            keyboard.write("喵")
            time.sleep(0.08)
        
        # 发送Enter
        keyboard.press_and_release("enter")
        
        keyboard.unblock_key(e.scan_code)
        return False

    def get_and_replace_text(self):
        """获取当前行文本并根据规则进行替换"""
        if not self.replacement_rules.get("enabled", True):
            return None
            
        try:
            # 保存当前剪贴板内容
            old_clipboard = pyperclip.paste()
            
            # 选择当前行的所有文本
            keyboard.press('home')
            time.sleep(0.02)
            keyboard.release('home')
            time.sleep(0.02)
            keyboard.press('shift')
            keyboard.press('end')
            time.sleep(0.02)
            keyboard.release('end')
            keyboard.release('shift')
            time.sleep(0.02)
            
            # 复制选中的文本
            keyboard.press_and_release('ctrl+c')
            time.sleep(0.05)
            
            # 获取复制的文本
            current_text = pyperclip.paste()
            
            # 恢复剪贴板
            pyperclip.copy(old_clipboard)
            
            # 如果文本为空或与剪贴板内容相同（可能复制失败），返回None
            if not current_text or current_text == old_clipboard:
                return None
            
            # 应用替换规则 - 对所有匹配项进行替换
            replaced = False
            result_text = current_text
            
            for rule in self.replacement_rules.get("rules", []):
                pattern = rule.get("pattern", "")
                replacement = rule.get("replacement", "")
                
                if not pattern:
                    continue
                
                # 使用正则表达式进行全局替换（替换所有匹配项）
                if re.search(re.escape(pattern), result_text):
                    result_text = re.sub(re.escape(pattern), replacement, result_text, flags=0)
                    replaced = True
            
            return result_text if replaced else None
            
        except Exception as ex:
            # 如果出错，返回None使用默认行为
            return None

    def clear_current_line(self):
        """清除当前行的文本"""
        try:
            # 选择当前行
            keyboard.press('home')
            time.sleep(0.02)
            keyboard.release('home')
            time.sleep(0.02)
            keyboard.press('shift')
            keyboard.press('end')
            time.sleep(0.02)
            keyboard.release('end')
            keyboard.release('shift')
            time.sleep(0.02)
            
            # 删除选中的文本
            keyboard.press_and_release('backspace')
            time.sleep(0.02)
        except:
            pass

    def run(self):
        self.icon.run()

if __name__ == "__main__":
    # 优先检查单实例
    event = check_single_instance()
    if not event:
        sys.exit(0)
        
    # 检查管理员权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        ctypes.windll.kernel32.CloseHandle(event)
        sys.exit(0)
        
    if getattr(sys, 'frozen', False):
        import os
        os.environ['PYTHONUNBUFFERED'] = '1'
        
    meow = AutoMeow()
    try:
        meow.run()
    finally:
        # 确保清理资源
        if hasattr(meow, 'event') and meow.event:
            ctypes.windll.kernel32.CloseHandle(meow.event)
