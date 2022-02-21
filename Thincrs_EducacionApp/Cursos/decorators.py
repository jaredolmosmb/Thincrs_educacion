from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('cursos:inicioPlataforma')
			#return redirect('cursos:lista')
	return wrapper_func
