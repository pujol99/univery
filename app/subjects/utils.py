import requests
from bs4 import BeautifulSoup
from flask_login import current_user

LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}


def check_subject(id):
    payload = {
        "adAS_i18n_theme": "ca",
        "adAS_mode": "authn",
        "adAS_username": current_user.identification,
        "adAS_password": current_user.password,
    }
    req_url = "https://aulaglobal.upf.edu/course/view.php?id=" + str(id)

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=payload)
        req = session.get(req_url)
        soup = BeautifulSoup(req.text, "html.parser")
        name = soup.find("a", {"href":req_url})
        if name:
            return True, name.text, id
        return False, "", ""
