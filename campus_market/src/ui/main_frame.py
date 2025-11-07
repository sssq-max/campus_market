import tkinter as tk
from tkinter import ttk, messagebox
from models.product import ProductCategory

class MainFrame(ttk.Frame):
    def __init__(self, parent, auth_service, product_service, switch_to_publish, switch_to_admin):
        super().__init__(parent)
        self.auth_service = auth_service
        self.product_service = product_service
        self.switch_to_publish = switch_to_publish
        self.switch_to_admin = switch_to_admin
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        # 顶部导航栏
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        # 用户信息
        user = self.auth_service.get_current_user()
        user_label = ttk.Label(nav_frame, text=f"你好，{user.username}({user.get_user_type_display()})", font=("Arial", 12, "bold"))
        user_label.pack(side="left")
        
        # 管理入口（仅管理员可见）
        if user.user_type == "admin":
            admin_btn = ttk.Button(nav_frame, text="管理后台", command=self.switch_to_admin)
            admin_btn.pack(side="right", padx=(0, 10))
        
        logout_btn = ttk.Button(nav_frame, text="退出", command=self.logout)
        logout_btn.pack(side="right")
        
        # 搜索区域
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_btn = ttk.Button(search_frame, text="搜索", command=self.search_products)
        search_btn.pack(side="right")
        
        # 分类筛选
        category_frame = ttk.Frame(self)
        category_frame.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(category_frame, text="分类:").pack(side="left")
        
        self.category_var = tk.StringVar(value="全部")
        categories = ["全部"] + [category.value for category in ProductCategory]
        
        for category in categories:
            ttk.Radiobutton(category_frame, text=category, value=category, 
                           variable=self.category_var, command=self.search_products).pack(side="left", padx=10)
        
        # 校区筛选
        campus_frame = ttk.Frame(self)
        campus_frame.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(campus_frame, text="校区:").pack(side="left")
        
        self.campus_var = tk.StringVar(value="全部")
        campuses = ["全部", "东校区", "西校区", "主校区", "南校区", "北校区"]
        
        for campus in campuses:
            ttk.Radiobutton(campus_frame, text=campus, value=campus, 
                           variable=self.campus_var, command=self.search_products).pack(side="left", padx=10)
        
        # 商品列表
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 创建滚动框架
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
        
        # 发布按钮
        publish_btn = ttk.Button(self, text="发布商品", command=self.switch_to_publish, style="Accent.TButton")
        publish_btn.pack(pady=10)
    
    def load_products(self, keyword="", category="全部", campus="全部"):
        # 清空现有商品
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # 获取商品数据 - 显示所有商品，不过滤卖家
        campus_filter = campus if campus != "全部" else ""
        max_price = None  # 可以根据需要添加价格筛选
        
        category_str = category if category != "全部" else ""
        products = self.product_service.search_products(keyword, category_str, campus_filter, max_price, show_all=True)
        
        # 显示商品
        for i, product in enumerate(products):
            self.create_product_card(product, i)
    
    def create_product_card(self, product, index):
        card_frame = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=1)
        card_frame.pack(fill="x", padx=5, pady=5, ipady=5)
        
        # 商品标题和价格
        title_frame = ttk.Frame(card_frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text=product['title'], font=("Arial", 12, "bold"))
        title_label.pack(side="left")
        
        price_label = ttk.Label(title_frame, text=f"¥{product['price']}", font=("Arial", 12, "bold"), foreground="red")
        price_label.pack(side="right")
        
        # 商品描述
        desc_label = ttk.Label(card_frame, text=product['description'][:50] + "...")
        desc_label.pack(anchor="w", padx=10, pady=2)
        
        # 商品信息
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill="x", padx=10, pady=2)
        
        # 显示卖家类型（学生/教师）
        seller_type_color = "#3498db" if product['seller_type'] == "学生" else "#e74c3c"
        seller_type_label = ttk.Label(
            info_frame, 
            text=product['seller_type'],
            foreground=seller_type_color,
            font=("Arial", 9, "bold")
        )
        seller_type_label.pack(side="left")
        
        ttk.Label(info_frame, text=f"卖家: {product['seller_name']}").pack(side="left", padx=(5, 0))
        ttk.Label(info_frame, text=f"信用: {product['seller_credit']}").pack(side="left", padx=(20, 0))
        ttk.Label(info_frame, text=f"校区: {product['campus']}").pack(side="right")
    
    def search_products(self):
        keyword = self.search_var.get()
        category = self.category_var.get()
        campus = self.campus_var.get()
        self.load_products(keyword, category, campus)
    
    def logout(self):
        self.auth_service.logout()
        self.master.switch_to_login()