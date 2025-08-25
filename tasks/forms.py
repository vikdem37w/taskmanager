from django import forms
from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }