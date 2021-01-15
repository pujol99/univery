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
    form = AddSubjectForm()
    if form.validate_on_submit():
        # If exists in user university subjects add subject else display error message
        exists, name, id = check_subject(form.subject_id.data, session["password"])
        if not exists:
            return render_template('subject/add-subject.html', title="Subjects", form=form, 
                message="Subject not found")

        if not getSubjectById(id):
            addSubjectDB(name, id)
        addUserSubjectDB(id, "#"+form.subject_color.data)
        return redirect(url_for('subjects.subjects_list'))
    subjects = session["subjects"] if session.get("subjects") else []
    return render_template('subject/add-subject.html', title="Subjects", form=form, subjects=subjects)

@subjects.route("/subject-search")
@login_required
def subject_search():
    session["subjects"] = search_subjects(session["password"])
    return redirect(url_for('subjects.add_subject'))
