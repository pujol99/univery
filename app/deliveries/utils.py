import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


MONTHS = {
    "gener": "01", "febrer": "02",
    "març": "03", "abril": "04",
    "maig": "05", "juny": "06",
    "juliol": "07", "agost": "08",
    "setembre": "09", "octubre": "10",
    "novembre": "11", "desembre": "12",
}

class Delivery:
    def __init__(self, url, session, subject_name, subject_id):
        self.url = url
        self.session = session

        self.subject_name = subject_name
        self.subject_id = subject_id
        self.name = None
        self.description = None
        self.date = None

    def scrape_delivery(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        self.name = soup.find('h2').text
        self.description = soup

        info_cols = soup.findAll('tr')
        for col in info_cols:
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