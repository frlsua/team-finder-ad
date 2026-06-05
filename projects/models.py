from django.db import models
from django.core.validators import RegexValidator

from .constants import (
    SKILL_NAME_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICE,
    PROJECT_STATUS_OPEN,
    PROJECT_STATUS_MAX_LENGTH
)
from team_finder.settings import AUTH_USER_MODEL


class Skill(models.Model):
    name = models.CharField(
        max_length=SKILL_NAME_MAX_LENGTH,
        verbose_name='Наименование'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=PROJECT_NAME_MAX_LENGTH,
        verbose_name='Наименование'
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True
    )
    github_url = models.URLField(
        null=True, blank=True,
        validators=[RegexValidator(
            regex=r'^https://github.com/[\w\-]+/[\w\-]+/?$'
        )],
        verbose_name='Ссылка на репозиторий проекта'
    )
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=PROJECT_STATUS_CHOICE,
        default=PROJECT_STATUS_OPEN,
        verbose_name='Статус'
    )
    participants = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )
    skills = models.ManyToManyField(
        Skill, blank=True, related_name='projects',
        verbose_name='Навыки'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
