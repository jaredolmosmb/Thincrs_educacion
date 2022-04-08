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
import pandas
import json
from datetime import date
import math
import copy
import time
import re
import csv
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
ACCOUNT_NAME= 'thincrs-one'
CLIENT_ID= 'cFLdzohBmNbxdjAiqCZlq2h1TBjEUw0foqYaFicf'
SECRET_ID= 'OkcFvpaNuAiao8FoC2S3UjJrj1gbJhU6ZFw3h2DPo4vIHy1g8uqOos1OyUApQgW1sFhpHXXskrk695zqcQ1NZ6fXoNrbj8PLqkspc9210mZcttMP53btfdB7phMTeXpN'
ACCOUNT_ID= '79612'

url = f'https://{ACCOUNT_NAME}.udemy.com/api-2.0/organizations/{ACCOUNT_ID}/courses/list/?page_size=12'

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
            
            file2 = pandas.read_excel(archivo2, 'To Be Retired')
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

        # exoresion regular para negación ^((?!hede).)*$

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

            # exoresion regular para negación ^((?!hede).)*$

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
            #return HttpResponse("""El formulario está mal, favor verifica que los datos esten correctos o que la imagen no pese mas de 10MB recarga en <a href = "javascript:history.back()"> Recargar </a>""")
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