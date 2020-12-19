from flask import Blueprint
import os
from random import choice
from flask import render_template, url_for, redirect, request
from app import db, bcrypt
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Review, Like, Movie
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql.expression import func
from .utils import save_picture

DEFAULT_IMG = ['def1.jpg', 'def2.jpg', 'def3.jpg', 'def4.jpg', 'def5.jpg']
users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file=choice(DEFAULT_IMG))
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            next_page = request.args.get('next')
            login_user(user)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template('user/login.html', form=form)

@users.route("/account/<int:user_id>")
def account(user_id):
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(user_id=user_id).paginate(page=page, per_page=5)
    user = User.query.get_or_404(user_id)
    likes = Like.query
    return render_template('user/account.html', user=user, reviews=reviews, likes=likes)

@users.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.description.data:
            current_user.personal_info = form.description.data
        db.session.commit()
        return redirect(url_for('users.account', user_id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.personal_info:
            form.description.data = current_user.personal_info
    return render_template('user/update_account.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))