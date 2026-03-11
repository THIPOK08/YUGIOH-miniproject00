from flask import Blueprint, render_template, request
import sqlalchemy as sa
# เปลี่ยนชื่อการ import ให้ตรงกับชื่อโฟลเดอร์และ Model ใหม่ของคุณ
from yugioh.models import db, Card, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    # แก้ตรงนี้เพื่อแยกเด็คของใครของมัน
    query = sa.select(Card).where(Card.user_id == current_user.id) 
    cards = db.session.paginate(query, per_page=8, page=page)

    return render_template('core/index.html', title='Home', cards=cards)