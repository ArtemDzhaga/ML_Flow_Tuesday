"""
Test package for core application.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Project, Document, DocumentVersion
from django.contrib.auth.models import User

class CoreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description'
        )
        self.document = Document.objects.create(
            title='Test Document',
            content='Test Content',
            project=self.project
        )
        self.version = DocumentVersion.objects.create(
            document=self.document,
            content='Test Version Content'
        )

class CoreAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description'
        )

# This file is intentionally empty to mark the directory as a Python package 