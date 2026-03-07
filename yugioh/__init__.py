import os
from flask import Flask
# ตรวจสอบชื่อโฟลเดอร์โปรเจกต์ (ถ้าเป็นชื่ออื่นให้แก้จาก pokemon. เป็นชื่อนั้น)
from yugioh.extensions import db, login_manager, bcrypt
from yugioh.models import User, Type, Card # เปลี่ยนจาก Pokemon เป็น Card
from yugioh.core.routes import core_bp
from yugioh.users.routes import users_bp
from yugioh.yugioh.routes import pokemon_bp

def create_app():
    app = Flask(__name__)
    
    # การตั้งค่า Config (ใช้ค่า Default ถ้าหา Environment Variable ไม่เจอ)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///yugioh.db')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'yugioh-secret-key-123')

    # Initializing Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # ตั้งค่าระบบ Login (ให้เด้งไปที่ Blueprint 'users' ฟังก์ชัน 'login')
    login_manager.login_view = 'users.login' 
    login_manager.login_message = 'Please login before accessing your deck!'
    login_manager.login_message_category = 'warning'

    # Registering Blueprints
    # หน้าหลัก (Home/Detail)
    app.register_blueprint(core_bp, url_prefix='/')
    
    # ระบบสมาชิก (Register/Login/Profile)
    app.register_blueprint(users_bp, url_prefix='/users')
    
    # ระบบจัดการการ์ด (My Collection/New Card)
    app.register_blueprint(pokemon_bp, url_prefix='/my-deck') 
    
    return app