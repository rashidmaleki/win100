from django.shortcuts import render
from rest_framework import generics
from .serializers import DepartmansSerializer, TicketSaveSerializer, UserTicketsSerialiyer
from support.models import Departman, Ticket
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from accounts.v1.functions import check_user_status
# Create your views here.


class DepartmansViewSet(generics.ListAPIView):
    serializer_class = DepartmansSerializer
    queryset = Departman.objects.all()

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TicketSaveViewSet(generics.GenericAPIView):
    serializer_class = TicketSaveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = request.data['token']
            user = Token.objects.get(key=token).user
            departman = Departman.objects.get(id=request.data['departman'])
            ticket = Ticket.objects.create(
                user=user,
                departman=departman,
                subject=request.data['subject'],
                text=request.data['text']
            )
            ticket.save()
            return Response(
                {'Detail': {
                    "Success": True,
                    "Messege": "Ticket Sent!"
                }})
        else:
            raise ValidationError(serializer.errors)


class UserTicketsViewSet(generics.ListAPIView):
    serializer_class = UserTicketsSerialiyer

    def get_queryset(self):
        check_user_status(self.request.data['token'])
        token = self.request.data['token']
        user = Token.objects.get(key=token).user
        query = Ticket.objects.filter(user=user)
        return query

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
