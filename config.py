import os


class Config(object):
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL")
    CONTACT_PHONE = os.environ.get("CONTACT_PHONE")
    DEPARTMENT_NAME = os.environ.get("DEPARTMENT_NAME")
    DEPARTMENT_URL = os.environ.get("DEPARTMENT_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SERVICE_NAME = os.environ.get("SERVICE_NAME")
    SERVICE_PHASE = os.environ.get("SERVICE_PHASE")
    SERVICE_URL = os.environ.get("SERVICE_URL")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    HOSTNAME = os.environ.get("HOSTNAME")
