from ..models import *
from app import db
from flask_login import current_user
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
from flask import request



DATE_FORMAT = "%d-%m %H:%M" 

LOGIN = "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
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

def get_days(ndays, view):
    """
    List starting in this week's monday 
        elements [] : element -> 
        {   
            deliveries: (Delivery, UserSubject) [] (of that day),
            day: day of the month,
            color: HEX str
        }
    """
    today = datetime.strptime('2-10-2020', '%d-%m-%Y')
    # today = datetime.today()
    first_day = today - timedelta(days=today.weekday()) + timedelta(days=ndays*view)

    days = []
    months = []
    for i in range(0, ndays):
        i_day = first_day + timedelta(days=i)
        month_name = i_day.strftime("%B")
        if month_name not in months:
            months.append(month_name)

        elements = {
            # For UserDelivery object in day i get (Delivery, UserSubject)
            'deliveries':[(
                    ud.delivery, 
                    db.session.query(UserSubject).filter_by(
                        subject_id=ud.delivery.subject_id,
                        user_id=current_user.id
                    ).first()
                ) for ud in db.session.query(UserDelivery).filter_by(
                    user_id=current_user.id,
                    isDone=False,
                    isEliminated=False
                ).all() if ud.delivery.toDateStr == str(i_day.date())
            ] if i_day >= today else [],
            'day': i_day.day,
            'color': day_color(today, i_day)}
        days.append(elements)
    return days, "/".join(months)

def day_color(today, iday):
    if iday == today: 
        return '#d6ceba'    # Color for today 
    elif iday.weekday() > 4:
        return '#ffb600'    # Color for weekend 
    elif iday < today:
        return '#000'       # Color for past   
    else:
        return '#fff'       # Color for future

def isSafeUrl(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
