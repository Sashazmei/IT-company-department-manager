from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    RedirectView, ListView, CreateView, FormView
)
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Task
from .forms import TaskForm


# 🔁 Главная страница: редирект на список задач
class HomeRedirectView(RedirectView):
    pattern_name = 'task_list'


# 👤 Регистрация пользователя
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# 📋 Список задач: свои и назначенные
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(creator=user) | Q(assignee=user))


# ➕ Создание задачи
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# ✅ Взять задачу себе
class TakeTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if task.assignee is None:
            task.assignee = request.user
            task.save()
        return HttpResponseRedirect(reverse_lazy('task_list'))


# 🔄 Отказаться от задачи
class ReleaseTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if task.assignee == request.user:
            task.assignee = None
            task.save()
        return HttpResponseRedirect(reverse_lazy('task_list'))
