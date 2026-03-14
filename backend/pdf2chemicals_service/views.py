import logging

from django.core.files.storage import default_storage

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pdf2chemicals_service.util.util import generate_random_alphanumeric_sequence
from pdf2chemicals_service.serializers import PDFSerializer
from pdf2chemicals_service.tasks import extract_and_save_chemicals_from_pdf
from tasks.models import UserTask

logger = logging.getLogger(__name__)

FILE_RANDOM_NAME_SIZE = 10
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@extend_schema(
    request=PDFSerializer,
    responses={
        202: OpenApiResponse(description="Files successfully enqueued for processing."),
        400: OpenApiResponse(description="Invalid request or file exceeds size limit."),
        500: OpenApiResponse(description="Error processing files."),
    },
)
class PDFUploadView(APIView):
    """
    Upload and enqueue PDF files for chemical extraction.

    Handles:
    1. File validation (size, format)
    2. Temporary file storage
    3. Celery task enqueueing
    4. UserTask database tracking
    5. Atomic cleanup on errors

    Permissions:
        - IsAuthenticated: User must be logged in

    Example Request:
        POST /api/pdf2chemicals/upload/
        Authorization: Bearer <token>
        Content-Type: multipart/form-data

        Form:
        - pdf_files: [file1.pdf, file2.pdf]
        - export_format: 'zip'
        - conf_format: ['3D']
        - structure_format: ['sdf']

    Example Response (202):
        {
            "message": "2 file(s) enqueued for processing.",
            "task_ids": [
                "550e8400-e29b-41d4-a716-446655440000",
                "550e8400-e29b-41d4-a716-446655440001"
            ],
            "count": 2
        }

    Example Response (400):
        {
            "error": "File document.pdf exceeds 50MB limit"
        }

    Example Response (500):
        {
            "error": "Error processing files: Database connection failed"
        }
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PDFSerializer

    def post(self, request, *args, **kwargs):
        """
        Upload and enqueue PDF files for chemical extraction.

        Process Flow:
        1. Validate request with PDFSerializer
        2. For each file:
            - Check file size
            - Save to temporary storage
            - Create UserTask record
            - Enqueue Celery task
        3. Return task_ids for frontend tracking
        4. On error: Cleanup files + database records

        Args:
            request: HTTP request with pdf_files and options

        Returns:
            202: Files enqueued (with task_ids)
            400: Invalid request or file size exceeded
            500: Processing error (files + DB cleaned up)
        """
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 1: Validate request data
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        serializer = PDFSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning(
                f"Invalid PDF upload from user {request.user.id}: "
                f"{serializer.errors}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        uploaded_files = serializer.validated_data.get("pdf_files", [])
        export_format = serializer.validated_data.get("export_format", "zip")
        conf_formats = list(serializer.validated_data.get("conf_format", []))
        structure_formats = list(serializer.validated_data.get("structure_format", []))

        user_id = request.user.id

        # Track created resources for cleanup on error
        temp_files = []
        created_task_ids = []

        try:
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # STEP 2: Process each uploaded file
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            for file in uploaded_files:
                original_filename = file.name

                # Validate file size (prevent abuse/storage exhaustion)
                if file.size > MAX_FILE_SIZE:
                    logger.warning(
                        f"File {original_filename} exceeds size limit "
                        f"({file.size} bytes > {MAX_FILE_SIZE} bytes) "
                        f"from user {user_id}"
                    )
                    return Response(
                        {"error": f"File {original_filename} exceeds 50MB limit"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Save file to temporary storage
                random_name = generate_random_alphanumeric_sequence(
                    FILE_RANDOM_NAME_SIZE
                )
                pdf_file_path = default_storage.save(
                    f"tmp_pdfs/{random_name}.pdf", file
                )
                temp_files.append(pdf_file_path)

                logger.info(
                    f"✓ PDF saved to temporary storage: {pdf_file_path} "
                    f"(user: {user_id}, file: {original_filename})"
                )

                # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                # STEP 3: Enqueue Celery task
                # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                result = extract_and_save_chemicals_from_pdf.delay(
                    user_id=user_id,
                    pdf_path=pdf_file_path,
                    original_filename=original_filename,
                    export_format=export_format,
                    conf_formats=conf_formats,
                    structure_formats=structure_formats,
                )

                # ✅ Use .id instead of .get() to avoid blocking
                task_id = result.id  # Returns immediately
                created_task_ids.append(str(task_id))

                logger.info(
                    f"✓ Celery task enqueued: {task_id} "
                    f"(file: {original_filename}, user: {user_id})"
                )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # STEP 4: All files processed successfully
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            logger.info(
                f"✓ PDF upload completed: {len(uploaded_files)} files "
                f"enqueued (user: {user_id})"
            )

            return Response(
                {
                    "message": f"{len(uploaded_files)} file(s) enqueued for processing.",
                    "task_ids": created_task_ids,
                    "count": len(uploaded_files),
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # STEP 5: Error handling - atomic cleanup
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            logger.error(
                f"Error processing PDF upload from user {user_id}: {e}", exc_info=True
            )

            # Cleanup: Remove temporary files
            for temp_file in temp_files:
                try:
                    if default_storage.exists(temp_file):
                        default_storage.delete(temp_file)
                        logger.info(f"✓ Cleaned up temporary file: {temp_file}")
                except Exception as cleanup_error:
                    logger.warning(
                        f"Failed to cleanup file {temp_file}: {cleanup_error}"
                    )

            # Cleanup: Remove UserTask database records (if any created)
            if created_task_ids:
                try:
                    deleted_count, _ = UserTask.objects.filter(
                        task_id__in=created_task_ids
                    ).delete()
                    logger.info(f"✓ Cleaned up {deleted_count} UserTask records")
                except Exception as db_error:
                    logger.warning(f"Failed to cleanup UserTask records: {db_error}")

            # Return error response to client
            return Response(
                {"error": f"Error processing files: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
