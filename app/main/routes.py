from flask import Blueprint
from app.models import Movie, User
import random
from flask import render_template

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')