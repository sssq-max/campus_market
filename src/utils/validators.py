"""
验证器工具模块
提供各种数据验证功能
"""

import re
from typing import Union

def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        bool: 如果邮箱格式正确返回True，否则返回False
    """
    if not email or not isinstance(email, str):
        return False
    
    # 简单的邮箱格式验证
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """
    验证密码强度
    
    Args:
        password: 待验证的密码
        
    Returns:
        bool: 如果密码符合要求返回True，否则返回False
    """
    if not password or not isinstance(password, str):
        return False
    
    # 密码要求：至少6位，包含字母和数字
    if len(password) < 6:
        return False
    
    # 检查是否包含数字
    if not any(char.isdigit() for char in password):
        return False
    
    # 检查是否包含字母
    if not any(char.isalpha() for char in password):
        return False
    
    return True

def validate_price(price: Union[str, float, int]) -> bool:
    """
    验证价格是否有效
    
    Args:
        price: 待验证的价格，可以是字符串、浮点数或整数
        
    Returns:
        bool: 如果价格有效返回True，否则返回False
    """
    if price is None:
        return False
    
    try:
        price_value = float(price)
        return price_value > 0
    except (ValueError, TypeError):
        return False

def validate_username(username: str) -> bool:
    """
    验证用户名格式
    
    Args:
        username: 待验证的用户名
        
    Returns:
        bool: 如果用户名符合要求返回True，否则返回False
    """
    if not username or not isinstance(username, str):
        return False
    
    # 用户名要求：3-20个字符，只能包含字母、数字、下划线
    if len(username) < 3 or len(username) > 20:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None

def validate_campus(campus: str) -> bool:
    """
    验证校区名称是否有效
    
    Args:
        campus: 待验证的校区名称
        
    Returns:
        bool: 如果校区名称有效返回True，否则返回False
    """
    valid_campuses = ["东校区", "西校区", "主校区", "南校区", "北校区"]
    return campus in valid_campuses

def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国手机号）
    
    Args:
        phone: 待验证的手机号
        
    Returns:
        bool: 如果手机号格式正确返回True，否则返回False
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # 中国手机号验证：1开头，11位数字
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

def validate_student_id(student_id: str) -> bool:
    """
    验证学号格式
    
    Args:
        student_id: 待验证的学号
        
    Returns:
        bool: 如果学号格式正确返回True，否则返回False
    """
    if not student_id or not isinstance(student_id, str):
        return False
    
    # 简单的学号验证：至少6位数字
    pattern = r'^\d{6,}$'
    return re.match(pattern, student_id) is not None

def validate_product_title(title: str) -> bool:
    """
    验证商品标题
    
    Args:
        title: 待验证的商品标题
        
    Returns:
        bool: 如果标题有效返回True，否则返回False
    """
    if not title or not isinstance(title, str):
        return False
    
    # 商品标题要求：2-50个字符
    return 2 <= len(title) <= 50

def validate_product_description(description: str) -> bool:
    """
    验证商品描述
    
    Args:
        description: 待验证的商品描述
        
    Returns:
        bool: 如果描述有效返回True，否则返回False
    """
    if not description or not isinstance(description, str):
        return False
    
    # 商品描述要求：10-1000个字符
    return 10 <= len(description) <= 1000

def validate_condition(condition: str) -> bool:
    """
    验证商品新旧程度
    
    Args:
        condition: 待验证的新旧程度
        
    Returns:
        bool: 如果新旧程度有效返回True，否则返回False
    """
    valid_conditions = ["全新", "九成新", "七成新", "五成新", "其他"]
    return condition in valid_conditions

def sanitize_input(text: str, max_length: int = None) -> str:
    """
    清理用户输入，防止XSS等安全问题
    
    Args:
        text: 待清理的文本
        max_length: 最大长度限制
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ""
    
    # 移除危险字符
    sanitized = re.sub(r'[<>"\'&]', '', text)
    
    # 限制长度
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_file_extension(filename: str, allowed_extensions: list = None) -> bool:
    """
    验证文件扩展名
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名列表，默认为图片格式
        
    Returns:
        bool: 如果文件扩展名允许返回True，否则返回False
    """
    if not filename:
        return False
    
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # 获取文件扩展名并转换为小写
    file_ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    return file_ext in allowed_extensions

def validate_file_size(file_size: int, max_size_mb: int = 5) -> bool:
    """
    验证文件大小
    
    Args:
        file_size: 文件大小（字节）
        max_size_mb: 最大允许大小（MB）
        
    Returns:
        bool: 如果文件大小在限制范围内返回True，否则返回False
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # 转换为字节
    return 0 < file_size <= max_size_bytes

# 测试函数
if __name__ == "__main__":
    # 测试验证器
    print("邮箱验证测试:")
    print(f"test@example.com: {validate_email('test@example.com')}")
    print(f"invalid-email: {validate_email('invalid-email')}")
    
    print("\n密码验证测试:")
    print(f"password123: {validate_password('password123')}")
    print(f"12345: {validate_password('12345')}")
    
    print("\n价格验证测试:")
    print(f"100: {validate_price('100')}")
    print(f"-10: {validate_price(-10)}")
    
    print("\n用户名验证测试:")
    print(f"user_123: {validate_username('user_123')}")
    print(f"ab: {validate_username('ab')}")
    
    print("\n所有验证器测试完成!")