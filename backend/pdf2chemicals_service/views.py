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

from celery.result import AsyncResult

from tasks.models import UserTask

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
        
@extend_schema(
    responses={
        200: OpenApiResponse(description="Task revocation requested successfully."),
        403: OpenApiResponse(description="Unauthorized - task does not belong to user."),
        404: OpenApiResponse(description="Task not found."),
        500: OpenApiResponse(description="Error revoking task.")
    }
)
class PDF2ChemicalsTaskRevokeView(APIView):
    """
    API view to revoke a running PDF2Chemicals task.
    
    Handles task revocation by:
    1. Verifying task ownership (authorization)
    2. Marking task as revoked in database
    3. Sending abort signal to Celery worker
    4. Triggering resource cleanup
    
    Permissions:
        - IsAuthenticated: User must be logged in
        - User must own the task (verified via UserTask.user)
    
    Example:
        POST /api/pdf2chemicals/revoke/abc-123-def/
        Authorization: Bearer <token>
        
        Response (200):
        {
            "status": "revocation requested",
            "task_id": "abc-123-def",
            "message": "Task will be aborted and resources cleaned up"
        }
        
        Response (403):
        {
            "error": "Unauthorized - task does not belong to you"
        }
        
        Response (404):
        {
            "error": "Task not found"
        }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, task_id, *args, **kwargs):
        """
        Revoke a running PDF2Chemicals task.
        
        Steps:
        1. Fetch UserTask from database using task_id
        2. Verify authorization (task.user == request.user)
        3. Check if already revoked (idempotent)
        4. Mark UserTask.is_revoked = True in database
        5. Send abort signal to Celery worker via AsyncResult.abort()
        6. Log the action for audit trail
        
        Request:
            POST /api/pdf2chemicals/revoke/{task_id}/
            Headers: Authorization: Bearer <token>
            
        Args:
            task_id (str): Celery task ID to revoke
        
        Returns:
            Response: JSON with status and message
        """
        try:
            # Step 1: Fetch task from database
            user_task = UserTask.objects.get(task_id=task_id)
            
            # Step 2: Authorization check
            if user_task.user != request.user:
                logger.warning(
                    f"Unauthorized revocation attempt: "
                    f"user {request.user.id} tried to revoke task {task_id} "
                    f"owned by {user_task.user.id}"
                )
                return Response(
                    {'error': 'Unauthorized - task does not belong to you'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Step 3: Idempotency check - allow multiple revoke requests
            if user_task.is_revoked:
                logger.info(
                    f"Task {task_id} already revoked, returning idempotent response"
                )
                return Response(
                    {
                        'status': 'already revoked',
                        'task_id': task_id,
                        'message': 'Task was already revoked'
                    },
                    status=status.HTTP_200_OK
                )
            
            # Step 4: Mark task as revoked in database
            user_task.is_revoked = True
            user_task.save()
            
            # Step 5: Send abort signal to Celery worker
            # Worker detects via is_aborted() in check_revocation()
            # Triggers cleanup_pdf2chemicals_resources task
            AsyncResult(task_id).abort()
            
            # Step 6: Log for audit trail
            logger.info(
                f"✓ Revocation requested for task {task_id} by user {request.user.id}"
            )
            
            return Response(
                {
                    'status': 'revocation requested',
                    'task_id': task_id,
                    'message': 'Task will be aborted and resources cleaned up'
                },
                status=status.HTTP_200_OK
            )
        
        except UserTask.DoesNotExist:
            logger.warning(
                f"Revocation attempt for non-existent task {task_id} "
                f"by user {request.user.id}"
            )
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            logger.error(
                f"Error revoking task {task_id} for user {request.user.id}: {e}",
                exc_info=True
            )
            return Response(
                {'error': f'Error revoking task: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )