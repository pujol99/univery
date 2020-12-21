from flask import Blueprint
from app import db
from app.models import *
from .forms import *
from ..main.utils import get_deliveries
from flask_login import current_user
from flask import render_template, redirect, url_for

deliveries = Blueprint('deliveries', __name__)

@deliveries.route("/add-delivery", methods=['GET', 'POST'])
def add_delivery():
    return redirect(url_for('main.home'))


@deliveries.route("/update-deliveries")
def update_deliveries():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    for delivery in get_deliveries():
        subject_id = delivery.subject_id
        delivery_name = delivery.name
        toDate = delivery.date
        existent_delivery = Delivery.query.filter_by(name=delivery_name,
                                                    subject_id=subject_id).first()
        if existent_delivery and existent_delivery.toDate != toDate:
            existent_delivery.toDate = toDate
            db.session.commit()
        elif not existent_delivery:
            db.session.add(Delivery(name=delivery_name, toDate=toDate, 
                user_id=current_user.id, subject_id=subject_id, isDone=False))
            db.session.commit()
    return redirect(url_for('main.home'))
