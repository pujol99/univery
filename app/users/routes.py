from flask import Blueprint
from flask import render_template, url_for, redirect, request
from app import db, bcrypt
from ..main.utils import check_user
from .forms import *
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit() and check_user(form.identification.data, form.password.data):
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, identification=form.identification.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('user/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(identification=form.identification.data).first()
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
    return render_template('user/login.html', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))