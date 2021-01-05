LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
REQUEST = "https://aulaglobal.upf.edu/course/view.php?id="
PAYLOAD = {
    "adAS_i18n_theme": "ca",
    "adAS_mode": "authn",
    "adAS_username": None,
    "adAS_password": None}

MONTHS = {
    "gener": "01", "febrer": "02",
    "març": "03", "abril": "04",
    "maig": "05", "juny": "06",
    "juliol": "07", "agost": "08",
    "setembre": "09", "octubre": "10",
    "novembre": "11", "desembre": "12",
}

DATE_FORMAT = "%d-%m %H:%M" 