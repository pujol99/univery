import requests
from bs4 import BeautifulSoup
from ..deliveries.utils import Delivery

class Subject:
    def __init__(self, url, session, id):
        self.url = url
        self.session = session

        self.name = None
        self.deliveries = None
        self.id = id

    def scrape_subject(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        self.name = " ".join(soup.find('h1').text.split()[1:])

        activities = soup.findAll('div', {'class':'activityinstance'})

        deliveries_url = [activity.find('a')['href'] for activity in activities 
                            if "assign" in activity.find('a')['href']]
        
        self.deliveries = [Delivery(url, self.session, self.name, self.id) for url in deliveries_url]

    def __str__(self):
        return "Subject " + self.name + "\n\tdeliveries: " + str(len(self.deliveries))
