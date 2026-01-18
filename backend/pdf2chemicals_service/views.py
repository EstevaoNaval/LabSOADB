import os
import logging

from django.core.files.storage import default_storage

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .util.util import generate_random_alphanumeric_sequence
from .serializers import PDFSerializer
from .tasks import (
    extract_and_save_chemicals_from_pdf
)

FILE_RANDOM_NAME_SIZE = 10

logger = logging.getLogger(__name__)

@extend_schema(
    responses={
        202: OpenApiResponse(description="Files enqueued for processing."),
        400: OpenApiResponse(description="Error validating the data sent.")
    }
)
class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PDFSerializer
    
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
                
                result = extract_and_save_chemicals_from_pdf.delay(
                    user_id=user_id, 
                    pdf_path=pdf_file_path,
                    original_filename=original_filename,
                    export_format=export_format,
                    conf_formats=conf_formats,
                    structure_formats=structure_formats
                )
                task_id = result.get()
            return Response(
                {"message": f"{len(uploaded_files)} files enqueued for processing."},
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            # Garantia de limpeza em caso de erro
            for temp_file in temp_files:
                default_storage.delete(temp_file)
            
            raise e