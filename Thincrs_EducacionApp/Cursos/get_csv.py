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

        query2 = '''select * from question;'''
        data2 = pd.read_sql_query(query2, conn)

        print("type(data2): ", type(data2))
        print("data2: ", data2)
        compression_opts = dict(method='zip',
                        archive_name='out.csv')
        data2.to_csv('out.zip', index=False,
          compression=compression_opts)



        conn.close()

if __name__ == '__main__':
    main()
