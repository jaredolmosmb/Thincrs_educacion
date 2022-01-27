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
	last_update_date=models.DateTimeField(auto_now=True)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title

class WhatYouWillLearnModel(models.Model):
	creado_en=models.DateTimeField(auto_now_add=True)
	actualzado_en=models.DateTimeField(auto_now=True)
	id_what_you_will_learn = models.IntegerField()
	what_you_will_learn = models.CharField(max_length=200)
	#cliente=models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.what_you_will_learn

class CourseHasWhatYouWillLearn(models.Model):
	course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
	what_you_will_learn = models.ForeignKey(WhatYouWillLearnModel, on_delete=models.CASCADE)


"""class Usuario(AbstractUser):
	telefono = models.CharField(max_length=15,default="")
	rol = models.IntegerField(default=0)

	@property
	def usuario_id(self):
		return unicode(self.id)
	def __str__(self):
		return self.email"""