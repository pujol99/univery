import requests
import random
from bs4 import BeautifulSoup
from flask_login import current_user
from ..main.utils import LOGIN, PAYLOAD, HEADERS
from app import db

def check_subject(id, user_password):
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = user_password
    request_url = "https://aulaglobal.upf.edu/course/view.php?id=" + id

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)
        request = session.get(request_url)
        soup = BeautifulSoup(request.text, "html.parser")

        # If we found the an a tag with name -> subject exists
        name = soup.find("a", {"href":request_url})
        if name:
            return True, clean_name(name.text), id
        return False, "", ""
    
def search_subjects(user_password):
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = user_password
    request_url = "https://www.upf.edu/intranet/campus-global"
    subjects = []

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)

        req = session.get(request_url)
        soup = BeautifulSoup(req.text, "html.parser")
        panel = soup.find('div', {'id':'aula-global-portlet'})
        a_tags = panel.findAll('a')
        for a in a_tags:
            if "course/view" in a['href']:
                subjects.append((
                    session.get(a['href']).url.split('=')[1],
                    clean_name(a.text)
                ))
    
    return subjects

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def clean_name(name):
    # Remove words in name that contain a number
    words = []
    for word in name.split():
        if not any(letter.isdigit() for letter in word) or "mtc" in word.lower():
            words.append(word)
    return " ".join(words)


class SubjectObject :
    def __init__(self, url, session, id):
        self.url = url
        self.session = session

        self.deliveries_url = None
        self.id = id

    def scrape_subject(self):
        req = self.session.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")

        activities = soup.findAll('div', {'class':'activityinstance'})

        self.deliveries_url = [activity.find('a')['href'] for activity in activities 
                            if "assign" in activity.find('a')['href']]
