from django.urls import path
from .views import (
    RegisterView,
    TaskListView,
    TaskCreateView,
    TakeTaskView,
    ReleaseTaskView,
)

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),  # Главная страница = список завдань
    path('register/', RegisterView.as_view(), name='register'),
    path('tasks/create/', TaskCreateView.as_view(), name='create_task'),
    path('tasks/take/<int:task_id>/', TakeTaskView.as_view(), name='take_task'),
    path('tasks/release/<int:task_id>/', ReleaseTaskView.as_view(), name='release_task'),
]
