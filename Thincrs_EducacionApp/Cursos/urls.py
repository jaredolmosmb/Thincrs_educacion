from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'cursos'

urlpatterns = [
	path('index/', views.IndexView, name =  "index"),
	path('prueba/', views.PruebaView, name =  "prueba"),
	path('', views.Index2View, name =  "index2"),
	path('inicioPlataforma', views.InicioPlataforma.as_view(), name='inicioPlataforma'),
	path('loginJson/', views.LoginJsonView.as_view(), name='loginjson'),
	path('agregarRegistro/', views.AgregarRegistro.as_view(), name='agregarRegistro'),
	path('logout/', auth_views.LogoutView.as_view() , name='logout'),
	path('agregarRegistro2/', views.AgregarRegistro2.as_view(), name='agregarRegistro2'),
	path('cargar_usuario/', views.CreateUsuarioView, name='cargar_usuario'),
	path('cursos', views.CursosView, name =  "cursos"),
	path('lista', views.ListaCursosView, name='lista'),
	path('listaU', views.ListaUsuariosView, name='listaU'),
	path('actualizar/<int:pk>/', views.ActualizarCursos.as_view(), name='actualizar'),
	path('crear/', views.CrearCursos.as_view(), name='crear'),
	path('eliminar/<int:pk>/', views.EliminarCursos.as_view(), name='eliminar'),
	path('actualizarU/<int:pk>/', views.ActualizarUsuarios.as_view(), name='actualizarU'),
	path('eliminarU/<int:pk>/', views.EliminarUsuarios.as_view(), name='eliminarU'),
	path('actualizacion/', views.UpdateProcessView, name='actualizacion'),
	
	

	]