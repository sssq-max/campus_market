import uuid
from src.services.auth_service import AuthService
from src.services.product_service import ProductService
from src.models.product import ProductCategory


def test_integration_user_publish_and_search_product():
    unique_username = f"integration_{uuid.uuid4().hex[:8]}"
    password = "abc123"

    # 1. 用户注册
    auth = AuthService()
    register_result = auth.register(
        username=unique_username,
        password=password,
        email=f"{unique_username}@test.com",
        campus="主校区"
    )
    assert register_result["success"] is True

    # 2. 用户登录（⭐关键：只有这里才能拿到 user）
    login_result = auth.login(
        username=unique_username,
        password=password
    )
    assert login_result["success"] is True
    user = login_result["user"]

    # 3. 发布商品
    product_service = ProductService()
    publish_result = product_service.publish_product(
        title="集成测试商品",
        description="用于集成测试",
        price=99,
        category=ProductCategory.ELECTRONICS,
        seller_id=user.user_id,      # ✅ 合法来源
        campus="主校区",
        condition="全新"
    )
    assert publish_result["success"] is True

    # 4. 管理员审核商品
    product_id = publish_result["product"].product_id
    assert product_service.approve_product(product_id) is True

    # 5. 搜索商品
    results = product_service.search_products(keyword="集成测试商品")
    assert any(p["product_id"] == product_id for p in results)
