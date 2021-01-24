from flask import Blueprint, render_template
from ..main.utils import *

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Error"), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Error"), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Error"), 500

@errors.app_errorhandler(502)
def error_502(error):
    return render_template('errors/502.html', lenguages=LANGUAGES, cl=get_lenguage(), title="Error"), 502