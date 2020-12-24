from flask import Blueprint
from app import db
from app.models import *
from .forms import *
from ..main.utils import get_deliveries
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for

deliveries = Blueprint('deliveries', __name__)

@deliveries.route("/add-delivery", methods=['GET', 'POST'])
@login_required
def add_delivery():
    if not len(current_user.subjects):
        return redirect(url_for('subjects.subjects_page'))
    form = AddDeliveryForm()
    form.subject_id.choices = [subject.name for subject in 
                               db.session.query(Subject).filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        
        delivery = Delivery(
            name=form.delivery_name.data, description=form.delivery_description.data, 
            toDate=form.toDate.data, user_id=current_user.id, 
            subject_id=db.session.query(Subject).filter_by(name=form.subject_id.data).first().identification)
        db.session.add(delivery)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('delivery/add-delivery.html', title="Add delivery", form=form)

@deliveries.route("/delivery-done/<int:id>")
@login_required
def delivery_done(id):
    d = Delivery.query.filter_by(id=id).first()
    if d:
        d.isDone = True
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/delivery-undone/<int:id>")
@login_required
def delivery_undone(id):
    d = Delivery.query.filter_by(id=id).first()
    if d:
        d.isDone = False
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/delivery-remove/<int:id>")
@login_required
def delivery_remove(id):
    d = Delivery.query.filter_by(id=id).first()
    if d:
        d.isEliminated = True
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/update-deliveries")
@login_required
def update_deliveries():
    current_user.last_update = datetime.now()
    for delivery in get_deliveries():
        subject_id = delivery.subject_id
        delivery_name = delivery.name
        toDate = delivery.date
        existent_delivery = Delivery.query.filter_by(name=delivery_name,
                                                    subject_id=subject_id).first()
        if existent_delivery and existent_delivery.toDate != toDate:
            existent_delivery.toDate = toDate
        elif not existent_delivery:
            db.session.add(Delivery(name=delivery_name, toDate=toDate, 
                user_id=current_user.id, subject_id=subject_id))
    db.session.commit()
    return redirect(url_for('main.home'))
