import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.product import Product, ProductCategory
from utils.validators import validate_price, validate_product_title, validate_product_description
import os
from PIL import Image, ImageTk
import base64

class ProductPublishFrame(ttk.Frame):
    def __init__(self, parent, auth_service, product_service, switch_to_main):
        super().__init__(parent)
        self.auth_service = auth_service
        self.product_service = product_service
        self.switch_to_main = switch_to_main
        self.images = []  # 存储上传的图片
        self.create_widgets()
    
    def create_widgets(self):
        # 返回按钮
        back_btn = ttk.Button(self, text="← 返回", command=self.switch_to_main)
        back_btn.pack(anchor="w", padx=10, pady=5)
        
        # 主标题
        title_label = ttk.Label(self, text="发布商品", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)
        
        # 创建滚动框架
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # 发布商品表单
        self.create_form()
    
    def create_form(self):
        # 商品图片区域
        image_frame = ttk.LabelFrame(self.scrollable_frame, text="商品图片", padding=10)
        image_frame.pack(fill="x", pady=(0, 20))
        
        # 图片预览区域
        self.image_preview_frame = ttk.Frame(image_frame)
        self.image_preview_frame.pack(fill="x", pady=(0, 10))
        
        # 图片上传按钮
        upload_btn = ttk.Button(
            image_frame, 
            text="选择图片", 
            command=self.upload_image
        )
        upload_btn.pack(side="left", padx=(0, 10))
        
        # 清除图片按钮
        clear_btn = ttk.Button(
            image_frame,
            text="清除所有图片",
            command=self.clear_images
        )
        clear_btn.pack(side="left")
        
        # 图片提示
        ttk.Label(
            image_frame, 
            text="支持 JPG、PNG 格式，最多5张", 
            foreground="gray",
            font=("Arial", 9)
        ).pack(side="right")
        
        # 商品信息区域
        info_frame = ttk.LabelFrame(self.scrollable_frame, text="商品信息", padding=10)
        info_frame.pack(fill="x", pady=(0, 20))
        
        # 商品标题
        ttk.Label(info_frame, text="商品标题 *").pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(info_frame, font=("Arial", 11))
        self.title_entry.pack(fill="x", pady=(0, 15))
        
        # 商品分类
        ttk.Label(info_frame, text="商品分类 *").pack(anchor="w", pady=(0, 5))
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            info_frame, 
            textvariable=self.category_var,
            values=[cat.value for cat in ProductCategory],
            state="readonly",
            font=("Arial", 11)
        )
        category_combo.pack(fill="x", pady=(0, 15))
        
        # 价格
        ttk.Label(info_frame, text="价格 *").pack(anchor="w", pady=(0, 5))
        price_frame = ttk.Frame(info_frame)
        price_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(price_frame, text="¥", font=("Arial", 12)).pack(side="left")
        self.price_entry = ttk.Entry(price_frame, font=("Arial", 11))
        self.price_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # 校区位置
        ttk.Label(info_frame, text="校区位置 *").pack(anchor="w", pady=(0, 5))
        self.campus_var = tk.StringVar()
        campus_combo = ttk.Combobox(
            info_frame, 
            textvariable=self.campus_var,
            values=["东校区", "西校区", "主校区", "南校区", "北校区"],
            state="readonly",
            font=("Arial", 11)
        )
        campus_combo.pack(fill="x", pady=(0, 15))
        
        # 新旧程度
        ttk.Label(info_frame, text="新旧程度").pack(anchor="w", pady=(0, 5))
        self.condition_var = tk.StringVar(value="九成新")
        condition_combo = ttk.Combobox(
            info_frame, 
            textvariable=self.condition_var,
            values=["全新", "九成新", "七成新", "五成新", "其他"],
            state="readonly",
            font=("Arial", 11)
        )
        condition_combo.pack(fill="x", pady=(0, 15))
        
        # 商品描述
        ttk.Label(info_frame, text="商品描述 *").pack(anchor="w", pady=(0, 5))
        self.desc_text = tk.Text(info_frame, height=8, font=("Arial", 11))
        self.desc_text.pack(fill="x", pady=(0, 15))
        
        # 发布按钮
        publish_btn = ttk.Button(
            self.scrollable_frame, 
            text="发布商品", 
            command=self.publish_product,
            style="Accent.TButton"
        )
        publish_btn.pack(fill="x", pady=20)
        
        # 添加示例数据以便测试
        self.add_sample_data()
    
    def upload_image(self):
        """上传图片"""
        if len(self.images) >= 5:
            messagebox.showwarning("警告", "最多只能上传5张图片")
            return
        
        file_path = filedialog.askopenfilename(
            title="选择商品图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.gif")]
        )
        
        if file_path:
            try:
                # 这里简化处理，实际项目中应该保存图片文件
                # 现在只是存储图片路径用于演示
                self.images.append(file_path)
                self.update_image_preview()
                messagebox.showinfo("成功", f"已添加图片 {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"图片上传失败: {e}")
    
    def clear_images(self):
        """清除所有图片"""
        self.images = []
        self.update_image_preview()
        messagebox.showinfo("成功", "已清除所有图片")
    
    def update_image_preview(self):
        """更新图片预览"""
        # 清空现有预览
        for widget in self.image_preview_frame.winfo_children():
            widget.destroy()
        
        if not self.images:
            # 显示占位符
            placeholder = ttk.Label(
                self.image_preview_frame, 
                text="暂无图片，点击上方按钮添加", 
                foreground="gray"
            )
            placeholder.pack(pady=20)
            return
        
        # 显示图片预览
        preview_frame = ttk.Frame(self.image_preview_frame)
        preview_frame.pack(fill="x")
        
        for i, image_path in enumerate(self.images):
            try:
                # 创建缩略图
                img = Image.open(image_path)
                img.thumbnail((80, 80))
                photo = ImageTk.PhotoImage(img)
                
                # 图片容器
                img_container = ttk.Frame(preview_frame, relief="solid", borderwidth=1)
                img_container.pack(side="left", padx=5)
                
                # 图片标签
                img_label = ttk.Label(img_container, image=photo)
                img_label.image = photo  # 保持引用
                img_label.pack(padx=2, pady=2)
                
                # 图片序号
                ttk.Label(img_container, text=f"{i+1}").pack()
                
            except Exception as e:
                print(f"加载图片失败: {e}")
                # 显示错误占位符
                error_label = ttk.Label(
                    preview_frame, 
                    text=f"图片{i+1}加载失败", 
                    foreground="red"
                )
                error_label.pack(side="left", padx=5)
    
    def add_sample_data(self):
        """添加示例数据用于测试"""
        self.title_entry.insert(0, "二手笔记本电脑")
        self.category_var.set(ProductCategory.ELECTRONICS.value)
        self.price_entry.insert(0, "1200")
        self.campus_var.set("东校区")
        self.desc_text.insert("1.0", "联想ThinkPad，i5处理器，8G内存，256G固态硬盘。使用两年，保养良好，运行流畅，适合学习和办公使用。")
    
    def publish_product(self):
        """发布商品"""
        title = self.title_entry.get().strip()
        category_name = self.category_var.get()
        price_str = self.price_entry.get().strip()
        campus = self.campus_var.get()
        condition = self.condition_var.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # 验证输入
        if not title:
            messagebox.showerror("错误", "请输入商品标题")
            self.title_entry.focus()
            return
        
        if not validate_product_title(title):
            messagebox.showerror("错误", "商品标题必须是2-50个字符")
            self.title_entry.focus()
            return
        
        if not category_name:
            messagebox.showerror("错误", "请选择商品分类")
            return
        
        if not validate_price(price_str):
            messagebox.showerror("错误", "请输入有效的价格（大于0的数字）")
            self.price_entry.select_range(0, tk.END)
            self.price_entry.focus()
            return
        
        if not campus:
            messagebox.showerror("错误", "请选择校区位置")
            return
        
        if not validate_product_description(description):
            messagebox.showerror("错误", "商品描述必须是10-1000个字符")
            self.desc_text.focus()
            return
        
        # 转换价格
        price = float(price_str)
        
        # 查找对应的分类枚举
        try:
            category = next(cat for cat in ProductCategory if cat.value == category_name)
        except StopIteration:
            messagebox.showerror("错误", "请选择有效的商品分类")
            return
        
        # 发布商品
        user = self.auth_service.get_current_user()
        result = self.product_service.publish_product(
            title, description, price, category, user.user_id, campus, condition
        )
        
        if result["success"]:
            messagebox.showinfo("成功", result["message"])
            # 清空表单
            self.clear_form()
            self.switch_to_main()
        else:
            messagebox.showerror("错误", result["message"])
    
    def clear_form(self):
        """清空表单"""
        self.title_entry.delete(0, tk.END)
        self.category_var.set("")
        self.price_entry.delete(0, tk.END)
        self.campus_var.set("")
        self.condition_var.set("九成新")
        self.desc_text.delete("1.0", tk.END)
        self.images = []
        self.update_image_preview()