# SRCNN 超分辨率图像处理系统

## 📌 项目简介

基于深度学习的超分辨率图像处理系统，使用 Flask 构建的 Web 应用，实现图像分辨率提升功能。

## 🌟 主要功能

• ✅ 用户注册/登录系统
• ✅ 图像上传和处理
• ✅ 支持 2x/3x/4x 超分辨率
• ✅ 处理历史记录查看
• ✅ 响应式前端界面

## 🛠️ 技术栈

### 后端
• Python 3.8+
• Flask (Web 框架)
• PyTorch 1.0.0 (深度学习)
• OpenCV PIL (图像处理)

### 前端
• Bootstrap 5 (UI 框架)
• HTML5/CSS3/JavaScript

### 数据库
• MySQL

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库设置

1. 创建 MySQL 数据库:
```sql
CREATE DATABASE srcnn;
```

2. 配置数据库连接 (修改 `app.py`):
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'srcnn'
```

### 3. 运行应用

```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 启动

## 📂 项目结构

```
srcnn_app/
├── app.py                  # 主应用入口
├── auth/                  # 认证模块
│   ├── __init__.py
│   ├── models.py          # 数据模型
│   ├── routes.py          # 认证路由
│   └── database.py        # 数据库操作
├── static/                # 静态文件
│   ├── uploads/           # 上传图像
│   └── outputs/           # 处理结果
├── templates/             # HTML模板
└── requirements.txt      # 依赖列表
```

## 🔧 配置选项

在 `.env` 文件中设置环境变量:

```ini
FLASK_SECRET_KEY=your_secret_key
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=16  # MB
```

## 🧪 测试账号

• 用户名: `testuser`
• 密码: `test123`

## 📜 开源许可

MIT License

## 🤝 贡献指南

1. Fork 项目
2. 创建分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

