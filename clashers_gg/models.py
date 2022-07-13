from pyexpat import model
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class User(AbstractBaseUser) :
    email = models.EmailField(
        verbose_name='email address',        #TODO: do we need 'email address' ??
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()

    #'is_active' Designates whether this user account should be considered active.
    # We recommend that you set this flag to False instead of deleting accounts;
    # #that way, if your applications have any foreign keys to users, the foreign keys won’t break.
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # objects = UserManager()   #TODO: create UserManager class

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self) :
        return self.email

    def has_perm(self, perm, obj=None) :
        #Does a user have a specific permission? 
        return True

    def has_module_perms(self, app_label) :
        #Does the user have permissions to view the app `app_label`
        return True

    #TODO: do we need this here?
    # @property
    # def is_staff(self) :
    #     #Is the user a member of staff?
    #     return self.is_admin
