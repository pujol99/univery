from ..subjects.utils import Subject
from ..deliveries.utils import Delivery
from ..models import Subject as SubjectModel
from app import db
from flask_login import current_user
from datetime import datetime

import requests
from bs4 import BeautifulSoup


LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
REQUEST = "https://aulaglobal.upf.edu/course/view.php?id="
PAYLOAD = {
    "adAS_i18n_theme": "ca",
    "adAS_mode": "authn",
    "adAS_username": None,
    "adAS_password": None}

def check_subject(id):
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = current_user.password
    req_url = "https://aulaglobal.upf.edu/course/view.php?id=" + str(id)

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)
        req = session.get(req_url)
        soup = BeautifulSoup(req.text, "html.parser")

        # If we found the an a tag with name -> subject exists
        name = soup.find("a", {"href":req_url})
        if name:
            return True, clean_name(name.text), id
        return False, "", ""

def check_user(identification, password):
    PAYLOAD["adAS_username"] = identification
    PAYLOAD["adAS_password"] = password

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)
        req = session.get("https://www.upf.edu/intranet/campus-global")
        soup = BeautifulSoup(req.text, "html.parser")

        # If this message is found login is incorrect
        return not("Identificació d'usuaris" in soup.find('h1').text)

def get_deliveries():
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = current_user.password

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)

        deliveries = []
        subject_ids = [subject.identification for subject in current_user.subjects]
        subjects = [Subject(REQUEST+id, session, id) for id in subject_ids]

        for subject in subjects:
            subject.scrape_subject()
            deliveries += subject.deliveries
        
        for delivery in deliveries:
            delivery.scrape_delivery()

        return [delivery for delivery in deliveries if delivery.date]

def get_deliveries_todo(deliveries):
    deliveries = [(i, db.session.query(SubjectModel).filter_by(identification=i.subject_id).first())
        for i in deliveries if not i.isDone and not i.isEliminated]
    # Remove past ones
    #deliveries = [i for i in deliveries if is_future(i.toDate)]
    # Sort
    return list(reversed(sorted(deliveries, key=lambda x: x[0].toDate)))

def get_deliveries_done(deliveries):
    deliveries = [(i, db.session.query(SubjectModel).filter_by(identification=i.subject_id).first())
        for i in deliveries if i.isDone and not i.isEliminated]
    # Remove past ones
    #deliveries = [i for i in deliveries if is_future(i.toDate)]
    # Sort
    return list(reversed(sorted(deliveries, key=lambda x: x[0].toDate)))

def is_future(date):
    return date > datetime.now()

def clean_name(name):
    # Remove words in name that contain a number
    words = []
    for word in name.split():
        if not any(letter.isdigit() for letter in word):
            words.append(word)
    return " ".join(words)
