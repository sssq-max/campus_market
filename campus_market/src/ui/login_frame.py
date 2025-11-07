import tkinter as tk
from tkinter import ttk, messagebox

class LoginFrame(ttk.Frame):
    def __init__(self, parent, auth_service, on_login_success, switch_to_register):
        super().__init__(parent)
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.switch_to_register = switch_to_register
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = ttk.Label(self, text="校易集", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self, text="让闲置流动，让校园更轻松", font=("Arial", 12))
        subtitle_label.pack(pady=(0, 30))
        
        # 登录表单容器
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        # 用户名输入
        ttk.Label(form_frame, text="学号/校园邮箱").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # 密码输入
        ttk.Label(form_frame, text="密码").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.pack(fill="x", pady=(0, 15))
        
        # 记住我选项
        self.remember_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="记住我", variable=self.remember_var).pack(anchor="w", pady=(0, 10))
        
        # 登录按钮
        login_btn = ttk.Button(form_frame, text="登录", command=self.login, style="Accent.TButton")
        login_btn.pack(fill="x", pady=(0, 10))
        
        # 注册链接
        register_frame = ttk.Frame(form_frame)
        register_frame.pack(fill="x")
        ttk.Label(register_frame, text="还没有账号？").pack(side="left")
        register_link = ttk.Button(register_frame, text="立即注册", command=self.switch_to_register, style="Link.TButton")
        register_link.pack(side="left")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        result = self.auth_service.login(username, password)
        if result["success"]:
            messagebox.showinfo("成功", result["message"])
            self.on_login_success()
        else:
            messagebox.showerror("错误", result["message"])