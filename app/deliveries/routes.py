from app import db
from app.models import *
from .forms import *
from ..main.utils import *
from ..global_utils import * 
from .utils import *

from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for
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
        delivery = addDeliveryDB(
            name=form.delivery_name.data, 
            description=clean_description(form.delivery_description.data),
            toDate=form.toDate.data, 
            subject_name=form.subject_name.data)
        addUserDeliveryDB(delivery.id)

        return redirect_to('main.home')

    # GET method
    return render_template('delivery/add-delivery.html', title="Add delivery", form=form)

@deliveries.route("/delivery/<string:action>/<int:id>")
@login_required
def delivery(action, id):
    # Modify delivery state
    delivery = UDbyDelivery(id)

    if delivery:
        if action == "done":
            delivery.isDone = True
        elif action == "undone":
            delivery.isDone = False
        elif action == "remove":
            delivery.isEliminated = True
        else:
            delivery.isEliminated = False
            delivery.isDone = False
        db.session.commit()
    
    return redirect_to('main.home')


@deliveries.route("/calendar")
@deliveries.route("/calendar/<int:n>")
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

    current_user.last_update = datetime.now()

    # Read all the DeliveryObjects from {user.subjects} university pages
    for d in get_deliveries(current_user.subjects, session["password"]):
        # Check if the Delivery is already on our database
        ed = getDelivery(d.id) # Existent Delivery object

        if not ed:
            # Add deliveries to DB
            delivery = addDeliveryDB(
                d.name, d.id, d.description, 
                d.date, None, d.subject_id, d.url)
            addUserDeliveryDB(delivery.id)
        else:
            # Update old existing Delivery
            if ed.toDate != d.date or ed.description != d.description:
                updateDeliveryInfo(ed, d.date, d.description)
            
            # Check if the UserDelivery is already on our database
            delivery_id = getDelivery(d.id).id
            if not UDbyDelivery(delivery_id):
                addUserDeliveryDB(delivery_id)

    return redirect_to('main.home')
