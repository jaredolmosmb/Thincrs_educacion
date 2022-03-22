from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, PermissionsMixin, UserManager, BaseUserManager
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid, random
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy  as _

from .managers import CustomUserManager


class CourseRetireModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True, null=True, blank=True)
	actualizado_en=models.DateTimeField(auto_now=True, null=True, blank=True)
	id_course = models.IntegerField(unique = True)
	scheduled_removal_date = models.DateTimeField()
	language = models.CharField(max_length=2000)
	title=models.CharField(max_length=2000,null=True, blank=True)
	course_category = models.CharField(max_length=2000)
	course_subcategory = models.CharField(max_length=2000)
	alternative_course_1 = models.IntegerField()
	title_alternative_course_1 = models.CharField(max_length=2000)
	alternative_course_2 = models.IntegerField()
	title_alternative_course_2 = models.CharField(max_length=2000)

	def __str__(self):
		return self.title

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

"""class CourseModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	id_course=models.IntegerField()
	title=models.CharField(max_length=200)
	description=models.CharField(max_length=200)
	url=models.CharField(max_length=500)
	estimated_content_length=models.IntegerField()
	has_closed_caption=models.BooleanField()
	#last_update_date=models.DateTimeField(auto_now=True)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title"""

class CourseModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True, null=True, blank=True)
	actualizado_en=models.DateTimeField(auto_now=True, null=True, blank=True)
	id_course = models.IntegerField(unique = True)
	title=models.CharField(max_length=2000,null=True, blank=True)
	description=models.CharField(max_length=4000,null=True, blank=True)
	url=models.CharField(max_length=500,null=True, blank=True)
	estimated_content_length=models.IntegerField(null=True, blank=True)
	category = models.CharField(max_length=2000, default = '',null=True, blank=True)
	num_lectures=models.IntegerField(null=True, blank=True)
	num_videos=models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=2000,null=True, blank=True)
	requirements = models.CharField(max_length=4000,null=True, blank=True)
	what_you_will_learn=models.CharField(max_length=4000,null=True, blank=True)	
	locale_description = models.CharField(max_length=2000,null=True, blank=True)
	is_practice_test_course = models.CharField(max_length=2000,null=True, blank=True)
	primary_category=models.CharField(max_length=2000,null=True, blank=True)
	primary_subcategory=models.CharField(max_length=2000,null=True, blank=True)
	num_quizzes = models.IntegerField(null=True, blank=True)
	num_practice_tests = models.IntegerField(null=True, blank=True)
	has_closed_caption=models.CharField(max_length=2000,null=True, blank=True)
	caption_languages = models.CharField(max_length=2000, null=True, blank=True)
	estimated_content_length_video = models.IntegerField(null=True, blank=True)
	required_education=models.CharField(max_length=2000, null=True, blank=True)
	keyword= models.CharField(max_length=2000, null=True, blank=True)
	empresa = models.CharField(max_length=200, null=True, blank=True)
	user=models.CharField(max_length=200, null=True, blank=True)
	#last_update_date=models.DateTimeField(auto_now=True)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title


"""class Usuario(AbstractUser):
	telefono = models.CharField(max_length=15,default="")
	rol = models.IntegerField(default=0)

	@property
	def usuario_id(self):
		return unicode(self.id)
	def __str__(self):
		return self.email"""