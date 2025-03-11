from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import UserTask
from .serializers import UserTaskSerializer
# Create your views here.

class UserTaskReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field='user'