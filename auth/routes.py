from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from .models import User
from .database import validate_user, create_user
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = validate_user(username, password)
        if user:
            user_obj = User.get(user['id'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('用户名或密码不正确!', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if not username or not password or not email:
            flash('请填写所有字段!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('无效的邮箱地址!', 'error')
        elif not re.match(r'^[A-Za-z0-9_]+$', username):
            flash('用户名只能包含字母、数字和下划线!', 'error')
        else:
            if create_user(username, email, password):
                flash('注册成功! 请登录。', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('该用户名或邮箱已被注册!', 'error')
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))