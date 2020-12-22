from flask import Blueprint
from app import db
from app.models import *
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for
from .utils import get_deliveries_done, get_deliveries_todo

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    return render_template('home.html', 
            deliveries_todo=get_deliveries_todo(current_user.deliveries),
            deliveries_done=get_deliveries_done(current_user.deliveries))
