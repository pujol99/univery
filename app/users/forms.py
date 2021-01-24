from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app import bcrypt

from .utils import *
from ..main.utils import *
from ..global_utils import *
from ..models import *


class RegistrationForm(FlaskForm):
    fullname = StringField(LANGUAGES['Fullname'][get_lenguage()],
        validators=[DataRequired(), Length(max=40)])
    identification = StringField(LANGUAGES['University identification'][get_lenguage()], 
        validators=[DataRequired(), Length(max=15)])
    password = PasswordField(LANGUAGES['University password'][get_lenguage()], 
        validators=[DataRequired()])
    submit = SubmitField(LANGUAGES['Sign up'][get_lenguage()])

    def validate_identification(self, identification):
        # If user identification exists -> error
        if getUser(identification.data):
            raise ValidationError('That identification is taken.')

class LoginForm(FlaskForm):
    identification = StringField(LANGUAGES['University identification'][get_lenguage()], 
        validators=[DataRequired(), Length(max=15)])
    password = PasswordField(LANGUAGES['University password'][get_lenguage()], 
        validators=[DataRequired()])
    submit = SubmitField(LANGUAGES['Login'][get_lenguage()])

class UpdatePassword(FlaskForm):
    password = PasswordField(LANGUAGES['Password'][get_lenguage()], 
        validators=[DataRequired()])
    submit = SubmitField(LANGUAGES['Update'][get_lenguage()])

    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user.password, password.data):
            raise ValidationError(LANGUAGES['That is your current password'][get_lenguage()])
        if not check_user(current_user.identification, password.data):
            raise ValidationError(LANGUAGES['That password doesnt pass the login in the university'][get_lenguage()])
