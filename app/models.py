from app import login_manager, db
from flask_login import UserMixin


class UserDelivery(db.Model):
    __tablename__ = 'userDelivery'
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    isDone = db.Column(db.Boolean, nullable=False, default=False)
    isEliminated = db.Column(db.Boolean, nullable=False, default=False)
    delivery = db.relationship("Delivery", back_populates="users")
    user = db.relationship("User", back_populates="deliveries")


class UserSubject(db.Model):
    __tablename__ = 'userSubject'
    subject_id = db.Column(db.String(15), db.ForeignKey('subject.identification'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    color = db.Column(db.String(10), nullable=False, default="#000")
    subject = db.relationship("Subject", back_populates="users")
    user = db.relationship("User", back_populates="subjects")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(70), nullable=False)
    identification = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)

    deliveries = db.relationship("UserDelivery", back_populates="user")
    subjects = db.relationship("UserSubject", back_populates="user")

    def __repr__(self):
        return f"User('{self.fullname}', '{self.identification }')"


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(15), nullable=False, default=0)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(1000))
    toDate = db.Column(db.DateTime, nullable=True)
    toDateStr = db.Column(db.String(20), nullable=True)
    url = db.Column(db.String(300), nullable=True)
    subject_id = db.Column(db.String(15), db.ForeignKey('subject.identification'), nullable=False)

    users = db.relationship("UserDelivery", back_populates="delivery")

    def __repr__(self):
        return f"Delivery('{self.name}', '{self.toDateStr}')"


class Subject(db.Model):
    identification = db.Column(db.String(15), nullable=False, primary_key=True)
    name = db.Column(db.String(70), nullable=False)

    users = db.relationship("UserSubject", back_populates="subject")
    deliveries = db.relationship('Delivery', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.name}', '{self.identification }')"