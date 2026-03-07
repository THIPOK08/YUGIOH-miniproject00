from flask import Blueprint, render_template, request
import sqlalchemy as sa
# เปลี่ยนชื่อการ import ให้ตรงกับชื่อโฟลเดอร์และ Model ใหม่ของคุณ
from models import db, Card, Type 

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    # กำหนดค่าเริ่มต้นเป็นหน้า 1 ถ้าไม่มีการส่งค่า page มา
    page = request.args.get('page', 1, type=int) 
    
    # เปลี่ยนจาก Pokemon เป็น Card และปรับจำนวนต่อหน้า (per_page) ตามเหมาะสม
    cards = db.paginate(sa.select(Card), per_page=8, page=page)
    
    return render_template('core/index.html',
                           title='Yugioh Deck',
                           cards=cards) # ส่งตัวแปรชื่อ cards ไปให้ HTML

@core_bp.route('/card/<int:id>')
def detail(id):
    # ดึงข้อมูลการ์ดตาม ID
    card = db.session.get(Card, id)
    
    return render_template('core/pokemon_detail.html', # ชื่อไฟล์เดิมที่คุณใช้
                           title='Card Details',
                           card=card) # ส่งตัวแปรชื่อ card ไปให้ HTML