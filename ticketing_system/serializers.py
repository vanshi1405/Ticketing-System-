import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ticketing_system.models import Ticket, TicketStausEnum


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
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_date','updated_date',)

    def _get_user(self):
        return self.request.user

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status != instance.status:
            user = self._get_user()
            if not user.is_superuser and status != TicketStausEnum.COMPLETED:
                raise Exception("currunt user only change ongoing status to completed  ")

        return super().update(validated_data=validated_data,instance=instance)