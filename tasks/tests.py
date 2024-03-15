from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskManagementTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "osama",
            "password": "swati12345",
            "email": "osama@email.com",
        }
        self.task_data = {
            "title": "Test Task",
            "description": "This is a test task.",
            "due_date": "2024-03-15",
            "priority": "High",
        }

    def test_task_creation(self):
        self.client.login(**self.user_data)
        response = self.client.post(reverse("task_create"), data=self.task_data)
        self.assertEqual(
            response.status_code, 302
        )

    def test_task_update(self):
        # user = User.objects.create_user(**self.user_data)
        task = Task.objects.create(**self.task_data)
        self.client.login(**self.user_data)
        updated_data = {
            "title": "Updated Test Task",
            "description": "This is an updated test task.",
            "due_date": "2024-03-20",
            "priority": "Medium",
        }
        response = self.client.post(
            reverse("task_update", kwargs={"pk": task.pk}), data=updated_data
        )
        self.assertEqual(
            response.status_code, 302
        )
