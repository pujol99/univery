from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..deliveries.utils import *
from .utils import DATE_FORMAT

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if not current_user.is_authenticated:
        return render_template('welcome.html', title="Welcome")
    
    return render_template('delivery/not-done-deliveries.html', title="Home",
            deliveries=filter_deliveries(
                current_user.deliveries,
                lambda d: not d.isDone and not d.isEliminated),
            date_format=DATE_FORMAT)

@main.route("/done")
@login_required
def done_deliveries():
    return render_template('delivery/done-deliveries.html', title="Done",
            deliveries=filter_deliveries(
                current_user.deliveries,
                lambda d: d.isDone and not d.isEliminated),
            date_format=DATE_FORMAT)

@main.route("/removed")
@login_required
def removed_deliveries():
    return render_template('delivery/removed-deliveries.html', title="Removed",
            deliveries=filter_deliveries(
                current_user.deliveries,
                lambda d: d.isEliminated == True),
            date_format=DATE_FORMAT)