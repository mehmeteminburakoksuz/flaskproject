import uuid
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from .models import db, Square, Note

app = Flask(__name__)

# Veritabanı bağlantı bilgilerini çevre değişkenlerinden al
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # db'yi Flask uygulamasına bağla

with app.app_context():
    db.create_all()  # Veritabanı tablolarını oluştur

def hash_id(id):
    return hashlib.sha256(str(id).encode()).hexdigest()

app.jinja_env.filters['hash_id'] = hash_id

@app.route('/')
def index():
    squares = Square.query.all()
    return render_template('index.html', squares=squares)

@app.route('/add', methods=['POST'])
def add_square():
    title = request.form.get('title')  # Formdan başlığı al
    square_key = uuid.uuid4().hex
    new_square = Square(title=title, key=square_key)  # Yeni kareyi başlık ile oluştur

    db.session.add(new_square)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/square/<key>', methods=['GET', 'POST'])
def view_square(key):
    square_record = Square.query.filter_by(key=key).first()
    if not square_record:
        return redirect(url_for('index'))

    if request.method == 'POST':
        return handle_post(square_record)
    return handle_get(square_record)

def handle_get(square_record):
    return render_template('square.html', square=square_record)

def handle_post(square_record):
    if 'title' in request.form:
        square_record.title = request.form['title']
        db.session.commit()
    elif 'note' in request.form:
        new_note = Note(content=request.form['note'], square=square_record)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('view_square', key=square_record.key))

@app.route('/list')
def list_squares():
    squares = Square.query.all()
    return render_template('list.html', squares=squares)

if __name__ == '__main__':
    app.run(debug=True)
