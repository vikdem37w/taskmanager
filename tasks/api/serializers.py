from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    # STATUS_CHOICES = [
    #     ('pending', 'Pending'),
    #     ('in_progress', 'In Progress'),
    #     ('completed', 'Completed'),
    # ]
    # PRIORITY_CHOICES = [
    #     ('low', 'Low'),
    #     ('medium', 'Medium'),
    #     ('high', 'High'),
    # ]
    # user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)  #i madeth a little changeth overe here
    # title = models.CharField(max_length=255)
    # description = models.TextField(blank=True)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    # due_date = models.DateField(null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # user = serializers. #GOTTA FIND INFO ON MANYTOONE SERIALIZATION
    pass #PASS TO SHUT UP THE COMPILER