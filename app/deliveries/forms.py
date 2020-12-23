from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeLocalField, DateField
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, InputRequired
from datetime import datetime


class AddDeliveryForm(FlaskForm):
    delivery_name = StringField('Delivery name', validators=[DataRequired(), Length(max=50)])
    delivery_description = TextAreaField('Delivery description', validators=[DataRequired()])
    subject_id = SelectField('Subject', choices=[])
    toDate = DateTimeLocalField('Delivery date', format='%Y-%m-%dT%H:%M', validators=[InputRequired()])
    submit = SubmitField('Add')