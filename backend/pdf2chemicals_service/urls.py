from django.urls import path
from .views import (
    PDFUploadView
)

urlpatterns = [
    path('submit/', PDFUploadView.as_view(), name='pdf2chemicals-submit')
]