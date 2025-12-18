from src.services.auth_service import AuthService
from src.services.product_service import ProductService
from src.models.product import ProductCategory

def test_integration_get_products_by_seller():
    # 1. 注册并登录用户
    auth = AuthService()
    auth.register(
        username="seller_integration",
        password="abc123",
        email="seller_integration@test.com",
        campus="西校区"
    )
    login_result = auth.login("seller_integration", "abc123")
    user = login_result["user"]

    product_service = ProductService()

    # 2. 发布两个商品
    product_service.publish_product(
        "商品A",
        "测试商品A",
        30,
        ProductCategory.BOOKS,
        user.user_id,
        "西校区",
        "良好"
    )

    product_service.publish_product(
        "商品B",
        "测试商品B",
        50,
        ProductCategory.BOOKS,
        user.user_id,
        "西校区",
        "良好"
    )

    # 3. 按卖家查询商品
    products = product_service.get_products_by_seller(user.user_id)

    assert len(products) >= 2
    for p in products:
        assert p["seller_id"] == user.user_id
