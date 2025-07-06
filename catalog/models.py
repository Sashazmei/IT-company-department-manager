from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(default=timezone.now)
    is_completed = models.BooleanField(default=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True,      # Позволяет быть пустым в базе (задача не назначена)
        blank=True      # Позволяет оставлять поле пустым в формах
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
