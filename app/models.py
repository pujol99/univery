from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    identification = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    deliveries = db.relationship('Delivery', backref='user', lazy=True)
    subjects = db.relationship('Subject', backref='user', lazy=True)
    last_update = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.identification }')"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deliveries = db.relationship('Delivery', backref='subject', lazy=True)
    color = db.Column(db.String(10), nullable=False, default="#ffffff")

    def __repr__(self):
        return f"Subject('{self.name}', '{self.identification }')"

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(400))
    toDate = db.Column(db.DateTime, nullable=True)
    toDateStr = db.Column(db.String(20), nullable=True)
    url = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    isDone = db.Column(db.Boolean, nullable=False, default=False)
    isEliminated = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Delivery('{self.name}', '{self.toDateStr }')"
