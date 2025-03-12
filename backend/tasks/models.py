from django.db import models
from user.models import User

class UserTask(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
        ('REVOKED', 'Revoked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255)
    label = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    result = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task_name} ({self.task_id}) - {self.status}"
