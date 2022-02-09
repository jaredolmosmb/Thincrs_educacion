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
#import pandas as pd
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