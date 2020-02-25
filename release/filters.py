import django_filters
from .models import Deploy


class DeployFilter(django_filters.rest_framework.FilterSet):
    """
    发布状态的过滤类
    """
    statusmin = django_filters.NumberFilter(field_name='status', help_text="最低价格",lookup_expr='lt')
    statusmax = django_filters.NumberFilter(field_name='status', lookup_expr='gte')

    class Meta:
        model = Deploy
        fields = ['statusmin', 'statusmax']