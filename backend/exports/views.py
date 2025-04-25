from import_export_extensions.api.views import BaseExportJobViewSet as BaseBaseExportJobViewSet
from exports.mixins import ExportStartActionMixin
from exports.models import ExportJob

class BaseExportJobViewSet(BaseBaseExportJobViewSet):
    queryset = ExportJob.objects.all()
    serializer_class = ExportStartActionMixin.export_detail_serializer_class

class ExportJobViewSet(BaseExportJobViewSet, ExportStartActionMixin):
    export_action_name = "start"
    export_action_url = "start"

    def get_queryset(self):
        """Filter export jobs by resource used in viewset."""
        if self.action == getattr(self, "export_action", ""):
            # To make it consistent and for better support of drf-spectacular
            return super().get_queryset()  # pragma: no cover
        return super().get_queryset().filter(
            resource_path=self.resource_class.class_path,
        )
    