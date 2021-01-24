from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired
from ..main.utils import *


class AddDeliveryForm(FlaskForm):
    delivery_name = StringField(LANGUAGES['Delivery name'][get_lenguage()], 
        validators=[DataRequired(), Length(max=50)], 
        render_kw={'autofocus': True})
    delivery_description = TextAreaField(LANGUAGES['Delivery description (optional)'][get_lenguage()], 
        validators=[Length(max=3000)])
    subject_name = SelectField(LANGUAGES['Subject'][get_lenguage()], 
        validators=[DataRequired()],
        choices=[])
    toDate = DateTimeLocalField(LANGUAGES['Delivery date'][get_lenguage()],
        validators=[InputRequired()],
        format='%Y-%m-%dT%H:%M')
    submit = SubmitField(LANGUAGES['Add'][get_lenguage()])