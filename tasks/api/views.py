from rest_framework import viewsets
from tasks.models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("id")
    serializer_class = TaskSerializer
    filterset_fields = ["user", "title", "status", "priority", "due_date"]
    ordering_fields = ["title", "due_date", "id"]
    ordering = ["id"]
