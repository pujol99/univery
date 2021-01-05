from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from ..models import *
from ..global_utils import *
from flask_login import current_user

class AddSubjectForm(FlaskForm):
    subject_id = StringField('Subject ID',
        validators=[DataRequired(), Length(max=15)])
    subject_color = StringField('Subject Color (HEX)',
        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Add')

    def validate_subject_id(self, subject_id):
        # If UserSubject exists -> error
        if USbySubject(subject_id.data):
            raise ValidationError('This subject already exists. Please choose a different one.')