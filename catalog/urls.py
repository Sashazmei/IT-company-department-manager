from django.urls import path
from .views import (
    HomeRedirectView,
    RegisterView,
    TaskListView,
    TaskCreateView,
    TakeTaskView,
    ReleaseTaskView,
)

urlpatterns = [
    path('', HomeRedirectView.as_view(), name='home_redirect'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='create_task'),
    path('tasks/take/<int:task_id>/', TakeTaskView.as_view(), name='take_task'),
    path('tasks/release/<int:task_id>/', ReleaseTaskView.as_view(), name='release_task'),
]
