from import_export_extensions.api.views import ExportJobViewSet as BaseExportJobViewSet

from exports.models import ExportJob
from exports.serializers import ExportJobSerializer

# Create your views here.
class ExportJobViewSet(BaseExportJobViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportJobSerializer
    
    def get_export_resource_kwargs(self) -> dict[str, any]:
        # passes the authenticated user to the resource,
        # which in turn will be used to populate created_by
        return {'created_by': self.request.user}