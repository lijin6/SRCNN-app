import os

class Config:
    SECRET_KEY = 'zero'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/srcnn'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    OUTPUT_FOLDER = 'static/outputs'
