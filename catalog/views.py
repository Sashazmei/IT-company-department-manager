from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, FormView

from .models import Task
from .forms import TaskForm


class HomeRedirectView(View):
    def get(self, request):
        return redirect('task_list')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.assignee is None:
        task.assignee = request.user
        task.save()
    return redirect('task_list')


@login_required
def release_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.assignee == request.user:
        task.assignee = None
        task.save()
    return redirect('task_list')
