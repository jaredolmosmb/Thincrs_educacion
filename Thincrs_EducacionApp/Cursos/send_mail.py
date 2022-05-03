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

        query2 = '''select * from resource;'''
        data2 = pd.read_sql_query(query2, conn)


        #for indx2, curso2 in data2.iterrows():
            #if indx2 == 0:
                #print("type(curso2.url) ", type(curso2.url))
                #print("curso2.url ", curso2.url) #url de los cursos de resource table 
        database = r"../db.sqlite3"

        # create a database connection
        conn2 = create_connection(database)
        cur = conn2.cursor()
        cur.execute("SELECT * FROM Cursos_coursemodel")



        rows = cur.fetchall()
        array_cursos=[]
        cont = 0
        for indx2, curso2 in data2.iterrows():
            cont = cont + 1
            if (curso2.url[30:36] == "course"):
                la_url = curso2.url[:29] + curso2.url[36:]
                indice_primer_slash = la_url[30:].find("/")
                sub_la_url = la_url[30:30+indice_primer_slash]#pedazo de string para buscar en  Cursos_coursemodel
                #print("sub_la_url en course", sub_la_url)
                if sub_la_url not in array_cursos:
                    array_cursos.append(sub_la_url)
            else:
                indice_primer_slash = la_url[30:].find("/")
                sub_la_url = la_url[30:30+indice_primer_slash]#pedazo de string para buscar en  Cursos_coursemodel
                #print("sub_la_url sin course", sub_la_url)
                if sub_la_url not in array_cursos:
                    array_cursos.append(sub_la_url)

        #en array_cursos estan todas las partes de la url que identifican a cada curso en resource
        array_cursoid = []
        for element in array_cursos:
            for indx3, el in enumerate(rows):
                if element+"/" in el[6]:
                    if el[3] not in array_cursoid:
                        array_cursoid.append(el[3])

        match_retirar_thincrs = []

        for indx, curso in data.iterrows(): #de la tbala course retiremodel
            for item in array_cursoid:
                if item == int(curso.id_course):
                    match_retirar_thincrs.append([curso.id_course, curso.title, curso.scheduled_removal_date, curso.alternative_course_1, curso.title_alternative_course_1, curso.alternative_course_2, curso.title_alternative_course_2])

        #print("len(match_retirar_thincrs): ", len(match_retirar_thincrs))
        #print("match_retirar_thincrs: ", match_retirar_thincrs)


                #if indx3 == 0:
                 #   print("el[6]", el[6])#obtener el url
                  #  print("type(el[6]) ",type(el[6]))s

        """print("array_cursoid: ", array_cursoid)
                                        print("len(array_cursoid: ", len(array_cursoid))"""


        """for indx3, el in enumerate(rows):
                                            if indx3 == 0:
                                                print("el[6]", el[6])#obtener el url
                                                print("type(el[6]) ",type(el[6]))
                                
                                                print("el[3]", el[3])#obtener el id
                                                print("type(el[3]) ",type(el[3]))"""

        conn.close()
        sender_email = "no-reply-educacion@thincrs.com"
        receiver_email = "alan@thincrs.com"
        receiver_email2 = "simon@thincrs.com"
        receiver_email3 = "miguel@thincrs.com"
        receiver_email4 = "jared@thincrs.com"
        receiver_email5 = "edgar@thincrs.com"
        password = "ThincrsPassword22"
        # creacion de texto plano y html
        message = MIMEMultipart("alternative")
        message["Subject"] = "Cursos Retirados test"
        message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        Hola"""

        match_dataframe = pd.DataFrame(match_retirar_thincrs)
        pd.set_option('colheader_justify', 'center')
        match_dataframe.columns =['id_course', 'Titulo', 'Fecha de Retiro', 'Curso alternativo 1', 'Titulo curso alternativo 1', 'Curso alternativo 2', 'Titulo curso alternativo 2']
        
        #print("match_dataframe: ", match_dataframe)
        #print("type(match_dataframe): ", type(match_dataframe))  
        html = """\
        <html>
          <body>
            <p>Los cursos por ser retirados asociados a trayectorias de clientes son los siguientes<br>
               {}
            </p>
          </body>
        </html>
        """.format(match_dataframe.to_html())

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
            server.sendmail(
                sender_email, receiver_email2, message.as_string()
            )
            server.sendmail(
                sender_email, receiver_email3, message.as_string()
            )

if __name__ == '__main__':
    main()
