import requests
from flask_login import current_user
from bs4 import BeautifulSoup
from datetime import datetime
import re

LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
REQUEST = "https://aulaglobal.upf.edu/course/view.php?id="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}


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

def update_deliveries():
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

        subjects = [Subject(REQUEST+id, session) for id in subject_ids]
        for subject in subjects:
            subject.scrape_subject()
            deliveries += subject.deliveries
            print(subject)
        
        for delivery in deliveries:
            delivery.scrape_delivery()

        return [delivery for delivery in deliveries if delivery.date]

class Subject:
    def __init__(self, url, session):
        self.url = url
        self.session = session

        self.name = None
        self.deliveries = None

    def scrape_subject(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        self.name = " ".join(soup.find('h1').text.split()[1:])

        activities = soup.findAll('div', {'class':'activityinstance'})

        deliveries_url = [activity.find('a')['href'] for activity in activities 
                            if "assign" in activity.find('a')['href']]
        
        self.deliveries = [Delivery(url, self.session, self.name) for url in deliveries_url]

    def __str__(self):
        return "Subject " + self.name + "\n\tdeliveries: " + str(len(self.deliveries))

 
class Delivery:
    def __init__(self, url, session, subject_name):
        self.url = url
        self.session = session

        self.subject_name = subject_name
        self.name = None
        self.date = None

    def scrape_delivery(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        self.name = soup.find('h2').text

        info_cols = soup.findAll('tr')
        for col in info_cols:
            if not col.find('th'):
                continue
            if "Data de venciment" in col.find('th').text:    
                self.date = to_datetime_ca(col.find('td').text)
            elif "Due date" in col.find('th').text:
                self.date = to_datetime_en(col.find('td').text)

    def __str__(self):
        if self.date:
            return print_date(self.date) + " | " + self.subject_name + "\n\t" + self.name + "\n" + "-"*55
        return "No date found"


month_tr = {
    "gener": "01", "febrer": "02",
    "març": "03", "abril": "04",
    "maig": "05", "juny": "06",
    "juliol": "07", "agost": "08",
    "setembre": "09", "octubre": "10",
    "novembre": "11", "desembre": "12",
}

def read_ids(url):
    f = open(url, "r")
    return f.read().splitlines()

def is_future(date):
    return date > datetime.now()

def to_datetime_ca(date):
    # Parse date time from catalan
    parts = re.split("[,’ ]+", date)
    day = parts[1]
    month = month_tr[parts[-3]]
    year = parts[-2]
    hour = parts[-1]
    full_date = year + "-" + month + "-" + day + " " + hour
    date = datetime.strptime(full_date, '%Y-%m-%d %H:%M')
    
    return date

def to_datetime_en(date):
    # Parse date time from english
    parts = re.split("[, ]+", date)
    day = parts[1]
    month = parts[2]
    year = parts[3]
    hour = parts[4]
    htype = parts[5]
    full_date = year + "-" + month + "-" + day + " " + hour
    date = datetime.strptime(full_date, '%Y-%B-%d %H:%M')
    
    return date

def print_date(date):
    days_left = (date - datetime.now()).days
    if days_left == 0:
        days_left_str = " (today)"
    elif days_left == 1:
        days_left_str = " (tomorrow)"
    else:
        days_left_str = " (" + str(days_left) + " days)"

    return date.strftime("%d/%m %H:%M") + days_left_str