from django.db import models
from undelete.models import TrashableMixin
from sbhs_server.helpers import mailer
from sbhs_server.helpers import simple_encrypt
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from sbhs_server import settings
from sbhs_formula.formula import Formula

import random


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email='hello@gola.com',
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(TrashableMixin, AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=127, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    # password = models.CharField(max_length=255) # Already covered in AbstractBaseUser

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Model version assigned to a user
    coeff_ID = models.IntegerField(default=random.randint(1, Formula.count_coeff()))

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def send_confirmation(self):
        message = """Hi,\n\nPlease visit the link """ + settings.BASE_URL + """account/confirm/"""
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

    def __unicode__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Experiment(TrashableMixin):

    user = models.ForeignKey("Account")

    log = models.CharField(max_length=255)
    checksum = models.CharField(max_length=255, default="NONE")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.log
