from flask import Blueprint
from app.models import *
from .forms import *
from ..main.utils import check_subject
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for

subjects = Blueprint('subjects', __name__)

@subjects.route("/add-subject", methods=['GET', 'POST'])
@login_required
def add_subject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        correct, name, identification = check_subject(form.subject_id.data)
        if correct:
            subject = Subject(identification=identification, name=name, user_id=current_user.id)
            db.session.add(subject)
            db.session.commit()
    return render_template('subject/add-subject.html', form=form)