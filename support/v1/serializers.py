from django.contrib.auth import get_user_model
from rest_framework import serializers
from support.models import Departman, Ticket
from rest_framework.authtoken.models import Token

User = get_user_model()


class DepartmansSerializer(serializers.ModelSerializer):

    class Meta:
        model = Departman
        fields = ('id', 'name')


class TicketSaveSerializer(serializers.Serializer):
    token = serializers.CharField()
    departman = serializers.IntegerField()
    subject = serializers.CharField()
    text = serializers.CharField()


class UserTicketsSerialiyer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
