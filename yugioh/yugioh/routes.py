from flask import Blueprint, render_template, request, flash, redirect, url_for
# ตรวจสอบชื่อโฟลเดอร์โปรเจกต์ (ถ้าไม่ใช่ pokemon ให้แก้ตรงนี้ด้วยครับ)
from yugioh.extensions import db 
from yugioh.models import Card, Type, User # เปลี่ยนจาก Pokemon เป็น Card
from flask_login import login_required, current_user
import sqlalchemy as sa

# เปลี่ยนชื่อ Blueprint เป็น card_bp หรือคงเดิมไว้ก็ได้ แต่ในที่นี้ผมปรับให้สื่อสารง่ายขึ้น
yugioh_bp = Blueprint('card', __name__, template_folder='templates')

@yugioh_bp.route('/')
@login_required
def index():
    # ดึงเฉพาะการ์ดที่เป็นของ User คนที่ล็อกอินอยู่ (My Collection)
    query = sa.select(Card).where(Card.user_id == current_user.id)
    cards = db.session.scalars(query).all()
    return render_template('yugioh/index.html', # ใช้ไฟล์เดิมที่คุณมี
                           title='My Card Collection',
                           cards=cards)

@yugioh_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_card():
    # ดึงประเภทการ์ด (เช่น Monster, Spell, Trap) มาแสดงใน Dropdown
    query = sa.select(Type)
    card_types = db.session.scalars(query).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        atk = request.form.get('atk')   # รับค่าจากช่อง ATK ในฟอร์ม
        def_val = request.form.get('def_val') # รับค่าจากช่อง DEF ในฟอร์ม
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
      # แก้ไขส่วนการสร้าง Object ใน routes.py
        new_card_obj = Card(
           name=name,
           height=atk,        # ใช้ตัวแปร atk ที่รับมาจาก request.form.get('atk')
           weight=def_val,    # ใช้ตัวแปร def_val ที่รับมาจาก request.form.get('def_val')
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

    return render_template('yugioh/new_yugioh.html', # ใช้ไฟล์เดิมที่คุณมี
                           title='Register New Card',
                           card_types=card_types)

@yugioh_bp.route('/setup-types')
def setup_types():
    # ลิสต์ข้อมูลประเภทการ์ดที่ต้องการเพิ่ม
    default_types = ['Monster', 'Spell', 'Trap']
    
    try:
        for t_name in default_types:
            # ตรวจสอบว่ามีชื่อนี้อยู่ในตาราง Type หรือยัง
            exists = db.session.scalar(sa.select(Type).where(Type.name == t_name))
            if not exists:
                new_type = Type(name=t_name)
                db.session.add(new_type)
        
        db.session.commit()
        return "สำเร็จ! เพิ่มข้อมูลประเภทการ์ดเรียบร้อยแล้ว ลองไปเช็คที่หน้า /new ดูนะ"
    except Exception as e:
        db.session.rollback()
        return f"เกิดข้อผิดพลาด: {str(e)}"
    
@yugioh_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    # ดึงข้อมูลการ์ดตาม id ที่ส่งมา
    card = db.session.get(Card, id)
    
    # ถ้าไม่เจอการ์ด หรือการ์ดนั้นไม่ใช่ของ User คนที่ล็อกอินอยู่ ให้เด้งกลับ
    if not card or card.user_id != current_user.id:
        flash('Card not found!', 'danger')
        return redirect(url_for('card.index'))
    
    return render_template('yugioh/detail.html', # นายต้องมีไฟล์ detail.html ในโฟลเดอร์ templates/yugioh ด้วยนะ
                           title=card.name,
                           card=card)

@yugioh_bp.route('/cleanup-types')
def cleanup_types():
    # ระบุชื่อที่จะลบ (Dragon และ Warrior ที่นายไม่อยากได้แล้ว)
    to_delete = ['Dragon', 'Warrior']
    try:
        for name in to_delete:
            # ค้นหาชื่อในตาราง Type ของฐานข้อมูล
            t = db.session.scalar(sa.select(Type).where(Type.name == name))
            if t:
                db.session.delete(t) # สั่งลบข้อมูลทิ้ง
        
        db.session.commit() # ยืนยันการลบ
        return "ลบ Dragon และ Warrior ออกจากฐานข้อมูลสำเร็จ! ลองกลับไปหน้า /new ดูนะ"
    except Exception as e:
        db.session.rollback() # ถ้าพลาดให้ดึงข้อมูลกลับมา
        return f"เกิดข้อผิดพลาด: {str(e)}"