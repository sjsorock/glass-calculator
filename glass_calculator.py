import tkinter as tk
from tkinter import ttk
import ctypes
from ctypes import wintypes

class GlassCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("极简计算器")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # 透明度和毛玻璃设置
        self.opacity = 0.95
        self.setup_glass_effect()
        
        # 历史记录
        self.history = []
        self.current = ""
        
        self.create_ui()
        
    def setup_glass_effect(self):
        """设置毛玻璃/透明效果"""
        # 设置窗口透明
        self.root.attributes('-alpha', self.opacity)
        self.root.attributes('-transparentcolor', '')
        
        # Windows 毛玻璃效果 (DWM)
        if ctypes.windll.user32.GetSystemMetrics(0) > 0:  # 检测 Windows
            try:
                dwm = ctypes.windll.dwmapi
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_MICA_EFFECT = 1029
                
                hwnd = wintypes.HWND(self.root.winfo_id())
                value = ctypes.c_int(2)  # 启用 Mica 效果
                dwm.DwmSetWindowAttribute(hwnd, DWMWA_MICA_EFFECT, 
                                         ctypes.byref(value), ctypes.sizeof(value))
            except:
                pass
        
        # 设置深色背景
        self.bg_color = "#1e1e1e"
        self.glass_color = "#2d2d2d"
        self.text_color = "#ffffff"
        self.accent_color = "#0078d4"
        
        self.root.configure(bg=self.bg_color)
        
    def create_ui(self):
        """创建界面"""
        # 主容器 - 使用 Frame 实现毛玻璃效果
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 透明度滑块
        opacity_frame = tk.Frame(main_frame, bg=self.bg_color)
        opacity_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(opacity_frame, text="透明度", fg="#888", bg=self.bg_color, 
                font=("微软雅黑", 8)).pack(side=tk.LEFT)
        
        opacity_slider = tk.Scale(opacity_frame, from_=0.3, to=1.0, 
                                 resolution=0.05, orient=tk.HORIZONTAL,
                                 bg=self.bg_color, fg=self.text_color,
                                 highlightthickness=0, bd=0,
                                 command=self.set_opacity)
        opacity_slider.set(self.opacity)
        opacity_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # 显示区域 - 毛玻璃效果
        self.display_frame = tk.Frame(main_frame, bg=self.glass_color, 
                                     highlightbackground="#3d3d3d", 
                                     highlightthickness=1)
        self.display_frame.pack(fill=tk.X, pady=5, ipady=20)
        
        # 当前输入显示
        self.current_label = tk.Label(self.display_frame, text="", 
                                     font=("微软雅黑", 32, "bold"),
                                     fg=self.text_color, bg=self.glass_color,
                                     anchor=tk.E, padx=10)
        self.current_label.pack(fill=tk.X)
        
        # 历史记录区域
        history_frame = tk.Frame(main_frame, bg=self.bg_color)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(history_frame, text="历史记录", fg="#888", bg=self.bg_color,
                font=("微软雅黑", 9)).pack(anchor=tk.W)
        
        # 历史记录列表 - 小字体、半透明
        self.history_text = tk.Text(history_frame, bg=self.bg_color, 
                                   fg="#666666", font=("微软雅黑", 8),
                                   highlightthickness=0, bd=0,
                                   height=10, state=tk.DISABLED)
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮区域 - 极简设计，只有数字和基本运算
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # 按钮样式
        buttons = [
            ('C', self.clear, self.accent_color),
            ('÷', lambda: self.operator('/'), self.glass_color),
            ('×', lambda: self.operator('*'), self.glass_color),
            ('⌫', self.backspace, self.glass_color),
            ('7', lambda: self.number('7'), self.glass_color),
            ('8', lambda: self.number('8'), self.glass_color),
            ('9', lambda: self.number('9'), self.glass_color),
            ('-', lambda: self.operator('-'), self.glass_color),
            ('4', lambda: self.number('4'), self.glass_color),
            ('5', lambda: self.number('5'), self.glass_color),
            ('6', lambda: self.number('6'), self.glass_color),
            ('+', lambda: self.operator('+'), self.glass_color),
            ('1', lambda: self.number('1'), self.glass_color),
            ('2', lambda: self.number('2'), self.glass_color),
            ('3', lambda: self.number('3'), self.glass_color),
            ('=', self.calculate, self.accent_color),
            ('0', lambda: self.number('0'), self.glass_color),
            ('.', lambda: self.number('.'), self.glass_color),
        ]
        
        row, col = 0, 0
        for text, cmd, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd,
                          font=("微软雅黑", 14, "bold"),
                          bg=color, fg=self.text_color,
                          activebackground=self.accent_color,
                          activeforeground=self.text_color,
                          bd=0, relief=tk.FLAT,
                          width=4, height=2,
                          cursor="hand2")
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # 等号按钮跨两行
            if text == '=':
                btn.grid(rowspan=2)
            # 0 按钮跨两列
            elif text == '0':
                btn.grid(columnspan=2, sticky="nsew")
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # 设置行列权重
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
            
    def set_opacity(self, value):
        """设置透明度"""
        self.opacity = float(value)
        self.root.attributes('-alpha', self.opacity)
        
    def number(self, num):
        """输入数字"""
        self.current += num
        self.update_display()
        
    def operator(self, op):
        """输入运算符"""
        if self.current and self.current[-1] not in '+-*/':
            self.current += op
            self.update_display()
        elif self.current:
            self.current = self.current[:-1] + op
            self.update_display()
            
    def clear(self):
        """清空"""
        self.current = ""
        self.update_display()
        
    def backspace(self):
        """退格"""
        self.current = self.current[:-1]
        self.update_display()
        
    def calculate(self):
        """计算结果"""
        if not self.current:
            return
            
        try:
            # 替换显示符号为实际运算符
            expr = self.current.replace('×', '*').replace('÷', '/')
            result = eval(expr)
            
            # 格式化结果
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            # 添加到历史记录
            history_entry = f"{self.current} = {result}"
            self.history.insert(0, history_entry)
            if len(self.history) > 20:
                self.history.pop()
                
            self.current = str(result)
            self.update_display()
            self.update_history()
            
        except Exception as e:
            self.current = "错误"
            self.update_display()
            self.root.after(1000, self.clear)
            
    def update_display(self):
        """更新显示"""
        display_text = self.current if self.current else "0"
        # 调整字体大小以适应内容
        if len(display_text) > 12:
            font_size = 20
        elif len(display_text) > 8:
            font_size = 26
        else:
            font_size = 32
            
        self.current_label.config(text=display_text, font=("微软雅黑", font_size, "bold"))
        
    def update_history(self):
        """更新历史记录显示"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for entry in self.history[:10]:  # 只显示最近10条
            self.history_text.insert(tk.END, entry + "\n")
            
        self.history_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GlassCalculator(root)
    root.mainloop()
