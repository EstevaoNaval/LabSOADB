from rest_framework.serializers import ModelSerializer
from .models import UserTask

class UserTaskSerializer(ModelSerializer):
    class Meta:
        model = UserTask
        read_only_fields=['task_id', 'task_name']
        fields = '__all__'