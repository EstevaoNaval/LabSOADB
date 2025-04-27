import django_filters

from tasks.models import UserTask


class UserTaskFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(field_name='status', choices=UserTask.TaskStatus)
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')
    
    
    class Meta:
        model = UserTask
        fields = []