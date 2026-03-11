from flask import Blueprint, render_template, request
import sqlalchemy as sa
# เปลี่ยนชื่อการ import ให้ตรงกับชื่อโฟลเดอร์และ Model ใหม่ของคุณ
from yugioh.models import db, Card, Type
from flask_login import login_required, current_user

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    # กำหนดค่าเริ่มต้นเป็นหน้า 1 ถ้าไม่มีการส่งค่า page มา
    page = request.args.get('page', 1, type=int) 
    
@core_bp.route('/')
@login_required # เพิ่มเพื่อให้ต้อง login ก่อนถึงจะเข้าหน้าโฮมได้
def index():
    page = request.args.get('page', 1, type=int)
    
    # แก้บรรทัดนี้: ใส่ .where เพื่อกรองให้เห็นเฉพาะการ์ดของตัวเอง
    query = sa.select(Card).where(Card.user_id == current_user.id) 
    cards = db.session.paginate(query, per_page=8, page=page)
    
    return render_template('core/index.html',
                           title='Yugioh Deck',
                           cards=cards)