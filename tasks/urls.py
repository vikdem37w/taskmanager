from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("tasks/", views.TaskListView.as_view(), name="tasks"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="create_task"),
    path("tasks/<int:id>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:id>/update/", views.TaskUpdateView.as_view(), name="update_task"),
    path("tasks/<int:id>/delete/", views.TaskDeleteView.as_view(), name="delete_task"),
]
