from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    personal_info = db.Column(db.String(100))
    password = db.Column(db.String(60), nullable=False)
    my_likes = db.relationship('Like', backref='user_like', lazy=True)
    n_likes = db.Column(db.Integer, default=0)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mark = db.Column(db.Float, default=0.00)
    release_year = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='movie')

    def __repr__(self):
        return f"Movie('{self.name}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    movie_mark = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_likes = db.relationship('Like', backref='review_like', lazy=True)
    n_likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
    def __repr__(self):
        return f"Review('{self.title}', '{self.user_id}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.user_id}', '{self.review_id}')"