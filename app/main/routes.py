from flask import Blueprint
from app.models import Movie, User
import random
from fuzzywuzzy import fuzz
from flask import render_template

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    movies = Movie.query.all()
    selected = []
    if len(movies) < 8:
        return render_template('home.html', movies=movies)
    else:
        for i in range(0, 8):
            temp = random.choice(movies)
            if temp not in selected:
                selected.append(temp)
            else:
                i -= 1
        return render_template('home.html', movies=selected)

@main.route("/search/<string:search>")
def search(search):
    movies = []
    for movie in Movie.query.all():
        ratio1 = fuzz.ratio(movie.name.lower(),search.lower())
        ratio2 = fuzz.partial_ratio(movie.name.lower(),search.lower())
        ratio3 = fuzz.token_sort_ratio(movie.name.lower(),search.lower())
        if ratio1 > 80 or ratio2 > 80 or ratio3 > 80:
            movies.append(movie)
    users = []
    for user in User.query.all():
        ratio1 = fuzz.ratio(user.username.lower(),search.lower())
        ratio2 = fuzz.partial_ratio(user.username.lower(),search.lower())
        ratio3 = fuzz.token_sort_ratio(user.username.lower(),search.lower())
        if ratio1 > 80 or ratio2 > 80 or ratio3 > 80:
            users.append(user)
    return render_template('search.html', movies=movies, users=users)