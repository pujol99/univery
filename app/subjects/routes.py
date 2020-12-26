from flask import Blueprint
from app.models import *
from .forms import *
from ..main.utils import check_subject
from flask_login import current_user, login_required
from flask import render_template, redirect, url_for

subjects = Blueprint('subjects', __name__)

@subjects.route("/subjects", methods=['GET', 'POST'])
@login_required
def subjects_page():
    form = AddSubjectForm()
    if form.validate_on_submit():
        correct, name, identification = check_subject(form.subject_id.data)
        if correct and not Subject.query.filter_by(identification=identification, user_id=current_user.id).first():
            subject = Subject(identification=identification, name=name, user_id=current_user.id, color="#"+form.subject_color.data)
            db.session.add(subject)
            db.session.commit()
    return render_template('subject/add-subject.html', title="Subjects", form=form)

@subjects.route("/subject-remove/<int:id>")
@login_required
def subject_remove(id):
    s = Subject.query.filter_by(id=id)

    Delivery.query.filter_by(subject_id=s.first().identification).delete()
    s.delete()
    db.session.commit()

    return redirect(url_for('subjects.subjects_page'))