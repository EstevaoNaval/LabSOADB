from django.urls import path
from .views import (
    PDFUploadView,
    DownloadPDF2ChemicalsOutputFileView
)

urlpatterns = [
    path('submit/', PDFUploadView.as_view(), name='pdf2chemicals-submit'),
    path('result/<str:task_id>/', DownloadPDF2ChemicalsOutputFileView.as_view(), name='pdf2chemicals-result')
]