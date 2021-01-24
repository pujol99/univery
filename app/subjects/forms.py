from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
import re
from ..models import *
from ..global_utils import *
from ..main.utils import *

class AddSubjectForm(FlaskForm):
    subject_id = StringField(LANGUAGES["Subject ID"][get_lenguage()],
        validators=[DataRequired(), Length(max=15)])
    subject_color = StringField(LANGUAGES['Subject Color'][get_lenguage()],
        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField(LANGUAGES['Add'][get_lenguage()])
    
    def validate_subject_color(self, subject_color):
        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', subject_color.data):
            raise ValidationError(LANGUAGES['Invalid HEX color'][get_lenguage()])