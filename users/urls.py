from django.urls import path

from . import views


app_name = 'users'


urlpatterns = [
    path('<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('list/', views.UserListView.as_view(), name='users_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
