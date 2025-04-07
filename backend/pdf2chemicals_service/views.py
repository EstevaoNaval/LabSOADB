import os

from django.core.files.storage import default_storage
from django.conf import settings
from django.http import FileResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from user.models import User
from tasks.models import UserTask

from .util.util import generate_random_alphanumeric_sequence
from .serializers import PDFSerializer
from .tasks import (
    extract_and_save_chemicals_from_pdf
)

FILE_RANDOM_NAME_SIZE = 10

class DownloadPDF2ChemicalsOutputFileView(APIView):
    MAP_FORMAT_TO_CONTENT_TYPE = {
        'zip': 'application/zip',
        'json': 'application/json'
    }
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id, *args, **kwargs):
        if not task_id:
            return Response(data={"error": "task_id is a required attribute"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(queryset=User, id=request.user.id)
        
        user_task = get_object_or_404(queryset=UserTask, task_id=task_id, user=user)
        
        if user_task.status in ('PENDING', 'RETRY'):
            return Response(data={"status": user_task.status}, status=status.HTTP_202_ACCEPTED)
        
        if user_task.status == 'REVOKED':
            return Response(data={"status": user_task.status}, status=status.HTTP_400_BAD_REQUEST)
        
        if user_task.status == 'FAILURE':
            return Response(data={"status": user_task.status}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not user_task.result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        export_format = user_task.result.get('format')
        output_abs_filepath = os.path.join(settings.MEDIA_ROOT, user_task.result.get('output_filepath'))
        
        with open(output_abs_filepath, mode='r+') as output_file:
            return FileResponse(
                output_file,
                filename=f'{task_id}.{export_format}',
                content_type=self.MAP_FORMAT_TO_CONTENT_TYPE[export_format], 
                as_attachment=True
            )      

# Create your views here.
class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = PDFSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_files = serializer.validated_data.get('pdf_files')
        export_format = serializer.validated_data.get('export_format', 'zip')
        conf_formats = list(serializer.validated_data.get('conf_format', []))
        structure_formats = list(serializer.validated_data.get('structure_format', []))
        
        user_id = request.user.id
        
        temp_files = []
        
        try:
            for file in uploaded_files:
                original_filename = file.name
                
                # Salva cada arquivo como temporário
                pdf_file_path = default_storage.save(f"tmp_pdfs/{generate_random_alphanumeric_sequence(FILE_RANDOM_NAME_SIZE)}.pdf", file)
                temp_files.append(pdf_file_path)
                
                extract_and_save_chemicals_from_pdf.delay(
                    user_id=user_id, 
                    pdf_path=pdf_file_path,
                    original_filename=original_filename,
                    export_format=export_format,
                    conf_formats=conf_formats,
                    structure_formats=structure_formats
                )
            return Response(
                {"message": f"{len(uploaded_files)} files enqueued for processing."},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            # Garantia de limpeza em caso de erro
            for temp_file in temp_files:
                default_storage.delete(temp_file)
            
            raise e
        
            