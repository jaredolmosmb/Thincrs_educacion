import sqlite3
from sqlite3 import Error
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cursos_coursemodel")

    rows = cur.fetchall()

    print(rows[1])



def main():
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
    database = r"C:\Users\artur\prueba\Thincrs_educacion\Thincrs_EducacionApp\db.sqlite3"


    # create a database connection
    conn = create_connection(database)
    with conn:

        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()