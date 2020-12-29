import requests
from bs4 import BeautifulSoup
from ..main.utils import PAYLOAD, HEADERS, LOGIN

def check_user(identification, password):
    PAYLOAD["adAS_username"] = identification
    PAYLOAD["adAS_password"] = password
    request_url = "https://www.upf.edu/intranet/campus-global"

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=PAYLOAD)
        request = session.get(request_url)
        soup = BeautifulSoup(request.text, "html.parser")

        # If this message is found login is incorrect
        return not("Identificació d'usuaris" in soup.find('h1').text)