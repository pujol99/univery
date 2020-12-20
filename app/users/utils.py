import requests
from bs4 import BeautifulSoup

LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}


def check_user(identification, password):
    payload = {
        "adAS_i18n_theme": "ca",
        "adAS_mode": "authn",
        "adAS_username": identification,
        "adAS_password": password,
    }

    with requests.Session() as session:
        session.post(LOGIN, headers=HEADERS, data=payload)
        req = session.get("https://www.upf.edu/intranet/campus-global")
        soup = BeautifulSoup(req.text, "html.parser")
        return not("Identificació d'usuaris" in soup.find('h1').text)