from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from .constants import USERS_PER_PAGE
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ProfileEditForm
)
from .models import User


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participant'
    queryset = User.objects.all()
    paginate_by = USERS_PER_PAGE


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'users/register.html', {'form': form})
    user = form.save()
    login(request, user)
    return redirect('project_list')


def login_user(request):
    form = UserLoginForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'users/login.html', {'form': form})
    login(request, form.user)
    return redirect('project_list')


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if not form.is_valid():
        return render(request, 'users/edit_profile.html', {'form': form})
    form.save()
    return redirect('users:user_detail', user_id=request.user.id)


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if not form.is_valid():
        return render(request, 'users/change_password.html', {'form': form})
    user = form.save()
    update_session_auth_hash(request, user)
    return redirect('users:user_detail', user_id=request.user.id)


@login_required
def logout_user(request):
    logout(request)
    return redirect('project_list')
