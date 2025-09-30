from rest_framework import serializers

from common.fields import RelativePathFileField

from .models import UserTask

class UserTaskSerializer(serializers.ModelSerializer):
    data_file = RelativePathFileField()
    
    class Meta:
        model = UserTask
        read_only_fields=[
            'id',
            'task_id',
            'concluded_at', 
            'created_at', 
            'update_at'
        ]
        fields = '__all__'

class RevokeTaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()