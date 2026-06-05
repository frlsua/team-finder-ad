import re
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label='Пароль'
    )
    phone = forms.CharField(required=True, label='Номер телефона')

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'phone', 'password']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'Почта'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Почта')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Пароль'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(request=None, email=email, password=password)
            if not user:
                raise forms.ValidationError('Неверный пароль или почта')
            self.user = user
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(
        label="Фотография",
        required=False,
        widget=forms.FileInput(
            attrs={
                "accept": "image/png,image/jpeg,image/webp",
                "class": "visually-hidden",
            }
        ),
    )
    phone = forms.CharField(required=False, label='Номер телефона')

    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'phone': 'Номер телефона',
            'about': 'О себе',
            'github_url': 'Ссылка на GitHub',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar and self.instance and self.instance.avatar:
            return self.instance.avatar
        return avatar

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return None

        digits = re.sub(r'\D', '', phone)

        if not re.fullmatch(r"(8|\+7)\d{10}", phone):
            raise forms.ValidationError(
                'Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
            )

        if digits.startswith('8') or digits.startswith('7'):
            digits = '+7' + digits[1:]

        if self.instance and self.instance.pk:
            existing = User.objects.exclude(pk=self.instance.pk).filter(
                phone=digits).first()
        else:
            existing = User.objects.filter(phone=digits).first()

        if existing:
            raise ValidationError(
                'Номер телефона уже используется другим пользователем'
                )

        return digits

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            validator = URLValidator()
            try:
                validator(url)
            except ValidationError:
                raise ValidationError('Введите корректную ссылку')

            if 'github.com' not in url.lower():
                raise ValidationError('Ссылка должна вести на GitHub')
        return url


class UserChangePasswordForm(PasswordChangeForm):
    pass
