import requests, re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from flask_login import current_user
from ..subjects.utils import SubjectObject
from ..models import *
from ..main.utils import PAYLOAD, REQUEST, LOGIN, HEADERS, MONTHS
from app import db

def get_deliveries():
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = current_user.password

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)

        deliveries = []
        subject_ids = [subject.identification for subject in current_user.subjects]
        subjects = [SubjectObject(REQUEST+id, session, id) for id in subject_ids]

        for subject in subjects:
            subject.scrape_subject()
            deliveries += [DeliveryObject(url, subject.session, subject.id) for url in subject.deliveries_url]
        
        for delivery in deliveries:
            delivery.scrape_delivery()

        return [delivery for delivery in deliveries if delivery.date]

def filter_deliveries(deliveries, restriction):
    deliveries = [(i, db.session.query(Subject).filter_by(
        identification=i.subject_id,
        user_id=current_user.id).first()
        ) for i in deliveries if restriction(i)]
    # Remove past ones
    #deliveries = [i for i in deliveries if is_future(i.toDate)]
    # Sort
    return list(reversed(sorted(deliveries, key=lambda x: x[0].toDate)))
    
def is_future(date):
    return date > datetime.now()

class DeliveryObject:
    def __init__(self, url, session, subject_id):
        self.session = session

        self.name = None
        self.description = None
        self.date = None
        self.url = url
        self.subject_id = subject_id

    def scrape_delivery(self):
        request = self.session.get(self.url)
        soup = BeautifulSoup(request.text, "html.parser")

        self.name = soup.find('h2').text
        description = soup.find(id='intro')
        self.description = description.text if description else None

        # Find to do date information
        info_columns = soup.findAll('tr')
        for col in info_columns:
            if not col.find('th'):
                continue
            if "Data de venciment" in col.find('th').text:    
                self.date = to_datetime_ca(col.find('td').text)
            elif "Due date" in col.find('th').text:
                self.date = to_datetime_en(col.find('td').text)

def to_datetime_ca(date):
    # Parse date time from catalan
    parts = re.split("[,’ ]+", date)
    day = parts[1]
    month = MONTHS[parts[-3]]
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

def clean_description(description):
    return '~'.join(description.splitlines())