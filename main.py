from yugioh import create_app
from yugioh.extensions import db  # เพิ่มบรรทัดนี้เพื่อดึงตัวจัดการฐานข้อมูลมาใช้

app = create_app()

# เพิ่มส่วนนี้ลงไปครับ
with app.app_context():
    db.create_all()
