import json
import os

def create_test_data():
    """创建测试数据"""
    
    # 创建数据目录
    os.makedirs("data", exist_ok=True)
    
    # 创建测试用户数据
    users_data = {
        "1": {
            "user_id": "1",
            "username": "admin",
            "password": "admin123",
            "email": "admin@campus.com",
            "campus": "主校区",
            "credit_score": 100,
            "registration_date": "2024-01-01 10:00:00",
            "status": "active",
            "user_type": "admin"
        },
        "2": {
            "user_id": "2",
            "username": "student",
            "password": "student123",
            "email": "student@campus.com",
            "campus": "东校区",
            "credit_score": 95,
            "registration_date": "2024-01-02 14:30:00",
            "status": "active",
            "user_type": "student"
        },
        "3": {
            "user_id": "3",
            "username": "teacher",
            "password": "teacher123",
            "email": "teacher@campus.com",
            "campus": "西校区",
            "credit_score": 98,
            "registration_date": "2024-01-03 09:15:00",
            "status": "active",
            "user_type": "teacher"
        }
    }
    
    # 创建测试商品数据 - 确保所有用户都能看到所有商品
    products_data = {
        "1": {
            "product_id": "1",
            "title": "二手运动鞋",
            "description": "九成新运动鞋，仅穿几次，舒适透气，适合跑步和日常穿搭。鞋底几乎没有磨损，保持得很好。",
            "price": 120.0,
            "original_price": 150.0,
            "category": "服装鞋帽",
            "seller_id": "2",  # student发布的
            "campus": "东校区",
            "condition": "九成新",
            "status": "在售",
            "create_time": "2024-01-10 15:20:00",
            "images": [],
            "view_count": 25,
            "like_count": 3
        },
        "2": {
            "product_id": "2",
            "title": "Python编程书籍",
            "description": "Python编程入门到实践，几乎全新，无笔记无划痕，适合初学者学习使用。",
            "price": 45.0,
            "original_price": 69.0,
            "category": "图书资料",
            "seller_id": "3",  # teacher发布的
            "campus": "西校区",
            "condition": "全新",
            "status": "在售",
            "create_time": "2024-01-11 10:45:00",
            "images": [],
            "view_count": 18,
            "like_count": 2
        },
        "3": {
            "product_id": "3",
            "title": "无线蓝牙耳机",
            "description": "音质良好，续航时间长，几乎全新，包装配件齐全。因换新耳机而出售。",
            "price": 180.0,
            "original_price": 299.0,
            "category": "电子数码",
            "seller_id": "2",  # student发布的
            "campus": "东校区",
            "condition": "九成新",
            "status": "在售",
            "create_time": "2024-01-12 16:30:00",
            "images": [],
            "view_count": 32,
            "like_count": 5
        },
        "4": {
            "product_id": "4",
            "title": "高等数学教材",
            "description": "大学高等数学教材，包含习题解答，适合大一学生使用。",
            "price": 30.0,
            "original_price": 50.0,
            "category": "图书资料",
            "seller_id": "3",  # teacher发布的
            "campus": "西校区",
            "condition": "七成新",
            "status": "在售",
            "create_time": "2024-01-13 09:20:00",
            "images": [],
            "view_count": 15,
            "like_count": 1
        },
        "5": {
            "product_id": "5",
            "title": "待审核的商品测试",
            "description": "这是一个测试待审核状态的商品，应该在管理后台中显示为待审核状态。",
            "price": 99.0,
            "original_price": 120.0,
            "category": "其他",
            "seller_id": "2",  # student发布的
            "campus": "东校区",
            "condition": "七成新",
            "status": "待审核",
            "create_time": "2024-01-13 14:20:00",
            "images": [],
            "view_count": 0,
            "like_count": 0
        }
    }
    
    # 保存用户数据
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    
    # 保存商品数据
    with open("data/products.json", "w", encoding="utf-8") as f:
        json.dump(products_data, f, indent=2, ensure_ascii=False)
    
    print("测试数据创建完成！")
    print("可用账号：")
    print("管理员 - 用户名: admin, 密码: admin123")
    print("学生用户 - 用户名: student, 密码: student123")
    print("教师用户 - 用户名: teacher, 密码: teacher123")
    print("\n商品发布者分布：")
    print("- 学生发布: 二手运动鞋, 无线蓝牙耳机, 待审核商品")
    print("- 教师发布: Python编程书籍, 高等数学教材")

if __name__ == "__main__":
    create_test_data()