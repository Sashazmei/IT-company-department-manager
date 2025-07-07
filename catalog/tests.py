from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.task = Task.objects.create(title='Sample Task', creator=self.user)

    def test_login_required_task_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, '/accounts/login/?next=/tasks/')

    def test_authenticated_task_list(self):
        self.client.login(username='tester', password='pass123')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Task')

    def test_create_task_view(self):
        self.client.login(username='tester', password='pass123')
        response = self.client.post(reverse('create_task'), {
            'title': 'New Task',
            'description': 'Some description',
            'deadline': '2025-12-31'
        }, follow=True)
        self.assertEqual(Task.objects.count(), 2)
        self.assertContains(response, 'New Task')

    def test_take_task(self):
        self.client.login(username='tester', password='pass123')
        response = self.client.get(reverse('take_task', args=[self.task.id]), follow=True)
        self.task.refresh_from_db()
        self.assertEqual(self.task.assignee, self.user)

    def test_release_task(self):
        self.task.assignee = self.user
        self.task.save()
        self.client.login(username='tester', password='pass123')
        response = self.client.get(reverse('release_task', args=[self.task.id]), follow=True)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.assignee)
