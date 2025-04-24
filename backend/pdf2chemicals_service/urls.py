from django.urls import path
from .views import (
    PDFUploadView,
    DownloadPDF2ChemicalsOutputFileView
)

urlpatterns = [
    path('submit/', PDFUploadView.as_view(), name='pdf2chemicals-submit')
]