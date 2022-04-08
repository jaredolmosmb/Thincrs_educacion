import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
"""import django
from django.db import models
from Cursos.models import *"""
"""from django.apps import apps"""

"""os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Thincrs_EducacionApp.settings")
django.setup()


ap=apps.get_model('Thincrs_EducacionApp','CourseRetireModel')
q=ap.objects.get(id = 1)
print(q)
print("q")"""


def run():
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'no-reply-educacion@thincrs.com'
    EMAIL_HOST_PASSWORD = 'ThincrsPassword22'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    sender_email = "no-reply-educacion@thincrs.com"
    receiver_email = "jaredarturolmos@gmail.com"
    password = "ThincrsPassword22"

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    curso = CourseRetireModel.objects.get(id = 1)


    # creacion de texto plano y html
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           {{q.title}}
        </p>
      </body>
    </html>
    """

    # convertir a mimetext
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # añadir texto y html 
    message.attach(part1)
    message.attach(part2)

    # crear coneccion y enviar el email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )



