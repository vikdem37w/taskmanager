from django.shortcuts import render
from .models import Task

def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/tasks.html', {"tasks": tasks})

def login(request):
    return render(request, 'tasks/login.html')