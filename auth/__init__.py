from flask_login import LoginManager
from .models import User
from .database import init_db

login_manager = LoginManager()

def init_auth(app):
    # 初始化数据库
    init_db(app)
    
    # 配置登录管理器
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # 必须在这里定义 user_loader，确保它在应用上下文中
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    
    # 注册蓝图
    from .routes import auth_bp
    app.register_blueprint(auth_bp)