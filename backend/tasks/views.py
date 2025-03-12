from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from user.models import User
from .models import UserTask
from .serializers import UserTaskSerializer

class UserTaskReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(queryset=User, id=user_id)
        return UserTask.objects.filter(user=user)
