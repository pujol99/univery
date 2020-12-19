from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[
        DataRequired(), Length(max=40)])
    identification = StringField('Identification', validators=[
        DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    def validate_identification(self, identification):
        user = User.query.filter_by(identification=identification.data).first()
        if user:
            raise ValidationError('That identification is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    identification = StringField('Identification', validators=[
        DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')