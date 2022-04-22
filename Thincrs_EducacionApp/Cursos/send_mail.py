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
import sqlite3
from sqlite3 import Error

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
        query = '''select * from Cursos_courseretiremodel;'''
        data = pd.read_sql_query(query, conn)
        print("data", data)
        print("type(data)", type(data))
        """for indx, curso in data.iterrows():
                                            print("curso.id_course", curso.id_course) #id de los cursos"""

        query2 = '''select * from resource;'''
        data2 = pd.read_sql_query(query2, conn)
        print("data2", data2.iloc[0])

        for indx2, curso2 in data2.iterrows():
            print("curso2.url", curso2.url)

        database = r"../db.sqlite3"

        # create a database connection
        conn2 = create_connection(database)
        cur = conn2.cursor()
        cur.execute("SELECT * FROM Cursos_coursemodel")



        rows = cur.fetchall()

        """for el in rows:
                                            print("el[6]", el[6])#obtener el url"""

        print(rows[1][6])
        conn.close()

if __name__ == '__main__':
    main()
