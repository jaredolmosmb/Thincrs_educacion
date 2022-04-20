import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

#home = expanduser('~')
mypkey = paramiko.RSAKey.from_private_key_file("clave.pem")
# if you want to use ssh password use - ssh_password='your ssh password', bellow

sql_hostname = 'develop-instance.cici1guul97n.us-east-2.rds.amazonaws.com'
sql_username = 'develop_thincrs'
sql_password = 'Thincrs_password2021'
sql_main_database = 'Develop_thincrs'
sql_port = 3306
ssh_host = '18.222.146.90'
ssh_user = 'ubuntu'
ssh_port = 22
sql_ip = '1.1.1.1.1'

def main():
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'no-reply-educacion@thincrs.com'
    EMAIL_HOST_PASSWORD = 'ThincrsPassword22'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=mypkey,
            remote_bind_address=(sql_hostname, sql_port)) as tunnel:
        conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                passwd=sql_password, db=sql_main_database,
                port=tunnel.local_bind_port)
        query = '''select * from udemy_course;'''
        data = pd.read_sql_query(query, conn)
        print("data", data.iloc[0])
        conn.close()
        sender_email = "no-reply-educacion@thincrs.com"
        receiver_email = "jaredarturolmos@gmail.com"
        password = "ThincrsPassword22"
        # creacion de texto plano y html
        message = MIMEMultipart("alternative")
        message["Subject"] = "Cursos Retirados test"
        message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br> {}
            </p>
          </body>
        </html>
        """.format(data.iloc[0][1])

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

if __name__ == '__main__':
    main()
"""import mysql.connector
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def main():
    print("en mail")
    with sshtunnel.SSHTunnelForwarder(
    ('18.222.146.90'),
    ssh_username='ubuntu', ssh_pkey="clave.pem",
    remote_bind_address=('develop-instance.cici1guul97n.us-east-2.rds.amazonaws.com', 3306)
    ) as tunnel:
        connection = mysql.connector.connect(
            user='develop_thincrs', password='Thincrs_password2021',
            host='127.0.0.1', port=tunnel.local_bind_port,
            database='Develop_thincrs',
        )
    # Do stuff
        print("conexion")
        connection.close()
    




if __name__ == '__main__':
    main()"""