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


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле с почтой должно быть заполнено")
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
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=USER_SURNAME_MAX_LENGTH,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to=AVATAR_PATH,
        blank=True,
        verbose_name='Фотография'
    )
    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^\+7\d{10}$',
            message='Номер телефона должен быть в формате: "+7XXXXXXXXXX"'
        )],
        unique=True,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    github_url = models.URLField(
        validators=[RegexValidator(
            regex=r'^https://github.com/[\w\-]+/?$'
        )], blank=True, null=True,
        verbose_name='Ссылка на профиль GitHub'
    )
    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH, blank=True, null=True,
        verbose_name='О себе'
    )

    is_active = models.BooleanField(
        default=True, verbose_name='В сети'
    )
    is_staff = models.BooleanField(
        default=False, verbose_name='Модератор'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    objects = UserManager()

    class Meta:
        ordering = ['email', 'surname', 'name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            first_letter = self.name[0]
            self.avatar = generate_avatar(first_letter)
        super().save(*args, **kwargs)
