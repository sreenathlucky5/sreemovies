from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sreemovies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Your simple route data (FIXED SYNTAX)
Profit = [{
    'name': 'screenath',
    'age': 20,
    'salary': 20000
}]  # Removed the extra } that was causing the syntax error

# Models (from SreeMovies)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(20), default='Telugu')
    cover_image = db.Column(db.String(100), default='default_book.jpg')
    synopsis = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    release_date = db.Column(db.Date)
    is_featured = db.Column(db.Boolean, default=False)

class ReadingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    session_time = db.Column(db.DateTime, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, default=0.0)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('reading_session.id'), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    seats = db.Column(db.Integer, default=1)

# Your simple route
@app.route('/simple')
def hollo_sreenath():
    return render_template('home.html', profit=Profit)

# SreeMovies routes
@app.route('/')
def home():
    featured_books = Book.query.filter_by(is_featured=True).limit(5).all()
    upcoming_books = Book.query.filter(Book.release_date > datetime.now()).order_by(Book.release_date).limit(5).all()
    return render_template('index.html', featured_books=featured_books, upcoming_books=upcoming_books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    sessions = ReadingSession.query.filter_by(book_id=book_id).filter(ReadingSession.session_time > datetime.now()).all()
    return render_template('book.html', book=book, sessions=sessions)

# ... (keep all other SreeMovies routes from the previous code)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add sample data if needed
        if not Book.query.first():
            sample_book = Book(
                title="Veyi Padagalu",
                author="Viswanatha Satyanarayana",
                genre="Classic Fiction",
                synopsis="A monumental work in Telugu literature...",
                release_date=datetime(2023, 11, 15),
                is_featured=True,
                cover_image="veyi_padagalu.jpg",
                rating=4.7
            )
            db.session.add(sample_book)
            db.session.commit()
    app.run(host='0.0.0.0', debug=True)