from django.views.generic import View
from django.http import HttpResponse
from rest_framework.permissions import DjangoModelPermissions,IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from utils.baseviews import BaseView
from utils.github_api import GithubApi
from .serializers import ProjetcSerializer,WebSerializer,DeploySerializer
from .models import Project,Web,Deploy
from .filters import DeployFilter
from .tasks import mail
import json
# Create your views here.

class TagListView(View):
    def get(self,request):
        web = request.GET.get("web")
        gitserver = GithubApi()
        taglist = gitserver.get_tag(web)
        return HttpResponse(json.dumps(taglist),content_type="application/json")

class ProjectViewSet(BaseView):
    serializer_class = ProjetcSerializer
    queryset = Project.objects.all()
    search_fields = ('name',)


class WebViewSet(BaseView):
    serializer_class = WebSerializer
    queryset = Web.objects.all()
    search_fields = ('name',)

class DeployViewSet(BaseView):
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    serializer_class = DeploySerializer
    queryset = Deploy.objects.all()
    filter_class = DeployFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        return self.queryset.filter(Q(applicant=user)|Q(reviewer=user))
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = 3
        mail.delay(obj.id,revie=obj.applicant.email,statu=3)
        obj.save()
        return Response(status=204)
