from app import db
from .models import *

from flask_login import current_user
from datetime import datetime

def UDnotDone():
    return db.session.query(UserDelivery).filter_by(
        user_id=current_user.id,
        isDone=False,
        isEliminated=False
    ).all()

def UDbySubject(subject_id):
    """
        Get the UserDelivery where the delivery is from
        subject (subject_id) and user (current_user)
    """
    return db.session.query(UserDelivery).join(
        Delivery, UserDelivery.delivery_id==Delivery.id
    ).filter(Delivery.subject_id==subject_id
    ).filter(UserDelivery.user_id==current_user.id
    ).all()

def UDbyDelivery(delivery_id):
    """
        Get the UserDelivery where the delivery is from
        delivery (delivery_id) and user (current_user)
    """
    return db.session.query(UserDelivery
    ).filter_by(
        delivery_id=delivery_id,
        user_id=current_user.id
    ).first()

def USbySubject(subject_id):
    """
        Get the UserSubject where the delivery is from
        delivery (delivery_id) and user (current_user)
    """
    return db.session.query(UserSubject).filter_by(
        subject_id=subject_id,
        user_id=current_user.id
    ).first()

def MDbySubject(subject_id):
    return db.session.query(Delivery).join(
        UserDelivery, Delivery.id==UserDelivery.delivery_id
    ).filter(UserDelivery.user_id==current_user.id
    ).filter(Delivery.identification==0
    ).filter(Delivery.subject_id==subject_id
    ).all()

def addDeliveryDB(name, id=None, description=None, toDate=None, subject_name=None, subject_id=None, url=None):
    d = Delivery(
        identification=id,
        name=name, 
        description=description, 
        toDate=toDate,
        toDateStr=str(toDate.date()),
        hasEnded=toDate<datetime.now(),
        subject_id=getSubject(subject_name).identification if subject_name else subject_id,
        url=url)
    db.session.add(d)
    db.session.commit()
    return d

def addSubjectDB(name, identification):
    db.session.add(Subject(
        identification=identification, 
        name=name))
    db.session.commit()

def addUserDB(fullname, identification, password):
    u = User(
        fullname=fullname, 
        identification=identification, 
        password=password)
    db.session.add(u)
    db.session.commit()
    return u

def addUserDeliveryDB(delivery_id):
    db.session.add(UserDelivery(
        delivery_id=delivery_id,
        user_id=current_user.id))
    db.session.commit()

def addUserSubjectDB(subject_id, user_id, color):
    db.session.add(UserSubject(  
        subject_id=subject_id,
        user_id=user_id, 
        color=color))
    db.session.commit()

def getSubject(name):
    return db.session.query(Subject
    ).filter_by(name=name
    ).first()

def getUser(identification):
    return db.session.query(User
    ).filter_by(identification=identification
    ).first()

def getDelivery(identification):
    return db.session.query(Delivery
    ).filter_by(identification=identification
    ).first()

def deleteElements(elements):
    for element in elements:
        db.session.delete(element)
    db.session.commit()

def deleteDelivery(elements):
    for element in elements:
        db.session.query(Delivery
            ).filter_by(id=element.id).delete()
    db.session.commit()

def updateDeliveryInfo(delivery, date, description):
    existent_delivery.description = description
    existent_delivery.toDate = date
    existent_delivery.toDateStr = str(date.date())
    db.session.commit()

def checkDeliveryEnded(delivery_id):
    d = getDelivery(delivery_id)
    if not d:
        return False
    return d.hasEnded