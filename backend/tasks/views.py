from celery import current_app

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from user.models import User
from .models import UserTask
from .serializers import UserTaskSerializer

class UserTaskReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    
    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(queryset=User, id=user_id)
        return UserTask.objects.filter(user=user)

class RevokeTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        task_id = request.data.get("task_id")
        
        if not task_id:
            return Response(data={"error": "task_id is a required attribute"}, status=400)
        
        user = User.objects.get(id=request.user.id)
        
        user_task = UserTask.objects.filter(user=user, task_id=task_id)
        
        if not user_task.exists():
            return Response(data={"message": "Task not found"}, status=404)
        
        current_app.control.revoke(task_id, terminate=True, signal='SIGKILL')
        user_task.update(status='REVOKED')
        
        return Response(status=200)
        
    
    