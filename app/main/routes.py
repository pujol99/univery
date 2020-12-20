from flask import Blueprint
from app.models import *
import random
from ..users.utils import check_user, update_deliveries
from flask_login import current_user
from flask import render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if len(current_user.subjects) == 0:
        return redirect(url_for('subjects.add_subject'))
    for d in update_deliveries():
        print(d)
    return render_template('home.html')