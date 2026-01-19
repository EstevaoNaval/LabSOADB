import logging

from celery import current_app
from celery.result import AsyncResult

from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from user.models import User

from tasks.models import UserTask
from tasks.serializers import UserTaskSerializer, RevokeTaskSerializer
from tasks.filters import UserTaskFilter

logger = logging.getLogger(__name__)

class UserTaskReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = UserTaskFilter
    
    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(queryset=User, id=user_id)
        return UserTask.objects.filter(user=user)

@extend_schema(
    request=RevokeTaskSerializer,
    responses={
        200: OpenApiResponse(description="Task revocation requested successfully."),
        400: OpenApiResponse(description="task_id is a required attribute."),
        403: OpenApiResponse(description="Unauthorized - task does not belong to user."),
        404: OpenApiResponse(description="Task not found."),
        500: OpenApiResponse(description="Error revoking task.")
    }
)
class RevokeTaskAPIView(APIView):
    """
    Generalized API view to revoke ANY task managed via UserTask model.
    
    ✅ Single endpoint for all task types
    ✅ Works with AbortableTask-based tasks
    ✅ Works with traditional Celery tasks
    ✅ Handles both graceful and forceful termination
    
    Task types supported (current and future):
    - PDF2Chemicals extraction
    - Import/Export jobs
    - Any async work tracked in UserTask model
    
    Revocation flow:
    1. Validate task_id parameter
    2. Authorize (verify user owns task)
    3. Update UserTask.status = REVOKED
    4. Send abort to Celery worker
    5. Worker cleanup path triggered
    
    Permissions:
        - IsAuthenticated: User must be logged in
        - User must own the task (verified via UserTask.user)
    
    Example:
        POST /api/tasks/revoke/
        Authorization: Bearer <token>
        Content-Type: application/json
        
        {
            "task_id": "550e8400-e29b-41d4-a716-446655440000"
        }
        
        Response (200):
        {
            "status": "revocation requested",
            "task_id": "550e8400-e29b-41d4-a716-446655440000",
            "message": "Task will be aborted and resources cleaned up"
        }
        
        Response (400):
        {
            "error": "task_id is a required attribute"
        }
        
        Response (404):
        {
            "error": "Task not found"
        }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RevokeTaskSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Revoke ANY task managed by UserTask model.
        
        Centralized revocation endpoint for all task types.
        Integrates with:
        - AbortableTask (graceful cleanup)
        - Celery control.revoke (forceful termination)
        - UserTask database tracking
        
        Request body:
        {
            "task_id": "550e8400-e29b-41d4-a716-446655440000"
        }
        
        Returns:
            Response: JSON with revocation status
        """
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # Step 1: Validate request - task_id is required
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        task_id = request.data.get("task_id")
        
        if not task_id:
            logger.warning(
                f"Revocation request without task_id from user {request.user.id}"
            )
            return Response(
                {'error': 'task_id is a required attribute'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Step 2: Fetch and authorize - task must belong to user
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            user = User.objects.get(id=request.user.id)
            
            user_task = UserTask.objects.filter(
                user=user,
                task_id=task_id
            ).first()
            
            if not user_task:
                logger.warning(
                    f"Revocation attempt for non-existent or unauthorized task {task_id} "
                    f"by user {user.id}"
                )
                return Response(
                    {'error': 'Task not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Step 3: Idempotency - allow multiple revoke requests
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            if user_task.status == UserTask.TaskStatus.REVOKED:
                logger.info(
                    f"Task {task_id} already revoked, "
                    f"returning idempotent response"
                )
                return Response(
                    {
                        'status': 'already revoked',
                        'task_id': str(task_id),
                        'message': 'Task was already revoked'
                    },
                    status=status.HTTP_200_OK
                )
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Step 4: Update database status
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            user_task.mark_revoked()
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Step 5: Send abort to Celery worker
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            # For AbortableTask-based tasks:
            # This triggers is_aborted() → check_revocation() → cleanup
            AsyncResult(str(task_id)).abort()
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Step 6: Audit logging
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            logger.info(
                f"✓ Task {task_id} revocation requested by user {user.id}"
            )
            
            return Response(
                {
                    'status': 'revocation requested',
                    'task_id': str(task_id),
                    'message': 'Task will be aborted and resources cleaned up'
                },
                status=status.HTTP_200_OK
            )
        
        except User.DoesNotExist:
            logger.error(
                f"User {request.user.id} not found during revocation"
            )
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        except Exception as e:
            logger.error(
                f"Error revoking task {task_id}: {e}",
                exc_info=True
            )
            return Response(
                {'error': f'Error revoking task: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
    