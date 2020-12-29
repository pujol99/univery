from app.models import *
from .forms import *
from .utils import check_subject
from app import db
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for

subjects = Blueprint('subjects', __name__)

@subjects.route("/subjects", methods=['GET', 'POST'])
@login_required
def subjects_page():
    form = AddSubjectForm()
    if form.validate_on_submit():
        # If exists in user university subjects add subject else display error message
        exists, name, id = check_subject(form.subject_id.data)
        if exists:
            db.session.add(Subject(
                identification=id, 
                name=name, user_id=current_user.id, 
                color="#"+form.subject_color.data))
            db.session.commit()
        else:
            return render_template('subject/add-subject.html', title="Subjects", form=form, 
                message="Subject not found")
    return render_template('subject/add-subject.html', title="Subjects", form=form)

@subjects.route("/subject-remove/<int:id>")
@login_required
def subject_remove(id):
    s = Subject.query.filter_by(
        id=id,
        user_id=current_user.id)
    # Delete all the deliveries and the subject
    Delivery.query.filter_by(
        subject_id=s.first().identification,
        user_id=current_user.id
    ).delete()
    s.delete()
    db.session.commit()

    return redirect(url_for('subjects.subjects_page'))