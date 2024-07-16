import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Square(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)  # Başlık nullable olmalı
    notes = db.relationship('Note', back_populates='square', cascade='all, delete-orphan')
    key = db.Column(db.String(64), unique=True, nullable=False, default=uuid.uuid4().hex)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    square_key = db.Column(db.String(64), db.ForeignKey('square.key'), nullable=False)  # 64 olmalı
    square = db.relationship('Square', back_populates='notes')
