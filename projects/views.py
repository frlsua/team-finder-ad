import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, redirect, render

from http import HTTPStatus

from .models import Project, Skill
from .forms import ProjectForm
from .constants import (
    PROJECT_STATUS_OPEN,
    PROJECT_STATUS_CLOSED,
    PROJECTS_PER_PAGE,
    SKILL_AUTOCOMPLETE_LIMIT
)


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'project'
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        queryset = Project.objects.all()
        skill_active = self.request.GET.get('skill')
        if skill_active:
            queryset = queryset.filter(skills__name=skill_active)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_skills'] = Skill.objects.all().order_by('name')
        context['active_skill'] = self.request.GET.get('skill', '')
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'


def get_project_and_check_owner(request, project_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Unauthorized'},
            status=HTTPStatus.UNAUTHORIZED
        )

    project = get_object_or_404(Project, pk=project_id)

    if project.owner != request.user:
        return JsonResponse({'error': 'Forbidden'}, status=HTTPStatus.FORBIDDEN)

    return project


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': False}
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner != request.user:
        return JsonResponse(
            {'error': 'Access denied'},
            status=HTTPStatus.FORBIDDEN
        )

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {'form': form, 'is_edit': True}
    )


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner != request.user or project.status != PROJECT_STATUS_OPEN:
        return JsonResponse(
            {'error': 'Access denied'},
            status=HTTPStatus.FORBIDDEN
        )
    
    project.status = PROJECT_STATUS_CLOSED
    project.save(update_fields=['status'])

    return JsonResponse({
        'is_complete': True,
        'project_status': PROJECT_STATUS_CLOSED
    })


@require_GET
def skill_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(
        name__istartswith=q
    ).order_by('name')[:SKILL_AUTOCOMPLETE_LIMIT]
    data = [
        {'id': skill.id, 'name': skill.name} for skill in skills
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_POST
def add_skill_to_project(request, project_id):
    project = get_project_and_check_owner(request, project_id)
    if isinstance(project, JsonResponse):
        return project

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON'},
            status=HTTPStatus.BAD_REQUEST
        )

    skill_id = data.get('skill_id')
    name = data.get('name')
    created = False
    skill = None

    if skill_id:
        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return JsonResponse(
                {'error': 'Skill not found'},
                status=HTTPStatus.NOT_FOUND
            )
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse(
            {'error': 'Missing skill\'s ID or name'},
            status=HTTPStatus.BAD_REQUEST
        )
    
    added = not project.skills.filter(pk=skill_id).exists()
    if added:
        project.skills.add(skill)
    
    return JsonResponse({
        'skill_id': skill.id,
        'created': created,
        'added': added
    })


@csrf_exempt
@require_POST
def remove_skill_from_project(request, project_id, skill_id):
    project = get_project_and_check_owner(request, project_id)
    if isinstance(project, JsonResponse):
        return project

    skill = get_object_or_404(Skill, id=skill_id)

    if skill not in project.skills.all():
        return JsonResponse({
            'error': 'Project doesn\'t have such a skill'
        }, status=HTTPStatus.NOT_FOUND)
    
    project.skills.remove(skill)
    return JsonResponse({'removed': True})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    participant = not project.participants.filter(pk=request.user.pk).exists()
    if participant:
        project.participants.add(request.user)
    else:
        project.participants.remove(request.user)
    return JsonResponse({"status": "ok", "participant": participant})
