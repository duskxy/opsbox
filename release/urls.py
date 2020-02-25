from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ProjectViewSet,WebViewSet,TagListView,DeployViewSet

route = DefaultRouter()
route.register(r'project',ProjectViewSet,base_name="项目")
route.register(r'web',WebViewSet,base_name="WEB")
route.register(r'deploy',DeployViewSet,base_name="发布")

urlpatterns = [
    path(r'api/tag/info/',TagListView.as_view(),name="tag"),
    path(r'api/',include(route.urls)),
]