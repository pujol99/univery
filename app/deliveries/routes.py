from flask import Blueprint
from app import db
from app.models import *
from .forms import *
from ..main.utils import get_deliveries
from .utils import clean_description
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for
from datetime import datetime

deliveries = Blueprint('deliveries', __name__)

@deliveries.route("/add-delivery", methods=['GET', 'POST'])
@login_required
def add_delivery():
    # At least one subject to add deliveries
    if not current_user.subjects:
        return redirect(url_for('subjects.subjects_page'))
    
    # Set the subject choice to the subject names of the user
    form = AddDeliveryForm()
    form.subject_id.choices = [subject.name for subject in 
                               db.session.query(Subject).filter_by(user_id=current_user.id).all()]
    
    # POST method
    if form.validate_on_submit():
        db.session.add(Delivery(
            name=form.delivery_name.data, 
            description=clean_description(form.delivery_description.data), 
            toDate=form.toDate.data, 
            user_id=current_user.id, 
            subject_id=db.session.query(Subject).filter_by(name=form.subject_id.data).first().identification))
        db.session.commit()
        return redirect(url_for('main.home'))

    # GET method
    return render_template('delivery/add-delivery.html', title="Add delivery", form=form)

@deliveries.route("/delivery-done/<int:id>")
@login_required
def delivery_done(id):
    # Mark delivery as done
    delivery = Delivery.query.filter_by(id=id).first()
    if delivery:
        delivery.isDone = True
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/delivery-undone/<int:id>")
@login_required
def delivery_undone(id):
    # Mark delivery as not done
    delivery = Delivery.query.filter_by(id=id).first()
    if delivery:
        delivery.isDone = False
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/delivery-remove/<int:id>")
@login_required
def delivery_remove(id):
    # Mark delivery as eliminated
    delivery = Delivery.query.filter_by(id=id).first()
    if delivery:
        delivery.isEliminated = True
        db.session.commit()
    return redirect(url_for('main.home'))

@deliveries.route("/update-deliveries")
@login_required
def update_deliveries():
    # Update user's last update time
    current_user.last_update = datetime.now()

    # Read all the deliveries from {user.subjects} university pages
    for delivery in get_deliveries():
        # Check if the delivery is already on our database
        subject_id = delivery.subject_id
        delivery_name = delivery.name
        delivery_description = delivery.description
        toDate = delivery.date
        existent_delivery = Delivery.query.filter_by(
            name=delivery_name,
            subject_id=subject_id).first()

        # If it exists check for date changes else add the new delivery to our db
        if existent_delivery and existent_delivery.toDate != toDate:
            existent_delivery.toDate = toDate
        elif not existent_delivery:
            db.session.add(Delivery(
                name=delivery_name,
                description=delivery_description,
                toDate=toDate, 
                user_id=current_user.id, 
                subject_id=subject_id))
    db.session.commit()
    return redirect(url_for('main.home'))
