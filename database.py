from app import app, db

with app.app_context():
    db.create_all()
    print("数据库创建成功！")
