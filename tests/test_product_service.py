from src.services.product_service import ProductService
from src.models.product import ProductCategory
from src.services.auth_service import AuthService

def setup_user():
    auth = AuthService()
    result = auth.register(
        "seller",
        "abc123",
        "seller@test.com",
        "主校区"
    )
    return auth

def test_publish_product_success():
    service = ProductService()
    setup_user()
    result = service.publish_product(
        title="二手教材",
        description="九成新",
        price=20,
        category=ProductCategory.BOOKS,
        seller_id="1",
        campus="主校区",
        condition="良好"
    )
    assert result["success"] is True

def test_publish_product_empty_title():
    service = ProductService()
    result = service.publish_product(
        title="",
        description="描述",
        price=10,
        category=ProductCategory.BOOKS,
        seller_id="1",
        campus="主校区",
        condition="良好"
    )
    assert result["success"] is False

def test_publish_product_negative_price():
    service = ProductService()
    result = service.publish_product(
        title="手机",
        description="描述",
        price=-1,
        category=ProductCategory.ELECTRONICS,
        seller_id="1",
        campus="主校区",
        condition="一般"
    )
    assert result["success"] is False

def test_search_products_empty():
    service = ProductService()
    results = service.search_products()
    assert isinstance(results, list)
    assert len(results) > 0


def test_search_products_after_publish():
    service = ProductService()
    setup_user()

    
    result = service.publish_product(
        "鼠标",
        "无线鼠标",
        50,
        ProductCategory.ELECTRONICS,
        "1",
        "主校区",
        "良好"
    )

    assert result["success"] is True

    #  从返回的 product 中拿到 product_id
    product_id = result["product"].product_id
    service.approve_product(product_id)

    results = service.search_products(keyword="鼠标")
    assert any(p["title"] == "鼠标" for p in results)


def test_get_pending_products():
    service = ProductService()
    pending = service.get_pending_products()
    assert isinstance(pending, list)

def test_approve_product_invalid_id():
    service = ProductService()
    assert service.approve_product("999") is False

def test_get_products_by_seller_empty():
    service = ProductService()
    products = service.get_products_by_seller("1")
    for p in products:
        assert p["seller_id"] == "1"


