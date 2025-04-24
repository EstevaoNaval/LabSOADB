from import_export_extensions.api.views import ExportJobViewSet as BaseExportJobViewSet

from exports.models import ExportJob
from exports.serializers import ExportJobSerializer

# Create your views here.
class ExportJobViewSet(BaseExportJobViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportJobSerializer