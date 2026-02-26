import tkinter as tk
from tkinter import ttk
import platform

class GlassCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("极简计算器")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        
        # 设置清新紫色主题
        self.setup_theme()
        
        # 历史记录
        self.history = []
        self.current = ""
        
        self.create_ui()
        
    def setup_theme(self):
        """设置清新紫色主题"""
        # 主背景：淡紫色渐变效果（用纯色模拟）
        self.bg_color = "#f0e6ff"  # 淡紫背景
        self.card_color = "#faf5ff"  # 卡片白色偏紫
        self.display_bg = "#ffffff"  # 显示区域纯白
        
        # 文字颜色
        self.text_primary = "#2d2d3a"  # 深灰紫，主要文字
        self.text_secondary = "#8b8ba7"  # 浅灰紫，次要文字
        self.text_history = "#a0a0b8"  # 历史记录文字
        
        # 按钮颜色
        self.btn_number = "#f5f0ff"  # 数字按钮淡紫
        self.btn_number_hover = "#ebe5f5"  # 悬停色
        self.btn_op = "#f0e8ff"  # 运算符按钮
        self.btn_clear = "#ffe6f0"  # 清除按钮淡粉
        self.btn_equal = "#d4a5ff"  # 等号按钮紫色
        self.btn_equal_hover = "#c995f5"  # 等号悬停
        
        self.root.configure(bg=self.bg_color)
        
    def create_ui(self):
        """创建界面"""
        # 主容器 - 圆角卡片效果
        main_frame = tk.Frame(self.root, bg=self.card_color, 
                             highlightbackground="#e0d5f0",
                             highlightthickness=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 显示区域 - 白色背景
        display_frame = tk.Frame(main_frame, bg=self.display_bg,
                                highlightbackground="#f0e8ff",
                                highlightthickness=2,
                                bd=0)
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10), ipady=25)
        
        # 当前输入显示 - 右对齐大字体
        self.current_label = tk.Label(display_frame, text="0", 
                                     font=("SF Pro Display", 48, "light"),
                                     fg=self.text_primary, bg=self.display_bg,
                                     anchor=tk.E, padx=15)
        self.current_label.pack(fill=tk.X)
        
        # 历史记录区域
        history_header = tk.Frame(main_frame, bg=self.card_color)
        history_header.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        tk.Label(history_header, text="历史记录", fg=self.text_secondary,
                bg=self.card_color, font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        clear_btn = tk.Label(history_header, text="清空", fg="#d4a5ff",
                            bg=self.card_color, font=("微软雅黑", 10),
                            cursor="hand2")
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind("<Button-1>", lambda e: self.clear_history())
        
        # 历史记录列表
        history_container = tk.Frame(main_frame, bg=self.card_color)
        history_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.history_text = tk.Text(history_container, bg=self.card_color,
                                   fg=self.text_history, font=("微软雅黑", 10),
                                   highlightthickness=0, bd=0,
                                   height=6, state=tk.DISABLED,
                                   spacing1=8, spacing3=8)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮区域
        btn_frame = tk.Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill=tk.X, padx=12, pady=(5, 15))
        
        # 按钮配置 (文字, 命令, 背景色, 文字颜色)
        buttons = [
            ('C', self.clear, self.btn_clear, self.text_primary),
            ('÷', lambda: self.operator('/'), self.btn_op, self.text_primary),
            ('×', lambda: self.operator('*'), self.btn_op, self.text_primary),
            ('⌫', self.backspace, self.btn_op, self.text_primary),
            ('7', lambda: self.number('7'), self.btn_number, self.text_primary),
            ('8', lambda: self.number('8'), self.btn_number, self.text_primary),
            ('9', lambda: self.number('9'), self.btn_number, self.text_primary),
            ('-', lambda: self.operator('-'), self.btn_op, self.text_primary),
            ('4', lambda: self.number('4'), self.btn_number, self.text_primary),
            ('5', lambda: self.number('5'), self.btn_number, self.text_primary),
            ('6', lambda: self.number('6'), self.btn_number, self.text_primary),
            ('+', lambda: self.operator('+'), self.btn_op, self.text_primary),
            ('1', lambda: self.number('1'), self.btn_number, self.text_primary),
            ('2', lambda: self.number('2'), self.btn_number, self.text_primary),
            ('3', lambda: self.number('3'), self.btn_number, self.text_primary),
            ('=', self.calculate, self.btn_equal, "#ffffff"),
            ('0', lambda: self.number('0'), self.btn_number, self.text_primary),
            ('.', lambda: self.number('.'), self.btn_number, self.text_primary),
        ]
        
        row, col = 0, 0
        for text, cmd, bg_color, fg_color in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd,
                          font=("SF Pro Display", 16, "medium"),
                          bg=bg_color, fg=fg_color,
                          activebackground=self.btn_equal if text == '=' else self.btn_number_hover,
                          activeforeground=fg_color,
                          bd=0, relief=tk.FLAT,
                          width=4, height=2,
                          cursor="hand2",
                          highlightthickness=0)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            
            # 等号按钮跨两行
            if text == '=':
                btn.grid(row=row, column=col, rowspan=2, sticky="nsew")
            # 0 按钮跨两列
            elif text == '0':
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew")
                col += 1  # 额外跳过一格
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # 设置行列权重
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        
    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self.update_history()
        
    def number(self, num):
        """输入数字"""
        if self.current == "0" and num != '.':
            self.current = num
        else:
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
        """清空当前输入"""
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
        if len(display_text) > 14:
            font_size = 28
        elif len(display_text) > 10:
            font_size = 36
        else:
            font_size = 48
            
        self.current_label.config(text=display_text, 
                                 font=("SF Pro Display", font_size, "light"))
        
    def update_history(self):
        """更新历史记录显示"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for entry in self.history[:8]:  # 只显示最近8条
            self.history_text.insert(tk.END, entry + "\n")
            
        self.history_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GlassCalculator(root)
    root.mainloop()
