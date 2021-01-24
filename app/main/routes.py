from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..deliveries.utils import *
from .utils import *

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if not current_user.is_authenticated:
        return render_template('welcome.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Welcome")
    
    return render_template('delivery/not-done-deliveries.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Home", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: not d.isDone and not d.isEliminated and is_future(d.delivery.toDate)),
                date_format=DATE_FORMAT)

@main.route("/done")
@login_required
def done_deliveries():
    return render_template('delivery/done-deliveries.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Done", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: d.isDone and not d.isEliminated and is_future(d.delivery.toDate)),
            date_format=DATE_FORMAT)

@main.route("/removed")
@login_required
def removed_deliveries():
    return render_template('delivery/removed-deliveries.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Removed", actions=ACTIONS,
            deliveries=filter_deliveries(
                lambda d: d.isEliminated and is_future(d.delivery.toDate)),
            date_format=DATE_FORMAT)

@main.route("/language/<lan>")
def language(lan):
    update_lenguage(lan)
    return redirect(url_for('main.home'))