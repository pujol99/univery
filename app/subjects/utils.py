import requests
from bs4 import BeautifulSoup
from flask_login import current_user
from ..main.utils import LOGIN, PAYLOAD, HEADERS

def check_subject(id):
    PAYLOAD["adAS_username"] = current_user.identification
    PAYLOAD["adAS_password"] = current_user.password
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

def clean_name(name):
    # Remove words in name that contain a number
    words = []
    for word in name.split():
        if not any(letter.isdigit() for letter in word):
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
