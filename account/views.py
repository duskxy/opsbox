from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,Permission
from django.shortcuts import HttpResponse
from .serializers import UserSerializer,GroupSerializer,PermissionSerializer
from .models import User
from utils.baseviews import BaseView
import json

# Create your views here.

User = get_user_model()
def get_user_info(request):
    udata = {}
    if request.method == "GET":
        token = request.GET.get('token')
        if token:
            token_user = jwt_decode_handler(token)
            user_id = token_user['user_id']
            data = User.objects.get(pk=user_id)

            udata = {
                "name": data.username,
                "user_id": data.id,
                "avator": "https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png",
                "access": ["super_admin"]
                # "access": ["super_admin"] if data.is_superuser else []
            }
    return HttpResponse(json.dumps(udata))

class UserViewSet(BaseView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ('username','email')

class GroupViewSet(BaseView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    search_fields = ('name',)

class PermissionViewSet(ListModelMixin,GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()