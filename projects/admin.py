from django.contrib import admin

from .models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'status', 'skills_list')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'owner__email',)
    filter_horizontal = ('participants', 'skills')

    @admin.display(description='Skills')
    def skills_list(self, obj):
        return ", ".join(obj.skills.value_list('name', flat=True))


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
