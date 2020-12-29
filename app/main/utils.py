from ..models import *
from app import db
from flask_login import current_user
from datetime import datetime, timedelta

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

def get_days(ndays):
    """
    List starting in this week's monday 
        for element in list : element -> {
            deliveries:[(delivery1, subject1),...] of that day,
            day:day of the month,
            str:color}
    """
    # today = datetime.strptime('2-11-2020', '%d-%m-%Y')
    today = datetime.today()
    first_day = today - timedelta(days=today.weekday())

    days = []
    for i in range(0, ndays):
        i_day = first_day + timedelta(days=i)
        elements = {
            'deliveries':[
                (delivery, db.session.query(Subject).filter_by(
                    user_id=current_user.id,
                    identification=delivery.subject_id
                ).first()) for delivery in 
                db.session.query(Delivery).filter_by(
                    user_id=current_user.id,
                    toDateStr=str(i_day.date()),
                    isDone=False,
                    isEliminated=False
                ).all()] if i_day >= today else [],
            'day': i_day.day,
            'color': day_color(today, i_day)}
        days.append(elements)
    return days

def day_color(today, iday):
    if iday == today: 
        return '#d6ceba'    # Color for today 
    elif iday.weekday() > 4:
        return '#ffb600'    # Color for weekend 
    elif iday < today:
        return '#000'       # Color for past   
    else:
        return '#fff'       # Color for future
