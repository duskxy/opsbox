from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class BasePagination(PageNumberPagination):
    page_size_query_param = 'pagesize'
    page_query_param = 'page'
    max_page_size = 1000

class DefaultPagination(BasePagination):
    page_size = 10

class BaseView(ModelViewSet):
    queryset = None
    serializer_class = None
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = [IsAuthenticated]
    # 分页
    pagination_class = DefaultPagination
    # 搜索
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = []
