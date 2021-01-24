from flask import Blueprint, render_template, url_for, redirect, request, session
from app import db, bcrypt
from .utils import check_user
from ..main.utils import *
from .forms import *
from app.models import *
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if check_user(form.identification.data, form.password.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = addUserDB(
                fullname=form.fullname.data, 
                identification=form.identification.data, 
                password=hashed_password)
            login_user(user)
            session["password"] = form.password.data
            return redirect(url_for('subjects.subjects_list'))
        return render_template('user/register.html', lenguages=LANGUAGES, cl=get_lenguage(), title='Register', form=form, 
                message="Incorrect identification or password for universty login")
    
    return render_template('user/register.html', lenguages=LANGUAGES, cl=get_lenguage(), title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = getUser(form.identification.data)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session["password"] = form.password.data
            return redirect(url_for('main.home'))
        return render_template('user/login.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Login", form=form,
            message="Incorrect identification or password")

    return render_template('user/login.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Login", form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdatePassword()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        return redirect(url_for('main.home'))
    
    return render_template('user/account.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Account", form=form)
    


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))