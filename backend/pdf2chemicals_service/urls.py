from django.urls import path
from .views import (
    PDFUploadView,
    PDF2ChemicalsTaskRevokeView
)

urlpatterns = [
    path('submit/', PDFUploadView.as_view(), name='pdf2chemicals-submit'),
    path('revoke/<str:task_id>/', PDF2ChemicalsTaskRevokeView.as_view, 'revoke-pdf2chemicals-task')
]