from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Project
from .constants import (
    FORM_PROJECT_DESCRIPTION_ROWS,
    PROJECT_STATUS_CHOICE,
    PROJECT_STATUS_OPEN
)


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=PROJECT_STATUS_CHOICE,
        widget=forms.Select
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': FORM_PROJECT_DESCRIPTION_ROWS
            }),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название проекта',
            'description': 'Описание',
            'github_url': 'Ссылка на GitHub',
            'status': 'Статус',
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if not url:
            return url

        validator = URLValidator()
        try:
            validator(url)
        except ValidationError:
            raise ValidationError('Введите корректный URL')

        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.netloc not in ('github.com', 'www.github.com'):
            raise ValidationError('Ссылка должна вести на GitHub')
        return url
