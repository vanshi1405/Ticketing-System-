import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ticketing_system.models import Ticket, TicketStausEnum, Project, LinkingUserToProject


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('created_date','updated_date','last_login','groups','date_joined')

    def validate(self, attrs):
        view = self.context.get('view')
        if view.action == "update":
            current_date_time = timezone.now()
            attrs['updated_date'] = current_date_time
        return attrs

    def create(self, validated_data):
        return super().create(validated_data=validated_data)
    
    def update(self, instance, validated_data):
        return super().update(validated_data=validated_data,instance=instance)

class TicketSerializers(serializers.ModelSerializer):
    assigned_user = serializers.CharField(source='assigned_to.first_name',read_only=True)
    ticket_status = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_date','updated_date',)

    def validate(self, attrs):
        view = self.context.get('view')
        if view.action == "update":
            current_date_time = timezone.now()
            attrs['updated_date'] = current_date_time
        return attrs

    def _get_user(self):
        return self.context['request'].user

    def get_ticket_status(self,instance):
        return TicketStausEnum(instance.status).name

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status != instance.status:
            user = self._get_user()
            if not user.is_superuser and status != TicketStausEnum.COMPLETED:
                raise Exception("currunt user only change ongoing status to completed  ")

        return super().update(validated_data=validated_data,instance=instance)

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.ListField(write_only=True,allow_null=True)
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_date','updated_date',)

    def get_assigned_users(self,instance):
        linking_users = instance.projects.all()
        users = []
        for linking_user in linking_users:
            users.append(linking_user.user.first_name)
        return users

    def validate(self, attrs):
        view = self.context.get('view')
        if view.action == "update":
            current_date_time = timezone.now()
            attrs['updated_date'] = current_date_time
        return attrs

    def create(self, validated_data):
        users = validated_data.pop('users')
        instance = super().create(validated_data=validated_data)
        linking_list = []
        if users is not None:
            users_objs = User.objects.filter(id__in=users)
            for obj in users_objs:
                linking_list.append(LinkingUserToProject(project=instance,
                                 user=obj))
            LinkingUserToProject.objects.bulk_create(objs=linking_list)

        return instance

    def update(self, instance, validated_data):
        users = validated_data.pop('users')
        instance = super().update(validated_data=validated_data,instance=instance)
        linking_list = []
        if users is not None:
            users_objs = User.objects.filter(id__in=users)
            for obj in users_objs:
                linking_list.append(LinkingUserToProject(project=instance,
                                                         user=obj))
            LinkingUserToProject.objects.bulk_create(objs=linking_list)

        return  instance


