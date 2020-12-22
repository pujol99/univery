from ..subjects.utils import Subject
from ..deliveries.utils import Delivery
from flask_login import current_user
from datetime import datetime

import requests
from bs4 import BeautifulSoup


LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
REQUEST = "https://aulaglobal.upf.edu/course/view.php?id="

def check_subject(id):
    payload = {
        "adAS_i18n_theme": "ca",
        "adAS_mode": "authn",
        "adAS_username": current_user.identification,
        "adAS_password": current_user.password,
    }
    req_url = "https://aulaglobal.upf.edu/course/view.php?id=" + str(id)

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=payload)
        req = session.get(req_url)
        soup = BeautifulSoup(req.text, "html.parser")
        name = soup.find("a", {"href":req_url})
        if name:
            return True, name.text, id
        return False, "", ""

def check_user(identification, password):
    payload = {
        "adAS_i18n_theme": "ca",
        "adAS_mode": "authn",
        "adAS_username": identification,
        "adAS_password": password,
    }

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=payload)
        req = session.get("https://www.upf.edu/intranet/campus-global")
        soup = BeautifulSoup(req.text, "html.parser")
        return not("Identificació d'usuaris" in soup.find('h1').text)

def get_deliveries():
    payload = {
        "adAS_i18n_theme": "ca",
        "adAS_mode": "authn",
        "adAS_username": current_user.identification,
        "adAS_password": current_user.password,
    }

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=payload)

        deliveries = []
        subject_ids = []
        for subject in current_user.subjects:
            subject_ids.append(subject.identification)

        subjects = [Subject(REQUEST+id, session, id) for id in subject_ids]
        for subject in subjects:
            subject.scrape_subject()
            deliveries += subject.deliveries
        
        for delivery in deliveries:
            delivery.scrape_delivery()

        return [delivery for delivery in deliveries if delivery.date]

def get_deliveries_todo(deliveries):
    deliveries = [i for i in deliveries if not i.isDone and not i.isEliminated]
    # Remove past ones
    #deliveries = [i for i in deliveries if is_future(i.toDate)]
    # Sort
    return sorted(deliveries, key=lambda x: x.toDate)

def get_deliveries_done(deliveries):
    deliveries = [i for i in deliveries if i.isDone and not i.isEliminated]
    # Remove past ones
    #deliveries = [i for i in deliveries if is_future(i.toDate)]
    # Sort
    return sorted(deliveries, key=lambda x: x.toDate)

def is_future(date):
    return date > datetime.now()
