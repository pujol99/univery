import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import timedelta
from flask_login import current_user
from ..models import Delivery as DeliveryModel, Subject as SubjectModel
from .. import db


MONTHS = {
    "gener": "01", "febrer": "02",
    "març": "03", "abril": "04",
    "maig": "05", "juny": "06",
    "juliol": "07", "agost": "08",
    "setembre": "09", "octubre": "10",
    "novembre": "11", "desembre": "12",
}

class Delivery:
    def __init__(self, url, session, subject_id):
        self.url = url
        self.session = session

        self.subject_id = subject_id
        self.name = None
        self.description = None
        self.date = None

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

def get_days(size):
    """
        List starting in this week's monday 
            for element in list : element -> {
                deliveries:(delivery, subject) of that day,
                day:day of the month,
                bool:isToday,
                bool:past}
    """
    today = datetime.now()
    first_day = today - timedelta(days=today.weekday())

    days = []
    for i in range(0, 10):
        i_day = first_day + timedelta(days=i)
        elements = {
            'deliveries':[
                (delivery, db.session.query(SubjectModel).filter_by(
                    user_id=current_user.id,
                    identification=delivery.subject_id
                ).first()) for delivery in 
                db.session.query(DeliveryModel).filter_by(
                    user_id=current_user.id,
                    toDateStr=str(i_day.date())
                ).all()],
            'day': i_day.day,
            'isToday': today.day == i_day.day,
            'isPast': today > i_day}
        days.append(elements)
    return days