from import_export_extensions.api.serializers import ExportJobSerializer as BaseExportJobSerializer

from exports.models import ExportJob

class ExportJobSerializer(BaseExportJobSerializer):
    class Meta(BaseExportJobSerializer.Meta):
        model = ExportJob