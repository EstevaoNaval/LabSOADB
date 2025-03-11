from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserTaskReadOnlyViewSet

router = DefaultRouter()
router.register(r'', UserTaskReadOnlyViewSet, basename='user-task')

urlpatterns = [
    path('', include(router.urls)),
]