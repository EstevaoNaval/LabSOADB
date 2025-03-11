from django.urls import path
from .views import UserTaskReadOnlyViewSet

urlpatterns = [
    path('user/<int:user_id>/', UserTaskReadOnlyViewSet.as_view({'get': 'list'}), name="user-tasks"),
]