from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeLocalField
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired


class AddDeliveryForm(FlaskForm):
    delivery_name = StringField('Delivery name', 
        validators=[DataRequired(), Length(max=50)])
    delivery_description = TextAreaField('Delivery description', 
        validators=[Length(max=3000)])
    subject_id = SelectField('Subject', 
        validators=[DataRequired()],
        choices=[])
    toDate = DateTimeLocalField('Delivery date',
        validators=[InputRequired()],
        format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Add')