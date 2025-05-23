from factory import Faker, SubFactory, LazyAttribute
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from .models import (
    Topic, Project, ProjectSettings, Task, TaskDetail, Subtask,
    Comment, Document, DocumentVersion, Template
)
import random

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs['password'] = 'password123'
        return super()._create(model_class, *args, **kwargs)

class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = Faker('sentence', nb_words=3)
    description = Faker('paragraph')

class TemplateFactory(DjangoModelFactory):
    class Meta:
        model = Template

    name = Faker('sentence', nb_words=2)
    content = Faker('paragraph')
    topic = SubFactory(TopicFactory)

class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    topic = SubFactory(TopicFactory)

class ProjectSettingsFactory(DjangoModelFactory):
    class Meta:
        model = ProjectSettings

    project = SubFactory(ProjectFactory)
    notification_enabled = Faker('boolean')
    template_default = SubFactory(TemplateFactory)

class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = Faker('sentence', nb_words=5)
    description = Faker('paragraph')
    project = SubFactory(ProjectFactory)
    status = LazyAttribute(lambda _: random.choice(['new', 'in_progress', 'review', 'done']))
    assigned_to = SubFactory(UserFactory)

class TaskDetailFactory(DjangoModelFactory):
    class Meta:
        model = TaskDetail

    task = SubFactory(TaskFactory)
    requirements = Faker('paragraph')
    acceptance_criteria = Faker('paragraph')

class SubtaskFactory(DjangoModelFactory):
    class Meta:
        model = Subtask

    title = Faker('sentence', nb_words=4)
    description = Faker('paragraph')
    task = SubFactory(TaskFactory)
    status = LazyAttribute(lambda _: random.choice(['new', 'in_progress', 'review', 'done']))

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = Faker('paragraph')
    task = SubFactory(TaskFactory)
    author = SubFactory(UserFactory)

class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    title = Faker('sentence', nb_words=4)
    content = Faker('paragraph')
    project = SubFactory(ProjectFactory)

class DocumentVersionFactory(DjangoModelFactory):
    class Meta:
        model = DocumentVersion

    document = SubFactory(DocumentFactory)
    content = Faker('paragraph')
    version_number = LazyAttribute(lambda _: random.randint(1, 10))
    created_by = SubFactory(UserFactory) 