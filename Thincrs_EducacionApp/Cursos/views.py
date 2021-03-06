from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages 
from .decorators import authenticated_user
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import requests
import pandas as pd
import json
from datetime import date
import math
import copy
import time
import re
import csv
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
#import markdownify
import html2markdown
import markdown
import chardet

from difflib import SequenceMatcher

import pymysql
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
import os

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
ACCOUNT_NAME= 'thincrs-one'
CLIENT_ID= 'cFLdzohBmNbxdjAiqCZlq2h1TBjEUw0foqYaFicf'
SECRET_ID= 'OkcFvpaNuAiao8FoC2S3UjJrj1gbJhU6ZFw3h2DPo4vIHy1g8uqOos1OyUApQgW1sFhpHXXskrk695zqcQ1NZ6fXoNrbj8PLqkspc9210mZcttMP53btfdB7phMTeXpN'
ACCOUNT_ID= '79612'

url = f'https://{ACCOUNT_NAME}.udemy.com/api-2.0/organizations/{ACCOUNT_ID}/courses/list/?page_size=12'

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def PruebaView(request):
    url = f'https://{ACCOUNT_NAME}.udemy.com/api-2.0/organizations/{ACCOUNT_ID}/courses/list/?page_size=12'

    while url:
        response = requests.get(url, auth=(CLIENT_ID, SECRET_ID))
        data = response.json()
        try:
            
            for indx, curso in enumerate(data['results']):
                if 'es' in curso['locale']['locale'] or 'en' in curso['locale']['locale'] or 'fr' in curso['locale']['locale'] or 'pt' in curso['locale']['locale']:
                    c = CourseModel(
                        id_course = curso['id'],
                        title=curso['title'],
                        description=cleanhtml(curso['description']),
                        url=curso['url'],
                        estimated_content_length=curso['estimated_content_length'],
                        has_closed_caption=curso['has_closed_caption'],
                        what_you_will_learn='\n'.join([str(item) for item in curso['what_you_will_learn']['list']]),
                        language = '\n'.join([str(item) for item in curso['caption_languages']]),
                        name = '\n'.join([str(item) for item in curso['instructors']]),
                        requirements = '\n'.join([str(item) for item in curso['requirements']['list']]),
                        locale_description = curso['locale']['locale'],
                        category = '\n'.join([str(item) for item in curso['categories']]),
                        primary_category=curso['primary_category']['title'])

                    c.save()
                    print("guardado: "+indx)
                    
                else:
                    continue
        except:
            pass
       
        url = data['next']
       


    return render (request, 'Cursos/prueba.html')

@authenticated_user
def UpdateProcessView(request):
    if request.method == 'POST':
        archivo = request.POST.get('actualizacion-nombre', False)
        archivo2 = request.POST.get('retirar-nombre', False)

        cursos_guardados = []

        if archivo2:
            
            file2 = pd.read_excel(archivo2, 'To Be Retired')
            lista_values = file2.values.tolist()
        
        for i in range(2,len(lista_values)):
            #print(lista_values[i][0])
            #print(type(lista_values[i][0]))

            """id_course = models.IntegerField(unique = True)
                scheduled_removal_date = models.DateTimeField()
                language = models.CharField(max_length=2000)
                title=models.CharField(max_length=2000,null=True, blank=True)
                course_category = models.CharField(max_length=2000)
                course_subcategory = models.CharField(max_length=2000)
                alternative_course_1 = models.IntegerField()
                title_alternative_course_1 = models.IntegerField()
                alternative_course_2 = models.IntegerField()
                title_alternative_course_2 = models.IntegerField()"""
            """el_curso = CourseModel.objects.filter(id_course = 2329814)
                                                            print("el_curso")
                                                            if el_curso:
                                                                print(el_curso[0].id_course)
                                                                print(el_curso[0].category)"""

            if CourseModel.objects.filter(id_course = int(lista_values[i][0])).exists():

                if math.isnan(lista_values[i][6]):
                    if not CourseRetireModel.objects.filter(id_course = int(lista_values[i][0])).exists():
                        obj, created = CourseRetireModel.objects.update_or_create(
                                    id_course = int(lista_values[i][0]),
                                    scheduled_removal_date = lista_values[i][1],
                                    language = str(lista_values[i][2]),
                                    title = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).title),
                                    course_category = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).category),
                                    course_subcategory = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).primary_subcategory),
                                    alternative_course_1 = 0,
                                    title_alternative_course_1 = "",
                                    alternative_course_2 = 0,
                                    title_alternative_course_2= ""
                                    )
                
                elif math.isnan(lista_values[i][8]) and not math.isnan(lista_values[i][6]):
                    if not CourseRetireModel.objects.filter(id_course = int(lista_values[i][0])).exists():
                        obj, created = CourseRetireModel.objects.update_or_create(
                                    id_course = int(lista_values[i][0]),
                                    scheduled_removal_date = lista_values[i][1],
                                    language = str(lista_values[i][2]),
                                    title = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).title),
                                    course_category = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).category),
                                    course_subcategory = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).primary_subcategory),
                                    alternative_course_1 = int(lista_values[i][6]),
                                    title_alternative_course_1 = str(lista_values[i][7]),
                                    alternative_course_2 = 0,
                                    title_alternative_course_2= ""
                                    )
                else:
                    if not CourseRetireModel.objects.filter(id_course = int(lista_values[i][0])).exists():
                        obj, created = CourseRetireModel.objects.update_or_create(
                                    id_course = int(lista_values[i][0]),
                                    scheduled_removal_date = lista_values[i][1],
                                    language = str(lista_values[i][2]),
                                    title = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).title),
                                    course_category = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).category),
                                    course_subcategory = str(CourseModel.objects.get(id_course = int(lista_values[i][0])).primary_subcategory),
                                    alternative_course_1 = int(lista_values[i][6]),
                                    title_alternative_course_1 = str(lista_values[i][7]),
                                    alternative_course_2 = int(lista_values[i][8]),
                                    title_alternative_course_2= str(lista_values[i][9])
                                    )
            else:
               print("curso no existe")
        else:
            print("no existe archivo2")





        """
        file = pandas.read_csv(archivo, encoding='utf-8')
        #print(file)
        #print("type(file)", type(file))
        lista = file.values.tolist()
        #print(lista[0][0])
        cursos_a_buscar = []
        

        for i in lista:
            if 'ES' in str(i[2]) or 'EN' in str(i[2]):
                cursos_a_buscar.append(i[0])

        for i in cursos_a_buscar:
            url = f'https://{ACCOUNT_NAME}.udemy.com/api-2.0/organizations/{ACCOUNT_ID}/courses/list/{i}'
            response = requests.get(url, auth=(CLIENT_ID, SECRET_ID))
            data = response.json()
            #print("data", data)
            #print("type(data)",type(data))
            try:
                if response.status_code == 200:
                    obj, created = CourseModel.objects.update_or_create(
                        id_course = data['id'],
                        title=data['title'],
                        description=cleanhtml(data['description']),
                        url=data['url'],
                        estimated_content_length=data['estimated_content_length'],
                        category = '\n'.join([str(item) for item in data['categories']]),
                        num_lectures = data['num_lectures'],
                        num_videos = data['num_videos'],
                        name = '\n'.join([str(item) for item in data['instructors']]),
                        requirements = '\n'.join([str(item) for item in data['requirements']['list']]),
                        what_you_will_learn='\n'.join([str(item) for item in data['what_you_will_learn']['list']]),
                        locale_description = data['locale']['locale'],
                        is_practice_test_course = data['is_practice_test_course'],
                        primary_category=data['primary_category']['title'],
                        primary_subcategory=data['primary_subcategory']['title'],
                        num_quizzes = data['num_quizzes'],
                        num_practice_tests = data['num_practice_tests'],
                        has_closed_caption=data['has_closed_caption'],
                        caption_languages = '\n'.join([str(item) for item in data['caption_languages']]),
                        estimated_content_length_video = data['estimated_content_length_video'],
                        defaults={'id_course': data['id']},
                        )
                
                    #print("created", created)
                    if created:
                        cursos_guardados.append(data['id'])
                    
            except:
                pass"""


        #print("se guardaron :len(cursos_guardados)", len(cursos_guardados))
        return render(request, 'Cursos/actualizacion.html', {'cursos_guardados': cursos_guardados})
    return render(request, 'Cursos/actualizacion.html')

@authenticated_user
def ListaUsuariosView(request):
    todos_u=CustomUser.objects.all()
    return render(request, 'Cursos/ListaUsuarios.html', {'todos_u': todos_u})

#---configuraciones para BD thincrs en servidor de AWS
mypkey = paramiko.RSAKey.from_private_key_file("clave.pem")
# if you want to use ssh password use - ssh_password='your ssh password', bellow

"""sql_hostname = 'develop-instance.cici1guul97n.us-east-2.rds.amazonaws.com'
sql_username = 'develop_thincrs'
sql_password = 'Thincrs_password2021'
sql_main_database = 'Develop_thincrs'
sql_port = 3306"""

sql_hostname = 'production-instance.cici1guul97n.us-east-2.rds.amazonaws.com'
sql_username = 'production_doom'
sql_password = 'EduPaszword2021_'
sql_main_database = 'Production_thincrs'
sql_port = 3306

ssh_host = '18.222.146.90'
ssh_user = 'ubuntu'
ssh_port = 22
sql_ip = '1.1.1.1.1'
#----------Termina configuraciones en servidor de AWS


"""#---configuraciones para BD local
# if you want to use ssh password use - ssh_password='your ssh password', bellow
sql_hostname = '127.0.0.1'
sql_username = 'root'
sql_password = ''
sql_main_database = 'develop_thincrs'
sql_port = 3306
#-------Termina las configuraciones en Bd local"""

@authenticated_user
def CargaTrayectoriaView(request):
    lista_verificacion = []
    lista_verificacion_BD = []
    valido = True 
    valido2 = True
    if request.method == 'POST':
        form = ReaderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            

            #--------------preguntas del archivo nuevo a cargar
            file = form.cleaned_data.get('file')# archivo preguntas
            file2 = form.cleaned_data.get('file2')# archivo config
            obj = form.save(commit=False)
            #print("type(file): ", type(file))
            obj.file = file
            obj.file2 = file2
            obj.save()

            #f = obj.file.open('r')
            #reader_file = csv.reader(open(obj.file.path,'r'))
            with open(obj.file.path, 'rb') as f:
                result = chardet.detect(f.read())  # or readline if the file is large


            #pd.read_csv('filename.csv', )
            df = pd.read_csv(open(obj.file.path,'rb'), encoding=result['encoding'])#archivo de preguntas
            #dffile2 = pd.read_csv(open(obj.file2.path,'r'))# archivo de config
            #print("dffile2: ", dffile2)
            #print("reader_file ", reader_file)
            #-------obtener la descripcion de cada pregunta
            """  for indx, row in enumerate(reader_file):
                                              print("row[0]")
                                              print(row[0])"""

               
            #print(f.read())

            #comparacion consigo mismo (archivo de excel)
            valido = True
            
            for index, element in df.iterrows():#recorro lista para comparacion de elemento con los otros de la lista
              for index2, element2 in df.iterrows():#recorro lista para 
                if index<index2:
                    if element[0] == element2[0]:# verifico que compara solo preguntas con el mismo ID
                        probabilidad_similitud = similar(element[12], element2[12]) # sace nivel de similitudo de descripciones
                        #print("probabilidad_similitud: ", probabilidad_similitud)
                        if probabilidad_similitud >0.9 and probabilidad_similitud < 1.0:# si se sospecha de una descripcion que pudiera ser la misma se marca como invalido para carga ra bd
                            valido = False
                            lista_verificacion.append([element[0], index+2, index2+2])
                            print("La descripcion " +str(index)+ " es similar en un: " +str(probabilidad_similitud)+ " de la descripci??n " +str(index2)+ " podria tratarse de la misma pregunta. Favor de revisar DE LA PREGUNTA " +element[0])# se indica los renglones a revisar
            if valido:
              print("El excel mismo esta correcto pasar a evaluaci??n de BD completa")
            else:
              print("checar archivo de excel hay posible repeticion en el archivo")
              for pregunta in lista_verificacion:
                print("En la pregunta "+ str(pregunta[0]) + " en la linea "+str(pregunta[1])+ " y la linea "+str(pregunta[2]))

            #-------------Conexion a la BD de thincrs para sacar el total de preguntas de aws via ssh
            with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_pkey=mypkey,
                remote_bind_address=(sql_hostname, sql_port)) as tunnel:
                conn = pymysql.connect(host='127.0.0.1', user=sql_username,
                        passwd=sql_password, db=sql_main_database,
                        port=tunnel.local_bind_port)
                query2 = '''select * from question;'''
                df2 = pd.read_sql_query(query2, conn)
            #------Termina conexion de BD thincrs para sacer el totla de preguntas

            """for ind, fila in data2.iterrows():
                                                    if ind == 0:
                                                        print(markdownify.markdownify(fila[5]).replace("\n", "").replace("  "," "))"""
            #-------------Conexion a la BD de thincrs en local para sacar el total de preguntas
            #conn = pymysql.connect(host='127.0.0.1', user=sql_username,
             #       passwd=sql_password, db=sql_main_database,
              #      port=sql_port)
            #query2 = '''select * from question;'''
            #df2 = pd.read_sql_query(query2, conn)

            #--------------Conexion a la BD replica en local-------------
            
            

            valido2 = True
            #comparacion de archivo nuevo de trayectorias con todas las preguntas precargadas
            for index, element in df.iterrows():#recorro lista para comparacion de elemento con los otros de la lista
              for index2, element2 in df2.iterrows():#recorro lista de conjunto total de preguntas
                #if index == 16 and index2 == 522:
                #if index<index2: # asegurar que no se compara de manera reciproca
                  if element[0] == element2[4]:# verifico que compara solo preguntas con el mismo ID:
                    probabilidad_similitud = similar(element[12].replace("\n", "").replace("  "," "), html2markdown.convert(element2[5]).replace("\n", "").replace("  "," ").replace(" ![alt text]", "![alt text]").replace("&amp;space", "&space").replace("__", "**")) # saque nivel de similitud de descripciones

                    if probabilidad_similitud >0.9 and probabilidad_similitud < 1.0:# si se sospecha de una descripcion que pudiera ser la misma se marca como invalido para carga ra bd
                        #print("descripcion "+str(index+2)+" en preguntas2: ")
                        #print(element[12])
                        #print("descripcion "+str(index2+2)+" en out: ")
                        #print(markdownify.markdownify(element2[5]).replace("\n", "").replace("  "," "))
                        print("descripcion "+str(index+2)+" en preguntas2: ")
                        print(element[12].replace("\n", "").replace("  "," "))
                        print("descripcion "+str(index2+2)+" en out: ")
                        print(html2markdown.convert(element2[5]).replace("\n", "").replace("  "," ").replace(" ![alt text]", "![alt text]").replace("&amp;space", "&space").replace("__", "**"))
                        lista_verificacion_BD.append([element[0], index+2, index2+2, html2markdown.convert(element2[5]).replace("\n", "").replace("  "," ")])
                        valido2 = False
                        print("La descripcion " +str(index+2)+ " es similar en un: " +str(probabilidad_similitud)+ " de la descripci??n " +str(index2+2)+ " podria tratarse de la misma pregunta. Favor de revisar  " +element[0])# se indica los renglones a revisar
            if valido2:
              print("La nueva trayectoria es correcta cargar a BD")
            else:
              print("checar archivo de excel hay posible repeticion con alguna(s) pregunta(s) en la BD")

            para_prueba = True
            #if de prueba par ano utilizar el codigo que ya funciona para el archivo de config y una sola pregunta del archivo de preguntas
            if valido and valido2 and not para_prueba:
                print("entre en para prueba")
                #-----------------------------------INICIO DE CARGA DEL ARCHIVO DE CONFIG-------------------
                #------------------CARGA DE TABLA COURSE DEL ARCHIVO DE CONFIG-----------
                cur = conn.cursor()

                course_id_sql = cur.execute('''SELECT MAX(id) FROM course; ''')
                max_course_id = cur.fetchone()
                course_id = max_course_id[0] + 1

                #course_id = cur.execute('''SELECT * FROM `course`; ''') + 1
                course_name = dffile2.iloc[0][3]
                course_short_name_list = [ s[0]+s[1]+s[2] if len(s) >= 3 else s[0] for s in course_name.split() ]
                course_short_name = ''.join(course_short_name_list).upper()
                course_created_at = datetime.now()
                course_updated_at = datetime.now()
                course_descripcion_html = markdown.markdown(dffile2.iloc[0][4])
                cur.execute('''INSERT INTO `course` VALUES ({},1,'art - digital.svg',"{}","{}",'',"{}","{}",1,"{}",NULL,1,1,30,1,NULL,NULL,NULL,0,NULL,NULL,'published',1,1,0)'''.format (course_id, course_name, course_short_name, course_created_at, course_updated_at, course_descripcion_html))            
                conn.commit()
                print("se hizo la insercion en tabla course checar en BD con id = ", course_id)

                #------------------CARGA DE TABLA EVALUATION DEL ARCHIVO DE CONFIG-----------
                #evaluation_id = cur.execute('''SELECT * FROM `evaluation`; ''') + 1

                evaluation_id_sql = cur.execute('''SELECT MAX(id) FROM evaluation; ''')
                max_evaluation_id = cur.fetchone()
                evaluation_id = max_evaluation_id[0] + 1

                evaluation_name = dffile2.iloc[0][0]
                evaluation_instructions = markdown.markdown(dffile2.iloc[0][5])
                evaluation_limit_time = 0
                if dffile2.iloc[0][11] == "pre-assesment" :
                    evaluation_limit_time = 15
                evaluation_min_score = dffile2.iloc[0][6]
                evaluation_weight = dffile2.iloc[0][8]
                evaluation_max_intents = dffile2.iloc[0][7]
                evaluation_created_at = datetime.now()
                evaluation_updated_at = datetime.now()
                evaluation_type = dffile2.iloc[0][11]
               
                evaluation_type_id_sql = cur.execute('''SELECT id FROM `evaluation_type` WHERE `name` = "{}"; '''.format(evaluation_type))
                evaluation_type_id = cur.fetchone()
                cur.execute('''INSERT INTO `evaluation` VALUES ({},1,NULL,"{}",'',"{}",NULL,NULL,{},{},{},{},1,1,0,"{}","{}",1,{},0,8,'published',0,0,NULL,1,NULL)'''.format (evaluation_id, evaluation_name, evaluation_instructions, evaluation_limit_time, evaluation_min_score, evaluation_weight, evaluation_max_intents, evaluation_created_at, evaluation_updated_at, evaluation_type_id[0]))
                conn.commit()
                print("se hizo la insercion en tabla evaluation checar en BD con id: ", evaluation_id)
                #------------------TABLA EVALUATION_METHOD------------------
                #evaluation_method_id = cur.execute('''SELECT * FROM `evaluation_method`; ''') + 1

                evaluation_method_id_sql = cur.execute('''SELECT MAX(id) FROM evaluation_method; ''')
                max_evaluation_method_id = cur.fetchone()
                evaluation_method_id = max_evaluation_method_id[0] + 1

                evaluation_method_evaluation = dffile2.iloc[0][0]
                evaluation_method_evaluation_id_sql = cur.execute('''SELECT id FROM `evaluation` WHERE `name` = "{}"; '''.format(evaluation_method_evaluation))
                evaluation_method_evaluation_id_fetch = cur.fetchone()
                if evaluation_method_evaluation_id_fetch:
                    evaluation_method_evaluation_id = evaluation_method_evaluation_id_fetch[0]

                evaluation_method_created_at = datetime.now()
                evaluation_method_updated_at = datetime.now()


                cur.execute('''INSERT INTO `evaluation_method` VALUES ({},{},'',25,"{}","{}")'''.format (evaluation_method_id, evaluation_method_evaluation_id, evaluation_method_created_at, evaluation_method_updated_at))
                conn.commit()
                print("se hizo la insercion en tabla evaluation_method checar en BD con id: ", evaluation_method_id)
             
                #------------------TABLA EVALUATION_RULE------------------
                #evaluation_rule_id = cur.execute('''SELECT * FROM `evaluation_rule`; ''') + 1

                evaluation_rule_id_sql = cur.execute('''SELECT MAX(id) FROM evaluation_rule; ''')
                max_evaluation_rule_id = cur.fetchone()
                evaluation_rule_id = max_evaluation_rule_id[0] + 1

                evaluation_rule_evaluation = dffile2.iloc[0][0]
                evaluation_rule_evaluation_id_sql = cur.execute('''SELECT id FROM `evaluation` WHERE `name` = "{}"; '''.format(evaluation_rule_evaluation))
                evaluation_rule_evaluation_id_fetch = cur.fetchone()
                if evaluation_rule_evaluation_id_fetch:
                    evaluation_rule_evaluation_id = evaluation_rule_evaluation_id_fetch[0]

                evaluation_rule_created_at = datetime.now()
                evaluation_rule_updated_at = datetime.now()

                cur.execute('''INSERT INTO `evaluation_rule` VALUES ({},4,"",{},"{}","{}")'''.format (evaluation_rule_id, evaluation_rule_evaluation_id, evaluation_rule_created_at, evaluation_rule_updated_at))
                conn.commit()
                print("se hizo la insercion en tabla evaluation_rule checar en BD con id: ", evaluation_rule_id)
                #-----------------------------------FIN DE CARGA DEL ARCHIVO DE CONFIG-------------------

                #-----------------------------------INICIO DE CARGA DEL ARCHIVO DE PREGUNTAS-------------------
                #df es el dataframe del archivo de data
                print("len(df.iterrows())")
                #print(len(df.iterrows()))
                for ind1, elem1 in df.iterrows():
                    igual = False
                    #ID_Pregunta = elem1[0]
                    ID_Pregunta = elem1[0]
                    #-----------Hay que cambiar todo el df.iloc[0] por elem1 en la seccion de alta
                    print("ID_Pregunta: ", ID_Pregunta)
                    #DF2 es el dataframe de las preguntas en la base de datos
                    for ind2, elem2 in df2.iterrows():
                        #comparacion por id para checar si est ala pregunta
                        #si esta la pregunta en la base de datos hay dos posibilidades que se agregue otro parrafo, o que se agregue solo lo demas porque la similitud es 1
                        if ID_Pregunta == elem2[4]:
                            igual = True
                            probabilidad_similitud2 = similar(elem1[12].replace("\n", "").replace("  "," "), html2markdown.convert(elem2[5]).replace("\n", "").replace("  "," ").replace(" ![alt text]", "![alt text]"))
                            print("misma pregunta por id = ", elem2[0])
                            if probabilidad_similitud2 == 1:
                                print("igual a 1")
                                #----------------------------------------------------------------no insertar pregunta solo todo lo demas-----------------------------
                                #------------------TABLA QUESTION------------------
                                #question_id = cur.execute('''SELECT * FROM `question`; ''') + 1

                                question_id_sql = cur.execute('''SELECT MAX(id) FROM question; ''')
                                max_question_id = cur.fetchone()
                                question_id = max_question_id[0] + 1

                                question_type = elem1[8]
                                question_type_id_sql = cur.execute('''SELECT id FROM `question_type` WHERE `name` = "{}"; '''.format(question_type))
                                question_question_type_id_fetch = cur.fetchone()
                                if question_question_type_id_fetch:
                                    question_question_type_id = question_question_type_id_fetch[0]
                                else:
                                    #question_type_id = cur.execute('''SELECT * FROM `question_type`; ''') + 1

                                    question_type_id_sql = cur.execute('''SELECT MAX(id) FROM question_type; ''')
                                    max_question_type_id = cur.fetchone()
                                    question_type_id = max_question_type_id[0] + 1

                                    question_type_created_at = datetime.now()
                                    question_type_updated_at = datetime.now()
                                    cur.execute('''INSERT INTO `question_type` VALUES ({},"{}","{}", NULL,"{}","{}"  )'''.format(question_type_id, question_type, question_type, question_type_created_at, question_type_updated_at)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla question_type checar en BD con id: ", question_type_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_question_type_id = question_type_id       

                                question_shortname = elem1[0]
                                question_question = markdown.markdown(elem1[12]) 
                                question_created_at = datetime.now()
                                question_updated_at = datetime.now()

                                question_category = elem1[7]
                                question_category_id_sql = cur.execute('''SELECT id FROM `question_category` WHERE `name` = "{}"; '''.format(question_category))
                                question_question_category_id_fetch = cur.fetchone()
                                if question_question_category_id_fetch:
                                    question_question_category_id = question_question_category_id_fetch[0]
                                else:
                                    #question_category_id = cur.execute('''SELECT * FROM `question_category`; ''') + 1

                                    question_category_id_sql = cur.execute('''SELECT MAX(id) FROM question_category; ''')
                                    max_question_category_id = cur.fetchone()
                                    question_category_id = max_question_category_id[0] + 1

                                    question_category_created_at = datetime.now()
                                    question_category_updated_at = datetime.now()
                                    cur.execute('''INSERT INTO `question_category` VALUES ({},"{}","{}","{}"  )'''.format(question_category_id, question_category, question_category, question_category_created_at, question_category_updated_at)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla question_category checar en BD con id: ", question_category_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_question_category_id = question_category_id 

                                question_level = elem1[10]
                                question_instructions = markdown.markdown(elem1[11]) 
                                question_code = elem1[1]
                                #question count nromal termina en 2497
                                #cur.execute('''INSERT INTO `question` VALUES ({},{},1,NULL,"{}","{}",0,"{}","{}",{},{},"{}","{}")'''.format(question_id, question_question_type_id, question_shortname, question_question, question_created_at, question_updated_at, question_question_category_id, question_level, question_instructions, question_code))
                                #conn.commit()
                                #print("se hizo la insercion en tabla question checar en BD con id: ", question_id)

                                #------------------TABLA QUESTION_COMPETENCE------------------
                                 
                                #question_competence_id = cur.execute('''SELECT * FROM `question_competence`; ''') + 1

                                question_competence_id_sql = cur.execute('''SELECT MAX(id) FROM question_competence; ''')
                                max_question_competence_id = cur.fetchone()
                                question_competence_id = max_question_competence_id[0] + 1

                                question_competence_question = elem1[0]
                                question_competence_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(question_competence_question))
                                question_competence_question_id_fetch = cur.fetchone()
                                if question_competence_question_id_fetch:
                                    question_competence_question_id = question_competence_question_id_fetch[0]

                                question_competence_competence = elem1[2]
                                question_competence_competence_id_sql = cur.execute('''SELECT id FROM `competence` WHERE `shortname` = "{}"; '''.format(question_competence_competence))
                                question_competence_competence_id_fetch = cur.fetchone()
                                if question_competence_competence_id_fetch:
                                    question_competence_competence_id = question_competence_competence_id_fetch[0]
                                else:
                                    #competence_id = cur.execute('''SELECT * FROM `competence`; ''') + 1

                                    competence_id_sql = cur.execute('''SELECT MAX(id) FROM competence; ''')
                                    max_competence_id= cur.fetchone()
                                    competence_id = max_competence_id[0] + 1

                                    competence_name = elem1[3]
                                    competence_created_at = datetime.now()
                                    competence_updated_at = datetime.now()
                                    competence_shortname = elem1[2]
                                    cur.execute('''INSERT INTO `competence` VALUES ({},1,NULL,"{}",NULL,NULL,NULL,"{}","{}","{}",NULL,'published')'''.format(competence_id, competence_name, competence_created_at, competence_updated_at, competence_shortname)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla competence checar en BD con id: ", competence_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_competence_competence_id = competence_id

                                if elem1[4] == "null":
                                    question_competence_order = 0
                                else:
                                    question_competence_order = 1

                                question_competence_created_at = datetime.now()
                                question_competence_updated_at = datetime.now()
                                #en la bd los registros son de 2637
                                cur.execute('''INSERT INTO `question_competence` VALUES ({},{},{},{},"{}","{}")'''.format(question_competence_id, question_competence_question_id, question_competence_competence_id, question_competence_order, question_competence_created_at, question_competence_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla question_competence checar en BD con id: ", question_competence_id)

                                #------------------TABLA ANSWER------------------
                                

                                answer_answer1 = str(elem1[13]) #primer respuesta del archivo pregunta
                                if "nan" not in answer_answer1 and len(answer_answer1) != 3:
                                    
                                    max_answer_id_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id = max_answer_id[0] + 1

                                    answer_question = elem1[0]
                                    answer_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question))
                                    answer_question_id_fetch = cur.fetchone()
                                    if answer_question_id_fetch:
                                        answer_question_id = answer_question_id_fetch[0]
                                    
                                    answer_answer1_html = markdown.markdown(answer_answer1)
                                    
                                    answer_qualification1 = elem1[14]
                                    answer_order1 = elem1[14]
                                    answer_created_at1 = datetime.now()
                                    answer_updated_at1 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id, answer_question_id, answer_answer1_html, answer_qualification1, answer_order1, answer_created_at1, answer_updated_at1))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id)
                                answer_answer2 = str(elem1[15]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer2 and len(answer_answer2) != 3:
                                    max_answer_id2_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id2 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id2 = max_answer_id2[0] + 1

                                    answer_question2 = elem1[0]
                                    answer_question2_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question2))
                                    answer_question2_id_fetch = cur.fetchone()
                                    if answer_question2_id_fetch:
                                        answer_question2_id = answer_question2_id_fetch[0]
                                    
                                    answer_answer2_html = markdown.markdown(answer_answer2)
                                    
                                    answer_qualification2 = elem1[16]
                                    answer_order2 = elem1[16]
                                    answer_created_at2 = datetime.now()
                                    answer_updated_at2 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id2, answer_question2_id, answer_answer2_html, answer_qualification2, answer_order2, answer_created_at2, answer_updated_at2))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id2)


                                answer_answer3 = str(elem1[17]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer3 and len(answer_answer3) != 3:
                                    max_answer_id3_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id3 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id3 = max_answer_id3[0] + 1

                                    answer_question3 = elem1[0]
                                    answer_question3_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question3))
                                    answer_question3_id_fetch = cur.fetchone()
                                    if answer_question3_id_fetch:
                                        answer_question3_id = answer_question3_id_fetch[0]
                                    
                                    answer_answer3_html = markdown.markdown(answer_answer3)
                                    
                                    answer_qualification3 = elem1[18]
                                    answer_order3 = elem1[18]
                                    answer_created_at3 = datetime.now()
                                    answer_updated_at3 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id3, answer_question3_id, answer_answer3_html, answer_qualification3, answer_order3, answer_created_at3, answer_updated_at3))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id3)

                                answer_answer4 = str(elem1[19]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer4 and len(answer_answer4) != 3: 
                                    max_answer_id4_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id4 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id4 = max_answer_id4[0] + 1

                                    answer_question4 = elem1[0]
                                    answer_question4_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question4))
                                    answer_question4_id_fetch = cur.fetchone()
                                    if answer_question4_id_fetch:
                                        answer_question4_id = answer_question4_id_fetch[0]
                                    
                                    answer_answer4_html = markdown.markdown(answer_answer4)
                                    
                                    answer_qualification4 = elem1[20]
                                    answer_order4 = elem1[20]
                                    answer_created_at4 = datetime.now()
                                    answer_updated_at4 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id4, answer_question4_id, answer_answer4_html, answer_qualification4, answer_order4, answer_created_at4, answer_updated_at4))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id4)

                                #------------------TABLA FEEDBACK------------------

                                max_feedback_id_sql = cur.execute('''SELECT MAX(id) FROM feedback; ''')
                                max_feedback_id = cur.fetchone()
                                feedback_id = max_feedback_id[0] + 1
                                feedback_description = elem1[21]
                                feedback_created_at = datetime.now()
                                feedback_updated_at = datetime.now()


                                cur.execute('''INSERT INTO `feedback` VALUES ({},NULL,"{}",1,NULL,"{}","{}",1)'''.format(feedback_id, feedback_description, feedback_created_at, feedback_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla feedback checar en BD con id: ", feedback_id)
                            
                                
                                #------------------TABLA FEEDBACK_RESOURCE------------------
                                max_feedback_resource_id_sql = cur.execute('''SELECT MAX(id) FROM feedback_resource; ''')
                                max_feedback_resource_id = cur.fetchone()
                                feedback_resource_id = max_feedback_resource_id[0] + 1

                                feedback_resource_feedback = elem1[21]
                                feedback_resource_feedback_id_sql = cur.execute('''SELECT id FROM `feedback` WHERE `description` = "{}"; '''.format(feedback_resource_feedback))
                                feedback_resource_feedback_id_fetch = cur.fetchone()
                                if feedback_resource_feedback_id_fetch:
                                    fedback_resource_feedback_id = feedback_resource_feedback_id_fetch[0]

                                feedback_resource_resource1 = str(elem1[22])
                                if "nan" not in feedback_resource_resource1 and len(feedback_resource_resource1) != 3:
                                    feedback_resource_resource1_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource1))
                                    feedback_resource_resource1_id_fetch = cur.fetchone()
                                    if feedback_resource_resource1_id_fetch:
                                        feedback_resource_resource1_id = feedback_resource_resource1_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 1/3-------------------
                                        max_resource1_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource1_id = cur.fetchone()
                                        resource1_id = max_resource1_id[0] + 1

                                        resource1_name = elem1[22]
                                        resource1_url = elem1[23]
                                        resource1_language = elem1[24]
                                        resource1_created_at = datetime.now()
                                        resource1_updated_at = datetime.now()

                                        feedback_resource_resource1_id = resource1_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource1_id, resource1_name, resource1_url, resource1_language, resource1_created_at, resource1_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource1_id)

                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource1_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                                feedback_resource_resource2 = str(elem1[25])
                                if "nan" not in feedback_resource_resource2 and len(feedback_resource_resource2) != 3:
                                    feedback_resource_resource2_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource2))
                                    feedback_resource_resource2_id_fetch = cur.fetchone()
                                    if feedback_resource_resource2_id_fetch:
                                        feedback_resource_resource2_id = feedback_resource_resource2_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 2/3-------------------
                                        max_resource2_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource2_id = cur.fetchone()
                                        resource2_id = max_resource2_id[0] + 1

                                        resource2_name = elem1[25]
                                        resource2_url = elem1[26]
                                        resource2_language = elem1[27]
                                        resource2_created_at = datetime.now()
                                        resource2_updated_at = datetime.now()

                                        feedback_resource_resource2_id = resource2_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource2_id, resource2_name, resource2_url, resource2_language, resource2_created_at, resource1_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource2_id)
                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource2_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                                feedback_resource_resource3 = str(elem1[28])
                                if "nan" not in feedback_resource_resource3 and len(feedback_resource_resource3) != 3:
                                    feedback_resource_resource3_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource3))
                                    feedback_resource_resource3_id_fetch = cur.fetchone()
                                    if feedback_resource_resource3_id_fetch:
                                        feedback_resource_resource3_id = feedback_resource_resource3_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 3/3-------------------
                                        max_resource3_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource3_id = cur.fetchone()
                                        resource3_id = max_resource3_id[0] + 1

                                        resource3_name = elem1[28]
                                        resource3_url = elem1[29]
                                        resource3_language = elem1[30]
                                        resource3_created_at = datetime.now()
                                        resource3_updated_at = datetime.now()

                                        feedback_resource_resource3_id = resource3_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource3_id, resource3_name, resource3_url, resource3_language, resource3_created_at, resource3_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource3_id)
                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource3_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)
                                    #------------------------------------------------termina "no insertar pregunta solo todo lo demas"--------------------------------------
                            else:
                                print("igual a 2")
                                #------------------------------------------------a??adir la descricpion del csv a la pregunta en la columna question convertida a html"--------------------------------------
                                #------------------TABLA QUESTION------------------
                                #question_id = cur.execute('''SELECT * FROM `question`; ''') + 1

                                question_id_sql = cur.execute('''SELECT MAX(id) FROM question; ''')
                                max_question_id = cur.fetchone()
                                question_id = max_question_id[0] + 1

                                question_type = elem1[8]
                                question_type_id_sql = cur.execute('''SELECT id FROM `question_type` WHERE `name` = "{}"; '''.format(question_type))
                                question_question_type_id_fetch = cur.fetchone()
                                if question_question_type_id_fetch:
                                    question_question_type_id = question_question_type_id_fetch[0]
                                else:
                                    question_type_id = cur.execute('''SELECT * FROM `question_type`; ''') + 1
                                    question_type_created_at = datetime.now()
                                    question_type_updated_at = datetime.now()
                                    cur.execute('''INSERT INTO `question_type` VALUES ({},"{}","{}", NULL,"{}","{}"  )'''.format(question_type_id, question_type, question_type, question_type_created_at, question_type_updated_at)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla question_type checar en BD con id: ", question_type_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_question_type_id = question_type_id       

                                question_shortname = elem1[0]
                                question_question = markdown.markdown(elem1[12]) #descripcion del excel
                                question_question_elem2 = elem2[5] #descripcion de la base de datos
                                question_compuesto = question_question_elem2 + question_question
                                question_created_at = datetime.now()
                                question_updated_at = datetime.now()

                                question_category = elem1[7]
                                question_category_id_sql = cur.execute('''SELECT id FROM `question_category` WHERE `name` = "{}"; '''.format(question_category))
                                question_question_category_id_fetch = cur.fetchone()
                                if question_question_category_id_fetch:
                                    question_question_category_id = question_question_category_id_fetch[0]
                                else:
                                    question_category_id = cur.execute('''SELECT * FROM `question_category`; ''') + 1
                                    question_category_created_at = datetime.now()
                                    question_category_updated_at = datetime.now()
                                    cur.execute('''INSERT INTO `question_category` VALUES ({},"{}","{}","{}"  )'''.format(question_category_id, question_category, question_category, question_category_created_at, question_category_updated_at)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla question_category checar en BD con id: ", question_category_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_question_category_id = question_category_id 

                                question_level = elem1[10]
                                question_instructions = markdown.markdown(elem1[11]) 
                                question_code = elem1[1]
                                #question count nromal termina en 2497
                                cur.execute('''UPDATE `question` SET question="{}" WHERE short_name="{}";'''.format(question_compuesto, ID_Pregunta))
                                #
                                #cur.execute('''INSERT INTO `question` VALUES ({},{},1,NULL,"{}","{}",0,"{}","{}",{},{},"{}","{}")'''.format(question_id, question_question_type_id, question_shortname, question_question, question_created_at, question_updated_at, question_question_category_id, question_level, question_instructions, question_code))
                                conn.commit()
                                print("se hizo la insercion como update en tabla question checar en BD con id: ", question_id)

                                #------------------TABLA QUESTION_COMPETENCE------------------
                                 
                                #question_competence_id = cur.execute('''SELECT * FROM `question_competence`; ''') + 1

                                question_competence_id_sql = cur.execute('''SELECT MAX(id) FROM question_competence; ''')
                                max_question_competence_id = cur.fetchone()
                                question_competence_id = max_question_competence_id[0] + 1

                                question_competence_question = elem1[0]
                                question_competence_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(question_competence_question))
                                question_competence_question_id_fetch = cur.fetchone()
                                if question_competence_question_id_fetch:
                                    question_competence_question_id = question_competence_question_id_fetch[0]

                                question_competence_competence = elem1[2]
                                question_competence_competence_id_sql = cur.execute('''SELECT id FROM `competence` WHERE `shortname` = "{}"; '''.format(question_competence_competence))
                                question_competence_competence_id_fetch = cur.fetchone()
                                if question_competence_competence_id_fetch:
                                    question_competence_competence_id = question_competence_competence_id_fetch[0]
                                else:
                                    #competence_id = cur.execute('''SELECT * FROM `competence`; ''') + 1

                                    competence_id_sql = cur.execute('''SELECT MAX(id) FROM competence; ''')
                                    max_competence_id= cur.fetchone()
                                    competence_id = max_competence_id[0] + 1

                                    competence_name = elem1[3]
                                    competence_created_at = datetime.now()
                                    competence_updated_at = datetime.now()
                                    competence_shortname = elem1[2]
                                    cur.execute('''INSERT INTO `competence` VALUES ({},1,NULL,"{}",NULL,NULL,NULL,"{}","{}","{}",NULL,'published')'''.format(competence_id, competence_name, competence_created_at, competence_updated_at, competence_shortname)) 
                                    conn.commit()
                                    print("se hizo la insercion en tabla competence checar en BD con id: ", competence_id)
                                    #print("es none y se a;adio: ", question_type)
                                    question_competence_competence_id = competence_id

                                if elem1[4] == "null":
                                    question_competence_order = 0
                                else:
                                    question_competence_order = 1

                                question_competence_created_at = datetime.now()
                                question_competence_updated_at = datetime.now()
                                #en la bd los registros son de 2637
                                cur.execute('''INSERT INTO `question_competence` VALUES ({},{},{},{},"{}","{}")'''.format(question_competence_id, question_competence_question_id, question_competence_competence_id, question_competence_order, question_competence_created_at, question_competence_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla question_competence checar en BD con id: ", question_competence_id)

                                #------------------TABLA ANSWER------------------
                                

                                answer_answer1 = str(elem1[13]) #primer respuesta del archivo pregunta
                                if "nan" not in answer_answer1 and len(answer_answer1) != 3:
                                    
                                    max_answer_id_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id = max_answer_id[0] + 1

                                    answer_question = elem1[0]
                                    answer_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question))
                                    answer_question_id_fetch = cur.fetchone()
                                    if answer_question_id_fetch:
                                        answer_question_id = answer_question_id_fetch[0]
                                    
                                    answer_answer1_html = markdown.markdown(answer_answer1)
                                    
                                    answer_qualification1 = elem1[14]
                                    answer_order1 = elem1[14]
                                    answer_created_at1 = datetime.now()
                                    answer_updated_at1 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id, answer_question_id, answer_answer1_html, answer_qualification1, answer_order1, answer_created_at1, answer_updated_at1))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id)
                                answer_answer2 = str(elem1[15]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer2 and len(answer_answer2) != 3:
                                    max_answer_id2_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id2 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id2 = max_answer_id2[0] + 1

                                    answer_question2 = elem1[0]
                                    answer_question2_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question2))
                                    answer_question2_id_fetch = cur.fetchone()
                                    if answer_question2_id_fetch:
                                        answer_question2_id = answer_question2_id_fetch[0]
                                    
                                    answer_answer2_html = markdown.markdown(answer_answer2)
                                    
                                    answer_qualification2 = elem1[16]
                                    answer_order2 = elem1[16]
                                    answer_created_at2 = datetime.now()
                                    answer_updated_at2 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id2, answer_question2_id, answer_answer2_html, answer_qualification2, answer_order2, answer_created_at2, answer_updated_at2))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id2)


                                answer_answer3 = str(elem1[17]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer3 and len(answer_answer3) != 3:
                                    max_answer_id3_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id3 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id3 = max_answer_id3[0] + 1

                                    answer_question3 = elem1[0]
                                    answer_question3_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question3))
                                    answer_question3_id_fetch = cur.fetchone()
                                    if answer_question3_id_fetch:
                                        answer_question3_id = answer_question3_id_fetch[0]
                                    
                                    answer_answer3_html = markdown.markdown(answer_answer3)
                                    
                                    answer_qualification3 = elem1[18]
                                    answer_order3 = elem1[18]
                                    answer_created_at3 = datetime.now()
                                    answer_updated_at3 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id3, answer_question3_id, answer_answer3_html, answer_qualification3, answer_order3, answer_created_at3, answer_updated_at3))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id3)

                                answer_answer4 = str(elem1[19]) #segunda respuesta del archivo pregunta
                                if "nan" not in answer_answer4 and len(answer_answer4) != 3: 
                                    max_answer_id4_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                                    max_answer_id4 = cur.fetchone()
                                    #print("max_answer_id")
                                    #print(max_answer_id)
                                    answer_id4 = max_answer_id4[0] + 1

                                    answer_question4 = elem1[0]
                                    answer_question4_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question4))
                                    answer_question4_id_fetch = cur.fetchone()
                                    if answer_question4_id_fetch:
                                        answer_question4_id = answer_question4_id_fetch[0]
                                    
                                    answer_answer4_html = markdown.markdown(answer_answer4)
                                    
                                    answer_qualification4 = elem1[20]
                                    answer_order4 = elem1[20]
                                    answer_created_at4 = datetime.now()
                                    answer_updated_at4 = datetime.now()
                                    
                                    cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id4, answer_question4_id, answer_answer4_html, answer_qualification4, answer_order4, answer_created_at4, answer_updated_at4))
                                    conn.commit()
                                    print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id4)

                                #------------------TABLA FEEDBACK------------------

                                max_feedback_id_sql = cur.execute('''SELECT MAX(id) FROM feedback; ''')
                                max_feedback_id = cur.fetchone()
                                feedback_id = max_feedback_id[0] + 1
                                feedback_description = elem1[21]
                                feedback_created_at = datetime.now()
                                feedback_updated_at = datetime.now()


                                cur.execute('''INSERT INTO `feedback` VALUES ({},NULL,"{}",1,NULL,"{}","{}",1)'''.format(feedback_id, feedback_description, feedback_created_at, feedback_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla feedback checar en BD con id: ", feedback_id)
                            
                                
                                #------------------TABLA FEEDBACK_RESOURCE------------------
                                max_feedback_resource_id_sql = cur.execute('''SELECT MAX(id) FROM feedback_resource; ''')
                                max_feedback_resource_id = cur.fetchone()
                                feedback_resource_id = max_feedback_resource_id[0] + 1

                                feedback_resource_feedback = elem1[21]
                                feedback_resource_feedback_id_sql = cur.execute('''SELECT id FROM `feedback` WHERE `description` = "{}"; '''.format(feedback_resource_feedback))
                                feedback_resource_feedback_id_fetch = cur.fetchone()
                                if feedback_resource_feedback_id_fetch:
                                    fedback_resource_feedback_id = feedback_resource_feedback_id_fetch[0]

                                feedback_resource_resource1 = str(elem1[22])
                                if "nan" not in feedback_resource_resource1 and len(feedback_resource_resource1) != 3:
                                    feedback_resource_resource1_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource1))
                                    feedback_resource_resource1_id_fetch = cur.fetchone()
                                    if feedback_resource_resource1_id_fetch:
                                        feedback_resource_resource1_id = feedback_resource_resource1_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 1/3-------------------
                                        max_resource1_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource1_id = cur.fetchone()
                                        resource1_id = max_resource1_id[0] + 1

                                        resource1_name = elem1[22]
                                        resource1_url = elem1[23]
                                        resource1_language = elem1[24]
                                        resource1_created_at = datetime.now()
                                        resource1_updated_at = datetime.now()

                                        feedback_resource_resource1_id = resource1_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource1_id, resource1_name, resource1_url, resource1_language, resource1_created_at, resource1_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource1_id)

                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource1_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                                feedback_resource_resource2 = str(elem1[25])
                                if "nan" not in feedback_resource_resource2 and len(feedback_resource_resource2) != 3:
                                    feedback_resource_resource2_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource2))
                                    feedback_resource_resource2_id_fetch = cur.fetchone()
                                    if feedback_resource_resource2_id_fetch:
                                        feedback_resource_resource2_id = feedback_resource_resource2_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 2/3-------------------
                                        max_resource2_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource2_id = cur.fetchone()
                                        resource2_id = max_resource2_id[0] + 1

                                        resource2_name = elem1[25]
                                        resource2_url = elem1[26]
                                        resource2_language = elem1[27]
                                        resource2_created_at = datetime.now()
                                        resource2_updated_at = datetime.now()

                                        feedback_resource_resource2_id = resource2_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource2_id, resource2_name, resource2_url, resource2_language, resource2_created_at, resource1_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource2_id)
                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource2_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                                feedback_resource_resource3 = str(elem1[28])
                                if "nan" not in feedback_resource_resource3 and len(feedback_resource_resource3) != 3:
                                    feedback_resource_resource3_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource3))
                                    feedback_resource_resource3_id_fetch = cur.fetchone()
                                    if feedback_resource_resource3_id_fetch:
                                        feedback_resource_resource3_id = feedback_resource_resource3_id_fetch[0]
                                    else:
                                        #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 3/3-------------------
                                        max_resource3_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                        max_resource3_id = cur.fetchone()
                                        resource3_id = max_resource3_id[0] + 1

                                        resource3_name = elem1[28]
                                        resource3_url = elem1[29]
                                        resource3_language = elem1[30]
                                        resource3_created_at = datetime.now()
                                        resource3_updated_at = datetime.now()

                                        feedback_resource_resource3_id = resource3_id

                                        cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource3_id, resource3_name, resource3_url, resource3_language, resource3_created_at, resource3_updated_at))
                                        conn.commit()
                                        print("se hizo la insercion en tabla resource checar en BD con id: ", resource3_id)
                                    cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource3_id))
                                    conn.commit()
                                    print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)
                                    #------------------------------------------------termina "a??adir la descricpion del csv a la pregunta en la columna question convertida a html"--------------------------------------
                                #a??adir la descricpion del csv a la pregunta en la columna question convertida a html
                    if igual == False:

                        #------------------------------------------------a;adir pregunta a la Bs porque no existe--------------------------------------
                        #------------------TABLA QUESTION------------------
                        #question_id = cur.execute('''SELECT * FROM `question`; ''') + 1

                        question_id_sql = cur.execute('''SELECT MAX(id) FROM question; ''')
                        max_question_id = cur.fetchone()
                        question_id = max_question_id[0] + 1

                        question_type = elem1[8]
                        question_type_id_sql = cur.execute('''SELECT id FROM `question_type` WHERE `name` = "{}"; '''.format(question_type))
                        question_question_type_id_fetch = cur.fetchone()
                        if question_question_type_id_fetch:
                            question_question_type_id = question_question_type_id_fetch[0]
                        else:
                            question_type_id = cur.execute('''SELECT * FROM `question_type`; ''') + 1
                            question_type_created_at = datetime.now()
                            question_type_updated_at = datetime.now()
                            cur.execute('''INSERT INTO `question_type` VALUES ({},"{}","{}", NULL,"{}","{}"  )'''.format(question_type_id, question_type, question_type, question_type_created_at, question_type_updated_at)) 
                            conn.commit()
                            print("se hizo la insercion en tabla question_type checar en BD con id: ", question_type_id)
                            #print("es none y se a;adio: ", question_type)
                            question_question_type_id = question_type_id       

                        question_shortname = elem1[0]
                        question_question = markdown.markdown((elem1[12]).replace("![alt text]", " ![alt text]")) #descripcion del excel
                        print("question_question convertido a html: ", question_question)
                        question_question = question_question.replace("![alt text]", " ![alt text]")
                        print("question_question convertido a html y remplazando el alt: ", question_question)

                        question_question_elem2 = elem2[5] #descripcion de la base de datos
                        question_compuesto = question_question_elem2 + question_question
                        question_created_at = datetime.now()
                        question_updated_at = datetime.now()

                        question_category = elem1[7]
                        question_category_id_sql = cur.execute('''SELECT id FROM `question_category` WHERE `name` = "{}"; '''.format(question_category))
                        question_question_category_id_fetch = cur.fetchone()
                        if question_question_category_id_fetch:
                            question_question_category_id = question_question_category_id_fetch[0]
                        else:
                            question_category_id = cur.execute('''SELECT * FROM `question_category`; ''') + 1
                            question_category_created_at = datetime.now()
                            question_category_updated_at = datetime.now()
                            cur.execute('''INSERT INTO `question_category` VALUES ({},"{}","{}","{}"  )'''.format(question_category_id, question_category, question_category, question_category_created_at, question_category_updated_at)) 
                            conn.commit()
                            print("se hizo la insercion en tabla question_category checar en BD con id: ", question_category_id)
                            #print("es none y se a;adio: ", question_type)
                            question_question_category_id = question_category_id 

                        question_level = elem1[10]
                        question_instructions = markdown.markdown(elem1[11]) 
                        question_code = elem1[1]
                        #question count nromal termina en 2497
                        #cur.execute('''UPDATE `question` SET question="{}" WHERE short_name="{}";'''.format(question_compuesto, ID_Pregunta))
                        #
                        cur.execute('''INSERT INTO `question` VALUES ({},{},1,NULL,"{}","{}",0,"{}","{}",{},{},"{}","{}")'''.format(question_id, question_question_type_id, question_shortname, question_question, question_created_at, question_updated_at, question_question_category_id, question_level, question_instructions, question_code))
                        conn.commit()
                        print("se hizo la insercion en tabla question checar en BD con id: ", question_id)

                        #------------------TABLA QUESTION_COMPETENCE------------------
                         
                        #question_competence_id = cur.execute('''SELECT * FROM `question_competence`; ''') + 1

                        question_competence_id_sql = cur.execute('''SELECT MAX(id) FROM question_competence; ''')
                        max_question_competence_id = cur.fetchone()
                        question_competence_id = max_question_competence_id[0] + 1

                        question_competence_question = elem1[0]
                        question_competence_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(question_competence_question))
                        question_competence_question_id_fetch = cur.fetchone()
                        if question_competence_question_id_fetch:
                            question_competence_question_id = question_competence_question_id_fetch[0]

                        question_competence_competence = elem1[2]
                        question_competence_competence_id_sql = cur.execute('''SELECT id FROM `competence` WHERE `shortname` = "{}"; '''.format(question_competence_competence))
                        question_competence_competence_id_fetch = cur.fetchone()
                        if question_competence_competence_id_fetch:
                            question_competence_competence_id = question_competence_competence_id_fetch[0]
                        else:
                            #competence_id = cur.execute('''SELECT * FROM `competence`; ''') + 1

                            competence_id_sql = cur.execute('''SELECT MAX(id) FROM competence; ''')
                            max_competence_id= cur.fetchone()
                            competence_id = max_competence_id[0] + 1

                            competence_name = elem1[3]
                            competence_created_at = datetime.now()
                            competence_updated_at = datetime.now()
                            competence_shortname = elem1[2]
                            cur.execute('''INSERT INTO `competence` VALUES ({},1,NULL,"{}",NULL,NULL,NULL,"{}","{}","{}",NULL,'published')'''.format(competence_id, competence_name, competence_created_at, competence_updated_at, competence_shortname)) 
                            conn.commit()
                            print("se hizo la insercion en tabla competence checar en BD con id: ", competence_id)
                            #print("es none y se a;adio: ", question_type)
                            question_competence_competence_id = competence_id

                        if elem1[4] == "null":
                            question_competence_order = 0
                        else:
                            question_competence_order = 1

                        question_competence_created_at = datetime.now()
                        question_competence_updated_at = datetime.now()
                        #en la bd los registros son de 2637
                        cur.execute('''INSERT INTO `question_competence` VALUES ({},{},{},{},"{}","{}")'''.format(question_competence_id, question_competence_question_id, question_competence_competence_id, question_competence_order, question_competence_created_at, question_competence_updated_at))
                        conn.commit()
                        print("se hizo la insercion en tabla question_competence checar en BD con id: ", question_competence_id)

                        #------------------TABLA ANSWER------------------
                        

                        answer_answer1 = str(elem1[13]) #primer respuesta del archivo pregunta
                        if "nan" not in answer_answer1 and len(answer_answer1) != 3:
                            
                            max_answer_id_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                            max_answer_id = cur.fetchone()
                            #print("max_answer_id")
                            #print(max_answer_id)
                            answer_id = max_answer_id[0] + 1

                            answer_question = elem1[0]
                            answer_question_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question))
                            answer_question_id_fetch = cur.fetchone()
                            if answer_question_id_fetch:
                                answer_question_id = answer_question_id_fetch[0]
                            
                            answer_answer1_html = markdown.markdown(answer_answer1)
                            
                            answer_qualification1 = elem1[14]
                            answer_order1 = elem1[14]
                            answer_created_at1 = datetime.now()
                            answer_updated_at1 = datetime.now()
                            
                            cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id, answer_question_id, answer_answer1_html, answer_qualification1, answer_order1, answer_created_at1, answer_updated_at1))
                            conn.commit()
                            print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id)
                        answer_answer2 = str(elem1[15]) #segunda respuesta del archivo pregunta
                        if "nan" not in answer_answer2 and len(answer_answer2) != 3:
                            max_answer_id2_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                            max_answer_id2 = cur.fetchone()
                            #print("max_answer_id")
                            #print(max_answer_id)
                            answer_id2 = max_answer_id2[0] + 1

                            answer_question2 = elem1[0]
                            answer_question2_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question2))
                            answer_question2_id_fetch = cur.fetchone()
                            if answer_question2_id_fetch:
                                answer_question2_id = answer_question2_id_fetch[0]
                            
                            answer_answer2_html = markdown.markdown(answer_answer2)
                            
                            answer_qualification2 = elem1[16]
                            answer_order2 = elem1[16]
                            answer_created_at2 = datetime.now()
                            answer_updated_at2 = datetime.now()
                            
                            cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id2, answer_question2_id, answer_answer2_html, answer_qualification2, answer_order2, answer_created_at2, answer_updated_at2))
                            conn.commit()
                            print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id2)


                        answer_answer3 = str(elem1[17]) #segunda respuesta del archivo pregunta
                        if "nan" not in answer_answer3 and len(answer_answer3) != 3:
                            max_answer_id3_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                            max_answer_id3 = cur.fetchone()
                            #print("max_answer_id")
                            #print(max_answer_id)
                            answer_id3 = max_answer_id3[0] + 1

                            answer_question3 = elem1[0]
                            answer_question3_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question3))
                            answer_question3_id_fetch = cur.fetchone()
                            if answer_question3_id_fetch:
                                answer_question3_id = answer_question3_id_fetch[0]
                            
                            answer_answer3_html = markdown.markdown(answer_answer3)
                            
                            answer_qualification3 = elem1[18]
                            answer_order3 = elem1[18]
                            answer_created_at3 = datetime.now()
                            answer_updated_at3 = datetime.now()
                            
                            cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id3, answer_question3_id, answer_answer3_html, answer_qualification3, answer_order3, answer_created_at3, answer_updated_at3))
                            conn.commit()
                            print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id3)

                        answer_answer4 = str(elem1[19]) #segunda respuesta del archivo pregunta
                        if "nan" not in answer_answer4 and len(answer_answer4) != 3: 
                            max_answer_id4_sql = cur.execute('''SELECT MAX(id) FROM answer; ''')
                            max_answer_id4 = cur.fetchone()
                            #print("max_answer_id")
                            #print(max_answer_id)
                            answer_id4 = max_answer_id4[0] + 1

                            answer_question4 = elem1[0]
                            answer_question4_id_sql = cur.execute('''SELECT id FROM `question` WHERE `short_name` = "{}"; '''.format(answer_question4))
                            answer_question4_id_fetch = cur.fetchone()
                            if answer_question4_id_fetch:
                                answer_question4_id = answer_question4_id_fetch[0]
                            
                            answer_answer4_html = markdown.markdown(answer_answer4)
                            
                            answer_qualification4 = elem1[20]
                            answer_order4 = elem1[20]
                            answer_created_at4 = datetime.now()
                            answer_updated_at4 = datetime.now()
                            
                            cur.execute('''INSERT INTO `answer` VALUES ({},{},"{}",{},{},"{}","{}")'''.format(answer_id4, answer_question4_id, answer_answer4_html, answer_qualification4, answer_order4, answer_created_at4, answer_updated_at4))
                            conn.commit()
                            print("se hizo la insercion en tabla answer checar en BD con id: ", answer_id4)

                        #------------------TABLA FEEDBACK------------------

                        max_feedback_id_sql = cur.execute('''SELECT MAX(id) FROM feedback; ''')
                        max_feedback_id = cur.fetchone()
                        feedback_id = max_feedback_id[0] + 1
                        feedback_description = elem1[21]
                        feedback_created_at = datetime.now()
                        feedback_updated_at = datetime.now()


                        cur.execute('''INSERT INTO `feedback` VALUES ({},NULL,"{}",1,NULL,"{}","{}",1)'''.format(feedback_id, feedback_description, feedback_created_at, feedback_updated_at))
                        conn.commit()
                        print("se hizo la insercion en tabla feedback checar en BD con id: ", feedback_id)
                    
                        
                        #------------------TABLA FEEDBACK_RESOURCE------------------
                        max_feedback_resource_id_sql = cur.execute('''SELECT MAX(id) FROM feedback_resource; ''')
                        max_feedback_resource_id = cur.fetchone()
                        feedback_resource_id = max_feedback_resource_id[0] + 1

                        feedback_resource_feedback = elem1[21]
                        feedback_resource_feedback_id_sql = cur.execute('''SELECT id FROM `feedback` WHERE `description` = "{}"; '''.format(feedback_resource_feedback))
                        feedback_resource_feedback_id_fetch = cur.fetchone()
                        if feedback_resource_feedback_id_fetch:
                            fedback_resource_feedback_id = feedback_resource_feedback_id_fetch[0]

                        feedback_resource_resource1 = str(elem1[22])
                        if "nan" not in feedback_resource_resource1 and len(feedback_resource_resource1) != 3:
                            feedback_resource_resource1_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource1))
                            feedback_resource_resource1_id_fetch = cur.fetchone()
                            if feedback_resource_resource1_id_fetch:
                                feedback_resource_resource1_id = feedback_resource_resource1_id_fetch[0]
                            else:
                                #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 1/3-------------------
                                max_resource1_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                max_resource1_id = cur.fetchone()
                                resource1_id = max_resource1_id[0] + 1

                                resource1_name = elem1[22]
                                resource1_url = elem1[23]
                                resource1_language = elem1[24]
                                resource1_created_at = datetime.now()
                                resource1_updated_at = datetime.now()

                                feedback_resource_resource1_id = resource1_id
                                print("resource1_id", resource1_id)
                                print("type(resource1_id)", type(resource1_id))

                                cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource1_id, resource1_name, resource1_url, resource1_language, resource1_created_at, resource1_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla resource checar en BD con id: ", resource1_id)

                            cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource1_id))
                            conn.commit()
                            print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                        feedback_resource_resource2 = str(elem1[25])
                        if "nan" not in feedback_resource_resource2 and len(feedback_resource_resource2) != 3:
                            feedback_resource_resource2_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource2))
                            feedback_resource_resource2_id_fetch = cur.fetchone()
                            if feedback_resource_resource2_id_fetch:
                                feedback_resource_resource2_id = feedback_resource_resource2_id_fetch[0]
                            else:
                                #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 2/3-------------------
                                max_resource2_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                max_resource2_id = cur.fetchone()
                                resource2_id = max_resource2_id[0] + 1

                                resource2_name = elem1[25]
                                resource2_url = elem1[26]
                                resource2_language = elem1[27]
                                resource2_created_at = datetime.now()
                                resource2_updated_at = datetime.now()

                                feedback_resource_resource2_id = resource2_id

                                cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource2_id, resource2_name, resource2_url, resource2_language, resource2_created_at, resource1_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla resource checar en BD con id: ", resource2_id)
                            cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource2_id))
                            conn.commit()
                            print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)

                        feedback_resource_resource3 = str(elem1[28])
                        if "nan" not in feedback_resource_resource3 and len(feedback_resource_resource3) != 3:
                            feedback_resource_resource3_id_sql = cur.execute('''SELECT id FROM `resource` WHERE `name` = "{}"; '''.format(feedback_resource_resource3))
                            feedback_resource_resource3_id_fetch = cur.fetchone()
                            if feedback_resource_resource3_id_fetch:
                                feedback_resource_resource3_id = feedback_resource_resource3_id_fetch[0]
                            else:
                                #------------------TABLA RESOURCE POR RESOURCE EN ARCHIVO DE PREGUNTAS 3/3-------------------
                                max_resource3_id_sql = cur.execute('''SELECT MAX(id) FROM resource; ''')
                                max_resource3_id = cur.fetchone()
                                resource3_id = max_resource3_id[0] + 1

                                resource3_name = elem1[28]
                                resource3_url = elem1[29]
                                resource3_language = elem1[30]
                                resource3_created_at = datetime.now()
                                resource3_updated_at = datetime.now()

                                feedback_resource_resource3_id = resource3_id

                                cur.execute('''INSERT INTO `resource` VALUES ({},"{}",NULL, "{}", 'web', "{}", 1, "{}", "{}")'''.format(resource3_id, resource3_name, resource3_url, resource3_language, resource3_created_at, resource3_updated_at))
                                conn.commit()
                                print("se hizo la insercion en tabla resource checar en BD con id: ", resource3_id)
                            cur.execute('''INSERT INTO `feedback_resource` VALUES (%s,%s,%s)''', (feedback_resource_id, fedback_resource_feedback_id, feedback_resource_resource3_id))
                            conn.commit()
                            print("se hizo la insercion en tabla feedback_resource checar en BD con id: ", feedback_resource_id)
                            #------------------------------------------------termina "a;adir pregunta a la Bs porque no existe"--------------------------------------
                        #a;adir pregunta a la Bs porque no existe
                        print("pregunta con ind1 = "+str(ind1)+" es diferente a las de la bd")



            #quitar para_prueba para que funciona la carga a BD
            if valido and valido2 and para_prueba:
               
                pass

                
                

                





            else:
                print("no se hizo la inserci??n a la BD porque se debe de verificar el archivo")

            open(obj.file.path,'r').close()
            #open(obj.file2.path,'r').close()
            os.remove(obj.file.path)
            #os.remove(obj.file2.path)
            return render(request, 'Cursos/carga_trayectoria.html',{'form': form, 'valido': valido, 'valido2': valido2, 'lista_verificacion' : lista_verificacion, 'lista_verificacion_BD' : lista_verificacion_BD})
            
            



    else:
        form = ReaderForm()
        return render(request, 'Cursos/carga_trayectoria.html',{'form': form, 'lista_verificacion' : lista_verificacion, 'lista_verificacion_BD' : lista_verificacion_BD})
    

    
@authenticated_user
def CursosView(request):
    """busqueda = request.GET.get("buscar")
                    #print("busqueda", busqueda)
                    primer =request.GET.get("mytext[1]")
                    #print("primer = ", primer)
                    segundo =request.GET.get("mytext[2]")
                    #print("segundo = ", segundo)
                    tercer =request.GET.get("mytext[3]")
                    #print("tercer = ", tercer)
                    cuarto =request.GET.get("mytext[4]")
                    #print("cuarto = ", cuarto)
                    quinto =request.GET.get("mytext[5]")
                    #print("quinto = ", quinto)
                    sexto =request.GET.get("mytext[6]")
                    #print("sexto = ", sexto)
                    septimo =request.GET.get("mytext[7]")
                    #print("septimo = ", septimo)
                    octavo =request.GET.get("mytext[8]")
                    #print("octavo = ", octavo)
                    noveno =request.GET.get("mytext[9]")
                    #print("noveno = ", noveno)
                    decimo =request.GET.get("mytext[10]")"""
    #print("decimo = ", decimo)

    conceptos = []
    conceptos_a_buscar = []
    expresion = ""

    for i in range(10):

        if i != 0:
            concepto = request.GET.get("mytext["+str(i+1)+"]")
            if concepto != None:
                conceptos.append(request.GET.get("bool"+str(i)+""))
                conceptos.append(request.GET.get("not"+str(i)+""))
                conceptos.append(concepto)
                
        else:
            conceptos.append(request.GET.get("not"+str(i)+""))
            conceptos.append(request.GET.get("mytext["+str(i+1)+"]"))

        # exoresion regular para negaci??n ^((?!hede).)*$

    #print("conceptos", conceptos)
    for index, elem in enumerate(conceptos):
        if index%3 == 0:            
            if elem == "not":
                conceptos_a_buscar.append("^((?!"+conceptos[index+1]+").)*$")
                if (index+2) < len(conceptos):
                    conceptos_a_buscar.append(conceptos[index+2])
                else:
                    continue
            elif elem == "normal":
                conceptos_a_buscar.append(conceptos[index+1])
                if (index+2) < len(conceptos):
                    conceptos_a_buscar.append(conceptos[index+2])
                else:
                    continue
    conceptos_listos = []
    for index2, elem2 in enumerate(conceptos_a_buscar):
        if elem2 == "or":
            conceptos_a_buscar[index2] = "|"

    if len(conceptos_a_buscar) == 1:
        conceptos_listos.append(conceptos_a_buscar[0])
    elif "and" not in conceptos_a_buscar:
        conceptos_listos = copy.deepcopy(conceptos_a_buscar)


    elif len(conceptos_a_buscar) > 1:
        #print("conceptos a buscar antes", conceptos_a_buscar)
        while "and" in conceptos_a_buscar:

            for index2, elem2 in enumerate(conceptos_a_buscar[::-1]):
                if conceptos_a_buscar[index2] == "and":
                    if "(?=.*" in conceptos_a_buscar[index2-1]:
                        primer = conceptos_a_buscar[index2-1]
                    else:
                        primer = "(?=.*"+conceptos_a_buscar[index2-1]+")"
                    if "(?=.*" in conceptos_a_buscar[index2+1]:
                        segundo = conceptos_a_buscar[index2+1]
                    else:
                        segundo = "(?=.*"+conceptos_a_buscar[index2+1]+")"
                    a = primer + segundo 
                    conceptos_a_buscar.pop(index2-1)
                    conceptos_a_buscar.pop(index2-1)
                    conceptos_a_buscar.pop(index2-1)
                    conceptos_a_buscar.insert(index2-1, a)
                    #print("conceptos a buscar en if", conceptos_a_buscar)
                    break


    #print("conceptos a buscar", conceptos_a_buscar)
    #print("conceptos_listos", conceptos_listos)
    frase_a_buscar = ""
    for i in conceptos_listos:
        frase_a_buscar = frase_a_buscar + i 
    #print("frase_a_buscar", frase_a_buscar)




    return render (request, 'Cursos/cursos.html')

@authenticated_user
def ListaCursosView(request):
    start_time = time.time()

    busqueda = request.GET.get("buscar")
    objetos = CourseModel.objects.all()
    """for i in objetos:
                    if len(i.caption_languages) == 0:
                        i.caption_languages = "N/A"
                        i.save()"""
    array = request.GET.get("este")
    list_to_filter=[]
    #print("array", array)
    #print("type(array)", type(array))
    if array == None or array == "":
        pass
    else:
        list_to_filter = array.split(",")
        #print("list_to_filter", list_to_filter)
        #print("type(list_to_filter", type(list_to_filter))
    inp = request.GET.get("mytext[1]")
    and_string = "&&"
    para_buscar=""
    conceptos = []
    if busqueda:      
        if and_string in busqueda:
            myArray = busqueda.split(" && ")
            for i in myArray:
                para_buscar= para_buscar+"(?=.*"+i+")"
            todos_c = CourseModel.objects.all()
            todos_m = todos_c.filter(
                Q(title__iregex=para_buscar) |
                Q(description__iregex=para_buscar) |
                Q(url__iregex=para_buscar) |
                Q(category__iregex=para_buscar) |
                Q(name__iregex=para_buscar) |
                Q(requirements__iregex=para_buscar) |
                Q(what_you_will_learn__iregex=para_buscar) |
                Q(locale_description__iregex=para_buscar) |
                Q(primary_category__iregex=para_buscar) |
                Q(primary_subcategory__iregex=para_buscar)|
                Q(caption_languages__iregex=para_buscar) |
                Q(required_education__iregex=para_buscar) |
                Q(keyword__iregex=para_buscar) |
                Q(empresa__iregex=para_buscar)
            ).distinct()
        else:
            todos_c = CourseModel.objects.all()
            todos_m = todos_c.filter(
                Q(title__iregex=busqueda) |
                Q(description__iregex=busqueda) |
                Q(url__iregex=busqueda) |
                Q(category__iregex=busqueda) |
                Q(name__iregex=busqueda) |
                Q(requirements__iregex=busqueda) |
                Q(what_you_will_learn__iregex=busqueda) |
                Q(locale_description__iregex=busqueda) |
                Q(primary_category__iregex=busqueda) |
                Q(primary_subcategory__iregex=busqueda)|
                Q(caption_languages__iregex=busqueda) |
                Q(required_education__iregex=busqueda) |
                Q(keyword__iregex=busqueda) |
                Q(empresa__iregex=busqueda)
                ).distinct()
    
    
    elif inp:
        
        conceptos_a_buscar = []
        expresion = ""

        for i in range(10):

            if i != 0:
                concepto = request.GET.get("mytext["+str(i+1)+"]")
                if concepto != None:
                    conceptos.append(request.GET.get("bool"+str(i)+""))
                    conceptos.append(request.GET.get("not"+str(i)+""))
                    conceptos.append(concepto)
                    
            else:
                conceptos.append(request.GET.get("not"+str(i)+""))
                conceptos.append(request.GET.get("mytext["+str(i+1)+"]"))

            # exoresion regular para negaci??n ^((?!hede).)*$

        #print("conceptos", conceptos)
        print("--- %s seconds en sacar conceptos ---" % (time.time() - start_time))
        if conceptos[0] != None:
            for index, elem in enumerate(conceptos):
                if index%3 == 0:            
                    if elem == "not":
                        conceptos_a_buscar.append("^((?!"+conceptos[index+1]+").)*$")
                        if (index+2) < len(conceptos):
                            conceptos_a_buscar.append(conceptos[index+2])
                        else:
                            continue
                    elif elem == "normal":
                        conceptos_a_buscar.append(conceptos[index+1])
                        if (index+2) < len(conceptos):
                            conceptos_a_buscar.append(conceptos[index+2])
                        else:
                            continue
            print("conceptos a buscar", conceptos_a_buscar)
            conceptos_listos = []
            for index2, elem2 in enumerate(conceptos_a_buscar):
                if elem2 == "or":
                    conceptos_a_buscar[index2] = "|"

            
            else:
                frase_buscada = " "
            
            if len(conceptos_a_buscar) == 1:
                conceptos_listos.append(conceptos_a_buscar[0])
            elif "and" not in conceptos_a_buscar:
                conceptos_listos = copy.deepcopy(conceptos_a_buscar)

            elif len(conceptos_a_buscar) > 1:
                for index2, elem2 in enumerate(conceptos_a_buscar):
                    if index2%2 != 0:
                        if elem2 == "and":
                            if "(?=.*"+conceptos_a_buscar[index2-1]+")" not in conceptos_listos:
                                conceptos_listos.append("(?=.*"+conceptos_a_buscar[index2-1]+")")
                                conceptos_listos.append("(?=.*"+conceptos_a_buscar[index2+1]+")")
                            else:
                                conceptos_listos.append("(?=.*"+conceptos_a_buscar[index2+1]+")")
                        if elem2 == "|":
                            if index2 == 1:
                                conceptos_listos.append(conceptos_a_buscar[index2-1])
                                conceptos_listos.append("|")
                            elif index2+2 == len(conceptos_a_buscar):
                                conceptos_listos.append("|")
                                conceptos_listos.append(conceptos_a_buscar[index2+1])
                            else:
                                conceptos_listos.append("|")
                print("conceptos a buscar", conceptos_a_buscar)
                print("conceptos_listos", conceptos_listos)
                print("--- %s seconds en sacar conceptos a buscar y conceptos listos ---" % (time.time() - start_time))
            frase_a_buscar = ""
            for i in conceptos_listos:
                frase_a_buscar = frase_a_buscar + i 
            #print("frase_a_buscar", frase_a_buscar)

            #todos_c = CourseModel.objects.all()
            todos_m2 = CourseModel.objects.filter(
                Q(title__iregex=frase_a_buscar)                
            ).distinct()
            #print("type todos_m2", type(todos_m2))
            print("--- %s seconds en filtrar ---" % (time.time() - start_time))
            if None in list_to_filter:
                todos_m = todos_m2
                print("--- %s seconds en none ---" % (time.time() - start_time))
            else:
                print("list_to_filter")
                print(list_to_filter)
                if len(list_to_filter) > 0 and list_to_filter[0] == 'None':
                    todos_m = todos_m2
                    print("--- %s seconds en lis_to_filter ---" % (time.time() - start_time))
                else:
                    queryset = CourseModel.objects.filter(id__in=list_to_filter)
                    #print("queryset", queryset)
                    todos_m = todos_m2.union(queryset)
                    print("--- %s seconds en union ---" % (time.time() - start_time))
            """todos_m = todos_c.filter(
                                                                Q(title__iregex=frase_a_buscar) |
                                                                Q(description__iregex=frase_a_buscar) |
                                                                Q(url__iregex=frase_a_buscar) |
                                                                Q(category__iregex=frase_a_buscar) |
                                                                Q(name__iregex=frase_a_buscar) |
                                                                Q(requirements__iregex=frase_a_buscar) |
                                                                Q(what_you_will_learn__iregex=frase_a_buscar) |
                                                                Q(locale_description__iregex=frase_a_buscar) |
                                                                Q(primary_category__iregex=frase_a_buscar) |
                                                                Q(primary_subcategory__iregex=frase_a_buscar)|
                                                                Q(caption_languages__iregex=frase_a_buscar) |
                                                                Q(required_education__iregex=frase_a_buscar) |
                                                                Q(keyword__iregex=frase_a_buscar) |
                                                                Q(empresa__iregex=frase_a_buscar)
                                                            ).distinct()"""

    else:
        frase_buscada = ""
        if array != None:
            todos_m2=CourseModel.objects.all()[:100]
            if None in list_to_filter:
                todos_m=CourseModel.objects.all()[:100]
            elif len(list_to_filter) > 0 and list_to_filter[0] == 'None':
                todos_m=CourseModel.objects.all()[:100]
            else:
                if len(list_to_filter) > 0:                    
                    #print("list_to_filter aqui ", list_to_filter)
                    queryset = CourseModel.objects.filter(id__in=list_to_filter)
                    #print("queryset", queryset)
                    todos_m = queryset
                else:
                    todos_m=CourseModel.objects.all()[:100]
        else:
            todos_m=CourseModel.objects.all()[:100]

        
    print("--- %s seconds en final antes de render ---" % (time.time() - start_time))
    #print("frase_buscada", frase_buscada)
    frase_buscada = ""
    if conceptos:
        for i in conceptos:
            if i == 0:
                frase_buscada = i
            else:
                frase_buscada = frase_buscada +" "+ i
    print("frase_buscada: ", frase_buscada)
    return render(request, 'Cursos/listaCursos.html', {'todos_m': todos_m, 'array':array, 'list_to_filter': list_to_filter, 'buscado': frase_buscada})

    """for i in todos_m:
                        print(i.id_course)"""


    
# Create your views here.

class ActualizarUsuarios(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'Cursos/modU.html'
    success_url = reverse_lazy('cursos:listaU')

class EliminarUsuarios(DeleteView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'Cursos/u_confirm_delete.html'
    success_url = reverse_lazy('cursos:listaU')

class ActualizarCursos(LoginRequiredMixin, UpdateView):
    model = CourseModel
    form_class = CourseForm
    template_name = 'Cursos/modM.html'
    success_url = reverse_lazy('cursos:lista')

    def form_valid(self, form):
        form.instance.user = self.request.user.email
        form.instance.save()
        return super().form_valid(form)

class CrearCursos(CreateView):
    model = CourseModel
    form_class = CourseForm
    template_name = 'Cursos/modCM.html'
    success_url = reverse_lazy('cursos:lista')

class EliminarCursos(DeleteView):
    model = CourseModel
    form_class = CourseForm
    template_name = 'Cursos/cur_confirm_delete.html'
    success_url = reverse_lazy('cursos:lista')

# Create your views here.
@authenticated_user
def IndexView(request):
	return render (request, 'Cursos/index.html')

@authenticated_user
def Index2View(request):
	return render (request, 'Cursos/index2.html')


class InicioPlataforma(View):
    def get(self, request):
        #registroForm = RegistroForm()
        loginForm = LoginForm()
        return render(request, 'Cursos/inicioPlataforma.html', {  'loginForm': loginForm})

class LoginJsonView(View):
    def post(self, request):

        loginForm = LoginForm(request.POST)
        json_stuff = {"success": 0}
        if loginForm.is_valid():
            user = authenticate(username=loginForm.cleaned_data.get(
                'email'), password=loginForm.cleaned_data.get('password'))
        if user:
            login(request, user)
            request.session['usuario'] = None
            json_stuff["success"] = 1
        json_stuff = JsonResponse(json_stuff, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

class AgregarRegistro(View):
    def post(self, request):
        registroForm = RegistroForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.set_password(registroForm.cleaned_data.get('password'))
            usuario.username = usuario.email
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')

@authenticated_user
def CreateUsuarioView(request):
    
    if request.method == 'POST':
        registroForm = CustomUserCreationForm(request.POST) 
        if registroForm.is_valid():
            usuario = registroForm.save()
            usuario.save()
            registroForm.save()
            return(redirect('cursos:index2'))
        else:
        
            return render(request, 'Cursos/cargarUsuario.html', {'registroForm':registroForm})
            #return HttpResponse("""El formulario est?? mal, favor verifica que los datos esten correctos o que la imagen no pese mas de 10MB recarga en <a href = "javascript:history.back()"> Recargar </a>""")
    else:
        registroForm = CustomUserCreationForm()
        return render(request, 'Cursos/cargarUsuario.html', {'registroForm':registroForm})

class AgregarRegistro2(View):
    def post(self, request):
        registroForm = CustomUserCreationForm(request.POST)
        if registroForm.is_valid():
            usuario = registroForm.save()
            #grupo = Group.objects.get(name=registroForm.cleaned_data.get('grupo'))
            # usuario.groups.add(grupo)
            usuario.save()
            json_stuff = JsonResponse({"success": 1}, safe=False)
            return HttpResponse(json_stuff, content_type='application/json')
        else:
            #print("entre en el else de agregarregistro")
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')