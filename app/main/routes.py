from flask import Blueprint, request
from app import db
from app.models import *
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for
from .utils import *

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    return render_template('delivery/not-done-deliveries.html', title="Home",
            deliveries=filter_deliveries(
                current_user.deliveries,
                lambda d: not d.isDone and not d.isEliminated),
            date_format=DATE_FORMAT)

@main.route("/done")
@login_required
def done_deliveries():
    return render_template('delivery/done-deliveries.html', title="Done",
            deliveries=get_deliveries_done(current_user.deliveries),
            date_format=DATE_FORMAT)

@main.route("/removed")
@login_required
def removed_deliveries():
    return render_template('delivery/removed-deliveries.html', title="Removed",
            deliveries=get_deliveries_removed(current_user.deliveries),
            date_format=DATE_FORMAT)