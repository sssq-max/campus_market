import tkinter as tk
from tkinter import ttk, messagebox
from models.product import Product, ProductCategory
from utils.validators import validate_price, validate_product_title, validate_product_description

class ProductPublishFrame(ttk.Frame):
    # ... 之前的代码保持不变 ...
    
    def publish_product(self):
        title = self.title_entry.get().strip()
        category_name = self.category_var.get()
        price_str = self.price_entry.get().strip()
        campus = self.campus_var.get()
        condition = self.condition_var.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # 使用验证器进行输入验证
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
    
    # ... 其余代码保持不变 ...