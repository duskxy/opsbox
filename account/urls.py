from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserViewSet,GroupViewSet,PermissionViewSet,get_user_info

route = DefaultRouter()
route.register(r'user',UserViewSet,base_name="user")
route.register(r'group',GroupViewSet,base_name='group')
route.register(r'permission',PermissionViewSet,base_name='permission')

urlpatterns = [
    path(r'api/user/info/',get_user_info),
    path(r'api/',include(route.urls)),
    ]
