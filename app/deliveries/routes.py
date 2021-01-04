from app import db
from app.models import *
from .forms import *
from ..main.utils import *
from .utils import *

from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, abort
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
    form.subject_name.choices = [us.subject.name
        for us in current_user.subjects]
    
    # POST method - Add Delivery to DB and add relation between delivery and user
    if form.validate_on_submit():
        addDeliveryDB(
            None, form.delivery_name.data, form.delivery_description.data,
            form.toDate.data, form.subject_name.data, None, None)
        addUserDeliveryDB(
            db.session.query(Delivery)
            .order_by(Delivery.id.desc())
            .first().id)

        db.session.commit()

        next_page = request.args.get('next')
        if not isSafeUrl(next_page):
            return abort(400)
        return redirect(url_for(next_page if next_page else 'main.home'))

    # GET method
    return render_template('delivery/add-delivery.html', title="Add delivery", form=form)

@deliveries.route("/delivery-done/<int:id>")
@login_required
def delivery_done(id):
    # Mark delivery as done
    delivery = UserDelivery.query.filter_by(
        delivery_id=id, user_id=current_user.id
    ).first()

    if delivery:
        delivery.isDone = True
        db.session.commit()
    
    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
            return abort(400)
    return redirect(url_for(next_page if next_page else 'main.home'))

@deliveries.route("/delivery-undone/<int:id>")
@login_required
def delivery_undone(id):
    # Mark delivery as not done
    delivery = UserDelivery.query.filter_by(
        delivery_id=id, user_id=current_user.id
    ).first()

    if delivery:
        delivery.isDone = False
        db.session.commit()

    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
            return abort(400)
    return redirect(url_for(next_page if next_page else 'main.done_deliveries'))

@deliveries.route("/delivery-remove/<int:id>")
@login_required
def delivery_remove(id):
    # Mark delivery as eliminated
    delivery = UserDelivery.query.filter_by(
        delivery_id=id, user_id=current_user.id
    ).first()

    if delivery:
        delivery.isEliminated = True
        db.session.commit()

    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
            return abort(400)
    return redirect(url_for(next_page if next_page else 'main.home'))

@deliveries.route("/delivery-restore/<int:id>")
@login_required
def delivery_restore(id):
    # Mark delivery as not eliminated
    delivery = UserDelivery.query.filter_by(
        delivery_id=id, user_id=current_user.id
    ).first()

    if delivery:
        delivery.isEliminated = False
        delivery.isDone = False
        db.session.commit()

    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
            return abort(400)
    return redirect(url_for(next_page if next_page else 'main.removed_deliveries'))

@deliveries.route("/calendar/<int:n>")
@deliveries.route("/calendar")
@login_required
def calendar(n=0):
    days, month = get_days(14, n)
    return render_template('delivery/calendar.html', title="Calendar",
        days=days, month=month, view=n)


@deliveries.route("/update-deliveries")
@login_required
def update_deliveries():
    #Check that at least has one subject
    if not current_user.subjects:
        return redirect(url_for('subjects.subjects_page'))

    # Update user's last update time
    current_user.last_update = datetime.now()

    # Read all the DeliveryObjects from {user.subjects} university pages
    for delivery in get_deliveries(current_user.subjects):
        identification = delivery.id
        date = delivery.date
        description = delivery.description

        # Check if the delivery is already on our database
        existent_delivery = Delivery.query.filter_by(
            identification=identification).first()

        if not existent_delivery:
            # Add deliveries to DB
            addDeliveryDB(
                identification, delivery.name, description, 
                date, None, delivery.subject_id, delivery.url)
            addUserDeliveryDB(
                db.session.query(Delivery)
                .order_by(Delivery.id.desc())
                .first().id)
        else:
            # Update old existing delivery
            if existent_delivery.toDate != date or existent_delivery.description != description:
                existent_delivery.description = description
                existent_delivery.toDate = date
                existent_delivery.toDateStr = str(date.date())
            
            # Check if the userDelivery is already on our database
            delivery_id = db.session.query(Delivery
                ).filter_by(identification=identification
                ).first().id
    
            existent_userDelivery = UserDelivery.query.filter_by(
                delivery_id=delivery_id,
                user_id=current_user.id).first()
            
            if not existent_userDelivery:
                addUserDeliveryDB(delivery_id)

    db.session.commit()

    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
            return abort(400)
    return redirect(url_for(next_page if next_page else 'main.home'))
