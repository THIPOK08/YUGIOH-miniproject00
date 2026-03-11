from flask import Blueprint, render_template, request
import sqlalchemy as sa
# เปลี่ยนชื่อการ import ให้ตรงกับชื่อโฟลเดอร์และ Model ใหม่ของคุณ
from yugioh.models import db, Card, Type

core_bp = Blueprint('core', __name__, template_folder='templates')

@core_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    cards = db.paginate(sa.select(Card), per_page=8, page=page)

    return render_template('core/index.html',
                           title='Yugioh Deck',
                           cards=cards)

@core_bp.route('/card/<int:id>')
def detail(id):
    card = db.session.get(Card, id)

    return render_template('core/yugioh_detail.html',
                           title='Card Details',
                           card=card)