from django import forms
#from operadores.models import Operadores, ImageId, ImageDomicilio
#from .models import OperadoresModel, TiposDocOperadoresModel, DocumentosModel
#from .models import Usuario
from django.contrib.auth.models import Group
from django.db.models import Q
import datetime
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        
"""sclass CourseForm(forms.ModelForm):
	class Meta:
		model=CourseModel
		fields = (
        'id_course',
        'title',
        'description',
        'url',
        'estimated_content_length',
        'has_closed_caption',
        #'last_update_date'
        )
		widgets = {
			'id_course': forms.TextInput(attrs={'class': 'form-control'}),
			'title': forms.Textarea(attrs={'class': 'form-control' , 'rows' : '4'}),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
	        'url': forms.TextInput(attrs={'class': 'form-control'}),
	        'estimated_content_length':forms.TextInput(attrs={'class': 'form-control'}),
	        'has_closed_caption':forms.TextInput(attrs={'class': 'form-control'}),
	        #'last_update_date':forms.TextInput(attrs={'class': 'form-control'}),
			}"""

class CourseForm(forms.ModelForm):
	class Meta:
		model=CourseModel
		fields = (
        'id_course',
        'title',
        'description',
        'url',
        'estimated_content_length',
        'category',
        'num_lectures',
        'num_videos',
        'name',
        'requirements',
        'what_you_will_learn',
        'locale_description',
        'is_practice_test_course',
        'has_closed_caption',
        'primary_category',
        'primary_subcategory',
        'num_quizzes',
        'num_practice_tests',
        'has_closed_caption',
        'caption_languages',
        'estimated_content_length_video',
        #'required_education',
		#'keyword',
		#'empresa'
        #'last_update_date'
        )
		widgets = {
			'id_course': forms.TextInput(attrs={'class': 'form-control'}),
			'title': forms.Textarea(attrs={'class': 'form-control' , 'rows' : '4'}),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
	        'url': forms.TextInput(attrs={'class': 'form-control'}),
	        'estimated_content_length':forms.TextInput(attrs={'class': 'form-control'}),
	        'category':forms.TextInput(attrs={'class': 'form-control'}),
	        'num_lectures':forms.TextInput(attrs={'class': 'form-control'}),
	        'num_videos':forms.TextInput(attrs={'class': 'form-control'}),
			'name':forms.TextInput(attrs={'class': 'form-control'}),
			'requirements':forms.TextInput(attrs={'class': 'form-control'}),
			'what_you_will_learn':forms.TextInput(attrs={'class': 'form-control'}),
			'locale_description':forms.TextInput(attrs={'class': 'form-control'}),
			'is_practice_test_course':forms.TextInput(attrs={'class': 'form-control'}),	
			'has_closed_caption':forms.TextInput(attrs={'class': 'form-control'}),	
	        'primary_category':forms.TextInput(attrs={'class': 'form-control'}),
	        'primary_subcategory':forms.TextInput(attrs={'class': 'form-control'}),
	        'num_quizzes':forms.TextInput(attrs={'class': 'form-control'}),
	        'num_practice_tests':forms.TextInput(attrs={'class': 'form-control'}),
	        'has_closed_caption':forms.TextInput(attrs={'class': 'form-control'}),
			'caption_languages':forms.TextInput(attrs={'class': 'form-control'}),
			'estimated_content_length_video':forms.TextInput(attrs={'class': 'form-control'}),			
			#'required_education':forms.TextInput(attrs={'class': 'form-control'}),
			#'keyword':forms.TextInput(attrs={'class': 'form-control'}),
			#'empresa':forms.TextInput(attrs={'class': 'form-control'}),
	        #'last_update_date':forms.TextInput(attrs={'class': 'form-control'}),
			}

"""class RegistroForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input90', 'placeholder':'Password', 'id':'password2'}))
	class Meta:
		model = Usuario
		fields = ['first_name','last_name','email', 'telefono', 'password','groups']#'__all__','celular', 'empresa', 'num_empleados'
		groups = forms.ModelMultipleChoiceField(queryset=Group.objects.filter(~Q(name = "admin")))
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'input90', 'placeholder':'Nombre', 'id':'nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'input90', 'placeholder':'Apellidos', 'id':'apellidos'}),
			'email': forms.TextInput(attrs={'class':'input90', 'placeholder':'Email/Usuario', 'id':'email2'}),
			'telefono': forms.TextInput(attrs={'class':'input90', 'placeholder':'Celular', 'id':'telefono'}),

			#'groups': forms.ModelMultipleChoiceField(queryset=Group.objects.filter(~Q(name = "admin")))
			'groups' : forms.CheckboxSelectMultiple()
			#'groups' : forms.SelectMultiple()
			}

	def __init__(self, *args, **kwargs):
		super(RegistroForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = ''
		self.fields['last_name'].label = ''
		self.fields['email'].label = ''
		self.fields['telefono'].label = ''
		self.fields['password'].label = ''
		self.fields['groups'].label = 'Tipo'
		self.fields['groups'].queryset = Group.objects.filter(~Q(name = "admin") & ~Q(name = "general"))
		self.fields['groups'].help_text = ''
"""
class LoginForm(forms.Form):
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuario', 'id':'email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'id':'password'}))

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = ''
		self.fields['password'].label = ''
"""
class Registro2Form(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input90', 'id':'password2'}))
	class Meta:
		model = Usuario
		fields = ['first_name','last_name','email', 'telefono', 'password']#
		fields = '__all__'
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'input90', 'id':'nombre'}),
			'last_name': forms.TextInput(attrs={'class': 'input90', 'id':'apellidos'}),
			'email': forms.TextInput(attrs={'class':'input90', 'id':'email2'}),
			'telefono': forms.TextInput(attrs={'class':'input90', 'id':'telefono'}),
			}

	def __init__(self, *args, **kwargs):
		super(Registro2Form, self).__init__(*args, **kwargs)
		self.fields['first_name'].label = 'Nombre'
		self.fields['last_name'].label = 'Apellidos'
		self.fields['email'].label = 'Email/Usuario'
		self.fields['telefono'].label = 'Telefono'
		self.fields['password'].label = 'Password'
		"""