from flask import Blueprint, render_template, request, redirect, url_for, flash
# ตรวจสอบชื่อโฟลเดอร์โปรเจกต์ (ถ้าเปลี่ยนจาก pokemon เป็น yugioh ให้แก้ตรงนี้ด้วยครับ)
from yugioh.extensions import db, bcrypt 
from yugioh.models import User
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa

users_bp = Blueprint('users', __name__, template_folder='templates')

@users_bp.route('/')
@login_required
def index():
    # หน้าแรกหลัง Login ของ User
    return render_template('users/index.html', title='Duelist Dashboard')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # ตรวจสอบ Username ซ้ำ
        user = db.session.scalar(sa.select(User).where(User.username==username))
        if user:
            flash('This Duelist Name is already taken!', 'warning')
            return redirect(url_for('users.register'))
        
        # ตรวจสอบ Email ซ้ำ
        user = db.session.scalar(sa.select(User).where(User.email==email))
        if user:
            flash('This Email is already registered!', 'warning')
            return redirect(url_for('users.register'))

        if password == confirm_password:
            # Hash รหัสผ่านเพื่อความปลอดภัย
            pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            # สร้าง User ใหม่ (ตรวจสอบชื่อ Field ใน models.py ของคุณอีกทีนะครับ)
            new_user = User(username=username, email=email, password=pwd_hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Welcome to the Duel Academy! Please login.', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('users.register'))

    return render_template('users/register.html', title='Register Duelist')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.session.scalar(sa.select(User).where(User.username==username))
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('core.index')) # ล็อกอินแล้วส่งไปหน้าดูการ์ดทั้งหมด
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/login.html', title='Login')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('core.index'))

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        
        if firstname and lastname:
            current_user.first_name = firstname # ปรับให้ตรงกับโมเดล
            current_user.last_name = lastname
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('users.profile'))
    
    return render_template('users/profile.html', title='Duelist Profile')