LOGIN = (
    "https://sso.upf.edu/CAS/index.php/login?service=https://www.upf.edu/c/portal/login"
)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}
REQUEST = "https://aulaglobal.upf.edu/course/view.php?id="
PAYLOAD = {
    "adAS_i18n_theme": "ca",
    "adAS_mode": "authn",
    "adAS_username": None,
    "adAS_password": None,
}

MONTHS = {
    "gener": "01",
    "febrer": "02",
    "març": "03",
    "abril": "04",
    "maig": "05",
    "juny": "06",
    "juliol": "07",
    "agost": "08",
    "setembre": "09",
    "octubre": "10",
    "novembre": "11",
    "desembre": "12",
}

DATE_FORMAT = "%d-%m %H:%M"

ACTIONS = ["done", "undone", "remove", "restore"]

from flask import render_template


class MaintenanceModeHandler:
    def __init__(self, boolean):
        self.boolean = boolean

    def __call__(self):
        if self.boolean:
            return render_template(
                "errors/maintenance.html",
                lenguages=LANGUAGES,
                cl=get_lenguage(),
                title="Error",
            )

def update_lenguage(l):
    LANGUAGE.update(l)

def get_lenguage():
    return LANGUAGE.cl

class Language():
    def __init__(self):
        self.cl = "ca"
    def update(self, l):
        self.cl = l

LANGUAGE = Language()
LANGUAGES = {
    "Subjects": {"ca": "Materies", "es": "Materias", "en": "Subjects"},
    "Account": {"ca": "Compte", "es": "Cuenta", "en": "Account"},
    "Login": {"ca": "Entra", "es": "Entra", "en": "Login"},
    "Register": {"ca": "Registra't", "es": "Registrate", "en": "Register"},
    "Remember to periodically update the deliveries with": {
        "ca": "Recorda't de actualitzar les entregues amb",
        "es": "Acuerdate de actualizar las entregas con",
        "en": "Remember to periodically update the deliveries with",
    },
    "Have an account?": {
        "ca": "Ja tens un compte?",
        "es": "Ya tienes una cuenta?",
        "en": "Have an account?",
    },
    "Dont have an account?": {
        "ca": "No tens un compte?",
        "es": "No tienes una cuenta?",
        "en": "Dont have an account?",
    },
    "Update password": {
        "ca": "Nova contrasenya",
        "es": "Nueva contraseña",
        "en": "Update password",
    },
    "Logout": {"ca": "Sortir", "es": "Salir", "en": "Logout"},
    "Your subjects": {
        "ca": "Les teves materies",
        "es": "Tus materias",
        "en": "Your subjects",
    },
    "Select subject": {
        "ca": "Selecciona una materia",
        "es": "Selecciona una materia",
        "en": "Select subject",
    },
    "Find subjects": {
        "ca": "Trova materies",
        "es": "Encuentra materias",
        "en": "Find subjects",
    },
    "Oops. You don't have permission": {
        "ca": "Oops. No tens permissos",
        "es": "Oops. no tienes permisos",
        "en": "Oops. You don't have permission",
    },
    "Please check your account and try again": {
        "ca": "Mira si el teu compte es correcte i torna",
        "es": "Mira si tu cuenta es correcta y vuelve",
        "en": "Please check your account and try again",
    },
    "Home": {"ca": "Inici", "es": "Inicio", "en": "Home"},
    "Oops... Page Not Found": {
        "ca": "Oops... Pagina no trovada",
        "es": "Oops... Pagina no encontrada",
        "en": "Oops... Page Not Found",
    },
    "Try another one": {
        "ca": "Prova una altre",
        "es": "Prueba otra",
        "en": "Try another one",
    },
    "Oops. Something went wrong": {
        "ca": "Oops. Alguna cosa no ha anat be",
        "es": "Oops. Algo no ha ido bien",
        "en": "Oops. Something went wrong",
    },
    "We're having some trouble": {
        "ca": "Estem tenint problemes",
        "es": "Estamos teniendo problemas",
        "en": "We're having some trouble",
    },
    "Oops. University page is having problems": {
        "ca": "Oops. La universitat esta tenint problemes",
        "es": "Oops. La universidad esta teniendo problemas",
        "en": "Oops. University page is having problems",
    },
    "Maintenance time": {
        "ca": "Manteniment",
        "es": "Mantenimiento",
        "en": "Maintenance time",
    },
    "Come back later": {
        "ca": "Torna en una estona",
        "es": "Vuelve en un rato",
        "en": "Come back later",
    },
    "No future deliveries": {
        "ca": "No tens mes entregues",
        "es": "No tienes mas entregas",
        "en": "No future deliveries",
    },
    "Show subjects": {
        "ca": "Mostra materies",
        "es": "Muestra materias",
        "en": "Show subjects",
    },
    "Add delivery": {
        "ca": "Afegeix entrega",
        "es": "Añade entrega",
        "en": "Add delivery",
    },
    "Delivery name": {
        "ca": "Nom entregable",
        "es": "Nombre entregable",
        "en": "Delivery name",
    },
    "Delivery description (optional)": {
        "ca": "Descripcio de la entrega",
        "es": "Descripcion de la entrega",
        "en": "Delivery description (optional)",
    },
    "Subject": {
        "ca": "Materia", 
        "es": "Materia", 
        "en": "Subject"
    },
    "Delivery date": {
        "ca": "Data entrega",
        "es": "Fecha entrega",
        "en": "Delivery date",
    },
    "Subject ID": {
        "ca": "ID de la materia",
        "es": "ID de la materia",
        "en": "Subject ID",
    },
    "Subject Color": {
        "ca": "Color de la materia",
        "es": "Color de la materia",
        "en": "Subject Color",
    },
    "Add": {"ca": "Afegeix", "es": "Añade", "en": "Add"},
    "Invalid HEX color": {
        "ca": "Color invalid",
        "es": "Color invalido",
        "en": "Invalid HEX color",
    },
    "Fullname": {"ca": "Nom complet", "es": "Nombre completo", "en": "Fullname"},
    "University identification": {
        "ca": "Identificacio de l'universitat",
        "es": "Identificacion de la universidad",
        "en": "University identification",
    },
    "University password": {
        "ca": "Contrasenya de la universitat",
        "es": "Contraseña de la universidad",
        "en": "University password",
    },
    "Sign up": {"ca": "Registra't", "es": "Registrate", "en": "Sign up"},
    "Password": {"ca": "Contrasenya", "es": "Contraseña", "en": "Password"},
    "Update": {"ca": "Actualitza", "es": "Actualiza", "en": "Update"},
    "That is your current password": {
        "ca": "Aquesta es la teva contrasenya actual",
        "es": "Esta es tu contraseña actual",
        "en": "That is your current password",
    },
    "That password doesnt pass the login in the university": {
        "ca": "Aquesta contrasenya no funciona per la universitat",
        "es": "Esta contraseña no entra en la universidad",
        "en": "That password doesnt pass the login in the university",
    },
    "Language": {
        "ca": "Idioma",
        "es": "Idioma",
        "en": "Language"
    }
}
