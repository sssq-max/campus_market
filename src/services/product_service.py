from src.models.product import Product, ProductManager, ProductStatus, ProductCategory
from src.models.user import UserManager

class ProductService:
    def __init__(self):
        self.product_manager = ProductManager()
        self.user_manager = UserManager()
    
    def publish_product(self, title: str, description: str, price: float,
                       category: ProductCategory, seller_id: str, campus: str, condition: str) -> dict:
        """发布商品"""
        if not title or not description or price <= 0:
            return {"success": False, "message": "请填写完整的商品信息"}
        
        product_id = str(len(self.product_manager.products) + 1)
        product = Product(product_id, title, description, price, category, seller_id, campus, condition)
        
        if self.product_manager.add_product(product):
            return {"success": True, "message": "商品发布成功，等待审核", "product": product}
        else:
            return {"success": False, "message": "商品发布失败"}
    
    def search_products(self, keyword: str = "", category: str = "", 
                       campus: str = "", max_price: float = None, 
                       show_all: bool = True) -> list:
        """搜索商品
        Args:
            show_all: 是否显示所有商品（包括其他用户的）
        """
        category_enum = None
        if category:
            try:
                category_enum = ProductCategory(category)
            except ValueError:
                pass
        
        # 搜索时不过滤卖家，显示所有商品
        products = self.product_manager.search_products(keyword, category_enum, campus, max_price)
        
        # 丰富商品信息
        enriched_products = []
        for product in products:
            seller = self.user_manager.get_user_by_id(product.seller_id)
            enriched_product = product.to_dict()
            enriched_product['seller_name'] = seller.username if seller else "未知用户"
            enriched_product['seller_credit'] = seller.credit_score if seller else 100
            enriched_product['seller_type'] = seller.get_user_type_display() if seller else "用户"
            enriched_products.append(enriched_product)
        
        return enriched_products
    
    def get_pending_products(self) -> list:
        """获取待审核商品"""
        pending_products = self.product_manager.get_products_by_status(ProductStatus.PENDING)
        enriched_products = []
        
        for product in pending_products:
            seller = self.user_manager.get_user_by_id(product.seller_id)
            enriched_product = product.to_dict()
            enriched_product['seller_name'] = seller.username if seller else "未知用户"
            enriched_product['seller_type'] = seller.get_user_type_display() if seller else "用户"
            enriched_products.append(enriched_product)
        
        return enriched_products
    
    def approve_product(self, product_id: str) -> bool:
        """审核通过商品"""
        return self.product_manager.approve_product(product_id)
    
    def get_products_by_seller(self, seller_id: str) -> list:
        """获取指定卖家的商品（用于个人中心）"""
        products = self.product_manager.products.values()
        seller_products = [p for p in products if p.seller_id == seller_id]
        
        enriched_products = []
        for product in seller_products:
            seller = self.user_manager.get_user_by_id(product.seller_id)
            enriched_product = product.to_dict()
            enriched_product['seller_name'] = seller.username if seller else "未知用户"
            enriched_product['seller_type'] = seller.get_user_type_display() if seller else "用户"
            enriched_products.append(enriched_product)
        
        return enriched_products