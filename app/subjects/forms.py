from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError


class AddSubjectForm(FlaskForm):
    subject_id = StringField('Subject ID',
        validators=[DataRequired(), Length(max=15)])
    subject_color = StringField('Subject Color (HEX)',
        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Add')