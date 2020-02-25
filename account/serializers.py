from rest_framework import serializers
from django.contrib.auth.models import Group,Permission
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","role","leader","password","is_active","is_superuser",'groups')
    def getrule(self,instance):
        ruleList = {
            "id": instance.role,
            "rules": instance.get_role_display()
        }
        return  ruleList
    def to_representation(self, instance):
        ret = super(UserSerializer,self).to_representation(instance)
        if instance.leader:
            ret['leader'] = {
                "id" :instance.leader.id,
                "leaders": instance.leader.username}
        else:
            ret['leader'] ={
                "id": "",
                "leaders": ""
            }
        ret['role'] = self.getrule(instance)
        group_instance = instance.groups.first()
        ret['groups'] = {'id':group_instance.id, 'name':group_instance.name} if group_instance else {}
        return ret
    def create(self, validated_data):
        instance = super(UserSerializer,self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        if password != instance.password:
            instance.set_password(password)
        return super(UserSerializer,self).update(instance, validated_data)

class GroupSerializer(serializers.ModelSerializer):
    class Meta():
        model = Group
        fields = "__all__"

class PermissionSerializer(serializers.ModelSerializer):
    class Meta():
        model = Permission
        fields = ("id","name","codename")
