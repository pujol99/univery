import requests
from bs4 import BeautifulSoup
from ..deliveries.utils import Delivery

class Subject:
    def __init__(self, url, session, id):
        self.url = url
        self.session = session

        self.deliveries = None
        self.id = id

    def scrape_subject(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        activities = soup.findAll('div', {'class':'activityinstance'})

        deliveries_url = [activity.find('a')['href'] for activity in activities 
                            if "assign" in activity.find('a')['href']]
        
        self.deliveries = [Delivery(url, self.session, self.id) for url in deliveries_url]

