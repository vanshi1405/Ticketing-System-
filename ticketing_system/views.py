from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ticketing_system.models import Ticket
from ticketing_system.serializers import UserSerializers, TicketSerializers


class DashBoardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_user(self):
        return self.request.user

    @action(methods=['GET'],detail=False,url_name='all_tickets')
    def all_tickets(self,request):
        user = self._get_user()
        # filter ticket based on user if admin then show all tickets
        user_filter = {}
        if not user.is_superuser:
            user_filter['assigned_to']=user.id
        tickets = Ticket.objects.filter(**user_filter)
        serializer = TicketSerializers(tickets, many=True)
        return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # permission_classes = [IsAdminUser]


class TicketViewset(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializers
    # permission_classes = [IsAuthenticated]