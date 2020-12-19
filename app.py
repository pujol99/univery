from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import *
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = '4222df3be198bdd5c545cf587f0f11f3'

db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('registration.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.identification.data == 'U151110' and 
                  form.password.data == '1234'):
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)