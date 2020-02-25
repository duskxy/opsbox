from rest_framework import serializers
from .models import Project,Web,Deploy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from .tasks import mail,codedeploy

User = get_user_model()
class ProjetcSerializer(serializers.ModelSerializer):
    class Meta():
        model = Project
        fields = "__all__"
    def to_resp_web(self,instance):
        result = []
        data = instance.web_set.all()
        for i in data:
            result.append({
                "id": i.id,
                "name": i.name
            })
        return  result
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["web"] = self.to_resp_web(instance)
        return ret

class WebSerializer(serializers.ModelSerializer):
    class Meta():
        model = Web
        fields = "__all__"
    def to_representation(self, instance):
        ret = super(WebSerializer,self).to_representation(instance)
        ret['projectname'] = {"id": instance.projectname.id,"name":instance.projectname.name } if instance.projectname else {}
        return ret

class DeploySerializer(serializers.ModelSerializer):
    applicant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta():
        model = Deploy
        fields = "__all__"
    def to_representation(self, instance):
        ret = super(DeploySerializer,self).to_representation(instance)
        ret["projectname"] = {
            "id": instance.projectname.id,
            "name": instance.projectname.name
        }
        ret["webname"] = {
            "id": instance.webname.id,
            "name": instance.webname.name
        }
        ret["applicant"] = {
            "id": instance.applicant.id,
            "name": instance.applicant.username
        }
        ret['reviewer'] = {"id": instance.reviewer.id, "name": instance.reviewer.username } if instance.reviewer else {}
        return ret
    def create(self, validated_data):
        user = self.context['request'].user
        admin = User.objects.get(is_superuser=True,username="admin")
        validated_data['reviewer'] = user.leader if user.leader else admin
        instance = super().create(validated_data)
        instance.save()
        mail.delay(instance.id,instance.applicant.username,instance.reviewer.email)
        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        status = int(validated_data['status'])
        group = user.groups.first()
        saemail =  [ i.email for i in Group.objects.get(name="SA").user_set.all()]
        instance = super().update(instance,validated_data)
        if status == 1:
            mail.delay(instance.id,instance.applicant.username,revie=",".join(saemail),statu=1)
        if status == 2:
            if group.name != "SA":
                raise PermissionDenied()
            codedeploy.delay(instance.id)
            mail.delay(instance.id,revie=instance.applicant.email,statu=2)
        return instance

