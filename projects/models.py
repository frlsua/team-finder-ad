from django.db import models
from users.models import User
from django.core.validators import RegexValidator

from .constants import (
    SKILL_NAME_MAX_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICE,
    PROJECT_STATUS_MAX_LENGTH
)
from team_finder.settings import AUTH_USER_MODEL


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateTimeField(
        'Дата создания', auto_now_add=True
    )
    github_url = models.URLField(
        null=True, blank=True,
        validators=[RegexValidator(
            regex=r'^https://github.com/[\w\-]+/[\w\-]+/?$',
            message='Ссылка на репозиторий проекта'
        )]
    )
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=PROJECT_STATUS_CHOICE
    )
    participants = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects'
    )
    skills = models.ManyToManyField(
        Skill, blank=True, related_name='projects'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
