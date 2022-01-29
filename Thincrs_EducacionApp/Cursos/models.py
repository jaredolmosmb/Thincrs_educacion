from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser, PermissionsMixin, UserManager, BaseUserManager
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid, random
from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy  as _

from .managers import CustomUserManager



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CourseModel(models.Model):
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
		return self.title

class Course2Model(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	id_course = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
	#id_course=models.IntegerField()
	title=models.CharField(max_length=200)
	description=models.CharField(max_length=200)
	url=models.CharField(max_length=500)
	estimated_content_length=models.IntegerField()
	has_closed_caption=models.BooleanField()
	what_you_will_learn=models.CharField(max_length=2000)
	language = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	requirements = models.CharField(max_length=200)
	locale_description = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	primary_category=models.CharField(max_length=200)
	required_education=models.CharField(max_length=200)
	#last_update_date=models.DateTimeField(auto_now=True)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title

class WhatYouWillLearnModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	what_you_will_learn = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.what_you_will_learn

class CourseHasWhatYouWillLearn(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	what_you_will_learn = models.ForeignKey(WhatYouWillLearnModel, on_delete=models.CASCADE)

class CaptionLanguagesModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	language = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.language

class CourseHasCaptionLanguage(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	language = models.ForeignKey(CaptionLanguagesModel, on_delete=models.CASCADE)

class InstructorsModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	name = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

class CourseHasInstructor(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	name = models.ForeignKey(InstructorsModel, on_delete=models.CASCADE)

class RequirementsModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	requirements = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.requirements

class CourseHasRequirement(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	requirements = models.ForeignKey(RequirementsModel, on_delete=models.CASCADE)

class LocalesModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	locale_description = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.locale_description

class CourseHasLocales(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	locale_description = models.ForeignKey(LocalesModel, on_delete=models.CASCADE)

class CategoriesModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	category = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.category

class CourseHasCategories(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)

class PrimaryCategoriesModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	primary_category = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.primary_category

class CourseHasPrimaryCategories(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	primary_category = models.ForeignKey(PrimaryCategoriesModel, on_delete=models.CASCADE)

class RequiredEducationModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	#id_what_you_will_learn = models.IntegerField()
	required_education = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.required_education

class CourseHasRequiredEducation(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	required_education = models.ForeignKey(RequiredEducationModel, on_delete=models.CASCADE)

"""class Usuario(AbstractUser):
	telefono = models.CharField(max_length=15,default="")
	rol = models.IntegerField(default=0)

	@property
	def usuario_id(self):
		return unicode(self.id)
	def __str__(self):
		return self.email"""