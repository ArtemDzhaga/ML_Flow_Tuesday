from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.factories import (
    UserFactory, TopicFactory, ProjectFactory, ProjectSettingsFactory,
    TaskFactory, TaskDetailFactory, SubtaskFactory, CommentFactory,
    DocumentFactory, DocumentVersionFactory, TemplateFactory
)
import random

class Command(BaseCommand):
    help = 'Генерирует тестовые данные для системы документооборота'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем генерацию тестовых данных...')

        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Создан суперпользователь admin/admin123')

        # Создаем обычных пользователей
        users = UserFactory.create_batch(5)
        self.stdout.write(f'Создано {len(users)} пользователей')

        # Создаем темы
        topics = TopicFactory.create_batch(3)
        self.stdout.write(f'Создано {len(topics)} тем')

        # Создаем шаблоны для каждой темы
        templates = []
        for topic in topics:
            topic_templates = TemplateFactory.create_batch(2, topic=topic)
            templates.extend(topic_templates)
        self.stdout.write(f'Создано {len(templates)} шаблонов')

        # Создаем проекты для каждой темы
        projects = []
        for topic in topics:
            topic_projects = ProjectFactory.create_batch(3, topic=topic)
            projects.extend(topic_projects)
        self.stdout.write(f'Создано {len(projects)} проектов')

        # Создаем настройки для каждого проекта
        for project in projects:
            ProjectSettingsFactory.create(
                project=project,
                template_default=random.choice(templates)
            )
        self.stdout.write('Созданы настройки проектов')

        # Создаем задачи для каждого проекта
        tasks = []
        for project in projects:
            project_tasks = TaskFactory.create_batch(
                random.randint(3, 7),
                project=project,
                assigned_to=random.choice(users)
            )
            tasks.extend(project_tasks)
        self.stdout.write(f'Создано {len(tasks)} задач')

        # Создаем детали для каждой задачи
        for task in tasks:
            TaskDetailFactory.create(task=task)
        self.stdout.write('Созданы детали задач')

        # Создаем подзадачи для каждой задачи
        subtasks = []
        for task in tasks:
            task_subtasks = SubtaskFactory.create_batch(
                random.randint(1, 4),
                task=task
            )
            subtasks.extend(task_subtasks)
        self.stdout.write(f'Создано {len(subtasks)} подзадач')

        # Создаем комментарии для задач и подзадач
        for task in tasks:
            CommentFactory.create_batch(
                random.randint(2, 5),
                task=task,
                author=random.choice(users)
            )
        for subtask in subtasks:
            CommentFactory.create_batch(
                random.randint(1, 3),
                subtask=subtask,
                author=random.choice(users)
            )
        self.stdout.write('Созданы комментарии')

        # Создаем документы для каждого проекта
        documents = []
        for project in projects:
            project_docs = DocumentFactory.create_batch(
                random.randint(2, 5),
                project=project
            )
            documents.extend(project_docs)
        self.stdout.write(f'Создано {len(documents)} документов')

        # Создаем версии для каждого документа
        for doc in documents:
            DocumentVersionFactory.create_batch(
                random.randint(1, 5),
                document=doc,
                created_by=random.choice(users)
            )
        self.stdout.write('Созданы версии документов')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!')) 