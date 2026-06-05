from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from .constants import USERS_PER_PAGE
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    ProfileEditForm,
    UserChangePasswordForm
)
from .models import User


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participant'
    queryset = User.objects.all().order_by('id')
    paginate_by = USERS_PER_PAGE


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('project_list')
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return redirect('project_list')
    return render(request, 'users/login.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('users:user_detail', user_id=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = UserChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('users:user_detail', user_id=request.user.id)

    return render(request, 'users/change_password.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('project_list')
