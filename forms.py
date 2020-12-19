from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[
        DataRequired(), Length(max=40)])
    identification = StringField('Identification', validators=[
        DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    identification = StringField('Identification', validators=[
        DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')