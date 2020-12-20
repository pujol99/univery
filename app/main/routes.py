from flask import Blueprint
from app.models import *
import random
from flask_login import current_user
from flask import render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if not len(current_user.deliveries):
        return redirect(url_for('subjects.add_subject'))
    return render_template('home.html')