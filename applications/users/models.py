from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from applications.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'customer'),
        ('executor', 'executor'),
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=55, choices=ROLE_CHOICES)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email