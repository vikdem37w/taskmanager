from django.shortcuts import render
from .models import Task

# Create your views here.
def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/tasks.html', {"tasks": tasks})