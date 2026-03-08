from flask import Blueprint, render_template, request, flash, redirect, url_for
# ตรวจสอบชื่อโฟลเดอร์โปรเจกต์ (ถ้าไม่ใช่ pokemon ให้แก้ตรงนี้ด้วยครับ)
from yugioh.extensions import db 
from yugioh.models import Card, Type, User # เปลี่ยนจาก Pokemon เป็น Card
from flask_login import login_required, current_user
import sqlalchemy as sa

# เปลี่ยนชื่อ Blueprint เป็น card_bp หรือคงเดิมไว้ก็ได้ แต่ในที่นี้ผมปรับให้สื่อสารง่ายขึ้น
yugioh_bp = Blueprint('card', __name__, template_folder='templates')

@card_bp.route('/')
@login_required
def index():
    # ดึงเฉพาะการ์ดที่เป็นของ User คนที่ล็อกอินอยู่ (My Collection)
    query = sa.select(Card).where(Card.user_id == current_user.id)
    cards = db.session.scalars(query).all()
    return render_template('yugioh/index.html', # ใช้ไฟล์เดิมที่คุณมี
                           title='My Card Collection',
                           cards=cards)

@card_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_card():
    # ดึงประเภทการ์ด (เช่น Monster, Spell, Trap) มาแสดงใน Dropdown
    query = sa.select(Type)
    card_types = db.session.scalars(query).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        atk = request.form.get('ATK')   # รับค่าจากช่อง ATK ในฟอร์ม
        def_val = request.form.get('DEF') # รับค่าจากช่อง DEF ในฟอร์ม
        description = request.form.get('description')
        img_url = request.form.get('img_url')
        selected_types = request.form.getlist('yugioh_types')

        # จัดการเรื่องความสัมพันธ์ Many-to-Many ของ Types
        p_types = []
        for type_id in selected_types:
            t = db.session.get(Type, type_id)
            if t:
                p_types.append(t)

        # ตรวจสอบว่าชื่อการ์ดซ้ำในระบบหรือไม่
        check_query = sa.select(Card).where(Card.name == name)
        existing_card = db.session.scalar(check_query)
        
        if existing_card:
            flash(f'Card: {name} already exists in the database!', 'warning')
            return redirect(url_for('card.new_card'))
        
        # สร้าง Object การ์ดใหม่
        new_card_obj = Card(
            name=name,
            height=atk,        # แมตช์กับ Field ใน DB เดิม
            weight=def_val,    # แมตช์กับ Field ใน DB เดิม
            description=description,
            img_url=img_url,
            user_id=current_user.id,
            types=p_types
        )
        
        try:
            db.session.add(new_card_obj)
            db.session.commit()
            flash('Registered new card to your deck successful!', 'success')
            return redirect(url_for('card.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('yugioh/yugioh.html', # ใช้ไฟล์เดิมที่คุณมี
                           title='Register New Card',
                           pokemon_types=card_types)