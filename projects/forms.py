from django import forms

from .models import Project
from .constants import PROJECT_STATUS_CHOICE
from team_finder.validators import validate_url


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=PROJECT_STATUS_CHOICE,
        widget=forms.Select
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if not url:
            return url

        validate_url(url)
        return url
