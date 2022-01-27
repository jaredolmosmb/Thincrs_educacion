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

@authenticated_user
def CursosView(request):
    return render (request, 'Cursos/cursos.html')

@authenticated_user
def ListaCursosView(request):
    todos_m=CourseModel.objects.all()
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
    template_name = 'Cursos/man_confirm_delete.html'
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