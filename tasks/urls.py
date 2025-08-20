from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("tasks/", views.TaskListView.as_view(), name="tasks"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="create_task"),
    path("tasks/<int:id>/", views.TaskDetailView.as_view(), name="task_detail"),
]
