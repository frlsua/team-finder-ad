from django.core.management.base import BaseCommand

from users.models import User
from projects.models import Project, Skill


class Command(BaseCommand):
    help = 'Заполняет базу данных демонстрационными данными'

    def handle(self, *args, **options):
        email = 'maria@yandex.ru'
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': 'Мария',
                'surname': 'Демо',
                'phone': '+71234567890',
                'is_active': True,
                'is_staff': False,
            }
        )
        if created:
            user.set_password('password')
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Создан пользователь: {email}\nПароль: password'))
        else:
            self.stdout.write(f'Пользователь {email} уже существует')

        self.create_project(user)

    def create_project(self, user):
        skills_data = ['Python', 'Django', 'PostgreSQL', 'Docker', 'JavaScript']
        for skill_name in skills_data:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                self.stdout.write(f'Создан навык: {skill_name}')

        project_title = 'Пример проекта TeamFinder'
        project, created = Project.objects.get_or_create(
            name=project_title,
            owner=user,
            defaults={
                'description': 'Этот проект создан для демонстрации',
                'github_url': 'https://github.com/maria/demo',
                'status': 'open',
            }
        )
        if created:
            project.participants.add(user)
            for skill in Skill.objects.all()[:2]:
                project.skills.add(skill)
            self.stdout.write(
                self.style.SUCCESS(f'Создан проект: {project_title}')
            )
        else:
            self.stdout.write(f'Проект "{project_title}" уже существует')

        self.stdout.write(self.style.SUCCESS('Готово!'))
