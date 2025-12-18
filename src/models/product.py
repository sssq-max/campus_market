import json
import os
from datetime import datetime
from typing import Dict, List
from enum import Enum

class ProductStatus(Enum):
    PENDING = "待审核"
    ON_SALE = "在售"
    SOLD = "已售"
    REMOVED = "下架"

class ProductCategory(Enum):
    ELECTRONICS = "电子数码"
    BOOKS = "图书资料"
    CLOTHING = "服装鞋帽"
    SPORTS = "运动器材"
    DAILY = "生活用品"
    OTHER = "其他"

class Product:
    def __init__(self, product_id: str, title: str, description: str, price: float,
                 category: ProductCategory, seller_id: str, campus: str, condition: str = "九成新"):
        self.product_id = product_id
        self.title = title
        self.description = description
        self.price = price
        self.original_price = price * 1.2  # 模拟原价
        self.category = category
        self.seller_id = seller_id
        self.campus = campus
        self.condition = condition
        self.status = ProductStatus.PENDING
        self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.images = []
        self.view_count = 0
        self.like_count = 0
    
    def to_dict(self) -> Dict:
        return {
            'product_id': self.product_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'category': self.category.value,
            'seller_id': self.seller_id,
            'campus': self.campus,
            'condition': self.condition,
            'status': self.status.value,
            'create_time': self.create_time,
            'images': self.images,
            'view_count': self.view_count,
            'like_count': self.like_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        product = cls(
            data['product_id'],
            data['title'],
            data['description'],
            data['price'],
            ProductCategory(data['category']),
            data['seller_id'],
            data['campus'],
            data.get('condition', '九成新')
        )
        product.original_price = data.get('original_price', product.price * 1.2)
        product.status = ProductStatus(data['status'])
        product.create_time = data.get('create_time')
        product.images = data.get('images', [])
        product.view_count = data.get('view_count', 0)
        product.like_count = data.get('like_count', 0)
        return product

class ProductManager:
    def __init__(self, data_file: str = None):
        # 使用绝对路径确保能找到数据文件
        if data_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(current_dir, '..', '..', 'data', 'products.json')
        self.data_file = data_file
        print(f"商品数据文件路径: {self.data_file}")  # 调试信息
        self.products = self._load_products()
    
    def _load_products(self) -> Dict[str, Product]:
        try:
            print(f"正在加载商品数据从: {self.data_file}")  # 调试信息
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"成功加载 {len(data)} 个商品")  # 调试信息
                return {pid: Product.from_dict(product_data) for pid, product_data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"加载商品数据失败: {e}")  # 调试信息
            return {}
    
    def _save_products(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({pid: product.to_dict() for pid, product in self.products.items()}, f, indent=2, ensure_ascii=False)
    
    def add_product(self, product: Product) -> bool:
        self.products[product.product_id] = product
        self._save_products()
        return True
    
    def get_products_by_status(self, status: ProductStatus) -> List[Product]:
        return [product for product in self.products.values() if product.status == status]
    
    def search_products(self, keyword: str = "", category: ProductCategory = None, 
                       campus: str = "", max_price: float = None) -> List[Product]:
        results = []
        for product in self.products.values():
            if product.status != ProductStatus.ON_SALE:
                continue
            
            # 关键词搜索
            if keyword and keyword.lower() not in product.title.lower() and keyword.lower() not in product.description.lower():
                continue
            
            # 分类筛选
            if category and product.category != category:
                continue
            
            # 校区筛选
            if campus and product.campus != campus:
                continue
            
            # 价格筛选
            if max_price and product.price > max_price:
                continue
            
            results.append(product)
        
        return sorted(results, key=lambda x: x.create_time, reverse=True)
    
    def approve_product(self, product_id: str) -> bool:
        if product_id in self.products:
            self.products[product_id].status = ProductStatus.ON_SALE
            self._save_products()
            return True
        return False