from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')  # tu correo
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')  # tu app password
    MAIL_DEFAULT_SENDER = os.getenv('EMAIL_USER')
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")