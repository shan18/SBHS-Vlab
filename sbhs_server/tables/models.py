from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from undelete.models import TrashableMixin
import random, datetime, os
from sbhs_server.helpers import mailer, simple_encrypt
from django.contrib.auth.models import UserManager
from sbhs_server import settings
#from yaksh.models import Profile
# Create your models here.


class Account(TrashableMixin, AbstractBaseUser):

    name                = models.CharField(max_length=255)
    username            = models.CharField(max_length=127, unique=True)
    email               = models.EmailField(max_length=255, unique=True)
    # password = models.CharField(max_length=255) # Already covered in AbstractBaseUser

    is_active           = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def send_confirmation(self):
        message = """Hi,\n\nPlease visit the link """ + settings.BASE_URL +  """account/confirm/"""
        message = message + self.confirmation_token()
        message = message + """ to confirm your account.\n\n\nRegards,\nVlabs Team"""
        mailer.email(self.email, "Please confirm your account", message)

    def send_password_link(self, token):
        message = """Hi,\n\nPlease visit the link """ + settings.BASE_URL +  """password/edit/"""
        message = message + token
        message = message + """ to change your password.\n\n\nRegards,\nVlabs Team"""
        mailer.email(self.email, "SBHS vlabs password reset link", message)

    def get_profile(self):
        return self.profile


    def confirmation_token(self):
        return simple_encrypt.encrypt(self.email)



class Experiment(TrashableMixin):

    #booking             = models.ForeignKey("Booking")
    user                = models.ForeignKey("Account")

    log                 = models.CharField(max_length=255)
    checksum            = models.CharField(max_length=255, default="NONE")

    created_at          = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at          = models.DateTimeField(auto_now=True, editable=False)
