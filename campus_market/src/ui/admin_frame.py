import tkinter as tk
from tkinter import ttk, messagebox
from models.product import ProductStatus

class AdminFrame(ttk.Frame):
    def __init__(self, parent, auth_service, product_service, switch_to_main):
        super().__init__(parent)
        self.auth_service = auth_service
        self.product_service = product_service
        self.switch_to_main = switch_to_main
        
        # 创建自定义样式
        self.create_styles()
        self.create_widgets()
        self.load_pending_products()
    
    def create_styles(self):
        """创建自定义按钮样式"""
        style = ttk.Style()
        
        # 配置危险按钮样式（红色）
        style.configure(
            "Red.TButton",
            foreground="white",
            background="#e74c3c",
            font=("Arial", 10, "bold"),
            padding=(10, 5)
        )
        
        style.map(
            "Red.TButton",
            background=[
                ('active', '#c0392b'),
                ('pressed', '#c0392b')
            ]
        )
        
        # 配置主要按钮样式（蓝色）
        style.configure(
            "Blue.TButton", 
            foreground="white",
            background="#3498db",
            font=("Arial", 10, "bold"),
            padding=(10, 5)
        )
        
        style.map(
            "Blue.TButton",
            background=[
                ('active', '#2980b9'),
                ('pressed', '#2980b9')
            ]
        )
    
    def create_widgets(self):
        # 返回按钮
        back_btn = ttk.Button(
            self, 
            text="← 返回主界面", 
            command=self.switch_to_main
        )
        back_btn.pack(anchor="w", padx=10, pady=5)
        
        # 管理标题
        title_label = ttk.Label(
            self, 
            text="校易集管理后台", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # 数据概览卡片
        self.create_stats_cards()
        
        # 待审核商品区域
        ttk.Label(
            self, 
            text="待审核商品", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # 创建滚动框架
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        self.canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_stats_cards(self):
        """创建数据概览卡片"""
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # 注册用户数卡片
        user_card = self.create_stat_card(stats_frame, "1,248", "注册用户", "#3498db")
        user_card.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # 待审商品卡片
        pending_count = len(self.product_service.get_pending_products())
        product_card = self.create_stat_card(stats_frame, str(pending_count), "待审商品", "#e74c3c")
        product_card.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # 纠纷处理卡片
        dispute_card = self.create_stat_card(stats_frame, "5", "纠纷处理", "#f39c12")
        dispute_card.pack(side="left", expand=True, fill="x")
    
    def create_stat_card(self, parent, value, label, color):
        """创建单个统计卡片"""
        card = ttk.Frame(parent, relief="solid", borderwidth=1, padding=10)
        
        # 数值
        value_label = ttk.Label(
            card, 
            text=value, 
            font=("Arial", 24, "bold"),
            foreground=color
        )
        value_label.pack(pady=(5, 5))
        
        # 标签
        label_label = ttk.Label(card, text=label, font=("Arial", 11))
        label_label.pack(pady=(0, 5))
        
        return card
    
    def load_pending_products(self):
        """加载待审核商品"""
        # 清空现有内容
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 获取待审核商品
        pending_products = self.product_service.get_pending_products()
        
        if not pending_products:
            empty_label = ttk.Label(
                self.scrollable_frame, 
                text="暂无待审核商品", 
                font=("Arial", 12),
                foreground="gray"
            )
            empty_label.pack(pady=50)
            return
        
        # 显示待审核商品
        for product in pending_products:
            self.create_product_card(product)
    
    def create_product_card(self, product):
        """创建商品卡片"""
        card_frame = ttk.Frame(
            self.scrollable_frame, 
            relief="solid", 
            borderwidth=1,
            padding=10
        )
        card_frame.pack(fill="x", padx=5, pady=8)
        
        # 商品标题和价格
        title_frame = ttk.Frame(card_frame)
        title_frame.pack(fill="x", pady=(0, 8))
        
        title_label = ttk.Label(
            title_frame, 
            text=product['title'], 
            font=("Arial", 14, "bold")
        )
        title_label.pack(side="left")
        
        price_frame = ttk.Frame(title_frame)
        price_frame.pack(side="right")
        
        ttk.Label(price_frame, text="价格:", font=("Arial", 10)).pack(side="left")
        price_label = ttk.Label(
            price_frame, 
            text=f"¥{product['price']}", 
            font=("Arial", 14, "bold"),
            foreground="red"
        )
        price_label.pack(side="left", padx=(5, 0))
        
        # 商品描述
        desc_text = product['description']
        if len(desc_text) > 100:
            desc_text = desc_text[:100] + "..."
        
        desc_label = ttk.Label(
            card_frame, 
            text=desc_text, 
            wraplength=600,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 8))
        
        # 商品详细信息
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill="x", pady=(0, 8))
        
        # 分类和校区
        ttk.Label(info_frame, text=f"分类: {product['category']}").pack(side="left")
        ttk.Label(info_frame, text=f"校区: {product['campus']}").pack(side="left", padx=(20, 0))
        ttk.Label(info_frame, text=f"新旧: {product.get('condition', '九成新')}").pack(side="left", padx=(20, 0))
        
        # 卖家信息和发布时间
        seller_frame = ttk.Frame(card_frame)
        seller_frame.pack(fill="x", pady=(0, 8))
        
        ttk.Label(seller_frame, text=f"卖家: {product['seller_name']}").pack(side="left")
        ttk.Label(seller_frame, text=f"发布时间: {product['create_time']}").pack(side="right")
        
        # 审核按钮 - 使用自定义样式确保显示
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(fill="x", pady=(5, 0))
        
        # 使用 tk.Button 而不是 ttk.Button 以确保样式正确应用
        # 拒绝按钮（红色）
        reject_btn = tk.Button(
            btn_frame, 
            text="拒绝",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief="flat",
            command=lambda pid=product['product_id']: self.reject_product(pid)
        )
        reject_btn.pack(side="right", padx=(10, 0))
        
        # 通过按钮（蓝色）
        approve_btn = tk.Button(
            btn_frame, 
            text="审核通过",
            bg="#3498db", 
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief="flat",
            command=lambda pid=product['product_id']: self.approve_product(pid)
        )
        approve_btn.pack(side="right")
        
        # 绑定鼠标悬停效果
        self.bind_button_hover(reject_btn, "#e74c3c", "#c0392b")
        self.bind_button_hover(approve_btn, "#3498db", "#2980b9")
    
    def bind_button_hover(self, button, normal_color, hover_color):
        """绑定按钮的鼠标悬停效果"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def approve_product(self, product_id):
        """审核通过商品"""
        if self.product_service.approve_product(product_id):
            messagebox.showinfo("成功", "商品审核通过，已上架展示")
            self.load_pending_products()  # 刷新列表
        else:
            messagebox.showerror("错误", "审核失败，请重试")
    
    def reject_product(self, product_id):
        """拒绝商品"""
        if messagebox.askyesno("确认拒绝", "确定要拒绝这个商品吗？"):
            # 这里可以添加拒绝逻辑，比如设置商品状态为拒绝
            # 暂时简单地从待审核列表中移除
            messagebox.showinfo("成功", "商品已拒绝")
            self.load_pending_products()  # 刷新列表