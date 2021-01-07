import requests, re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, abort, session
from flask_login import current_user
from ..subjects.utils import SubjectObject
from ..models import *
from ..main.utils import *
from ..global_utils import * 
from app import db

def get_deliveries(subjects, user_password):
    """
        Scrape all deliveries from university selected subjects
        UserSubject [] -> DeliveryObject []
    """
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = user_password

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)
    
        deliveries = []
        subject_ids = [subject.subject.identification for subject in subjects]
        subjectObjects = [SubjectObject(REQUEST+id, session, id) for id in subject_ids]
    
        for subject in subjectObjects:
            subject.scrape_subject()
            deliveries += [DeliveryObject(
                url, subject.session, subject.id
            ) for url in subject.deliveries_url if not checkDeliveryEnded(url.split('=')[1])]
        
        for delivery in deliveries:
            delivery.scrape_delivery()
    
        return [delivery for delivery in deliveries if delivery.date]

def filter_deliveries(deliveries, restriction):
    """
        filter deliveries that pass certain restriction
        (UserDelivery [], lambda function) -> (Delivery, UserSubject) []
    """
    deliveries = [(
        ud.delivery,
        USbySubject(ud.delivery.subject_id)
        ) for ud in deliveries if restriction(ud) #and ud.delivery.toDate > datetime.now()
    ]
    # Sort by date
    return sorted(deliveries, key=lambda x: x[0].toDate)


def get_days(ndays, view):
    """ 
        List starting in this week's monday 
        elements [ndays] : element -> {   
            deliveries: (Delivery, UserSubject) [] (of that day i),
            day: day of the month,
            color: HEX str}
    """
    today = datetime.strptime('2-10-2020', '%d-%m-%Y')
    # today = datetime.today()
    first_day = today - timedelta(days=today.weekday()) # Current week's Monday
    first_day += timedelta(days=ndays*view)             # Go back/forward view weeks

    days, months = [], set()
    for i in range(0, ndays):
        i_day = first_day + timedelta(days=i)
        months.add(i_day.strftime("%B"))

        elements = {
            'deliveries':[(
                    ud.delivery, 
                    USbySubject(ud.delivery.subject_id)
                ) for ud in UDnotDone() if ud.delivery.toDateStr == str(i_day.date())
            ] if i_day >= today else [],
            'day': str(i_day.day) + " " + i_day.strftime("%A"),
            'color': day_color(today, i_day)}
        days.append(elements)
    return days, "/".join(list(months))


def day_color(today, iday):
    if iday == today: 
        return '#d6ceba'    # Color for today 
    elif iday.weekday() > 4:
        return '#ffb600'    # Color for weekend 
    elif iday < today:
        return '#000'       # Color for past   
    else:
        return '#fff'       # Color for future

class DeliveryObject:
    def __init__(self, url, session, subject_id):
        self.session = session

        self.id = url.split('=')[1]
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

        # Find to do date defintion
        info_columns = soup.findAll('tr')
        for col in info_columns:
            if not col.find('th'):
                continue
            if " de venciment" in col.find('th').text:    
                self.date = self.to_datetime_catalan(col.find('td').text)
            elif "Due date" in col.find('th').text:
                self.date = self.to_datetime_english(col.find('td').text)
    
    
    def to_datetime_catalan(self, date):
        parts = re.split("[,’ ]+", date)
        # YEAR - MONTH - DAY - HOUR/MINUTE
        return datetime.strptime(
            parts[-2] + "-" + MONTHS[parts[-3]] + "-" + parts[1] + " " + parts[-1], 
            '%Y-%m-%d %H:%M')

    def to_datetime_english(self, date):
        parts = re.split("[, ]+", date)
        # YEAR - MONTH - DAY - HOUR/MINUTE
        return datetime.strptime(
            parts[3] + "-" + parts[2] + "-" + parts[1] + " " + parts[4],
            '%Y-%B-%d %H:%M')

def clean_description(description):
    return '~'.join(description.splitlines())

def isSafeUrl(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_to(next_route):
    next_page = request.args.get('next')
    if not isSafeUrl(next_page):
        return abort(400)
    return redirect(url_for(next_page if next_page else next_route))