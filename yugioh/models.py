from yugioh.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, Table, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin

# User Loader สำหรับ Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)
    avatar: Mapped[str] = mapped_column(String(25), nullable=True, default='avatar.png')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # เปลี่ยนจาก pokemons เป็น cards
    cards: Mapped[List['Card']] = relationship(back_populates='user')
    
    def __repr__(self):
        return f'<User: {self.username}>'

# เปลี่ยนชื่อตารางกลางจาก pokedex เป็น card_types (Many-to-Many)
card_types = Table(
    'card_types',
    db.metadata,
    Column('type_id', Integer, ForeignKey('type.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('card.id'), primary_key=True)
)  

class Type(db.Model):
    __tablename__ = 'type'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    # เปลี่ยนความสัมพันธ์ให้ชี้ไปที่ Card
    cards: Mapped[List['Card']] = relationship(back_populates='types', secondary=card_types)
    
    def __repr__(self):
        return f'<Type: {self.name}>'
  
class Card(db.Model): # เปลี่ยนชื่อ Class จาก Pokemon เป็น Card
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    # เราใช้ height แทน ATK และ weight แทน DEF ตามที่ตกลงกันเพื่อความง่าย
    height: Mapped[str] = mapped_column(String(20), nullable=False) 
    weight: Mapped[str] = mapped_column(String(20), nullable=False) 
    description: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates='cards')
    types: Mapped[List['Type']] = relationship(back_populates='cards', secondary=card_types)
    
    def __repr__(self):
        return f'<Card: {self.name}>'