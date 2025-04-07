from rest_framework.serializers import ModelSerializer
from .models import UserTask

class UserTaskSerializer(ModelSerializer):
    class Meta:
        model = UserTask
        read_only_fields=['id','task_id', 'task_name']
        exclude = ['result']