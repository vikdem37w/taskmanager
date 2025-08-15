from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required

@login_required(login_url="/users/login/")
def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/tasks.html', {"tasks": tasks})

@login_required(login_url="/users/login/")
def create_task(request):
    return render(request, 'tasks/create_task.html')
