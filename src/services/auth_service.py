from src.models.user import UserManager
from src.utils.validators import validate_email, validate_password, validate_username

class AuthService:
    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
    
    def register(self, username: str, password: str, email: str, campus: str) -> dict:
        """用户注册"""
        # 输入验证
        if not username or not password or not email or not campus:
            return {"success": False, "message": "所有字段都必须填写"}
        
        if not validate_username(username):
            return {"success": False, "message": "用户名必须是3-20位的字母、数字或下划线"}
        
        if not validate_email(email):
            return {"success": False, "message": "邮箱格式不正确"}
        
        if not validate_password(password):
            return {"success": False, "message": "密码必须至少6位，包含字母和数字"}
        
        # 注册用户
        if self.user_manager.register_user(username, password, email, campus):
            return {"success": True, "message": "注册成功"}
        else:
            return {"success": False, "message": "用户名或邮箱已存在"}
    
    def login(self, username: str, password: str) -> dict:
        """用户登录"""
        user = self.user_manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            return {"success": True, "message": "登录成功", "user": user}
        else:
            return {"success": False, "message": "用户名或密码错误"}
    
    def logout(self):
        """用户登出"""
        self.current_user = None
    
    def get_current_user(self):
        """获取当前用户"""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.current_user is not None