import logging
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Task
from .forms import TaskForm

logger = logging.getLogger(__name__)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    context_object_name = "task"
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    login_url = "/users/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info(f"{self.request.user} created task '{form.instance.title}' successfully")
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
    template_name = "tasks/task_detail.html"
    login_url = "/users/login/"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = "task"
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    login_url = "/users/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info(f"{self.request.user} updated task '{form.instance.title}' successfully")
        return super().form_valid(form)

    def get_success_url(self):
        return f"/tasks/{self.object.id}/"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    login_url = "/users/login/"

    def get_success_url(self):
        logger.info(f"{self.request.user} deleted task '{self.object.title}' successfully")
        return "/"
