from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id=None, username=None, email=None):
        self.id = id
        self.username = username
        self.email = email
    
    @staticmethod
    def get(user_id):
        from .database import get_user_by_id
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(
                id=user_data['id'], 
                username=user_data['username'],
                email=user_data['email']
            )
        return None