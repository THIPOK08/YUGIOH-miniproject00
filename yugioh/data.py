
# รายการธาตุ (Attributes) ของการ์ดยูกิโอ
yugioh_attributes = [
    'DARK', 'LIGHT', 'EARTH', 'WATER', 'FIRE', 'WIND', 'DIVINE',
    'Monster', 'Spell', 'Trap' # แถมประเภทหลักของการ์ดไปด้วยเลย
]

from models import Type # มั่นใจว่า import จาก models ที่เราแก้แล้ว
# สร้าง Object เพื่อเตรียม Save ลง Database
types = [Type(name=attr) for attr in yugioh_attributes]