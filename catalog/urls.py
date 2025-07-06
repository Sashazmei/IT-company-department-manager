from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('register/', views.register_view, name='register'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/take/<int:task_id>/', views.take_task, name='take_task'),
    path('tasks/release/<int:task_id>/', views.release_task, name='release_task'),

]