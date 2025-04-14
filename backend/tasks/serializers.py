from rest_framework import serializers
from .models import UserTask

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        read_only_fields=['id','task_id', 'task_name']
        exclude = ['result']

class RevokeTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()