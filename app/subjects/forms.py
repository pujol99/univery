from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import User


class AddSubjectForm(FlaskForm):
    subject_id = StringField('Subject ID', validators=[
        DataRequired(), Length(max=15)])
    submit = SubmitField('Add')