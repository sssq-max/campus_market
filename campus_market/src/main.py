import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from services.auth_service import AuthService
from services.product_service import ProductService
from ui.login_frame import LoginFrame
from ui.main_frame import MainFrame
from ui.product_frame import ProductPublishFrame
from ui.admin_frame import AdminFrame

class CampusMarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("校易集 - 校园二手交易平台")
        self.root.geometry("800x600")
        
        # 初始化服务
        self.auth_service = AuthService()
        self.product_service = ProductService()
        
        # 设置样式
        self.setup_styles()
        
        # 创建主容器
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill="both", expand=True)
        
        # 显示登录界面
        self.show_login_frame()
    
    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 配置主按钮样式
        style.configure("Accent.TButton", 
                       font=("Arial", 10, "bold"),
                       padding=(20, 8))
        
        # 配置链接按钮样式
        style.configure("Link.TButton", 
                       foreground="blue", 
                       font=("Arial", 9),
                       borderwidth=0,
                       focuscolor=style.lookup("TButton", "focuscolor"))
        
        # 配置危险按钮样式（红色）
        style.configure("Danger.TButton",
                       foreground="white",
                       background="#e74c3c",
                       font=("Arial", 10),
                       padding=(15, 6))
        
        style.map("Danger.TButton",
                 background=[('active', '#c0392b'),
                           ('pressed', '#c0392b')])
    
    def show_login_frame(self):
        self.clear_frame()
        self.login_frame = LoginFrame(
            self.main_container, 
            self.auth_service, 
            self.show_main_frame,
            self.show_register_frame
        )
        self.login_frame.pack(fill="both", expand=True)
    
    def show_register_frame(self):
        # 注册界面实现类似登录界面
        # 这里可以先跳过，或者创建一个简单的消息框
        from tkinter import messagebox
        messagebox.showinfo("提示", "注册功能待实现，请使用测试账号登录")
    
    def show_main_frame(self):
        self.clear_frame()
        self.main_frame = MainFrame(
            self.main_container,
            self.auth_service,
            self.product_service,
            self.show_publish_frame,
            self.show_admin_frame
        )
        self.main_frame.pack(fill="both", expand=True)
    
    def show_publish_frame(self):
        self.clear_frame()
        self.publish_frame = ProductPublishFrame(
            self.main_container,
            self.auth_service,
            self.product_service,
            self.show_main_frame
        )
        self.publish_frame.pack(fill="both", expand=True)
    
    def show_admin_frame(self):
        self.clear_frame()
        self.admin_frame = AdminFrame(
            self.main_container,
            self.auth_service,
            self.product_service,
            self.show_main_frame
        )
        self.admin_frame.pack(fill="both", expand=True)
    
    def clear_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusMarketApp(root)
    root.mainloop()