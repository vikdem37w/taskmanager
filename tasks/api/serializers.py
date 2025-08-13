from rest_framework import serializers
from django.contrib.auth.models import User

class TaskSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    status = serializers.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = serializers.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
