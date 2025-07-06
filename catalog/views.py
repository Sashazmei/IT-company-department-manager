from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, redirect


def home_redirect(request):
    return redirect('task_list')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Обрати внимание: обычно url называется 'login' с маленькой буквы
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.all()  # показываем ВСЕ задачи, без фильтрации
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user  # По твоей модели поле называется creator
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.assignee is None:  # Если задача свободна
        task.assignee = request.user  # Назначаем текущего пользователя исполнителем
        task.save()
    return redirect('task_list')


@login_required
def release_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.assignee == request.user:
        task.assignee = None
        task.save()
    return redirect('task_list')
