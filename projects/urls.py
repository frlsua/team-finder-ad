from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='project_list'),
    path('skills/', views.skill_autocomplete, name='skill_autocomplete'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/complete/', views.complete_project,
         name='complete_project'),
    path(
        '<int:project_id>/skills/add/',
        views.add_skill_to_project,
        name='add_skill'
    ),
    path(
        '<int:project_id>/skills/<int:skill_id>/remove/',
        views.remove_skill_from_project,
        name='remove_skill'
    ),
    path(
        '<int:project_id>/',
        views.ProjectDetailView.as_view(),
        name='project_detail'
    ),
    path('<int:project_id>/toggle-participate/', views.toggle_participate,
         name='toggle_participate')
]
