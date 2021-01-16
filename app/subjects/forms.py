from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
import re
from ..models import *
from ..global_utils import *

class AddSubjectForm(FlaskForm):
    subject_id = StringField("Subject ID",
        validators=[DataRequired(), Length(max=15)])
    subject_color = StringField('Subject Color (HEX)',
        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Add')
    
    def validate_subject_color(self, subject_color):
        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', subject_color.data):
            raise ValidationError('Invalid HEX color')