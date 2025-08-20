from .models import Task
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ["-created_at"]
    template_name = "tasks/tasks.html"
    login_url = "/users/login/"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    context_object_name = "task"
    fields = ["title", "description", "status", "priority", "due_date"]
    template_name = "tasks/create_task.html"
    login_url = "/users/login/"


class HomeView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ["-created_at"]
    template_name = "tasks/home.html"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/tasks.html"
    login_url = "/users/login/"

    def get_object(self, queryset=None):
        task_id = self.kwargs.get("id")
        return Task.objects.get(id=task_id)
