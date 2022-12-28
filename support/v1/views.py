from django.shortcuts import render
from rest_framework import generics
from .serializers import DepartmansSerializer, TicketSaveSerializer, UserTicketsSerialiyer
from support.models import Departman, Ticket
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# Create your views here.


class DepartmansViewSet(generics.ListAPIView):
    serializer_class = DepartmansSerializer
    queryset = Departman.objects.all()


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
            return Response({
                "Success": True,
                "Messege": "Ticket sent!"
            })
        else:
            raise ValidationError(serializer.errors)


class UserTicketsViewSet(generics.ListAPIView):
    serializer_class = UserTicketsSerialiyer

    def get_queryset(self):
        token = self.request.data['token']
        user = Token.objects.get(key=token).user
        query = Ticket.objects.filter(user=user)
        return query
