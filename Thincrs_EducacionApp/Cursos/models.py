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

"""class Usuario(AbstractUser):
	telefono = models.CharField(max_length=15,default="")
	rol = models.IntegerField(default=0)

	@property
	def usuario_id(self):
		return unicode(self.id)
	def __str__(self):
		return self.email"""