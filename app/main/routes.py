from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..deliveries.utils import *
from .utils import DATE_FORMAT, ACTIONS

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if not current_user.is_authenticated:
        return render_template('welcome.html', title="Welcome")
    
    return render_template('delivery/not-done-deliveries.html', title="Home", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: not d.isDone and not d.isEliminated and is_future(d.delivery.toDate)),
                date_format=DATE_FORMAT)

@main.route("/done")
@login_required
def done_deliveries():
    return render_template('delivery/done-deliveries.html', title="Done", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: d.isDone and not d.isEliminated and is_future(d.delivery.toDate)),
            date_format=DATE_FORMAT)

@main.route("/removed")
@login_required
def removed_deliveries():
    return render_template('delivery/removed-deliveries.html', title="Removed", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: d.isEliminated and is_future(d.delivery.toDate)),
            date_format=DATE_FORMAT)