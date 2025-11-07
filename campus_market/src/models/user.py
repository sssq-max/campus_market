import json
import os
from datetime import datetime
from typing import Dict, List

class User:
    def __init__(self, user_id: str, username: str, password: str, email: str, 
                 campus: str, credit_score: int = 100, user_type: str = "student"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.campus = campus
        self.credit_score = credit_score
        self.user_type = user_type  # student, teacher, admin
        self.registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "active"
    
    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'campus': self.campus,
            'credit_score': self.credit_score,
            'user_type': self.user_type,
            'registration_date': self.registration_date,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        user = cls(
            data['user_id'],
            data['username'],
            data['password'],
            data['email'],
            data['campus'],
            data.get('credit_score', 100),
            data.get('user_type', 'student')
        )
        user.registration_date = data.get('registration_date')
        user.status = data.get('status', 'active')
        return user
    
    def get_user_type_display(self) -> str:
        """获取用户类型的显示文本"""
        type_map = {
            'student': '学生',
            'teacher': '教师', 
            'admin': '管理员'
        }
        return type_map.get(self.user_type, '用户')

class UserManager:
    def __init__(self, data_file: str = None):
        # 使用绝对路径确保能找到数据文件
        if data_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(current_dir, '..', '..', 'data', 'users.json')
        self.data_file = data_file
        print(f"用户数据文件路径: {self.data_file}")
        self.users = self._load_users()
    
    def _load_users(self) -> Dict[str, User]:
        try:
            print(f"正在加载用户数据从: {self.data_file}")
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"成功加载 {len(data)} 个用户")
                return {user_id: User.from_dict(user_data) for user_id, user_data in data.items()}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"加载用户数据失败: {e}")
            return {}
    
    def _save_users(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({uid: user.to_dict() for uid, user in self.users.items()}, f, indent=2, ensure_ascii=False)
    
    def register_user(self, username: str, password: str, email: str, campus: str, user_type: str = "student") -> bool:
        # 检查用户是否已存在
        for user in self.users.values():
            if user.username == username or user.email == email:
                return False
        
        user_id = str(len(self.users) + 1)
        new_user = User(user_id, username, password, email, campus, user_type=user_type)
        self.users[user_id] = new_user
        self._save_users()
        return True
    
    def authenticate_user(self, username: str, password: str) -> User:
        print(f"尝试认证用户: {username}")
        print(f"当前用户数量: {len(self.users)}")
        for user_id, user in self.users.items():
            print(f"用户 {user_id}: {user.username} ({user.user_type})")
        
        for user in self.users.values():
            if user.username == username and user.password == password and user.status == "active":
                print(f"用户认证成功: {username} ({user.user_type})")
                return user
        print(f"用户认证失败: {username}")
        return None
    
    def get_user_by_id(self, user_id: str) -> User:
        return self.users.get(user_id)