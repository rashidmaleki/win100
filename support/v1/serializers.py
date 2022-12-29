from django.contrib.auth import get_user_model
from rest_framework import serializers
from support.models import Departman, Ticket
from rest_framework.authtoken.models import Token
from accounts.v1.functions import check_user_status

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

    def validate(self, attrs):
        check_user_status(attrs['token'])
        return super().validate(attrs)


class UserTicketsSerialiyer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
