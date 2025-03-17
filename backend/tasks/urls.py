from django.urls import path
from .views import UserTaskReadOnlyViewSet, RevokeTaskAPIView

urlpatterns = [
    path('user/', UserTaskReadOnlyViewSet.as_view({'get': 'list'}), name="user-tasks"),
    path('revoke/', RevokeTaskAPIView.as_view(), name="revoke-task")
]