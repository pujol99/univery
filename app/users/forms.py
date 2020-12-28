from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from ..main.utils import check_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname',
        validators=[DataRequired(), Length(max=40)])
    identification = StringField('Identification', 
        validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_identification(self, identification):
        # If user identification exists -> error
        if User.query.filter_by(identification=identification.data).first():
            raise ValidationError('That identification is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    identification = StringField('Identification', 
        validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdatePassword(FlaskForm):
    password = PasswordField('Password', 
        validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_password(self, password):
        if password.data == current_user.password:
            raise ValidationError('That is your current password')
        if not check_user(current_user.identification, password.data):
            raise ValidationError('That password doesnt pass the login in the university')
