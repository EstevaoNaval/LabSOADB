from rest_framework import serializers
from .models import UserTask

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        read_only_fields=[
            'id',
            'task_id', 
            'task_name', 
            'concluded_at', 
            'created_at', 
            'update_at'
        ]

class RevokeTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()