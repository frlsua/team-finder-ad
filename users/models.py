from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import RegexValidator

from .constants import (
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
    AVATAR_PATH
)
from .tools import generate_avatar


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField(
        upload_to=AVATAR_PATH,
        blank=True
    )
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^\+7\d{10}$',
            message='Номер телефона должен быть в формате: "+7XXXXXXXXXX"'
        )],
        unique=True,
        blank=True,
        null=True
    )
    github_url = models.URLField(
        validators=[RegexValidator(
            regex=r'^https://github.com/[\w\-]+/?$',
            message='Ссылка на профиль GitHub'
        )], blank=True, null=True
    )
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH, blank=True, null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    objects = MyUserManager()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            first_letter = self.name[0]
            self.avatar = self.generate_user_avatar(first_letter)
        super().save(*args, **kwargs)

    def generate_user_avatar(self, first_letter):
        return generate_avatar(first_letter)
