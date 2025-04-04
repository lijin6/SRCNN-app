from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from auth import init_auth
from function.method import ImageProcessor
import os
from datetime import datetime
import uuid
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL 配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'srcnn'

# 初始化认证模块
init_auth(app)

# 配置上传和输出文件夹
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# 初始化图像处理器
image_processor = ImageProcessor()

@app.route('/',methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        scale = request.form.get('scale', 'x2')
        
        if file.filename == '':
            flash('没有选择文件', 'error')
            return redirect(request.url)
            
        if file and image_processor.allowed_file(file.filename) and scale in image_processor.models:
            filename = image_processor.generate_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            try:
                output_path = image_processor.process_image(filepath, scale, OUTPUT_FOLDER)
                
                # 保存图片记录到数据库
                from auth.database import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO user_images (user_id, original_path, processed_path, scale)
                VALUES (%s, %s, %s, %s)
                ''', (current_user.id, filepath, output_path, scale))
                conn.commit()
                conn.close()
                
                return render_template('index.html', 
                                     input_image=filepath, 
                                     output_image=output_path, 
                                     scale=scale,
                                     input_filename=file.filename)
            except Exception as e:
                flash(f'处理图像时出错: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('不允许的文件类型或无效的缩放比例', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/history')
@login_required
def history():
    from auth.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('''
    SELECT original_path, processed_path, scale, created_at 
    FROM user_images 
    WHERE user_id = %s 
    ORDER BY created_at DESC
    ''', (current_user.id,))
    images = cursor.fetchall()
    conn.close()
    
    # 关键修复：统一路径格式
    for img in images:
        # 方案1：如果数据库存的是完整路径（包含static/）
        img['original_path'] = img['original_path'].replace('\\', '/').replace('static/', '')
        img['processed_path'] = img['processed_path'].replace('\\', '/').replace('static/', '')
        
        # 方案2：如果数据库存的是绝对路径（根据实际情况调整）
        # img['original_path'] = os.path.relpath(img['original_path'], 'static').replace('\\', '/')
    
    return render_template('history.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)