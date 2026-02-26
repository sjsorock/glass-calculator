import tkinter as tk
from tkinter import ttk
from datetime import datetime

class HistoryCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 设置清新紫色主题
        self.setup_theme()
        
        # 历史记录
        self.history = []
        self.current = "0"
        
        self.create_ui()
        
        # 绑定键盘输入
        self.root.bind('<Key>', self.on_key_press)
        
    def setup_theme(self):
        """设置清新紫色主题"""
        # 主背景：淡紫色
        self.bg_color = "#f5f0ff"  # 淡紫背景
        self.card_color = "#faf7ff"  # 卡片背景，更浅的紫
        
        # 文字颜色
        self.text_primary = "#3d3d5c"  # 深灰紫，主要文字
        self.text_secondary = "#9a9ab8"  # 浅灰紫，次要文字
        self.text_history = "#7a7a9a"  # 历史记录文字
        self.text_time = "#b8b8d0"  # 时间文字
        
        # 清空按钮颜色
        self.clear_color = "#d4a5ff"  # 紫色
        
        self.root.configure(bg=self.bg_color)
        
    def create_ui(self):
        """创建界面"""
        # 主容器 - 圆角卡片效果
        main_frame = tk.Frame(self.root, bg=self.card_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # 顶部显示区域 - 当前数值（右上角对齐）
        display_frame = tk.Frame(main_frame, bg=self.card_color)
        display_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # 当前数值 - 右对齐大字体
        self.current_label = tk.Label(display_frame, text=self.current, 
                                     font=("SF Pro Display", 56, "light"),
                                     fg=self.text_primary, bg=self.card_color,
                                     anchor=tk.E)
        self.current_label.pack(fill=tk.X)
        
        # 历史记录区域
        history_header = tk.Frame(main_frame, bg=self.card_color)
        history_header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # 历史记录标题
        tk.Label(history_header, text="历史记录", fg=self.text_secondary,
                bg=self.card_color, font=("微软雅黑", 11)).pack(side=tk.LEFT)
        
        # 清空按钮
        clear_btn = tk.Label(history_header, text="清空", fg=self.clear_color,
                            bg=self.card_color, font=("微软雅黑", 11),
                            cursor="hand2")
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind("<Button-1>", lambda e: self.clear_history())
        
        # 历史记录列表容器
        self.history_container = tk.Frame(main_frame, bg=self.card_color)
        self.history_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 15))
        
        # 创建历史记录标签列表
        self.history_labels = []
        for i in range(5):  # 显示最近5条
            row_frame = tk.Frame(self.history_container, bg=self.card_color)
            row_frame.pack(fill=tk.X, pady=6)
            
            # 算式文本
            expr_label = tk.Label(row_frame, text="", fg=self.text_history,
                                 bg=self.card_color, font=("微软雅黑", 11),
                                 anchor=tk.W)
            expr_label.pack(side=tk.LEFT)
            
            # 时间文本
            time_label = tk.Label(row_frame, text="", fg=self.text_time,
                                 bg=self.card_color, font=("微软雅黑", 9),
                                 anchor=tk.E)
            time_label.pack(side=tk.RIGHT)
            
            self.history_labels.append((expr_label, time_label))
        
    def on_key_press(self, event):
        """处理键盘输入"""
        key = event.char
        
        if key.isdigit() or key == '.':
            if self.current == "0" and key != '.':
                self.current = key
            else:
                self.current += key
            self.update_display()
        elif key in '+-*/':
            self.operator(key)
        elif key == '\r' or key == '=':  # 回车或等号
            self.calculate()
        elif key == '\x08':  # 退格
            self.backspace()
        elif key == '\x1b':  # ESC
            self.clear()
            
    def operator(self, op):
        """输入运算符"""
        if self.current and self.current[-1] not in '+-*/':
            self.current += op
            self.update_display()
        elif self.current:
            self.current = self.current[:-1] + op
            self.update_display()
            
    def clear(self):
        """清空当前输入"""
        self.current = "0"
        self.update_display()
        
    def backspace(self):
        """退格"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()
        
    def calculate(self):
        """计算结果"""
        if not self.current or self.current == "0":
            return
            
        # 如果最后一个字符是运算符，先移除
        expr = self.current
        if expr[-1] in '+-*/':
            expr = expr[:-1]
            
        try:
            # 计算结果
            result = eval(expr)
            
            # 格式化结果
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            # 添加到历史记录
            history_entry = {
                'expr': f"{expr} = {result}",
                'time': self.get_time_str()
            }
            self.history.insert(0, history_entry)
            if len(self.history) > 20:
                self.history.pop()
                
            self.current = str(result)
            self.update_display()
            self.update_history()
            
        except Exception as e:
            self.current = "错误"
            self.update_display()
            self.root.after(1000, lambda: self.clear())
            
    def get_time_str(self):
        """获取当前时间字符串"""
        now = datetime.now()
        hour = now.hour
        
        if hour < 12:
            period = "上午"
        elif hour < 18:
            period = "下午"
        else:
            period = "晚上"
            
        return f"{period}{hour}:{now.minute:02d}"
            
    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self.update_history()
        
    def update_display(self):
        """更新显示"""
        display_text = self.current if self.current else "0"
        
        # 调整字体大小以适应内容
        if len(display_text) > 12:
            font_size = 36
        elif len(display_text) > 8:
            font_size = 44
        else:
            font_size = 56
            
        self.current_label.config(text=display_text, 
                                 font=("SF Pro Display", font_size, "light"))
        
    def update_history(self):
        """更新历史记录显示"""
        for i, (expr_label, time_label) in enumerate(self.history_labels):
            if i < len(self.history):
                entry = self.history[i]
                expr_label.config(text=entry['expr'])
                time_label.config(text=entry['time'])
            else:
                expr_label.config(text="")
                time_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = HistoryCalculator(root)
    root.mainloop()
