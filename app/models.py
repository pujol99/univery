from app import login_manager, db
from flask_login import UserMixin

deliveries = db.Table('deliveries',
    db.Column('delivery_id', db.Integer, db.ForeignKey('delivery.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('isDone', db.Boolean, nullable=False, default=False),
    db.Column('isEliminated', db.Boolean, nullable=False, default=False)
)

subjects = db.Table('subjects',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('color', db.String(10), nullable=False, default="#000")
)   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    identification = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)

    deliveries = db.relationship('Delivery', secondary=deliveries, lazy='subquery',
        backref=db.backref('users', lazy=True))
    subjects = db.relationship('Subject', secondary=subjects, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"User('{self.fullname}', '{self.identification }')"


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(400))
    toDate = db.Column(db.DateTime, nullable=True)
    toDateStr = db.Column(db.String(20), nullable=True)
    url = db.Column(db.String(300), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    def __repr__(self):
        return f"Delivery('{self.name}', '{self.toDateStr}')"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Subject('{self.name}', '{self.identification }')"