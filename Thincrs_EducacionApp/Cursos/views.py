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
import re

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
    response = requests.get(url, auth=(CLIENT_ID, SECRET_ID))
    data = response.json() # ya esta parseado
    courses = pd.DataFrame(columns=[
        'id', 
        'title', 
        'description', 
        'url', 
        'estimated_content_length', 
        'categories', 
        'instructors', 
        'requirements', 
        'what_you_will_learn', 
        'locale', 
        'primary_category', 
        'has_closed_caption', 
        'caption_languages', 
        'last_update_date'
    ])
    try:
      for course in data['results']:
        if 'es' in course['locale']['locale'] or 'en' in course['locale']['locale']:
          courses = courses.append({
                    'id': course['id'],
                    'title': course['title'], 
                    'description': cleanhtml(course['description']), 
                    'url': course['url'], 
                    'estimated_content_length': course['estimated_content_length'], 
                    #'categories': course['categories'], 
                    'categories': ' '.join([str(item) for item in course['categories']]),
                    #'instructors': course['instructors'],
                    'instructors': ' \n-'.join([str(item) for item in course['instructors']]), 
                    #'requirements': course['requirements']['list'], 
                    'requirements': ' \n-'.join([str(item) for item in course['requirements']['list']]), 
                    #'what_you_will_learn': course['what_you_will_learn']['list'], 
                    'what_you_will_learn': ' \n-'.join([str(item) for item in course['what_you_will_learn']['list']]),
                    'locale': course['locale']['locale'],
                    'primary_category': course['primary_category']['title'],
                    'has_closed_caption': course['has_closed_caption'], 
                    #'caption_languages': course['caption_languages'], 
                    'caption_languages': ' \n-'.join([str(item) for item in course['caption_languages']]), 
                    'last_update_date': course['last_update_date']
                }, ignore_index=True)
    except:
      pass
    print(len(courses))


    return render (request, 'Cursos/prueba.html')

@authenticated_user
def CursosView(request):
    return render (request, 'Cursos/cursos.html')

#@authenticated_user
def ListaCursosView(request):
    todos_m=CourseModel.objects.all()

    for i in todos_m:
        print(i.id_course)


    return render(request, 'Cursos/listaCursos.html', {'todos_m': todos_m})
# Create your views here.

class ActualizarCursos(UpdateView):
    model = CourseModel
    form_class = CourseForm
    template_name = 'Cursos/modM.html'
    success_url = reverse_lazy('cursos:lista')

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
            print("entre en el else de agregarregistro")
            json_stuff = JsonResponse({"success": 0}, safe=False)
        return HttpResponse(json_stuff, content_type='application/json')