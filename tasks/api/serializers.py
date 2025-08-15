from rest_framework import serializers
from django.contrib.auth.models import User

class TaskSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    status = serializers.CharField(max_length=20, default='pending')
    priority = serializers.CharField(max_length=10, default='medium')
    due_date = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
