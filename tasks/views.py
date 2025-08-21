from .models import Task
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"/tasks/{self.object.id}/"


class HomeView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ["-created_at"]
    template_name = "tasks/home.html"
    login_url = "/users/login/"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/tasks.html"
    login_url = "/users/login/"

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = "task"
    fields = ["title", "description", "status", "priority", "due_date"]
    template_name = "tasks/update_task.html"
    login_url = "/users/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return f"/tasks/{self.object.id}/"

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = "/"