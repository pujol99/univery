from ..models import *
from .forms import *
from ..global_utils import *
from .utils import *
from app import db

from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, session

subjects = Blueprint('subjects', __name__)

@subjects.route("/subjects")
@login_required
def subjects_list():
    return render_template('subject/subjects.html', title="Subjects")
    

@subjects.route("/subject-remove/<int:id>")
@login_required
def subject_remove(id):
    # Remove US relation
    deleteElements([USbySubject(id)])

    # Remove deliveries with no identification made by user and subject s
    # Remove all UD with subject deliveries
    deleteElements(UDbySubject(id) + MDbySubject(id))

    return redirect(url_for('subjects.subjects_list'))


@subjects.route("/add-subject", methods=['GET', 'POST'])
@login_required
def add_subject():
    message = ""
    form = AddSubjectForm()
    if form.validate_on_submit():
        message, validated = validate_add_subject(form, session["password"])
        if validated:
            return redirect(url_for('subjects.subjects_list'))

    subjects = session["subjects"] if session.get("subjects") else []
    return render_template('subject/add-subject.html', title="Subjects", 
        form=form, 
        subjects=list(reversed(subjects)), 
        get_subject=USbySubject,
        message=message)


@subjects.route("/subject-search")
@login_required
def subject_search():
    session["subjects"] = search_subjects(session["password"])
    return redirect(url_for('subjects.add_subject'))
